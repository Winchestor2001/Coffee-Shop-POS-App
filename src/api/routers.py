from fastapi.routing import APIRouter
from src.settings import settings

from src.api.docs.views import router as docs_router
from src.api.user.views import router as user_router

api_router = APIRouter(prefix=settings.api.prefix)

api_router.include_router(docs_router)
api_router.include_router(user_router, prefix="/user", tags=['User'])
