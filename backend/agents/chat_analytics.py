"""Agent 6: Chat Analytics — Natural language Q&A on financial data."""
import json
from agents.base import BaseAgent
from services.database import db


class ChatAnalyticsAgent(BaseAgent):
    name = "chat_analytics"
    description = "Answers natural language questions about financial data"
    system_prompt = """You are a financial data analyst assistant for John Keells Holdings PLC. 
You answer questions about uploaded financial data conversationally and accurately.
When asked about numbers, always cite specific values from the data.
If you cannot find the answer in the provided data, say so clearly.
For complex queries, explain your reasoning step by step.
Format monetary values with appropriate currency symbols and thousands separators.

Respond with valid JSON: {answer: string, data_points: array, chart_suggestion: object|null, follow_up_questions: array}"""

    async def chat(self, upload_id: str, question: str, chat_history: list = None) -> dict:
        data_context = self._get_data_context(upload_id, limit=300)
        
        # Get prior analyses for richer context
        analysis_df = db.get_analysis_results(upload_id)
        analyses_context = ""
        if not analysis_df.empty:
            for _, row in analysis_df.iterrows():
                analyses_context += f"\n[{row['agent_name']}]: {str(row['result'])[:500]}\n"

        history_text = ""
        if chat_history:
            for msg in chat_history[-6:]:  # Last 6 messages for context
                history_text += f"\n{msg['role'].upper()}: {msg['content']}"

        prompt = f"""Based on this financial data, answer the user's question.

DATA CONTEXT:
{data_context}

ANALYSIS CONTEXT:
{analyses_context if analyses_context else "No prior analyses."}

CONVERSATION HISTORY:
{history_text if history_text else "No prior messages."}

USER QUESTION: {question}

Return JSON:
- answer: detailed answer string with specific numbers when available
- data_points: array of relevant data points cited
- chart_suggestion: {{type: "bar"|"line"|"pie", title: string, data: object}} or null
- follow_up_questions: array of 2-3 relevant follow-up questions the user might ask"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {
                "answer": result_text,
                "data_points": [],
                "chart_suggestion": None,
                "follow_up_questions": []
            }

        return result

    async def run(self, upload_id: str, context: dict = None) -> dict:
        question = context.get("question", "Summarize the key financial metrics") if context else "Summarize the key financial metrics"
        return await self.chat(upload_id, question)
