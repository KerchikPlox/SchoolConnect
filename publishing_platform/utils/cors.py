from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from publishing_platform.constants import CONFIG

__all__ = [
    "enable_cors"
]


def enable_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CONFIG["cors"]["origins"],
        allow_credentials=True,
        allow_methods=["*"],
        expose_headers=["*"],
        allow_headers=["*"],  # language=regexp
        allow_origin_regex=r"https://.*\.newwheel\.org",
    )
