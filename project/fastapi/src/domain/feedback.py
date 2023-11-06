from sqlalchemy import Column, Integer, ARRAY, String

from src.core import Base, TimestampMixin


class FeedbackDomain(TimestampMixin, Base):
    __tablename__ = "feedbacks"

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    recommended_movie_id_list = Column(String)
    selected_movie_id = Column(Integer)
    score = Column(Integer)
    user_type = Column(String)
    action_cycle = Column(Integer)
