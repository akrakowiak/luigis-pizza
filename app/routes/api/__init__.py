from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.routes.api.book import router as book_router
from app.routes.api.cart import router as cart_router
from app.routes.api.pizza import router as pizza_router
from app.routes.api.table import router as table_router

router = APIRouter(prefix="/api", tags=["api"], default_response_class=JSONResponse)
router.include_router(pizza_router)
router.include_router(cart_router)
router.include_router(table_router)
router.include_router(book_router)
