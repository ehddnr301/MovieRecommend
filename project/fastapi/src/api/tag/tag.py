from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.services import TagService

tag_router = APIRouter()


@tag_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_tag(
    user_id: int,
    movie_id: str,
    tag: str,
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    return await tag_service.create_tag(user_id, movie_id, tag)
