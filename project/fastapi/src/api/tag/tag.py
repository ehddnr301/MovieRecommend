from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.services import TagService

from src.api.tag.request import CreateTagRequest

tag_router = APIRouter()


@tag_router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_tag(
    request: CreateTagRequest,
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    return await tag_service.create_tag(**request.model_dump())
