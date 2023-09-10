from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.services import FeedbackService

from .request import CreateFeedbackRequest

feedback_router = APIRouter()


@feedback_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_feedback(
    request: CreateFeedbackRequest,
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):
    return await feedback_service.create_feedback(**request.model_dump())
