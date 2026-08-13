

from abc import ABC
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from backend.infra.db import AsyncSession
from backend.infra.open_library.client import OpenLibraryClient
from backend.infra.open_library.mappers import to_book_detail, to_book_summary
from backend.schemas.books import BookDetail, Book
from backend.schemas.common import Paginated
from backend.services.a_book import ABookService



class OLBookService(ABookService):
    def __init__(self, db: AsyncSession, open_library_client: OpenLibraryClient) -> None:
        self.db = db
        self.open_library_client = open_library_client
    
    async def get_books(self, subject: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            subject_works = await self.open_library_client.get_subject_works(subject, limit, offset)
            return Paginated(
                limit=limit,
                offset=offset,
                total=subject_works.work_count,
                items=[to_book_summary(work) for work in subject_works.works.items]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e) or repr(e))

    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            works = await self.open_library_client.search_books(query, limit, offset)
            return Paginated(
                limit=limit,
                offset=offset,
                total=works.total,
                items=[to_book_summary(work) for work in works.items]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e) or repr(e))
    
    async def get_book_detail(self, book_id: str) -> BookDetail:
        try:
            work = await self.open_library_client.get_work(book_id)
            return to_book_detail(work)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e) or repr(e))
    
    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Book]:
        try:
            works = await self.open_library_client.get_popular_books(limit, offset)
            return Paginated(
                limit=limit,
                offset=offset,
                total=works.total,
                items=[to_book_summary(work) for work in works.items]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e) or repr(e))




