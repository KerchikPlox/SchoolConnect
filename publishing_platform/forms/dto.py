from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from publishing_platform.users.enums import *

__all__ = [
    "FormFAPI",
    "AddFormFAPI",
    "AddRelationFormToStudentFAPI",
    "UserAndFormRelationsFAPI",
    "UpdateFormFAPI",
]


class FormFAPI(BaseModel):

    id: UUID
    name: str


class AddFormFAPI(BaseModel):

    name: str


class UpdateFormFAPI(BaseModel):

    name: Optional[str]


class UserAndFormRelationsFAPI(BaseModel):

    user_id: UUID
    form_id: UUID
    role: Roles


class AddRelationFormToStudentFAPI(BaseModel):

    user_id: List[UUID]
    form_id: UUID
