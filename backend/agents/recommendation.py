"""Agent 7: Recommendation — Actionable financial insights and suggestions."""
import json
from agents.base import BaseAgent
from services.database import db


class RecommendationAgent(BaseAgent):
    name = "recommendation"
    description = "Generates actionable financial recommendations"
    system_prompt = """You are a senior financial advisor for John Keells Holdings PLC. Based on data analysis:
1. Provide actionable cost optimization recommendations
2. Identify revenue growth opportunities
3. Suggest cash flow improvements
4. Highlight compliance or risk mitigation steps
5. Prioritize recommendations by impact and effort

Rate each recommendation by: impact (1-10), effort (1-10), urgency (low/medium/high).
Always respond with valid JSON."""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id)

        # Gather all prior analyses
        analysis_df = db.get_analysis_results(upload_id)
        all_analyses = ""
        if not analysis_df.empty:
            for _, row in analysis_df.iterrows():
                all_analyses += f"\n--- {row['agent_name']} ---\n{str(row['result'])[:800]}\n"

        prompt = f"""Based on this financial data and all prior analyses, generate strategic recommendations:

DATA:
{data_context}

PRIOR ANALYSES:
{all_analyses if all_analyses else "No prior analyses available."}

Return JSON with:
- recommendations: array of {{
    title: string,
    description: string,
    category: "cost_optimization"|"revenue_growth"|"cash_flow"|"risk_mitigation"|"compliance",
    impact: number 1-10,
    effort: number 1-10,
    urgency: "low"|"medium"|"high",
    estimated_value: string (estimated financial impact),
    action_items: array of specific steps
  }}
- priority_matrix: object grouping recommendations by urgency
- quick_wins: array of top 3 low-effort high-impact items
- strategic_summary: string (2-3 paragraphs)"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_text, "status": "parsed_as_text"}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
