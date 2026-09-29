"""Contrato HTTP de materias.

Estes schemas existem para desenhar o JSON da API, e nao descem para o service:
ele recebe `str` e devolve `Subject`. Se o service conhecesse TopicIn/SubjectIn,
renomear um campo do JSON quebraria regra de negocio.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubjectIn(BaseModel):
    name: str


class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SubjectTrashOut(BaseModel):
    """Schema separado porque so a lixeira precisa expor `deleted_at`.

    Poderia ser um campo opcional no SubjectOut, mas ali ele seria sempre nulo
    -- a listagem normal so devolve materias vivas.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    deleted_at: datetime
