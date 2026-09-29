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

---

## DT-003 — Apagar matéria apaga anotações em silêncio 🔴

**Desde:** Fase 1 · **Decisão pendente**

Esta não é dívida estrutural, é **risco de produto**. Apagar uma matéria por
engano apaga todos os tópicos e todas as anotações, sem confirmação e sem volta.
As anotações são o ativo mais valioso do Studyy — são elas que alimentam o RAG
da Fase 14.

**Alternativas:**

1. Recusar apagar matéria que ainda tenha tópicos; o usuário esvazia antes
2. Soft delete: marcar como apagada e nunca remover de fato
3. Manter a cascata, mas exigir confirmação explícita na borda

**Recomendação:** a 2, combinada com a 3. O custo é baixo e o erro é
irreversível — é o tipo de assimetria que justifica pagar antes.

**Decisão do Hugo:** Vamos implementar soft delete

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
