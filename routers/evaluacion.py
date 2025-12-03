from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Evaluacion
from db import get_session
from sqlalchemy.exc import IntegrityError 

router = APIRouter(prefix="/evaluacion", tags=["Evaluacion"])

@router.post("/")
def crear_evaluacion(evaluacion: Evaluacion, session: Session = Depends(get_session)):
    try:
        session.add(evaluacion)
        session.commit()
        session.refresh(evaluacion)
        return evaluacion
    except IntegrityError as e:
        session.rollback() 
        print(f"Error de Integridad de Base de Datos al crear evaluación: {e}")
        raise HTTPException(status_code=400, detail="Error al crear evaluación: Verifique que las IDs de deportista y entrenador sean válidas y no haya duplicados.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

@router.get("/")
def listar_evaluacion(session: Session = Depends(get_session)):
    return session.exec(select(Evaluacion).where(Evaluacion.estado == True)).all()

@router.put("/{evaluacion_id}")
def actualizar_evaluacion(evaluacion_id: int, evaluacion_actualizada: Evaluacion, session: Session = Depends(get_session)):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion or not evaluacion.estado:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    update_data = evaluacion_actualizada.dict(exclude_unset=True)
    evaluacion.sqlmodel_update(update_data)
    
    try:
        session.add(evaluacion)
        session.commit()
        session.refresh(evaluacion)
        return evaluacion
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar evaluación: Verifique las IDs de deportista y entrenador.")
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(evaluacion_id: int, session: Session = Depends(get_session)):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    evaluacion.estado = False
    session.add(evaluacion)
    session.commit()
    return {"mensaje": "Evaluación eliminada (borrado lógico)"}