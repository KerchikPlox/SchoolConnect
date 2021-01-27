from sqlalchemy.dialects.postgresql import UUID, BYTEA

from publishing_platform.app import db
from publishing_platform.users.enums import *

__all__ = [
    "SendFilesORM",
]


class SendFilesORM(db.Model):
    __tablename__ = "sendfiles"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    user_id = db.Column(UUID(), nullable=False)
    task_id = db.Column(UUID(), nullable=False)
    file = db.Column(BYTEA(), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)
    sent_at = db.Column(db.DateTime(), nullable=True)

    __user_id_fk = db.ForeignKeyConstraint(["user_id"], ["users.id"])

