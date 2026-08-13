

from typing import Annotated, Optional
from fastapi import APIRouter, Depends,Response
import httpx

from backend.infra.cache import RedisStorage
from backend.infra.db import AsyncSession, get_db
from backend.infra.open_library.client import OpenLibraryClient, get_ol_http_client
from backend.schemas.books import Book, BookDetail
from backend.schemas.common import Paginated
from backend.services.cached_book import CachedBookService
from backend.services.ol_book import OLBookService
from backend.services.rated_book import RatedBookService



router = APIRouter(prefix="/books", tags=["books"])



@router.get("/search", response_model=Paginated[Book])
async def search(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    ol_http_client: Annotated[httpx.AsyncClient, Depends(get_ol_http_client)],
    q: str,
    limit: int = 24,
    offset: int = 0,
):
    book_service = CachedBookService(RatedBookService(OLBookService(db, OpenLibraryClient(ol_http_client)), db), RedisStorage())
    return await book_service.search_books(q, limit, offset)


@router.get("/popular", response_model=Paginated[Book])
async def popular(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    ol_http_client: Annotated[httpx.AsyncClient, Depends(get_ol_http_client)],
    limit: int = 6,
    offset: int = 0,
):
    book_service = CachedBookService(RatedBookService(OLBookService(db, OpenLibraryClient(ol_http_client)), db), RedisStorage())
    return await book_service.get_popular_books(limit, offset)

@router.get("/{book_id}", response_model=BookDetail)
async def book_detail(
    response: Response,
    book_id: str,  
    db: Annotated[AsyncSession, Depends(get_db)],
    ol_http_client: Annotated[httpx.AsyncClient, Depends(get_ol_http_client)],
):
    book_service = CachedBookService(RatedBookService(OLBookService(db, OpenLibraryClient(ol_http_client)), db), RedisStorage())
    return await book_service.get_book_detail(book_id)