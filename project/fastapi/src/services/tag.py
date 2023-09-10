from src.repositories import TagRepository
from src.domain import TagDomain


class TagService:
    def __init__(self, tag_repository: TagRepository) -> None:
        self._repository: TagRepository = tag_repository

    async def create_tag(self, user_id: int, movie_id: int, tag: str) -> TagDomain:
        tag = TagDomain(user_id=user_id, movie_id=movie_id, tag=tag)
        return await self._repository.create(tag=tag)
