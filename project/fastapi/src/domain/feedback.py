from sqlalchemy import Column, Integer, ARRAY

from src.core import Base, TimestampMixin


class FeedbackDomain(TimestampMixin, Base):
    __tablename__ = "feedbacks"

    recommend_id = Column(Integer, primary_key=True, autoincrement=True)
    recommended_movie_id_list = Column(ARRAY(Integer()))
    selected_movie_id = Column(Integer)
