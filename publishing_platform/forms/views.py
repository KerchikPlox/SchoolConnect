from typing import List
from uuid import UUID

from fastapi import APIRouter

import publishing_platform.forms.service as forms_service
from publishing_platform.forms.dto import *
from publishing_platform.users.enums import *

forms_router = APIRouter()


__all__ = [
    "forms_router"
]


@forms_router.get("/all_forms", response_model=List[FormFAPI]) # noqa
async def get_forms_all():
    return await forms_service.get_forms_all()


@forms_router.post("/create_form")
async def create_form(add_form_info: AddFormFAPI):
    return await forms_service.create_form(add_form_info)


@forms_router.delete("/delete_{form_id}")
async def delete_user(form_id: UUID):
    await forms_service.delete_form(form_id)


@forms_router.get("/all_relations", response_model=List[UserAndFormRelationsFAPI]) # noqa
async def get_all_realtions():
    return await forms_service.get_all_realtions()


@forms_router.get("/relations_by_role", response_model=List[UserAndFormRelationsFAPI]) # noqa
async def get_relations_by_role(role: Roles):
    return await forms_service.get_relations_by_role(role)


@forms_router.post("/relation_form_to_student_{form_id}") # noqa
async def create_relation_form_to_student(add_relation_info: AddRelationFormToStudentFAPI):
    return await forms_service.create_relation_form_to_student(add_relation_info)
