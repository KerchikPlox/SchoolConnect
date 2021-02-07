from fastapi import FastAPI
from gino_starlette import Gino
from fastapi.templating import Jinja2Templates

from publishing_platform.constants import CONFIG, PROJECT_DIR

__all__ = [
    "app",
    "db",
    "index_templates"
]


app: FastAPI = FastAPI(title="Publishing platform", debug=True)

index_templates = Jinja2Templates(directory=PROJECT_DIR / "templates/")

# app.mount("/static", StaticFiles(directory=PROJECT_DIR / "static"), name="static")

db = Gino(app, **CONFIG["gino"], pool_max_size=100, retry_limit=10, retry_interval=3)  # , echo=True
