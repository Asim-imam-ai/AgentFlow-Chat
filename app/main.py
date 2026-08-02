"""AgentFlow FastAPI Application Factory.

This module creates and configures the FastAPI application.
It exposes ONLY the REST API — no HTML templates, no static files.
The Streamlit frontend is a separate service (see docker/Dockerfile.frontend).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.events import register_event_handlers
from app.core.settings import settings
from exceptions import register_exception_handlers


def create_app() -> FastAPI:
    """FastAPI Application Factory.

    Returns a configured FastAPI application that exposes:
      - REST API endpoints under /api/*
      - Swagger UI at /docs
      - OpenAPI schema at /openapi.json
      - Health check at /api/health
      - Root status at / (JSON, not HTML)

    FastAPI does NOT serve any HTML, templates, or static files.
    All frontend traffic is handled by the Streamlit service.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        debug=settings.DEBUG,
        description=(
            "AgentFlow REST API. "
            "Frontend is served separately by Streamlit (port 8501). "
            "See /docs for the interactive API reference."
        ),
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    # In production, replace allow_origins=["*"] with your actual domain list.
    allowed_origins = (
        ["*"]
        if settings.DEBUG
        else [
            "http://localhost",
            "http://localhost:8501",
            "http://frontend:8501",
        ]
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Startup / Shutdown Lifecycle ──────────────────────────────────────────
    register_event_handlers(app)

    # ── Exception Handlers ────────────────────────────────────────────────────
    register_exception_handlers(app)

    # ── API Routes ────────────────────────────────────────────────────────────
    app.include_router(
        api_router,
        prefix=settings.API_PREFIX,
    )

    # ── Root Status (JSON only — NO HTML) ─────────────────────────────────────
    @app.get("/", include_in_schema=False, tags=["Status"])
    async def root():
        """API health/info endpoint.
        Returns JSON — never HTML. The frontend is Streamlit (separate service).
        """
        return {
            "service": "AgentFlow API",
            "status": "online",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/api/health",
        }

    return app


app = create_app()
