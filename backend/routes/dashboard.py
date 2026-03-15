"""Dashboard overview and statistics routes."""
from fastapi import APIRouter
from services.database import db
from services.store import store

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats():
    """Get overview statistics for the dashboard."""
    uploads = store.find("uploads")
    total_uploads = len(uploads)
    total_rows = sum(u.get("total_rows", 0) for u in uploads)

    analysis_df = db.get_analysis_results()
    total_analyses = len(analysis_df) if not analysis_df.empty else 0

    chat_history = store.find("chat_history")
    total_chats = len(chat_history)

    recent_uploads = sorted(uploads, key=lambda x: x.get("_created_at", ""), reverse=True)[:5]

    return {
        "status": "success",
        "data": {
            "total_uploads": total_uploads,
            "total_rows": total_rows,
            "total_analyses": total_analyses,
            "total_chats": total_chats,
            "recent_uploads": recent_uploads,
            "agents_available": 7
        }
    }
