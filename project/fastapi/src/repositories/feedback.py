from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import FeedbackDomain


class FeedbackRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def create(self, feedback: FeedbackDomain) -> FeedbackDomain:
        async with self.session_factory() as session:
            session.add(feedback)
            await session.commit()
        return feedback
