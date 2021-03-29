from typing import List

from fastapi import APIRouter, File, UploadFile, Depends, Path
from fastapi.responses import StreamingResponse

from uuid import UUID

import publishing_platform.tasks.service as tasks_service
import publishing_platform.attachments.service as attachment_service
from publishing_platform.tasks.dto import *

tasks_router = APIRouter()


__all__ = [
    "tasks_router",
]


@tasks_router.post("/create_task/")  # noqa
async def create_task(add_task_info: CreateTaskFAPI = Depends()):
    return await tasks_service.create_task(add_task_info)


@tasks_router.get("/get_all_tasks/")  # noqa
async def get_all_tasks() -> List[TaskFAPI]:
    return await tasks_service.get_all_tasks()


@tasks_router.get("/get_all_relations/")  # noqa
async def get_all_relations() -> List[TaskAndUserRelationFAPI]:
    return await tasks_service.get_all_relations()


@tasks_router.get("/get_all_relations_by_user_id/")  # noqa
async def get_all_relations(user_id: UUID) -> List[TaskAndUserRelationFAPI]:
    return await tasks_service.get_all_relations_by_user_id(user_id)


@tasks_router.put("/{task_id}", response_model=TaskFAPI)
async def update_task(task_id: UUID = Path(...), update_info = Depends(UpdateTaskFAPI)):
    return await tasks_service.update_task(update_info, task_id)


@tasks_router.delete("/delete_task/{task_id}")
async def delete_task(task_id: UUID):
    await tasks_service.delete_task(task_id)


@tasks_router.post("/create_file/{task_id}")
async def create_file_attachment(task_id: UUID, file: UploadFile = File(...)):
    await attachment_service.create_attachment(task_id, file)


@tasks_router.get("/get_file/{task_id}")
async def get_attachment_by_task(task_id: UUID):
    return await attachment_service.get_attachment_by_task(task_id)


@tasks_router.put("/update_file/{task_id}")
async def update_attachment_in_task(task_id: UUID, file: UploadFile = File(...)):
    await attachment_service.update_attachment(task_id, file)


@tasks_router.delete("/delete_attachment/{task_id}")
async def delete_attachment_by_task(task_id: UUID):
    await attachment_service.delete_attachment(task_id)
