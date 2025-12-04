from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Entrenador
from db import get_session
from sqlalchemy.exc import IntegrityError

# ANTES: prefix="/entrenadores"
router = APIRouter(prefix="/api/entrenadores", tags=["Entrenadores"])

@router.post("/")
def crear_entrenador(entrenador: Entrenador, session: Session = Depends(get_session)):
    ...

@router.get("/")
def listar_entrenadores(session: Session = Depends(get_session)):
    ...

@router.get("/{entrenador_id}")
def obtener_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    ...
