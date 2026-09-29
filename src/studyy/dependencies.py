"""Montagem das dependencias de cada requisicao.

Este e o unico arquivo do projeto que instancia repositorio e service. Em todo
o resto, as classes so aparecem em anotacao de tipo -- ninguem faz
`TopicRepository(...)` no meio de uma rota.

E o Composition Root do sistema, em versao embrionaria. Na Fase 5 ele cresce,
passa a montar casos de uso em vez de services, e ganha o nome proprio.
"""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from studyy.notes.repository import NoteRepository
from studyy.notes.service import NoteService
from studyy.subjects.repository import SubjectRepository
from studyy.subjects.service import SubjectService
from studyy.topics.repository import TopicRepository
from studyy.topics.service import TopicService


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    factory: async_sessionmaker[AsyncSession] = request.app.state.sessionmaker
    async with factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ---------------------------------------------------------------------------
# Repositorios
# ---------------------------------------------------------------------------
def get_subject_repository(session: SessionDep) -> SubjectRepository:
    return SubjectRepository(session)


def get_topic_repository(session: SessionDep) -> TopicRepository:
    return TopicRepository(session)


def get_note_repository(session: SessionDep) -> NoteRepository:
    return NoteRepository(session)


SubjectRepoDep = Annotated[SubjectRepository, Depends(get_subject_repository)]
TopicRepoDep = Annotated[TopicRepository, Depends(get_topic_repository)]
NoteRepoDep = Annotated[NoteRepository, Depends(get_note_repository)]


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
def get_subject_service(
    session: SessionDep,
    subjects: SubjectRepoDep,
    topics: TopicRepoDep,
    notes: NoteRepoDep,
) -> SubjectService:
    return SubjectService(session, subjects, topics, notes)


def get_topic_service(
    session: SessionDep,
    topics: TopicRepoDep,
    subjects: SubjectRepoDep,
    notes: NoteRepoDep,
) -> TopicService:
    return TopicService(session, topics, subjects, notes)


def get_note_service(
    session: SessionDep,
    notes: NoteRepoDep,
    topics: TopicRepoDep,
) -> NoteService:
    return NoteService(session, notes, topics)


SubjectServiceDep = Annotated[SubjectService, Depends(get_subject_service)]
TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]
