from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import init_db
from deportista import router as deportista_router
from entrenador import router as entrenador_router
from evaluacion import router as evaluacion_router
from routes.web import router as web_router  

app = FastAPI(
    title="Sistema de Bienestar Deportivo",
    description="Gestión de deportistas, entrenadores y evaluaciones emocionales.",
    version="1.0.0",
)

# Archivos estáticos (CSS, imágenes, etc)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup():
    init_db()


# Rutas API (JSON, /api/...)
app.include_router(deportista_router)
app.include_router(entrenador_router)
app.include_router(evaluacion_router)

# Rutas WEB (HTML)
app.include_router(web_router)



