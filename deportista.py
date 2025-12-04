from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Deportista
from db import get_session

router = APIRouter(prefix="/api/deportistas", tags=["API Deportistas"])


# Crear deportista vía API
@router.post("/")
def crear_deportista(deportista: Deportista, session: Session = Depends(get_session)):
    session.add(deportista)
    session.commit()
    session.refresh(deportista)
    return deportista


# Listar todos (API)
@router.get("/")
def listar_deportistas(session: Session = Depends(get_session)):
    query = select(Deportista).where(Deportista.estado == True)
    return session.exec(query).all()


# Obtener por ID (API)
@router.get("/{deportista_id}")
def obtener_deportista(deportista_id: int, session: Session = Depends(get_session)):
    deportista = session.get(Deportista, deportista_id)
    if not deportista or deportista.estado is False:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")
    return deportista

