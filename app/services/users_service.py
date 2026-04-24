from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User

async def get_users(db: AsyncSession, offset: int, limit: int, search: str | None = None    ):
    total_query = select(func.count()).select_from(User)
    users_query = select(User)

    if search:
        ts_query = func.websearch_to_tsquery('english', search)

        document = func.to_tsvector(
            'english',
            func.coalesce(User.id, '') + ' ' + 
            func.coalesce(User.top_category, '') + ' ' + 
            func.coalesce(User.top_books, '')
        )

        match_filter = document.op('@@')(ts_query)

        total_query = total_query.where(match_filter)
        users_query = users_query.where(match_filter)

        users_query = users_query.order_by(func.ts_rank(document, ts_query).desc())

    users_query = users_query.offset(offset).limit(limit)

    total_result = await db.execute(total_query)
    total = total_result.scalar_one()

    users_result = await db.execute(users_query)
    users = users_result.scalars().all()

    return users, total

async def get_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()