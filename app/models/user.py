from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.reviews import Review

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(40), primary_key=True, index=True)
    top_category: Mapped[str] = mapped_column(String(100), nullable=True)
    top_books: Mapped[str] = mapped_column(String(150), nullable=True)  # Store as comma-separated string

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")