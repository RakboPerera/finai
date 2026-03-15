"""DuckDB database service for financial data storage and querying."""
import duckdb
import pandas as pd
from pathlib import Path
from config import DUCKDB_PATH


class DuckDBService:
    def __init__(self):
        self.db_path = DUCKDB_PATH
        self._init_db()

    def _get_conn(self):
        return duckdb.connect(self.db_path)

    def _init_db(self):
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS financial_data (
                id INTEGER,
                upload_id VARCHAR,
                file_name VARCHAR,
                sheet_name VARCHAR,
                data JSON,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER,
                upload_id VARCHAR,
                agent_name VARCHAR,
                result JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE SEQUENCE IF NOT EXISTS financial_data_seq START 1
        """)
        conn.execute("""
            CREATE SEQUENCE IF NOT EXISTS analysis_results_seq START 1
        """)
        conn.close()

    def store_dataframe(self, df: pd.DataFrame, upload_id: str, file_name: str, sheet_name: str):
        conn = self._get_conn()
        records = df.to_dict(orient="records")
        import json
        for record in records:
            conn.execute(
                "INSERT INTO financial_data (id, upload_id, file_name, sheet_name, data) VALUES (nextval('financial_data_seq'), ?, ?, ?, ?)",
                [upload_id, file_name, sheet_name, json.dumps(record, default=str)]
            )
        conn.close()
        return len(records)

    def store_analysis(self, upload_id: str, agent_name: str, result: dict):
        conn = self._get_conn()
        import json
        conn.execute(
            "INSERT INTO analysis_results (id, upload_id, agent_name, result) VALUES (nextval('analysis_results_seq'), ?, ?, ?)",
            [upload_id, agent_name, json.dumps(result, default=str)]
        )
        conn.close()

    def get_financial_data(self, upload_id: str = None, limit: int = 1000):
        conn = self._get_conn()
        if upload_id:
            result = conn.execute(
                "SELECT * FROM financial_data WHERE upload_id = ? ORDER BY id LIMIT ?",
                [upload_id, limit]
            ).fetchdf()
        else:
            result = conn.execute(
                "SELECT * FROM financial_data ORDER BY id DESC LIMIT ?", [limit]
            ).fetchdf()
        conn.close()
        return result

    def get_analysis_results(self, upload_id: str = None, agent_name: str = None):
        conn = self._get_conn()
        query = "SELECT * FROM analysis_results WHERE 1=1"
        params = []
        if upload_id:
            query += " AND upload_id = ?"
            params.append(upload_id)
        if agent_name:
            query += " AND agent_name = ?"
            params.append(agent_name)
        query += " ORDER BY created_at DESC"
        result = conn.execute(query, params).fetchdf()
        conn.close()
        return result

    def query(self, sql: str):
        """Execute arbitrary SQL for the chat analytics agent."""
        conn = self._get_conn()
        try:
            result = conn.execute(sql).fetchdf()
            conn.close()
            return result
        except Exception as e:
            conn.close()
            raise e

    def get_uploads_list(self):
        conn = self._get_conn()
        result = conn.execute("""
            SELECT DISTINCT upload_id, file_name, 
                   MIN(uploaded_at) as uploaded_at,
                   COUNT(*) as row_count
            FROM financial_data 
            GROUP BY upload_id, file_name 
            ORDER BY MIN(uploaded_at) DESC
        """).fetchdf()
        conn.close()
        return result

    def get_data_summary(self, upload_id: str):
        conn = self._get_conn()
        result = conn.execute("""
            SELECT file_name, sheet_name, COUNT(*) as rows,
                   MIN(uploaded_at) as first_upload
            FROM financial_data 
            WHERE upload_id = ?
            GROUP BY file_name, sheet_name
        """, [upload_id]).fetchdf()
        conn.close()
        return result


db = DuckDBService()
