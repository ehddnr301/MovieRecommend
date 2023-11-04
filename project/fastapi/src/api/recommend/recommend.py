from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, status

from src.containers import Container
from src.services import MovieService
from src.services import RecommendService

recommend_router = APIRouter()


@recommend_router.get("/v1", status_code=status.HTTP_200_OK)
@inject
async def get_movie_recommendations(
    user_id: int,
    recommend_service: RecommendService = Depends(Provide[Container.recommend_service]),
):
    return await recommend_service.get_random_recommendations()


@recommend_router.get("/v2", status_code=status.HTTP_200_OK)
@inject
def get_movie_recommendations2(
    user_id: int,
    recommend_service: RecommendService = Depends(Provide[Container.recommend_service]),
):
    return [1,2,3,4,5,6,7,8,9]
    # return recommend_service.get_model_recommendations(user_id)