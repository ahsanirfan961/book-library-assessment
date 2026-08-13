


from backend.infra.open_library.schemas import Work
from backend.mappers.books import cover_url
from backend.schemas.books import BookDetail, Book, Author as SAuthor
from backend.schemas.common import RatingStatus


def to_book_summary(work: Work) -> Book:
    return Book(
        id=work.key,
        title=work.title,
        authors=[SAuthor(id=a.key, name=a.name) for a in work.authors],
        firstPublishYear=work.first_publish_year,
        coverUrl=cover_url(work.cover_id),
        rating=None,
        ratingStatus=RatingStatus.unavailable,
    )

def to_book_detail(work: Work) -> BookDetail:
    return BookDetail(
        id=work.key,
        title=work.title,
        authors=[SAuthor(id=a.key, name=a.name) for a in work.authors],
        firstPublishYear=work.first_publish_year,
        coverUrl=cover_url(work.cover_id),
        rating=None,
        ratingStatus=RatingStatus.unavailable,
    )