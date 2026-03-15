"""Agent 4: Forecasting — Revenue/expense predictions."""
import json
from agents.base import BaseAgent


class ForecastingAgent(BaseAgent):
    name = "forecasting"
    description = "Generates financial forecasts and predictions"
    system_prompt = """You are a financial forecasting specialist. Based on historical data:
1. Project revenue and expenses for next 3-6 months
2. Provide confidence intervals for predictions
3. Identify key assumptions in the forecast
4. Create scenario analysis (optimistic, base, pessimistic)
5. Generate forecast data suitable for charting

Always respond with valid JSON containing forecast results."""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id)
        prompt = f"""Generate financial forecasts based on this historical data:

{data_context}

Return JSON with:
- forecast: object with {{periods: array, base_case: array, optimistic: array, pessimistic: array}}
- assumptions: array of key assumptions
- confidence_level: number 0-100
- risk_factors: array of factors that could impact the forecast
- chart_data: object with forecast visualization data for ECharts (labels, actual, forecast_base, forecast_optimistic, forecast_pessimistic)
- summary: string executive summary of the forecast"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_text, "status": "parsed_as_text"}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
