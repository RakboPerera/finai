"""FinAI — Financial Intelligence Platform API Server."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data, analysis, chat, dashboard, insights
from config import HOST, PORT

app = FastAPI(
    title="FinAI API",
    description="Financial Intelligence Platform — John Keells Holdings PLC",
    version="1.0.0",
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(data.router)
app.include_router(analysis.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(insights.router)


@app.get("/")
async def root():
    return {
        "app": "FinAI",
        "version": "1.0.0",
        "description": "Financial Intelligence Platform",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
