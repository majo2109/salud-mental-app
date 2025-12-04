from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import get_session
from models import Deportista, Entrenador, Evaluacion  # y Feedback si lo usas

router = APIRouter()

# AQUÍ creamos el objeto templates, SIN importar main
templates = Jinja2Templates(directory="templates")


# ============================
# HOME
# ============================
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# (aquí van tus demás rutas web: dashboard, deportistas, entrenadores, evaluaciones, etc.)
# Ejemplo deportistas:

@router.get("/deportistas", response_class=HTMLResponse)
def lista_deportistas(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == True)
    ).all()
    return templates.TemplateResponse(
        "deportistas.html",
        {"request": request, "deportistas": deportistas},
    )

@router.get("/deportistas/nuevo", response_class=HTMLResponse)
def form_deportista(request: Request):
    return templates.TemplateResponse("crear_deportista.html", {"request": request})

@router.post("/deportistas/nuevo")
def crear_deportista_web(
    nombre: str = Form(...),
    edad: int = Form(...),
    disciplina: str = Form(...),
    session: Session = Depends(get_session),
):
    nuevo = Deportista(nombre=nombre, edad=edad, disciplina=disciplina, estado=True)
    session.add(nuevo)
    session.commit()
    return RedirectResponse(url="/deportistas", status_code=303)
