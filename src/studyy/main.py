"""Ponto de entrada HTTP.

`create_app()` e uma fabrica, nao um `app = FastAPI()` global. Isso permite que
o teste construa uma aplicacao com outras configuracoes sem variavel de ambiente
e sem monkeypatch. Na Fase 5 esta funcao cresce e vira o Composition Root.

Este arquivo tinha 379 linhas na Fase 1, com tabelas, schemas, regras de negocio
e 15 rotas dentro. Hoje ele so monta a aplicacao: o que cada modulo faz mora no
proprio modulo.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypedDict

from fastapi import FastAPI, Request, Response, status
from sqlalchemy import text

from studyy.config import Settings, get_settings
from studyy.database import create_engine, create_sessionmaker
from studyy.error_handlers import register_error_handlers
from studyy.notes.router import router as notes_router
from studyy.subjects.router import router as subjects_router
from studyy.topics.router import router as topics_router

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


class HealthPayload(TypedDict):
    status: str


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(settings)
        app.state.engine = engine
        app.state.sessionmaker = create_sessionmaker(engine)
        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(
        title="Studyy",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    register_error_handlers(app)

    @app.get("/health/live", tags=["health"])
    async def live() -> HealthPayload:
        """Liveness: o processo esta vivo?

        NAO consulta o banco de proposito. Se consultasse, uma oscilacao de
        2 segundos no Postgres faria o orquestrador matar um processo saudavel,
        e voce teria restart em loop causado pelo proprio healthcheck.
        """
        return {"status": "alive"}

    @app.get("/health/ready", tags=["health"])
    async def ready(request: Request, response: Response) -> HealthPayload:
        """Readiness: consigo atender requisicao agora?

        Aqui sim o banco entra, porque sem ele a resposta e nao.
        Na Fase 10 o deploy usa este endpoint para decidir entre promover
        a versao nova e fazer rollback.
        """
        engine: AsyncEngine = request.app.state.engine
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "database unavailable"}
        return {"status": "ready"}

    app.include_router(subjects_router)
    app.include_router(topics_router)
    app.include_router(notes_router)

    return app
