"""Rotas de anotacoes.

Mesmo formato dos outros dois: traduzir, chamar, traduzir de volta.
"""

from typing import TypedDict

from fastapi import APIRouter, status

from studyy.dependencies import NoteServiceDep
from studyy.notes.schemas import NoteIn, NoteOut

router = APIRouter(tags=["notes"])


class DeletedPayload(TypedDict):
    deleted: int


@router.get("/topics/{topic_id}/notes")
async def list_notes(topic_id: int, service: NoteServiceDep) -> list[NoteOut]:
    notes = await service.list_by_topic(topic_id)
    return [NoteOut.model_validate(n) for n in notes]


@router.post("/topics/{topic_id}/notes", status_code=status.HTTP_201_CREATED)
async def create_note(topic_id: int, payload: NoteIn, service: NoteServiceDep) -> NoteOut:
    note = await service.create(topic_id, payload.title, payload.content)
    return NoteOut.model_validate(note)


@router.get("/notes/{note_id}")
async def get_note(note_id: int, service: NoteServiceDep) -> NoteOut:
    note = await service.get(note_id)
    return NoteOut.model_validate(note)


@router.put("/notes/{note_id}")
async def edit_note(note_id: int, payload: NoteIn, service: NoteServiceDep) -> NoteOut:
    note = await service.edit(note_id, payload.title, payload.content)
    return NoteOut.model_validate(note)


@router.delete("/notes/{note_id}")
async def delete_note(note_id: int, service: NoteServiceDep) -> DeletedPayload:
    await service.delete(note_id)
    return {"deleted": note_id}


@router.post("/notes/{note_id}/restore")
async def restore_note(note_id: int, service: NoteServiceDep) -> NoteOut:
    note = await service.restore(note_id)
    return NoteOut.model_validate(note)
