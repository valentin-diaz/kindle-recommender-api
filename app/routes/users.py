from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import user
from app.schemas.users import UserResponse, PaginatedUsersResponse
from app.services import users_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=PaginatedUsersResponse)
async def get_users(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users, total = await users_service.get_users(db, offset, limit)
    users_response = [UserResponse.model_validate(user) for user in users]
    return PaginatedUsersResponse(users=users_response, total=total)