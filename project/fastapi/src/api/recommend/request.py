from pydantic import BaseModel


class GetMovieRecommendations(BaseModel):
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
            }
        }
