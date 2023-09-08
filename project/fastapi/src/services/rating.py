from src.repositories import RatingRepository
from src.domain import RatingDomain


class RatingService:
    def __init__(self, rating_repository: RatingRepository) -> None:
        self._repository: RatingRepository = rating_repository

    async def create_rating(
        self, user_id: int, movie_id: int, rating: float
    ) -> RatingDomain:
        rating = RatingDomain.create(user_id=user_id, movie_id=movie_id, rating=rating)
        return await self._repository.create(rating=rating)
