

from typing import Annotated, Optional
from fastapi import APIRouter, Depends,Response
import httpx

from backend.infra.db import AsyncSession, get_db
from backend.infra.open_library.client import OpenLibraryClient, get_ol_http_client
from backend.schemas.books import Book, BookDetail
from backend.schemas.common import Paginated
from backend.services.books import OLBookService



router = APIRouter(prefix="/books", tags=["books"])



@router.get("/search", response_model=Paginated[Book])
async def search(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    q: str,
    subject: Optional[str] = None,
    cursor: Optional[str]= None,
    limit: int = 24,
):
    pass


@router.get("/popular", response_model=Paginated[Book])
async def popular(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = 6,
):
    pass

@router.get("/{book_id}", response_model=BookDetail)
async def book_detail(
    book_id: str,  
    db: Annotated[AsyncSession, Depends(get_db)],
    ol_http_client: Annotated[httpx.AsyncClient, Depends(get_ol_http_client)],
):
    book_service = OLBookService(db, OpenLibraryClient(ol_http_client))
    return await book_service.get_book_detail(book_id)