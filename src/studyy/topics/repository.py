from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from studyy.topics.models import Topic


class TopicRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, topic_id: int) -> Topic | None:
        result = await self._session.get(Topic, topic_id)
        return result

    async def list_by_subject(self, subject_id: int) -> list[Topic]:
        result = await self._session.execute(select(Topic).where(Topic.subject_id == subject_id))
        return list(result.scalars().all())

    async def exists_with_title(
        self, subject_id: int, title: str, *, excluding_id: int | None = None
    ) -> bool:
        condicoes = []
        if excluding_id is not None:
            condicoes.append(Topic.id != excluding_id)

        query = select(
            exists().where(Topic.subject_id == subject_id, Topic.title == title, *condicoes)
        )
        result = await self._session.execute(query)
        return bool(result.scalar())

    async def add(self, topic: Topic) -> None:
        self._session.add(topic)

    async def delete(self, topic: Topic) -> None:
        await self._session.delete(topic)

    async def list_ids_by_subject(self, subject_id: int) -> list[int]:
        """So os ids, para a cascata de delecao de materia.

        Separado do list_by_subject porque quem apaga nao precisa dos dados,
        so das chaves.
        """
        result = await self._session.execute(select(Topic.id).where(Topic.subject_id == subject_id))
        return list(result.scalars().all())

    async def delete_by_subject(self, subject_id: int) -> None:
        await self._session.execute(delete(Topic).where(Topic.subject_id == subject_id))
