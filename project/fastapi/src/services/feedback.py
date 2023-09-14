from src.repositories import FeedbackRepository
from src.domain import FeedbackDomain


class FeedbackService:
    def __init__(self, feedback_repository: FeedbackRepository) -> None:
        self._repository: FeedbackRepository = feedback_repository

    async def create_feedback(
        self, user_id: int, recommended_movie_id_list: list[int], selected_movie_id: int
    ) -> FeedbackDomain:
        feedback = FeedbackDomain(
            user_id=user_id,
            recommended_movie_id_list=recommended_movie_id_list,
            selected_movie_id=selected_movie_id,
        )
        return await self._repository.create(feedback=feedback)
