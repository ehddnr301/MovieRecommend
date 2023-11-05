import pandas as pd
from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import MovieDomain, RatingDomain
from sqlalchemy.future import select

import mlflow


class ModelRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    def _load_model(self, user_id: int):
        model = mlflow.sklearn.load_model(f"models:/rec_model_{user_id}/Production")
        return model

    async def _get_all_movies(self):
        query = select(MovieDomain.movie_id, MovieDomain.title, MovieDomain.genres)
        async with self.session_factory() as session:
            return (await session.execute(query)).all()

    async def create_prediction(self, user_id: int):
        movies = await self._get_all_movies()

        model = self._load_model(user_id)
        movies_df = pd.DataFrame(movies, columns=["movie_id", "title", "genres"])
        genres = movies_df["genres"].str.get_dummies(sep="|")

        movies_df[genres.columns] = genres
        movies_df["predict_rating"] = model.predict(movies_df[genres.columns])
        sorted_df = movies_df.sort_values(by=["predict_rating"], ascending=False)
        top_10_movie_ids = sorted_df["movie_id"].head(10).tolist()

        return top_10_movie_ids
