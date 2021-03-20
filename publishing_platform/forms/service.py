from typing import List
from uuid import uuid4, UUID

from fastapi import Path

from publishing_platform.forms.dto import *
from publishing_platform.forms.models import *
from publishing_platform.users.enums import *
from publishing_platform.users.models import *

__all__ = [
    "create_form"
]


async def create_form(add_form_info: AddFormFAPI):

    await FormORM.create(
        id=uuid4(), name=add_form_info.name
    )


async def get_forms_all() -> List[FormFAPI]:
    return [FormFAPI(**u.to_dict()) for u in await FormORM.query.gino.all()]


async def get_form_by_id(form_id: UUID) -> FormFAPI:
    form = await FormORM.query.where(FormORM.id == form_id).gino.first_or_404()
    return FormFAPI(**form.to_dict())


async def get_form_by_user_id(user_id: UUID) -> List[FormFAPI]:
    form_ids = [
        r.form_id
        for r in (
            await UserAndFormRelationsORM
                .query
                .where(UserAndFormRelationsORM.user_id == user_id)
                .gino.all()
        )
    ]

    forms: List[FormORM] = await (
        FormORM.query.where(FormORM.id.in_(form_ids)).gino.all()
    )

    print(FormORM.query.where(FormORM.id.in_(form_ids)))

    return forms


async def delete_form(form_id: UUID) -> None:
    form = await FormORM.query.where(FormORM.id == form_id).gino.first_or_404()
    relations_ids = [
        r.form_id
        for r in (
            await UserAndFormRelationsORM
                .query
                .where(UserAndFormRelationsORM.form_id == form_id)
                .gino.all()
        )
    ]
    relations: List[UserAndFormRelationsORM] = await (
        UserAndFormRelationsORM.query.where(UserAndFormRelationsORM.form_id.in_(relations_ids)).gino.all()
    )

    for i in relations:
        await i.delete()

    await form.delete()


async def update_form(update_form_info: UpdateFormFAPI, form_id: UUID = Path(...)):
    await FormORM.update.values(**update_form_info.dict(exclude_unset=True)).where(FormORM.id == form_id).gino.status()


async def get_all_realtions() -> List[UserAndFormRelationsFAPI]:
    return [UserAndFormRelationsFAPI(**u.to_dict()) for u in await UserAndFormRelationsORM.query.gino.all()]


async def get_relations_by_role(role: Roles) -> List[UserAndFormRelationsFAPI]:
    return [UserAndFormRelationsFAPI(**u.to_dict()) for u in await UserAndFormRelationsORM.query.where(UserAndFormRelationsORM.role == role).gino.all()]


async def get_relations_by_user_id(user_id: UUID) -> List[UserAndFormRelationsFAPI]:
    return [UserAndFormRelationsFAPI(**u.to_dict()) for u in await UserAndFormRelationsORM.query.where(UserAndFormRelationsORM.user_id == user_id).gino.all()]


async def create_relation_form_to_student(add_relation_info: AddRelationFormToStudentFAPI):
    for i in add_relation_info.user_id:
        user = await User.query.where(User.id == i).gino.first_or_404()
        user_role = user.role
        await UserAndFormRelationsORM.create(
            user_id=user.id, form_id=add_relation_info.form_id, role=user_role
        )