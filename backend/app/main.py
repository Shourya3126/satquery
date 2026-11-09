from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(
    title="SatQuery AI",
    description="Agentic vision-language assistant for multimodal remote-sensing analysis.",
    version="0.1.0",
)

cors_origins = settings.cors_origins_list
allow_all = "*" in cors_origins or not cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else cors_origins,
    allow_credentials=not allow_all,
    allow_origin_regex=r"https?://.*" if allow_all else None,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {"name": "SatQuery AI", "demo_mode": settings.demo_mode, "docs": "/docs"}
