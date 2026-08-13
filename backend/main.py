from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.api import books, subjects
from backend.infra.cache import RedisStorage
from backend.infra.db import engine
from backend.infra.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await RedisStorage().test_connection()
    
    yield
   
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

api = FastAPI()
api.include_router(books.router)
api.include_router(subjects.router)


app.mount("/api/v1", api)



@app.get("/")
def read_root():
    return {"status": "running"}
