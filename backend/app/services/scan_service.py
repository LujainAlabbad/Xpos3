"""
Business logic for scan operations.

Every scan runs Bandit inside an isolated Docker container (DockerService).
LLM explanations are generated after the scan and stored alongside results.
"""
from app.models.scan import Scan
from app.extensions import db
from app.services.docker_service import DockerService
from app.services.llm_service import LLMService
from app.services.file_service import FileService


class ScanService:

    @staticmethod
    def create_scan(user_id: int, file) -> Scan:
        """
        Full scan pipeline:
          1. Validate & save the uploaded file
          2. Create a DB record (status=scanning)
          3. Run Bandit in an isolated Docker container
          4. Generate LLM explanations for each finding
          5. Update community statistics
          6. Persist results and return the Scan object
        """
        file_path = None
        scan = None

        try:
            # Step 1: validate & persist the upload
            FileService.validate_file(file)
            file_meta = FileService.save_file(file, upload_folder='uploads')
            file_path = file_meta['file_path']

            # Step 2: create DB record
            scan = Scan(
                user_id=user_id,
                filename=file_meta['original_name'],
                status='scanning',
            )
            db.session.add(scan)
            db.session.commit()
            print(f"[Scan {scan.id}] Created — file: {scan.filename}")

            # Step 3: Docker-isolated Bandit scan
            scan_result = DockerService.run_bandit_scan(file_path)

            if scan_result['success']:
                vulnerabilities = scan_result['vulnerabilities']

                # Step 4: LLM explanations (best-effort)
                llm_insights = {}
                if vulnerabilities:
                    try:
                        llm_insights = LLMService.generate_bulk_explanations(vulnerabilities)
                    except Exception as exc:
                        print(f"[Scan {scan.id}] LLM generation skipped: {exc}")

                scan.status = 'completed'
                scan.bandit_report = {'results': vulnerabilities}
                scan.severity_summary = scan_result['severity_summary']
                scan.llm_insights = llm_insights

                s = scan_result['severity_summary']
                print(
                    f"[Scan {scan.id}] Completed — "
                    f"{scan_result['total_issues']} issues  "
                    f"H:{s['high']} M:{s['medium']} L:{s['low']}"
                )

                # Step 5: update community stats
                try:
                    ScanService._update_community_stats(vulnerabilities)
                except Exception as exc:
                    print(f"[Scan {scan.id}] Community stats update skipped: {exc}")

            else:
                scan.status = 'failed'
                print(f"[Scan {scan.id}] Failed — {scan_result.get('error')}")

            db.session.commit()
            return scan

        except Exception as exc:
            db.session.rollback()
            if scan and scan.id:
                try:
                    scan.status = 'failed'
                    db.session.commit()
                except Exception:
                    pass
            print(f"[ScanService] Unhandled error: {exc}")
            raise

        finally:
            # Always clean up the temporary upload
            if file_path:
                FileService.delete_file(file_path)

    # ── Queries ──────────────────────────────────────────────────────────────

    @staticmethod
    def get_user_scans(user_id: int) -> list:
        """Retrieve all scans for a user, newest first."""
        return (
            Scan.query
            .filter_by(user_id=user_id)
            .order_by(Scan.created_at.desc())
            .all()
        )

    @staticmethod
    def get_scan_report(user_id: int, scan_id: int) -> dict:
        """Get detailed scan report; raises ValueError if not found/owned."""
        scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
        if not scan:
            raise ValueError('Scan not found')
        return {
            'scan': scan.to_dict(),
            'bandit_report': scan.bandit_report,
            'llm_insights': scan.llm_insights,
            'severity_summary': scan.severity_summary,
        }

    @staticmethod
    def get_scan_status(user_id: int, scan_id: int) -> dict:
        """Check scan progress status."""
        scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
        if not scan:
            raise ValueError('Scan not found')
        return {'status': scan.status}

    @staticmethod
    def delete_scan(user_id: int, scan_id: int) -> None:
        """Delete a scan record; raises ValueError if not found/owned."""
        scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
        if not scan:
            raise ValueError('Scan not found')
        db.session.delete(scan)
        db.session.commit()

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _update_community_stats(vulnerabilities: list) -> None:
        """Increment occurrence counters for each vulnerability type found."""
        from app.models.community_stats import CommunityStats

        for vuln in vulnerabilities:
            test_id = vuln.get('test_id', 'UNKNOWN')
            severity = vuln.get('issue_severity', 'LOW')

            stat = CommunityStats.query.filter_by(vulnerability_type=test_id).first()
            if stat:
                stat.occurrence_count += 1
            else:
                db.session.add(CommunityStats(
                    vulnerability_type=test_id,
                    severity=severity,
                    occurrence_count=1,
                ))

        db.session.commit()
