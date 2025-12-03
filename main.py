from fastapi import FastAPI
from db import init_db
from routers import deportista, entrenador, evaluacion

app = FastAPI(title="Juego Limpio Mental API")


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(deportista.router)
app.include_router(entrenador.router)
app.include_router(evaluacion.router)

