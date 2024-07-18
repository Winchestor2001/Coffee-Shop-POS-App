from fastapi.routing import APIRouter
from src.api.docs.views import router as docs_router
from src.settings import settings

api_router = APIRouter(prefix=settings.api.prefix)

api_router.include_router(docs_router)
