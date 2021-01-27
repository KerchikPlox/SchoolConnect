import datetime
from sqlalchemy.dialects.postgresql import UUID, BYTEA

from publishing_platform.app import db
from publishing_platform.users.enums import *

__all__ = [
    "TaskORM",
    "TaskAndUserRelationORM"
]


class TaskORM(db.Model):
    __tablename__ = "tasks"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    creator_id = db.Column(UUID(), nullable=False)
    form_id = db.Column(UUID(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    file = db.Column(BYTEA(), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    __creator_id_fk = db.ForeignKeyConstraint(["creator_id"], ["users.id"])


class TaskAndUserRelationORM(db.Model):
    __tablename__ = "userandtaskrelations"

    user_id = db.Column(UUID(), nullable=False)
    task_id = db.Column(UUID(), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)

    __user_id_fk = db.ForeignKeyConstraint(["user_id"], ["users.id"])
    __task_id_fk = db.ForeignKeyConstraint(["task_id"], ["tasks.id"])
    __unique_constrait_pk = db.PrimaryKeyConstraint("task_id", "user_id")
