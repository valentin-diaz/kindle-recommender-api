from pydantic import BaseModel, ConfigDict, Field

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(min_length=8, max_length=15, examples=["B00DNQWXQM"])
    title: str = Field(min_length=1, max_length=255, examples=["The Great Gatsby"])
    categories: str = Field(min_length=2, max_length=255, examples=["[  Literature & Fiction]"])
    author_name: str = Field(min_length=2, max_length=255, examples=["F. Scott Fitzgerald"])
    image_url: str = Field(min_length=0, max_length=255, examples=["https://m.media-amazon.com/images/I/51bDQOZv-YL.jpg"])
    description: str = Field(min_length=0, examples=["A classic American novel."])

class PaginatedBooksResponse(BaseModel):
    books: list[BookResponse]
    total: int = Field(ge=0, examples=[100])

class SimilarBookResponse(BaseModel):
    book: BookResponse
    similarity: float = Field(ge=0.0, le=1.0, examples=[0.85])