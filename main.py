from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from supabase import create_client, Client
from dotenv import load_dotenv
import os


load_dotenv()  

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en variables de entorno")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI()

# Servir carpeta static para CSS, imágenes, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carpeta de plantillas HTML
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Página principal con formulario de estado de ánimo,
    feedback y contacto.
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# ============================================================
#              FORM PRINCIPAL – ESTADO DE ÁNIMO
# ============================================================

@app.post("/registros")
async def crear_registro(
    request: Request,
    estado_animo: str = Form(...),
    comentario: str = Form("")
):
    """
    Crea un registro de estado de ánimo para el usuario logueado.
    Si no hay usuario en cookie, redirige al login.
    """
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # Guardar en tabla registros
    supabase.table("registros").insert({
        "usuario_id": int(user_id),
        "estado_animo": estado_animo,
        "comentario": comentario if comentario else None,
    }).execute()

    return RedirectResponse(url="/dashboard", status_code=303)


# ============================================================
#                       FEEDBACK SOBRE LA APP
# ============================================================

@app.post("/feedback")
async def feedback(
    request: Request,
    nombre_usuario: str = Form("Anónimo"),
    mensaje: str = Form("")
):
    """
    Guarda un comentario sobre la aplicación en la tabla feedback.
    """
    if mensaje.strip():
        supabase.table("feedback").insert({
            "nombre": nombre_usuario if nombre_usuario else "Anónimo",
            "mensaje": mensaje,
        }).execute()

    return RedirectResponse(url="/", status_code=303)


# ============================================================
#                         LOGIN
# ============================================================

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    """
    Muestra el formulario de login.
    """
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
    )


@app.post("/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Valida correo y contraseña contra la tabla usuarios.
    Si es correcto, guarda user_id en una cookie y redirige al dashboard.
    Si falla, vuelve al login.
    """
    resp = supabase.table("usuarios").select("*") \
        .eq("email", email) \
        .eq("password", password) \
        .execute()

    data = resp.data

    if not data:
        # login fallido
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Correo o contraseña incorrectos"}
        )

    usuario = data[0]
    user_id = usuario["id"]

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user_id", value=str(user_id))

    return response


# ============================================================
#                       REGISTRO DE USUARIO
# ============================================================

@app.get("/registro", response_class=HTMLResponse)
async def registro_get(request: Request):
    """
    Muestra el formulario de registro.
    """
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@app.post("/registro")
async def registro_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    rol: str = Form(...),          # entrenador / deportista
):
    """
    Crea un usuario en la tabla usuarios.
    Por simplicidad, la contraseña se guarda en texto plano.
    (En un proyecto real se debe hashear).
    """

    # Verificar si ya existe el correo
    existe = supabase.table("usuarios").select("id").eq("email", email).execute()
    if existe.data:
        # Ya existe usuario con ese correo: volver a registro o login
        return templates.TemplateResponse(
            "register.html",
            {"request": request}
        )

    supabase.table("usuarios").insert({
        "nombre": name,
        "email": email,
        "password": password,
        "rol": rol,
    }).execute()

    return RedirectResponse(url="/login", status_code=303)


# ============================================================
#                        DASHBOARD
# ============================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Muestra el panel de seguimiento del usuario:
    - información básica del usuario
    - historial de registros
    """
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # Obtener datos del usuario
    resp_user = supabase.table("usuarios").select("*").eq("id", user_id).single().execute()
    usuario = resp_user.data

    # Obtener registros del usuario
    resp_reg = supabase.table("registros") \
        .select("*") \
        .eq("usuario_id", user_id) \
        .order("fecha", desc=True) \
        .execute()

    registros = resp_reg.data

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "registros": registros
        }
    )
