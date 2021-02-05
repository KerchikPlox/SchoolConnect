import datetime
from sqlalchemy.dialects.postgresql import UUID, BYTEA

from publishing_platform.app import db
from publishing_platform.users.enums import *

__all__ = [
    "AttachmentORM",
]


class AttachmentORM(db.Model):
    __tablename__ = "attachments"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    task_id = db.Column(UUID(), nullable=False)
    file = db.Column(BYTEA(), nullable=False)
    filename = db.Column(db.String(), nullable=False)
    media_type = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    __task_id_fk = db.ForeignKeyConstraint(["task_id"], ["tasks.id"])