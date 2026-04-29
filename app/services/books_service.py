from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import book
from app.models.book import Book

async def get_books(db: AsyncSession, offset: int, limit: int, search: str | None = None):
    total_query = select(func.count()).select_from(Book)
    books_query = select(Book)

    if search:
        ts_query = func.websearch_to_tsquery('english', search)

        document = func.to_tsvector(
            'english',
            func.coalesce(Book.title, '') + ' ' + 
            func.coalesce(Book.author_name, '') + ' ' + 
            func.coalesce(Book.description, '')
        )

        match_filter = document.op('@@')(ts_query)

        total_query = total_query.where(match_filter)
        books_query = books_query.where(match_filter)

        books_query = books_query.order_by(func.ts_rank(document, ts_query).desc())

    books_query = books_query.offset(offset).limit(limit)

    total_result = await db.execute(total_query)
    total = total_result.scalar_one()

    books_result = await db.execute(books_query)
    books = books_result.scalars().all()

    return books, total

async def get_books_count(db: AsyncSession):
    stmt = select(func.count(Book.id)).select_from(Book)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_book(db: AsyncSession, book_id: str):
    stmt = select(Book).where(Book.id == book_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_similar_books(db: AsyncSession, book_id: str, limit: int = 5):
    book_stmt = select(Book).where(Book.id == book_id)
    book_result = await db.execute(book_stmt)
    book = book_result.scalar_one_or_none()

    if not book or book.embedding is None:
        return []

    similarity_expr = (
        1 - (Book.embedding.cosine_distance(book.embedding) / 2.0)
    ).label('similarity')    

    similarity_stmt = (
        select(Book, similarity_expr)
        .where(Book.id != book_id)
        .order_by(Book.embedding.cosine_distance(book.embedding).asc())
        .limit(limit)
    )

    similarity_result = await db.execute(similarity_stmt)
    similar_books = [(row.Book, row.similarity) for row in similarity_result.fetchall()]

    return similar_books