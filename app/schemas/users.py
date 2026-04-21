from pydantic import BaseModel, ConfigDict, Field

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(min_length=1, max_length=40, examples=["user123"])
    top_category: str = Field(min_length=0, max_length=100, examples=["Literature & Fiction"])
    top_books: str = Field(min_length=0, max_length=150, examples=["B00DNQWXQM,B01N5IB20Q"])

class PaginatedUsersResponse(BaseModel):
    users: list[UserResponse]
    total: int = Field(ge=0, examples=[100])