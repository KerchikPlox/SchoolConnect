from typing import List
from uuid import UUID

from fastapi import APIRouter, File, UploadFile, Form

import publishing_platform.files.service as files_service
from publishing_platform.files.dto import *

files_router = APIRouter()


__all__ = [
    "files_router"
]


@files_router.get("/{file_id}", response_model=List[FileFAPI]) # noqa
async def get_sent_file_by_id(user_id: UUID):
    return await files_service.get_sent_file_by_user_id(user_id)


@files_router.post("/send_file")
async def send_file(user_id: UUID = Form(...)):
    return await files_service.send_file(user_id)


@files_router.post("/", response_model=FileFAPI)
async def upload_file(user_id: UUID = Form(...), file: UploadFile = File(...)):
    return await files_service.send_file(user_id, file)
