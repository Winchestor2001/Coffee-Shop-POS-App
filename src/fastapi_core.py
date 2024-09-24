from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.db.dependencies import db_helper
from src.logging_conf import setup_logger

APP_ROOT = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def mount_folders(app: FastAPI):
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "assets/static"),
        name="static",
    )
    app.mount("/media", StaticFiles(directory=Path("assets/media")), name="media")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Coffe Shop POS API",
        version="1.0.0",
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )

    mount_folders(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_logger()
    return app
