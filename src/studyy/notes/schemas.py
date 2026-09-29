"""Contrato HTTP de anotacoes."""

from pydantic import BaseModel, ConfigDict


class NoteIn(BaseModel):
    title: str
    content: str


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    content: str
