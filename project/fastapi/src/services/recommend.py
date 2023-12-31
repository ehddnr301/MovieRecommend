from src.repositories import MovieRepository
from src.repositories import ModelRepository


class RecommendService:
    def __init__(
        self, movie_repository: MovieRepository, model_repository: ModelRepository
    ) -> None:
        self._repository: MovieRepository = movie_repository
        self._model_repository: ModelRepository = model_repository

    async def get_random_recommendations(self):
        return await self._repository.get_random_recommendations()

    async def get_model_recommendations(self, user_id: int):
        movie_id_list = await self._repository.get_random_recommendations()
        recommend_movie_ids = await self._model_repository.create_prediction(
            user_id, movie_id_list
        )

        return recommend_movie_ids
