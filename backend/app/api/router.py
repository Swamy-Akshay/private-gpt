from fastapi import APIRouter
from backend.app.api.routes.home import router as home_router
from backend.app.api.routes.health import router as health_router

router = APIRouter()

router.include_router(home_router)
router.include_router(health_router)