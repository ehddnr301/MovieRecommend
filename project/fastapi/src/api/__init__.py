from fastapi import APIRouter

from .movie import sub_router as movie_router
from .rating import sub_router as rating_router
from .tag import sub_router as tag_router

router = APIRouter()
router.include_router(movie_router)
router.include_router(rating_router)
router.include_router(tag_router)

__all__ = ["router"]
