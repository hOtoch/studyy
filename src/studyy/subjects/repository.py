"""Acesso a dados de materias.

Mesmo formato do TopicRepository: recebe a sessao, nao cria; nao da commit;
entra e sai `Subject`, nunca schema do Pydantic.
"""

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from studyy.subjects.models import Subject


class SubjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, subject_id: int) -> Subject | None:
        return await self._session.get(Subject, subject_id)

    async def exists_by_id(self, subject_id: int) -> bool:
        query = select(exists().where(Subject.id == subject_id))
        return bool(await self._session.scalar(query))

    async def list_all(self) -> list[Subject]:
        result = await self._session.execute(select(Subject).order_by(Subject.name))
        return list(result.scalars().all())

    async def exists_with_name(self, name: str, *, excluding_id: int | None = None) -> bool:
        condicoes = []
        if excluding_id is not None:
            condicoes.append(Subject.id != excluding_id)

        query = select(exists().where(Subject.name == name, *condicoes))
        return bool(await self._session.scalar(query))

    async def add(self, subject: Subject) -> None:
        self._session.add(subject)

    async def delete(self, subject: Subject) -> None:
        await self._session.delete(subject)
