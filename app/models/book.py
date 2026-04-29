from typing import TYPE_CHECKING, List
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from pgvector.sqlalchemy import Vector

if TYPE_CHECKING:
    from app.models.reviews import Review

class Book(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String(40), primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    categories: Mapped[str] = mapped_column(String(255), nullable=True)
    author_name: Mapped[str] = mapped_column(String(150), nullable=False)
    image_url: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    embedding: Mapped[Vector] = mapped_column(Vector(384), nullable=True)

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="book")