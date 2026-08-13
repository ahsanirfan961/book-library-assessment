from typing import Annotated, Literal, Optional
from fastapi import APIRouter, Depends, Response
import httpx

from backend.infra.db import AsyncSession, get_db
from backend.infra.open_library.client import OpenLibraryClient, get_ol_http_client
from backend.schemas.books import Book
from backend.schemas.common import Paginated
from backend.schemas.subjects import Subject
from backend.services.books import OLBookService


router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("/", response_model=Paginated[Subject])
async def list_subjects(response: Response, db:   Annotated[AsyncSession, Depends(get_db)], limit: int = 12, offset: int = 0):
    return Paginated[Subject](items=[
        Subject(slug="fiction", name="Fiction"),
        Subject(slug="science_fiction", name="Science Fiction"),
        Subject(slug="fantasy", name="Fantasy"),
        Subject(slug="mystery_and_detective_stories", name="Mystery and detective stories"),
        Subject(slug="romance", name="Romance"),
        Subject(slug="history", name="History"),
        Subject(slug="biographies", name="Biographies"),
        Subject(slug="religion", name="Religion"),
        Subject(slug="art", name="Art"),
        Subject(slug="children", name="Children"),
    ], total=10, offset=offset, limit=limit)


@router.get("/{slug}/books", response_model=Paginated[Book])
async def subject_books(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    ol_http_client: Annotated[httpx.AsyncClient, Depends(get_ol_http_client)],
    limit: int = 12,
    offset: int = 0,
):
    return await OLBookService(db, OpenLibraryClient(ol_http_client)).get_books(slug, limit, offset)
