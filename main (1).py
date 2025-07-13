from fastapi import FastAPI
from routers import process_data
import os

app = FastAPI(
    title="Medical AI Backend",
    description="Backend para procesar datos clínicos con diversos modelos de IA",
    version="1.0.0"
)

# Cargar variables de entorno (ej. desde un .env en desarrollo)
from dotenv import load_dotenv
load_dotenv()

app.include_router(process_data.router, prefix="/api/v1", tags=["clinical-processing"])

@app.get("/")
async def read_root():
    return {"message": "Medical AI Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    # Para desarrollo, puedes ejecutar: uvicorn main:app --reload
    # En producción, usar Gunicorn con Uvicorn workers.
    uvicorn.run(app, host="0.0.0.0", port=8000)