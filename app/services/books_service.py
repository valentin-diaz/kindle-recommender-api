from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.book import Book

async def get_books(db: AsyncSession, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    stmt = select(Book).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()