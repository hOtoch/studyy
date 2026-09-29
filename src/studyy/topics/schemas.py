"""Contrato HTTP de topicos."""

from pydantic import BaseModel, ConfigDict


class TopicIn(BaseModel):
    title: str


class TopicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_id: int
    title: str
