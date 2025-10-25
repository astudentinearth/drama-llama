"""Main FastAPI application for caching service."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import cache_router
from services import embedding_service, qdrant_service
from ..ai.db_config.database import init_db

# Initialize database (create all tables)
init_db()
# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Gracefully handles connection failures and allows app to start.
    """
    # Startup
    logger.info("Starting caching service...")
    
    # Track initialization status
    embedding_loaded = False
    qdrant_connected = False
    
    try:
        # Load embedding model (critical - must succeed)
        logger.info("Loading embedding model...")
        embedding_service.load_model()
        embedding_loaded = True
        logger.info("✓ Embedding model loaded successfully")
        
    except Exception as e:
        logger.error(f"✗ Failed to load embedding model: {e}")
        logger.error("Cannot start service without embedding model")
        raise
    
    try:
        # Connect to Qdrant (non-critical - allow startup to continue)
        logger.info("Connecting to Qdrant...")
        qdrant_service.connect()
        qdrant_connected = True
        logger.info("✓ Qdrant connected successfully")
        
        # Create collection if not exists
        logger.info("Initializing collection...")
        qdrant_service.create_collection()
        logger.info("✓ Collection initialized successfully")
        
    except Exception as e:
        logger.warning(f"✗ Qdrant connection failed: {e}")
        logger.warning("Service will start but vector storage is unavailable")
        logger.warning("Check Qdrant configuration and connection settings")
        # Don't raise - allow app to start for health checks and troubleshooting
    
    if embedding_loaded and qdrant_connected:
        logger.info("🚀 Caching service started successfully (all systems operational)")
    elif embedding_loaded:
        logger.warning("⚠️  Caching service started with limited functionality (Qdrant unavailable)")
    
    yield
    
    # Shutdown
    logger.info("Shutting down caching service...")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Vector-based caching service for learning materials using Qdrant",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cache_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Caching Service",
        "version": settings.api_version,
        "status": "running"
    }


@app.get("/ping")
async def ping():
    """Simple ping endpoint for basic health checks."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False
    )

