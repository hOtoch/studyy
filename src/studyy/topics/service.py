"""Regras de negocio de topicos.

Esta camada nao conhece HTTP nem SQL. Ela recebe primitivos, decide, e levanta
erros de dominio. Quem traduz esses erros em codigo de status e a borda.

Os repositorios respondem perguntas; quem transforma resposta em erro e o
service. Por isso nao ha `try/except` aqui: um `None` ou um `False` vindo do
repositorio e um fato, e a decisao de que aquele fato e um problema e tomada
com `if`.
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.repository import NoteRepository
from studyy.subjects.repository import SubjectRepository
from studyy.topics.exceptions import (
    DuplicateTopicTitle,
    EmptyTopicTitle,
    SubjectNotFound,
    TopicNotFound,
    TopicNotInTrash,
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
        """Manda o topico e as anotacoes dele para a lixeira.

        Nada e removido do banco. A marca de tempo e a MESMA nos dois niveis,
        e e ela que permite restaurar exatamente o que caiu junto.
        """
        topic = await self.get(topic_id)
        at = datetime.now(UTC)

        await self._notes.soft_delete_by_topics([topic_id], at)
        await self._topics.soft_delete(topic, at)
        await self._session.commit()

    async def restore(self, topic_id: int) -> Topic:
        """Tira o topico da lixeira, junto com as anotacoes que cairam com ele.

        Duas regras nao obvias:

        1. A materia precisa estar viva. Restaurar um topico dentro de uma
           materia que continua na lixeira produziria um orfao invisivel.
        2. O titulo precisa continuar livre. Enquanto o topico estava na
           lixeira, alguem pode ter criado outro com o mesmo nome -- e
           restaurar sem checar violaria a regra de unicidade por um caminho
           que ninguem previu.
        """
        topic = await self._topics.get_deleted_by_id(topic_id)
        if topic is None:
            raise TopicNotInTrash(topic_id)

        if not await self._subjects.exists_by_id(topic.subject_id):
            raise SubjectNotFound(topic.subject_id)

        if await self._topics.exists_with_title(topic.subject_id, topic.title):
            raise DuplicateTopicTitle(topic.subject_id, topic.title)

        at = topic.deleted_at
        assert at is not None  # garantido pelo get_deleted_by_id

        await self._topics.restore(topic)
        await self._notes.restore_by_topics([topic_id], at)
        await self._session.commit()
        return topic
