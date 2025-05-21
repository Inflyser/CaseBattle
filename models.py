import enum
from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, JSON, func
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class StatusEnum(enum.Enum):
    neutral = "neutral"
    profit = "profit"
    loss = "loss"

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    stars = Column(Integer, default=0)
    tickets = Column(Integer, default=0)
    stars_earned_total = Column(Integer, default=0)
    stars_spent_total = Column(Integer, default=0)
    tickets_earned_total = Column(Integer, default=0)
    tickets_spent_total = Column(Integer, default=0)
    app_visits = Column(Integer, default=0)
    last_visit = Column(DateTime)
    cases_opened = Column(Integer, default=0)
    status = Column(Enum(StatusEnum), default=StatusEnum.neutral)
    inventory = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())