from typing import List

from fastapi import APIRouter, File, UploadFile, Depends

import publishing_platform.tasks.service as tasks_service
from publishing_platform.tasks.dto import *

tasks_router = APIRouter()


__all__ = [
    "tasks_router",
]


@tasks_router.post("/create_task/")  # noqa
async def create_task(add_task_info: CreateTaskFAPI = Depends()):
    return await tasks_service.create_task(add_task_info)


@tasks_router.get("")  # noqa
async def get_all_tasks() -> List[TaskFAPI]:
    return await tasks_service.get_all_tasks()
