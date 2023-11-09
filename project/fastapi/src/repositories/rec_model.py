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

    async def _get_movies_by_ids(self, movie_id_list):
        query = select(
            MovieDomain.movie_id,
            MovieDomain.title,
            MovieDomain.genres,
            MovieDomain.created_at,
        ).where(MovieDomain.movie_id.in_(movie_id_list))
        async with self.session_factory() as session:
            return (await session.execute(query)).all()

    async def create_prediction(self, user_id: int, movie_id_list: list):
        # fmt: off
        GENRES = ['(no genres listed)', 'Action', 'Adventure', 'Animation', 'Children',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
       'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
       'War', 'Western']
        # fmt: on

        movies = await self._get_movies_by_ids(movie_id_list)

        model = self._load_model(user_id)
        movies_df = pd.DataFrame(
            movies, columns=["movie_id", "title", "genres", "created_at"]
        )
        genres = movies_df["genres"].str.get_dummies(sep="|")

        for genre in GENRES:
            if genre not in genres.columns:
                genres[genre] = 0

        genres = genres[GENRES]

        movies_df[genres.columns] = genres
        movies_df["predict_rating"] = model.predict(movies_df[genres.columns])
        sorted_df = movies_df.sort_values(
            by=["predict_rating", "created_at"], ascending=[False, False]
        )
        top_10_movie_ids = sorted_df["movie_id"].head(9).tolist()

        return top_10_movie_ids
