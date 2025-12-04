from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from models import Evaluacion
from db import get_session

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])


@router.post("/", response_model=Evaluacion)
def crear_evaluacion(
    evaluacion: Evaluacion,
    session: Session = Depends(get_session)
):
    session.add(evaluacion)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al crear evaluación. Revisa deportista_id y entrenador_id."
        )
    session.refresh(evaluacion)
    return evaluacion


@router.get("/", response_model=List[Evaluacion])
def listar_evaluaciones(session: Session = Depends(get_session)):
    consulta = select(Evaluacion).where(Evaluacion.estado == True)
    return session.exec(consulta).all()


@router.get("/{evaluacion_id}", response_model=Evaluacion)
def obtener_evaluacion(
    evaluacion_id: int,
    session: Session = Depends(get_session)
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion or not evaluacion.estado:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion


@router.put("/{evaluacion_id}", response_model=Evaluacion)
def actualizar_evaluacion(
    evaluacion_id: int,
    datos: Evaluacion,
    session: Session = Depends(get_session)
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion or not evaluacion.estado:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    evaluacion.fecha = datos.fecha
    evaluacion.estado_emocional = datos.estado_emocional
    evaluacion.rendimiento = datos.rendimiento
    evaluacion.comentarios = datos.comentarios
    evaluacion.deportista_id = datos.deportista_id
    evaluacion.entrenador_id = datos.entrenador_id
    evaluacion.estado = datos.estado

    try:
        session.add(evaluacion)
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar evaluación. Revisa deportista_id y entrenador_id."
        )
    session.refresh(evaluacion)
    return evaluacion


@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(
    evaluacion_id: int,
    session: Session = Depends(get_session)
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion or not evaluacion.estado:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    evaluacion.estado = False
    session.add(evaluacion)
    session.commit()
    return {"mensaje": "Evaluación eliminada (borrado lógico)"}
