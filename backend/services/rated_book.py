

from abc import ABC
from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select
from backend.infra.db import AsyncSession
from backend.infra.google_books.client import GoogleBooksClient
from backend.infra.models import EnrichmentQueue, Rating as RatingModel
from backend.infra.open_library.client import OpenLibraryClient
from backend.infra.open_library.mappers import to_book_detail, to_book_summary
from backend.mappers.books import map_rating
from backend.schemas.books import BookDetail, Book, Rating
from backend.schemas.common import Paginated
from backend.services.a_book import ABookService



class RatedBookService(ABookService):
    def __init__(self,book_service: ABookService, db: AsyncSession,  google_books_client: GoogleBooksClient) -> None:
        self.db = db
        self.book_service = book_service
        self.open_library_client = google_books_client
    
    async def enqueue_books_for_enrichment(self, books: List[Book]) -> None:
        if not books:
            return

        stmt = (
            insert(EnrichmentQueue)
            .values([{"book_id": book.id} for book in books])
            .on_conflict_do_nothing(index_elements=["book_id"])
        )
        await self.db.execute(stmt)
        await self.db.commit()
  

    def attach_rating(self, book: Book, rating: RatingModel) -> Book:
        rating, rating_status = map_rating(rating)
        return book.model_copy(update={"rating": rating, "ratingStatus": rating_status})

    def attach_ratings(self, books: List[Book], ratings: List[RatingModel]) -> List[Book]:
        return [
            self.attach_rating(book, rating)
            for book in books
            for rating in ratings
            if rating.book_id == book.id
        ]

    
    async def get_books(self, subject: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            books = (await self.book_service.get_books(subject, limit, offset)).items

            book_ids = [book.id for book in books]

            stat = select(RatingModel).where(RatingModel.book_id.in_(book_ids))
            ratings = await self.db.execute(stat).scalars().all()

            books_missing_ratings = [book for book in books if book.id not in book_ids]

            await self.enqueue_books_for_enrichment(books_missing_ratings)

            books = self.attach_ratings(books, ratings)

            return Paginated(
                limit=limit,
                offset=offset,
                total=len(books),
                items=[to_book_summary(book) for book in books]
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            books = (await self.book_service.search_books(query, limit, offset)).items

            book_ids = [book.id for book in books]

            stat = select(RatingModel).where(RatingModel.book_id.in_(book_ids))
            ratings = await self.db.execute(stat).scalars().all()

            books_missing_ratings = [book for book in books if book.id not in [rating.book_id for rating in ratings]]

            await self.enqueue_books_for_enrichment(books_missing_ratings)

            books = self.attach_ratings(books, ratings)

            return Paginated(
                limit=limit,
                offset=offset,
                total=len(books),
                items=[to_book_summary(book) for book in books]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_book_detail(self, book_id: str) -> BookDetail:
        try:
            book = await self.book_service.get_book_detail(book_id)

            stat = select(RatingModel).where(RatingModel.book_id == book_id)
            rating = await self.db.execute(stat).scalar_one_or_none()

            book = self.attach_rating(book, rating)

            return book
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Book]:
        try:
            books = (await self.book_service.get_popular_books(limit, offset)).items

            book_ids = [book.id for book in books]
            stat = select(RatingModel).where(RatingModel.book_id.in_(book_ids))
            ratings = await self.db.execute(stat).scalars().all()

            books_missing_ratings = [book for book in books if book.id not in book_ids]
            await self.enqueue_books_for_enrichment(books_missing_ratings)
            books = self.attach_ratings(books, ratings)
            return Paginated(limit=limit, offset=offset, total=len(books), items=[to_book_summary(book) for book in books])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))




