#!/usr/bin/env python3
"""
Bandit scanner script — runs inside the Docker container.

IMPORTANT: This script always exits with code 0 so the Docker SDK
returns stdout normally. The caller uses the JSON 'success' field
(not the exit code) to detect failures.
"""
import sys
import json
import subprocess


def scan_file(file_path: str) -> dict:
    """Run bandit on a Python file and return the parsed JSON report."""
    result = subprocess.run(
        ['bandit', '-f', 'json', file_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    # Bandit exits 0 = no issues, 1 = issues found, 2 = error.
    # We always capture stdout regardless of exit code.
    if result.stdout:
        try:
            report = json.loads(result.stdout)
            report['_scanner_exit_code'] = result.returncode
            return report
        except json.JSONDecodeError as exc:
            return {
                'results': [],
                'success': False,
                'errors': [f'JSON parse error: {exc}'],
                '_scanner_exit_code': result.returncode,
            }

    # No stdout — bandit encountered a real error (e.g. file not found)
    return {
        'results': [],
        'success': False,
        'errors': [result.stderr.strip() or 'bandit produced no output'],
        '_scanner_exit_code': result.returncode,
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'success': False, 'error': 'Usage: bandit_scanner.py <file_path>'}))
        sys.exit(0)  # Always exit 0 so Docker SDK returns stdout

    report = scan_file(sys.argv[1])
    print(json.dumps(report))
    sys.exit(0)  # Always exit 0 — caller reads JSON, not exit code
