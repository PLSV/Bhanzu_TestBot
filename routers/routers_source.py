from fastapi import APIRouter
from routers.practice_session_router import router as practice_router
from routers.practice_landing import router as practice_landing_router

router = APIRouter()
router.include_router(practice_router)
router.include_router(practice_landing_router)
