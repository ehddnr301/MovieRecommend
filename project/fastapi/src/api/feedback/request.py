from pydantic import BaseModel


class CreateFeedbackRequest(BaseModel):
    user_id: int
    recommended_movie_id_list: list[int]
    selected_movie_id: int
    user_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "recommended_movie_id_list": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "selected_movie_id": 1,
                "user_type": "A",
            }
        }
