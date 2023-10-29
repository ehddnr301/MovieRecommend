from pydantic import BaseModel


class CreateMovieRequest(BaseModel):
    movie_id: int
    title: str
    genres: str

    class Config:
        json_schema_extra = {
            "example": {
                "movie_id": 1,
                "title": "Toy Story (1995)",
                "genres": "Adventure|Children|Fantasy",
            }
        }
