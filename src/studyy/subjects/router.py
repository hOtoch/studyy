"""Rotas de materias.

Cada rota faz exatamente tres coisas: traduz HTTP para vocabulario do dominio,
chama quem decide, e traduz o resultado de volta.

O que NAO aparece aqui: sessao, select, commit, HTTPException, regra de
negocio. Se alguma dessas voltar a este arquivo, a camada vazou.
"""

from typing import TypedDict

from fastapi import APIRouter, status

from studyy.dependencies import SubjectServiceDep
from studyy.subjects.schemas import SubjectIn, SubjectOut, SubjectTrashOut

router = APIRouter(tags=["subjects"])


class DeletedPayload(TypedDict):
    deleted: int


@router.get("/subjects")
async def list_subjects(service: SubjectServiceDep) -> list[SubjectOut]:
    subjects = await service.list_all()
    return [SubjectOut.model_validate(s) for s in subjects]


# Declarada ANTES de /subjects/{subject_id} de proposito. O FastAPI resolve as
# rotas na ordem em que foram registradas, e "trash" nao e um inteiro valido.
@router.get("/subjects/trash")
async def list_trash(service: SubjectServiceDep) -> list[SubjectTrashOut]:
    subjects = await service.list_trash()
    return [SubjectTrashOut.model_validate(s) for s in subjects]


@router.post("/subjects", status_code=status.HTTP_201_CREATED)
async def create_subject(payload: SubjectIn, service: SubjectServiceDep) -> SubjectOut:
    subject = await service.create(payload.name)
    return SubjectOut.model_validate(subject)


@router.get("/subjects/{subject_id}")
async def get_subject(subject_id: int, service: SubjectServiceDep) -> SubjectOut:
    subject = await service.get(subject_id)
    return SubjectOut.model_validate(subject)


@router.put("/subjects/{subject_id}")
async def rename_subject(
    subject_id: int, payload: SubjectIn, service: SubjectServiceDep
) -> SubjectOut:
    subject = await service.rename(subject_id, payload.name)
    return SubjectOut.model_validate(subject)


@router.delete("/subjects/{subject_id}")
async def delete_subject(subject_id: int, service: SubjectServiceDep) -> DeletedPayload:
    await service.delete(subject_id)
    return {"deleted": subject_id}


@router.post("/subjects/{subject_id}/restore")
async def restore_subject(subject_id: int, service: SubjectServiceDep) -> SubjectOut:
    subject = await service.restore(subject_id)
    return SubjectOut.model_validate(subject)
