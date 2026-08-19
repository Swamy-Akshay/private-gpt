from fastapi import APIRouter

from backend.app.api.routes.home import router as home_router
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.document import router as document_router


router = APIRouter()

router.include_router(home_router)
router.include_router(health_router)
router.include_router(chat_router)
router.include_router(document_router)