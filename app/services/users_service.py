from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User

async def get_users(db: AsyncSession, offset: int, limit: int):
    total_query = select(func.count()).select_from(User)
    users_query = select(User).offset(offset).limit(limit)

    total_result = await db.execute(total_query)
    total = total_result.scalar_one()

    users_result = await db.execute(users_query)
    users = users_result.scalars().all()

    return users, total