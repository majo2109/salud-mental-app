from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Entrenador
from db import get_session
from sqlalchemy.exc import IntegrityError 

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

@router.post("/")
def crear_entrenador(entrenador: Entrenador, session: Session = Depends(get_session)):
    try:
        session.add(entrenador)
        session.commit()
        session.refresh(entrenador)
        return entrenador
    except IntegrityError as e:
        session.rollback() 
        print(f"Error de Integridad de Base de Datos al crear entrenador: {e}")
        raise HTTPException(status_code=400, detail="Error al crear entrenador: Cedula duplicada o campo obligatorio faltante.")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error interno del servidor al crear el entrenador.")

@router.get("/")
def listar_entrenadores(session: Session = Depends(get_session)):
    return session.exec(select(Entrenador).where(Entrenador.estado == True)).all()

@router.put("/{entrenador_id}")
def actualizar_entrenador(entrenador_id: int, entrenador_actualizado: Entrenador, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador or not entrenador.estado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    update_data = entrenador_actualizado.dict(exclude_unset=True)
    entrenador.sqlmodel_update(update_data)
    
    try:
        session.add(entrenador)
        session.commit()
        session.refresh(entrenador)
        return entrenador
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar entrenador: Cedula duplicada.")

@router.delete("/{entrenador_id}")
def eliminar_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    entrenador.estado = False
    session.add(entrenador)
    session.commit()
    return {"mensaje": "Entrenador eliminado (borrado lógico)"}