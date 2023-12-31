from fastapi import APIRouter

from .movie import movie_router

sub_router = APIRouter()
sub_router.include_router(movie_router, prefix="/movies", tags=["Movie"])


__all__ = ["sub_router"]
