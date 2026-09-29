"""Tabela de materias."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from studyy.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    # NULL = viva. Preenchida = na lixeira.
    # A mesma marca de tempo e usada no pai e nos filhos quando a delecao e em
    # cascata: e isso que permite restaurar so o que caiu junto, sem ressuscitar
    # o que ja estava apagado antes.
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
