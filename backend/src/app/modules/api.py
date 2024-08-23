from fastapi import APIRouter

from src.app.modules.digest.router import router as digest_router
from src.app.modules.health.router import router as health_checking_router

api_router = APIRouter()
api_router.include_router(health_checking_router, prefix="/healthz")
api_router.include_router(digest_router, prefix="/digest")
