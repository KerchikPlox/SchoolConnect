import datetime
from typing import List
from uuid import uuid4, UUID

from fastapi import File, UploadFile, Form

from publishing_platform.files.dto import *
from publishing_platform.files.models import *
from publishing_platform.users.models import *

__all__ = [
    "pin_file_to_task",
    "get_sent_file_by_user_id",
    "create_file"
]


async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


async def get_sent_file_by_user_id(user_id: UUID) -> List[FileFAPI]:
    return [FileFAPI(**u.to_dict()) for u in await SendFilesORM.query.where(SendFilesORM.user_id == user_id).gino.all()]


async def pin_file_to_task(file: UploadFile = File(...)):
    content: bytes = await file.read()
    await file.close()
    return content

