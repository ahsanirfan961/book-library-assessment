

from abc import ABC
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from backend.infra.db import AsyncSession
from backend.infra.open_library.client import OpenLibraryClient
from backend.infra.open_library.mappers import to_book_detail, to_book_summary
from backend.schemas.books import BookDetail, Book
from backend.schemas.common import Paginated


class ABookService(ABC):
    def __init__(self, book_service: "ABookService") -> None:
        self.book_service = book_service

      
    async def get_books(self, subject, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        return await self.book_service.get_books(subject, limit, offset)
    
    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        return await self.book_service.search_books(query, limit, offset)
    
    async def get_book_detail(self, book_id: str) -> BookDetail:
        return await self.book_service.get_book_detail(book_id)
    
    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Book]:
        return await self.book_service.get_popular_books(limit, offset)


