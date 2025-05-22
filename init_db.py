import asyncio
from models import Base
from database import engine  # Импорты подгони под свою структуру

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())