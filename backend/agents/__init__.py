"""Agent registry and orchestrator."""
from agents.data_ingestion import DataIngestionAgent
from agents.anomaly_detection import AnomalyDetectionAgent
from agents.trend_analysis import TrendAnalysisAgent
from agents.forecasting import ForecastingAgent
from agents.report_generator import ReportGeneratorAgent
from agents.chat_analytics import ChatAnalyticsAgent
from agents.recommendation import RecommendationAgent

# Registry of all agents
AGENTS = {
    "data_ingestion": DataIngestionAgent,
    "anomaly_detection": AnomalyDetectionAgent,
    "trend_analysis": TrendAnalysisAgent,
    "forecasting": ForecastingAgent,
    "report_generator": ReportGeneratorAgent,
    "chat_analytics": ChatAnalyticsAgent,
    "recommendation": RecommendationAgent,
}

# Pipeline order for full analysis
PIPELINE_ORDER = [
    "data_ingestion",
    "anomaly_detection",
    "trend_analysis",
    "forecasting",
    "report_generator",
    "recommendation",
]


async def run_pipeline(upload_id: str, agents_to_run: list = None) -> dict:
    """Run agents in sequence. Each agent builds on prior results."""
    agents_to_run = agents_to_run or PIPELINE_ORDER
    results = {}
    for agent_name in agents_to_run:
        if agent_name in AGENTS:
            agent = AGENTS[agent_name]()
            try:
                result = await agent.run(upload_id)
                results[agent_name] = {"status": "success", "result": result}
            except Exception as e:
                results[agent_name] = {"status": "error", "error": str(e)}
    return results


async def run_single_agent(agent_name: str, upload_id: str, context: dict = None) -> dict:
    if agent_name not in AGENTS:
        return {"error": f"Unknown agent: {agent_name}"}
    agent = AGENTS[agent_name]()
    return await agent.run(upload_id, context)
