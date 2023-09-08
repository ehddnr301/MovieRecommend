from fastapi import APIRouter

from .rating import rating_router

sub_router = APIRouter()
sub_router.include_router(rating_router, prefix="/ratings", tags=["Rating"])


__all__ = ["sub_router"]
