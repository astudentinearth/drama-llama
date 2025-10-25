from typing import Union
from fastapi import FastAPI
from sqlalchemy import text
from models.schemas import ChatRequest
from utils.llm_tools import master
from db_config.database import init_db, get_db_context
app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    # call master function
    return await master(request)

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