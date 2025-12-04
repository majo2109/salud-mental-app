from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from sqlalchemy.exc import IntegrityError

from models import Evaluacion
from db import get_session

router = APIRouter(prefix="/evaluaciones-api", tags=["API Evaluaciones"])


@router.post("/", response_model=Evaluacion)
def crear_evaluacion(evaluacion: Evaluacion, session: Session = Depends(get_session)):
    try:
        session.add(evaluacion)
        session.commit()
        session.refresh(evaluacion)
        return evaluacion
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="IDs inválidos: deportista_id o entrenador_id no existen",
        )



@router.get("/", response_model=List[Evaluacion])
def listar_evaluaciones(session: Session = Depends(get_session)):
    consulta = select(Evaluacion).where(Evaluacion.estado == True)
    return session.exec(consulta).all()


@router.get("/{evaluacion_id}", response_model=Evaluacion)
def obtener_evaluacion(
    evaluacion_id: int, session: Session = Depends(get_session)
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion or not evaluacion.estado:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion


@router.put("/{evaluacion_id}", response_model=Evaluacion)
def actualizar_evaluacion(
    evaluacion_id: int,
    datos: Evaluacion,
    session: Session = Depends(get_session),
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
        session.refresh(evaluacion)
        return evaluacion
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="IDs inválidos: deportista_id o entrenador_id no existen",
        )



@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(
    evaluacion_id: int, session: Session = Depends(get_session)
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion or not evaluacion.estado:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    evaluacion.estado = False
    session.add(evaluacion)
    session.commit()
    return {"mensaje": "Evaluación eliminada (borrado lógico)"}
