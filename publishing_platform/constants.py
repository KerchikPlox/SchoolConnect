import pathlib
import os

from publishing_platform.utils.configuration import init_config

__all__ = [
    "PROJECT_DIR",
    "DATA_DIR",
    "CONFIG",
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "JWT_EXP_DELTA_SECONDS",
    "BACKEND_DOMAIN"
]

CONFIG = init_config()
PROJECT_DIR = pathlib.Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"

JWT_SECRET = "5a6a80f5c776eb849bdfb58cdd33f1f74fe86923a7b0dd64816dc6313d18c27f"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 30

BACKEND_DOMAIN = os.environ.get("BACKEND_DOMAIN", "http://localhost:8085/%22")
