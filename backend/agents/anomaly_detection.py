"""Agent 2: Anomaly Detection — Flags unusual transactions and patterns."""
import json
from agents.base import BaseAgent


class AnomalyDetectionAgent(BaseAgent):
    name = "anomaly_detection"
    description = "Detects anomalies, outliers, and unusual patterns in financial data"
    system_prompt = """You are a financial anomaly detection specialist. Analyze financial data to:
1. Identify statistical outliers in transaction amounts
2. Detect unusual patterns (sudden spikes, drops, irregular timing)
3. Flag potential duplicate entries
4. Identify transactions outside normal business patterns
5. Rate severity of each anomaly (low/medium/high/critical)

Always respond with valid JSON containing: anomalies array, summary, risk_score."""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id)
        prompt = f"""Analyze this financial data for anomalies and irregularities:

{data_context}

Return JSON with:
- anomalies: array of objects with {{description, severity, affected_rows, category, recommendation}}
- summary: string overview of findings
- risk_score: number 0-100 (0=no risk, 100=critical)
- patterns: array of unusual patterns detected
- chart_data: object with data suitable for visualization (categories and counts)"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_text, "status": "parsed_as_text"}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
