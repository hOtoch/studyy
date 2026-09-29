"""Acesso a dados de anotacoes.

Mesmo formato do TopicRepository: recebe a sessao, nao cria; nao da commit;
entra e sai `Note`, nunca schema do Pydantic.

Nao ha metodo de atualizacao: a sessao rastreia mudancas em objetos carregados,
entao alterar `note.content` ja basta para o UPDATE sair no commit.

O delete_by_topics existe para a cascata, mas repare que ele nao DECIDE nada:
apaga o que mandarem apagar. Quem decide que apagar um topico implica apagar as
anotacoes dele e o service.
"""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.models import Note


class NoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, note_id: int) -> Note | None:
        return await self._session.get(Note, note_id)

    async def list_by_topic(self, topic_id: int) -> list[Note]:
        result = await self._session.execute(
            select(Note).where(Note.topic_id == topic_id).order_by(Note.id)
        )
        return list(result.scalars().all())

    async def add(self, note: Note) -> None:
        self._session.add(note)

    async def delete(self, note: Note) -> None:
        await self._session.delete(note)

    async def delete_by_topics(self, topic_ids: list[int]) -> None:
        """Remove em bloco as anotacoes de varios topicos.

        Existe para a cascata de delecao, orquestrada pelos services de topico
        e materia. E um DELETE unico em vez de carregar cada anotacao para
        remover uma a uma.
        """
        if not topic_ids:
            return
        await self._session.execute(delete(Note).where(Note.topic_id.in_(topic_ids)))
