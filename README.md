# 🧠 Proyecto Integrador – App de Bienestar para Deportistas y Entrenadores

Aplicación web desarrollada con **FastAPI**, **Supabase** y **Render**, diseñada para que **deportistas** y **entrenadores** puedan registrar su estado de ánimo, dejar comentarios de su día y enviar sugerencias al sistema.  

---

## 🎯 Objetivo del Proyecto

Crear una plataforma simple, funcional y desplegada en la nube que permita:

- Registrar cómo se siente el usuario cada día.
- Guardar comentarios o reflexiones diarias.
- Permitir feedback sobre la aplicación.
- Diferenciar usuarios según su **rol**:
  - 👤 Deportista  
  - 🧑‍🏫 Entrenador
- Mostrar un panel de historial (Dashboard).

---

## 🛠️ Tecnologías Utilizadas

| Componente       | Tecnología |
|------------------|-----------|
| Backend          | Python + FastAPI |
| Base de datos    | Supabase (PostgreSQL + API REST) |
| Frontend         | HTML + Jinja2 + Bulma CSS |
| Despliegue       | Render |
| Autenticación    | Cookies simples (próxima mejora: JWT) |
| Estilos extra    | CSS personalizado |

---


---

## 🧪 Requisitos Previos

- Python 3.10+
- Cuenta de Supabase
- Cuenta en Render
- Git

---

## 📥 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/salud-mental-app.git
cd salud-mental-app

##Crear y activar entorno virtual:

python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

##instalar dependecias:
pip install -r requirements.txt

##Ejecutar Localmente:

uvicorn main:app --reload


##Abrir en el navegador:

http://127.0.0.1:8000/


👥 Roles: Deportista y Entrenador

Durante el registro el usuario debe elegir:

Deportista

Entrenador

Esto permite:

Filtrar comportamiento en el Dashboard

Crear vistas personalizadas en el futuro

Registrar tipos de usuarios distintos

😋AUTOR:

Mi nombre es Maria Jose Rincón, soy estudiante de ingenria de sistemas en la universidad catolica de colombia.
Puedes contactarme por mi correo:
mjrincon69@ucatolica.edu.co

o por medio de mi instagram:

majorincon_

Gracias por ver mi proyecto, espero te guste tanto como a mi😘


