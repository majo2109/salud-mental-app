from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from models import Deportista, Entrenador, Evaluacion
from db import get_session
from main import templates

router = APIRouter()


# LISTAR DEPORTISTAS (HTML)
@router.get("/deportistas", response_class=HTMLResponse)
def lista_deportistas(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == True)
    ).all()
    return templates.TemplateResponse(
        "deportistas.html",
        {"request": request, "deportistas": deportistas},
    )


# FORMULARIO (HTML)
@router.get("/deportistas/nuevo", response_class=HTMLResponse)
def form_deportista(request: Request):
    return templates.TemplateResponse(
        "crear_deportista.html",
        {"request": request},
    )


# CREAR (POST HTML)
@router.post("/deportistas/nuevo")
def crear_deportista_web(
    nombre: str = Form(...),
    edad: int = Form(...),
    disciplina: str = Form(...),
    session: Session = Depends(get_session),
):
    nuevo = Deportista(
        nombre=nombre,
        edad=edad,
        disciplina=disciplina,
        estado=True,
    )
    session.add(nuevo)
    session.commit()
    return RedirectResponse(url="/deportistas", status_code=303)
