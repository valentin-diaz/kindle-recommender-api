from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.book import Book

async def get_books(db: AsyncSession, offset: int = 0, limit: int = 10):
    stmt = select(Book).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_books_count(db: AsyncSession):
    stmt = select(func.count(Book.id)).select_from(Book)
    result = await db.execute(stmt)
    return result.scalar_one()