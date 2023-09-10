from pydantic import BaseModel


class CreateFeedbackRequest(BaseModel):
    recommended_movie_id_list: list[int]
    selected_movie_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "recommended_movie_id_list": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "selected_movie_id": 1,
            }
        }
