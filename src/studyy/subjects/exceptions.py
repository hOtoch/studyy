"""Erros de dominio do modulo de materias."""

from studyy.exceptions import Conflict, Invalid, NotFound


class SubjectNotFound(NotFound):
    """Existe uma classe de mesmo nome em `topics/exceptions.py`, e e proposital.

    Cada modulo tem o seu vocabulario de erro. La, SubjectNotFound e uma
    afirmacao sobre criar um topico numa materia que nao existe; aqui, e sobre
    operar a propria materia. Sao contextos diferentes, e na Fase 4, quando
    virarem Bounded Contexts de verdade, a separacao deixa de ser opcional.

    As duas herdam de DomainError, entao o handler da borda trata ambas sem
    precisar conhecer nenhuma.
    """

    def __init__(self, subject_id: int) -> None:
        self.subject_id = subject_id
        super().__init__(f"Materia {subject_id} nao encontrada")


class EmptySubjectName(Invalid):
    def __init__(self) -> None:
        super().__init__("Nome da materia nao pode ser vazio")


class DuplicateSubjectName(Conflict):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Ja existe a materia '{name}'")


class SubjectNotInTrash(Conflict):
    """Tentativa de restaurar algo que nao esta na lixeira."""

    def __init__(self, subject_id: int) -> None:
        self.subject_id = subject_id
        super().__init__(f"Materia {subject_id} nao esta na lixeira")
