"""
Database configuration and session management.
Uses SQLAlchemy 2.0 async patterns with asyncpg.
"""
from typing import AsyncGenerator
from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, String, DateTime, select, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base, Session
from fastapi import Depends

from app.core.config import settings


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
    future=True,
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get a database session.

    Yields:
        AsyncSession instance
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections."""
    await engine.dispose()


class AuditedBase(Base):
    """
    Base class for all models with audit fields.
    Provides created_at, updated_at, and created_by fields.
    """

    __abstract__ = True

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    created_by = Column(
        String(36),
        nullable=True,
        index=True,
    )


class BaseQuery:
    """Helper class for common query operations."""

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        model,
        id: str,
    ):
        """Get a record by ID."""
        stmt = select(model).where(model.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        session: AsyncSession,
        model,
        skip: int = 0,
        limit: int = 100,
    ):
        """Get all records with pagination."""
        stmt = select(model).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def count(
        session: AsyncSession,
        model,
    ):
        """Count total records."""
        stmt = select(func.count()).select_from(model)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def delete_by_id(
        session: AsyncSession,
        model,
        id: str,
    ):
        """Delete a record by ID."""
        stmt = select(model).where(model.id == id)
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if record:
            await session.delete(record)
            await session.commit()
            return True

        return False
