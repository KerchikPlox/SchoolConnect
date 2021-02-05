import datetime
from typing import List
from uuid import uuid4
from io import BytesIO


from fastapi import File, UploadFile, Depends, Path
from fastapi.responses import StreamingResponse

from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.constants import BACKEND_DOMAIN, PROJECT_DIR

from publishing_platform.forms.models import UserAndFormRelationsORM
from publishing_platform.tasks.dto import *
from publishing_platform.attachments.models import *
from publishing_platform.users.enums import *
from publishing_platform.users.models import *
from publishing_platform.files.service import pin_file_to_task
from publishing_platform.tasks.models import *


__all__ = [
    "create_attachment",
    "get_attachment_by_task",
    "update_attachment",
    "delete_attachment"
]


async def create_attachment(task_id: UUID = Path(...), file: UploadFile = File(...)):

    content = await file.read()
    filename = file.filename
    media_type = file.content_type
    await file.close()

    file_url = rf"{BACKEND_DOMAIN}/api/tasks/files/{task_id}.updated"

    await AttachmentORM.create(
        id=uuid4(),
        task_id=task_id,
        file=content,
        filename=filename,
        media_type=media_type,
        created_at=datetime.datetime.utcnow()
    )

    await TaskORM.update.values(file_url=file_url).where(TaskORM.id == task_id).gino.status()


async def update_attachment(task_id: UUID = Path(...), file: UploadFile = File(...)):

    content = await file.read()
    filename = file.filename
    media_type = file.content_type
    await file.close()

    file_url = rf"{BACKEND_DOMAIN}/api/tasks/files/{task_id}.updated"

    await TaskORM.update.values(file_url=file_url).where(TaskORM.id == task_id).gino.status()
    await AttachmentORM.update.values(file=content, filename=filename, media_type=media_type).where(TaskORM.id == task_id).gino.status()


async def get_attachment_by_task(task_id: UUID):

    file = await (
        AttachmentORM.query.where(AttachmentORM.task_id == task_id)
        .gino.first_or_404()
    )

    uploaded_file = file.file

    path_to_file = rf"{PROJECT_DIR}/data/{uuid4().hex}"

    with open(file=path_to_file, mode="wb") as f:
        f.write(uploaded_file)

    return StreamingResponse(content=BytesIO(initial_bytes=uploaded_file),
                             media_type="text/plain;",
                             headers={"Content-Disposition": 'attachment; filename="test"'})


async def delete_attachment(task_id: UUID):
    file = await AttachmentORM.query.where(AttachmentORM.task_id == task_id).gino.first_or_404()
    await file.delete()
    await TaskORM.update.values(file_url=None).where(TaskORM.id == task_id).gino.status()
