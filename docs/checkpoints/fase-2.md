# Checkpoint Socrático — Fase 2

> Três perguntas, escolhidas entre as cinco do roadmap por serem as que tratam
> do que de fato aconteceu na construção. As outras duas estão no fim.
>
> Responda sem pesquisar. "Não sei, e o que me confunde é X" é resposta válida.

---

## 1. Você extraiu duas coisas nesta fase: Repository e Service. Qual das duas extrações reduziu mais o acoplamento?

Escolha **uma**. Não vale responder "as duas".

<!-- sua resposta -->

---

## 2. O teste de service roda em menos de 5ms com um repositório em memória. Se ele passasse a levar 2 segundos, o que isso te diria sobre a arquitetura — antes mesmo de você abrir o código?

<!-- sua resposta -->

---

## 3. Os testes com o fake passam, e o `mypy` recusa os quatro argumentos.

Explique **por que** o Python aceita e o `mypy` não. E responda: qual dos dois
está certo?

<!-- sua resposta -->

---

## Perguntas descartadas

**"O seu `Service` ainda recebe a `Session` do SQLAlchemy? Que tipo de
acoplamento é esse?"** — Descartada porque virou a DT-001 antes de ser
perguntada. A resposta já está escrita na dívida técnica, com a fase em que
será paga.

**"Você duplicou DTO e Model. Construa o melhor argumento a favor de
unificá-los, depois refute."** — Descartada porque o argumento foi feito na
prática, e não em teoria: o repositório chegou a devolver `TopicOut`, e o
problema (seta apontando da persistência para a apresentação) apareceu sozinho
na revisão.
