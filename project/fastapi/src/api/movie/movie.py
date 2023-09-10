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


@movie_router.get("/last")
@inject
async def get_last_movie_id(
    movie_service: MovieService = Depends(Provide[Container.movie_service]),
):
    return await movie_service.get_last_movie_id()


@movie_router.get("/all")
@inject
async def get_all_movies_id(
    movie_service: MovieService = Depends(Provide[Container.movie_service]),
):
    return await movie_service.get_all_movies_id()
