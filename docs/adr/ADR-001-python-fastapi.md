# ADR-001: Backend em Python 3.12 + FastAPI

- **Status:** aceito
- **Data:** 2026-09-21

## Contexto

O Studyy tem dois objetivos que competem entre si:

1. **Ser um produto que eu uso de verdade** para estudar — anotações, roadmap,
   Pomodoro, gamificação e, na Fase 14, um tutor baseado em RAG sobre as
   próprias anotações.
2. **Ser o veículo para eu aprender arquitetura de software do zero** — SOLID,
   DDD, Clean Architecture, event-driven, sistemas distribuídos.

Restrições reais no momento da decisão:

- Time de uma pessoa, em tempo parcial, desenvolvendo no Windows.
- Sou iniciante em arquitetura. A linguagem precisa não atrapalhar o
  aprendizado do que de fato importa aqui, que não é sintaxe.
- A Fase 14 é toda de IA (embeddings, RAG, agentes). O ecossistema dessa área
  é majoritariamente Python.

## Decisão

Vamos usar **Python 3.12 + FastAPI** no backend, com SQLAlchemy 2.0 async,
Pydantic v2 na borda e uv como gerenciador de dependências.

## Alternativas consideradas

- **Java + Spring Boot** — é o ambiente onde DDD, hexagonal e microsserviços
  têm a literatura mais madura, e o compilador impõe fronteiras de graça.
  Descartado pela curva: eu gastaria energia aprendendo a linguagem e o
  framework em vez de aprender arquitetura, que é o objetivo real. Além disso
  afastaria muito a Fase 14.

- **C# + .NET** — excelente para Clean Architecture, DDD tático e EF Core, com
  tooling forte no Windows. Descartado pelo mesmo motivo do Java (curva
  competindo com o objetivo), somado ao mesmo afastamento da trilha de IA.

- **TypeScript + Node (NestJS)** — seria o menor atrito, já que o frontend vai
  ser TypeScript, e o NestJS já força módulos, camadas e injeção de dependência.
  Descartado porque a Fase 14 ficaria significativamente mais trabalhosa: o
  ecossistema de RAG e agentes em JS existe, mas é derivado do de Python.

## Consequências

- ✅ Caminho curto para a Fase 14. Embeddings, pgvector, SDKs de LLM e
  ferramentas de avaliação são todos primeira classe em Python.
- ✅ Menos atrito de linguagem significa mais atenção sobrando para o que o
  roadmap realmente quer ensinar.
- ✅ FastAPI já tem injeção de dependência (`Depends`), o que ajuda a praticar
  DIP sem construir infraestrutura própria para isso.

- ❌ **Python não impõe nenhuma fronteira arquitetural.** Nada impede um import
  do SQLAlchemy dentro do domínio. Em Java ou C# o compilador e o sistema de
  módulos reclamariam; aqui, não reclama ninguém.
- ❌ A consequência acima cria uma tentação específica e perigosa: reaproveitar
  o model do SQLAlchemy como entidade de domínio "para não duplicar". Isso
  destruiria a Fase 4 inteira.

**Mitigação assumida:** `mypy --strict` desde a Fase 0 e `import-linter` a
partir da Fase 5, ambos rodando no CI. Eles são o atrito artificial que
substitui o compilador. Isso já está registrado como comentário no
`pyproject.toml` e na seção de stack do `ROADMAP.md`.

- 🔄 **Gatilho de reversão:** reescrever este projeto em outra linguagem nunca
  vai valer a pena — o custo é sempre maior que o benefício, e seria trocar
  aprendizado real por retrabalho. O gatilho, então, não é sobre *este*
  projeto, e sim sobre o próximo serviço que eu escrever:

  > Se eu me pegar gastando mais tempo *consertando violações de fronteira que
  > um compilador teria pego* do que escrevendo regra de negócio, a conclusão é
  > que para aquele tipo de sistema uma linguagem com tipos nominais e módulos
  > reais vale o custo da curva.

  Métrica prática para medir isso: número de violações pegas pelo
  `import-linter` no CI por mês, a partir da Fase 5. Se passar de ~4 por mês de
  forma sustentada, a disciplina não está vindo da ferramenta, e sim da minha
  atenção — que é exatamente o recurso que eu queria economizar.
