from sqlalchemy import Column, Integer, ARRAY, String

from src.core import Base, TimestampMixin


class MovieDomain(TimestampMixin, Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(ARRAY(String()))

    @classmethod
    def create(cls, movie_id: int, title: str, genres: list[str]) -> "MovieDomain":
        return cls(
            movie_id=movie_id,
            title=title,
            genres=genres,
        )

    @classmethod
    def get_all_movies_id(cls):
        return cls.query.with_entities(cls.movie_id).all()
