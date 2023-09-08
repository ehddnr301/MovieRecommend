from sqlalchemy import Column, Integer, String

from src.core import Base, TimestampMixin


class TagDomain(TimestampMixin, Base):
    __tablename__ = "tags"

    user_id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, primary_key=True)
    tag = Column(String)

    @classmethod
    def create(cls, user_id: int, movie_id: int, tag: str) -> "TagDomain":
        return cls(
            user_id=user_id,
            movie_id=movie_id,
            tag=tag,
        )
