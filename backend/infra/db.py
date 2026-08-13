import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, connect_args={"statement_cache_size": 0})
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSession() as session:
        try:
            yield session
        finally:
            await session.close()