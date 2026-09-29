"""Traducao de erro de dominio para resposta HTTP.

Este e o UNICO lugar do projeto que sabe que 404, 409 e 422 existem. Nenhum
service, nenhum repositorio, nenhuma entidade conhece esses numeros.

E e isso que torna o nucleo reaproveitavel fora de HTTP: numa CLI, o mesmo
DuplicateTopicTitle viraria uma mensagem no terminal e um exit code. Trocaria
este arquivo, e nenhuma regra mudaria de lugar.

Na Fase 1 existiam 25 `raise HTTPException` espalhados pelas rotas.
"""

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from studyy.exceptions import Conflict, DomainError, Invalid, NotFound

# A ordem importa: do mais especifico para o mais generico. Hoje as tres
# categorias sao irmas e nao se sobrepoem, mas se um dia alguem criar uma
# subcategoria, ela precisa vir antes da base.
_STATUS_BY_CATEGORY: tuple[tuple[type[DomainError], int], ...] = (
    (NotFound, status.HTTP_404_NOT_FOUND),
    (Conflict, status.HTTP_409_CONFLICT),
    (Invalid, status.HTTP_422_UNPROCESSABLE_CONTENT),
)


async def handle_domain_error(request: Request, exc: Exception) -> Response:
    """Converte qualquer DomainError na resposta HTTP correspondente.

    O fallback e 400, e nao 500, porque um DomainError E uma recusa legitima --
    o servidor nao falhou, ele disse nao. Cair aqui significa que alguem criou
    um erro herdando direto de DomainError sem escolher categoria.
    """
    for category, http_status in _STATUS_BY_CATEGORY:
        if isinstance(exc, category):
            return JSONResponse(status_code=http_status, content={"detail": str(exc)})

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})


def register_error_handlers(app: FastAPI) -> None:
    """Registra UM handler para toda a hierarquia.

    O Starlette percorre o MRO da excecao ao procurar handler, entao registrar
    em DomainError captura os catorze erros concretos dos tres modulos.
    """
    app.add_exception_handler(DomainError, handle_domain_error)
