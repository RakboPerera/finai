"""AI Agent analysis routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents import AGENTS, PIPELINE_ORDER, run_pipeline, run_single_agent
from services.database import db

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


class AgentRequest(BaseModel):
    upload_id: str
    context: Optional[dict] = None


class PipelineRequest(BaseModel):
    upload_id: str
    agents: Optional[list] = None


@router.get("/agents")
async def list_agents():
    """List all available AI agents."""
    agents = []
    for name, cls in AGENTS.items():
        agent = cls()
        agents.append({
            "name": name,
            "description": agent.description,
            "is_pipeline": name in PIPELINE_ORDER,
        })
    return {"status": "success", "data": agents}


@router.post("/run/{agent_name}")
async def run_agent(agent_name: str, request: AgentRequest):
    """Run a specific AI agent on uploaded data."""
    if agent_name not in AGENTS:
        raise HTTPException(404, f"Agent '{agent_name}' not found")

    try:
        result = await run_single_agent(agent_name, request.upload_id, request.context)
        return {"status": "success", "agent": agent_name, "data": result}
    except Exception as e:
        raise HTTPException(500, f"Agent error: {str(e)}")


@router.post("/pipeline")
async def run_analysis_pipeline(request: PipelineRequest):
    """Run the full analysis pipeline (or selected agents)."""
    try:
        results = await run_pipeline(request.upload_id, request.agents)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(500, f"Pipeline error: {str(e)}")


@router.get("/results/{upload_id}")
async def get_results(upload_id: str, agent_name: str = None):
    """Get analysis results for an upload."""
    df = db.get_analysis_results(upload_id, agent_name)
    if df.empty:
        return {"status": "success", "data": []}

    import json
    results = []
    for _, row in df.iterrows():
        result_data = row["result"]
        if isinstance(result_data, str):
            try:
                result_data = json.loads(result_data)
            except json.JSONDecodeError:
                pass
        results.append({
            "agent_name": row["agent_name"],
            "result": result_data,
            "created_at": str(row["created_at"])
        })
    return {"status": "success", "data": results}
