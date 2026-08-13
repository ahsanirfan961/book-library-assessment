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


class Edition(BaseModel):
    id: str
    publishYear: Optional[int] = None
    isbn13: Optional[str] = None


class Book(BaseModel):
    id: str
    title: str
    authors: List[Author]
    firstPublishYear: Optional[int] = None
    coverUrl: Optional[str] = None
    rating: Optional[Rating] = None
    ratingStatus: RatingStatus


class SubjectRef(BaseModel):
    slug: str
    name: str


class BookDetail(Book):
    editionCount: Optional[int] = 0
    language: Optional[str] = None
    description: Optional[str] = None
    coverUrlLarge: Optional[str] = None
    subjects: list[SubjectRef]
    editions: list[Edition] = Field(default_factory=list, max_length=5)


