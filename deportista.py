from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from db import get_session
from models import Deportista

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ============================================================
# LISTAR DEPORTISTAS ACTIVOS
# ============================================================
@router.get("/deportistas", response_class=HTMLResponse)
def lista_deportistas(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == True)
    ).all()

    return templates.TemplateResponse(
        "deportistas.html",
        {"request": request, "deportistas": deportistas},
    )


# ============================================================
# LISTAR DEPORTISTAS INACTIVOS
# ============================================================
@router.get("/deportistas/inactivos", response_class=HTMLResponse)
def lista_deportistas_inactivos(request: Request, session: Session = Depends(get_session)):
    deportistas = session.exec(
        select(Deportista).where(Deportista.estado == False)
    ).all()

    return templates.TemplateResponse(
        "deportistas_inactivos.html",
        {"request": request, "deportistas": deportistas},
    )


# ============================================================
# FORMULARIO PARA CREAR DEPORTISTA
# ============================================================

