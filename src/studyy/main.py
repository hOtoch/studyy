"""Ponto de entrada HTTP.

`create_app()` e uma fabrica, nao um `app = FastAPI()` global. Isso permite que
o teste construa uma aplicacao com outras configuracoes sem variavel de ambiente
e sem monkeypatch. Na Fase 5 esta funcao cresce e vira o Composition Root.

=============================================================================
FASE 1 - MONOLITO INGENUO

Tabelas, schemas, regras de negocio e rotas estao todos neste arquivo DE
PROPOSITO. Este nao e o desenho final do Studyy: e o ponto de partida que as
Fases 2 a 5 vao refatorar, um conceito por vez.

Se voce chegou aqui vindo de fora do projeto, leia o ROADMAP.md antes de
concluir qualquer coisa sobre a arquitetura deste sistema.
=============================================================================
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypedDict

from fastapi import FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey, String, Text, delete, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from studyy.config import Settings, get_settings
from studyy.database import create_engine, create_sessionmaker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


# ---------------------------------------------------------------------------
# Tabelas
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    title: Mapped[str] = mapped_column(String(200))


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text())


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class SubjectIn(BaseModel):
    name: str


class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TopicIn(BaseModel):
    title: str


class TopicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_id: int
    title: str


class NoteIn(BaseModel):
    title: str
    content: str


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    content: str


class HealthPayload(TypedDict):
    status: str


class DeletedPayload(TypedDict):
    deleted: int


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

    # -----------------------------------------------------------------------
    # Health
    # -----------------------------------------------------------------------
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

    # -----------------------------------------------------------------------
    # Subjects
    # -----------------------------------------------------------------------
    @app.get("/subjects", tags=["subjects"])
    async def list_subjects(request: Request) -> list[SubjectOut]:
        async with request.app.state.sessionmaker() as session:
            result = await session.execute(select(Subject).order_by(Subject.name))
            return [SubjectOut.model_validate(s) for s in result.scalars().all()]

    @app.post("/subjects", tags=["subjects"], status_code=status.HTTP_201_CREATED)
    async def create_subject(request: Request, payload: SubjectIn) -> SubjectOut:
        name = payload.name.strip()
        if not name:
            raise HTTPException(status_code=422, detail="Nome da materia nao pode ser vazio")

        async with request.app.state.sessionmaker() as session:
            existing = await session.execute(select(Subject).where(Subject.name == name))
            if existing.scalar_one_or_none() is not None:
                raise HTTPException(status_code=409, detail=f"Ja existe a materia '{name}'")

            subject = Subject(name=name)
            session.add(subject)
            await session.commit()
            await session.refresh(subject)
            return SubjectOut.model_validate(subject)

    @app.get("/subjects/{subject_id}", tags=["subjects"])
    async def get_subject(request: Request, subject_id: int) -> SubjectOut:
        async with request.app.state.sessionmaker() as session:
            subject = await session.get(Subject, subject_id)
            if subject is None:
                raise HTTPException(status_code=404, detail="Materia nao encontrada")
            return SubjectOut.model_validate(subject)

    @app.put("/subjects/{subject_id}", tags=["subjects"])
    async def update_subject(request: Request, subject_id: int, payload: SubjectIn) -> SubjectOut:
        name = payload.name.strip()
        if not name:
            raise HTTPException(status_code=422, detail="Nome da materia nao pode ser vazio")

        async with request.app.state.sessionmaker() as session:
            subject = await session.get(Subject, subject_id)
            if subject is None:
                raise HTTPException(status_code=404, detail="Materia nao encontrada")

            existing = await session.execute(
                select(Subject).where(Subject.name == name, Subject.id != subject_id)
            )
            if existing.scalar_one_or_none() is not None:
                raise HTTPException(status_code=409, detail=f"Ja existe a materia '{name}'")

            subject.name = name
            await session.commit()
            await session.refresh(subject)
            return SubjectOut.model_validate(subject)

    @app.delete("/subjects/{subject_id}", tags=["subjects"])
    async def delete_subject(request: Request, subject_id: int) -> DeletedPayload:
        async with request.app.state.sessionmaker() as session:
            subject = await session.get(Subject, subject_id)
            if subject is None:
                raise HTTPException(status_code=404, detail="Materia nao encontrada")

            topics = await session.execute(select(Topic).where(Topic.subject_id == subject_id))
            topic_ids = [t.id for t in topics.scalars().all()]
            if topic_ids:
                await session.execute(delete(Note).where(Note.topic_id.in_(topic_ids)))
                await session.execute(delete(Topic).where(Topic.id.in_(topic_ids)))

            await session.delete(subject)
            await session.commit()
            return {"deleted": subject_id}

    # -----------------------------------------------------------------------
    # Topics
    # -----------------------------------------------------------------------
    @app.get("/subjects/{subject_id}/topics", tags=["topics"])
    async def list_topics(request: Request, subject_id: int) -> list[TopicOut]:
        async with request.app.state.sessionmaker() as session:
            subject = await session.get(Subject, subject_id)
            if subject is None:
                raise HTTPException(status_code=404, detail="Materia nao encontrada")

            result = await session.execute(
                select(Topic).where(Topic.subject_id == subject_id).order_by(Topic.title)
            )
            return [TopicOut.model_validate(t) for t in result.scalars().all()]

    @app.post("/subjects/{subject_id}/topics", tags=["topics"], status_code=201)
    async def create_topic(request: Request, subject_id: int, payload: TopicIn) -> TopicOut:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=422, detail="Titulo do topico nao pode ser vazio")

        async with request.app.state.sessionmaker() as session:
            subject = await session.get(Subject, subject_id)
            if subject is None:
                raise HTTPException(status_code=404, detail="Materia nao encontrada")

            # Regra de negocio: nao pode haver dois topicos com o mesmo titulo
            # dentro da mesma materia.
            existing = await session.execute(
                select(Topic).where(Topic.subject_id == subject_id, Topic.title == title)
            )
            if existing.scalar_one_or_none() is not None:
                raise HTTPException(
                    status_code=409,
                    detail=f"A materia ja tem um topico chamado '{title}'",
                )

            topic = Topic(subject_id=subject_id, title=title)
            session.add(topic)
            await session.commit()
            await session.refresh(topic)
            return TopicOut.model_validate(topic)

    @app.get("/topics/{topic_id}", tags=["topics"])
    async def get_topic(request: Request, topic_id: int) -> TopicOut:
        async with request.app.state.sessionmaker() as session:
            topic = await session.get(Topic, topic_id)
            if topic is None:
                raise HTTPException(status_code=404, detail="Topico nao encontrado")
            return TopicOut.model_validate(topic)

    @app.put("/topics/{topic_id}", tags=["topics"])
    async def update_topic(request: Request, topic_id: int, payload: TopicIn) -> TopicOut:
        title = payload.title.strip()
        if not title:
            raise HTTPException(status_code=422, detail="Titulo do topico nao pode ser vazio")

        async with request.app.state.sessionmaker() as session:
            topic = await session.get(Topic, topic_id)
            if topic is None:
                raise HTTPException(status_code=404, detail="Topico nao encontrado")

            # Regra de negocio: nao pode haver dois topicos com o mesmo titulo
            # dentro da mesma materia.
            existing = await session.execute(
                select(Topic).where(
                    Topic.subject_id == topic.subject_id,
                    Topic.title == title,
                    Topic.id != topic_id,
                )
            )
            if existing.scalar_one_or_none() is not None:
                raise HTTPException(
                    status_code=409,
                    detail=f"A materia ja tem um topico chamado '{title}'",
                )

            topic.title = title
            await session.commit()
            await session.refresh(topic)
            return TopicOut.model_validate(topic)

    @app.delete("/topics/{topic_id}", tags=["topics"])
    async def delete_topic(request: Request, topic_id: int) -> DeletedPayload:
        async with request.app.state.sessionmaker() as session:
            topic = await session.get(Topic, topic_id)
            if topic is None:
                raise HTTPException(status_code=404, detail="Topico nao encontrado")

            await session.execute(delete(Note).where(Note.topic_id == topic_id))
            await session.delete(topic)
            await session.commit()
            return {"deleted": topic_id}

    # -----------------------------------------------------------------------
    # Notes
    # -----------------------------------------------------------------------
    @app.get("/topics/{topic_id}/notes", tags=["notes"])
    async def list_notes(request: Request, topic_id: int) -> list[NoteOut]:
        async with request.app.state.sessionmaker() as session:
            topic = await session.get(Topic, topic_id)
            if topic is None:
                raise HTTPException(status_code=404, detail="Topico nao encontrado")

            result = await session.execute(
                select(Note).where(Note.topic_id == topic_id).order_by(Note.id)
            )
            return [NoteOut.model_validate(n) for n in result.scalars().all()]

    @app.post("/topics/{topic_id}/notes", tags=["notes"], status_code=201)
    async def create_note(request: Request, topic_id: int, payload: NoteIn) -> NoteOut:
        title = payload.title.strip()
        content = payload.content.strip()
        if not title:
            raise HTTPException(status_code=422, detail="Titulo da anotacao nao pode ser vazio")
        if not content:
            raise HTTPException(status_code=422, detail="Conteudo da anotacao nao pode ser vazio")

        async with request.app.state.sessionmaker() as session:
            topic = await session.get(Topic, topic_id)
            if topic is None:
                raise HTTPException(status_code=404, detail="Topico nao encontrado")

            note = Note(topic_id=topic_id, title=title, content=content)
            session.add(note)
            await session.commit()
            await session.refresh(note)
            return NoteOut.model_validate(note)

    @app.get("/notes/{note_id}", tags=["notes"])
    async def get_note(request: Request, note_id: int) -> NoteOut:
        async with request.app.state.sessionmaker() as session:
            note = await session.get(Note, note_id)
            if note is None:
                raise HTTPException(status_code=404, detail="Anotacao nao encontrada")
            return NoteOut.model_validate(note)

    @app.put("/notes/{note_id}", tags=["notes"])
    async def update_note(request: Request, note_id: int, payload: NoteIn) -> NoteOut:
        title = payload.title.strip()
        content = payload.content.strip()
        if not title:
            raise HTTPException(status_code=422, detail="Titulo da anotacao nao pode ser vazio")
        if not content:
            raise HTTPException(status_code=422, detail="Conteudo da anotacao nao pode ser vazio")

        async with request.app.state.sessionmaker() as session:
            note = await session.get(Note, note_id)
            if note is None:
                raise HTTPException(status_code=404, detail="Anotacao nao encontrada")

            note.title = title
            note.content = content
            await session.commit()
            await session.refresh(note)
            return NoteOut.model_validate(note)

    @app.delete("/notes/{note_id}", tags=["notes"])
    async def delete_note(request: Request, note_id: int) -> DeletedPayload:
        async with request.app.state.sessionmaker() as session:
            note = await session.get(Note, note_id)
            if note is None:
                raise HTTPException(status_code=404, detail="Anotacao nao encontrada")

            await session.delete(note)
            await session.commit()
            return {"deleted": note_id}

    return app
