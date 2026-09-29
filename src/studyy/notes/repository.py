"""Acesso a dados de anotacoes.

Recebe a sessao, nao cria. Nao da commit. Entra e sai `Note`.

Nao ha metodo de atualizacao: a sessao rastreia mudancas em objetos carregados,
entao alterar `note.content` ja basta para o UPDATE sair no commit.

SOFT DELETE: nada e apagado de verdade aqui. Ver o docstring do
TopicRepository para o raciocinio completo.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.models import Note

if TYPE_CHECKING:
    from sqlalchemy.engine import CursorResult


class NoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, note_id: int) -> Note | None:
        result = await self._session.execute(
            select(Note).where(Note.id == note_id, Note.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_deleted_by_id(self, note_id: int) -> Note | None:
        result = await self._session.execute(
            select(Note).where(Note.id == note_id, Note.deleted_at.is_not(None))
        )
        return result.scalar_one_or_none()

    async def list_by_topic(self, topic_id: int) -> list[Note]:
        result = await self._session.execute(
            select(Note)
            .where(Note.topic_id == topic_id, Note.deleted_at.is_(None))
            .order_by(Note.id)
        )
        return list(result.scalars().all())

    async def add(self, note: Note) -> None:
        self._session.add(note)

    async def soft_delete(self, note: Note, at: datetime) -> None:
        note.deleted_at = at

    async def soft_delete_by_topics(self, topic_ids: list[int], at: datetime) -> None:
        """Manda para a lixeira as anotacoes vivas de varios topicos.

        Um UPDATE unico em vez de carregar cada anotacao. E so as vivas: uma
        anotacao ja apagada antes mantem o `deleted_at` original, para nao
        voltar junto numa restauracao do topico.
        """
        if not topic_ids:
            return
        await self._session.execute(
            update(Note)
            .where(Note.topic_id.in_(topic_ids), Note.deleted_at.is_(None))
            .values(deleted_at=at)
        )

    async def restore(self, note: Note) -> None:
        note.deleted_at = None

    async def restore_by_topics(self, topic_ids: list[int], at: datetime) -> None:
        """Restaura as anotacoes que cairam JUNTO, pela marca de tempo exata."""
        if not topic_ids:
            return
        await self._session.execute(
            update(Note)
            .where(Note.topic_id.in_(topic_ids), Note.deleted_at == at)
            .values(deleted_at=None)
        )

    async def purge(self, before: datetime) -> int:
        """Remocao definitiva do que esta na lixeira ha tempo demais.

        Existe, mas nada chama ainda: falta o agendador, que e da Fase 12.
        """
        result = await self._session.execute(
            delete(Note).where(Note.deleted_at.is_not(None), Note.deleted_at < before)
        )
        return int(cast("CursorResult[Any]", result).rowcount)
