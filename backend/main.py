import asyncio
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from loguru import logger
from sqlalchemy import text

from backend.api import books, subjects
from backend.infra.cache import RedisStorage
from backend.infra.db import AsyncSession, engine
from backend.infra.google_books.client import GoogleBooksClient
from backend.infra.models import Base
from backend.jobs.rating_enrichment import RatingEnrichmentManager
from backend.jobs.rating_matchers import CompositeRatingMatcher, IsbnMatcher, TitleAuthorMatcher
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()


APP_API_KEY = os.getenv("APP_API_KEY")


async def run_enrichment_worker():
    try:
        async with httpx.AsyncClient(timeout=30.0) as http_client, AsyncSession() as db:
            logger.info("Rating enrichment worker started")
            client = GoogleBooksClient(http_client)
            matcher = CompositeRatingMatcher([IsbnMatcher(client), TitleAuthorMatcher(client)])
            manager = RatingEnrichmentManager(db, matcher)
            await manager.run()
    except asyncio.CancelledError:
        pass
    except Exception:
        logger.exception("Rating enrichment worker failed")


def worker_failur(task: asyncio.Task) -> None:
    if task.cancelled():
        return
    exc = task.exception()
    if exc:
        logger.error(f"Enrichment worker stopped with error: {exc}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await RedisStorage().test_connection()

    # enrichment_worker = asyncio.create_task(run_enrichment_worker())
    # enrichment_worker.add_done_callback(worker_failur)
    
    yield
   
    # enrichment_worker.cancel()
    # await enrichment_worker

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(books.router, prefix="/api/v1")
app.include_router(subjects.router, prefix="/api/v1")

# this is for security 
@app.middleware("http")
async def check_app_key(request: Request, call_next):
    if request.url.path.startswith("/api/"): 
        if request.headers.get("X-App-Key") != APP_API_KEY:
            raise HTTPException(status_code=403, detail="Forbidden")
    return await call_next(request)


# this is also for security (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}