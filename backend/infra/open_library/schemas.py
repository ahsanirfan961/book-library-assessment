

from pydantic import BaseModel


class Author(BaseModel):
    key: str
    name: str

class Availability(BaseModel):
    status: str
    isbn: str
    openlibrary_edition: str

class Work(BaseModel):
    key: str
    title: str
    edition_count: int
    cover_id: int
    cover_edition_key: str
    authors: list[Author]
    subjects: list[str]
    availability: Availability


class SubjectWorks(BaseModel):
    key: str
    name: str
    subject_type: str
    work_count: int
    works: list 