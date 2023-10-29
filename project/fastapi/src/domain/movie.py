from sqlalchemy import Column, Integer, ARRAY, String

from src.core import Base, TimestampMixin


class MovieDomain(TimestampMixin, Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String)
