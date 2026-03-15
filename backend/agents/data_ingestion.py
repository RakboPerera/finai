"""Agent 1: Data Ingestion — Parses, cleans, and normalizes SAP Excel data."""
import json
from agents.base import BaseAgent


class DataIngestionAgent(BaseAgent):
    name = "data_ingestion"
    description = "Parses SAP Excel files, cleans and normalizes financial data"
    system_prompt = """You are a financial data ingestion specialist. Your job is to analyze uploaded financial data from SAP systems and:
1. Identify the type of financial data (P&L, Balance Sheet, Cash Flow, GL entries, etc.)
2. Map columns to standard financial categories
3. Identify data quality issues (missing values, inconsistent formats, duplicates)
4. Suggest data transformations needed
5. Create a clean data profile

Always respond with valid JSON containing: data_type, column_mapping, quality_issues, transformations, and profile."""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id)
        prompt = f"""Analyze this financial dataset uploaded from an SAP system:

{data_context}

Provide a complete data analysis in JSON format with these keys:
- data_type: string identifying the financial data type
- column_mapping: object mapping original columns to standard financial categories
- quality_score: number 0-100
- quality_issues: array of issues found
- transformations: array of recommended data cleaning steps
- profile: object with key statistics
- financial_periods: identified date ranges/periods in the data"""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            result = {"raw_analysis": result_text, "status": "parsed_as_text"}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
