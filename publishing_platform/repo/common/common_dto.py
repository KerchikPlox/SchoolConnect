from uuid import UUID

from pydantic import BaseModel

__all__ = [
    "UpdateRatingFAPI",
]


class UpdateRatingFAPI(BaseModel):
    entity_id: UUID
    value: int
