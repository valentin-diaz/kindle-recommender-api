from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import book
from app.schemas.books import BookResponse, PaginatedBooksResponse
from app.services import books_service

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=PaginatedBooksResponse)
async def get_books(offset: int = 0, limit: int = 10, search: str | None = None, db: AsyncSession = Depends(get_db)):
    books, total = await books_service.get_books(db, offset, limit, search)
    books_response = [BookResponse.model_validate(book) for book in books]
    return PaginatedBooksResponse(books=books_response, total=total)