from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import RatingDomain


class RatingRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def create(self, rating: RatingDomain) -> RatingDomain:
        async with self.session_factory() as session:
            session.add(rating)
            await session.commit()
        return rating
