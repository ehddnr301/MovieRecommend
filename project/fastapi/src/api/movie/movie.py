from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.services import MovieService

from src.api.movie.request import CreateMovieRequest

movie_router = APIRouter()


@movie_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_movie(
    request: CreateMovieRequest,
    movie_service: MovieService = Depends(Provide[Container.movie_service]),
):
    return await movie_service.create_movie(**request.model_dump())
