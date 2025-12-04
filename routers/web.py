from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import get_session
from models import Deportista, Entrenador, Evaluacion, Feedback


router = APIRouter(tags=["Web"])
templates = Jinja2Templates(directory="templates")



@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(select(Deportista).where(Deportista.estado == True)).all()
    entrenadores = session.exec(select(Entrenador).where(Entrenador.estado == True)).all()
    evaluaciones = session.exec(select(Evaluacion).where(Evaluacion.estado == True)).all()

    ultimas = (
        session.exec(
            select(Evaluacion).where(Evaluacion.estado == True).order_by(Evaluacion.fecha.desc())
        ).all()[:5]
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_deportistas": len(deportistas),
            "total_entrenadores": len(entrenadores),
            "total_evaluaciones": len(evaluaciones),
            "ultimas_evaluaciones": ultimas,
        },
    )




@router.get("/deportistas", response_class=HTMLResponse)
def listar_deportistas(request: Request, session: Session = Depends(get_session)):
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
def crear_deportista_post(
    nombre: str = Form(...),
    edad: int = Form(...),
    disciplina: str = Form(...),
    session: Session = Depends(get_session),
):
    nuevo = Deportista(nombre=nombre, edad=edad, disciplina=disciplina)
    session.add(nuevo)
    session.commit()
    return RedirectResponse(url="/deportistas", status_code=303)


@router.get("/entrenadores", response_class=HTMLResponse)
def listar_entrenadores(request: Request, session: Session = Depends(get_session)):
    entrenadores = session.exec(
        select(Entrenador).where(Entrenador.estado == True)
    ).all()

    return templates.TemplateResponse(
        "entrenadores.html",
        {"request": request, "entrenadores": entrenadores},
    )


@router.get("/entrenadores/nuevo", response_class=HTMLResponse)
def form_entrenador(request: Request):
    return templates.TemplateResponse("crear_entrenador.html", {"request": request})


@router.post("/entrenadores/nuevo")
def crear_entrenador_post(
    nombre: str = Form(...),
    especialidad: str = Form(...),
    experiencia: int = Form(...),
    session: Session = Depends(get_session),
):
    nuevo = Entrenador(nombre=nombre, especialidad=especialidad, experiencia=experiencia)
    session.add(nuevo)
    session.commit()
    return RedirectResponse(url="/entrenadores", status_code=303)




@router.get("/evaluaciones", response_class=HTMLResponse)
def listar_evaluaciones(request: Request, session: Session = Depends(get_session)):
    evaluaciones = session.exec(
        select(Evaluacion).where(Evaluacion.estado == True)
    ).all()

    return templates.TemplateResponse(
        "evaluaciones.html",
        {"request": request, "evaluaciones": evaluaciones},
    )


@router.get("/evaluaciones/nueva", response_class=HTMLResponse)
def form_evaluacion(request: Request):
    return templates.TemplateResponse("crear_evaluacion.html", {"request": request})


@router.post("/evaluaciones/nueva")
def crear_evaluacion_post(
    fecha: str = Form(...),
    como_se_sintio: str = Form(...),          # "¿Cómo se sintió hoy?"
    como_estuvo_entrenamiento: str = Form(...),  # "¿Qué tal estuvo el entrenamiento hoy?"
    nivel_1_10: int = Form(...),              # "Del 1 al 10, ¿cómo se siente?"
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
    )

    session.add(nueva)
    session.commit()
    return RedirectResponse(url="/evaluaciones", status_code=303)




@router.post("/feedback")
def enviar_feedback(
    nombre: str = Form("Anónimo"),
    correo: str = Form(""),
    mensaje: str = Form(...),
    session: Session = Depends(get_session),
):
    fb = Feedback(
        nombre=nombre if nombre.strip() else "Anónimo",
        correo=correo if correo.strip() else None,
        mensaje=mensaje,
    )
    session.add(fb)
    session.commit()
   
    return RedirectResponse(url="/", status_code=303)
