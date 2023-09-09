from src.repositories import MovieRepository
from src.domain import MovieDomain


class MovieService:
    def __init__(self, movie_repository: MovieRepository) -> None:
        self._repository: MovieRepository = movie_repository

    async def create_movie(
        self, movie_id: int, title: str, genres: list[str]
    ) -> MovieDomain:
        movie = MovieDomain.create(movie_id=movie_id, title=title, genres=genres)
        return await self._repository.create(movie=movie)

    async def get_all_movies_id(self):
        return await self._repository.get_all_movies_id()
