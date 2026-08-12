

from fastapi import APIRouter

from backend.schemas.books import BookListResponse



router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=BookListResponse)
async def search():
    pass