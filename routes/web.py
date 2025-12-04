from fastapi import (
    APIRouter,
    Request,
    Depends,
    Form,
    HTTPException,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import get_session
from models import Deportista, Entrenador, Evaluacion

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ============================
# HOME
# ============================
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


# ============================
# DASHBOARD GENERAL
# ============================
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == True)
    ).all()
    entrenadores = session.exec(
        select(Entrenador).where(Entrenador.estado == True)
    ).all()
    evaluaciones = session.exec(
        select(Evaluacion).where(Evaluacion.estado == True)
    ).all()

    total_deportistas = len(deportistas)
    total_entrenadores = len(entrenadores)
    total_evaluaciones = len(evaluaciones)
    ultima_eval = evaluaciones[-1] if evaluaciones else None

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total_deportistas": total_deportistas,
            "total_entrenadores": total_entrenadores,
            "total_evaluaciones": total_evaluaciones,
            "ultima_eval": ultima_eval,
        },
    )


# ============================
# DEPORTISTAS (CRUD)
# ============================

@router.get("/deportistas", response_class=HTMLResponse)
def lista_deportistas(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == True)
    ).all()
    return templates.TemplateResponse(
        "deportistas.html",
        {"request": request, "deportistas": deportistas},
    )


@router.get("/deportistas/inactivos", response_class=HTMLResponse)
def lista_deportistas_inactivos(
    request: Request,
    session: Session = Depends(get_session),
):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == False)
    ).all()
    return templates.TemplateResponse(
        "deportistas_inactivos.html",
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


@router.get("/deportistas/{deportista_id}/editar", response_class=HTMLResponse)
def form_editar_deportista(
    deportista_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    return templates.TemplateResponse(
        "editar_deportistas.html",          # <--- nombre del template
        {"request": request, "deportista": deportista},
    )


@router.post("/deportistas/{deportista_id}/editar")
def editar_deportista_web(
    deportista_id: int,
    nombre: str = Form(...),
    edad: int = Form(...),
    disciplina: str = Form(...),
    session: Session = Depends(get_session),
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    deportista.nombre = nombre
    deportista.edad = edad
    deportista.disciplina = disciplina

    session.add(deportista)
    session.commit()
    return RedirectResponse(url="/deportistas", status_code=303)


@router.post("/deportistas/{deportista_id}/eliminar")
def eliminar_deportista_web(
    deportista_id: int,
    session: Session = Depends(get_session),
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    deportista.estado = False
    session.add(deportista)
    session.commit()
    return RedirectResponse(url="/deportistas", status_code=303)


@router.post("/deportistas/{deportista_id}/recuperar")
def recuperar_deportista_web(
    deportista_id: int,
    session: Session = Depends(get_session),
):
    deportista = session.get(Deportista, deportista_id)
    if not deportista:
        raise HTTPException(status_code=404, detail="Deportista no encontrado")

    deportista.estado = True
    session.add(deportista)
    session.commit()
    return RedirectResponse(url="/deportistas/inactivos", status_code=303)


# ============================
# ENTRENADORES (CRUD)
# ============================

@router.get("/entrenadores", response_class=HTMLResponse)
def lista_entrenadores(request: Request, session: Session = Depends(get_session)):
    entrenadores = session.exec(
        select(Entrenador).where(Entrenador.estado == True)
    ).all()
    return templates.TemplateResponse(
        "entrenadores.html",
        {"request": request, "entrenadores": entrenadores},
    )


@router.get("/entrenadores/inactivos", response_class=HTMLResponse)
def lista_entrenadores_inactivos(
    request: Request,
    session: Session = Depends(get_session),
):
    entrenadores = session.exec(
        select(Entrenador).where(Entrenador.estado == False)
    ).all()
    return templates.TemplateResponse(
        "entrenadores_inactivos.html",
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


@router.get("/entrenadores/{entrenador_id}/editar", response_class=HTMLResponse)
def form_editar_entrenador(
    entrenador_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    return templates.TemplateResponse(
        "editar_entrenador.html",
        {"request": request, "entrenador": entrenador},
    )


@router.post("/entrenadores/{entrenador_id}/editar")
def editar_entrenador_web(
    entrenador_id: int,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    experiencia: int = Form(...),
    session: Session = Depends(get_session),
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.nombre = nombre
    entrenador.especialidad = especialidad
    entrenador.experiencia = experiencia

    session.add(entrenador)
    session.commit()
    return RedirectResponse(url="/entrenadores", status_code=303)


@router.post("/entrenadores/{entrenador_id}/eliminar")
def eliminar_entrenador_web(
    entrenador_id: int,
    session: Session = Depends(get_session),
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.estado = False
    session.add(entrenador)
    session.commit()
    return RedirectResponse(url="/entrenadores", status_code=303)


@router.post("/entrenadores/{entrenador_id}/recuperar")
def recuperar_entrenador_web(
    entrenador_id: int,
    session: Session = Depends(get_session),
):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.estado = True
    session.add(entrenador)
    session.commit()
    return RedirectResponse(url="/entrenadores/inactivos", status_code=303)


# ============================
# EVALUACIONES (CRUD)
# ============================

@router.get("/evaluaciones", response_class=HTMLResponse)
def lista_evaluaciones(request: Request, session: Session = Depends(get_session)):
    evaluaciones = session.exec(
        select(Evaluacion).where(Evaluacion.estado == True)
    ).all()
    return templates.TemplateResponse(
        "evaluaciones.html",
        {"request": request, "evaluaciones": evaluaciones},
    )


@router.get("/evaluaciones/inactivas", response_class=HTMLResponse)
def lista_evaluaciones_inactivas(
    request: Request,
    session: Session = Depends(get_session),
):
    evaluaciones = session.exec(
        select(Evaluacion).where(Evaluacion.estado == False)
    ).all()
    return templates.TemplateResponse(
        "evaluaciones_inactivas.html",
        {"request": request, "evaluaciones": evaluaciones},
    )


@router.get("/evaluaciones/nueva", response_class=HTMLResponse)
def form_evaluacion(
    request: Request,
    session: Session = Depends(get_session),
):
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
    texto_comentarios = (
        f"Nivel de bienestar: {nivel_1_10}/10. {comentarios_extra}".strip()
    )

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


@router.get("/evaluaciones/{evaluacion_id}/editar", response_class=HTMLResponse)
def form_editar_evaluacion(
    evaluacion_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    return templates.TemplateResponse(
        "editar_evaluacion.html",
        {"request": request, "evaluacion": evaluacion},
    )


@router.post("/evaluaciones/{evaluacion_id}/editar")
def editar_evaluacion_web(
    evaluacion_id: int,
    fecha: str = Form(...),
    estado_emocional: str = Form(...),
    rendimiento: str = Form(...),
    comentarios: str = Form(...),
    session: Session = Depends(get_session),
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    evaluacion.fecha = fecha
    evaluacion.estado_emocional = estado_emocional
    evaluacion.rendimiento = rendimiento
    evaluacion.comentarios = comentarios

    session.add(evaluacion)
    session.commit()
    return RedirectResponse(url="/evaluaciones", status_code=303)


@router.post("/evaluaciones/{evaluacion_id}/eliminar")
def eliminar_evaluacion_web(
    evaluacion_id: int,
    session: Session = Depends(get_session),
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    evaluacion.estado = False
    session.add(evaluacion)
    session.commit()
    return RedirectResponse(url="/evaluaciones", status_code=303)


@router.post("/evaluaciones/{evaluacion_id}/recuperar")
def recuperar_evaluacion_web(
    evaluacion_id: int,
    session: Session = Depends(get_session),
):
    evaluacion = session.get(Evaluacion, evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    evaluacion.estado = True
    session.add(evaluacion)
    session.commit()
    return RedirectResponse(url="/evaluaciones/inactivas", status_code=303)
