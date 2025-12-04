from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models import Deportista
from db import get_session

router = APIRouter(prefix="/deportistas", tags=["Deportistas"])


@router.post("/", response_model=Deportista)
def crear_deportista(
    deportista: Deportista,
    session: Session = Depends(get_session)
):
    session.add(deportista)
    session.commit()
    session.refresh(deportista)
    return deportista


@router.get("/", response_model=List[Deportista])
def listar_deportistas(session: Session = Depends(get_session)):
    consulta = select(Deportista).where(Deportista.estado == True)
    return session.exec(consulta).all()


@router.get("/{deportista_id}", response_model=Deportista)
def obtener_deportista(
    deportista_id: int,
    session: Session = Depends(get_session)
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista or not deportista.estado:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")
    return deportista


@router.put("/{deportista_id}", response_model=Deportista)
def actualizar_deportista(
    deportista_id: int,
    datos: Deportista,
    session: Session = Depends(get_session)
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista or not deportista.estado:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    deportista.nombre = datos.nombre
    deportista.edad = datos.edad
    deportista.disciplina = datos.disciplina
    deportista.estado = datos.estado

    session.add(deportista)
    session.commit()
    session.refresh(deportista)
    return deportista


@router.delete("/{deportista_id}")
def eliminar_deportista(
    deportista_id: int,
    session: Session = Depends(get_session)
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista or not deportista.estado:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    deportista.estado = False
    session.add(deportista)
    session.commit()
    return {"mensaje": "Deportista eliminado (borrado lógico)"}
