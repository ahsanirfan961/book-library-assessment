


import asyncio

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from backend.infra.db import AsyncSession
from backend.infra.google_books.client import GoogleBooksClient
from backend.infra.models import EnrichmentQueue, Rating, RatingStatus


class RatingEnrichmentManager:

    def __init__(self, db: AsyncSession, google_books_client: GoogleBooksClient):
        self.db = db
        self.google_books_client = google_books_client

    async def run(self):
        logger.info("Rating enrichment loop running")
        while True:
            await self.enrich_rating()
            await asyncio.sleep(1.1)

    async def enrich_rating(self):
        
        try:
            stmt = select(EnrichmentQueue).order_by(EnrichmentQueue.enqueued_at.asc()).with_for_update(skip_locked=True).limit(1)
            result = await self.db.execute(stmt)
            enrichment_queue: EnrichmentQueue | None = result.scalars().first()

            if not enrichment_queue:
                await self.db.rollback()
                return

            try:
                volume = await self.google_books_client.search_by_isbn(enrichment_queue.isbn)
            except ValueError as e:
                logger.error(f"No match for rating found for book {enrichment_queue.book_id}")
                volume = None

            if volume and volume.volumeInfo.averageRating is not None:
                avg_rating = volume.volumeInfo.averageRating
                ratings_count = volume.volumeInfo.ratingsCount or 0
                status = RatingStatus.ok
            else:
                avg_rating = None
                ratings_count = 0
                status = RatingStatus.no_match

            upsert_stmt = (
                insert(Rating)
                .values(
                    book_id=enrichment_queue.book_id,
                    average_rating=avg_rating,
                    ratings_count=ratings_count,
                    status=status,
                )
                .on_conflict_do_update(
                    index_elements=[Rating.book_id],
                    set_={
                        "average_rating": avg_rating,
                        "ratings_count": ratings_count,
                        "status": status,
                    },
                )
            )
            await self.db.execute(upsert_stmt)

            await self.db.execute(delete(EnrichmentQueue).where(EnrichmentQueue.book_id == enrichment_queue.book_id))
            
            await self.db.commit()
            logger.success(f"Rating enriched for book {enrichment_queue.book_id}")

        except Exception as e:
            logger.error(f"Error enriching rating: {e}")
            await self.db.rollback()
            return
        









