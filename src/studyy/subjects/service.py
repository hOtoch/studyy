"""Regras de negocio de materias.

Mesmo formato do TopicService: recebe primitivos, decide com `if`, levanta erro
de dominio. Sem HTTP, sem try/except.

⚠️ Este service depende de TRES repositorios por causa da cascata de lixeira.
Ver DT-002 em `docs/divida-tecnica.md`: na Fase 4 isso vira um evento de
dominio e cada modulo cuida do que e seu.
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.repository import NoteRepository
from studyy.subjects.exceptions import (
    DuplicateSubjectName,
    EmptySubjectName,
    SubjectNotFound,
    SubjectNotInTrash,
)
from studyy.subjects.models import Subject
from studyy.subjects.repository import SubjectRepository
from studyy.topics.repository import TopicRepository


class SubjectService:
    def __init__(
        self,
        session: AsyncSession,
        subjects: SubjectRepository,
        topics: TopicRepository,
        notes: NoteRepository,
    ) -> None:
        self._session = session
        self._subjects = subjects
        self._topics = topics
        self._notes = notes

    async def list_all(self) -> list[Subject]:
        return await self._subjects.list_all()

    async def get(self, subject_id: int) -> Subject:
        subject = await self._subjects.get_by_id(subject_id)
        if subject is None:
            raise SubjectNotFound(subject_id)
        return subject

    async def create(self, name: str) -> Subject:
        name = name.strip()
        if not name:
            raise EmptySubjectName()

        if await self._subjects.exists_with_name(name):
            raise DuplicateSubjectName(name)

        subject = Subject(name=name)
        await self._subjects.add(subject)
        await self._session.commit()
        return subject

    async def rename(self, subject_id: int, name: str) -> Subject:
        name = name.strip()
        if not name:
            raise EmptySubjectName()

        subject = await self.get(subject_id)

        if await self._subjects.exists_with_name(name, excluding_id=subject_id):
            raise DuplicateSubjectName(name)

        subject.name = name
        await self._session.commit()
        return subject

    async def delete(self, subject_id: int) -> None:
        """Manda a materia, seus topicos e as anotacoes deles para a lixeira.

        Nada e removido do banco. A MESMA marca de tempo desce pelos tres
        niveis, e e ela que permite restaurar exatamente o que caiu junto --
        sem ressuscitar o que ja estava apagado antes.
        """
        subject = await self.get(subject_id)
        at = datetime.now(UTC)

        topic_ids = await self._topics.list_ids_by_subject(subject_id)
        await self._notes.soft_delete_by_topics(topic_ids, at)
        await self._topics.soft_delete_by_subject(subject_id, at)
        await self._subjects.soft_delete(subject, at)

        await self._session.commit()

    async def restore(self, subject_id: int) -> Subject:
        """Tira a materia da lixeira, com os topicos e anotacoes que cairam junto."""
        subject = await self._subjects.get_deleted_by_id(subject_id)
        if subject is None:
            raise SubjectNotInTrash(subject_id)

        if await self._subjects.exists_with_name(subject.name):
            raise DuplicateSubjectName(subject.name)

        at = subject.deleted_at
        assert at is not None  # garantido pelo get_deleted_by_id

        await self._subjects.restore(subject)
        restored_topic_ids = await self._topics.restore_by_subject(subject_id, at)
        await self._notes.restore_by_topics(restored_topic_ids, at)

        await self._session.commit()
        return subject

    async def list_trash(self) -> list[Subject]:
        return await self._subjects.list_deleted()
