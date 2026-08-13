

from abc import ABC
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from backend.infra.db import AsyncSession
from backend.infra.open_library.client import OpenLibraryClient
from backend.infra.open_library.mappers import to_book_detail, to_book_summary
from backend.schemas.books import BookDetail, Book
from backend.schemas.common import Paginated
from backend.services.a_book import ABookService



# class CachedBookService(ABookService):
#     def __init__(self, book_service: ABookService, redis) -> None:
#         self.book_repository = book_repository
        

#     async def get_books(self, subject, limit: int = 10, offset: int = 0) -> Paginated[Book]:
#         try:
#             return await self.book_repository.get_books(subject, limit, offset)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))
    
#     async def search_books(self, query: str, limit: int = 10, offset: int = 0) -> Paginated[Book]:
#         try:
#             return await self.book_repository.search_books(query, limit, offset)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))
    
#     async def get_book_detail(self, book_id: str) -> BookDetail:
#         try:
#             book = await self.book_repository.get_book_detail(book_id)
#             return to_book_detail(book)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))

