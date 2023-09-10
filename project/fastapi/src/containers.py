from dependency_injector import containers, providers

from src.core import Database, Config
from src.repositories import (
    MovieRepository,
    RatingRepository,
    TagRepository,
    FeedbackRepository,
)
from src.services import MovieService, RatingService, TagService, FeedbackService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".api.movie.movie",
            ".api.rating.rating",
            ".api.tag.tag",
            ".api.feedback.feedback",
        ]
    )

    db = providers.Singleton(Database, db_url=Config.DB_URL)

    movie_repository = providers.Factory(
        MovieRepository,
        session_factory=db.provided.session,
    )

    movie_service = providers.Factory(
        MovieService,
        movie_repository=movie_repository,
    )

    rating_repository = providers.Factory(
        RatingRepository,
        session_factory=db.provided.session,
    )

    rating_service = providers.Factory(
        RatingService,
        rating_repository=rating_repository,
    )

    tag_repository = providers.Factory(
        TagRepository,
        session_factory=db.provided.session,
    )

    tag_service = providers.Factory(
        TagService,
        tag_repository=tag_repository,
    )

    feedback_repository = providers.Factory(
        FeedbackRepository,
        session_factory=db.provided.session,
    )

    feedback_service = providers.Factory(
        FeedbackService,
        feedback_repository=feedback_repository,
    )
