

from abc import ABC
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from backend.infra.cache import RedisStorage
from backend.infra.db import AsyncSession
from backend.infra.open_library.client import OpenLibraryClient
from backend.infra.open_library.mappers import to_book_detail, to_book_summary
from pydantic import TypeAdapter
from backend.schemas.books import BookDetail, Book
from backend.schemas.common import Paginated
from backend.services.a_book import ABookService

_page_adapter = TypeAdapter(Paginated[Book])
_book_detail_adapter = TypeAdapter(BookDetail)


class CachedBookService(ABookService):

    def __init__(self,book_service: ABookService, redis: RedisStorage) -> None:
        self.redis = redis
        self.book_service = book_service

    async def _get_cached_page(self, key: str) -> Paginated[Book] | None:
        raw = await self.redis.get(key)
        if not raw:
            return None
        try:
            return _page_adapter.validate_json(raw)
        except Exception:
            await self.redis._local_db.delete(key)
            return None

    async def _get_cached_book(self, key: str) -> BookDetail | None:
        raw = await self.redis.get(key)
        if not raw:
            return None
        try:
            return _book_detail_adapter.validate_json(raw)
        except Exception:
            await self.redis._local_db.delete(key)
            return None
    
    
    async def get_books(self, subject: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            cache_key = f"books:{subject}:{limit}:{offset}"
            cached = await self._get_cached_page(cache_key)
            if cached:
                return cached
            books = await self.book_service.get_books(subject, limit, offset)
            await self.redis.set(cache_key, books.model_dump_json())
            return books

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}" or repr(e))

    async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
        try:
            cache_key = f"search_books:{query}:{limit}:{offset}"
            cached = await self._get_cached_page(cache_key)
            if cached:
                return cached
            books = await self.book_service.search_books(query, limit, offset)
            await self.redis.set(cache_key, books.model_dump_json())
            return books
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}" or repr(e))
    
    async def get_book_detail(self, book_id: str) -> BookDetail:
        try:
            cache_key = f"book:{book_id}"
            cached = await self._get_cached_book(cache_key)
            if cached:
                return cached
            book = await self.book_service.get_book_detail(book_id)
            await self.redis.set(cache_key, book.model_dump_json())
            return book
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}" or repr(e))
    
    async def get_popular_books(self, limit: int = 6, offset: int = 0) -> Paginated[Book]:
        try:
            cache_key = f"popular_books:{limit}:{offset}"
            cached = await self._get_cached_page(cache_key)
            if cached:
                return cached
            books = await self.book_service.get_popular_books(limit, offset)
            await self.redis.set(cache_key, books.model_dump_json())
            return books
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}" or repr(e))

