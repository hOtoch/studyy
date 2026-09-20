"""O primeiro teste do projeto.

O valor dele nao e testar o healthcheck (que e trivial). E provar que o
pipeline inteiro funciona: o pacote instala, a app monta, o cliente HTTP fala
com ela. Se este teste passa, as Fases 2 a 5 tem rede de seguranca.
"""

import httpx
import pytest
from asgi_lifespan import LifespanManager

from studyy.config import Settings
from studyy.main import create_app


def _settings() -> Settings:
    return Settings(
        environment="test",
        database_url="postgresql+asyncpg://studyy:studyy@localhost:5432/studyy",  # type: ignore[arg-type]
    )


async def test_liveness_nao_depende_do_banco() -> None:
    """Liveness responde mesmo com o banco fora do ar.

    Este teste roda SEM Postgres. Se um dia ele passar a exigir banco,
    alguem quebrou a distincao entre liveness e readiness.
    """
    app = create_app(_settings())
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@pytest.mark.integration
async def test_readiness_consulta_o_banco() -> None:
    """Readiness so passa com Postgres de pe. Marcado como integration."""
    app = create_app(_settings())
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
