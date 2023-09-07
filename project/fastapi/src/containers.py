from dependency_injector import containers, providers

from src.core import Database, Config
from src.repositories import MovieRepository
from src.services import MovieService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".api.movie.movie"])

    db = providers.Singleton(Database, db_url=Config.DB_URL)

    print(db.provided.session)

    movie_repository = providers.Factory(
        MovieRepository,
        session_factory=db.provided.session,
    )

    movie_service = providers.Factory(
        MovieService,
        movie_repository=movie_repository,
    )
