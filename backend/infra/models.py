import enum
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Index, func
from sqlalchemy.dialects.postgresql import ENUM, TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import Computed, ForeignKey, Identity
from sqlalchemy.types import (
    DateTime,
    Float,
    Integer,
    SmallInteger,
    String,
    Text,
)


class Base(DeclarativeBase):
    pass


class RatingStatus(str, enum.Enum):
    ok = "ok"
    stale = "stale"
    no_match = "no_match"
    unavailable = "unavailable"

class MatchMethod(str, enum.Enum):
    isbn13 = "isbn13"
    isbn10 = "isbn10"
    fuzzy = "fuzzy"



rating_status_enum = ENUM(RatingStatus, name="rating_status", create_type=True)
match_method_enum = ENUM(MatchMethod, name="match_method", create_type=True)

    

class Rating(Base):
    __tablename__ = "ratings"

    book_id: Mapped[str] = mapped_column(String, primary_key=True)
    
    status: Mapped[RatingStatus] = mapped_column(rating_status_enum, nullable=False)
    average_rating: Mapped[Optional[Decimal]] = mapped_column(Float)
    ratings_count: Mapped[int] = mapped_column(Integer)
    source_volume_id: Mapped[Optional[str]] = mapped_column(Text)
    matched_via: Mapped[Optional[MatchMethod]] = mapped_column(match_method_enum)
    match_confidence: Mapped[Optional[Decimal]] = mapped_column(Float)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())





class EnrichmentQueue(Base):
    __tablename__ = "enrichment_queue"

    book_id: Mapped[str] = mapped_column(String, primary_key=True)
    isbn: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    enqueued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default="0")
    last_error: Mapped[Optional[str]] = mapped_column(Text)


