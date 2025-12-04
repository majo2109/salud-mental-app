from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import get_session
from models import Entrenador

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/entrenadores", response_class=HTMLResponse)
def lista_entrenadores(request: Request, session: Session = Depends(get_session)):
    entrenadores = session.exec(
        select(Entrenador).where(Entrenador.estado == True)
    ).all()
    return templates.TemplateResponse(
        "entrenadores.html",
        {"request": request, "entrenadores": entrenadores},
    )


@router.get("/entrenadores/nuevo", response_class=HTMLResponse)
def form_entrenador(request: Request):
    return templates.TemplateResponse(
        "crear_entrenador.html",
        {"request": request},
    )


@router.post("/entrenadores/nuevo")
def crear_entrenador_web(
    nombre: str = Form(...),
    especialidad: str = Form(...),
    experiencia: int = Form(...),
    session: Session = Depends(get_session),
):
    nuevo = Entrenador(
        nombre=nombre,
        especialidad=especialidad,
        experiencia=experiencia,
        estado=True,
    )
    session.add(nuevo)
    session.commit()
    return RedirectResponse(url="/entrenadores", status_code=303)
