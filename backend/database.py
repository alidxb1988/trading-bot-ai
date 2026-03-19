"""
SQLite database setup via SQLAlchemy async.
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# ── ORM Models ────────────────────────────────────────────────────────────────

class Trade(Base):
    __tablename__ = "trades"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(String, unique=True, index=True)
    exchange   = Column(String)
    symbol     = Column(String, index=True)
    strategy   = Column(String)
    side       = Column(String)          # buy / sell
    amount     = Column(Float)
    price      = Column(Float)
    cost       = Column(Float)
    pnl        = Column(Float, default=0.0)
    pnl_pct    = Column(Float, default=0.0)
    status     = Column(String, default="open")   # open / closed / cancelled
    leverage   = Column(Integer, default=1)
    stop_loss  = Column(Float, nullable=True)
    take_profit= Column(Float, nullable=True)
    opened_at  = Column(DateTime, default=datetime.utcnow)
    closed_at  = Column(DateTime, nullable=True)
    meta       = Column(Text, default="{}")       # JSON extra data


class BotConfig(Base):
    __tablename__ = "bot_config"

    id        = Column(Integer, primary_key=True)
    key       = Column(String, unique=True, index=True)
    value     = Column(Text)
    updated_at= Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PerformanceSnapshot(Base):
    __tablename__ = "performance_snapshots"

    id            = Column(Integer, primary_key=True)
    timestamp     = Column(DateTime, default=datetime.utcnow, index=True)
    balance       = Column(Float)
    equity        = Column(Float)
    open_pnl      = Column(Float, default=0.0)
    daily_pnl     = Column(Float, default=0.0)
    total_trades  = Column(Integer, default=0)
    winning_trades= Column(Integer, default=0)
    strategy      = Column(String, default="all")


# ── Helpers ───────────────────────────────────────────────────────────────────

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
