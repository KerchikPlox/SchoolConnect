import os

import uvicorn

from publishing_platform.app import app as initial_app
from publishing_platform.constants import CONFIG
from publishing_platform.init_app import init_app

# uvicorn main:app --reload --port 8083 --host "0.0.0.0"
app = init_app(initial_app)


if __name__ == "__main__":
    uvicorn.run(app, **CONFIG["app"]["backend"], debug=os.environ.get("DEBUG", True), log_level="debug")
