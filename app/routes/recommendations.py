from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models import book
from app.schemas.books import BookResponse
from app.schemas.recommendations import SimilarBookContentBasedRecommendation, SimilarBooksContentBasedResponse, Top5RecommendationsResponse, Top5SingleRecommendation, SimilarBookImplicitRecommendation, SimilarBooksImplicitResponse
from app.services import books_service
from implicit.cpu.als import AlternatingLeastSquares
from surprise import SVD
from scipy.sparse import csr_matrix
from app.dependencies import get_als_model, get_svd_model, get_user_id_mapping, get_book_id_mapping, get_id_user_mapping, get_id_book_mapping, get_user_item_matrix

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.get("/top-5/{user_id}", response_model=Top5RecommendationsResponse)
async def get_top_5_recommendations(
    user_id: str, 
    db: AsyncSession = Depends(get_db), 
    als_model: AlternatingLeastSquares = Depends(get_als_model), 
    user_item_matrix: csr_matrix = Depends(get_user_item_matrix),
    user_id_mapping: dict = Depends(get_user_id_mapping), 
    id_book_mapping: dict = Depends(get_id_book_mapping),
    svd_model: SVD = Depends(get_svd_model)
):
    if user_id not in user_id_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_idx = user_id_mapping[user_id]
    candidate_indices, scores = als_model.recommend(user_idx, user_item_matrix[user_idx], N=5, filter_already_liked_items=True)
    
    recommended_books = []
    predicted_ratings = [(id_book_mapping[book_idx], svd_model.predict(user_id, id_book_mapping[book_idx]).est) for book_idx in candidate_indices]
    get_top_5_recommendations = sorted(predicted_ratings, key=lambda x: x[1], reverse=True)[:5]
    for (book_id, pred) in get_top_5_recommendations:
        book_data = await books_service.get_book(db, book_id)
        if book_data:
            recommended_books.append(Top5SingleRecommendation(book=BookResponse.model_validate(book_data), predicted_rating=pred))
            
    
    return Top5RecommendationsResponse(user_id=user_id, recommended_books=recommended_books)

@router.get("/similars-implicit/{book_id}", response_model=SimilarBooksImplicitResponse)
async def get_similar_books_implicit(
    book_id: str, 
    db: AsyncSession = Depends(get_db), 
    als_model: AlternatingLeastSquares = Depends(get_als_model), 
    user_item_matrix: csr_matrix = Depends(get_user_item_matrix),
    book_id_mapping: dict = Depends(get_book_id_mapping), 
    id_book_mapping: dict = Depends(get_id_book_mapping),
    svd_model: SVD = Depends(get_svd_model)
):
    if book_id not in book_id_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book_idx = book_id_mapping[book_id]
    candidate_indices, scores = als_model.similar_items(book_idx, N=10)
    # Obtener tuplas de todos los candidatos con su puntuación, pero sin el primer elemento (que es el mismo libro)
    candidates = [(idx, score) for idx, score in list(zip(candidate_indices, scores))[1:]]

    similar_books = []
    predictions = [
        (id_book_mapping[candidate_idx], svd_model.predict("user123", id_book_mapping[candidate_idx]).est, score) for candidate_idx, score in candidates
    ]
    get_top_5_similars = sorted(predictions, key=lambda x: (x[1] - 1) / 4 * x[2], reverse=True)[:5]
    for book_id, pred, score in get_top_5_similars:
        book_idx = book_id_mapping[book_id]
        book_data = await books_service.get_book(db, book_id)
        if book_data:
            already_liked = user_item_matrix[:, book_idx].sum() > 0
            similar_books.append(SimilarBookImplicitRecommendation(book=BookResponse.model_validate(book_data), predicted_rating=pred, score=score, already_liked=already_liked))
    
    return SimilarBooksImplicitResponse(book_id=book_id, similar_books=similar_books)

@router.get("/similars-content/{book_id}", response_model=SimilarBooksContentBasedResponse)
async def get_similar_books_content_based(book_id: str, limit: int = 5, db: AsyncSession = Depends(get_db)):
    similar_books = await books_service.get_similar_books(db, book_id, limit)
    return SimilarBooksContentBasedResponse(
        book_id=book_id,
        similar_books=[
            SimilarBookContentBasedRecommendation(book=BookResponse.model_validate(book), similarity=similarity)
            for book, similarity in similar_books
        ]
    )