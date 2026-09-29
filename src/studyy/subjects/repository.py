"""Acesso a dados de materias.

Recebe a sessao, nao cria. Nao da commit. Entra e sai `Subject`.

SOFT DELETE: nada e apagado de verdade aqui. Ver o docstring do
TopicRepository para o raciocinio completo.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from studyy.subjects.models import Subject

if TYPE_CHECKING:
    from sqlalchemy.engine import CursorResult


class SubjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, subject_id: int) -> Subject | None:
        result = await self._session.execute(
            select(Subject).where(Subject.id == subject_id, Subject.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_deleted_by_id(self, subject_id: int) -> Subject | None:
        result = await self._session.execute(
            select(Subject).where(Subject.id == subject_id, Subject.deleted_at.is_not(None))
        )
        return result.scalar_one_or_none()

    async def exists_by_id(self, subject_id: int) -> bool:
        query = select(exists().where(Subject.id == subject_id, Subject.deleted_at.is_(None)))
        return bool(await self._session.scalar(query))

    async def list_all(self) -> list[Subject]:
        result = await self._session.execute(
            select(Subject).where(Subject.deleted_at.is_(None)).order_by(Subject.name)
        )
        return list(result.scalars().all())

    async def list_deleted(self) -> list[Subject]:
        """A lixeira, para a interface poder oferecer restauracao."""
        result = await self._session.execute(
            select(Subject)
            .where(Subject.deleted_at.is_not(None))
            .order_by(Subject.deleted_at.desc())
        )
        return list(result.scalars().all())

    async def exists_with_name(self, name: str, *, excluding_id: int | None = None) -> bool:
        condicoes = []
        if excluding_id is not None:
            condicoes.append(Subject.id != excluding_id)

        query = select(
            exists().where(Subject.name == name, Subject.deleted_at.is_(None), *condicoes)
        )
        return bool(await self._session.scalar(query))

    async def add(self, subject: Subject) -> None:
        self._session.add(subject)

    async def soft_delete(self, subject: Subject, at: datetime) -> None:
        subject.deleted_at = at

    async def restore(self, subject: Subject) -> None:
        subject.deleted_at = None

    async def purge(self, before: datetime) -> int:
        result = await self._session.execute(
            delete(Subject).where(Subject.deleted_at.is_not(None), Subject.deleted_at < before)
        )
        return int(cast("CursorResult[Any]", result).rowcount)
