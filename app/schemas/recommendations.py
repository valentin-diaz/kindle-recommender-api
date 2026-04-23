from pydantic import BaseModel, ConfigDict, Field
from app.schemas import books

class SingleRecommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book: books.BookResponse
    score: float = Field(ge=0, examples=[4.5])
    already_liked: bool = Field(default=False, examples=[False])

class RecommendationsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(min_length=1, max_length=40, examples=["user123"])
    recommended_books: list[SingleRecommendation] = Field(default=[])