from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.services import RatingService

from src.api.rating.request import CreateRatingRequest

rating_router = APIRouter()


@rating_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_rating(
    request: CreateRatingRequest,
    rating_service: RatingService = Depends(Provide[Container.rating_service]),
):
    return await rating_service.create_rating(**request.model_dump())
