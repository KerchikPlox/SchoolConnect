import datetime
from uuid import uuid4

from publishing_platform.app import db
from publishing_platform.auth.service import get_password_hash
from publishing_platform.users.enums import *
from publishing_platform.users.models import User, UserIdentity

__all__ = [
    "setup_tables_before_start",
    "setup_admin_user",
]


async def setup_tables_before_start() -> None:
    await db.gino.create_all()


async def setup_admin_user() -> None:

    if await User.query.where(User.login == "admin").gino.first() is None:

        await UserIdentity.create(id=uuid4(), login="admin", password_hash=get_password_hash("sc2020"), role=Roles.admin)

        await User.create(
            id=uuid4(), login="admin", author_name="Administrator", created_at=datetime.datetime.utcnow(), role=Roles.admin
        )
