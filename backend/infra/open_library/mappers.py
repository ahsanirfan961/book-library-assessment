import re

from backend.infra.open_library.schemas import Work
from backend.mappers.books import cover_url
from backend.schemas.books import BookDetail, Book, Author as SAuthor, SubjectRef
from backend.schemas.common import RatingStatus


def _ol_key(key: str) -> str:
    return key.rsplit("/", 1)[-1]


def _slug(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name.lower()).strip()
    return re.sub(r"[\s_]+", "-", s) or "unknown"


def to_book_summary(work: Work) -> Book:
    return Book(
        id=_ol_key(work.key),
        title=work.title,
        authors=[SAuthor(id=_ol_key(a.key), name=a.name) for a in work.authors],
        firstPublishYear=work.first_publish_year,
        coverUrl=cover_url(work.cover_id),
        rating=None,
        ratingStatus=RatingStatus.unavailable,
    )


def to_book_detail(work: Work) -> BookDetail:
    return BookDetail(
        **to_book_summary(work).model_dump(),
        editionCount=work.edition_count or 0,
        description=work.description,
        coverUrlLarge=cover_url(work.cover_id, size="L"),
        subjects=[SubjectRef(slug=_slug(s), name=s) for s in work.subjects],
    )
