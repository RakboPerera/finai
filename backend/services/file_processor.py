"""SAP Excel file processing service."""
import pandas as pd
import uuid
import json
from pathlib import Path
from datetime import datetime
from config import UPLOAD_DIR, PROCESSED_DIR
from services.database import db
from services.store import store


class FileProcessor:
    SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv"}

    def process_upload(self, file_path: Path, original_filename: str) -> dict:
        upload_id = str(uuid.uuid4())[:8]
        ext = Path(original_filename).suffix.lower()

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {ext}. Supported: {self.SUPPORTED_EXTENSIONS}")

        sheets_data = {}
        total_rows = 0

        if ext == ".csv":
            df = pd.read_csv(file_path)
            df = self._clean_dataframe(df)
            sheets_data["Sheet1"] = df
            total_rows = len(df)
            db.store_dataframe(df, upload_id, original_filename, "Sheet1")
        else:
            xls = pd.ExcelFile(file_path)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df = self._clean_dataframe(df)
                if len(df) > 0:
                    sheets_data[sheet_name] = df
                    total_rows += len(df)
                    db.store_dataframe(df, upload_id, original_filename, sheet_name)

        # Store upload metadata
        metadata = {
            "upload_id": upload_id,
            "filename": original_filename,
            "sheets": list(sheets_data.keys()),
            "total_rows": total_rows,
            "columns": {name: list(df.columns) for name, df in sheets_data.items()},
            "status": "processed",
            "uploaded_at": datetime.now().isoformat()
        }
        store.append("uploads", metadata)

        # Save processed summary
        summary_path = PROCESSED_DIR / f"{upload_id}_summary.json"
        summary = self._generate_summary(sheets_data, original_filename)
        summary_path.write_text(json.dumps(summary, indent=2, default=str))

        return {
            "upload_id": upload_id,
            "filename": original_filename,
            "sheets": len(sheets_data),
            "total_rows": total_rows,
            "columns": {name: list(df.columns) for name, df in sheets_data.items()},
            "preview": {name: df.head(5).to_dict(orient="records") for name, df in sheets_data.items()},
            "status": "processed"
        }

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        # Drop fully empty rows/columns
        df = df.dropna(how="all").dropna(axis=1, how="all")
        # Replace NaN with None for JSON compatibility
        df = df.fillna("")
        # Strip whitespace from string columns
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip()
        # Clean column names
        df.columns = [str(c).strip().replace("\n", " ") for c in df.columns]
        return df

    def _generate_summary(self, sheets_data: dict, filename: str) -> dict:
        summary = {
            "filename": filename,
            "sheets": {}
        }
        for sheet_name, df in sheets_data.items():
            sheet_summary = {
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "numeric_columns": list(df.select_dtypes(include=["number"]).columns),
                "date_columns": list(df.select_dtypes(include=["datetime64"]).columns),
            }
            # Add numeric stats
            numeric_df = df.select_dtypes(include=["number"])
            if len(numeric_df.columns) > 0:
                sheet_summary["numeric_stats"] = numeric_df.describe().to_dict()
            summary["sheets"][sheet_name] = sheet_summary
        return summary

    def get_upload_data(self, upload_id: str) -> pd.DataFrame:
        return db.get_financial_data(upload_id)

    def get_upload_data_as_records(self, upload_id: str) -> list:
        df = db.get_financial_data(upload_id)
        if df.empty:
            return []
        records = []
        for _, row in df.iterrows():
            try:
                data = json.loads(row["data"]) if isinstance(row["data"], str) else row["data"]
                records.append(data)
            except (json.JSONDecodeError, TypeError):
                records.append({"raw": str(row["data"])})
        return records


file_processor = FileProcessor()
