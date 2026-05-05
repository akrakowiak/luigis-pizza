from fastapi import APIRouter

from app.routes.api import router as api_router
from app.routes.routes import router as main_router

router = APIRouter()
router.include_router(api_router)
router.include_router(main_router)
