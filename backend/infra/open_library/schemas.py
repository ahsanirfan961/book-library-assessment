

from typing import Optional
from pydantic import AliasChoices, BaseModel, Field, model_validator

from backend.schemas.common import Paginated


class Author(BaseModel):
    key: str
    name: str

class Availability(BaseModel):
    status: str
    isbn: Optional[str] = None
    openlibrary_edition: Optional[str] = None

class Work(BaseModel):
    key: str
    title: str
    edition_count: Optional[int] = Field(default=0)
    cover_id: Optional[int] = None
    cover_edition_key: Optional[str] = None
    authors: list[Author] = Field(default_factory=list)
    subjects: list[str] = Field(default_factory=list, validation_alias=AliasChoices("subject", "subjects"))
    availability: Optional[Availability] = None
    first_publish_year: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_authors(cls, data):
        if isinstance(data, dict) and "authors" in data:
            normalized = []
            for a in data["authors"]:
                if "author" in a: 
                    normalized.append({"key": a["author"]["key"], "name": ""})
                else:  
                    normalized.append(a)
            data["authors"] = normalized
        if isinstance(data, dict) and "covers" in data and not data.get("cover_id"):
            data["cover_id"] = data["covers"][0] if data["covers"] else None
        return data


class SubjectWorks(BaseModel):
    key: str
    name: str
    subject_type: str
    work_count: int
    works: Paginated[Work] 