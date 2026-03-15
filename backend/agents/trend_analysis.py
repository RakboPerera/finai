"""Agent 3: Trend Analysis — Identifies financial trends and seasonality."""
import json
from agents.base import BaseAgent


class TrendAnalysisAgent(BaseAgent):
    name = "trend_analysis"
    description = "Identifies financial trends, seasonality, and growth patterns"
    system_prompt = """You are a financial trend analysis specialist. Analyze financial data to:
1. Identify revenue/expense trends over time
2. Detect seasonal patterns
3. Calculate growth rates (MoM, QoQ, YoY)
4. Identify inflection points and trend changes
5. Compare categories and segments

Always respond with valid JSON containing trend analysis results suitable for charting."""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id)
        prompt = f"""Perform trend analysis on this financial data:

{data_context}

Return JSON with:
- trends: array of {{metric, direction, strength, period, description}}
- growth_rates: object with calculated growth rates
- seasonality: array of seasonal patterns found
- inflection_points: array of significant changes
- chart_data: object with time_series data for ECharts visualization (labels, datasets)
- key_insights: array of 3-5 most important trend findings"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_text, "status": "parsed_as_text"}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
