from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import book
from app.schemas.books import BookResponse, PaginatedBooksResponse
from app.services import books_service
from implicit.cpu.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
from app.dependencies import get_als_model, get_user_id_mapping, get_book_id_mapping, get_id_user_mapping, get_id_book_mapping, get_user_item_matrix

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.get("/top-5/{user_id}")
async def get_top_5_recommendations(
    user_id: str, 
    db: AsyncSession = Depends(get_db), 
    als_model: AlternatingLeastSquares = Depends(get_als_model), 
    user_item_matrix: csr_matrix = Depends(get_user_item_matrix),
    user_id_mapping: dict = Depends(get_user_id_mapping), 
    book_id_mapping: dict = Depends(get_book_id_mapping), 
    id_user_mapping: dict = Depends(get_id_user_mapping), 
    id_book_mapping: dict = Depends(get_id_book_mapping)
):
    if user_id not in user_id_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_idx = user_id_mapping[user_id]
    recommended_indices, scores = als_model.recommend(user_idx, user_item_matrix[user_idx], N=5, filter_already_liked_items=True)
    
    recommended_books = []
    for book_idx in recommended_indices:
        book_id = id_book_mapping[book_idx]
        book_data = await books_service.get_book(db, book_id)
        if book_data:
            recommended_books.append(BookResponse.model_validate(book_data))
    
    return recommended_books