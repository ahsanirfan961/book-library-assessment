

from typing import List, Optional
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from backend.infra.db import AsyncSession
from backend.infra.models import EnrichmentQueue, Rating as RatingModel, RatingStatus as DbRatingStatus
from backend.mappers.books import map_rating
from backend.schemas.books import BookDetail, Book
from backend.schemas.common import Paginated
from backend.services.a_book import ABookService


class RatedBookService(ABookService):
    def __init__(self, book_service: ABookService, db: AsyncSession) -> None:
        self.db = db
        self.book_service = book_service

    async def ensure_ratings_for_books(self, books: List[Book]) -> None:
        if not books:
            return

        book_ids = [book.id for book in books]
        result = await self.db.execute(
            select(RatingModel.book_id).where(RatingModel.book_id.in_(book_ids))
        )

        existing = set(result.scalars().all())

        missing = [book for book in books if book.id not in existing]

        if not missing:
            return

        no_isbn = [book for book in missing if not book.isbn]
        with_isbn = [book for book in missing if book.isbn]

        if no_isbn:
            stmt = (
                insert(RatingModel)
                .values([
                    {"book_id": book.id, "status": DbRatingStatus.no_match, "ratings_count": 0}
                    for book in no_isbn
                ])
                .on_conflict_do_nothing(index_elements=["book_id"])
            )
            await self.db.execute(stmt)

        if with_isbn:
            stmt = (
                insert(EnrichmentQueue)
                .values([{"book_id": book.id, "isbn": book.isbn} for book in with_isbn])
                .on_conflict_do_nothing(index_elements=["book_id"])
            )
            await self.db.execute(stmt)

        await self.db.commit()

    async def get_ratings_for_books(self, books: List[Book]) -> List[RatingModel]:

        if not books:
            return []

        book_ids = [book.id for book in books]

        result = await self.db.execute(
            select(RatingModel).where(RatingModel.book_id.in_(book_ids))
        )
        
        return list(result.scalars().all())

    def attach_rating(self, book: Book, rating: Optional[RatingModel]) -> Book:
        mapped_rating, rating_status = map_rating(rating)
        return book.model_copy(update={"rating": mapped_rating, "ratingStatus": rating_status})

    def attach_ratings(self, books: List[Book], ratings: List[RatingModel]) -> List[Book]:
        by_id = {rating.book_id: rating for rating in ratings}
        return [self.attach_rating(book, by_id.get(book.id)) for book in books]

    async def get_books(self, subject: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            page = await self.book_service.get_books(subject, limit, offset)
            await self.ensure_ratings_for_books(page.items)
            ratings = await self.get_ratings_for_books(page.items)
            return Paginated(
                limit=limit,
                offset=offset,
                total=page.total,
                items=self.attach_ratings(page.items, ratings),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            page = await self.book_service.search_books(query, limit, offset)
            await self.ensure_ratings_for_books(page.items)
            ratings = await self.get_ratings_for_books(page.items)
            return Paginated(
                limit=limit,
                offset=offset,
                total=page.total,
                items=self.attach_ratings(page.items, ratings),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_book_detail(self, book_id: str) -> BookDetail:
        try:
            book = await self.book_service.get_book_detail(book_id)
            await self.ensure_ratings_for_books([book])
            ratings = await self.get_ratings_for_books([book])
            return self.attach_rating(book, ratings[0] if ratings else None)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Book]:
        try:
            page = await self.book_service.get_popular_books(limit, offset)
            await self.ensure_ratings_for_books(page.items)
            ratings = await self.get_ratings_for_books(page.items)
            return Paginated(
                limit=limit,
                offset=offset,
                total=page.total,
                items=self.attach_ratings(page.items, ratings),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
