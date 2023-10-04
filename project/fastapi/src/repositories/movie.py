from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func

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

    async def get_all_movies_id(self):
        async with self.session_factory() as session:
            return (
                (
                    await session.execute(
                        select(MovieDomain.movie_id).order_by(MovieDomain.movie_id)
                    )
                )
                .scalars()
                .all()
            )

    async def get_last_movie_id(self):
        async with self.session_factory() as session:
            return (
                (
                    await session.execute(
                        select(MovieDomain.movie_id)
                        .order_by(MovieDomain.created_at.desc())
                        .limit(1)
                    )
                )
                .scalars()
                .first()
            )

    async def get_random_recommendations(self):
        async with self.session_factory() as session:
            return (
                (
                    await session.execute(
                        select(MovieDomain.movie_id).order_by(func.random()).limit(9)
                    )
                )
                .scalars()
                .all()
            )
