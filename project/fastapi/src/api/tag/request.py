from pydantic import BaseModel


class CreateTagRequest(BaseModel):
    user_id: int
    movie_id: int
    tag: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "tag": "funny",
            }
        }
