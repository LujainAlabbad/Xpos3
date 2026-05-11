"""
Docker service: spawns an isolated Bandit container for every scan request.

Each scan gets a brand-new container that:
  - Has NO network access
  - Is limited to 256 MB RAM
  - Mounts the uploaded file as read-only
  - Is auto-removed after completion

Docker-in-Docker volume strategy
─────────────────────────────────
When the backend itself runs inside Docker Compose, bind-mounting a host
path does not work because the path (e.g. /app/uploads) exists only inside
the backend container, not on the real host.

Solution: share the named Docker volume that stores uploads
  • docker-compose mounts  uploads_data → /app/uploads  in the backend container
  • This service mounts the same volume  uploads_data → /code  in bandit containers
  • Both containers read the same files

When running manually on the host (not inside Docker), a regular bind-mount
of the uploads directory is used instead.
"""
import os
import json
import subprocess

try:
    import docker
    from docker.errors import ImageNotFound, ContainerError, DockerException
    DOCKER_SDK_AVAILABLE = True
except ImportError:
    DOCKER_SDK_AVAILABLE = False

# ── Constants ────────────────────────────────────────────────────────────────

_DOCKER_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'docker')
)
BANDIT_IMAGE = 'xpos3-bandit:latest'
MEMORY_LIMIT = '256m'
SCAN_TIMEOUT = 60  # seconds

# Are we running inside a Docker container?
IS_IN_DOCKER = os.path.exists('/.dockerenv')

# Named Docker volume that stores uploads (set via env var in docker-compose)
UPLOADS_VOLUME = os.getenv('UPLOADS_VOLUME_NAME', 'xpos3_uploads_data')


def _to_docker_path(windows_path: str) -> str:
    """Convert a Windows path to a Docker-compatible path (no-op on Linux)."""
    if os.name != 'nt':
        return windows_path
    p = windows_path.replace('\\', '/')
    if len(p) >= 2 and p[1] == ':':
        p = '/' + p[0].lower() + p[2:]
    return p


class DockerService:

    # ── Image management ────────────────────────────────────────────────────

    @staticmethod
    def _get_client():
        if not DOCKER_SDK_AVAILABLE:
            raise RuntimeError("docker SDK not installed. Run: pip install docker")
        try:
            client = docker.from_env()
            client.ping()
            return client
        except Exception as exc:
            raise RuntimeError(f"Docker daemon not reachable: {exc}") from exc

    @staticmethod
    def ensure_bandit_image(client):
        """Build xpos3-bandit:latest if it does not already exist."""
        try:
            client.images.get(BANDIT_IMAGE)
            return  # already built
        except ImageNotFound:
            pass
        print(f"[Docker] Building {BANDIT_IMAGE} from {_DOCKER_DIR} ...")
        client.images.build(
            path=_DOCKER_DIR,
            dockerfile='Dockerfile.bandit',
            tag=BANDIT_IMAGE,
            rm=True,
        )
        print(f"[Docker] Image {BANDIT_IMAGE} ready.")

    # ── Core scan method ────────────────────────────────────────────────────

    @staticmethod
    def run_bandit_scan(file_path: str) -> dict:
        """
        Run Bandit inside an isolated Docker container, with automatic
        fallback to a direct subprocess call when Docker is unavailable
        or the container scan fails.
        """
        if not DOCKER_SDK_AVAILABLE:
            print("[Docker] SDK missing — using direct subprocess scan")
            return DockerService._fallback_scan(file_path)

        try:
            result = DockerService._docker_scan(file_path)
            if not result.get('success') or result.get('_docker_error'):
                reason = result.get('error', 'unknown')
                print(f"[Docker] Container scan error ({reason}) — falling back to direct scan")
                return DockerService._fallback_scan(file_path)
            return result

        except Exception as exc:
            print(f"[Docker] Exception during container scan ({exc}) — falling back to direct scan")
            return DockerService._fallback_scan(file_path)

    @staticmethod
    def _docker_scan(file_path: str) -> dict:
        client = DockerService._get_client()
        DockerService.ensure_bandit_image(client)

        abs_path = os.path.abspath(file_path)
        filename = os.path.basename(abs_path)

        # ── Choose the right volume strategy ────────────────────────────────
        if IS_IN_DOCKER:
            # Running inside Docker Compose: share the named uploads volume.
            # The bandit container sees the same files at /code/<filename>.
            volumes = {UPLOADS_VOLUME: {'bind': '/code', 'mode': 'ro'}}
            print(f"[Docker] Mode=compose — volume={UPLOADS_VOLUME}, file={filename}")
        else:
            # Running on the host: bind-mount the uploads directory directly.
            host_dir = _to_docker_path(os.path.dirname(abs_path))
            volumes = {host_dir: {'bind': '/code', 'mode': 'ro'}}
            print(f"[Docker] Mode=host — bind={host_dir}, file={filename}")

        try:
            # bandit_scanner.py always exits 0, so containers.run() returns
            # stdout without raising ContainerError.
            raw_output = client.containers.run(
                image=BANDIT_IMAGE,
                command=f'/code/{filename}',
                volumes=volumes,
                mem_limit=MEMORY_LIMIT,
                network_disabled=True,
                remove=True,
                stdout=True,
                stderr=False,
            )

            output = raw_output.decode('utf-8') if isinstance(raw_output, bytes) else str(raw_output)
            print(f"[Docker] Output: {output[:300]}")
            return DockerService._parse_bandit_output(output)

        except ContainerError as exc:
            stderr = exc.stderr.decode('utf-8') if exc.stderr else str(exc)
            print(f"[Docker] ContainerError exit={exc.exit_status}: {stderr}")
            return {'success': False, '_docker_error': True, 'error': f'Container error: {stderr}'}

        except Exception as exc:
            print(f"[Docker] Run error: {exc}")
            return {'success': False, '_docker_error': True, 'error': str(exc)}

    @staticmethod
    def _fallback_scan(file_path: str) -> dict:
        """Direct subprocess call to bandit — used when Docker is unavailable."""
        print(f"[Fallback] Running bandit directly on: {file_path}")
        try:
            result = subprocess.run(
                ['bandit', '-f', 'json', file_path],
                capture_output=True,
                text=True,
                timeout=SCAN_TIMEOUT,
            )
            print(f"[Fallback] bandit exit={result.returncode}, output_len={len(result.stdout)}")
            return DockerService._parse_bandit_output(result.stdout)
        except FileNotFoundError:
            return {'success': False, 'error': 'bandit is not installed'}
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timed out'}
        except Exception as exc:
            return {'success': False, 'error': str(exc)}

    # ── Parsing ──────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_bandit_output(output: str) -> dict:
        if not output or not output.strip():
            return {
                'success': False,
                '_docker_error': True,
                'error': 'Bandit produced no output (possible mount failure)',
            }
        try:
            report = json.loads(output)
        except json.JSONDecodeError as exc:
            return {'success': False, 'error': f'Failed to parse Bandit output: {exc}'}

        # bandit_scanner.py signals internal errors via the 'errors' key
        if report.get('errors') and not report.get('results'):
            return {
                'success': False,
                '_docker_error': True,
                'error': f"Scanner error: {report['errors']}",
            }

        vulnerabilities = report.get('results', [])
        summary = {
            'high':   sum(1 for v in vulnerabilities if v.get('issue_severity') == 'HIGH'),
            'medium': sum(1 for v in vulnerabilities if v.get('issue_severity') == 'MEDIUM'),
            'low':    sum(1 for v in vulnerabilities if v.get('issue_severity') == 'LOW'),
        }

        return {
            'success': True,
            'vulnerabilities': vulnerabilities,
            'severity_summary': summary,
            'total_issues': len(vulnerabilities),
        }
