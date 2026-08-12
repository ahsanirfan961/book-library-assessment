from typing import Annotated, Literal, Optional
from fastapi import APIRouter, Depends, Response

from backend.infra.db import AsyncSession, get_db
from backend.schemas.books import BookListResponse
from backend.schemas.subjects import SubjectListResponse


router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("/", response_model=SubjectListResponse)
async def list_subjects(response: Response, db:   Annotated[AsyncSession, Depends(get_db)]):
    pass


@router.get("/{slug}/books", response_model=BookListResponse)
async def subject_books(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    cursor: Optional[str] = None,
    limit: int = 12,
    sort: Literal["popularity", "year", "title"] = "popularity",
):
    pass
