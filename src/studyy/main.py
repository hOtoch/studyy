"""Ponto de entrada HTTP.

`create_app()` e uma fabrica, nao um `app = FastAPI()` global. Isso permite que
o teste construa uma aplicacao com outras configuracoes sem variavel de ambiente
e sem monkeypatch. Na Fase 5 esta funcao cresce e vira o Composition Root.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypedDict

from fastapi import FastAPI, Request, Response, status
from sqlalchemy import text

from studyy.config import Settings, get_settings
from studyy.database import create_engine, create_sessionmaker

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

        O engine vem de `request.app.state`, preenchido no lifespan. Nao ha
        variavel global de engine em lugar nenhum: quem precisa dele, pede.
        """
        engine: AsyncEngine = request.app.state.engine
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"status": "database unavailable"}
        return {"status": "ready"}

    return app
