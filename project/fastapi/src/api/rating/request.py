from pydantic import BaseModel


class CreateRatingRequest(BaseModel):
    user_id: int
    movie_id: int
    rating: float

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "rating": 3.0,
            }
        }
