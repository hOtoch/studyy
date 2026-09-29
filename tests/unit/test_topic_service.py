"""Regras de topico testadas sem banco, sem rede, sem event loop de verdade.

Na Fase 1 a conclusao foi: "para testar a regra do titulo duplicado eu preciso
de Postgres rodando". Este arquivo e a inversao daquela medicao.
"""

import pytest

from studyy.subjects.models import Subject
from studyy.topics.exceptions import (
    DuplicateTopicTitle,
    EmptyTopicTitle,
    SubjectNotFound,
)
from studyy.topics.models import Topic
from studyy.topics.service import TopicService
from tests.fakes import (
    FakeNoteRepository,
    FakeSession,
    FakeSubjectRepository,
    FakeTopicRepository,
)


def build_service(topics: list[Topic] | None = None) -> TopicService:
    """Monta o service com implementacoes em memoria.

    Os `type: ignore` abaixo NAO sao descuido, e sim um diagnostico.

    Em tempo de execucao isto funciona: os fakes tem os metodos certos, e o
    Python nao pede mais que isso. Os cinco testes deste arquivo passam.

    O mypy recusa porque o TopicService declara depender das classes CONCRETAS
    (`topics: TopicRepository`). O contrato dele diz "me de exatamente um
    TopicRepository", em vez de "me de algo que saiba responder estas
    perguntas".

    Ou seja: a substituicao que acabou de funcionar e ilegal pelo tipo. Isso e a
    Fase 2 esbarrando sozinha na Inversao de Dependencia, que e conteudo da
    Fase 3 -- e e a ordem certa de descobrir uma abstracao: nao porque um livro
    mandou, mas porque algo concreto nao pode ser substituido.

    Resolvido na Fase 3 com `typing.Protocol`. Ver DT-008.
    """
    session = FakeSession()
    return TopicService(
        session,  # type: ignore[arg-type]  # ver docstring: DT-008, Fase 3
        FakeTopicRepository(topics),  # type: ignore[arg-type]
        FakeSubjectRepository([Subject(id=1, name="Arquitetura")]),  # type: ignore[arg-type]
        FakeNoteRepository(),  # type: ignore[arg-type]
    )


async def test_recusa_titulo_duplicado_na_mesma_materia() -> None:
    service = build_service([Topic(id=1, subject_id=1, title="Coesao")])

    with pytest.raises(DuplicateTopicTitle):
        await service.create(1, "Coesao")


async def test_aceita_mesmo_titulo_em_materias_diferentes() -> None:
    service = build_service([Topic(id=1, subject_id=2, title="Coesao")])

    topic = await service.create(1, "Coesao")

    assert topic.title == "Coesao"


async def test_normaliza_o_titulo_antes_de_comparar() -> None:
    service = build_service([Topic(id=1, subject_id=1, title="Coesao")])

    with pytest.raises(DuplicateTopicTitle):
        await service.create(1, "  Coesao  ")


async def test_recusa_titulo_vazio() -> None:
    service = build_service()

    with pytest.raises(EmptyTopicTitle):
        await service.create(1, "   ")


async def test_recusa_materia_inexistente() -> None:
    service = build_service()

    with pytest.raises(SubjectNotFound):
        await service.create(999, "Coesao")
