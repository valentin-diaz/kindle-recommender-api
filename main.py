from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import books
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}