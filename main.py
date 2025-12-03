from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Plantillas HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/registros")
async def crear_registro(
    request: Request,
    estado_animo: str = Form(...),
    comentario: str = Form("")
):

    return RedirectResponse(url="/", status_code=303)

@app.post("/feedback")
async def feedback(
    request: Request,
    nombre_usuario: str = Form("Anónimo"),
    mensaje: str = Form("")
):

    return RedirectResponse(url="/", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/registro", response_class=HTMLResponse)
async def registro_get(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@app.post("/registro")
async def registro_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    return RedirectResponse(url="/login", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    
    registros = []  

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "registros": registros
        }
    )


