from fastapi import APIRouter

from .movie import sub_router as movie_router

router = APIRouter()
router.include_router(movie_router)

__all__ = ["router"]
