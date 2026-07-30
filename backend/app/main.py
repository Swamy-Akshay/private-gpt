from fastapi import FastAPI
from backend.app.api.router import router
from backend.app.core.config import settings
from backend.app.core.logger import setup_logger, logger
from backend.app.core.exceptions import register_exception_handlers
setup_logger()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(router)


@app.on_event("startup")
async def startup():
    logger.info("Private GPT server started successfully.")

register_exception_handlers(app)