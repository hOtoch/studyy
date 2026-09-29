"""Erros de dominio do modulo de anotacoes."""

from studyy.exceptions import Conflict, Invalid, NotFound


class NoteNotFound(NotFound):
    def __init__(self, note_id: int) -> None:
        self.note_id = note_id
        super().__init__(f"Anotacao {note_id} nao encontrada")


class TopicNotFound(NotFound):
    """A anotacao pertence a um topico que nao existe.

    Mesmo raciocinio do SubjectNotFound em `topics/exceptions.py`: quem levanta
    e o NoteService, entao o erro e dele. Nao e a mesma classe do
    `topics/exceptions.py`, e nao deve ser.
    """

    def __init__(self, topic_id: int) -> None:
        self.topic_id = topic_id
        super().__init__(f"Topico {topic_id} nao encontrado")


class EmptyNoteTitle(Invalid):
    def __init__(self) -> None:
        super().__init__("Titulo da anotacao nao pode ser vazio")


class EmptyNoteContent(Invalid):
    def __init__(self) -> None:
        super().__init__("Conteudo da anotacao nao pode ser vazio")


class NoteNotInTrash(Conflict):
    """Tentativa de restaurar algo que nao esta na lixeira."""

    def __init__(self, note_id: int) -> None:
        self.note_id = note_id
        super().__init__(f"Anotacao {note_id} nao esta na lixeira")
