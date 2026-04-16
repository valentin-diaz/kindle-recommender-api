from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import book
from app.schemas.books import BookResponse
from app.services import books_service

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=list[BookResponse])
async def get_books(page: int = 1, db: AsyncSession = Depends(get_db)):
    return await books_service.get_books(db, page)