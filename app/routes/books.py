from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import book
from app.schemas.books import BookResponse, PaginatedBooksResponse, SimilarBookResponse
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

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, db: AsyncSession = Depends(get_db)):
    book = await books_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BookResponse.model_validate(book)

@router.get("/{book_id}/similar", response_model=list[SimilarBookResponse])
async def get_similar_books(book_id: str, limit: int = 5, db: AsyncSession = Depends(get_db)):
    similar_books = await books_service.get_similar_books(db, book_id, limit)
    return [SimilarBookResponse(book=BookResponse.model_validate(book), similarity=similarity) for book, similarity in similar_books]