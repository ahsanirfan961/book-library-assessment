

from typing import Optional
from pydantic import BaseModel



class IndustryIdentifier(BaseModel):
    type: str
    identifier: str

class VolumeInfo(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    authors: list[str]
    industryIdentifiers: list[IndustryIdentifier]
    averageRating: Optional[float] = None
    ratingsCount: Optional[int] = None

class Volume(BaseModel):
    id: str
    volumeInfo: VolumeInfo