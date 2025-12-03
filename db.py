from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida. Revisa tu archivo .env")

# Engine hacia Supabase (Pooler)
engine = create_engine(
    DATABASE_URL,
    echo=True,   # si te cansa el ruido, pon False
)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
