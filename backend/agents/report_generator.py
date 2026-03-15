"""Agent 5: Report Generator — Creates executive summaries and reports."""
import json
from agents.base import BaseAgent
from services.database import db


class ReportGeneratorAgent(BaseAgent):
    name = "report_generator"
    description = "Generates executive summaries and financial reports"
    system_prompt = """You are a financial report specialist for John Keells Holdings PLC. Create:
1. Executive summaries with key financial highlights
2. KPI dashboards data
3. Variance analysis reports
4. Period-over-period comparisons
5. Actionable bullet points for leadership

Write in a professional tone suitable for C-suite executives. Always respond with valid JSON."""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id)

        # Also fetch any existing analysis results
        analysis_df = db.get_analysis_results(upload_id)
        prior_analyses = ""
        if not analysis_df.empty:
            for _, row in analysis_df.iterrows():
                prior_analyses += f"\n--- {row['agent_name']} analysis ---\n{row['result']}\n"

        prompt = f"""Generate an executive financial report based on this data and prior analyses:

DATA:
{data_context}

PRIOR AGENT ANALYSES:
{prior_analyses if prior_analyses else "No prior analyses available."}

Return JSON with:
- executive_summary: string (2-3 paragraph executive overview)
- kpis: array of {{name, value, change, change_pct, status}} (status: up/down/stable)
- highlights: array of key findings (top 5)
- concerns: array of areas needing attention
- recommendations: array of actionable items
- report_sections: array of {{title, content}} for full report"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_text, "status": "parsed_as_text"}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
