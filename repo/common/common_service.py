from typing import Any

from publishing_platform.repo.common.common_dto import *

__all__ = [
    "update_rating",
]


async def update_rating(data: UpdateRoleFAPI, entity_model: Any):
    result = (
        await entity_model.update.values(rating=entity_model.rating + data.value)
        .where(entity_model.id == data.entity_id)
        .gino.status()
    )
