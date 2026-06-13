from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.middleware.error_handler import register_exception_handlers
from api.routes import webhooks
from infrastructure.config.settings import get_settings
from infrastructure.observability.logging import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(title="GitHub PR Reviewer API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(webhooks.router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
