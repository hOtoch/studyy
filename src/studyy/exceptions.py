"""Vocabulario de erro da aplicacao.

Aqui mora apenas a classe base. Os erros concretos vivem no modulo a que
pertencem (`topics/exceptions.py`, `subjects/exceptions.py`), porque um erro
como DuplicateTopicTitle so faz sentido dentro do assunto dele.

O que esta classe existe para permitir: a camada de apresentacao registra UM
handler para DomainError e traduz todos os filhos de uma vez, sem precisar
conhecer cada um.

Nenhuma classe aqui conhece codigo HTTP. A traducao acontece na borda.
"""


class DomainError(Exception):
    """Algo que a aplicacao recusou por uma razao de negocio.

    Nao confundir com erro de programacao (TypeError, AttributeError) nem com
    falha de infraestrutura (banco fora do ar). Um DomainError e uma resposta
    legitima do sistema, nao um defeito.
    """
