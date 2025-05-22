import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# Загрузка переменных из .env

DATABASE_URL=os.getenv("DATABASE_URL")

port = os.getenv("DB_URLM")
if port not in DATABASE_URL:
    DATABASE_URL=os.getenv("DATABASE_URL")[:len(os.getenv("DATABASE_URL"))-len("/casebattle_db")] + os.getenv("DB_URLM") + "/casebattle_db"

# Создание движка и сессии
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Зависимость FastAPI для получения сессии
@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session