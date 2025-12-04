from fastapi import FastAPI
from db import init_db
from deportista import router as deportista_router
from entrenador import router as entrenador_router
from evaluacion import router as evaluacion_router

app = FastAPI(
    title="API Bienestar Deportivo",
    description="Gestión de deportistas, entrenadores y evaluaciones emocionales.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    # Crea las tablas en la BD (Supabase / Render) si no existen
    init_db()

# Rutas para la API
app.include_router(deportista_router)
app.include_router(entrenador_router)
app.include_router(evaluacion_router)
