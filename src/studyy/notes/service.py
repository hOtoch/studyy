"""Regras de negocio de anotacoes.

Mesmo formato do TopicService: recebe primitivos, decide com `if`, levanta erro
de dominio. Sem HTTP, sem try/except.

Diferenca em relacao aos outros dois: nao ha regra de unicidade aqui. Duas
anotacoes com o mesmo titulo no mesmo topico sao legitimas -- voce pode fazer
duas anotacoes chamadas "Aula 1" em dias diferentes. Repare que isso e uma
decisao de dominio, nao um esquecimento: a ausencia de regra tambem e desenho.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.exceptions import (
    EmptyNoteContent,
    EmptyNoteTitle,
    NoteNotFound,
    TopicNotFound,
)
from studyy.notes.models import Note
from studyy.notes.repository import NoteRepository
from studyy.topics.repository import TopicRepository


class NoteService:
    def __init__(
        self,
        session: AsyncSession,
        notes: NoteRepository,
        topics: TopicRepository,
    ) -> None:
        self._session = session
        self._notes = notes
        self._topics = topics

    async def list_by_topic(self, topic_id: int) -> list[Note]:
        if await self._topics.get_by_id(topic_id) is None:
            raise TopicNotFound(topic_id)
        return await self._notes.list_by_topic(topic_id)

    async def get(self, note_id: int) -> Note:
        note = await self._notes.get_by_id(note_id)
        if note is None:
            raise NoteNotFound(note_id)
        return note

    async def create(self, topic_id: int, title: str, content: str) -> Note:
        title, content = self._normalize(title, content)

        if await self._topics.get_by_id(topic_id) is None:
            raise TopicNotFound(topic_id)

        note = Note(topic_id=topic_id, title=title, content=content)
        await self._notes.add(note)
        await self._session.commit()
        return note

    async def edit(self, note_id: int, title: str, content: str) -> Note:
        title, content = self._normalize(title, content)

        note = await self.get(note_id)
        note.title = title
        note.content = content

        await self._session.commit()
        return note

    async def delete(self, note_id: int) -> None:
        note = await self.get(note_id)
        await self._notes.delete(note)
        await self._session.commit()

    @staticmethod
    def _normalize(title: str, content: str) -> tuple[str, str]:
        """Normaliza e valida os dois campos.

        Extraido porque `create` e `edit` aplicam exatamente as mesmas regras.
        No TopicService a duplicacao era de duas linhas e nao valia; aqui sao
        seis, e as regras mudariam juntas.

        E sincrono e estatico de proposito: nao espera nada, nao usa estado.
        Nem toda funcao precisa ser `async`.
        """
        title = title.strip()
        content = content.strip()
        if not title:
            raise EmptyNoteTitle()
        if not content:
            raise EmptyNoteContent()
        return title, content
