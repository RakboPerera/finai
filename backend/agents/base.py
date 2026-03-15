"""Base agent class for all Claude AI agents."""
import json
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from services.database import db


class BaseAgent:
    name: str = "base"
    description: str = ""
    system_prompt: str = ""

    def __init__(self):
        import httpcore
        httpcore._sync.connection.SSL_CONTEXT = None
        import httpx
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY, http_client=httpx.Client(verify=False))

    async def run(self, upload_id: str, context: dict = None) -> dict:
        raise NotImplementedError

    def _call_claude(self, user_message: str, system: str = None) -> str:
        if not self.client:
            return json.dumps({"error": "ANTHROPIC_API_KEY not configured. Set it in .env file."})
        try:
            response = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4096,
                system=system or self.system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            text = response.content[0].text
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _get_data_context(self, upload_id: str, limit: int = 200) -> str:
        """Get financial data as context string for the agent."""
        df = db.get_financial_data(upload_id, limit=limit)
        if df.empty:
            return "No data found for this upload."
        records = []
        for _, row in df.iterrows():
            try:
                data = json.loads(row["data"]) if isinstance(row["data"], str) else row["data"]
                records.append(data)
            except (json.JSONDecodeError, TypeError):
                pass
        if not records:
            return "No parseable records found."
        import pandas as pd
        sample_df = pd.DataFrame(records[:50])
        context = f"Total records: {len(records)}\n"
        context += f"Columns: {list(sample_df.columns)}\n"
        context += f"Data types:\n{sample_df.dtypes.to_string()}\n\n"
        context += f"Sample data (first 20 rows):\n{sample_df.head(20).to_string()}\n"
        numeric = sample_df.select_dtypes(include=["number"])
        if len(numeric.columns) > 0:
            context += f"\nNumeric statistics:\n{numeric.describe().to_string()}"
        return context

    def _save_result(self, upload_id: str, result: dict):
        db.store_analysis(upload_id, self.name, result)
