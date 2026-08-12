


from enum import Enum


class RatingStatus(str, Enum):
    ok = "ok"
    stale = "stale"
    no_match = "no_match"
    unavailable = "unavailable"