from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.config import get_settings
from src.auth import router as auth_router
from src.pii_routes import router as pii_router
from src.database import engine, Base
from src.models import User, SearchRequest, SearchSource

settings = get_settings()

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PII Scanner API",
    description="SaaS tool for discovering personal data exposure",
    version="0.1.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"] if settings.environment == "production" else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(pii_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}