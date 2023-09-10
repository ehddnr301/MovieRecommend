import random

from fastapi import APIRouter, status

recommend_router = APIRouter()


@recommend_router.get("/", status_code=status.HTTP_201_CREATED)
def get_movie_recommendations(user_id: int):
    # TODO: Implement Recommend System
    recommend_movie_id_list = random.sample(range(1, 10001), 9)
    return recommend_movie_id_list
