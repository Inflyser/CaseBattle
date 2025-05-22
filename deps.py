from contextlib import asynccontextmanager
from database import AsyncSessionLocal

@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session