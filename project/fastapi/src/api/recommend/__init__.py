from fastapi import APIRouter

from .recommend import recommend_router

sub_router = APIRouter()
sub_router.include_router(recommend_router, prefix="/recommend", tags=["Recommend"])


__all__ = ["sub_router"]
