from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import TagDomain


class TagRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def create(self, tag: TagDomain) -> TagDomain:
        async with self.session_factory() as session:
            session.add(tag)
            await session.commit()
        return tag
