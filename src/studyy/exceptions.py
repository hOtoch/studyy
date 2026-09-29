"""Vocabulario de erro da aplicacao.

Aqui moram a classe base e as tres categorias. Os erros concretos vivem no
modulo a que pertencem (`topics/exceptions.py`, `subjects/exceptions.py`),
porque um erro como DuplicateTopicTitle so faz sentido dentro do assunto dele.

Nenhuma classe aqui conhece codigo HTTP. A traducao acontece em
`error_handlers.py`, na borda.

POR QUE EXISTEM CATEGORIAS

A alternativa seria um dicionario na borda mapeando cada uma das doze excecoes
concretas para um status. Funciona, mas cresce junto com o dominio, e um erro
novo que alguem esqueca de registrar cai num status padrao em silencio.

Com as categorias, o erro novo e OBRIGADO a se classificar -- ele precisa
escolher uma base para herdar. E a borda mapeia tres classes em vez de doze.

O que isso separa: QUAL E A NATUREZA do erro e conhecimento do dominio; QUAL
NUMERO o HTTP usa para ela e conhecimento da borda.
"""


class DomainError(Exception):
    """Algo que a aplicacao recusou por uma razao de negocio.

    Nao confundir com erro de programacao (TypeError, AttributeError) nem com
    falha de infraestrutura (banco fora do ar). Um DomainError e uma resposta
    legitima do sistema, nao um defeito.

    Nao herde direto desta classe: escolha uma das tres categorias abaixo.
    """


class NotFound(DomainError):
    """O que voce pediu nao existe."""


class Conflict(DomainError):
    """O estado atual nao permite esta operacao.

    Diferente de NotFound: a coisa existe, mas nao no estado necessario.
    Ex.: restaurar algo que nao esta na lixeira, ou criar um titulo que outro
    ja ocupa.
    """


class Invalid(DomainError):
    """O que voce mandou nao e aceitavel.

    Diferente de Conflict: nao depende do estado do sistema. Titulo vazio e
    invalido sempre, independente do que exista no banco.
    """
