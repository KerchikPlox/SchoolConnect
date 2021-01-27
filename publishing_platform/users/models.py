from sqlalchemy.dialects.postgresql import UUID

from publishing_platform.app import db
from publishing_platform.users.enums import *

__all__ = [
    "UserIdentity",
    "User",
]


class UserIdentity(db.Model):
    __tablename__ = "user_identities"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    login = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)
    expire_date = db.Column(db.DateTime(), nullable=True)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(), nullable=False, primary_key=True)
    login = db.Column(db.String(), nullable=False, unique=True)
    author_name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)
