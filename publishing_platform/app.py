from fastapi import FastAPI
from gino_starlette import Gino

from publishing_platform.constants import CONFIG

__all__ = [
    "app",
    "db",
]


app: FastAPI = FastAPI(title="Publishing platform", debug=True)

# app.mount("/static", StaticFiles(directory=PROJECT_DIR / "static"), name="static")

db = Gino(app, **CONFIG["gino"], pool_max_size=100, retry_limit=10, retry_interval=3)  # , echo=True
