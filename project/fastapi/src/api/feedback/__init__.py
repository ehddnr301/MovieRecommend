from fastapi import APIRouter

from .feedback import feedback_router

sub_router = APIRouter()
sub_router.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])


__all__ = ["sub_router"]
