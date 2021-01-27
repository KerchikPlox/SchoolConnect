from fastapi import FastAPI

from publishing_platform.repo.setup_before_start import setup_tables_before_start, setup_admin_user
from publishing_platform.routes import init_routes
from publishing_platform.utils.cors import enable_cors
from publishing_platform.utils.extra_utils import make_dir_if_not_exists

__all__ = [
    "init_app",
]


def init_app(app: FastAPI) -> FastAPI:

    make_dir_if_not_exists("data")

    init_routes(app)
    enable_cors(app)

    app.add_event_handler("startup", setup_tables_before_start)
    app.add_event_handler("startup", setup_admin_user)

    return app
