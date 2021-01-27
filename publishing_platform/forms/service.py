from typing import List
from uuid import uuid4, UUID

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


async def delete_form(form_id: UUID) -> None:
    form = await FormORM.query.where(FormORM.id == form_id).gino.first_or_404()

    await form.delete()


async def get_all_realtions() -> List[UserAndFormRelationsFAPI]:
    return [UserAndFormRelationsFAPI(**u.to_dict()) for u in await UserAndFormRelationsORM.query.gino.all()]


async def get_relations_by_role(role: Roles) -> List[UserAndFormRelationsFAPI]:
    return [UserAndFormRelationsFAPI(**u.to_dict()) for u in await UserAndFormRelationsORM.query.where(UserAndFormRelationsORM.role == role).gino.all()]


async def create_relation_form_to_student(add_relation_info: AddRelationFormToStudentFAPI):
    for i in add_relation_info.user_id:
        user = await User.query.where(User.id == i).gino.first_or_404()
        user_role = user.role
        await UserAndFormRelationsORM.create(
            user_id=user.id, form_id=add_relation_info.form_id, role=user_role
        )