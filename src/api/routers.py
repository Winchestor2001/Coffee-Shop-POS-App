from fastapi.routing import APIRouter
from src.settings import settings

from src.api.docs import router as docs_router
from src.api.user import router as user_router
from src.api.product import router as product_router

api_router = APIRouter(prefix=settings.api.prefix)

api_router.include_router(docs_router)
api_router.include_router(user_router, prefix="/user", tags=['User'])
api_router.include_router(product_router, prefix="/product", tags=['Product'])
