import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, validator

from fastapi import Form, File, UploadFile

from publishing_platform.repo.base_validators import datetime_validator
from publishing_platform.users.dto import *
from publishing_platform.users.enums import *

__all__ = [
    "TaskFAPI",
    "CreateTaskFAPI",
    "TaskAndUserRealationFAPI",
    "CreateTaskAndUserRealationFAPI",
]


class TaskFAPI(BaseModel):
    id: UUID
    creator_id: UUID
    form_id: UUID
    title: str
    description: str
    file: bytes
    created_at: datetime.datetime

    @validator("created_at", pre=True, always=True)
    def set_created_at(cls, var):  # noqa
        return datetime_validator(var)


class CreateTaskFAPI:
    def __init__(
        self,
        creator_id: UUID = Form(...),
        form_id: UUID = Form(...),
        title: str = Form(""),
        description: Optional[str] = Form(""),
        file: UploadFile = File(...)
    ):
        self.creator_id = creator_id
        self.form_id = form_id
        self.title = title
        self.description = description
        self.file = file


#class UpdateTaskFAPI:
#    def __init__(
#            self,
#            form_id: Optional[UUID] = Form(...),
#            title: Optional[str] = Form(""),
#            description: Optional[str] = Form(""),
#            file: Optional[UploadFile] = File(...)
#    ):
#        self.form_id = form_id
#        self.title = title
#        self.description = description
#        self.file = file


class TaskAndUserRealationFAPI(BaseModel):
    user_id: UUID
    task_id: UUID
    role: Roles


class CreateTaskAndUserRealationFAPI(BaseModel):
    user_id: List[UUID]
    task_id: UUID
