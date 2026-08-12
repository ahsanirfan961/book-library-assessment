

from sqlalchemy import select
from backend.infra.db import AsyncSession
from backend.infra.open_library.client import OpenLibraryClient
from backend.schemas.subjects import Subject
from backend.infra.models import Subject as SubjectModel


class SubjectsService:
    def __init__(self, open_library_client: OpenLibraryClient, db: AsyncSession) -> None:
        self.open_library_client = open_library_client
        self.db = db

    async def get_subjects(self) -> list[Subject]:
        async with self.db as session:
            query = select(SubjectModel).order_by(SubjectModel.name)
            result = await session.execute(query)
            return result.scalars().all()
    
