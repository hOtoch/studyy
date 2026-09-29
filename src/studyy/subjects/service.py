"""Regras de negocio de materias.

Mesmo formato do TopicService: recebe primitivos, decide com `if`, levanta erro
de dominio. Sem HTTP, sem try/except.

⚠️ Este service depende de TRES repositorios por causa da delecao em cascata.
Ver o comentario no metodo `delete` e `docs/divida-tecnica.md`.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from studyy.notes.repository import NoteRepository
from studyy.subjects.exceptions import (
    DuplicateSubjectName,
    EmptySubjectName,
    SubjectNotFound,
)
from studyy.subjects.models import Subject
from studyy.subjects.repository import SubjectRepository
from studyy.topics.repository import TopicRepository


class SubjectService:
    def __init__(
        self,
        session: AsyncSession,
        subjects: SubjectRepository,
        topics: TopicRepository,
        notes: NoteRepository,
    ) -> None:
        self._session = session
        self._subjects = subjects
        self._topics = topics
        self._notes = notes

    async def list_all(self) -> list[Subject]:
        return await self._subjects.list_all()

    async def get(self, subject_id: int) -> Subject:
        subject = await self._subjects.get_by_id(subject_id)
        if subject is None:
            raise SubjectNotFound(subject_id)
        return subject

    async def create(self, name: str) -> Subject:
        name = name.strip()
        if not name:
            raise EmptySubjectName()

        if await self._subjects.exists_with_name(name):
            raise DuplicateSubjectName(name)

        subject = Subject(name=name)
        await self._subjects.add(subject)
        await self._session.commit()
        return subject

    async def rename(self, subject_id: int, name: str) -> Subject:
        name = name.strip()
        if not name:
            raise EmptySubjectName()

        subject = await self.get(subject_id)

        if await self._subjects.exists_with_name(name, excluding_id=subject_id):
            raise DuplicateSubjectName(name)

        subject.name = name
        await self._session.commit()
        return subject

    async def delete(self, subject_id: int) -> None:
        """Apaga a materia, seus topicos e as anotacoes desses topicos.

        ⚠️ DECISAO EM ABERTO. Este comportamento foi preservado da Fase 1 porque
        refatoracao nao muda comportamento -- nao porque seja o certo.

        O problema: apagar uma materia por engano apaga anos de anotacoes em
        silencio, sem confirmacao e sem volta. As anotacoes sao o ativo mais
        valioso do Studyy.

        Alternativas a decidir:
          1. Recusar apagar materia que ainda tem topicos (o usuario esvazia antes)
          2. Soft delete: marcar como apagada e nunca remover de fato
          3. Manter a cascata, mas exigir confirmacao explicita na borda

        E o custo estrutural: para cascatear, este service precisa de TopicRepository
        e NoteRepository. Um modulo mexendo nas tabelas dos outros dois. Na Fase 4
        isso vira um evento de dominio (`SubjectDeleted`) e cada modulo cuida do
        que e seu.
        """
        subject = await self.get(subject_id)

        topic_ids = await self._topics.list_ids_by_subject(subject_id)
        await self._notes.delete_by_topics(topic_ids)
        await self._topics.delete_by_subject(subject_id)
        await self._subjects.delete(subject)

        await self._session.commit()
