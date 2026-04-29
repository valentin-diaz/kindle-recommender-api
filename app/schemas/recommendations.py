from pydantic import BaseModel, ConfigDict, Field
from app.schemas import books

class Top5SingleRecommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book: books.BookResponse
    predicted_rating: float = Field(ge=0, le=5, examples=[4.5])
    already_liked: bool = Field(default=False, examples=[False])

class Top5RecommendationsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(min_length=1, max_length=40, examples=["user123"])
    recommended_books: list[Top5SingleRecommendation] = Field(default=[])

class SimilarBookImplicitRecommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book: books.BookResponse
    predicted_rating: float = Field(ge=0, le=5, examples=[4.5])
    score: float = Field(ge=0, le=1, examples=[0.85])
    already_liked: bool = Field(default=False, examples=[False])

class SimilarBooksImplicitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: str = Field(min_length=8, max_length=15, examples=["B00DNQWXQM"])
    similar_books: list[SimilarBookImplicitRecommendation] = Field(default=[])

class SimilarBookContentBasedRecommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book: books.BookResponse
    score: float = Field(ge=0.0, le=1.0, examples=[0.85])

class SimilarBooksContentBasedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    book_id: str = Field(min_length=8, max_length=15, examples=["B00DNQWXQM"])
    similar_books: list[SimilarBookContentBasedRecommendation] = Field(default=[])