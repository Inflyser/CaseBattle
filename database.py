from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

if f"{os.getenv("DB_PORT")}" not in DATABASE_URL:
    DATABASE_URL=os.getenv("DATABASE_URL")[:len(os.getenv("DATABASE_URL"))-len("/casebattle_db")] + os.getenv("DB_URLM") + "/casebattle_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)