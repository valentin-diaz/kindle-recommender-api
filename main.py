from fastapi import FastAPI
from app.routes import books

app = FastAPI()

app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}