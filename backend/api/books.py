

from typing import Annotated, Optional
from fastapi import APIRouter, Depends,Response

from backend.infra.db import AsyncSession, get_db
from backend.schemas.books import BookDetail, BookListResponse



router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=BookListResponse)
async def search(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    q: str,
    subject: Optional[str] = None,
    cursor: Optional[str]= None,
    limit: int = 24,
):
    pass


@router.get("/popular", response_model=BookListResponse)
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
):
    pass