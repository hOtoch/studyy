"""Tabela de topicos."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from studyy.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    # A FK e declarada por string ("subjects.id") e nao importando Subject.
    # Assim `topics` nao passa a depender de `subjects` no nivel de import.
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    title: Mapped[str] = mapped_column(String(200))
