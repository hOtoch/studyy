"""Tudo que sabe que existe um banco de dados mora aqui.

Hoje e um arquivo. Na Fase 5 vira o adaptador de persistencia de cada Bounded
Context. Manter isolado agora e o que torna aquela mudanca barata depois.

Repare no que este modulo NAO faz: ele nao cria o engine no momento do import.
O engine nasce no `lifespan` da aplicacao e vive em `app.state`. Assim:

- importar o modulo nao abre conexao nem le configuracao;
- o teste pode montar uma app com outro engine sem monkeypatch;
- o shutdown tem onde fechar o pool.
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from studyy.config import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        str(settings.database_url),
        echo=settings.database_echo,
        pool_pre_ping=True,  # descarta conexao morta antes de usar
    )


def create_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,  # objetos continuam usaveis depois do commit
        autoflush=False,
    )


async def session_scope(
    factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with factory() as session:
        yield session
