"""Tabela de anotacoes."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from studyy.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text())

    # NULL = viva. Preenchida = na lixeira.
    # A mesma marca de tempo e usada no pai e nos filhos quando a delecao e em
    # cascata: e isso que permite restaurar so o que caiu junto, sem ressuscitar
    # o que ja estava apagado antes.
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
