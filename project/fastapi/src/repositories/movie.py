from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import MovieDomain


class MovieRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def create(self, movie: MovieDomain) -> MovieDomain:
        async with self.session_factory() as session:
            session.add(movie)
            await session.commit()
        return movie
