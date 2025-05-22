import asyncio
from database import engine
from models import Base  # Импортируй свой Base из models.py

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())