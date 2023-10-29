from src.repositories import FeedbackRepository
from src.domain import FeedbackDomain


class FeedbackService:
    def __init__(self, feedback_repository: FeedbackRepository) -> None:
        self._repository: FeedbackRepository = feedback_repository

    async def create_feedback(
        self,
        user_id: int,
        recommended_movie_id_list: list[int],
        selected_movie_id: int,
        score: int = 0,
    ) -> FeedbackDomain:
        max_length = len(recommended_movie_id_list)  # recommended_movie_id_list의 최대 길이

        if selected_movie_id in recommended_movie_id_list:
            raw_score = len(
                recommended_movie_id_list
            ) - recommended_movie_id_list.index(selected_movie_id)
            score = (raw_score / max_length) * 10

        recommended_movie_id_list = ",".join(
            [str(movie_id) for movie_id in recommended_movie_id_list]
        )
        feedback = FeedbackDomain(
            user_id=user_id,
            recommended_movie_id_list=recommended_movie_id_list,
            selected_movie_id=selected_movie_id,
            score=score,
        )
        return await self._repository.create(feedback=feedback)
