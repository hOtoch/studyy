"""Erros de dominio do modulo de topicos.

Repare que nenhuma delas menciona 404, 409 ou 422. O numero e assunto da camada
de apresentacao. Numa CLI, o mesmo DuplicateTopicTitle viraria uma mensagem no
terminal e um exit code diferente de zero.
"""

from studyy.exceptions import Conflict, Invalid, NotFound


class TopicNotFound(NotFound):
    def __init__(self, topic_id: int) -> None:
        self.topic_id = topic_id
        super().__init__(f"Topico {topic_id} nao encontrado")


class SubjectNotFound(NotFound):
    """O topico pertence a uma materia que nao existe.

    Mora aqui, e nao em `subjects/`, porque quem levanta este erro e o
    TopicService: e uma afirmacao sobre a criacao de um topico, nao sobre a
    materia em si. Se um dia o SubjectService precisar de um erro parecido,
    ele tera o seu proprio.
    """

    def __init__(self, subject_id: int) -> None:
        self.subject_id = subject_id
        super().__init__(f"Materia {subject_id} nao encontrada")


class EmptyTopicTitle(Invalid):
    def __init__(self) -> None:
        super().__init__("Titulo do topico nao pode ser vazio")


class DuplicateTopicTitle(Conflict):
    def __init__(self, subject_id: int, title: str) -> None:
        self.subject_id = subject_id
        self.title = title
        super().__init__(f"A materia {subject_id} ja tem um topico chamado '{title}'")


class TopicNotInTrash(Conflict):
    """Tentativa de restaurar algo que nao esta na lixeira."""

    def __init__(self, topic_id: int) -> None:
        self.topic_id = topic_id
        super().__init__(f"Topico {topic_id} nao esta na lixeira")
