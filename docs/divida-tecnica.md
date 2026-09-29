# Dívida técnica consciente

Coisas que sabemos estar erradas e escolhemos manter, com o motivo e a fase em
que serão pagas. Dívida registrada é decisão; dívida esquecida é defeito.

---

## DT-001 — O service conhece `AsyncSession`

**Desde:** Fase 2 · **Paga em:** Fase 5

Os três services recebem uma `AsyncSession` no construtor só para poder chamar
`commit()`. Ou seja, a camada que não deveria conhecer tecnologia importa uma
classe do SQLAlchemy.

**Por que aceitamos:** resolver isso direito exige o padrão Unit of Work, que é
conteúdo da Fase 5. Antecipar significaria introduzir uma abstração antes de
sentir a dor que ela resolve — exatamente o erro que a Fase 1 existe para evitar.

**Como será pago:** o service passa a receber um port `UnitOfWork`, que a
infraestrutura implementa com SQLAlchemy.

---

## DT-002 — Cascata de deleção orquestrada entre módulos

**Desde:** Fase 2 · **Paga em:** Fase 4 ou 7

`SubjectService` depende de `TopicRepository` e `NoteRepository`.
`TopicService` depende de `NoteRepository`. Cada um mexe nas tabelas dos outros
para apagar em cascata.

**Por que aceitamos:** o comportamento veio da Fase 1, e refatoração não muda
comportamento. Removê-lo agora seria mudança de produto disfarçada de
refatoração.

**Como será pago:** um evento de domínio. `SubjectDeleted` é publicado, e cada
módulo reage apagando o que é seu. Ninguém mexe na tabela de ninguém.

⚠️ **Quando isso acontecer, o soft delete precisa mudar junto.** Hoje a
restauração em cascata identifica "o que caiu junto" pela marca de tempo
idêntica nos três níveis — o que só funciona porque a deleção acontece numa
transação única, com um `datetime` calculado uma vez e passado adiante.

Com eventos, cada módulo reage no seu tempo e os timestamps **vão** divergir.
Aí a coluna `deleted_batch_id` (UUID), hoje descartada por ser redundante,
deixa de ser preferência e vira necessidade.

---

## DT-003 — Apagar matéria apagava anotações em silêncio ✅ RESOLVIDO

**Aberto na:** Fase 1 · **Resolvido na:** Fase 2

Apagar uma matéria destruía todos os tópicos e todas as anotações, sem
confirmação e sem volta.

**Decisão do Hugo:** soft delete, com confirmação na interface e remoção
definitiva depois de X dias sem restaurar.

**Implementado:** coluna `deleted_at` nas três tabelas. Nada é removido do
banco; `delete` marca a data e toda consulta filtra `deleted_at IS NULL`.

O detalhe que faz funcionar: numa deleção em cascata, a **mesma marca de tempo**
desce pelos três níveis. Restaurar traz de volta só o que tem aquele timestamp
exato — um tópico apagado individualmente antes mantém a data dele e não
ressuscita junto.

**Onde o filtro mora:** no repositório. É o único lugar que monta consulta, então
não há como esquecer numa rota. Isto só é verdade por causa da refatoração da
Fase 2 — na Fase 1, com 8 `select()` espalhados, soft delete seria perigoso.

---

## DT-004 — Repositório devolve model do SQLAlchemy

**Desde:** Fase 2 · **Paga em:** Fase 4

Os repositórios devolvem `Subject`, `Topic` e `Note`, que são models do
SQLAlchemy — linha de tabela com roupa de objeto, não entidade de domínio. O
service, que não deveria conhecer persistência, manipula objetos dela.

**Por que aceitamos:** entidades de domínio de verdade são o conteúdo da Fase 4.
Criá-las agora, sem invariantes e sem value objects, produziria uma cópia
anêmica do model sem benefício nenhum.

**Como será pago:** entidades próprias em `domain/`, com um mapper traduzindo
entre elas e os models.

---

## DT-005 — `add` do repositório é `async` sem precisar

**Desde:** Fase 2 · **Provavelmente não será paga**

`TopicRepository.add` e os equivalentes são `async def`, mas `session.add()` é
síncrono. O `await` ali não espera nada.

**Por que aceitamos:** consistência de interface. Se todos os métodos do
repositório são aguardáveis, quem chama não precisa decorar quais são e quais
não são, e uma implementação futura que faça I/O não quebra a assinatura.

**Nota:** é um trade-off defensável, não um erro. Está aqui para ficar
registrado que foi escolha, e não descuido.

---

## DT-006 — `datetime.now()` direto no service

**Desde:** Fase 2 · **Paga em:** Fase 5

Os três services chamam `datetime.now(UTC)` para marcar `deleted_at`. É uma
dependência oculta em estado global, não declarada em assinatura nenhuma — o
mesmo problema do `os.getenv()` espalhado, discutido na Fase 0.

**Consequência prática:** não há como testar "purgar o que está na lixeira há
mais de 30 dias" sem esperar 30 dias de verdade.

**Como será pago:** port `Clock`, com `SystemClock` em produção e `FrozenClock`
nos testes. Esta é a motivação concreta que faz aquele port valer a pena — e é
por isso que ele não foi antecipado.

---

## DT-007 — Purga nunca é executada

**Desde:** Fase 2 · **Paga em:** Fase 12

Os três repositórios têm `purge(before)`, que remove de vez o que está na
lixeira há tempo demais. Nada chama esse método.

**Por que aceitamos:** purga é tarefa agendada, e agendador é conteúdo da Fase 12
(worker + tarefas periódicas). Dado parado na lixeira por algumas semanas não
causa dano.

**Pendente de decisão:** o valor de X. Sugestão: 30 dias, alinhado com o padrão
de lixeira que as pessoas já conhecem.
