"""Repositorios em memoria, para testar service sem banco.

Nao sao mocks: nao gravam chamadas nem devolvem valores programados. Sao
implementacoes de verdade, com uma lista Python no lugar do Postgres. O teste
exercita a REGRA, nao a interacao.
"""

from datetime import datetime

from studyy.notes.models import Note
from studyy.subjects.models import Subject
from studyy.topics.models import Topic


class FakeSession:
    """So precisa saber contar commits."""

    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1


class FakeSubjectRepository:
    def __init__(self, subjects: list[Subject] | None = None) -> None:
        self.items: list[Subject] = subjects or []

    async def get_by_id(self, subject_id: int) -> Subject | None:
        return next((s for s in self.items if s.id == subject_id and s.deleted_at is None), None)

    async def exists_by_id(self, subject_id: int) -> bool:
        return await self.get_by_id(subject_id) is not None


class FakeTopicRepository:
    def __init__(self, topics: list[Topic] | None = None) -> None:
        self.items: list[Topic] = topics or []
        self._next_id = 1

    async def get_by_id(self, topic_id: int) -> Topic | None:
        return next((t for t in self.items if t.id == topic_id and t.deleted_at is None), None)

    async def list_by_subject(self, subject_id: int) -> list[Topic]:
        return [t for t in self.items if t.subject_id == subject_id and t.deleted_at is None]

    async def exists_with_title(
        self, subject_id: int, title: str, *, excluding_id: int | None = None
    ) -> bool:
        return any(
            t.subject_id == subject_id
            and t.title == title
            and t.deleted_at is None
            and t.id != excluding_id
            for t in self.items
        )

    async def add(self, topic: Topic) -> None:
        topic.id = self._next_id
        self._next_id += 1
        self.items.append(topic)

    async def soft_delete(self, topic: Topic, at: datetime) -> None:
        topic.deleted_at = at


class FakeNoteRepository:
    def __init__(self) -> None:
        self.items: list[Note] = []

    async def soft_delete_by_topics(self, topic_ids: list[int], at: datetime) -> None:
        for n in self.items:
            if n.topic_id in topic_ids and n.deleted_at is None:
                n.deleted_at = at
