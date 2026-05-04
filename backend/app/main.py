from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.routes.analyze import router as analyze_router
from app.routes.health import router as health_router
from app.routes.history import router as history_router
from app.routes.github import router as github_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Developer Review API",
    version="0.1.0",
    description="Minimal MVP backend for AI-assisted code review.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(history_router)
app.include_router(github_router)
