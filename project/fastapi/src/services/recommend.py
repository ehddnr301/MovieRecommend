from src.repositories import MovieRepository


class RecommendService:
    def __init__(self, movie_repository: MovieRepository) -> None:
        self._repository: MovieRepository = movie_repository

    async def get_random_recommendations(self):
        return await self._repository.get_random_recommendations()
