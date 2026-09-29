"""Acesso a dados de topicos.

Recebe a sessao, nao cria. Nao da commit. Entra e sai `Topic`.

SOFT DELETE: nenhum metodo aqui apaga de verdade. `soft_delete` marca
`deleted_at`, e TODA consulta filtra `deleted_at IS NULL`.

Esse filtro e a razao pela qual soft delete e seguro neste projeto: existe um
unico arquivo que sabe montar consulta de topico. Na Fase 1, com 8 `select()`
espalhados pelas rotas, bastaria esquecer um para dado apagado reaparecer.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from studyy.topics.models import Topic

if TYPE_CHECKING:
    from sqlalchemy.engine import CursorResult


class TopicRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, topic_id: int) -> Topic | None:
        result = await self._session.execute(
            select(Topic).where(Topic.id == topic_id, Topic.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_deleted_by_id(self, topic_id: int) -> Topic | None:
        """Busca na lixeira. Usado so pela restauracao.

        Metodo separado em vez de um parametro `include_deleted=True` porque
        booleano que muda o comportamento da funcao esconde a intencao de quem
        chama. Aqui o nome diz o que vai acontecer.
        """
        result = await self._session.execute(
            select(Topic).where(Topic.id == topic_id, Topic.deleted_at.is_not(None))
        )
        return result.scalar_one_or_none()

    async def list_by_subject(self, subject_id: int) -> list[Topic]:
        result = await self._session.execute(
            select(Topic)
            .where(Topic.subject_id == subject_id, Topic.deleted_at.is_(None))
            .order_by(Topic.title)
        )
        return list(result.scalars().all())

    async def list_ids_by_subject(self, subject_id: int) -> list[int]:
        result = await self._session.execute(
            select(Topic.id).where(Topic.subject_id == subject_id, Topic.deleted_at.is_(None))
        )
        return list(result.scalars().all())

    async def exists_with_title(
        self, subject_id: int, title: str, *, excluding_id: int | None = None
    ) -> bool:
        condicoes = []
        if excluding_id is not None:
            condicoes.append(Topic.id != excluding_id)

        query = select(
            exists().where(
                Topic.subject_id == subject_id,
                Topic.title == title,
                Topic.deleted_at.is_(None),
                *condicoes,
            )
        )
        return bool(await self._session.scalar(query))

    async def add(self, topic: Topic) -> None:
        self._session.add(topic)

    async def soft_delete(self, topic: Topic, at: datetime) -> None:
        topic.deleted_at = at

    async def soft_delete_by_subject(self, subject_id: int, at: datetime) -> None:
        """Manda para a lixeira os topicos vivos de uma materia.

        Só os vivos: um topico ja apagado antes mantem o `deleted_at` original,
        para nao voltar junto quando a materia for restaurada.
        """
        await self._session.execute(
            update(Topic)
            .where(Topic.subject_id == subject_id, Topic.deleted_at.is_(None))
            .values(deleted_at=at)
        )

    async def restore(self, topic: Topic) -> None:
        topic.deleted_at = None

    async def restore_by_subject(self, subject_id: int, at: datetime) -> list[int]:
        """Restaura os topicos que cairam JUNTO com a materia.

        A comparacao e pela marca de tempo exata. Topicos apagados em outro
        momento tem `deleted_at` diferente e continuam na lixeira.

        Devolve os ids restaurados para que as anotacoes deles sejam restauradas
        na sequencia.
        """
        result = await self._session.execute(
            update(Topic)
            .where(Topic.subject_id == subject_id, Topic.deleted_at == at)
            .values(deleted_at=None)
            .returning(Topic.id)
        )
        return list(result.scalars().all())

    async def purge(self, before: datetime) -> int:
        """Remocao definitiva do que esta na lixeira ha tempo demais.

        Existe, mas nada chama ainda: falta o agendador, que e da Fase 12.
        Por enquanto da para rodar na mao.
        """
        result = await self._session.execute(
            delete(Topic).where(Topic.deleted_at.is_not(None), Topic.deleted_at < before)
        )
        return int(cast("CursorResult[Any]", result).rowcount)
