from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.app import db
from publishing_platform.users.enums import *

__all__ = [
    "FormORM",
    "UserAndFormRelationsORM",
]


class FormORM(db.Model):
    __tablename__ = "forms"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)


class UserAndFormRelationsORM(db.Model):
    __tablename__ = "userandformrelations"

    user_id = db.Column(UUID(), nullable=False)
    form_id = db.Column(UUID(), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)

    __user_id_fk = db.ForeignKeyConstraint(["user_id"], ["users.id"])
    __form_id_fk = db.ForeignKeyConstraint(["form_id"], ["forms.id"])
    __unique_constrait_pk = db.PrimaryKeyConstraint("form_id", "user_id")

