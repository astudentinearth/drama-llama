from fastapi import FastAPI, Depends
from sqlalchemy import text
from db_config.database import init_db, get_db_context, drop_db
from routes import sessions_router
from routes.ai_actions import router as ai_router
from routes.graduation_project import router as graduation_project_router
from utils.auth import verify_api_key
import logging
import sys
import os

# Enable development mode for auto-reloading prompts
os.environ['DEBUG'] = 'true'

# Configure logging to show INFO level and above
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific loggers to INFO level
logging.getLogger('utils.ai.service').setLevel(logging.INFO)
logging.getLogger('uvicorn.access').setLevel(logging.WARNING)  # Reduce noise from access logs

app = FastAPI(
    title="Drama Llama AI Learning Career Platform",
    description="AI-powered learning platform with personalized roadmaps and materials",
    version="1.0.0"
)

# Include routers
app.include_router(sessions_router)
app.include_router(ai_router)
app.include_router(graduation_project_router)

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
def drop_db_endpoint(api_key: str = Depends(verify_api_key)):
    try:
        drop_db()
        return {"status": "ok", "database": "dropped"}
    except Exception as e:
        return {"status": "error", "database": "not dropped", "error": str(e)}
    return {"status": "error", "database": "not dropped", "error": "Database drop failed"}