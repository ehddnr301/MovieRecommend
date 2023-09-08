from sqlalchemy import Column, Integer, String, Float

from src.core import Base, TimestampMixin


class RatingDomain(TimestampMixin, Base):
    __tablename__ = "ratings"

    user_id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, primary_key=True)
    rating = Column(Float)

    @classmethod
    def create(cls, user_id: int, movie_id: int, rating: float) -> "RatingDomain":
        return cls(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
        )
