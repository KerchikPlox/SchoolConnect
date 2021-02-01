import datetime
from typing import List
from uuid import uuid4

from fastapi import File, UploadFile, Depends, Path

from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.forms.models import UserAndFormRelationsORM
from publishing_platform.tasks.dto import *
from publishing_platform.tasks.models import *
from publishing_platform.users.enums import *
from publishing_platform.users.models import *
from publishing_platform.files.service import pin_file_to_task
from publishing_platform.tasks.models import *


__all__ = [
    "create_task",
    "get_all_tasks",
    "create_relations",
]


async def create_task(add_task_info: CreateTaskFAPI = Depends()):
    students_ids = [
        r.user_id
        for r in (
            await UserAndFormRelationsORM
                .query
                .where(UserAndFormRelationsORM.form_id == add_task_info.form_id)
                .where(UserAndFormRelationsORM.role == Roles.student)
                .gino.all()
        )
    ]
    users: List[User] = await User.query.where(User.id.in_(students_ids)).gino.all()

    content: bytes = await add_task_info.file.read()
    await add_task_info.file.close()

    task = await TaskORM.create(
        id=uuid4(),
        creator_id=add_task_info.creator_id,
        form_id=add_task_info.form_id,
        title=add_task_info.title,
        description=add_task_info.description,
        file=content,
        created_at=datetime.datetime.utcnow(),
    )
    await create_relations(users, task)


async def create_relations(users: List[User], task: TaskORM):
    for i in users:
        user = await User.query.where(User.id == i.id).gino.first_or_404()
        user_role = user.role
        await TaskAndUserRelationORM.create(
            user_id=user.id, task_id=task.id, role=user_role
        )


#async def update_task(update_info: UpdateTaskFAPI, task_id: UUID = Path(...)):
#    await TaskORM.update.values(**update_info.dict(exclude_unset=True)).where(TaskORM.id == task_id).gino.status()


async def get_all_tasks() -> List[TaskFAPI]:
    print([TaskFAPI(**u.to_dict()) for u in await TaskORM.query.gino.all()])
    return [TaskFAPI(**u.to_dict()) for u in await TaskORM.query.gino.all()]
