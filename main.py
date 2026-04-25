from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import books
from app.routes import users
from app.routes import recommendations
from config import settings
from contextlib import asynccontextmanager
import joblib
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.als_model = joblib.load("./ml/implicit_model.pkl")
    app.state.user_id_mapping = joblib.load("./ml/userid_to_idx.pkl")
    app.state.book_id_mapping = joblib.load("./ml/bookid_to_idx.pkl")
    app.state.id_user_mapping = joblib.load("./ml/idx_to_userid.pkl")
    app.state.id_book_mapping = joblib.load("./ml/idx_to_bookid.pkl")
    app.state.user_item_matrix = joblib.load("./ml/user_item_matrix.pkl")
    app.state.svd_model = joblib.load("./ml/svd_model.pkl")
    yield
    # Aquí puedes colocar cualquier código de limpieza que necesites, como cerrar conexiones a la base de datos
    print("Cerrando la aplicación...")
    app.state.als_model = None
    app.state.user_id_mapping = None
    app.state.book_id_mapping = None
    app.state.id_user_mapping = None
    app.state.id_book_mapping = None
    app.state.user_item_matrix = None
    app.state.svd_model = None
app = FastAPI(lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(recommendations.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)