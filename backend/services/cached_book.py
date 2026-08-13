

from abc import ABC
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from backend.infra.cache import RedisStorage
from backend.infra.db import AsyncSession
from backend.infra.open_library.client import OpenLibraryClient
from backend.infra.open_library.mappers import to_book_detail, to_book_summary
from backend.schemas.books import BookDetail, Book
from backend.schemas.common import Paginated
from backend.services.a_book import ABookService



class CachedBookService(ABookService):

    def __init__(self,book_service: ABookService, redis: RedisStorage) -> None:
        self.redis = redis
        self.book_service = book_service
    
    
    async def get_books(self, subject: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            books = await self.redis.get(f"books:{subject}:{limit}:{offset}")
            if books:
                return books
            books = await self.book_service.get_books(subject, limit, offset)
            await self.redis.set(f"books:{subject}:{limit}:{offset}", books)
            return books

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            books = await self.redis.get(f"search_books:{query}:{limit}:{offset}")
            if books:
                return books
            books = await self.book_service.search_books(query, limit, offset)
            await self.redis.set(f"search_books:{query}:{limit}:{offset}", books)
            return books
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_book_detail(self, book_id: str) -> BookDetail:
        try:
            book = await self.redis.get(f"book:{book_id}")
            if book:
                return book
            book = await self.book_service.get_book_detail(book_id)
            await self.redis.set(f"book:{book_id}", book)
            return book
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Book]:
        try:
            books = await self.redis.get(f"popular_books:{limit}:{offset}")
            if books:
                return books
            books = await self.book_service.get_popular_books(limit, offset)
            await self.redis.set(f"popular_books:{limit}:{offset}", books)
            return books
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

