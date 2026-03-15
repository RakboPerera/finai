"""Run this from the IAP folder to fix the insights files."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Fix 1: backend/routes/insights.py
insights_route = """from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.dashboard_builder import DashboardBuilderAgent
from services.database import db
from services.store import store
import json

router = APIRouter(prefix="/api/insights", tags=["insights"])


class InsightsRequest(BaseModel):
    upload_id: str


@router.post("/generate")
async def generate_dashboard(request: InsightsRequest):
    agent = DashboardBuilderAgent()
    try:
        result = await agent.run(request.upload_id)
        store.append("dashboards", {"upload_id": request.upload_id, "config": result})
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/dashboard/{upload_id}")
async def get_dashboard(upload_id: str):
    dashboards = store.find("dashboards", {"upload_id": upload_id})
    if dashboards:
        return {"status": "success", "data": dashboards[-1].get("config", {})}
    df = db.get_analysis_results(upload_id, "dashboard_builder")
    if not df.empty:
        row = df.iloc[0]
        result = row["result"]
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                pass
        return {"status": "success", "data": result}
    return {"status": "success", "data": None}
"""

p1 = os.path.join(BASE, "backend", "routes", "insights.py")
with open(p1, "w", encoding="utf-8") as f:
    f.write(insights_route)
print(f"[OK] Fixed {p1}")


# Fix 2: backend/agents/dashboard_builder.py
agent_code = '''import json
from agents.base import BaseAgent


class DashboardBuilderAgent(BaseAgent):
    name = "dashboard_builder"
    description = "Analyzes uploaded data and auto-configures interactive dashboards"
    system_prompt = (
        "You are an expert dashboard architect. Analyze financial data and generate "
        "a complete dashboard config as pure JSON with no markdown. The JSON must have: "
        "title (string), subtitle (string), kpis (array of objects with label, value, "
        "change like +12.5%, status as up/down/stable, icon as revenue/expense/profit/"
        "balance/growth/alert), charts (array with id, title, type as line/bar/pie/"
        "doughnut/area/stacked_bar/treemap/gauge, width as full/half/third, height as "
        "normal/tall/short, data with labels array and datasets array of objects with "
        "name/values/color, and insight string), and summary string. Use colors: "
        "#22d3ee #a78bfa #34d399 #fbbf24 #f87171 #60a5fa #fb923c. Generate 4-8 charts "
        "with real data values. Respond with ONLY valid JSON."
    )

    async def run(self, upload_id, context=None):
        data_context = self._get_data_context(upload_id, limit=500)
        prompt = (
            "Analyze this financial dataset and generate a dashboard JSON config "
            "with 4-6 KPIs and 4-8 mixed chart types using real numbers from the data. "
            "Respond with ONLY the JSON object, no markdown.\\n\\n"
            f"DATA:\\n{data_context}"
        )
        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            start = result_text.find("{")
            end = result_text.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    result = json.loads(result_text[start:end])
                except json.JSONDecodeError:
                    result = {"error": "Failed to parse", "raw": result_text[:500]}
            else:
                result = {"error": "Failed to parse", "raw": result_text[:500]}
        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
'''

p2 = os.path.join(BASE, "backend", "agents", "dashboard_builder.py")
with open(p2, "w", encoding="utf-8") as f:
    f.write(agent_code)
print(f"[OK] Fixed {p2}")

print("\\nDone! Restart the backend with: python main.py")
