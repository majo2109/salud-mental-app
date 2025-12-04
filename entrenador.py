from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models import Entrenador
from db import get_session

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])


@router.post("/", response_model=Entrenador)
def crear_entrenador(
    entrenador: Entrenador,
    session: Session = Depends(get_session)
):
    session.add(entrenador)
    session.commit()
    session.refresh(entrenador)
    return entrenador


@router.get("/", response_model=List[Entrenador])
def listar_entrenadores(session: Session = Depends(get_session)):
    consulta = select(Entrenador).where(Entrenador.estado == True)
    return session.exec(consulta).all()


@router.get("/{entrenador_id}", response_model=Entrenador)
def obtener_entrenador(
    entrenador_id: int,
    session: Session = Depends(get_session)
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador or not entrenador.estado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador


@router.put("/{entrenador_id}", response_model=Entrenador)
def actualizar_entrenador(
    entrenador_id: int,
    datos: Entrenador,
    session: Session = Depends(get_session)
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador or not entrenador.estado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.nombre = datos.nombre
    entrenador.especialidad = datos.especialidad
    entrenador.experiencia = datos.experiencia
    entrenador.estado = datos.estado

    session.add(entrenador)
    session.commit()
    session.refresh(entrenador)
    return entrenador


@router.delete("/{entrenador_id}")
def eliminar_entrenador(
    entrenador_id: int,
    session: Session = Depends(get_session)
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador or not entrenador.estado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.estado = False
    session.add(entrenador)
    session.commit()
    return {"mensaje": "Entrenador eliminado (borrado lógico)"}
