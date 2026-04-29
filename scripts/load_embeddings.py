# python3 -m scripts.load_embeddings
import asyncio
import joblib
from sqlalchemy import text
from tqdm import tqdm
from app.db.database import SessionLocal 

async def cargar_embeddings():
    print("Cargando diccionario de embeddings...")
    embeddings_dict = joblib.load("ml/book_embeddings.pkl")
    items = list(embeddings_dict.items())
    batch_size = 100

    print("Conectando a la base de datos...")
    # 1. ABRIR SESIÓN ASÍNCRONA: Usamos 'async with' para que se cierre sola al terminar
    async with SessionLocal() as db:
        
        for i in tqdm(range(0, len(items), batch_size)):
            batch = items[i:i + batch_size]
            
            for item_id, vector in batch:
                query = text("UPDATE books SET embedding = :vec WHERE id = :id")
                
                # 2. EJECUTAR CON AWAIT: Toda interacción con la DB debe esperarse
                await db.execute(query, {"vec": str(vector.tolist()), "id": item_id})
            
            # 3. COMMIT CON AWAIT: Guardamos los cambios del lote
            await db.commit()

    print("✅ Embeddings cargados correctamente.")

# 4. EL PUNTO DE ENTRADA ASÍNCRONO
if __name__ == "__main__":
    # asyncio.run() crea el bucle de eventos necesario para correr funciones 'async'
    asyncio.run(cargar_embeddings())