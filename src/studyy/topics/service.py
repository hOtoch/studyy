"""Regras de negocio de topicos.

Esta camada nao conhece HTTP nem SQL. Ela recebe primitivos, decide, e levanta
erros de dominio. Quem traduz esses erros em codigo de status e a borda.

Os repositorios respondem perguntas; quem transforma resposta em erro e o
service. Por isso nao ha `try/except` aqui: um `None` ou um `False` vindo do
repositorio e um fato, e a decisao de que aquele fato e um problema e tomada
com `if`.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.repository import NoteRepository
from studyy.subjects.repository import SubjectRepository
from studyy.topics.exceptions import (
    DuplicateTopicTitle,
    EmptyTopicTitle,
    SubjectNotFound,
    TopicNotFound,
)
from studyy.topics.models import Topic
from studyy.topics.repository import TopicRepository


class TopicService:
    def __init__(
        self,
        session: AsyncSession,
        topics: TopicRepository,
        subjects: SubjectRepository,
        notes: NoteRepository,
    ) -> None:
        self._session = session
        self._topics = topics
        self._subjects = subjects
        self._notes = notes

    async def list_by_subject(self, subject_id: int) -> list[Topic]:
        if not await self._subjects.exists_by_id(subject_id):
            raise SubjectNotFound(subject_id)
        return await self._topics.list_by_subject(subject_id)

    async def get(self, topic_id: int) -> Topic:
        topic = await self._topics.get_by_id(topic_id)
        if topic is None:
            raise TopicNotFound(topic_id)
        return topic

    async def create(self, subject_id: int, title: str) -> Topic:
        title = title.strip()
        if not title:
            raise EmptyTopicTitle()

        if not await self._subjects.exists_by_id(subject_id):
            raise SubjectNotFound(subject_id)

        if await self._topics.exists_with_title(subject_id, title):
            raise DuplicateTopicTitle(subject_id, title)

        topic = Topic(subject_id=subject_id, title=title)
        await self._topics.add(topic)
        await self._session.commit()
        return topic

    async def rename(self, topic_id: int, title: str) -> Topic:
        title = title.strip()
        if not title:
            raise EmptyTopicTitle()

        topic = await self.get(topic_id)

        if await self._topics.exists_with_title(topic.subject_id, title, excluding_id=topic_id):
            raise DuplicateTopicTitle(topic.subject_id, title)

        topic.title = title
        await self._session.commit()
        return topic

    async def delete(self, topic_id: int) -> None:
        """Apaga o topico e as anotacoes dele.

        ⚠️ Mesma decisao em aberto do SubjectService.delete: a cascata foi
        preservada da Fase 1, nao escolhida. Ver docs/divida-tecnica.md.
        """
        topic = await self.get(topic_id)
        await self._notes.delete_by_topics([topic_id])
        await self._topics.delete(topic)
        await self._session.commit()
