from datetime import date, datetime
from decimal import Decimal
import enum
from typing import Optional
from sqlalchemy import Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import Computed, ForeignKey, Identity
from sqlalchemy.types import CHAR, BigInteger, Boolean, Date, DateTime, Float, Integer, Numeric, SmallInteger, Text

from sqlalchemy.dialects.postgresql import ENUM, TSVECTOR


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

class SubjectKind(str, enum.Enum):
    subject = "subject"
    place = "place"
    time = "time"
    person = "person"


rating_status_enum = ENUM(RatingStatus, name="rating_status", create_type=False)
match_method_enum = ENUM(MatchMethod, name="match_method", create_type=False)
subject_kind_enum = ENUM(SubjectKind, name="subject_kind", create_type=False)



class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    ol_author_key: Mapped[str] = mapped_column(Text, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default_factory=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default_factory=datetime.now)
    
    books: Mapped[list["Book"]] = relationship(
        secondary="book_authors",
        back_populates="authors",
    )


class Isbn(Base):
    __tablename__ = "isbns"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)

    isbn13: Mapped[Optional[str]] = mapped_column(CHAR(13))
    isbn10: Mapped[Optional[str]] = mapped_column(CHAR(10))
    book: Mapped["Book"] = relationship(back_populates="isbns")
    edition: Mapped["Edition"] = relationship(back_populates="isbns")


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)

    cover_id: Mapped[Optional[int]] = mapped_column(Integer)
    ol_edition_key: Mapped[str] = mapped_column(Text, nullable=False)
    publisher: Mapped[Optional[str]] = mapped_column(Text)
    publish_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
    publish_date: Mapped[Optional[str]] = mapped_column(Text)
    pages: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default_factory=datetime.now)
    book: Mapped["Book"] = relationship(back_populates="editions")
    isbns: Mapped[list[Isbn]] = relationship(back_populates="edition")

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    
    name: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[SubjectKind] = mapped_column(
        subject_kind_enum,
        nullable=False,
        server_default=SubjectKind.subject.value,
    )
    work_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    is_curated: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    
    nav_order: Mapped[Optional[int]] = mapped_column(SmallInteger)
    illustration_key: Mapped[Optional[str]] = mapped_column(Text)

    books: Mapped[list["Book"]] = relationship(
        secondary="book_subjects",
        back_populates="subjects",
    )
    

class Rating(Base):
    __tablename__ = "ratings"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    
    status: Mapped[RatingStatus] = mapped_column(rating_status_enum, nullable=False)
    average_rating: Mapped[Optional[Decimal]] = mapped_column(Float)
    ratings_count: Mapped[int] = mapped_column(Integer)
    source_volume_id: Mapped[Optional[str]] = mapped_column(Text)
    matched_via: Mapped[Optional[MatchMethod]] = mapped_column(match_method_enum)
    match_confidence: Mapped[Optional[Decimal]] = mapped_column(Float)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default_factory=datetime.now)

    book: Mapped["Book"] = relationship(back_populates="rating")


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        Index("books_search_vector_idx", "search_vector", postgresql_using="gin"),
        Index("books_title_trgm_idx", "title", postgresql_using="gin", postgresql_ops={"title": "gin_trgm_ops"})
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    ol_work_key: Mapped[str] = mapped_column(Text, nullable=False) 
    title: Mapped[str] = mapped_column(Text, nullable=False)
    subtitle: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    cover_id: Mapped[Optional[int]] = mapped_column(Integer)
    first_publish_year: Mapped[Optional[int]] = mapped_column(SmallInteger)
    language: Mapped[Optional[str]] = mapped_column(CHAR(3))
    edition_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    popularity: Mapped[float] = mapped_column(Float, nullable=False, server_default="0")

    search_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        Computed(
            "setweight(to_tsvector('english', coalesce(title, '')), 'A') || "
            "setweight(to_tsvector('english', coalesce(subtitle, '')), 'B') || "
            "setweight(to_tsvector('english', coalesce(description, '')), 'D')",
            persisted=True,
        ),
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    authors: Mapped[list[Author]] = relationship(
        secondary="book_authors",
        back_populates="books",
        order_by="BookAuthor.position",
    )
    editions: Mapped[list[Edition]] = relationship(
        back_populates="book",
        order_by="Edition.publish_year.desc().nullslast()",
    )
    isbns: Mapped[list[Isbn]] = relationship(back_populates="book")
    subjects: Mapped[list[Subject]] = relationship(
        secondary="book_subjects",
        back_populates="books",
    )
    rating: Mapped[Optional[Rating]] = relationship(back_populates="book", uselist=False)
    enrichment: Mapped[Optional[EnrichmentQueue]] = relationship(back_populates="book", uselist=False)


class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default="0")




class BookSubject(Base):
    __tablename__ = "book_subjects"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True)




class EnrichmentQueue(Base):
    __tablename__ = "enrichment_queue"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    priority: Mapped[float] = mapped_column(Float, nullable=False, server_default="0")
    enqueued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default_factory=datetime.now)
    attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default="0")
    last_error: Mapped[Optional[str]] = mapped_column(Text)
    
    book: Mapped[Book] = relationship(back_populates="enrichment")


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    dump_date: Mapped[date] = mapped_column(Date, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rows_upserted: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="running")


class PopularBook(Base):
    __tablename__ = "popular_books"
    __table_args__ = {"info": {"is_materialized_view": True}}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ol_work_key: Mapped[str] = mapped_column(Text, nullable=False)
    popularity: Mapped[float] = mapped_column(Float, nullable=False)


class CuratedSubjectCount(Base):
    __tablename__ = "curated_subject_counts"
    __table_args__ = {"info": {"is_materialized_view": True}}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    slug: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    illustration_key: Mapped[Optional[str]] = mapped_column(Text)
    nav_order: Mapped[Optional[int]] = mapped_column(SmallInteger)
    book_count: Mapped[int] = mapped_column(BigInteger, nullable=False)
