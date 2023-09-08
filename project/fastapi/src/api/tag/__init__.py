from fastapi import APIRouter

from .tag import tag_router

sub_router = APIRouter()
sub_router.include_router(tag_router, prefix="/tags", tags=["Tag"])


__all__ = ["sub_router"]
