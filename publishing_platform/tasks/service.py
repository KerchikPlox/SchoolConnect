import datetime
from typing import List
from uuid import uuid4


from fastapi import File, UploadFile, Depends, Path

from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.forms.models import UserAndFormRelationsORM
from publishing_platform.attachments.models import AttachmentORM
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
                .gino.all()
        )
    ]
    users: List[User] = await User.query.where(User.id.in_(students_ids)).gino.all()

    task = await TaskORM.create(
        id=uuid4(),
        creator_id=add_task_info.creator_id,
        form_id=add_task_info.form_id,
        title=add_task_info.title,
        description=add_task_info.description,
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


async def get_all_relations() -> List[TaskAndUserRelationFAPI]:
    return [TaskAndUserRelationFAPI(**u.to_dict()) for u in await TaskAndUserRelationORM.query.gino.all()]


async def get_all_relations_by_user_id(user_id: UUID) -> List[TaskAndUserRelationFAPI]:
    task_ids = [
        r.task_id
        for r in (
            await TaskAndUserRelationORM
                .query
                .where(TaskAndUserRelationORM.user_id == user_id)
                .gino.all()
        )
    ]

    tasks: List[TaskORM] = []

    for i in task_ids:
        task = await TaskORM.query.where(TaskORM.id == i).gino.first_or_404()
        tasks.append(task)

    return tasks


async def update_task(update_info: UpdateTaskFAPI, task_id: UUID = Path(...)):
    await TaskORM.update.values(**update_info.exclude_unset()).where(TaskORM.id == task_id).gino.status()


async def get_all_tasks() -> List[TaskFAPI]:
    return [TaskFAPI(**u.to_dict()) for u in await TaskORM.query.gino.all()]


async def delete_task(task_id: UUID):
    task = await TaskORM.query.where(TaskORM.id == task_id).gino.first_or_404()
    user_relations_ids = [
        r.task_id
        for r in (
            await TaskAndUserRelationORM
                .query
                .where(TaskAndUserRelationORM.task_id == task_id)
                .gino.all()
        )
    ]
    task_relations_ids = [
        r.task_id
        for r in (
            await AttachmentORM
                .query
                .where(AttachmentORM.task_id == task_id)
                .gino.all()
        )
    ]
    task_relations: List[AttachmentORM] = await (
        AttachmentORM.query.where(AttachmentORM.task_id.in_(task_relations_ids)).gino.all()
    )
    user_relations: List[TaskAndUserRelationORM] = await (
        TaskAndUserRelationORM.query.where(TaskAndUserRelationORM.task_id.in_(user_relations_ids)).gino.all()
    )

    for i in user_relations:
        await i.delete()

    for i in task_relations:
        await i.delete()

    await task.delete()
