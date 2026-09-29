"""Rotas de topicos.

Mesmo formato do router de materias: traduzir, chamar, traduzir de volta.
"""

from typing import TypedDict

from fastapi import APIRouter, status

from studyy.dependencies import TopicServiceDep
from studyy.topics.schemas import TopicIn, TopicOut

router = APIRouter(tags=["topics"])


class DeletedPayload(TypedDict):
    deleted: int


@router.get("/subjects/{subject_id}/topics")
async def list_topics(subject_id: int, service: TopicServiceDep) -> list[TopicOut]:
    topics = await service.list_by_subject(subject_id)
    return [TopicOut.model_validate(t) for t in topics]


@router.post("/subjects/{subject_id}/topics", status_code=status.HTTP_201_CREATED)
async def create_topic(subject_id: int, payload: TopicIn, service: TopicServiceDep) -> TopicOut:
    topic = await service.create(subject_id, payload.title)
    return TopicOut.model_validate(topic)


@router.get("/topics/{topic_id}")
async def get_topic(topic_id: int, service: TopicServiceDep) -> TopicOut:
    topic = await service.get(topic_id)
    return TopicOut.model_validate(topic)


@router.put("/topics/{topic_id}")
async def rename_topic(topic_id: int, payload: TopicIn, service: TopicServiceDep) -> TopicOut:
    topic = await service.rename(topic_id, payload.title)
    return TopicOut.model_validate(topic)


@router.delete("/topics/{topic_id}")
async def delete_topic(topic_id: int, service: TopicServiceDep) -> DeletedPayload:
    await service.delete(topic_id)
    return {"deleted": topic_id}


@router.post("/topics/{topic_id}/restore")
async def restore_topic(topic_id: int, service: TopicServiceDep) -> TopicOut:
    topic = await service.restore(topic_id)
    return TopicOut.model_validate(topic)
