from uuid import UUID

from pydantic import BaseModel

from publishing_platform.users.enums import *

__all__ = [
    "UpdateRoleFAPI",
]


class UpdateRoleFAPI(BaseModel):
    entity_id: UUID
    value: Roles
