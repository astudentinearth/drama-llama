from typing import Union
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.schemas import ChatRequest
from utils.llm_tools import master
from db_config.database import init_db, get_db_context, drop_db, get_db
from routes import sessions_router

app = FastAPI(
    title="Drama Llama AI Learning Career Platform",
    description="AI-powered learning platform with personalized roadmaps and materials",
    version="1.0.0"
)

# Include routers
app.include_router(sessions_router)

@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint for conversational interactions.
    """
    # call master function
    return await master(request, db)

@app.get("/health")
def health_check():
    init_db()
    with get_db_context() as db:
        try:
            db.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected", "error": None}
        except Exception as e:
            return {"status": "error", "database": "not connected", "error": str(e)}
    return {"status": "error", "database": "not connected", "error": "Database connection failed"}

@app.get("/drop_db")
def drop_db_endpoint():
    try:
        drop_db()
        return {"status": "ok", "database": "dropped"}
    except Exception as e:
        return {"status": "error", "database": "not dropped", "error": str(e)}
    return {"status": "error", "database": "not dropped", "error": "Database drop failed"}