from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from db.connection import engine, Base
""" from models.db import Users, Products, Statistics """
from routers.users import usersRouter
from routers.products import productsRouter

# Inicialización de la API
app = FastAPI(
    title="StockOn API",
    description="API para la gestión de usuarios y productos en stockon",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# Endpoint de verificación de salud
@app.get("/healthCheck", tags=["health"])
def health_check():
    try:
        # Ejecuta una consulta simple para verificar la conexión
        with engine.connect() as connection:
            return JSONResponse(content={"status": "ok", "database": "connected"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error de conexión a la base de datos", "Exception": str(e)})
    
app.include_router(usersRouter)
app.include_router(productsRouter)
