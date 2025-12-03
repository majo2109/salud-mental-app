from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class Deportista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    disciplina: str
    estado: bool = Field(default=True)

    evaluaciones: List["Evaluacion"] = Relationship(back_populates="deportista")

class Entrenador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    especialidad: str
    experiencia: int
    estado: bool = Field(default=True)

    evaluaciones: List["Evaluacion"] = Relationship(back_populates="entrenador")

class Evaluacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    estado_emocional: str
    rendimiento: str
    comentarios: str
    estado: bool = Field(default=True)

    deportista_id: int = Field(foreign_key="deportista.id")
    entrenador_id: int = Field(foreign_key="entrenador.id")

    deportista: Deportista = Relationship(back_populates="evaluaciones")
    entrenador: Entrenador = Relationship(back_populates="evaluaciones")
