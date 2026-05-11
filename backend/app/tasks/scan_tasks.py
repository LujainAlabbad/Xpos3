"""
Celery background tasks for vulnerability scanning.

These tasks allow the API to return immediately after a file upload
while the scan runs asynchronously in a worker process.
"""
from app import create_app, celery_app
from app.services.docker_service import DockerService
from app.services.llm_service import LLMService
from app.services.file_service import FileService


@celery_app.task(bind=True, name='scan_tasks.process_scan', max_retries=2)
def process_scan_task(self, scan_id: int, file_path: str):
    """
    Celery task: run a full Docker-isolated Bandit scan for an existing Scan record.

    Called by the upload route when async processing is preferred.
    The scan DB record must already exist with status='pending'.
    """
    app = create_app()
    with app.app_context():
        from app.extensions import db
        from app.models.scan import Scan

        scan = Scan.query.get(scan_id)
        if not scan:
            return {'error': f'Scan {scan_id} not found'}

        try:
            scan.status = 'scanning'
            db.session.commit()

            # Docker-isolated Bandit scan
            result = DockerService.run_bandit_scan(file_path)

            if result['success']:
                vulnerabilities = result['vulnerabilities']

                # LLM explanations (best-effort)
                llm_insights = {}
                if vulnerabilities:
                    try:
                        llm_insights = LLMService.generate_bulk_explanations(vulnerabilities)
                    except Exception as exc:
                        print(f"[Task {scan_id}] LLM skipped: {exc}")

                scan.status = 'completed'
                scan.bandit_report = {'results': vulnerabilities}
                scan.severity_summary = result['severity_summary']
                scan.llm_insights = llm_insights
            else:
                scan.status = 'failed'
                print(f"[Task {scan_id}] Scan failed: {result.get('error')}")

            db.session.commit()

        except Exception as exc:
            scan.status = 'failed'
            db.session.commit()
            print(f"[Task {scan_id}] Unhandled error: {exc}")
            raise self.retry(exc=exc, countdown=10)

        finally:
            FileService.delete_file(file_path)

        return {'scan_id': scan_id, 'status': scan.status}
