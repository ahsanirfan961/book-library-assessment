import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.api import books, subjects
from backend.infra.cache import RedisStorage
from backend.infra.db import AsyncSession, engine
from backend.infra.google_books.client import GoogleBooksClient, get_gb_http_client
from backend.infra.models import Base
from backend.jobs.rating_enrichment import RatingEnrichmentManager


async def run_enrichment_worker():
    async with get_gb_http_client() as http_client, AsyncSession() as db:
        manager = RatingEnrichmentManager(db, GoogleBooksClient(http_client))
        try:
            await manager.run()
        except asyncio.CancelledError:
            pass  


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await RedisStorage().test_connection()

    enrichment_worker = asyncio.create_task(run_enrichment_worker())
    
    yield
   
    enrichment_worker.cancel()
    await enrichment_worker
    
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

api = FastAPI()
api.include_router(books.router)
api.include_router(subjects.router)


app.mount("/api/v1", api)



@app.get("/")
def read_root():
    return {"status": "running"}
