"""
Bandit scanning service
"""
import subprocess
import json
import os

class BanditService:
    @staticmethod
    def scan_file(file_path):
        """
        Run Bandit scan on a Python file
        Returns: dict with scan results
        """
        try:
            # Run Bandit command
            result = subprocess.run(
                ['bandit', '-f', 'json', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse JSON output
            if result.stdout:
                report = json.loads(result.stdout)
                
                # Extract vulnerabilities
                vulnerabilities = report.get('results', [])
                
                # Count by severity
                severity_summary = {
                    'high': len([v for v in vulnerabilities if v.get('issue_severity') == 'HIGH']),
                    'medium': len([v for v in vulnerabilities if v.get('issue_severity') == 'MEDIUM']),
                    'low': len([v for v in vulnerabilities if v.get('issue_severity') == 'LOW'])
                }
                
                return {
                    'success': True,
                    'vulnerabilities': vulnerabilities,
                    'severity_summary': severity_summary,
                    'total_issues': len(vulnerabilities)
                }
            else:
                return {
                    'success': True,
                    'vulnerabilities': [],
                    'severity_summary': {'high': 0, 'medium': 0, 'low': 0},
                    'total_issues': 0
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Scan timeout exceeded'
            }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': 'Failed to parse Bandit output'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }