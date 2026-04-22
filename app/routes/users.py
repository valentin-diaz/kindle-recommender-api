from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import user
from app.schemas.books import BookResponse
from app.schemas.users import UserResponse, PaginatedUsersResponse
from app.services import users_service, books_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=PaginatedUsersResponse)
async def get_users(offset: int = 0, limit: int = 10, search: str | None = None, db: AsyncSession = Depends(get_db)):
    users, total = await users_service.get_users(db, offset, limit, search)
    # Agregar los top_books como parte de la respuesta
    users_response = []
    for user in users:
        book_ids = user.top_books.split(",") if user.top_books else []
        top_books = [await books_service.get_book(db, book_id) for book_id in book_ids]
        user_response = UserResponse(
            id=user.id,
            top_category=user.top_category,
            top_books=[]  # Inicializar como lista vacía, se llenará después de obtener los libros
        )
        user_response.top_books = [BookResponse.model_validate(book) for book in top_books]  # Asignar los objetos BookResponse a la respuesta del usuario
        users_response.append(user_response)
    return PaginatedUsersResponse(users=users_response, total=total)