from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

from backend.schemas.common import RatingStatus


class Author(BaseModel):
    id: str 
    name: str


class Rating(BaseModel):
    average: float = Field(ge=0, le=5)
    count: int = Field(ge=0)
    asOf: Optional[date] = None


class EditionSummary(BaseModel):
    id: str
    publisher: Optional[str] = None
    publishYear: Optional[int] = None
    isbn13: Optional[str] = None


class BookSummary(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    authors: List[Author]
    firstPublishYear: Optional[int] = None
    coverUrl: Optional[str] = None
    rating: Optional[Rating] = None
    ratingStatus: RatingStatus


class SubjectRef(BaseModel):
    slug: str
    name: str
    kind: str = "subject"


class BookDetail(BookSummary):
    editionCount: int
    language: Optional[str] = None
    description: Optional[str] = None
    coverUrlLarge: Optional[str] = None
    subjects: list[SubjectRef]
    editions: list[EditionSummary] = Field(default_factory=list, max_length=5)



class BookListResponse(BaseModel):
    items: list[BookSummary]
    nextCursor: Optional[str]
    totalEstimate: Optional[int] = None