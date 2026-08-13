


from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel


class RatingStatus(str, Enum):
    ok = "ok"
    stale = "stale"
    no_match = "no_match"
    unavailable = "unavailable"


T = TypeVar('T')

class Paginated(BaseModel, Generic[T]):
    limit: int
    offset: int
    total: int
    items: list[T]
    