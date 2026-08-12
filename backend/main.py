from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.infra.db import engine
from backend.infra.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
   
    await engine.dispose()

app = FastAPI()



@app.get("/")
def read_root():
    return {"status": "running"}
