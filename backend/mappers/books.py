


from typing import Optional

from backend.infra.models import Rating as RatingRow, RatingStatus as DbRatingStatus
from backend.schemas.books import Author, Book, Edition, Rating, RatingStatus, BookDetail



def cover_url(cover_id: Optional[int], size: str = "M") -> str | None:
    if cover_id is None:
        return None
    return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"


def map_rating(row: Optional[RatingRow]) -> tuple[Optional[Rating], RatingStatus]:
    
    if row is None:
        return None, RatingStatus.unavailable

    if row.status == DbRatingStatus.no_match:
        return None, RatingStatus.no_match

    if row.status in (DbRatingStatus.ok, DbRatingStatus.stale):
        if row.average_rating is None:
            return None, RatingStatus.unavailable
        return (
            Rating(
                average=float(row.average_rating),
                count=row.ratings_count,
                asOf=row.fetched_at.date() if row.status == DbRatingStatus.stale else None,
            ),
            RatingStatus(row.status.value),
        )
    return None, RatingStatus.unavailable





    