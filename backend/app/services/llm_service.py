"""
LLM service: generates beginner-friendly explanations and secure code
fixes for each Bandit finding, using a local Ollama model.

Falls back to a plain-text response when Ollama is unreachable, so
the rest of the scan pipeline continues uninterrupted.
"""
import os
import json
import requests


class LLMService:

    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma2:2b')

    # ── Public API ──────────────────────────────────────────────────────────

    @staticmethod
    def generate_bulk_explanations(vulnerabilities: list) -> dict:
        """
        Generate an explanation + fix for every vulnerability in a scan.

        Returns a dict keyed by "{test_id}_{index}" for easy frontend lookup.
        """
        explanations = {}
        for idx, vuln in enumerate(vulnerabilities):
            key = f"{vuln.get('test_id', 'unknown')}_{idx}"
            explanations[key] = LLMService.generate_explanation(vuln)
        return explanations

    @staticmethod
    def generate_explanation(vulnerability: dict) -> dict:
        """
        Call Ollama to explain a single vulnerability.
        Falls back to a static explanation when Ollama is unavailable.
        """
        prompt = LLMService._build_prompt(vulnerability)
        try:
            ollama_url = os.getenv('OLLAMA_URL', LLMService.OLLAMA_URL)
            model = os.getenv('OLLAMA_MODEL', LLMService.OLLAMA_MODEL)

            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 600,
                    }
                },
                timeout=60,
            )
            response.raise_for_status()

            raw_text = response.json().get('response', '')
            return LLMService._parse_response(raw_text, vulnerability)

        except requests.exceptions.ConnectionError:
            print("Ollama not reachable (is it running?) — using fallback")
            return LLMService._static_fallback(vulnerability)
        except Exception as exc:
            print(f"LLM error (using fallback): {exc}")
            return LLMService._static_fallback(vulnerability)

    # ── Helpers ─────────────────────────────────────────────────────────────

    @staticmethod
    def _build_prompt(vuln: dict) -> str:
        cwe = vuln.get('issue_cwe', {})
        cwe_id = cwe.get('id', 'N/A') if isinstance(cwe, dict) else cwe

        return f"""You are a security educator helping a beginner Python developer understand a code vulnerability.

Vulnerability details:
- Bandit Test ID : {vuln.get('test_id', 'N/A')}
- Issue          : {vuln.get('issue_text', 'N/A')}
- Severity       : {vuln.get('issue_severity', 'N/A')}
- Confidence     : {vuln.get('issue_confidence', 'N/A')}
- CWE            : {cwe_id}
- Code line      : {vuln.get('code', 'N/A')}
- Line number    : {vuln.get('line_number', 'N/A')}

Respond ONLY with valid JSON (no markdown fences, no extra text):
{{"explanation": "2-3 sentence plain-English explanation of what the vulnerability is and why it is dangerous", "secure_code_example": "short Python code snippet showing how to fix it"}}"""

    @staticmethod
    def _parse_response(raw_text: str, vulnerability: dict) -> dict:
        """Extract JSON from the model response; fallback if malformed."""
        text = raw_text.strip()

        # Strip markdown fences if the model added them anyway
        if text.startswith('```'):
            lines = text.splitlines()
            text = '\n'.join(
                line for line in lines
                if not line.startswith('```')
            ).strip()

        try:
            data = json.loads(text)
            if 'explanation' in data and 'secure_code_example' in data:
                return LLMService._clean_fields(data)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON object from somewhere inside the text
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            try:
                data = json.loads(text[start:end + 1])
                if 'explanation' in data and 'secure_code_example' in data:
                    return LLMService._clean_fields(data)
            except json.JSONDecodeError:
                pass

        # If parsing failed entirely, wrap the raw text as an explanation
        return {
            'explanation': text or LLMService._static_fallback(vulnerability)['explanation'],
            'secure_code_example': '# See explanation above for remediation guidance.',
        }

    @staticmethod
    def _clean_fields(data: dict) -> dict:
        """Strip markdown fences from secure_code_example if the model added them."""
        code = data.get('secure_code_example', '')
        if '```' in code:
            lines = code.splitlines()
            cleaned = [
                line for line in lines
                if not line.strip().startswith('```')
            ]
            data['secure_code_example'] = '\n'.join(cleaned).strip()
        return data

    @staticmethod
    def _static_fallback(vuln: dict) -> dict:
        issue = vuln.get('issue_text', 'Unknown vulnerability')
        test_id = vuln.get('test_id', '')
        return {
            'explanation': (
                f"{issue} "
                f"This was flagged by Bandit rule {test_id}. "
                "Review the highlighted line and consult the Bandit documentation for remediation guidance."
            ),
            'secure_code_example': '# Refer to https://bandit.readthedocs.io for fix examples.',
        }
