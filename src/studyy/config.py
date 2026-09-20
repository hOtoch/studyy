"""A unica porta por onde o ambiente entra no sistema.

Em nenhum outro lugar do projeto deve existir `os.getenv()`. Se voce precisa de
um valor de configuracao, ele chega aqui primeiro e e passado adiante.

O motivo nao e organizacao, e acoplamento: `os.getenv()` espalhado cria uma
dependencia invisivel num singleton global mutavel (o ambiente do processo).
Nada na assinatura de uma funcao revela que ela le o ambiente. O mesmo problema
do `datetime.now()`, que na Fase 5 vira o port `Clock`.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "test", "preview", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    environment: Environment = "local"
    debug: bool = False

    database_url: PostgresDsn = Field(
        description="DSN async do Postgres (postgresql+asyncpg://...)",
    )
    database_echo: bool = Field(
        default=False,
        description="Loga todo SQL emitido. Util na Fase 11 para cacar N+1.",
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Fabrica cacheada das configuracoes.

    E uma funcao, e nao um `settings = Settings()` no nivel do modulo, por dois
    motivos:

    1. Importar um modulo nao deveria ter efeito colateral. Com o singleton no
       import, `import studyy.config` ja le o disco e ja pode falhar.
    2. Em teste da para sobrescrever com `get_settings.cache_clear()` ou via
       `dependency_overrides` do FastAPI. Com o singleton, nao da.

    Isto e o embriao do Composition Root da Fase 5.
    """
    return Settings()  # type: ignore[call-arg]  # pydantic-settings le do ambiente
