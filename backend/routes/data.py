"""File upload and data management routes."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from config import UPLOAD_DIR
from services.file_processor import file_processor
from services.database import db
from services.store import store

router = APIRouter(prefix="/api/data", tags=["data"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload an SAP Excel file for processing."""
    if not file.filename:
        raise HTTPException(400, "No filename provided")

    ext = Path(file.filename).suffix.lower()
    if ext not in {".xlsx", ".xls", ".csv"}:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    # Save uploaded file
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        result = file_processor.process_upload(save_path, file.filename)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")


@router.get("/uploads")
async def list_uploads():
    """List all uploaded files."""
    uploads = store.find("uploads")
    return {"status": "success", "data": uploads}


@router.get("/uploads/{upload_id}")
async def get_upload(upload_id: str):
    """Get details and preview for a specific upload."""
    meta = store.find_one("uploads", {"upload_id": upload_id})
    if not meta:
        raise HTTPException(404, "Upload not found")

    records = file_processor.get_upload_data_as_records(upload_id)
    summary = db.get_data_summary(upload_id)

    return {
        "status": "success",
        "data": {
            "metadata": meta,
            "summary": summary.to_dict(orient="records") if not summary.empty else [],
            "preview": records[:50],
            "total_rows": len(records)
        }
    }


@router.delete("/uploads/{upload_id}")
async def delete_upload(upload_id: str):
    """Delete an upload and its data."""
    store.delete("uploads", {"upload_id": upload_id})
    return {"status": "success", "message": f"Upload {upload_id} deleted"}
