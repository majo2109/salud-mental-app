# routes/web.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import get_session
from models import Deportista, Entrenador, Evaluacion

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ============ INICIO ============

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ============ DEPORTISTAS ============

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
    return templates.TemplateResponse(
        "crear_deportista.html",
        {"request": request},
    )

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


# ============ ENTRENADORES ============

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


# ============ EVALUACIONES ============

@router.get("/evaluaciones", response_class=HTMLResponse)
def lista_evaluaciones(request: Request, session: Session = Depends(get_session)):
    evaluaciones = session.exec(
        select(Evaluacion).where(Evaluacion.estado == True)
    ).all()
    return templates.TemplateResponse(
        "evaluaciones.html",
        {"request": request, "evaluaciones": evaluaciones},
    )

@router.get("/evaluaciones/nueva", response_class=HTMLResponse)
def form_evaluacion(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == True)
    ).all()
    entrenadores = session.exec(
        select(Entrenador).where(Entrenador.estado == True)
    ).all()
    return templates.TemplateResponse(
        "crear_evaluacion.html",
        {
            "request": request,
            "deportistas": deportistas,
            "entrenadores": entrenadores,
        },
    )

@router.post("/evaluaciones/nueva")
def crear_evaluacion_web(
    fecha: str = Form(...),
    como_se_sintio: str = Form(...),
    como_estuvo_entrenamiento: str = Form(...),
    nivel_1_10: int = Form(...),
    comentarios_extra: str = Form(""),
    deportista_id: int = Form(...),
    entrenador_id: int = Form(...),
    session: Session = Depends(get_session),
):
    texto_comentarios = f"Nivel de bienestar: {nivel_1_10}/10. {comentarios_extra}".strip()

    nueva = Evaluacion(
        fecha=fecha,
        estado_emocional=como_se_sintio,
        rendimiento=como_estuvo_entrenamiento,
        comentarios=texto_comentarios,
        deportista_id=deportista_id,
        entrenador_id=entrenador_id,
        estado=True,
    )
    session.add(nueva)
    session.commit()
    return RedirectResponse(url="/evaluaciones", status_code=303)
