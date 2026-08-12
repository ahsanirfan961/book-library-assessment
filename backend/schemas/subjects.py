



from pydantic import BaseModel
from typing import List, Optional
from backend.schemas.books import SubjectRef


class Subject(SubjectRef):
    bookCount: int


class SubjectListResponse(BaseModel):
    items: List[Subject]