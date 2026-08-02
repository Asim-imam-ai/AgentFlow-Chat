import logging
import os
from fastapi import FastAPI
from app.core.settings import settings
from app.core.logging import setup_logging
from app.database import Base, engine
from app.graph.factory import get_graph
from sqlalchemy import inspect

logger = logging.getLogger("agentflow.events")

def register_event_handlers(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        setup_logging()
        logger.info("Initializing AgentFlow Chat Server...")
        
        # Pre-build StateGraph compiled singleton
        logger.info("Pre-building and compiling Agent StateGraph...")
        get_graph()
        
        # Create uploads directory if it doesn't exist
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR)
            logger.info(f"Created upload directory: {settings.UPLOAD_DIR}")
            
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down AgentFlow Chat Server...")
        from app.graph.checkpoint import close_checkpointer_connection
        close_checkpointer_connection()
        logger.info("Checkpointer database connection closed.")
