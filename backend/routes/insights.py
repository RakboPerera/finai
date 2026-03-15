from fastapi import APIRouter, HTTPException
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
