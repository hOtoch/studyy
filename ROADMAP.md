# Studyy — Roadmap de Produto e Arquitetura

> Sistema pessoal de estudos: anotações organizadas por matéria/tópico, roadmap de estudos com agendamento diário, Pomodoro acoplado ao planejamento, e um sistema de progressão/gamificação. No futuro: RAG sobre as próprias anotações para virar um professor particular (flashcards estilo Anki, simulados, mapas mentais).

**Stack escolhida:** Python 3.12 + FastAPI (backend) · Next.js + React + TypeScript (frontend) · PostgreSQL · Redis (fases avançadas)
**Calibragem:** iniciante em arquitetura. Começamos com um monólito simples e **refatoramos passo a passo**, introduzindo um conceito por vez.
**Autor:** Hugo · **Última atualização:** 2026-09-19

---

## 0. Como usar este documento

Este roadmap tem duas trilhas que andam **juntas**:

| Trilha | O que é |
|---|---|
| 🎯 **Trilha de Produto** | As funcionalidades que o Studyy precisa ter para você usar de verdade. |
| 🧠 **Trilha de Arquitetura** | O conceito de engenharia que você aprende *fazendo* aquela funcionalidade. |

### Regras do jogo

1. **Uma fase por vez.** Não pule. Cada fase depende da anterior — inclusive a Fase 1, que é *propositalmente mal feita*.
2. **Nunca refatore e adicione feature no mesmo commit.** Ou você muda o comportamento, ou muda a estrutura. Nunca os dois. Essa é a disciplina mais valiosa deste roadmap inteiro.
3. **Critério de aceite é lei.** Cada fase tem um checklist. Se um item não está marcado, a fase não acabou.
4. **Escreva o "porquê" num ADR.** Toda decisão de arquitetura vira um arquivo em `docs/adr/`. Você vai esquecer o motivo em 3 semanas.
5. **Teste antes de refatorar.** Se não há teste cobrindo o comportamento, a refatoração é um chute.
6. **O Checkpoint Socrático não é opcional.** Ele é o entregável de aprendizado da fase — o código é só o pretexto.

### Como cada fase é estruturada

```
### Fase N — Nome
🧠 Conceito em foco     -> a teoria, explicada devagar
❓ Por que isso importa -> a dor que esse conceito resolve
🎯 O que construir      -> a tarefa de produto
🔧 Patterns aplicados   -> os design patterns concretos
📁 Estrutura de pastas  -> como o projeto fica ao final
✅ Critérios de aceite  -> checklist verificável
⚠️ Armadilhas           -> os erros que quase todo mundo comete
🎓 Checkpoint Socrático -> as perguntas que você responde por escrito
📚 Para estudar         -> o que ler/assistir antes ou durante
```

### 🎓 O Checkpoint Socrático

Toda fase termina com 5 perguntas. Elas **não** são questionário de revisão — são perguntas projetadas para expor o que você acha que entendeu e não entendeu. Várias delas pedem que você **defenda uma posição e depois a ataque**, porque conseguir argumentar os dois lados é a diferença entre saber uma regra e entender um trade-off.

**O protocolo:**

1. Ao terminar o código da fase, **antes** de marcar os critérios de aceite, responda as 5 perguntas em `docs/checkpoints/fase-N.md`.
2. Responda **sem consultar** o roadmap, sem pesquisar e sem perguntar a uma IA. Respostas erradas escritas com convicção valem mais que respostas certas copiadas — elas mostram exatamente onde seu modelo mental está torto.
3. Se não souber responder, escreva **"não sei, e o que me confunde é X"**. Isso é uma resposta válida e é a mais útil de todas.
4. Depois de escrever, **me chame para a arguição.** Eu vou:
   - questionar suas respostas em vez de corrigi-las de cara;
   - apontar onde o raciocínio está certo pelo motivo errado (o caso mais perigoso);
   - mostrar as alternativas que você não considerou e por que foram descartadas em projetos reais;
   - só então dar a resposta consolidada — e você atualiza o arquivo com o que mudou de ideia.

**Guarde os arquivos.** Os checkpoints das fases 1 e 5 são um par: você responde as mesmas perguntas antes e depois de aprender arquitetura, e a comparação é o registro mais honesto do seu progresso neste projeto inteiro.

> 📌 **Como eu devo te guiar** ao longo de todas as fases está definido no [`CLAUDE.md`](CLAUDE.md) na raiz do projeto. Se quiser mudar a forma como eu te ensino — mais direto, menos socrático, mais ou menos código pronto — edite aquele arquivo, não este.

### Convenção de commits

Use Conventional Commits — facilita gerar changelog e te força a separar intenções:

```
feat(notes): adiciona criação de anotação
refactor(notes): extrai NoteRepository do router
test(planning): cobre invariante de limite diário
docs(adr): ADR-004 escolha de arquitetura hexagonal
chore(ci): adiciona import-linter ao pipeline
```

---

## 1. Visão do produto

### O problema

Anotações de aula ficam espalhadas, sem estrutura, e viram lixo digital. Planos de estudo não são cumpridos porque não há feedback nem consequência. E o conteúdo estudado nunca é revisado de forma ativa.

### A solução em uma frase

> Um lugar onde a anotação, o planejamento, a execução do estudo e a recompensa vivem no mesmo fluxo — e onde o conteúdo acumulado vira, depois, um professor particular.

### Os pilares

| Pilar | Funcionalidade | Fase |
|---|---|---|
| 📝 **Capturar** | Anotações em Markdown, organizadas por Matéria -> Tópico -> Subtópico, com tags | 1–5 |
| 🗺️ **Planejar** | Roadmap de estudos: cada tópico alocado a um dia, com duração planejada | 6 |
| ⏱️ **Executar** | Pomodoro que nasce do planejamento — o timer já sabe quanto tempo é | 6 |
| 🏆 **Progredir** | XP, níveis, streak, badges, metas diárias — reagindo ao que foi executado | 7–8 |
| 🤖 **Aprender** | RAG sobre as anotações: tutor, flashcards, simulados, mapas mentais | 13+ |

### Princípio de produto que guia tudo

**O planejamento e a execução não podem ser dois apps.** A maior parte das ferramentas de estudo falha porque você planeja num lugar (Notion) e executa em outro (um timer qualquer), e nada conecta os dois. No Studyy, iniciar um tópico do roadmap *é* iniciar o Pomodoro, e terminar o Pomodoro *é* gerar progresso.

---

## 2. Linguagem Ubíqua (Ubiquitous Language)

> Isto é DDD começando antes de qualquer código. A linguagem ubíqua é o vocabulário **compartilhado** entre o domínio e o código. Se no seu domínio você chama de "Sessão de Estudo", a classe **não pode** se chamar `TimerRecord`.

| Termo (domínio) | Classe (código) | Definição |
|---|---|---|
| **Matéria** | `Subject` | Uma disciplina ampla. Ex.: "Cálculo I", "Arquitetura de Software". |
| **Tópico** | `Topic` | Uma unidade estudável dentro de uma Matéria. Ex.: "Derivadas". Pode ter subtópicos. |
| **Anotação** | `Note` | Um registro em Markdown feito durante ou após uma aula, ligado a um Tópico. |
| **Tag** | `Tag` | Rótulo transversal que cruza matérias. Ex.: `#prova`, `#duvida`, `#revisar`. |
| **Plano de Estudos** | `StudyPlan` | O roadmap: o conjunto de alocações de tópicos ao longo dos dias. |
| **Alocação** | `PlanEntry` | "Estudar o Tópico X no dia D por N minutos". A unidade do plano. |
| **Sessão de Estudo** | `StudySession` | A execução real de uma Alocação. Nasce ao clicar "iniciar". |
| **Ciclo Pomodoro** | `PomodoroCycle` | Um bloco de foco + pausa dentro de uma Sessão. |
| **Tempo Focado** | `FocusedTime` | Minutos efetivamente em foco (não conta pausa nem tempo pausado). |
| **Progresso do Estudante** | `LearnerProgress` | O agregado que guarda XP, nível, streak e badges. |
| **Ofensiva** | `Streak` | Dias consecutivos em que a meta diária foi cumprida. |
| **Meta Diária** | `DailyGoal` | Minutos de foco que você se comprometeu a fazer por dia. |
| **Conquista** | `Badge` | Recompensa desbloqueada por atingir uma condição. |
| **Nível** | `Level` | Faixa de progressão derivada do XP acumulado. |

**Termos banidos** (ambíguos — não use em código nem em conversa):
`Task`, `Item`, `Data`, `Manager`, `Helper`, `Util`, `Info`, `Process`, `Handler` (exceto para handlers de evento).

---

## 3. Contextos Delimitados (Bounded Contexts)

> Um **Bounded Context** é uma fronteira dentro da qual um termo tem *um* significado. "Tópico" dentro de Conteúdo é um nó de conhecimento; dentro de Planejamento, é só um `TopicId` que ocupa tempo na agenda. São coisas diferentes — e é por isso que são módulos separados.

```
┌─────────────────────┐        ┌─────────────────────┐
│   CONTEUDO          │        │   PLANEJAMENTO      │
│                     │        │                     │
│  Subject            │        │  StudyPlan          │
│  Topic              │<--id---│  PlanEntry          │
│  Note               │        │  DailyGoal          │
│  Tag                │        │                     │
└─────────────────────┘        └──────────┬──────────┘
                                          │ id
                                          v
┌─────────────────────┐        ┌─────────────────────┐
│   PROGRESSAO        │        │   EXECUCAO          │
│                     │        │                     │
│  LearnerProgress    │<-event-│  StudySession       │
│  XP / Level         │        │  PomodoroCycle      │
│  Streak / Badge     │        │  FocusedTime        │
└─────────────────────┘        └─────────────────────┘

                    ┌─────────────────────┐
                    │   ASSISTENTE (fut.) │
                    │  DocumentChunk      │
                    │  Flashcard / Quiz   │
                    │  MindMap            │
                    └─────────────────────┘
```

### Regras de integração entre contextos

1. **Contextos NUNCA importam entidades um do outro.** Planejamento não importa `Topic`. Ele guarda um `TopicId` (Value Object com um UUID dentro).
2. **Comunicação por eventos ou por porta explícita.** Progressão não chama Execução. Execução *publica* `StudySessionCompleted` e Progressão *reage*.
3. **Se precisar do dado do outro contexto, use uma porta de leitura.** Ex.: `TopicLookupPort.get_title(topic_id) -> str | None` — uma interface minúscula, definida por *quem consome*, não por quem fornece. (Isso é o ISP do SOLID aplicado entre módulos.)

---

## 4. Decisões de Arquitetura (ADRs)

Crie `docs/adr/`. Template (`docs/adr/TEMPLATE.md`):

```markdown
# ADR-000: Título curto da decisão

- **Status:** proposto | aceito | substituído por ADR-00X
- **Data:** AAAA-MM-DD

## Contexto
Qual é a situação? Que forças estão em jogo? O que me obriga a decidir agora?

## Decisão
O que eu decidi fazer. Em voz ativa: "Vamos usar X".

## Alternativas consideradas
- **Alternativa A** — por que foi descartada.
- **Alternativa B** — por que foi descartada.

## Consequências
- ✅ O que fica mais fácil.
- ❌ O que fica mais difícil / que dívida estou assumindo.
- 🔄 O que precisará ser revisitado se a premissa Y mudar.
```

### ADRs já decididos (escreva o arquivo de cada um)

| ADR | Decisão | Fase |
|---|---|---|
| ADR-001 | Backend em Python 3.12 + FastAPI | 0 |
| ADR-002 | PostgreSQL como banco principal (não SQLite) | 0 |
| ADR-003 | **Monólito Modular**, não microsserviços | 0 |
| ADR-004 | Arquitetura Hexagonal (Ports & Adapters) com Use Cases | 5 |
| ADR-005 | Domain Events in-process antes de fila externa | 7 |
| ADR-006 | Frontend Next.js (App Router) separado do backend | 9 |
| ADR-007 | pgvector no mesmo Postgres em vez de vector DB dedicado | 14 |
| ADR-008 | Origem em container (Fly.io) + borda no Cloudflare | 10 |
| ADR-009 | Cloudflare Access em vez de autenticação própria | 10 |
| ADR-010 | Não usar replicação/particionamento — com o gatilho que reverteria | 11 |

### 🔴 ADR-003 em detalhe: por que NÃO microsserviços

Você listou microsserviços na trilha de estudo, então isso merece uma resposta direta:

> **Este projeto não deve ser microsserviços.**

Motivos:

- Microsserviços resolvem um problema **organizacional** (times independentes fazendo deploy sem se coordenar), não técnico. Você é um time de uma pessoa.
- O custo é alto: rede não confiável, transações distribuídas, observabilidade distribuída, versionamento de contrato, orquestração. Você pagaria tudo isso sem receber o benefício.
- **A regra prática:** microsserviços exigem que você já tenha as fronteiras de domínio corretas. Se você errar as fronteiras num monólito modular, refatora em 2 horas. Se errar em microsserviços, refatora em 2 meses.

**O que fazer em vez disso:** construir um **Monólito Modular** onde cada Bounded Context é um módulo com fronteira real, verificada por ferramenta. Se um dia você *quiser* extrair um módulo para um serviço próprio, a Fase 13 tem um exercício opcional exatamente para isso — e vai ser viável justamente porque a fronteira já existia.

---

## 5. Stack definitiva

### Backend

| Camada | Escolha | Por quê |
|---|---|---|
| Runtime | Python 3.12+ | Escolhido por você; caminho curto pro RAG depois |
| Gerenciador | **uv** | Muito mais rápido que Poetry/pip, lockfile determinístico |
| Web framework | FastAPI | DI nativa via `Depends`, Pydantic, OpenAPI grátis |
| ORM | SQLAlchemy 2.0 (async) | O único maduro o bastante para separar modelo de domínio de modelo de persistência |
| Migrations | Alembic | Padrão do ecossistema SQLAlchemy |
| Validação | Pydantic v2 | Na **borda** (DTOs), nunca no domínio |
| Testes | pytest + pytest-asyncio + factory-boy | |
| Testes de integração | testcontainers-python | Postgres real no teste, não mock |
| Lint/format | **Ruff** | Substitui flake8 + isort + black, muito mais rápido |
| Tipos | **mypy --strict** | Seu "compilador". Essencial em Python para sustentar arquitetura |
| **Fronteiras** | **import-linter** | 🔑 Quebra o CI se uma camada importar a camada errada |

> ⚠️ **Nota sobre Python e arquitetura.** Em Java ou C#, o compilador e o sistema de módulos te impedem de fazer certas bobagens. Em Python, nada te impede de importar o ORM dentro do domínio. Por isso `mypy --strict` + `import-linter` não são opcionais neste roadmap: **eles são o atrito artificial que te ensina a disciplina.** Configure-os na Fase 0, antes de escrever a primeira regra de negócio.

### Frontend

| Camada | Escolha |
|---|---|
| Framework | Next.js 15 (App Router) + TypeScript strict |
| Estilo | Tailwind CSS |
| Componentes | shadcn/ui (você é dono do código, não é dependência) |
| Estado servidor | TanStack Query |
| Estado cliente | Zustand (só para o timer do Pomodoro) |
| Formulários | React Hook Form + Zod |
| Markdown | `@uiw/react-md-editor` ou Tiptap |

### Infraestrutura (evolui por fase)

| Fase | Infra |
|---|---|
| 0–10 | Docker Compose: Postgres |
| 11+ | + Redis, + worker (ARQ) |
| 12+ | + OpenTelemetry, Jaeger ou Grafana Tempo |
| 13+ | + extensão pgvector |

---

## 6. Estrutura alvo do projeto (ao final da Fase 8)

> Você **não** começa assim. Você **chega** aqui. Esta é a foto do destino.

```
studyy/
├── docs/
│   ├── ROADMAP.md              <- este arquivo
│   └── adr/
│       ├── TEMPLATE.md
│       └── ADR-001-python-fastapi.md
│
├── backend/
│   ├── pyproject.toml
│   ├── .importlinter            <- contratos de fronteira (o guardião)
│   ├── alembic/
│   │
│   ├── src/studyy/
│   │   ├── shared/                      # Shared Kernel — o mínimo possível
│   │   │   ├── domain/
│   │   │   │   ├── entity.py            # base Entity / AggregateRoot
│   │   │   │   ├── value_object.py
│   │   │   │   ├── events.py            # DomainEvent base
│   │   │   │   └── errors.py            # DomainError base
│   │   │   └── application/
│   │   │       ├── unit_of_work.py      # Port do UoW
│   │   │       └── event_bus.py         # Port do barramento
│   │   │
│   │   ├── content/                     # == BOUNDED CONTEXT: Conteudo ==
│   │   │   ├── domain/                  # ZERO imports de fora do domínio
│   │   │   │   ├── subject.py
│   │   │   │   ├── topic.py
│   │   │   │   ├── note.py
│   │   │   │   ├── value_objects.py
│   │   │   │   └── ports.py             # SubjectRepository (Protocol)
│   │   │   ├── application/
│   │   │   │   ├── create_note.py       # um arquivo por Use Case
│   │   │   │   ├── list_notes_by_topic.py
│   │   │   │   └── dtos.py
│   │   │   └── infrastructure/
│   │   │       ├── models.py            # tabelas SQLAlchemy
│   │   │       ├── repositories.py      # implementação do Port
│   │   │       ├── mappers.py           # domínio <-> modelo
│   │   │       └── http/routes.py       # driving adapter
│   │   │
│   │   ├── planning/                    # == BOUNDED CONTEXT: Planejamento ==
│   │   │   ├── domain/  application/  infrastructure/
│   │   │
│   │   ├── execution/                   # == BOUNDED CONTEXT: Execucao ==
│   │   │   ├── domain/  application/  infrastructure/
│   │   │
│   │   ├── progression/                 # == BOUNDED CONTEXT: Progressao ==
│   │   │   ├── domain/  application/  infrastructure/
│   │   │
│   │   └── composition_root.py          # onde TUDO é amarrado (DI)
│   │
│   └── tests/
│       ├── unit/           # domínio puro, sem I/O, milissegundos
│       ├── integration/    # repositórios contra Postgres real
│       ├── e2e/            # HTTP de ponta a ponta
│       └── architecture/   # testa as próprias regras de arquitetura
│
├── frontend/
│   └── src/
│       ├── app/                 # rotas Next.js
│       ├── features/            # organizado por feature, não por tipo
│       │   ├── notes/  planning/  pomodoro/  progression/
│       └── shared/
│
└── docker-compose.yml
```

### A regra de dependência (a mais importante de todas)

```
   infrastructure  ------>  application  ------>  domain
      (adapters)             (use cases)          (regras)

   As setas apontam SEMPRE para dentro. Nunca para fora.
   domain não importa NADA. Nem FastAPI, nem SQLAlchemy, nem Pydantic.
```

Memorize: **o domínio não sabe que existe banco de dados, não sabe que existe HTTP, e não sabe que existe internet.**

---

# PARTE II — AS FASES

---

## Fase 0 — Fundação e ferramental

**Duração estimada:** 1 a 2 sessões · **Sem arquitetura ainda — só higiene.**

### 🧠 Conceito em foco: a fundação é arquitetura disfarçada de configuração

Parece que esta fase é só ferramental. Não é — ela é quase toda **decisão de posicionamento**, que é o tipo de decisão que você nunca revisita e que cobra juros por 14 fases.

Antes de aprender arquitetura, você precisa de um lugar onde o feedback é rápido e automático. Sem isso, toda refatoração das próximas fases vira medo.

**As quatro decisões escondidas aqui:**

1. **Onde o código mora** (`src/` layout) — a estrutura de pastas define o que pode importar o quê. Aqui a regra é trivial; na Fase 5 vira `infrastructure → application → domain`. Mesma ideia, primeiro exercício.
2. **Por onde a configuração entra** — `os.getenv()` espalhado é dependência invisível num singleton global mutável. É o mesmo problema do `datetime.now()`, que na Fase 5 vira o port `Clock`. Você está aprendendo DIP sem o nome ainda.
3. **Guardrails antes de haver o que proteger** — tipar a primeira linha é grátis; tipar 5 mil linhas é um projeto. Ninguém adiciona CI a um projeto que já funciona sem ele.
4. **Como o sistema diz que está vivo** — `/health/live` (o processo) vs `/health/ready` (o processo *e* suas dependências). Se liveness checasse o banco, uma oscilação de 2s no Postgres faria o orquestrador matar um processo saudável. Paga na Fase 10.

> 📌 **Correção:** o `import-linter` **não** entra nesta fase, apesar de aparecer na tabela de stack. Ferramenta sem contrato para verificar é ruído, e ainda não existem camadas. Ele entra na Fase 5, junto com as fronteiras que ele protege.

### 🎯 O que construir

1. **Repositório e ambiente**
   - `uv init` no `backend/`, Python 3.12
   - Layout `src/` (`src/studyy/`) — evita o clássico "funciona no meu PC mas o import quebra no teste"
   - `docker-compose.yml` com Postgres 16
   - `.env.example` + `.env` (no `.gitignore`)

2. **Qualidade automatizada**
   - `ruff` configurado no `pyproject.toml` (lint + format)
   - `mypy` em modo `strict`
   - `pytest` com um teste bobo passando (`test_sanity.py`)
   - `pre-commit` rodando ruff + mypy antes de cada commit

3. **CI (GitHub Actions)**
   - Job que roda: ruff -> mypy -> pytest
   - Falhou, não mergeia. Sem exceção.

4. **Configuração tipada**
   - `Settings` com `pydantic-settings` lendo do `.env`
   - Nunca `os.getenv()` espalhado pelo código

5. **Healthcheck**
   - `GET /health` retornando `{"status": "ok"}`
   - `GET /health/db` que faz `SELECT 1` no Postgres

6. **Primeiros ADRs**
   - Escreva ADR-001, ADR-002 e ADR-003 agora, enquanto o motivo está fresco

### ✅ Critérios de aceite

- [ ] `docker compose up` sobe Postgres e o app conecta
- [ ] `uv run pytest` passa
- [ ] `uv run mypy src` passa em strict, sem `# type: ignore`
- [ ] `uv run ruff check .` sem erros
- [ ] CI verde no GitHub
- [ ] `pre-commit` bloqueia um commit com código mal formatado (teste de verdade: quebre o formato de propósito e tente commitar)
- [ ] 3 ADRs escritos em `docs/adr/`

### ⚠️ Armadilhas

- **Pular o mypy strict "por enquanto".** Adicionar tipos depois em 5000 linhas é sofrimento. Comece strict.
- **Usar SQLite "só pra começar".** Postgres tem tipos (`jsonb`, arrays, full-text, `tsvector`) que você vai usar nas fases 10 e 13. Migrar depois é retrabalho garantido.
- **Não colocar CI porque "é projeto pessoal".** O CI é exatamente o que te dá coragem de refatorar nas fases 2–8.

### 🎓 Checkpoint Socrático — Fase 0

> Responda **por escrito** em `docs/checkpoints/fase-0.md` antes de marcar a fase como concluída.

1. `mypy --strict` e o `import-linter` servem para proteger uma arquitetura que ainda **não existe**. Por que eles estão na Fase 0 e não na Fase 5?
2. O CI roda exatamente os mesmos comandos que você roda localmente. **Então o que ele te dá que a sua máquina não dá?** Dê uma resposta que não seja "automatiza".
3. Se você tivesse escolhido SQLite agora, qual decisão futura ficaria mais cara — e **quanto** mais cara? Estime em horas.
4. Qual é a diferença conceitual entre "configuração" e "código"? Por que um `Settings` tipado é melhor que `os.getenv()` espalhado — em termos de acoplamento?
5. Escolha o item desta fase que mais pareceu burocracia inútil. **Construa o melhor argumento possível para pular esse item.** Depois destrua seu próprio argumento.

### 📚 Para estudar

- Documentação do `uv` (gerenciamento de dependências)
- `pyproject.toml`: o que é PEP 621
- Por que layout `src/` (procure "Python src layout vs flat layout")

---

## Fase 1 — O monólito ingênuo (propositalmente ruim)

**Duração estimada:** 1 sessão · ⚠️ **Esta fase é um exercício de dor controlada.**

### 🧠 Conceito em foco: Acoplamento e Coesão

Estes são os dois conceitos mais fundamentais de toda a engenharia de software. Tudo o mais (SOLID, patterns, DDD, arquitetura) existe para gerenciar estes dois.

**Acoplamento** = o quanto uma parte do código depende de outra.
Alto acoplamento: mexer em A quebra B, C e D. Você não consegue entender A sem entender B.

**Coesão** = o quanto as coisas que estão juntas *pertencem* juntas.
Baixa coesão: uma classe que valida CPF, envia e-mail e calcula imposto. Ela não tem um motivo único para existir.

> **A meta eterna:** baixo acoplamento, alta coesão.

### ❓ Por que fazer errado de propósito?

Porque arquitetura ensinada em abstrato não gruda. Se você começar direto com Clean Architecture, você vai copiar uma estrutura de pastas sem entender qual dor ela resolve — e vai aplicá-la errado em todo projeto futuro. Aqui você vai *sentir* a dor em 200 linhas, e aí cada refatoração das fases seguintes vai ter um motivo concreto.

### 🎯 O que construir

**Um único arquivo `main.py`** (sim, um só) com:

- CRUD de `Subject` (matéria)
- CRUD de `Topic` (tópico, pertence a uma matéria)
- CRUD de `Note` (anotação em Markdown, pertence a um tópico)

E faça tudo do jeito "direto":

- SQLAlchemy chamado dentro da função de rota
- Validação misturada com a query
- Regra de negócio (ex.: "não pode ter dois tópicos com mesmo nome na mesma matéria") dentro do endpoint
- Modelo do Pydantic e modelo da tabela são a mesma coisa, ou quase
- Sem uma única classe de serviço

### 🔬 O experimento (a parte mais importante da fase)

Depois que funcionar, **pare e responda por escrito** em `docs/fase-1-retrospectiva.md`:

1. Para testar a regra "não pode haver tópico duplicado na matéria", **preciso de um banco de dados rodando?** Por quê?
2. Se eu quisesse trocar Postgres por MongoDB, **quantos arquivos/linhas eu tocaria?**
3. Se eu quisesse expor a mesma funcionalidade por uma CLI além da API, **quanto código eu duplicaria?**
4. Abra `main.py` e conte: **quantas responsabilidades diferentes** existem em uma única função de rota? (Listar: parsing HTTP, validação, regra de negócio, montar query, mapear resposta, tratar erro...)
5. Se a regra de negócio mudar, **onde eu procuro?**

Guarde essas respostas. Você vai reler ao final da Fase 5.

### ✅ Critérios de aceite

- [ ] Criar matéria, tópico e anotação funciona via `/docs` (Swagger)
- [ ] Anotação guarda conteúdo Markdown
- [ ] Pelo menos uma regra de negócio existe (nome duplicado)
- [ ] Alembic gerou a primeira migration
- [ ] `docs/fase-1-retrospectiva.md` escrito com as 5 respostas
- [ ] Tag no git: `git tag fase-1-monolito-ingenuo` (para poder voltar e comparar depois)

### ⚠️ Armadilhas

- **Fazer bonito aqui.** Sério: faça feio. Se você já separar em camadas, perde o experimento.
- **Não escrever a retrospectiva.** É literalmente o entregável principal da fase.

### 🎓 Checkpoint Socrático — Fase 1

> As 5 perguntas do experimento acima **são** o checkpoint desta fase. Salve as respostas em `docs/checkpoints/fase-1.md`.
>
> Este é o checkpoint mais importante do roadmap inteiro, porque é o único que você responde **sem saber a resposta certa**. Nas fases seguintes você já terá sido ensinado. Aqui, não. Escreva o que você realmente acha, mesmo que pareça ingênuo — o valor está em comparar com a sua própria resposta na Fase 5.

### 📚 Para estudar

- "Coupling and Cohesion" — conceitos clássicos de engenharia de software
- Tipos de acoplamento: content, common, control, stamp, data (do mais nocivo ao menos)
- Tipos de coesão: coincidental, lógica, temporal, procedural, funcional (do pior ao melhor)

---

## Fase 2 — Separação em camadas (Layered Architecture)

**Duração estimada:** 2 a 3 sessões

### 🧠 Conceito em foco: Arquitetura em Camadas + Separação de Responsabilidades

A primeira grande ideia de arquitetura: **agrupar código por responsabilidade técnica**, criando camadas com uma direção de dependência definida.

```
  ┌──────────────────────────────────┐
  │  PRESENTATION  (routers)         │  HTTP: receber, validar formato, responder
  └───────────────┬──────────────────┘
                  v
  ┌──────────────────────────────────┐
  │  APPLICATION   (services)        │  Orquestração, regra de negócio, transação
  └───────────────┬──────────────────┘
                  v
  ┌──────────────────────────────────┐
  │  PERSISTENCE   (repositories)    │  Só fala SQL/ORM. Não sabe regra nenhuma.
  └───────────────┬──────────────────┘
                  v
  ┌──────────────────────────────────┐
  │  DATABASE                        │
  └──────────────────────────────────┘
```

**Regra:** cada camada só conhece a camada imediatamente abaixo. O router **nunca** fala com o repositório direto.

### ❓ Por que isso importa

Responde diretamente às dores da Fase 1: agora a regra de negócio tem um lugar (service), e o SQL tem um lugar (repository). Trocar de banco = trocar o repository.

### 🎯 O que construir (refatorar, não reescrever)

1. **Extrair o `Repository`**
   - `SubjectRepository`, `TopicRepository`, `NoteRepository`
   - Métodos com nomes do **domínio**, não do banco: `find_by_subject_and_slug()`, não `select_where()`
   - O repositório retorna objetos, nunca `Row` ou `dict`

2. **Extrair o `Service`**
   - `SubjectService`, `TopicService`, `NoteService`
   - Toda regra de negócio migra do router para cá
   - O service recebe o repositório **no construtor** (não instancia dentro)

3. **Introduzir DTOs separados**
   - `CreateNoteRequest` / `NoteResponse` (Pydantic, camada HTTP)
   - `NoteModel` (SQLAlchemy, camada persistência)
   - **São classes diferentes.** Mesmo que hoje tenham os mesmos campos.

4. **Usar o sistema de DI do FastAPI**
   - `Depends(get_note_service)` no router
   - A função `get_note_service` monta o service com o repositório

5. **Erros de domínio tipados**
   - `SubjectNotFound`, `DuplicateTopicName` — classes de exceção próprias
   - Um `exception_handler` no FastAPI traduz `DomainError -> HTTP status`
   - **O service nunca levanta `HTTPException`.** Isso é vazamento da camada HTTP.

### 🔧 Patterns aplicados

| Pattern | Onde | O que resolve |
|---|---|---|
| **Repository** | `repositories.py` | Isola o acesso a dados atrás de uma interface do domínio |
| **DTO** | `schemas.py` | Separa contrato externo (API) de estrutura interna |
| **Dependency Injection** | `Depends()` | O service não constrói suas dependências -> testável |

### 📁 Estrutura ao final

```
src/studyy/
├── main.py
├── config.py
├── database.py
├── exceptions.py           # DomainError e filhos
├── subjects/
│   ├── router.py           # HTTP
│   ├── schemas.py          # DTOs Pydantic
│   ├── service.py          # regra de negócio
│   ├── repository.py       # acesso a dados
│   └── models.py           # tabelas SQLAlchemy
├── topics/    (mesma estrutura)
└── notes/     (mesma estrutura)
```

> Note que já estamos organizando **por feature** (`subjects/`, `notes/`) e não por tipo técnico (`routers/`, `services/`). Isso é intencional — é o embrião dos Bounded Contexts da Fase 4.

### ✅ Critérios de aceite

- [ ] Nenhum `import` de SQLAlchemy dentro de `router.py`
- [ ] Nenhum `HTTPException` dentro de `service.py`
- [ ] Nenhuma regra de negócio dentro de `router.py`
- [ ] Todo service recebe suas dependências via construtor
- [ ] Testes de service usando um **repositório fake em memória** (não mock, não banco) — prova de que a separação funcionou
- [ ] Um teste de service roda em **menos de 10ms**
- [ ] Endpoints continuam com exatamente o mesmo comportamento da Fase 1 (refatoração não muda comportamento)

### ⚠️ Armadilhas

- **Repositório anêmico que só repassa.** Se `NoteRepository.save()` é literalmente `session.add()`, ainda está ok nesta fase — mas repositório com método `execute_raw_sql()` exposto não é repositório, é wrapper.
- **Service que recebe `Session` do SQLAlchemy.** Aí ele conhece a tecnologia de banco. Nesta fase ainda é tolerável, mas anote como dívida — a Fase 5 resolve com Unit of Work.
- **DTO igual ao Model "pra não repetir".** A duplicação aqui é *proposital*. Eles mudam por motivos diferentes e em ritmos diferentes.
- **Repositório retornando DTO do Pydantic.** Não. Repositório retorna objeto de domínio (ou, nesta fase, o model). DTO é coisa da borda.

### 🎓 Checkpoint Socrático — Fase 2

> Responda **por escrito** em `docs/checkpoints/fase-2.md` antes de marcar a fase como concluída.

1. Você extraiu duas coisas: Repository e Service. **Qual das duas extrações reduziu mais o acoplamento?** Justifique escolhendo uma — não responda "as duas".
2. Seu `Service` ainda recebe a `Session` do SQLAlchemy em algum lugar? Se sim, **que tipo de acoplamento é esse**, e o que exatamente ele te impede de fazer?
3. Olhe os métodos do seu `NoteRepository`. Algum deles **vaza a tecnologia de banco** para quem chama? Como você conseguiria detectar isso sem olhar a implementação?
4. Você duplicou DTO e Model, mesmo tendo os mesmos campos. **Construa o melhor argumento a favor de unificá-los.** Agora refute-o com um cenário concreto do Studyy.
5. Seu teste de service roda em 10ms com um fake. Se ele passasse a levar 2 segundos, **o que isso te diria sobre a arquitetura**, antes mesmo de você abrir o código?

### 📚 Para estudar

- Layered Architecture / N-Tier — capítulo 1 de *Software Architecture Patterns* (Mark Richards, gratuito na O'Reilly)
- Repository Pattern (Martin Fowler, *PoEAA*)
- Dependency Injection: diferença entre DI e Service Locator

---

## Fase 3 — SOLID na prática

**Duração estimada:** 3 a 4 sessões · **Uma letra por sessão, com refatoração real.**

### 🧠 Conceito em foco: os cinco princípios

Não decore as siglas. Para cada uma, entenda **a dor** que ela evita.

---

#### **S — Single Responsibility Principle**

> "Uma classe deve ter apenas um motivo para mudar."

Não é "uma classe faz uma coisa". É sobre **atores**: se o time de Marketing e o time de Financeiro podem, cada um, pedir uma mudança na mesma classe, essa classe tem duas responsabilidades.

**No Studyy:** seu `NoteService` provavelmente já faz: validar, salvar, gerar slug, extrair tags do Markdown e contar palavras. Isso é 3 responsabilidades.

**Refatoração:**
- Extrair `MarkdownTagExtractor` (parsing de `#tag` no conteúdo)
- Extrair `SlugGenerator`
- O service **orquestra** essas peças, não as implementa

---

#### **O — Open/Closed Principle**

> "Aberto para extensão, fechado para modificação."

Adicionar um comportamento novo não deveria exigir editar código que já funciona e já foi testado.

**No Studyy:** imagine exportar uma anotação em Markdown, PDF ou HTML. A versão ruim:

```python
if formato == "md": ...
elif formato == "pdf": ...
elif formato == "html": ...   # e cada formato novo abre essa função de novo
```

**Refatoração (Strategy):**

```python
class NoteExporter(Protocol):
    def export(self, note: Note) -> bytes: ...

class MarkdownExporter: ...
class PdfExporter: ...

EXPORTERS: dict[str, NoteExporter] = {"md": MarkdownExporter(), "pdf": PdfExporter()}
```

Formato novo = classe nova + uma linha no registro. Nada existente é editado.

---

#### **L — Liskov Substitution Principle**

> "Se S é subtipo de T, posso trocar T por S sem quebrar nada."

A violação clássica: uma subclasse que levanta `NotImplementedError` num método herdado, ou que aperta uma pré-condição.

**No Studyy:** se você criar um `ReadOnlyNoteRepository` que herda de `NoteRepository` e cujo `save()` levanta erro, você violou LSP. A solução é segregar a interface (ver ISP), não herdar.

**Regra prática em Python:** prefira **composição + `Protocol`** a herança. Herança é a forma mais forte de acoplamento que existe.

---

#### **I — Interface Segregation Principle**

> "Nenhum cliente deve ser forçado a depender de métodos que não usa."

**No Studyy:** um `NoteRepository` com 15 métodos (`save`, `find_by_id`, `find_all`, `search_fulltext`, `bulk_import`, `count_by_tag`...) obriga qualquer fake de teste a implementar os 15.

**Refatoração:**

```python
class NoteWriter(Protocol):
    async def save(self, note: Note) -> None: ...

class NoteReader(Protocol):
    async def find_by_id(self, id: NoteId) -> Note | None: ...

class NoteSearcher(Protocol):
    async def search(self, query: str) -> list[Note]: ...
```

Uma classe concreta pode implementar as três. Mas cada use case depende só da que precisa.

---

#### **D — Dependency Inversion Principle** ⭐

> "Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações."

**Este é o princípio que sustenta toda a Fase 5.** É o mais importante dos cinco.

A sacada que quase ninguém percebe de primeira: **a interface pertence a quem a consome, não a quem a implementa.**

```
   ❌ ANTES                          ✅ DEPOIS

   NoteService                       NoteService
       │                                  │
       v                                  v
   SqlNoteRepository              NoteRepository (Protocol)
       │                            ^         (definido JUNTO do service)
       v                            │
   PostgreSQL                  SqlNoteRepository
                                     │
                                     v
                                PostgreSQL
```

A seta de dependência **inverteu**. Agora a infraestrutura depende do domínio, não o contrário.

**Em Python, use `typing.Protocol`, não `ABC`:**

```python
from typing import Protocol

class NoteRepository(Protocol):
    async def save(self, note: Note) -> None: ...
    async def find_by_id(self, note_id: NoteId) -> Note | None: ...
```

Por quê `Protocol` e não `ABC`? Porque com `Protocol` a implementação **não precisa importar a interface** (structural typing / duck typing tipado). Com `ABC`, `SqlNoteRepository` teria que fazer `from ...domain import NoteRepository` e herdar. Com `Protocol`, o mypy verifica a compatibilidade estruturalmente. Acoplamento ainda menor.

---

### 🎯 O que construir

Refatorar o código da Fase 2 aplicando as cinco letras, **uma por commit**:

1. `refactor(notes): extrai TagExtractor e SlugGenerator (SRP)`
2. `refactor(notes): substitui if/elif de export por Strategy (OCP)`
3. `refactor(shared): troca herança por composição em repositórios (LSP)`
4. `refactor(notes): segrega NoteRepository em Reader/Writer (ISP)`
5. `refactor(notes): inverte dependência com Protocol (DIP)`

### 🔧 Patterns aplicados

| Pattern | Princípio | Onde |
|---|---|---|
| **Strategy** | OCP | Exportadores de anotação |
| **Protocol / Port** | DIP | Interfaces de repositório |
| **Composition over Inheritance** | LSP | Em todo lugar |
| **Registry** | OCP | Dicionário de exportadores |

### ✅ Critérios de aceite

- [ ] Nenhuma classe de service tem mais de ~150 linhas
- [ ] Adicionar um formato de exportação novo não edita nenhum arquivo existente (só cria um e registra)
- [ ] Todos os repositórios são declarados como `Protocol` no módulo que os *consome*
- [ ] Os fakes de teste implementam a interface e o `mypy` confirma (escreva `_: NoteRepository = FakeNoteRepository()` num teste — se o mypy aceitar, a compatibilidade está provada)
- [ ] Você escreveu, em `docs/solid.md`, **um exemplo tirado do seu próprio código** para cada uma das 5 letras

### ⚠️ Armadilhas

- **Aplicar SOLID em tudo.** SOLID resolve o problema de mudança futura. Código que não vai mudar não precisa de abstração. Abstração prematura é tão cara quanto acoplamento.
- **Confundir SRP com "métodos pequenos".** Não é sobre tamanho, é sobre motivos-para-mudar.
- **Criar interface com uma única implementação "porque SOLID manda".** Só vale se: (a) você precisa de um fake no teste, ou (b) você realmente prevê uma segunda implementação. No Studyy, (a) já justifica os repositórios.

### 🎓 Checkpoint Socrático — Fase 3

> Responda **por escrito** em `docs/checkpoints/fase-3.md` antes de marcar a fase como concluída.

1. Escolha a letra do SOLID que te pareceu **mais inútil** na prática. Agora explique por que ela existe mesmo assim — qual dor ela resolve que você ainda não sentiu?
2. No DIP: quem é o **dono** da interface `NoteRepository` — o domínio ou a infraestrutura? Por que essa resposta muda tudo?
3. Aponte uma abstração que você criou e que hoje tem **uma única implementação**. Justifique-a. Se não conseguir justificar em duas frases, **delete-a** e anote isso aqui.
4. Qual a diferença prática entre `Protocol` e `ABC` neste projeto? **O que você perderia** se trocasse todos os `Protocol` por `ABC` amanhã?
5. Em que ponto SOLID te fez escrever **mais** código sem benefício visível? Isso é over-engineering ou investimento? **Qual evento futuro decidiria a resposta?**

### 📚 Para estudar

- *Clean Architecture* (Robert C. Martin), Parte III — capítulos 7 a 11, um por letra
- "The Single Responsibility Principle" — artigo do próprio Uncle Bob sobre a definição por *atores*
- `typing.Protocol` na documentação do Python (PEP 544)

---

## Fase 4 — Domínio rico e DDD Tático

**Duração estimada:** 4 a 6 sessões · 🔥 **A fase mais transformadora do roadmap.**

### 🧠 Conceito em foco: Domain-Driven Design (tático)

Até aqui seu `Note` é um saco de dados: um objeto com atributos públicos, e as regras moram no service. Isso tem nome: **Modelo de Domínio Anêmico** — e é considerado um antipadrão porque a lógica fica espalhada por N services, e nada impede alguém de criar um objeto em estado inválido.

**A virada:** o objeto de domínio passa a **proteger suas próprias regras**.

---

#### Os quatro blocos de construção

**1. Value Object (VO)**
Um objeto definido **pelo seu valor**, não por identidade. Imutável. Dois VOs com os mesmos valores são o mesmo VO.

```python
@dataclass(frozen=True)
class Duration:
    minutes: int

    def __post_init__(self) -> None:
        if self.minutes <= 0:
            raise InvalidDuration("Duração deve ser positiva")
        if self.minutes > 240:
            raise InvalidDuration("Duração máxima por alocação é 240 minutos")

    def __add__(self, other: "Duration") -> "Duration":
        return Duration(self.minutes + other.minutes)
```

O ganho: **é impossível existir uma `Duration` inválida no sistema.** A validação acontece uma vez, na construção, e nunca mais precisa ser repetida.

**Regra de ouro:** se você tem `minutos: int` circulando pelo código, você tem um VO escondido. `int` aceita `-5`. `Duration` não.

**VOs do Studyy:** `SubjectId`, `TopicId`, `NoteId`, `Duration`, `StudyDate`, `Slug`, `Tag`, `MarkdownContent`, `XpPoints`, `Streak`, `Level`.

---

**2. Entidade**
Um objeto definido pela **identidade**, não pelos atributos. Muda ao longo do tempo e continua sendo o mesmo.

```python
class Topic:
    def __init__(self, id: TopicId, subject_id: SubjectId, title: str) -> None:
        self._id = id
        self._subject_id = subject_id
        self._title = self._validate_title(title)
        self._status = TopicStatus.NOT_STARTED

    def mark_as_completed(self) -> None:
        if self._status is TopicStatus.NOT_STARTED:
            raise InvalidTopicTransition("Não é possível concluir um tópico nunca iniciado")
        self._status = TopicStatus.COMPLETED
```

Repare: **não existe `topic.status = "completed"`**. Existe `topic.mark_as_completed()`, que conhece as transições válidas. Isso é encapsulamento de verdade.

---

**3. Agregado e Raiz de Agregado** ⭐

Este é o conceito mais difícil e mais valioso do DDD tático.

Um **Agregado** é um grupo de objetos tratado como **uma unidade de consistência**. A **Raiz do Agregado** é a única entidade acessível de fora — tudo passa por ela.

Três regras:
1. **Referências externas apontam só para a Raiz.** Nunca para uma entidade interna.
2. **Uma transação = um agregado.** Se você precisa salvar dois agregados atomicamente, provavelmente suas fronteiras estão erradas.
3. **Entre agregados, referencie por ID**, nunca por objeto.

**Os agregados do Studyy:**

| Agregado (raiz) | Contém | Invariante que justifica a fronteira |
|---|---|---|
| `Subject` | `Topic[]` (subtópicos aninhados) | Não pode haver dois tópicos com o mesmo slug dentro da mesma matéria |
| `Note` | `Tag[]` | Anotação precisa ter conteúdo não vazio e pertencer a um tópico existente |
| `StudyPlan` | `PlanEntry[]` | A soma das durações alocadas num mesmo dia não pode exceder o limite diário |
| `StudySession` | `PomodoroCycle[]` | Só um ciclo pode estar ativo por vez; transições de estado válidas |
| `LearnerProgress` | `Badge[]`, `Streak` | XP nunca diminui; nível é sempre derivado do XP; badge não duplica |

> 🔑 **Note como a coluna "invariante" define a fronteira.** Um agregado existe porque há uma regra que precisa ser verdadeira o tempo todo, e para garanti-la você precisa ter todos aqueles dados na mão simultaneamente. Se não há invariante ligando duas coisas, elas **não** pertencem ao mesmo agregado.

**Exemplo concreto — `StudyPlan`:**

```python
class StudyPlan:  # Aggregate Root
    def __init__(self, id: StudyPlanId, daily_limit: Duration) -> None:
        self._id = id
        self._daily_limit = daily_limit
        self._entries: list[PlanEntry] = []

    def allocate(self, topic_id: TopicId, date: StudyDate, duration: Duration) -> None:
        already_allocated = self._total_for(date)
        if already_allocated + duration > self._daily_limit:
            raise DailyLimitExceeded(
                f"Dia {date} já tem {already_allocated.minutes}min "
                f"de {self._daily_limit.minutes}min disponíveis"
            )
        if self._has_entry_for(topic_id, date):
            raise TopicAlreadyAllocated(topic_id, date)
        self._entries.append(PlanEntry(topic_id, date, duration))

    def _total_for(self, date: StudyDate) -> Duration:
        return sum((e.duration for e in self._entries if e.date == date), Duration(0))
```

Essa regra **não pode** morar num service, porque aí qualquer outro caminho no código poderia adicionar uma entry burlando o limite. Dentro do agregado, é impossível burlar.

---

**4. Domain Service**
Para uma regra que **não pertence a nenhuma entidade específica** — tipicamente porque envolve vários agregados.

**No Studyy:** `StudyPlanScheduler` — dado um conjunto de tópicos, uma data de início e uma disponibilidade semanal, gera as alocações automaticamente. Isso não é responsabilidade de `Topic` nem de `StudyPlan` sozinhos.

> ⚠️ Cuidado: Domain Service é a porta de entrada para voltar ao modelo anêmico. Antes de criar um, pergunte três vezes: **essa regra realmente não cabe em nenhuma entidade?**

---

### 🎯 O que construir

1. **Criar a camada `domain/` em cada módulo**
   - `content/domain/`, `planning/domain/`, `execution/domain/`, `progression/domain/`
   - Aqui vivem entidades, VOs, eventos, erros e ports — e **nada mais**

2. **Criar o Shared Kernel mínimo**
   - `shared/domain/entity.py` — base `Entity` (identidade + igualdade por id) e `AggregateRoot` (que acumula domain events)
   - `shared/domain/value_object.py`
   - `shared/domain/errors.py` — `DomainError` base

3. **Modelar todos os VOs** da tabela acima

4. **Transformar as entidades anêmicas em ricas**
   - Atributos privados (`_title`)
   - Sem setters. Só métodos com nome de **intenção do domínio**: `rename()`, `mark_as_completed()`, `attach_tag()`
   - Construtor que garante o estado válido

5. **Definir as fronteiras dos agregados** (use a tabela)

6. **Separar modelo de domínio do modelo de persistência** 🔑
   - `Note` (domínio, dataclass/classe pura) ≠ `NoteModel` (SQLAlchemy)
   - Criar `mappers.py`: `NoteMapper.to_domain(model) -> Note` e `NoteMapper.to_model(note) -> NoteModel`
   - **Esta é a parte mais trabalhosa e a mais importante.** É o que vai permitir que seu domínio seja testado sem banco nenhum.

### 🔧 Patterns aplicados

| Pattern | Onde |
|---|---|
| **Value Object** | `Duration`, `StudyDate`, todos os IDs |
| **Aggregate / Aggregate Root** | `Subject`, `StudyPlan`, `StudySession`, `LearnerProgress` |
| **Factory Method** | `StudySession.start_from(entry)` — criação com invariantes garantidos |
| **Data Mapper** | `mappers.py` — domínio ↔ persistência |
| **Domain Service** | `StudyPlanScheduler` |
| **Specification** (introdução) | Regras de elegibilidade compostas |

### 📁 Estrutura ao final

```
src/studyy/
├── shared/domain/
│   ├── entity.py
│   ├── value_object.py
│   ├── events.py
│   └── errors.py
├── content/
│   ├── domain/
│   │   ├── subject.py        # AggregateRoot
│   │   ├── topic.py          # Entity dentro de Subject
│   │   ├── note.py           # AggregateRoot
│   │   ├── value_objects.py
│   │   ├── ports.py
│   │   └── errors.py
│   ├── service.py            # (vira application/ na Fase 5)
│   └── infrastructure/
│       ├── models.py
│       ├── mappers.py
│       └── repositories.py
```

### ✅ Critérios de aceite

- [ ] **Nenhum arquivo em `*/domain/` importa SQLAlchemy, Pydantic ou FastAPI** — verifique com `grep -r "import sqlalchemy\|from pydantic\|import fastapi" src/studyy/*/domain/` e o resultado deve ser vazio
- [ ] Nenhuma entidade tem atributo público mutável
- [ ] É **impossível** construir uma `Duration` negativa, um `Slug` vazio ou uma `StudySession` sem tópico
- [ ] Todo agregado tem pelo menos um teste unitário que **prova que o invariante é protegido** (testa que a operação inválida levanta erro)
- [ ] Testes de domínio rodam **sem banco, sem async, sem fixture** — Python puro
- [ ] A suíte de testes de domínio roda em menos de 1 segundo
- [ ] `docs/glossario.md` atualizado: cada classe do domínio aparece na tabela de linguagem ubíqua

### ⚠️ Armadilhas

- **Fazer o agregado grande demais.** Se `Subject` carregar todos os `Topic` e todas as `Note` de cada tópico, você carrega 10 MB para renomear uma matéria. Agregado pequeno é quase sempre melhor.
- **Fazer o agregado pequeno demais.** Se `PlanEntry` for um agregado separado de `StudyPlan`, você não consegue garantir o limite diário. O invariante decide.
- **Reutilizar o model do SQLAlchemy como entidade "pra não duplicar".** É a tentação nº1 em Python. Se você ceder, perde tudo: o domínio volta a depender do banco, os testes voltam a precisar de fixture, e o mapeamento lazy-load começa a vazar para dentro das regras. **Não ceda.**
- **VO com `@dataclass` sem `frozen=True`.** VO mutável não é VO.
- **Usar `Optional` em tudo.** Se um campo é obrigatório no domínio, ele não é `None`. `Optional` demais é sinal de que a entidade aceita estado inválido.

### 🎓 Checkpoint Socrático — Fase 4

> Responda **por escrito** em `docs/checkpoints/fase-4.md` antes de marcar a fase como concluída.

1. `StudyPlan` e `PlanEntry` são o **mesmo** agregado, mas `Note` e `Topic` **não** são. Explique a diferença usando a palavra **invariante** — e mostre que regra concreta justifica cada fronteira.
2. Liste **três coisas concretas** que você perde ao reutilizar o model do SQLAlchemy como entidade de domínio. Não responda "fica acoplado" — descreva três consequências que você conseguiria demonstrar.
3. Seus testes de domínio rodam sem banco. **Que classe de bug** isso te permite encontrar mais rápido? E que classe de bug isso te faz perder de vista?
4. `Duration` é um Value Object. **Descreva um bug específico** que existiria se ele fosse um `int` — com valores, não com teoria.
5. Você criou algum Domain Service? **Prove que aquela regra não cabia em nenhuma entidade.** Se não conseguir provar, ela cabia — mova-a e registre aqui.

### 📚 Para estudar

- *Domain-Driven Design Distilled* (Vaughn Vernon) — livro curto, direto, é o melhor ponto de partida
- *Implementing Domain-Driven Design* (Vernon) — capítulos 5 (Entidades), 6 (VOs) e **10 (Agregados)**
- "Effective Aggregate Design" (Vernon) — série de 3 artigos gratuitos em PDF. **Leitura obrigatória desta fase.**
- *Architecture Patterns with Python* (Percival & Gregory) — o livro é literalmente sobre fazer isso em Python. Gratuito em cosmicpython.com

---

## Fase 5 — Clean Architecture / Hexagonal (Ports & Adapters)

**Duração estimada:** 4 a 5 sessões

### 🧠 Conceito em foco: inverter todas as dependências

Arquitetura Hexagonal (Alistair Cockburn, 2005) e Clean Architecture (Uncle Bob, 2012) são, na prática, a mesma ideia com nomes diferentes:

> **O núcleo da aplicação não deve saber nada sobre o mundo externo. Tudo que é externo (HTTP, banco, e-mail, LLM) entra ou sai por uma "porta", e a implementação dessa porta é um "adaptador" plugado de fora.**

```
                        DRIVING SIDE                  DRIVEN SIDE
                     (quem chama a app)            (quem a app chama)

   ┌──────────┐                                                ┌──────────────┐
   │ REST API │──┐                                      ┌──────│  PostgreSQL  │
   └──────────┘  │                                      │      └──────────────┘
   ┌──────────┐  │   ┌────────────────────────────┐     │      ┌──────────────┐
   │   CLI    │──┼──>│        APPLICATION         │<────┼──────│    Redis     │
   └──────────┘  │   │         (Use Cases)        │     │      └──────────────┘
   ┌──────────┐  │   │  ┌──────────────────────┐  │     │      ┌──────────────┐
   │  Worker  │──┘   │  │       DOMAIN         │  │     └──────│   LLM API    │
   └──────────┘      │  │  Entidades, VOs,     │  │            └──────────────┘
                     │  │  Agregados, Eventos  │  │
     ADAPTERS        │  └──────────────────────┘  │              ADAPTERS
    (primários)      └────────────────────────────┘             (secundários)
                       ^                        ^
                   PORTS DE ENTRADA        PORTS DE SAÍDA
                   (o use case em si)      (Protocols definidos
                                            pela aplicação)
```

**Port de entrada (driving/primário):** a interface que o mundo externo usa para acionar a aplicação. Na prática: a assinatura do próprio Use Case.

**Port de saída (driven/secundário):** a interface que a aplicação usa para falar com o mundo. Ex.: `NoteRepository`, `Clock`, `EventPublisher`. **Definido pela aplicação. Implementado pela infraestrutura.**

---

#### Use Case: uma classe por operação

Substituímos os "services gordos" da Fase 2 por **um arquivo e uma classe por operação de negócio**.

```python
# content/application/create_note.py

@dataclass(frozen=True)
class CreateNoteCommand:
    topic_id: UUID
    title: str
    content: str

@dataclass(frozen=True)
class CreateNoteResult:
    note_id: UUID
    created_at: datetime

class CreateNote:
    def __init__(
        self,
        notes: NoteRepository,      # Port de saída
        topics: TopicReader,        # Port de saída
        uow: UnitOfWork,            # Port de saída
        clock: Clock,               # Port de saída (nada de datetime.now()!)
    ) -> None:
        self._notes = notes
        self._topics = topics
        self._uow = uow
        self._clock = clock

    async def execute(self, command: CreateNoteCommand) -> CreateNoteResult:
        topic_id = TopicId(command.topic_id)
        if not await self._topics.exists(topic_id):
            raise TopicNotFound(topic_id)

        note = Note.create(
            topic_id=topic_id,
            title=command.title,
            content=MarkdownContent(command.content),
            now=self._clock.now(),
        )

        async with self._uow:
            await self._notes.save(note)
            await self._uow.commit()

        return CreateNoteResult(note.id.value, note.created_at)
```

Por que um arquivo por use case?
- **Coesão máxima:** tudo sobre "criar anotação" está em um lugar.
- **Dependências mínimas:** este use case depende de 4 ports. Um service gordo dependeria de 12.
- **SRP no nível certo:** um motivo para mudar — a regra de criar anotação.
- **Legibilidade do sistema:** `ls application/` te mostra **tudo que o sistema faz**. Isso se chama *screaming architecture*: a estrutura de pastas grita o que o sistema faz, não qual framework usa.

---

#### O port `Clock` (detalhe pequeno, impacto enorme)

```python
class Clock(Protocol):
    def now(self) -> datetime: ...

class SystemClock:
    def now(self) -> datetime:
        return datetime.now(tz=UTC)

class FrozenClock:                      # para testes
    def __init__(self, at: datetime) -> None: self._at = at
    def now(self) -> datetime: return self._at
```

`datetime.now()` espalhado pelo código é uma dependência oculta e não determinística. Como você testa "o streak quebra se eu pular um dia" com `datetime.now()` hardcoded? Não testa. Com `FrozenClock`, testa em 3 linhas. **Isso vai ser essencial na Fase 8 (streak).**

O mesmo vale para geração de UUID: crie um port `IdGenerator`.

---

#### Unit of Work

Agrupa várias operações numa transação sem que o use case conheça `Session` do SQLAlchemy.

```python
class UnitOfWork(Protocol):
    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(self, *args: object) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
```

---

#### Composition Root

**Um único lugar** no sistema inteiro onde as classes concretas são instanciadas e ligadas. Fora dele, nenhum módulo faz `SqlNoteRepository()`.

```python
# composition_root.py
def build_create_note(session: AsyncSession) -> CreateNote:
    return CreateNote(
        notes=SqlNoteRepository(session),
        topics=SqlTopicReader(session),
        uow=SqlUnitOfWork(session),
        clock=SystemClock(),
    )
```

E no router: `Depends(build_create_note)`. O router não sabe que existe SQLAlchemy.

---

### 🔒 Guardrails: tornando a arquitetura obrigatória

Sem isso, em três semanas alguém (você) vai importar o ORM no domínio às 2h da manhã.

**1. `.importlinter`** na raiz do backend:

```ini
[importlinter]
root_package = studyy

[importlinter:contract:camadas]
name = Regra de dependência: infra -> application -> domain
type = layers
layers =
    infrastructure
    application
    domain
containers =
    studyy.content
    studyy.planning
    studyy.execution
    studyy.progression

[importlinter:contract:contextos-independentes]
name = Bounded contexts não se importam diretamente
type = independence
modules =
    studyy.content
    studyy.planning
    studyy.execution
    studyy.progression

[importlinter:contract:dominio-puro]
name = Domínio não conhece tecnologia
type = forbidden
source_modules =
    studyy.content.domain
    studyy.planning.domain
    studyy.execution.domain
    studyy.progression.domain
forbidden_modules =
    sqlalchemy
    fastapi
    pydantic
    httpx
    redis
```

**2. Rodar no CI:** `uv run lint-imports`. Se violar, o build quebra.

**3. Teste de arquitetura** em `tests/architecture/test_layers.py` — um teste que percorre os arquivos de `domain/` com `ast` e falha se encontrar import proibido. Redundante com o import-linter, mas roda junto com `pytest` e te dá feedback local instantâneo.

---

### 🎯 O que construir

1. Criar `application/` em cada módulo
2. Quebrar cada service gordo em use cases (um arquivo cada)
3. Mover todos os `Protocol` de repositório para `domain/ports.py`
4. Implementar `UnitOfWork`, `Clock`, `IdGenerator`
5. Criar `composition_root.py`
6. Configurar import-linter + testes de arquitetura + CI
7. Router vira **adaptador fino**: converte HTTP -> Command, chama use case, converte Result -> HTTP. Nada mais.
8. **Escrever ADR-004**
9. **Reler `docs/fase-1-retrospectiva.md`** e responder as mesmas 5 perguntas de novo. Compare. Este é o momento em que o roadmap inteiro faz sentido.

### 🔧 Patterns aplicados

| Pattern | Onde |
|---|---|
| **Ports & Adapters** | Toda a estrutura |
| **Use Case / Interactor** | `application/*.py` |
| **Command** | `CreateNoteCommand` — a entrada de cada use case |
| **Unit of Work** | Controle transacional |
| **Data Mapper** | domínio ↔ persistência |
| **Facade** | `composition_root.py` |
| **Null Object** | `NullEventPublisher` para testes |

### ✅ Critérios de aceite

- [ ] `uv run lint-imports` passa e está no CI
- [ ] Nenhum arquivo além de `composition_root.py` instancia um repositório concreto
- [ ] Todo use case é testável com 100% de fakes (zero mocks de biblioteca, zero banco)
- [ ] Nenhum `datetime.now()` fora de `SystemClock`
- [ ] Nenhum `uuid4()` fora de `UuidGenerator`
- [ ] `ls src/studyy/content/application/` descreve, só pelos nomes de arquivo, o que o sistema faz
- [ ] **Teste da inversão:** escreva um `InMemoryNoteRepository` e rode a suíte inteira de use cases com ele. Se passar sem tocar em nenhum use case, a arquitetura está correta.
- [ ] Retrospectiva da Fase 1 respondida de novo, em `docs/fase-5-retrospectiva.md`

### ⚠️ Armadilhas

- **Use case chamando outro use case.** Se A precisa de B, extraia a lógica comum para um Domain Service, ou use um evento. Encadear use cases recria o service gordo.
- **Vazar entidade de domínio na resposta HTTP.** O use case retorna um DTO de resultado, não o agregado. Senão, mudar o domínio quebra a API dos clientes.
- **Criar port para tudo.** Port existe para o que **atravessa a fronteira do processo** (banco, rede, relógio, aleatoriedade, arquivo). Um `SlugGenerator` puro não precisa de port — é lógica, não I/O.
- **Achar que Clean Architecture é uma estrutura de pastas.** É uma **regra de dependência**. Você pode ter as pastas certas e violar tudo. Por isso o import-linter existe.
- **Over-engineering.** Se um use case é um `SELECT` puro para uma tela (ex.: listar matérias), considere um **read model** direto: uma query que devolve o DTO sem passar pelo domínio. Isso é o embrião do CQRS e é perfeitamente legítimo. Domínio rico é para **escrita**, não para leitura.

### 🎓 Checkpoint Socrático — Fase 5

> Responda **por escrito** em `docs/checkpoints/fase-5.md`. Este é o checkpoint mais importante depois do da Fase 1.

1. **Abra `docs/checkpoints/fase-1.md` e responda as mesmas 5 perguntas de novo.** Coloque as duas versões lado a lado. O que mudou nas respostas — e o que mudou em *você* para que elas mudassem?
2. Se o `import-linter` fosse removido amanhã, **quanto tempo até a primeira violação** da regra de dependência? Por que uma ferramenta vence disciplina pessoal, mesmo num projeto solo?
3. O port `Clock` parece exagero para quem olha de fora. **Descreva um teste que seria impossível de escrever sem ele** — e que você vai precisar escrever na Fase 8.
4. Um use case chamando outro é proibido aqui. O problema mais óbvio é transacional. **Qual é o segundo problema**, o que não tem a ver com transação?
5. Clean Architecture é estrutura de pastas ou regra de dependência? **Prove sua resposta com um contra-exemplo:** descreva um projeto com as pastas exatamente certas e a arquitetura completamente errada.

### 📚 Para estudar

- *Clean Architecture* (Uncle Bob) — Parte V, capítulos 22 ("The Clean Architecture") e 23
- "Hexagonal Architecture" — artigo original de Alistair Cockburn
- *Architecture Patterns with Python* — capítulos 4 (Service Layer), 6 (Unit of Work), 7 (Aggregates)
- Documentação do `import-linter`
- "Screaming Architecture" (Uncle Bob) — artigo curto

---

## Fase 6 — Roadmap de Estudos + Pomodoro

**Duração estimada:** 5 a 7 sessões · 🎯 **A feature central do produto.**

### 🧠 Conceito em foco: State Machine e Specification

Até agora o domínio foi CRUD com regras. Agora vem comportamento **temporal** e **estados** — onde modelagem ruim dói de verdade.

---

#### A máquina de estados da Sessão de Estudo

```
                      ┌──────────────────────────────────┐
                      │                                  │
   [criada]           v                                  │
       │         ┌─────────┐   pause()    ┌─────────┐    │
       └────────>│ RUNNING │─────────────>│ PAUSED  │────┘ resume()
    start()      └────┬────┘<─────────────└────┬────┘
                      │                        │
        tick chega    │                        │ abandon()
        ao fim        │                        │
                      v                        v
                 ┌─────────┐              ┌───────────┐
                 │ BREAK   │              │ ABANDONED │ (final)
                 └────┬────┘              └───────────┘
                      │ startNextCycle()
                      │  ou complete()
                      v
                 ┌───────────┐
                 │ COMPLETED │ (final)  --> publica StudySessionCompleted
                 └───────────┘
```

**Transições inválidas que o domínio deve recusar:**
- `pause()` numa sessão `COMPLETED` -> erro
- `start()` numa sessão já `RUNNING` -> erro
- `complete()` numa sessão `PAUSED` sem tempo focado -> erro
- Duas sessões `RUNNING` ao mesmo tempo para o mesmo estudante -> erro

> ⚠️ **A armadilha nº1 aqui:** deixar o frontend controlar o estado e só mandar `PATCH /sessions/{id} {status: "completed"}`. Aí o backend vira um CRUD burro, e um clique errado (ou um F5) corrompe seu progresso. **O backend é a fonte da verdade do estado.** O frontend só envia *intenções* (`POST /sessions/{id}/pause`).

---

#### O tempo focado: a decisão de modelagem crítica

**❌ Abordagem ingênua:** guardar `started_at` e `ended_at`, e calcular a diferença.
Problema: pausas. Se você pausou 40 minutos para almoçar, a diferença mente.

**✅ Abordagem correta:** a sessão guarda uma **lista de intervalos de foco**:

```python
@dataclass(frozen=True)
class FocusInterval:
    started_at: datetime
    ended_at: datetime | None          # None = intervalo ainda aberto

    @property
    def elapsed(self) -> Duration:
        end = self.ended_at or self.started_at
        return Duration(int((end - self.started_at).total_seconds() // 60))
```

`FocusedTime` = soma dos intervalos **fechados**. Isso é auditável, resiliente a reload, e funciona mesmo se o app fechar.

> 💡 **Insight de arquitetura:** essa é uma versão simplificada de **event sourcing** — em vez de guardar o estado final ("focou 47 minutos"), você guarda os fatos que levaram a ele. Estado derivado > estado armazenado, sempre que houver risco de divergência.

---

#### Specification Pattern

Regras de negócio que são **predicados combináveis**, extraídas para objetos próprios.

```python
class Specification(Protocol[T]):
    def is_satisfied_by(self, candidate: T) -> bool: ...

class TopicHasNoNotes:
    def is_satisfied_by(self, topic: Topic) -> bool: ...

class DayHasCapacity:
    def __init__(self, plan: StudyPlan, date: StudyDate, duration: Duration) -> None: ...
    def is_satisfied_by(self, _: object) -> bool: ...

# Combináveis:
spec = DayHasCapacity(...).and_(NotAWeekend()).and_(TopicNotYetCompleted())
```

**Onde usar no Studyy:** regras de agendamento automático (Fase 6) e condições de badge (Fase 8). Em ambos os casos há muitas regras pequenas que se combinam — é exatamente o cenário do pattern.

> ⚠️ Não use Specification para uma regra só. É over-engineering. Use quando há **composição**.

---

### 🎯 O que construir

#### 6.1 — Bounded Context `planning`

**Domínio:**
- `StudyPlan` (raiz) com `PlanEntry[]`
- VOs: `PlanEntryId`, `StudyDate`, `Duration`, `WeeklyAvailability`
- Invariantes:
  - soma de durações por dia ≤ `daily_limit`
  - não alocar o mesmo tópico duas vezes no mesmo dia
  - não alocar em data passada (configurável)
- `StudyPlanScheduler` (Domain Service): distribui N tópicos ao longo dos dias respeitando a disponibilidade semanal

**Use cases:**
- `CreateStudyPlan` — cria plano com meta diária e disponibilidade
- `AllocateTopicToDay` — alocação manual
- `AutoScheduleTopics` — usa o Scheduler
- `RescheduleEntry` — mover uma alocação de dia
- `RemoveEntry`
- `GetDailyAgenda` — read model: o que estudar hoje

**HTTP:**
```
POST   /plans
POST   /plans/{id}/entries
POST   /plans/{id}/auto-schedule
PATCH  /plans/{id}/entries/{entry_id}     # remarcar
DELETE /plans/{id}/entries/{entry_id}
GET    /plans/{id}/agenda?date=2026-09-19
```

#### 6.2 — Bounded Context `execution`

**Domínio:**
- `StudySession` (raiz) com `PomodoroCycle[]` e `FocusInterval[]`
- VOs: `SessionId`, `PomodoroConfig` (foco/pausa curta/pausa longa/ciclos até pausa longa), `FocusedTime`
- Máquina de estados completa (diagrama acima)
- Factory: `StudySession.start_from(entry: PlanEntrySnapshot, config: PomodoroConfig, now: datetime)`

**A regra de ouro do produto:** a duração do Pomodoro **vem da alocação**. Se você planejou 90 minutos para "Derivadas", a sessão configura 90 minutos — quebrados em ciclos (ex.: 4 × 25min com pausas, sobrando ajuste no último).

**Estratégia de quebra em ciclos = Strategy Pattern:**

```python
class CycleBreakdownStrategy(Protocol):
    def breakdown(self, total: Duration, config: PomodoroConfig) -> list[PlannedCycle]: ...

class ClassicPomodoro:      # 25/5, pausa longa de 15 a cada 4
class DeepWork:             # blocos de 50/10
class SingleBlock:          # sem quebra, foco contínuo
```

O usuário escolhe a estratégia por sessão ou por matéria. Formato novo = classe nova. **OCP em ação.**

**Use cases:**
- `StartStudySession` — a partir de um `PlanEntry`
- `PauseSession` / `ResumeSession`
- `TickSession` — avanço do tempo (ou reconciliação, ver abaixo)
- `CompleteSession` -> **publica `StudySessionCompleted`**
- `AbandonSession`
- `GetActiveSession` — para o frontend se recuperar de um reload

**HTTP:**
```
POST /sessions                       {plan_entry_id, strategy}
POST /sessions/{id}/pause
POST /sessions/{id}/resume
POST /sessions/{id}/complete
POST /sessions/{id}/abandon
GET  /sessions/active
```

#### 6.3 — Onde o timer realmente roda (decisão importante)

**❌ Não faça:** o backend rodar um `asyncio.sleep(1500)` por sessão. Não escala, morre em restart, e é impossível de testar.

**✅ Faça:** o **frontend conta** (é o que dá a UI fluida de 1 em 1 segundo) e o **backend reconcilia**:

- Frontend roda o countdown localmente (Zustand + `requestAnimationFrame`/`setInterval`)
- Frontend envia apenas **transições**: `pause`, `resume`, `complete`
- Backend recalcula o tempo focado **a partir dos timestamps dos intervalos**, ignorando o que o frontend afirma
- Ao reabrir o app: `GET /sessions/active` devolve o estado real, e o frontend reconstrói o countdown a partir dele

> 🔑 **Princípio:** *nunca confie no cliente para dados que geram recompensa.* Se o frontend dissesse "focei 90 minutos", bastaria abrir o DevTools para burlar sua própria gamificação — e uma gamificação burlável não motiva ninguém.

### 🔧 Patterns aplicados

| Pattern | Onde | Por quê |
|---|---|---|
| **State** | `StudySession` | Transições válidas garantidas pelo domínio |
| **Strategy** | `CycleBreakdownStrategy` | Novas estratégias sem editar código existente |
| **Specification** | Regras de agendamento | Predicados combináveis |
| **Factory Method** | `StudySession.start_from()` | Criação sempre válida |
| **Domain Service** | `StudyPlanScheduler` | Regra que cruza agregados |
| **Snapshot / DTO de contexto** | `PlanEntrySnapshot` | Execução não importa entidade de Planning |

### ✅ Critérios de aceite

- [ ] Criar plano, alocar tópicos e ver a agenda do dia funciona
- [ ] `POST /sessions` com `plan_entry_id` cria sessão com a duração **vinda da alocação**
- [ ] Testes unitários cobrem **todas** as transições inválidas da máquina de estados
- [ ] Tempo focado é correto depois de: pausar 30min, retomar, pausar de novo, completar
- [ ] Fechar o navegador no meio da sessão e reabrir restaura o estado correto
- [ ] Invariante do limite diário testado (alocar 5h num dia de 4h -> `DailyLimitExceeded`)
- [ ] Trocar `ClassicPomodoro` por `DeepWork` não edita uma linha do agregado
- [ ] Testes de tempo usam `FrozenClock`, nunca `sleep()`
- [ ] Execução não importa nada de `planning.domain` (import-linter confirma)

### ⚠️ Armadilhas

- **Frontend como fonte da verdade do estado.** Já explicado. Não faça.
- **`sleep()` em teste.** Teste com `sleep(2)` é lento e instável. Injete o `Clock`.
- **Esquecer fuso horário.** Guarde tudo em UTC no banco. Converta só na borda. `StudyDate` deve carregar o timezone do usuário — senão o "dia" do streak quebra para quem estuda às 23h.
- **Acoplar Execução a Planejamento.** `StartStudySession` não recebe um `PlanEntry` (entidade de outro contexto). Recebe um `PlanEntrySnapshot` — DTO com `topic_id`, `planned_duration`, `topic_title`. Isso é um **Anti-Corruption Layer** em miniatura.
- **Modelar pausa como estado sem registrar o intervalo.** Aí o tempo focado vira chute.

### 🎓 Checkpoint Socrático — Fase 6

> Responda **por escrito** em `docs/checkpoints/fase-6.md` antes de marcar a fase como concluída.

1. O backend é a fonte da verdade do estado da sessão, não o frontend. **Descreva o ataque concreto**, passo a passo, que seria possível se fosse o contrário. Depois responda: por que isso importa num app que só você usa?
2. Tempo focado como lista de intervalos, em vez de `started_at` / `ended_at`. **Dê um cenário real do seu dia** em que a segunda abordagem mentiria — com horários.
3. Você implementou a máquina de estados com classes (State Pattern clássico) ou com `Enum` + tabela de transições? **Defenda a escolha** e diga em que situação a outra seria melhor.
4. `PlanEntrySnapshot` em vez de importar `PlanEntry`. **Que acoplamento isso evitou?** Descreva o que quebraria, daqui a seis meses, se você tivesse importado a entidade.
5. Houve alguma regra que você **quase** colocou num service em vez de dentro do agregado. Qual foi? Por que resistiu — ou por que não resistiu?

### 📚 Para estudar

- State Pattern (GoF) — e a alternativa mais simples em Python: `Enum` + dicionário de transições válidas
- Specification Pattern (Evans & Fowler) — PDF gratuito "Specifications"
- "Modelling time" — busque sobre modelagem temporal e o problema de "agora" em sistemas
- Documentação do `zoneinfo` (Python 3.9+) para timezone

---

## Fase 7 — Event-Driven Design (in-process)

**Duração estimada:** 3 a 4 sessões

### 🧠 Conceito em foco: Domain Events e desacoplamento por eventos

**O problema:** quando uma sessão de estudo termina, várias coisas precisam acontecer:
- somar XP
- atualizar a ofensiva (streak)
- checar badges
- marcar o tópico como estudado
- (futuro) agendar revisão espaçada
- (futuro) gerar flashcards com IA

Se `CompleteSession` chamar as seis, ele vira um monstro acoplado a metade do sistema. E cada feature nova edita ele de novo — violando OCP e SRP ao mesmo tempo.

**A solução:** o agregado **publica um fato**, e quem se interessa **reage**.

```
  StudySession.complete()
         │
         └──> publica  StudySessionCompleted(
                          session_id, topic_id, focused_minutes,
                          planned_minutes, occurred_at
                       )
                          │
       ┌──────────────────┼──────────────────┬──────────────────┐
       v                  v                  v                  v
  AwardXpHandler   UpdateStreakHandler  CheckBadgesHandler  MarkTopicStudied
   (progression)     (progression)        (progression)       (content)
```

`CompleteSession` **não sabe** que gamificação existe. Adicionar "gerar flashcard" no futuro = criar um handler novo. Zero edição no código existente.

---

#### Evento de domínio ≠ mensagem de integração

| | Domain Event | Integration Event |
|---|---|---|
| Escopo | Dentro do processo | Entre serviços |
| Nome | Passado, linguagem do domínio: `StudySessionCompleted` | Contrato versionado |
| Quando | Publicado pelo agregado, despachado após o commit | Publicado pela infra |
| Acoplamento | Baixo | Muito baixo |

Nesta fase fazemos só **Domain Events in-process**. A Fase 12 os promove a mensagens em fila.

---

#### Regra crítica: despachar DEPOIS do commit

```python
# ❌ ERRADO — handler roda antes de saber se salvou
session.complete(now)
await event_bus.publish(session.pull_events())   # e se o commit falhar?
await uow.commit()

# ✅ CORRETO
session.complete(now)
async with uow:
    await sessions.save(session)
    await uow.commit()
await event_bus.publish(session.pull_events())   # só depois do commit
```

Se você publicar antes, um commit que falha deixa o estudante com XP de uma sessão que não existe. (E mesmo o jeito correto tem uma falha: se o processo morrer entre o commit e o publish, o evento se perde. A solução definitiva é o **Outbox Pattern**, na Fase 12 — anote como dívida consciente.)

---

#### Implementação do agregado que acumula eventos

```python
# shared/domain/entity.py
class AggregateRoot:
    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events
```

```python
# execution/domain/study_session.py
def complete(self, now: datetime) -> None:
    if self._status not in (SessionStatus.RUNNING, SessionStatus.BREAK):
        raise InvalidSessionTransition(self._status, "complete")
    self._close_open_interval(now)
    self._status = SessionStatus.COMPLETED
    self._record(StudySessionCompleted(
        session_id=self._id,
        topic_id=self._topic_id,
        focused=self.focused_time,
        planned=self._planned_duration,
        occurred_at=now,
    ))
```

### 🎯 O que construir

1. `shared/domain/events.py` — `DomainEvent` base (com `event_id`, `occurred_at`)
2. `AggregateRoot` com `_record()` / `pull_events()`
3. `shared/application/event_bus.py` — Port `EventPublisher`
4. `InMemoryEventBus` na infraestrutura (dicionário `tipo de evento -> lista de handlers`)
5. Registro de handlers no `composition_root.py`
6. Definir o catálogo de eventos:
   - `StudySessionStarted`
   - `StudySessionCompleted`
   - `StudySessionAbandoned`
   - `NoteCreated`
   - `TopicCompleted`
   - `DailyGoalAchieved`
   - `LevelUp`
   - `BadgeUnlocked`
   - `StreakBroken`
7. Migrar as reações que hoje estão dentro dos use cases para handlers
8. **ADR-005**

### 🔧 Patterns aplicados

| Pattern | Onde |
|---|---|
| **Domain Event** | `shared/domain/events.py` |
| **Observer / Pub-Sub** | `InMemoryEventBus` |
| **Mediator** | O barramento desacopla publicador de handler |
| **Null Object** | `NullEventPublisher` para testes que não se importam com eventos |

### ✅ Critérios de aceite

- [ ] `CompleteSession` não importa **nada** do módulo `progression`
- [ ] Adicionar um handler novo não edita nenhum use case
- [ ] Eventos só são despachados **após** o commit (teste: force falha no commit e verifique que nenhum handler rodou)
- [ ] Todo evento é imutável (`@dataclass(frozen=True)`) e nomeado no passado
- [ ] Evento carrega **dados**, não entidades (`topic_id: UUID`, não `topic: Topic`)
- [ ] Teste de integração: completar sessão -> XP creditado -> ambos verificados no banco
- [ ] `docs/eventos.md` com o catálogo: nome, payload, quem publica, quem consome

### ⚠️ Armadilhas

- **Evento carregando o agregado inteiro.** Quebra a fronteira e vira serialização impossível. Só IDs e valores.
- **Handler que falha derrubando o use case.** Decida a política: se o XP falhar, a sessão ainda foi concluída? (Sim.) Então capture a exceção do handler, logue, e siga. Documente isso.
- **Nome no imperativo.** `CompleteSession` é um comando. `StudySessionCompleted` é um evento. Comando pode ser recusado; evento é um fato que já aconteceu.
- **Cadeia de eventos profunda.** Handler que publica evento que dispara handler que publica evento... vira impossível de depurar. Máximo 2 níveis, e logue o `correlation_id`.
- **Event-driven em tudo.** Se a reação é síncrona, obrigatória e parte da mesma transação conceitual, chamar direto é mais simples e mais honesto.

### 🎓 Checkpoint Socrático — Fase 7

> Responda **por escrito** em `docs/checkpoints/fase-7.md` antes de marcar a fase como concluída.

1. `CompleteSession` não sabe que gamificação existe. **Que princípio do SOLID isso realiza**, e por qual mecanismo exatamente?
2. Eventos são despachados **depois** do commit. **Descreva o bug**, com a sequência de passos, que aconteceria no jeito errado — e diga quanto tempo você levaria para notá-lo em produção.
3. Mesmo do jeito certo, o evento ainda pode se perder. **Onde exatamente?** Por que você aceitou conscientemente essa dívida agora em vez de resolvê-la já?
4. **Dê um exemplo do próprio Studyy** em que chamar o método diretamente é melhor do que publicar um evento. Qual é o critério que separa os dois casos?
5. `CompleteSession` é comando, `StudySessionCompleted` é evento. Além da convenção de nome, **o que muda na prática** entre os dois? (Dica: um deles pode ser recusado.)

### 📚 Para estudar

- *Architecture Patterns with Python* — capítulos 8, 9 e 10 (Events, Message Bus, Commands vs Events). **É o melhor material que existe para exatamente esta fase.**
- "Domain Events — Design and Implementation" (documentação de microsserviços da Microsoft)
- Diferença entre Event Notification, Event-Carried State Transfer e Event Sourcing (Martin Fowler, "What do you mean by Event-Driven?")

---

## Fase 8 — Gamificação e Progressão

**Duração estimada:** 3 a 5 sessões

### 🧠 Conceito em foco: um Bounded Context puramente reativo

`progression` é o módulo mais isolado do sistema: ele **não tem nenhuma API de escrita própria**. Ele só reage a eventos. É a prova viva de que a arquitetura das fases 5 e 7 funcionou.

### 🎯 Design do sistema de progressão

#### XP — quanto vale uma sessão

```
XP base       = minutos focados
Bônus de meta = +20% se a sessão cumpriu ≥ 100% do tempo planejado
Bônus streak  = +5% por dia de ofensiva, limitado a +50%
Penalidade    = sessão abandonada antes de 25% do tempo => 0 XP
```

A fórmula muda com o tempo (você vai querer calibrar). Então ela é uma **Strategy**:

```python
class XpPolicy(Protocol):
    def calculate(self, event: StudySessionCompleted, streak: Streak) -> XpPoints: ...

class DefaultXpPolicy: ...
class WeekendBoostPolicy: ...     # experimentos futuros
```

#### Níveis — curva de progressão

```
XP necessário para o nível N = 100 * N^1.5
```

| Nível | XP acumulado | ~Horas de estudo |
|---|---|---|
| 1 | 0 | 0 |
| 2 | 283 | ~5h |
| 5 | 1.118 | ~19h |
| 10 | 3.162 | ~53h |
| 20 | 8.944 | ~149h |

**Nível é derivado, nunca armazenado.** Se você guardar `level` numa coluna e depois mudar a curva, os dados ficam inconsistentes. Guarde `total_xp`; calcule o nível. Isso é um Value Object:

```python
@dataclass(frozen=True)
class Level:
    value: int

    @classmethod
    def from_xp(cls, xp: XpPoints) -> "Level":
        return cls(int((xp.value / 100) ** (1 / 1.5)) + 1)
```

#### Streak (ofensiva) — a mecânica mais motivadora e mais sutil

```
Meta diária cumprida  -> streak += 1
Dia perdido           -> streak = 0, publica StreakBroken
Freeze                -> 1 "congelamento" a cada 7 dias de ofensiva, máx. 2 acumulados
```

**A sutileza:** "dia perdido" só pode ser detectado pela **ausência** de algo — e ausência não gera evento. Duas opções:

| Opção | Como | Prós / Contras |
|---|---|---|
| **A. Cálculo preguiçoso** | Ao ler o progresso, compare `last_goal_date` com hoje e recalcule | ✅ Sem infra extra · ❌ Não gera notificação |
| **B. Job diário** | Tarefa agendada à meia-noite (timezone do usuário) verifica e quebra | ✅ Permite notificar · ❌ Precisa de scheduler (Fase 12) |

**Faça A agora, B na Fase 12.** E registre isso como dívida consciente.

#### Badges — Specification Pattern na veia

```python
class BadgeRule(Protocol):
    badge: Badge
    def is_satisfied_by(self, progress: LearnerProgress, ctx: ProgressContext) -> bool: ...
```

| Badge | Condição |
|---|---|
| 🌱 Primeiro Passo | Primeira sessão concluída |
| 🔥 Semana de Fogo | Streak de 7 dias |
| 🌋 Mês Imparável | Streak de 30 dias |
| 🦉 Coruja | Sessão concluída depois das 23h |
| 🐓 Madrugador | Sessão concluída antes das 7h |
| 📚 Maratonista | 4h de foco em um único dia |
| 🎯 Cirurgião | 10 sessões seguidas cumprindo 100% do planejado |
| 🧠 Polímata | Sessões em 5 matérias diferentes na mesma semana |
| ✍️ Escriba | 50 anotações criadas |
| 💎 Centurião | 100 horas de foco acumuladas |

Cada badge = uma classe. Badge nova = arquivo novo + registro. **Zero edição.** OCP puro.

#### ⚠️ Princípio de design de gamificação

Gamificação mal feita vira ansiedade e culpa, e aí você abandona o app — o oposto do objetivo. Três regras:

1. **Recompense esforço, não resultado.** XP por tempo focado, não por "tópico dominado".
2. **Nunca remova XP.** Progresso acumulado é permanente. Streak pode zerar (é a mecânica), XP não.
3. **Streak freeze existe por um motivo.** Streak de 60 dias que morre por uma gripe faz a pessoa desistir do app inteiro. Dê a rede de proteção.

### 🎯 O que construir

**Domínio (`progression/domain/`):**
- `LearnerProgress` (raiz): `total_xp`, `streak`, `badges`, `last_goal_date`, `freezes`
- VOs: `XpPoints`, `Level`, `Streak`, `Badge`, `DailyGoal`
- Invariantes: XP nunca diminui; badge não duplica; freezes ≤ 2

**Handlers (`progression/application/handlers/`):**
- `on_study_session_completed` -> credita XP, checa meta diária, atualiza streak, avalia badges
- `on_study_session_abandoned` -> registra, sem penalidade de XP
- `on_note_created` -> avalia badge de escriba

**Read models (para a tela):**
- `GetProgressSummary` — nível, XP, XP até o próximo nível, streak, badges
- `GetWeeklyHeatmap` — minutos focados por dia (estilo GitHub contributions)
- `GetSubjectDistribution` — tempo por matéria

**HTTP (somente leitura):**
```
GET /progress
GET /progress/heatmap?weeks=12
GET /progress/badges
GET /progress/distribution
```

### 🔧 Patterns aplicados

| Pattern | Onde |
|---|---|
| **Strategy** | `XpPolicy`, curva de nível |
| **Specification** | Regras de badge |
| **Registry** | Catálogo de badges |
| **Event Handler** | Reação a eventos de execução |
| **Read Model / CQRS-lite** | Queries de dashboard sem passar pelo domínio |

### ✅ Critérios de aceite

- [ ] `progression` **não tem nenhum endpoint de escrita** — só reage a eventos
- [ ] `progression` não importa nada de `execution` ou `planning` (import-linter confirma)
- [ ] Nível é sempre calculado a partir do XP, nunca persistido
- [ ] Badge nova = 1 arquivo novo + 1 linha no registro
- [ ] Streak testado com `FrozenClock`: 5 dias seguidos, pula 1, verifica quebra
- [ ] Streak freeze testado
- [ ] Teste de idempotência: processar `StudySessionCompleted` duas vezes **não** dá XP dobrado (use o `event_id` como chave de deduplicação — isso te prepara para a Fase 12)
- [ ] Heatmap responde em < 100ms com 1 ano de dados (índice em `(user_id, date)`)

### ⚠️ Armadilhas

- **Persistir o nível.** Já explicado. Não faça.
- **Calcular streak com `date.today()`.** Fuso horário. Use `StudyDate` com o timezone do usuário. Quem estuda às 23h30 em UTC-3 não pode perder o streak porque em UTC já é amanhã.
- **Handler não idempotente.** Se um dia você reprocessar eventos (e vai), XP duplica. Deduplique por `event_id` desde já.
- **Gamificação punitiva.** Remover XP por inatividade gera abandono, não motivação.
- **Badge que consulta o banco inteiro.** `Polímata` precisa de "matérias distintas na semana" — passe isso no `ProgressContext` montado pelo handler, não deixe a spec fazer I/O.

### 🎓 Checkpoint Socrático — Fase 8

> Responda **por escrito** em `docs/checkpoints/fase-8.md` antes de marcar a fase como concluída.

1. Nível é derivado do XP, nunca persistido. **Descreva o cenário exato**, com datas, em que persistir o nível te daria dados inconsistentes.
2. Detectar streak quebrado significa detectar uma **ausência**. Por que ausência é estruturalmente difícil num sistema que reage a eventos? Que outros "eventos que não acontecem" existem no Studyy?
3. Você implementou idempotência **antes** de ter fila. Por quê? Que evidência te faria concluir que foi trabalho desperdiçado?
4. O módulo `progression` não tem nenhum endpoint de escrita. **Isso é uma limitação ou uma propriedade desejada?** Argumente dos dois lados e depois escolha.
5. **Invente uma badge que seria impossível de implementar** com a arquitetura atual. Por que é impossível? O que precisaria mudar — e esse custo valeria a pena?

### 📚 Para estudar

- "Octalysis Framework" (Yu-kai Chou) — os 8 drivers da gamificação; útil para não fazer gamificação tóxica
- *Architecture Patterns with Python* — capítulo 12 (CQRS) para os read models
- Idempotência em processamento de mensagens

---

## Fase 9 — Frontend (Next.js)

**Duração estimada:** 6 a 10 sessões

### 🧠 Conceito em foco: o frontend é só mais um adaptador

Na arquitetura hexagonal, a UI web é um **driving adapter**. Ela não contém regra de negócio — ela traduz intenção humana em comandos para a aplicação.

**Corolário prático:** se você precisar reimplementar uma regra no frontend, ou a regra está no lugar errado, ou você está fazendo validação de UX (que é legítima, mas é *duplicação consciente*, não a fonte da verdade).

### 🎯 O que construir

#### Estrutura por feature, não por tipo

```
frontend/src/
├── app/
│   ├── (dashboard)/page.tsx           # hoje: agenda + progresso
│   ├── subjects/[id]/page.tsx
│   ├── notes/[id]/page.tsx
│   ├── plan/page.tsx                  # roadmap / calendário
│   └── focus/[sessionId]/page.tsx     # o Pomodoro em tela cheia
├── features/
│   ├── notes/     { api/ components/ hooks/ types.ts }
│   ├── planning/  { api/ components/ hooks/ types.ts }
│   ├── pomodoro/  { api/ components/ store.ts types.ts }
│   └── progression/
└── shared/  { ui/ lib/ api-client.ts }
```

#### Telas essenciais

| Tela | Conteúdo |
|---|---|
| **Dashboard** | Agenda de hoje, botão "iniciar" por tópico, card de progresso (nível/XP/streak), heatmap |
| **Matérias** | Árvore Matéria -> Tópico -> Subtópico, com status visual |
| **Editor de anotação** | Markdown com preview, autosave (debounce 2s), atalhos, seleção de tópico, tags |
| **Roadmap** | Calendário (semanal/mensal) com drag-and-drop de alocações; barra de capacidade por dia |
| **Foco (Pomodoro)** | Timer grande, anel de progresso, tópico atual, ciclo atual, pausar/retomar/concluir |
| **Progresso** | Nível, XP, badges (desbloqueados e bloqueados), heatmap, distribuição por matéria |

#### O timer no frontend — pontos de atenção

```typescript
// Nunca acumule: contador += 1 a cada tick. Drift garantido.
// Sempre derive do horário absoluto:
const remaining = endsAt.getTime() - Date.now();
```

- Use `Date.now()` contra um `endsAt` absoluto, não incremento
- `document.visibilitychange`: ao voltar à aba, **reconcilie com `GET /sessions/active`**
- Persista `sessionId` no `localStorage` para sobreviver a reload
- Notificação do navegador ao fim do ciclo (peça permissão antes)
- Áudio de alerta (com opção de mudo)
- `navigator.wakeLock` para a tela não apagar durante o foco

#### Cliente de API tipado

Gere tipos do OpenAPI do FastAPI (`openapi-typescript`) — assim o contrato entre back e front é verificado pelo compilador. Isso é DIP aplicado entre sistemas.

### ✅ Critérios de aceite

- [ ] Todas as 6 telas funcionam contra a API real
- [ ] Nenhuma regra de negócio duplicada no frontend (validação de UX é ok e está comentada como tal)
- [ ] Timer não sofre drift em 90 minutos (teste: compare com relógio externo)
- [ ] Fechar a aba no meio do foco e reabrir restaura o estado correto
- [ ] Tipos da API gerados do OpenAPI, não escritos à mão
- [ ] Estados de loading, erro e vazio em toda tela
- [ ] Funciona em mobile (você vai querer ver a agenda no celular)
- [ ] Atalhos de teclado: `n` nova anotação, `espaço` pausa/retoma

### ⚠️ Armadilhas

- **Reimplementar o cálculo de XP no frontend "pra mostrar na hora".** Se divergir do backend, gera desconfiança. Peça o valor ao backend ou mostre otimista com reconciliação.
- **Organizar por tipo (`components/`, `hooks/`, `services/`).** Escala mal. Por feature, sempre.
- **Deixar o `fetch` solto nos componentes.** Centralize em `features/*/api/`.
- **`setInterval` incremental.** Drift. Já explicado.

### 🎓 Checkpoint Socrático — Fase 9

> Responda **por escrito** em `docs/checkpoints/fase-9.md` antes de marcar a fase como concluída.

1. O frontend é um adaptador, não o sistema. **Onde você foi tentado a colocar regra de negócio nele?** Descreva a tentação e o que você fez.
2. Validação duplicada no frontend é aceitável como UX. **Qual é a regra objetiva** para distinguir duplicação sadia de duplicação perigosa? Aplique-a a um caso real do seu código.
3. Explique o drift do `setInterval` incremental **em números**: quanto de erro acumula em 90 minutos e por quê?
4. Tipos gerados do OpenAPI eliminam uma classe de bug. **Qual classe continua existindo** apesar deles? Dê um exemplo.
5. Se amanhã você tivesse que trocar o Next.js por uma CLI, **quanto do backend mudaria?** Responda em número de arquivos. Esse número é bom ou ruim — e qual fase o determinou?

### 📚 Para estudar

- Next.js App Router: Server Components vs Client Components (o timer é obrigatoriamente client)
- TanStack Query: `staleTime`, invalidação, optimistic updates
- `openapi-typescript` / `orval`

---

## Fase 10 — Infraestrutura, Deploy e Cloudflare

**Duração estimada:** 3 a 5 sessões · 🏁 **Marco: o Studyy sai da sua máquina e vai para o ar.**

### 🧠 Conceito em foco: a fronteira entre o seu código e o mundo

Até aqui, tudo que você construiu roda em `localhost`. Colocar no ar não é "só subir o servidor" — é tomar uma série de decisões arquiteturais que quase ninguém documenta:

- **Onde o código roda** (e por que não roda em qualquer lugar)
- **Quem fala com quem** (origem, borda, banco, usuário)
- **Como o segredo viaja** sem vazar
- **Como você atualiza** sem derrubar
- **Como você volta atrás** quando der errado

#### Borda (edge) vs Origem (origin)

```
   Você (navegador)
        │
        v
  ┌─────────────────────────────────────────────┐
  │  CLOUDFLARE  (a "borda" — 300+ cidades)     │
  │  DNS · TLS · CDN · WAF · Rate limit · Access│
  └──────────────┬──────────────────────────────┘
                 │  (só o tráfego que sobreviveu)
                 v
  ┌─────────────────────────────────────────────┐
  │  ORIGEM  (um lugar só — seu container)      │
  │  FastAPI + worker                           │
  └──────────────┬──────────────────────────────┘
                 v
  ┌─────────────────────────────────────────────┐
  │  BANCO  (Postgres gerenciado)               │
  └─────────────────────────────────────────────┘
```

**A ideia central:** quanto mais trabalho a borda resolve, menos a origem sofre. Um arquivo estático servido de São Paulo em 8ms nunca tocou seu servidor. Um bot bloqueado pelo WAF nunca consumiu sua CPU.

> 🔑 **Isto é o mesmo princípio da Fase 5, num nível diferente.** Lá, os adaptadores protegiam o domínio da tecnologia. Aqui, a borda protege a origem do mundo. Arquitetura é sempre sobre **onde você coloca as fronteiras e o que passa por elas**.

---

### 🏗️ A arquitetura de deploy escolhida

#### Uma verdade desconfortável primeiro

**O FastAPI não roda no Cloudflare Workers.** Workers executam JavaScript/WASM num runtime V8 isolado. Existe Python Workers (via Pyodide), mas sem suporte real a `asyncpg`, SQLAlchemy async e boa parte do ecossistema — e com limite de CPU por requisição incompatível com o que você precisa.

Isso é uma lição por si só: **"serverless" não é um lugar, é um conjunto de restrições.** Quem promete que você "roda qualquer coisa na borda" está vendendo.

#### A divisão que funciona

| Peça | Onde | Por quê |
|---|---|---|
| **Frontend Next.js** | **Cloudflare Pages** | Estático + SSR no edge. Grátis, rápido, preview por branch. |
| **Backend FastAPI** | **Container** (Fly.io, Railway ou VPS) | Precisa de runtime Python real, processo longo, conexão persistente com o banco |
| **Worker (Fase 12)** | Mesmo container ou processo irmão | Mesma imagem, comando diferente |
| **Postgres** | **Neon** ou **Supabase** (gerenciado) | Backup, PITR e réplica sem você operar nada |
| **Redis (Fase 12)** | Upstash ou o mesmo provedor | Serverless, cobra por requisição |
| **Arquivos** (PDFs, imagens) | **Cloudflare R2** | Egress grátis — a diferença que importa vs S3 |
| **DNS, TLS, CDN, WAF, Access** | **Cloudflare** | Tudo isso no plano gratuito |

> 💡 **Recomendação:** **Fly.io** para a origem. Roda container, tem região em Guarulhos (latência baixa até o banco e até você), escala para zero se quiser, e o `fly.toml` é simples de versionar. Railway é ainda mais fácil, porém mais caro. Uma VPS (Hetzner/DigitalOcean) é a opção mais barata e a que mais ensina — e também a que mais toma seu tempo.

---

### 🔐 O truque mais valioso desta fase: Cloudflare Access

O Studyy é pessoal. Você precisa que **só você** entre. O caminho óbvio seria construir login, hash de senha, sessão, refresh token, recuperação de senha, rate limit no login...

**Não construa nada disso.**

**Cloudflare Access** (Zero Trust, gratuito até 50 usuários) coloca uma tela de autenticação **na frente da sua aplicação**, na borda. Você define uma política ("só o e-mail X pode entrar"), escolhe o provedor (Google, GitHub ou código por e-mail), e pronto. A requisição só chega na sua origem **se já estiver autenticada** — e chega com um JWT assinado que sua aplicação pode validar.

```
Navegador -> Cloudflare Access -> [login Google] -> JWT assinado -> Sua origem
                    │
                    └── requisição sem auth morre aqui, nunca toca seu servidor
```

O que sua aplicação precisa fazer: validar o header `Cf-Access-Jwt-Assertion` contra a chave pública do Cloudflare e extrair o e-mail. **Umas 30 linhas**, num middleware — que é, mais uma vez, um **adaptador**.

> 🎯 **A lição de arquitetura aqui é grande:** a melhor autenticação é a que você não escreveu. Auth é uma das áreas onde errar é catastrófico e onde o problema já está resolvido por quem tem mais recursos que você. **Reconhecer o que NÃO construir é uma decisão de arquitetura tão legítima quanto escolher um pattern.**
>
> Se um dia o Studyy virar multiusuário público, aí sim você troca — e vai trocar só o adaptador. (Registre isso no ADR-009 como o gatilho de reversão.)

---

### 🛡️ O que mais a borda faz por você

| Recurso Cloudflare | O que resolve | Configuração |
|---|---|---|
| **DNS + Proxy (nuvem laranja)** | Esconde o IP da origem; ninguém ataca o que não encontra | Registro `A`/`CNAME` proxiado |
| **TLS automático** | HTTPS sem Certbot, sem renovação, sem cron quebrado | Modo **Full (strict)** |
| **CDN / Cache** | Assets do Next.js servidos da borda | Regra de cache por rota |
| **WAF** | Bloqueia SQLi, XSS, bots conhecidos | Regras gerenciadas (grátis) |
| **Rate Limiting** | Protege `/assistant/ask` (que custa dinheiro em LLM!) | Regra por IP/rota |
| **Cloudflare Tunnel** | Expõe sua máquina local sem abrir porta no roteador | `cloudflared` — ótimo para testar no celular |
| **R2** | Armazena anexos das anotações, egress grátis | Bucket + binding |
| **Web Analytics** | Métricas de uso sem cookie e sem LGPD-drama | Snippet no frontend |

> ⚠️ **Cuidado crítico com cache de borda:** **nunca** cacheie na borda uma resposta que contenha dados pessoais. `/progress` é seu progresso — se o Cloudflare cachear e servir para outra pessoa, você vazou dados. Regra: cacheie por rota, explicitamente, e só o que é público ou imutável. O padrão para a API deve ser `Cache-Control: private, no-store`.

---

### 📦 Containers e os 12 fatores

Seu backend vira uma imagem Docker. Princípios que importam (do [12-Factor App](https://12factor.net)):

| Fator | O que significa no Studyy |
|---|---|
| **Config no ambiente** | `DATABASE_URL`, `ANTHROPIC_API_KEY` vêm de variável, nunca do código. Seu `Settings` da Fase 0 já faz isso ✅ |
| **Dependências explícitas** | `uv.lock` commitado. Build reprodutível. |
| **Processos sem estado** | A origem não guarda nada em memória entre requisições. **Teste:** rode 2 instâncias — se quebrar, você tinha estado escondido. |
| **Paridade dev/prod** | Mesma imagem em todo lugar; só a config muda |
| **Logs como stream** | Escreva em `stdout`, não em arquivo. A plataforma coleta. (Prepara a Fase 13.) |
| **Descartabilidade** | Start rápido, shutdown gracioso (termine as requisições em voo antes de morrer) |

**Dockerfile multi-stage:** um estágio compila as dependências, outro só copia o resultado. Imagem final pequena, sem compilador, sem ferramenta de build — menos superfície de ataque.

**Rode como usuário não-root.** É uma linha no Dockerfile e elimina uma classe inteira de escalada de privilégio.

---

### 🔑 Segredos: o caminho que eles percorrem

Desenhe este caminho. É o exercício que mais pega gente desprevenida.

```
  .env local (gitignored)
        │
        v
  GitHub Secrets ──────> GitHub Actions ──────> fly secrets set
        │                      │                      │
        └── nunca no log       └── mascarado          v
                                               Variável de ambiente
                                               dentro do container
                                                      │
                                                      v
                                               Settings (Pydantic)
```

**Regras inegociáveis:**
- `.env` **nunca** no git. Verifique com `git log -p | grep -i "api_key"` — se achou, o segredo já vazou e precisa ser rotacionado, não apagado.
- Segredo diferente por ambiente. O banco de staging nunca usa a credencial de produção.
- Rotação: saiba **como** trocar cada segredo antes de precisar trocar às pressas.

---

### 🚀 Ambientes e pipeline

| Ambiente | Onde | Banco | Para quê |
|---|---|---|---|
| **local** | Docker Compose | Postgres local | Desenvolvimento |
| **preview** | Cloudflare Pages (por branch) + origem de staging | Banco de staging | Ver a feature antes do merge |
| **production** | Pages + Fly.io | Neon (com PITR) | Você usando de verdade |

**Pipeline no GitHub Actions:**

```
push na branch
    │
    ├─> ruff + mypy + lint-imports + pytest        (o CI da Fase 0)
    │
    ├─> [se passou] build da imagem Docker
    │
    ├─> [se for PR] deploy de preview -> comenta a URL no PR
    │
    └─> [se for main] migration -> deploy -> healthcheck -> pronto
                                       │
                                       └─ falhou? rollback automático
```

#### Migrations em produção: expand / contract

O erro clássico: rodar a migration e o deploy ao mesmo tempo. Durante alguns segundos, código velho conversa com schema novo — e quebra.

O padrão correto tem três deploys:

1. **Expand** — adiciona a coluna nova (nullable). O código velho ignora, o novo já pode usar.
2. **Migrate** — o código novo escreve nos dois lugares; um backfill preenche o histórico.
3. **Contract** — só depois que ninguém lê o campo antigo, remove-o.

> Parece exagero para um app de um usuário. Mas é exatamente a mesma lógica das suas refatorações das fases 2 a 5: **mude em passos onde cada passo individual é seguro**, em vez de um salto grande onde você reza. É o mesmo princípio, aplicado a dados em vez de código.

---

### 🏗️ Infraestrutura como Código

Configurar o Cloudflare clicando no painel funciona — até você não lembrar o que clicou.

**Terraform com o provider do Cloudflare** versiona: registros DNS, políticas do Access, regras de WAF e rate limit, regras de cache, buckets R2.

```hcl
resource "cloudflare_record" "api" {
  zone_id = var.zone_id
  name    = "api"
  content = var.origin_host
  type    = "CNAME"
  proxied = true          # a nuvem laranja: esconde a origem
}
```

> 💡 **O paralelo com a Fase 0 é direto:** você não aceita mudança de código sem commit e sem review. Por que aceitaria mudança de infraestrutura sem isso? IaC é controle de versão aplicado à infra — e `terraform plan` é o seu `git diff`.

**Comece pequeno:** DNS e Access no Terraform. O resto migra quando doer.

---

### 🎯 O que construir

1. **Dockerfile multi-stage** para o backend, rodando como não-root, com shutdown gracioso
2. **Deploy da origem** (Fly.io recomendado) com healthcheck apontando para `/health/ready`
3. **Postgres gerenciado** (Neon) com backup automático — e **um restore testado de verdade**
4. **Frontend no Cloudflare Pages**, com preview por branch
5. **Domínio + DNS proxiado + TLS Full (strict)**
6. **Cloudflare Access** na frente de tudo, com política de e-mail único; middleware validando o JWT
7. **Regras de cache por rota** — assets agressivo, API `no-store`
8. **Rate limiting** em `/assistant/*` (te salva de uma conta de LLM inesperada na Fase 14)
9. **R2** para anexos de anotação
10. **GitHub Actions**: teste -> build -> migration -> deploy -> healthcheck -> rollback em falha
11. **Terraform** para DNS e Access
12. **Cloudflare Tunnel** para acessar o ambiente local pelo celular durante o desenvolvimento
13. **Planilha de custo** mensal real de cada peça
14. **ADR-008** (onde hospedar cada coisa) e **ADR-009** (Access em vez de auth própria)

### 🔧 Patterns aplicados

| Pattern | Onde | O que resolve |
|---|---|---|
| **Reverse Proxy / Gateway** | Cloudflare na frente da origem | Ponto único de política: TLS, auth, rate limit |
| **Edge Cache** | Regras de cache do CDN | Trabalho que a origem nunca faz |
| **Sidecar de autenticação** | Access validando antes da origem | Auth fora da aplicação |
| **Preview Deploy** | Pages por branch | Ver antes de mergear |
| **Expand / Contract** | Migrations | Mudança de schema sem downtime |
| **Infrastructure as Code** | Terraform | Infra revisável e reproduzível |
| **Health Check** | `/health/live` e `/health/ready` | Deploy que sabe se deu certo |

### ✅ Critérios de aceite

- [ ] `https://studyy.seudominio.com` abre, com TLS válido
- [ ] Acesso de uma aba anônima cai na tela do Cloudflare Access
- [ ] O IP da origem **não** é descobrível (teste: `dig` no domínio devolve IP do Cloudflare)
- [ ] `git push` na `main` faz deploy sozinho, sem passo manual
- [ ] PR gera URL de preview funcionando
- [ ] Deploy que falha no healthcheck faz **rollback automático** (teste: quebre de propósito)
- [ ] Nenhum segredo no repositório (`git log -p | grep -iE "key|secret|password"` limpo)
- [ ] Backup do banco **restaurado de verdade** num banco novo
- [ ] Duas instâncias da origem rodando simultaneamente sem quebrar nada (prova de statelessness)
- [ ] `/progress` **não** é cacheado na borda (verifique o header `cf-cache-status: DYNAMIC`)
- [ ] Rate limit funciona (dispare 100 requisições e veja o 429)
- [ ] DNS e Access versionados em Terraform; `terraform plan` limpo
- [ ] Você abriu o Studyy **no celular**, autenticou e iniciou um Pomodoro
- [ ] Custo mensal documentado em `docs/custos.md`

### ⚠️ Armadilhas

- **Cachear resposta autenticada na borda.** Vazamento de dado pessoal. O default da API é `private, no-store`.
- **TLS em modo "Flexible".** Cloudflare fala HTTPS com o usuário e **HTTP** com sua origem. Parece seguro e não é. Use **Full (strict)**.
- **Deixar a origem acessível por IP direto.** Alguém contorna o Access e fala direto com seu servidor. Restrinja por IPs do Cloudflare, ou use Tunnel (que dispensa porta aberta).
- **Rodar migration junto com o deploy, sem expand/contract.** Funciona até o dia em que não funciona.
- **Backup que nunca foi restaurado.** Não é backup, é esperança. Teste o restore.
- **Painel como fonte da verdade.** Em três meses você não lembra o que configurou nem por quê.
- **Escolher a plataforma pelo "grátis".** Free tier de banco costuma dormir após inatividade — e um app de estudo que leva 8 segundos para abrir você não usa. Pague os poucos dólares do tier que não hiberna.
- **Adiar a fase de deploy.** Quanto mais tarde você coloca no ar, mais caro fica. Suba cedo, suba feio.

### 🎓 Checkpoint Socrático — Fase 10

> Responda **por escrito** em `docs/checkpoints/fase-10.md` antes de marcar a fase como concluída.

1. Por que o FastAPI não roda no Cloudflare Workers? O que esse limite te ensina sobre a palavra "serverless"?
2. O Cloudflare Access te deu autenticação sem escrever praticamente nada. **Qual trade-off você aceitou em troca?** Descreva o cenário exato em que essa decisão vira um problema — e o que você faria nesse dia.
3. Cache de borda e cache de aplicação (Fase 12) resolvem problemas diferentes. Explique cada um em uma frase. Depois descreva o que acontece, concretamente, se você cachear `/progress` na borda.
4. Rastreie o caminho de um segredo (ex.: `ANTHROPIC_API_KEY`) da sua máquina até dentro do container. **Em quantos lugares ele existe? Em quantos ele poderia vazar?** Qual é o mais provável?
5. Se o Cloudflare ficar indisponível por 2 horas, o que acontece com o Studyy? E se você quisesse sair do Cloudflare, quanto trabalho seria? **Isso é lock-in aceitável ou não?** Defenda sua resposta com um número, não com uma opinião.

### 📚 Para estudar

- **12-Factor App** (12factor.net) — curto, leia inteiro
- Documentação do **Cloudflare Zero Trust / Access** — comece por "Self-hosted applications"
- "Expand and Contract" / "Parallel Change" (Martin Fowler) — migrations sem downtime
- Docker: multi-stage builds e o que significa "distroless"
- Terraform: `terraform plan` vs `apply`, e o que é state
- *Release It!* (Nygard) — capítulo sobre deploy e "Design for Production"

---
## Fase 11 — Dados: modelagem, índices e busca

**Duração estimada:** 3 a 4 sessões

### 🧠 Conceito em foco: SQL de verdade, índices, e quando NoSQL

#### Índices — o mínimo que você precisa entender

Um índice é uma estrutura (B-tree, normalmente) que evita varrer a tabela inteira. Custo: escrita mais lenta e espaço em disco. Portanto **não indexe tudo**.

**Regra:** indexe o que aparece em `WHERE`, `JOIN` e `ORDER BY` com alta seletividade.

Índices necessários no Studyy:

```sql
CREATE INDEX idx_topics_subject      ON topics (subject_id);
CREATE INDEX idx_notes_topic_created ON notes (topic_id, created_at DESC);
CREATE INDEX idx_entries_plan_date   ON plan_entries (plan_id, scheduled_date);
CREATE INDEX idx_sessions_user_date  ON study_sessions (user_id, started_at DESC);
CREATE UNIQUE INDEX idx_topic_slug   ON topics (subject_id, slug);
```

> 🔑 **Índice composto e a regra do prefixo mais à esquerda:** `(plan_id, scheduled_date)` serve para consultas por `plan_id` e por `plan_id + scheduled_date`, mas **não** para consultas só por `scheduled_date`. A ordem das colunas importa.

**Aprenda a ler `EXPLAIN ANALYZE`.** É a habilidade de banco de dados com melhor retorno sobre investimento que existe. Rode em toda query do dashboard e procure por `Seq Scan` em tabela grande.

#### O problema N+1

O mais comum e mais caro em ORM:

```python
subjects = await session.scalars(select(SubjectModel))
for s in subjects:
    print(len(s.topics))     # 1 query por matéria => N+1
```

Solução: `selectinload()` / `joinedload()`. Detecção: ative `echo=True` no SQLAlchemy em dev e conte as queries. Melhor ainda: escreva um teste que falhe se uma rota disparar mais de X queries.

#### Busca full-text nas anotações (o que prepara o RAG)

Postgres resolve sem Elasticsearch:

```sql
ALTER TABLE notes ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (
    setweight(to_tsvector('portuguese', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('portuguese', coalesce(content, '')), 'B')
  ) STORED;

CREATE INDEX idx_notes_search ON notes USING GIN (search_vector);
```

Isso é **busca léxica** (por palavra). Na Fase 14 você adiciona **busca semântica** (por significado, com embeddings). O melhor RAG usa as duas — chama-se **busca híbrida**.

#### SQL vs NoSQL — a decisão honesta para este projeto

| Aspecto | Avaliação no Studyy |
|---|---|
| Relacionamentos | Muitos (matéria -> tópico -> anotação -> sessão -> XP). **Ponto para SQL.** |
| Transações | Sessão + XP precisam ser consistentes. **Ponto para SQL.** |
| Schema | Estável e conhecido. **Ponto para SQL.** |
| Volume | Um usuário. Irrelevante. |
| Dado semiestruturado | Metadados de anotação variam -> use **`jsonb`** numa coluna, não um banco novo |

**Conclusão: Postgres para tudo.** `jsonb` cobre o caso "documento" e `pgvector` cobre o caso "vetorial". Um banco, três modelos de dado. Adicionar MongoDB aqui seria *resume-driven development*.

> Estude NoSQL na teoria (CAP, BASE, modelos chave-valor/documento/coluna/grafo), mas não force no projeto. **A melhor decisão de arquitetura costuma ser a que você não tomou.**

### 🎯 O que construir

1. Revisar todo o schema e adicionar os índices
2. Rodar `EXPLAIN ANALYZE` em toda query do dashboard; documentar em `docs/queries.md`
3. Eliminar todo N+1 (teste de contagem de queries)
4. Implementar busca full-text nas anotações: `GET /notes/search?q=`
5. Script de seed com volume realista (2 anos de estudo: ~700 sessões, ~2000 anotações) para testar performance de verdade
6. Constraints no banco **além** dos invariantes do domínio (defesa em profundidade): `CHECK (duration_minutes > 0)`, `UNIQUE`, `FOREIGN KEY ... ON DELETE`
7. Estratégia de backup: `pg_dump` agendado + teste de restore

### ✅ Critérios de aceite

- [ ] Nenhuma query do dashboard faz `Seq Scan` em tabela com mais de 1000 linhas
- [ ] Nenhuma rota dispara mais de 5 queries (teste automatizado contando queries)
- [ ] Busca full-text funciona com acento e stemming em português ("derivada" acha "derivadas")
- [ ] Seed com 2 anos de dados; dashboard abre em < 200ms
- [ ] Todo invariante crítico tem também uma constraint no banco
- [ ] Backup testado — **restaurado de verdade**, não só gerado
- [ ] `docs/queries.md` com os planos de execução

### ⚠️ Armadilhas

- **Indexar tudo.** Cada índice desacelera escrita e ocupa disco.
- **Testar performance com 10 registros.** Tudo é rápido com 10 registros. Use o seed.
- **Confiar só no domínio para integridade.** Um script de migração mal feito passa por cima do domínio. Constraint no banco é a última linha de defesa.
- **`ON DELETE CASCADE` sem pensar.** Apagar uma matéria apagar 2 anos de anotações silenciosamente é um desastre. Prefira soft delete.

### 🎓 Checkpoint Socrático — Fase 11

> Responda **por escrito** em `docs/checkpoints/fase-11.md` antes de marcar a fase como concluída.

1. O índice `(plan_id, scheduled_date)`: **escreva uma query que ele acelera e uma que ele não acelera.** Explique a regra que separa as duas.
2. O N+1 é um bug que o ORM torna fácil de cometer. **A culpa é do ORM?** Defenda os dois lados e escolha um.
3. Você decidiu não usar NoSQL. **Que mudança concreta no produto** faria você reconsiderar? Descreva-a como um gatilho verificável, não como "se crescer muito".
4. As constraints no banco repetem invariantes que o domínio já garante. **Isso viola DRY?** Justifique — e diga o que você faria se elas discordassem uma da outra.
5. Replicação e particionamento não se aplicam aqui. **Em que número exato** (usuários? GB? consultas por segundo?) passariam a se aplicar? Escreva esse número no ADR — é ele que transforma "não precisa" em uma decisão de arquitetura, e não em preguiça.

### 📚 Para estudar

- *Use The Index, Luke!* (use-the-index-luke.com) — gratuito, é **o** recurso sobre índices
- `EXPLAIN ANALYZE` na documentação do Postgres
- *Designing Data-Intensive Applications* (Kleppmann), capítulo 3 — como índices funcionam por dentro
- Postgres full-text search: `tsvector`, `tsquery`, `GIN` vs `GiST`

---

## Fase 12 — Assincronia, filas e cache

**Duração estimada:** 4 a 5 sessões

### 🧠 Conceito em foco: sistemas distribuídos começam aqui

Você não vai fazer microsserviços, mas vai enfrentar os **problemas** de sistemas distribuídos assim que sair do processo único: mensagem perdida, mensagem duplicada, ordem de chegada, consistência eventual.

#### Por que precisamos de trabalho assíncrono

| Trabalho | Por que não pode ser síncrono |
|---|---|
| Gerar flashcards com IA (Fase 14) | 10–30 segundos. HTTP não espera. |
| Gerar embeddings das anotações | Custa dinheiro e tempo, e não é urgente |
| Verificar quebra de streak à meia-noite | Ninguém dispara — é agendado |
| Enviar lembrete "você tem 45min hoje" | Agendado |
| Exportar todas as anotações em PDF | Demora |

#### Outbox Pattern ⭐ (resolvendo a dívida da Fase 7)

**O problema:** salvar no banco e publicar na fila são dois sistemas. Não existe transação entre eles.

```
commit no banco  ✅
                     <- processo morre aqui
publish na fila  ❌      => evento perdido para sempre
```

**A solução:** grave o evento **no mesmo banco, na mesma transação**, numa tabela `outbox`. Um processo separado lê a tabela e publica.

```
┌─ TRANSAÇÃO ────────────────────┐
│  INSERT INTO study_sessions    │
│  INSERT INTO outbox (event)    │   <- atômico. ou os dois, ou nenhum.
└────────────────────────────────┘
              │
              v
     [Relay: lê outbox -> publica -> marca como publicado]
              │
              v
         [Fila / Handlers]
```

Isso garante **at-least-once delivery**: nenhum evento se perde, mas algum pode chegar duas vezes. Por isso:

#### Idempotência

> Processar a mesma mensagem N vezes tem o mesmo efeito de processar 1 vez.

Implementação simples: tabela `processed_events (event_id PK, handler_name, processed_at)`. Antes de processar, tenta inserir; se violar a PK, já foi processado -> ignora.

**Você já preparou isso na Fase 8.** Agora usa de verdade.

#### Cache com Redis

**Antes de cachear, meça.** Cache prematuro adiciona uma classe inteira de bugs (invalidação) para resolver um problema que talvez não exista.

Candidatos legítimos no Studyy:

| Dado | TTL | Invalidação |
|---|---|---|
| Heatmap anual | 1h | Ao concluir sessão |
| Distribuição por matéria | 1h | Ao concluir sessão |
| Catálogo de badges | 24h | Deploy |
| Resumo de progresso | 5min | Ao ganhar XP |

**Padrão: cache-aside**

```python
async def get_heatmap(user_id: UserId) -> Heatmap:
    if cached := await cache.get(f"heatmap:{user_id}"):
        return Heatmap.parse(cached)
    result = await repo.compute_heatmap(user_id)
    await cache.set(f"heatmap:{user_id}", result.serialize(), ttl=3600)
    return result
```

> 🔑 **O cache é implementado como um Decorator sobre o read model.** O use case não sabe que existe cache — ele depende do Port. Trocar Redis por memória, ou desligar o cache, é trocar o adaptador no `composition_root`. **Isso só é possível porque você fez a Fase 5.**

#### As duas coisas difíceis

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

Estratégias de invalidação, da mais simples à mais correta:
1. **TTL curto** — aceita dado velho por N segundos. Simples. Comece aqui.
2. **Invalidação por evento** — `StudySessionCompleted` apaga as chaves afetadas. Correto, mais trabalho.
3. **Write-through** — atualiza cache e banco juntos. Complexo.

### 🎯 O que construir

1. **Worker com ARQ** (mais simples que Celery e async-native; Dramatiq é boa alternativa)
2. **Tabela e relay do outbox**
3. **Migrar os handlers** de in-process para a fila (mantendo o Port `EventPublisher` — o use case não muda **nada**. Esta é a recompensa da Fase 5.)
4. **Idempotência** com `processed_events`
5. **Redis + cache-aside** nos read models de dashboard (como Decorator)
6. **Jobs agendados:**
   - Meia-noite (timezone do usuário): verificar quebra de streak -> `StreakBroken`
   - Manhã: lembrete da agenda do dia
   - Semanal: relatório "sua semana em números"
7. **Dead Letter Queue**: mensagem que falha 3 vezes vai para inspeção manual, não fica em loop
8. **Retry com backoff exponencial + jitter**

### 🔧 Patterns aplicados

| Pattern | Onde |
|---|---|
| **Transactional Outbox** | Garantia de entrega |
| **Idempotent Consumer** | `processed_events` |
| **Decorator** | Cache sobre read model |
| **Cache-Aside** | Estratégia de leitura |
| **Dead Letter Queue** | Mensagens venenosas |
| **Retry com backoff** | Falhas transitórias |

### ✅ Critérios de aceite

- [ ] Matar o worker no meio do processamento **não perde nenhum evento** (teste de verdade: `docker kill` no worker)
- [ ] Reprocessar a mesma mensagem não duplica XP
- [ ] Dashboard com cache responde em < 50ms; sem cache, < 200ms
- [ ] Invalidação funciona: concluir sessão atualiza o heatmap imediatamente
- [ ] Job de streak roda no timezone correto do usuário
- [ ] Mensagem que falha 3x vai para a DLQ e é inspecionável
- [ ] **Nenhum use case mudou** ao migrar de in-process para fila (prove com `git diff`)

### ⚠️ Armadilhas

- **Publicar direto na fila sem outbox.** Você vai perder eventos, e o bug será intermitente e impossível de reproduzir.
- **Assumir ordem de entrega.** Filas não garantem ordem global. Projete handlers que não dependem dela, ou use chave de particionamento.
- **Cache sem estratégia de invalidação.** Você vai passar uma tarde depurando XP que "não atualiza" — e era o cache.
- **Retry infinito.** Mensagem envenenada em loop consome o worker inteiro. Sempre limite + DLQ.
- **Colocar fila onde não precisa.** Se leva 50ms e o usuário precisa do resultado, faça síncrono.

### 🎓 Checkpoint Socrático — Fase 12

> Responda **por escrito** em `docs/checkpoints/fase-12.md` antes de marcar a fase como concluída.

1. **Desenhe a linha do tempo da falha** que o Outbox resolve — passo a passo, marcando o instante exato em que o processo morre e o que se perde.
2. *Exactly-once* é praticamente impossível de garantir. **Por quê?** E qual é a combinação de duas coisas que você usa no lugar para obter o mesmo efeito prático?
3. Nenhum use case mudou ao migrar de in-process para fila. **Qual decisão, de qual fase, pagou por isso?** Seja específico: nomeie o arquivo.
4. Você mediu antes de cachear? **Qual era o número e qual ficou?** Se não mediu, o cache foi fé, não engenharia — volte e meça.
5. Invalidação por TTL é mais simples que por evento. **Em quais dos seus read models o TTL é honestamente suficiente**, e em quais não é? Qual propriedade do dado decide isso?

### 📚 Para estudar

- "Transactional Outbox Pattern" (microservices.io)
- *Designing Data-Intensive Applications* — capítulo 11 (Stream Processing)
- "Exponential Backoff And Jitter" (AWS Architecture Blog)
- Documentação do ARQ
- Teorema CAP e consistência eventual

---

## Fase 13 — Observabilidade e resiliência

**Duração estimada:** 3 a 4 sessões

### 🧠 Conceito em foco: você não pode consertar o que não consegue ver

#### Os três pilares

| Pilar | O que responde | Ferramenta |
|---|---|---|
| **Logs** | "O que aconteceu neste evento específico?" | `structlog` -> JSON |
| **Métricas** | "Como o sistema está se comportando no agregado?" | Prometheus |
| **Traces** | "Por onde passou esta requisição e onde demorou?" | OpenTelemetry -> Jaeger |

#### Logs estruturados

```python
# ❌ Não dá para consultar
logger.info(f"Sessão {session_id} concluída com {minutes} minutos")

# ✅ Consultável, agregável, filtrável
logger.info("study_session.completed",
            session_id=str(session_id), topic_id=str(topic_id),
            focused_minutes=minutes, planned_minutes=planned,
            completion_rate=minutes / planned)
```

**Correlation ID:** middleware gera um `request_id`, coloca num `ContextVar`, e **todo** log da requisição o carrega — incluindo os do worker, se você propagar na mensagem. Sem isso, depurar fluxo assíncrono é impossível.

#### Métricas que importam no Studyy

**Técnicas (RED):** Rate, Errors, Duration por endpoint; tamanho da fila; taxa de acerto do cache.
**De negócio:** sessões iniciadas vs concluídas (taxa de abandono!), minutos focados/dia, anotações criadas/semana.

> As métricas de negócio são as que **te ajudam a estudar melhor**. "Taxa de abandono por horário do dia" pode te revelar que você não rende depois das 22h — informação que muda seu planejamento real.

#### Resiliência

| Pattern | Problema | Onde no Studyy |
|---|---|---|
| **Timeout** | Chamada que nunca volta | Toda chamada a LLM (Fase 14) |
| **Retry + backoff** | Falha transitória | Rede, LLM com rate limit |
| **Circuit Breaker** | Serviço caído sendo martelado | Provedor de LLM indisponível |
| **Bulkhead** | Uma falha consumindo todos os recursos | Pool separado para chamadas de IA |
| **Graceful degradation** | Funcionalidade opcional fora do ar | Sem IA, o app de anotações continua 100% |

**Circuit Breaker em uma frase:** depois de N falhas, pare de tentar por T segundos (circuito *aberto*), depois deixe uma requisição passar para testar (*meio-aberto*); se funcionar, volta ao normal (*fechado*).

### 🎯 O que construir

1. `structlog` com saída JSON; middleware de `request_id`
2. Propagar o `request_id` para as mensagens do worker
3. OpenTelemetry instrumentando FastAPI, SQLAlchemy e Redis; Jaeger no compose
4. Métricas Prometheus em `/metrics`; dashboard Grafana com as métricas de negócio
5. Healthchecks: `/health/live` (o processo está vivo) e `/health/ready` (dependências ok)
6. Timeout em toda chamada externa
7. Circuit breaker (`purgatory` ou implementação própria) para o futuro adaptador de LLM
8. `docs/runbook.md`: o que fazer quando cada alerta disparar

### 🔬 Exercício opcional: extrair um serviço

Se quiser *sentir* microsserviços sem se comprometer: extraia `progression` para um processo separado, comunicando só por fila.

Você vai enfrentar, na ordem: contrato de evento versionado, consistência eventual visível na UI, dois deploys, trace distribuído, e "o serviço B está fora, e agora?".

**Depois, reverta.** O aprendizado é o entregável — e a conclusão provavelmente será "o monólito modular estava certo". Escreva isso num ADR; é uma das lições mais valiosas que você pode registrar.

### ✅ Critérios de aceite

- [ ] Todo log é JSON com `request_id`
- [ ] Um trace mostra HTTP -> use case -> repositório -> SQL, com tempos
- [ ] Trace atravessa a fila (requisição -> worker no mesmo trace)
- [ ] Grafana com taxa de abandono de sessão
- [ ] Dependência externa fora do ar não derruba o app (degrada)
- [ ] Circuit breaker testado com um adaptador falso que sempre falha
- [ ] Runbook escrito

### ⚠️ Armadilhas

- **Logar dado sensível.** Nunca logue conteúdo integral de anotações nem tokens.
- **Log em nível errado.** `INFO` para fluxo normal, `WARNING` para recuperável, `ERROR` para o que exige ação. Se tudo é `ERROR`, nada é.
- **Métrica com alta cardinalidade.** `note_id` como label do Prometheus explode a memória. Labels são dimensões de baixa cardinalidade.
- **Observabilidade depois do incidente.** Instrumentar depois que quebrou é tarde.

### 🎓 Checkpoint Socrático — Fase 13

> Responda **por escrito** em `docs/checkpoints/fase-13.md` antes de marcar a fase como concluída.

1. Log, métrica e trace respondem perguntas diferentes. **Formule uma pergunta real sobre o Studyy para cada um** — perguntas que os outros dois não conseguiriam responder.
2. Por que usar `note_id` como label do Prometheus quebraria o sistema? **Explique o mecanismo**, não só a regra.
3. Circuit breaker: **por que parar de tentar é melhor do que continuar tentando?** Descreva o que acontece com a sua origem sem ele, quando o provedor de LLM fica lento (não fora do ar — lento).
4. Se você fez o exercício de extrair `progression` para um serviço separado: **o que doeu?** Liste na ordem em que doeu. Escreva o ADR da reversão.
5. Qual métrica de negócio do Studyy **mudou a forma como você de fato estuda?** Se nenhuma mudou, sua instrumentação está medindo o sistema e não o usuário — que métrica faltou?

### 📚 Para estudar

- *Observability Engineering* (Majors, Fong-Jones, Miranda) — capítulos 1 a 5
- *Release It!* (Michael Nygard) — **a** referência de patterns de resiliência
- OpenTelemetry: conceitos de trace, span e context propagation
- Google SRE Book, capítulo 6 ("Monitoring Distributed Systems") — os 4 sinais dourados

---

## Fase 14 — Base para o Assistente de IA (RAG)

**Duração estimada:** 6 a 10 sessões

### 🧠 Conceito em foco: Anti-Corruption Layer e integração com sistemas externos

Um provedor de LLM é o exemplo perfeito de dependência externa volátil: a API muda, o modelo é depreciado, o preço muda, você troca de fornecedor. Se `OpenAI` ou `Anthropic` aparecerem espalhados pelos seus use cases, você está refém.

**Anti-Corruption Layer (ACL):** uma camada de tradução que impede que o modelo do sistema externo contamine o seu domínio.

```python
# assistant/domain/ports.py — seu vocabulário, não o do fornecedor
class LlmProvider(Protocol):
    async def complete(self, prompt: Prompt, ctx: LlmContext) -> LlmAnswer: ...

class EmbeddingProvider(Protocol):
    async def embed(self, chunks: list[str]) -> list[Embedding]: ...

# assistant/infrastructure/llm/ — os adaptadores
class AnthropicLlmProvider: ...
class OpenAiLlmProvider: ...
class FakeLlmProvider: ...     # testes determinísticos, custo zero
```

Trocar de fornecedor = escrever um adaptador. Testar = usar o fake. **Nenhum use case muda.**

### 🎯 Como funciona o RAG (visão geral)

```
  INGESTÃO (offline, assíncrona)
  ─────────────────────────────
  Anotação -> Chunking -> Embedding -> Armazenar vetor + metadados
                                            (pgvector)

  CONSULTA (online)
  ─────────────────
  Pergunta -> Embedding -> Busca por similaridade ─┐
                                                   ├-> Re-rank -> Prompt + contexto -> LLM -> Resposta
           -> Busca full-text (Fase 11) ───────────┘                                          + citações
```

#### As decisões que determinam a qualidade

**1. Chunking — a decisão mais subestimada**

Chunk grande demais dilui o significado; pequeno demais perde o contexto.

| Estratégia | Quando |
|---|---|
| Tamanho fixo + overlap | Baseline simples (~500 tokens, 50 de overlap) |
| **Por estrutura do Markdown** | ✅ **Melhor para o Studyy** — quebre por `##`, mantendo o cabeçalho em cada chunk |
| Semântico | Quebra onde o assunto muda. Melhor qualidade, mais caro |

Como suas anotações são Markdown com hierarquia, **use a estrutura**. E enriqueça cada chunk com o caminho: `"Cálculo I > Derivadas > Regra da Cadeia"` no início do texto do chunk. Isso melhora drasticamente o retrieval.

**2. Metadados** — grave `subject_id`, `topic_id`, `note_id`, `created_at`, `heading_path`. Permite filtrar ("só responda com base em Cálculo I") e **citar a fonte**.

**3. Busca híbrida** — combine similaridade vetorial (semântica) com full-text (léxica) usando *Reciprocal Rank Fusion*. Quase sempre supera qualquer uma isolada, especialmente com termos técnicos e fórmulas.

**4. Citações sempre.** Toda resposta do tutor cita as anotações usadas, com link. Sem isso, você não consegue distinguir conhecimento seu de alucinação do modelo — o que é fatal numa ferramenta de estudo.

### 🎯 O que construir

#### 14.1 — Bounded Context `assistant`

```
assistant/
├── domain/
│   ├── document_chunk.py
│   ├── retrieval_query.py
│   ├── flashcard.py          # Card, Deck, ReviewSchedule
│   ├── quiz.py               # Question, Alternative, Attempt
│   ├── mind_map.py           # Node, Edge
│   └── ports.py              # LlmProvider, EmbeddingProvider, VectorStore
├── application/
│   ├── ingest_note.py
│   ├── ask_tutor.py
│   ├── generate_flashcards.py
│   ├── generate_quiz.py
│   └── generate_mind_map.py
└── infrastructure/
    ├── llm/           anthropic.py, openai.py, fake.py
    ├── embeddings/
    ├── vector/        pgvector_store.py
    └── chunking/      markdown_chunker.py
```

#### 14.2 — Pipeline de ingestão (assíncrono, via Fase 12)

`NoteCreated` / `NoteUpdated` -> job -> chunk -> embed -> upsert no pgvector.
Reingestão idempotente: chunks de uma nota são substituídos, não acumulados.

#### 14.3 — Tutor

```
POST /assistant/ask   { question, subject_id?, topic_id? }
->  { answer, sources: [{ note_id, title, excerpt, score }] }
```

Com streaming (SSE) para a resposta aparecer progressivamente.

#### 14.4 — Flashcards (estilo Anki)

- Geração a partir de um tópico: o LLM produz pares pergunta/resposta a partir dos chunks
- **Você revisa antes de aceitar** (o LLM erra; cartão errado memorizado é pior que nenhum cartão)
- **Repetição espaçada:** implemente **FSRS** (mais moderno e eficaz) ou SM-2 (o do Anki clássico)
- O algoritmo de agendamento é um **Strategy** — assim você pode trocar SM-2 por FSRS sem reescrever nada
- Sessão de revisão gera eventos -> **alimenta a gamificação da Fase 8 de graça** ✨

#### 14.5 — Simulados

- Geração de questões (múltipla escolha e discursivas) por tópico ou matéria
- Correção automática com citação do trecho da anotação que fundamenta
- Resultado gera evento -> XP e badges
- **Identificação de lacunas:** tópicos com baixo acerto voltam para o roadmap da Fase 6 com prioridade. **Este é o fecho do ciclo do produto inteiro:** estuda -> anota -> é testado -> erra -> é reagendado.

#### 14.6 — Mapas mentais

- Geração de estrutura hierárquica (JSON: nós e arestas) a partir dos tópicos e anotações
- Renderização com React Flow ou Markmap
- Edição manual persistida (o mapa é seu; a IA só dá o rascunho)

#### 14.7 — Controle de custo

- Contabilize tokens por chamada; exponha em métrica (Fase 13)
- Cache de embeddings: não reembeddar chunk cujo conteúdo não mudou (hash do conteúdo como chave)
- Limite diário configurável
- `FakeLlmProvider` em **todos** os testes — suíte de testes não pode custar dinheiro

### 🔧 Patterns aplicados

| Pattern | Onde |
|---|---|
| **Anti-Corruption Layer** | Todo o `infrastructure/llm/` |
| **Strategy** | Chunking, algoritmo de repetição espaçada, provedor de LLM |
| **Pipeline** | Ingestão: chunk -> embed -> store |
| **Adapter** | pgvector como implementação de `VectorStore` |
| **Circuit Breaker + Retry** | Chamadas ao LLM (Fase 13) |
| **Template Method** | Estrutura comum dos geradores (flashcard, quiz, mapa) |

### ✅ Critérios de aceite

- [ ] Nenhum use case importa SDK de fornecedor de LLM
- [ ] Toda a suíte de testes roda com `FakeLlmProvider`, custo zero
- [ ] Trocar de provedor é trocar uma linha no `composition_root.py`
- [ ] Criar anotação dispara ingestão assíncrona automaticamente
- [ ] Editar anotação reingere sem duplicar chunks
- [ ] Toda resposta do tutor cita as anotações fonte, com link clicável
- [ ] Busca híbrida implementada e comparada com vetorial pura (documente qual ganhou, com exemplos)
- [ ] Flashcards revisáveis antes de entrar no deck
- [ ] Repetição espaçada agenda corretamente (teste com `FrozenClock`)
- [ ] Simulado gera evento que credita XP
- [ ] Tópico com baixo desempenho é sugerido de volta no roadmap
- [ ] Custo por chamada é medido e visível no Grafana
- [ ] **ADR-007** escrito

### ⚠️ Armadilhas

- **Chunking ingênuo.** Cortar no meio de uma fórmula ou de um bloco de código destrói o significado. Respeite a estrutura do Markdown.
- **Sem citação.** Você não consegue distinguir sua anotação de alucinação. Inaceitável numa ferramenta de estudo.
- **Ingestão síncrona no POST da anotação.** Salvar uma anotação passa a levar 5 segundos. Use a fila.
- **Vector DB dedicado no dia 1.** `pgvector` aguenta centenas de milhares de vetores. Você tem um usuário. Um banco a menos para operar.
- **Reembeddar tudo a cada edição.** Hash do conteúdo por chunk; só reembedda o que mudou.
- **Aceitar flashcards sem revisar.** Memorizar informação errada é pior que não memorizar.
- **Testes que chamam a API real.** Lentos, instáveis e caros. Sempre o fake.

### 🎓 Checkpoint Socrático — Fase 14

> Responda **por escrito** em `docs/checkpoints/fase-14.md` antes de marcar a fase como concluída.

1. Chunking por estrutura vs tamanho fixo. **Pegue uma anotação sua de verdade** e mostre o trecho exato onde as duas estratégias produzem resultados diferentes. Qual recuperou melhor?
2. Sem citação, você não distingue sua anotação de uma alucinação. **Por que isso é pior numa ferramenta de estudo do que num chatbot genérico?** Pense no que acontece com o conhecimento errado depois que você o memoriza.
3. Quanto custaria trocar de provedor de LLM hoje? **Responda em número de arquivos alterados.** Se for mais que 2, seu ACL vazou — onde?
4. A busca híbrida ganhou da vetorial pura? **Mostre a consulta específica** onde a diferença apareceu, com os resultados dos dois lados. Se não encontrou nenhuma, a busca híbrida está se pagando?
5. Imagine um agente que lê seu progresso e **remarca seu roadmap sozinho**. Que ferramentas (tools) ele precisaria? **Quantas delas já existem como use case** nas fases 6 e 8? O que essa resposta te diz sobre o valor de ter feito a Fase 5 direito?

### 📚 Para estudar

- "Retrieval-Augmented Generation" — o paper original (Lewis et al., 2020)
- Documentação do `pgvector`: índices HNSW vs IVFFlat
- Reciprocal Rank Fusion para busca híbrida
- Algoritmo FSRS (repositório open-source) e SM-2
- "Anti-Corruption Layer" (Eric Evans, *DDD*, capítulo 14)

---
# PARTE III — REFERÊNCIA

---

## Mapa: trilha teórica ↔ fase do projeto

| Tema que você quer estudar | Fase onde é aplicado | Como aparece no Studyy |
|---|---|---|
| **Coesão e acoplamento** | 1, 2 | Sentir a dor no monólito ingênuo e resolver com camadas |
| **SOLID** | 3 | Uma refatoração por princípio, com commit próprio |
| **Modularidade** | 4, 5 | Bounded contexts com fronteira verificada por import-linter |
| **Design Patterns (GoF)** | 3, 6, 8, 12, 14 | Strategy, State, Factory, Decorator, Observer, Adapter, Template Method |
| **DDD tático** | 4 | Entidades, VOs, agregados, invariantes, domain services |
| **DDD estratégico** | 3, 4 | Linguagem ubíqua, bounded contexts, ACL, shared kernel |
| **Clean Architecture** | 5 | Use cases, regra de dependência, composition root |
| **Arquitetura Hexagonal** | 5 | Ports & adapters, fakes substituindo infra inteira |
| **Event-Driven Design** | 7, 12 | Domain events in-process; depois promovidos a fila |
| **Monólito vs camadas vs microsserviços** | 0 (ADR-003), 13 (exercício) | Monólito modular, com exercício opcional de extração |
| **APIs** | 2, 6, 9 | REST, versionamento, contratos tipados via OpenAPI |
| **Infraestrutura e deploy** | 10 | Cloudflare, containers, IaC, CI/CD, ambientes |
| **CDN e edge** | 10 | Cloudflare Pages + cache de borda, com medição antes/depois |
| **Load balancing** | 10 (conceito), 13 (teoria) | Cloudflare como proxy reverso; LB real fica na teoria |
| **Segurança de borda** | 10 | WAF, rate limiting, DDoS, TLS, Zero Trust Access |
| **Filas** | 12 | ARQ, outbox, DLQ, idempotência |
| **Cache** | 10, 12 | Cache de borda (Cloudflare) e cache de aplicação (Redis) |
| **Consistência** | 7, 12 | Consistência eventual entre execução e progressão |
| **SQL / índices** | 11 | `EXPLAIN ANALYZE`, índices compostos, N+1, full-text |
| **Modelagem de dados** | 4, 11 | Modelo de domínio vs modelo relacional, mapeamento, migrations |
| **NoSQL** | 11 (decisão), 14 (vetorial) | `jsonb` e `pgvector` no Postgres, com o porquê registrado |
| **Replicação / particionamento** | 11 (teoria + ADR) | Não aplicável a 1 usuário; exercício é justificar a não-decisão |
| **Observabilidade** | 13 | Logs estruturados, traces OTel, métricas de negócio |
| **Resiliência** | 13 | Timeout, retry, circuit breaker, degradação graciosa |
| **RAG** | 14 | Chunking, embeddings, busca híbrida, citações |
| **Agentes de IA** | 14 + backlog | Tool use, orquestração, avaliação de qualidade |

> 📌 **Sobre os temas que continuam "fora de escopo":** replicação, particionamento e load balancing real não têm como ser aplicados honestamente num sistema de um usuário. Forçá-los seria teatro de arquitetura. Estude-os na teoria (DDIA é o livro) e — este é o exercício real — **escreva um ADR explicando por que não os aplicou, e qual métrica faria você mudar de ideia.** Saber justificar uma não-decisão, com o gatilho que a reverteria, é uma habilidade de arquiteto mais rara do que saber aplicar o padrão.

---

## Catálogo de Design Patterns usados no projeto

| Pattern | Categoria | Fase | Onde exatamente |
|---|---|---|---|
| Repository | Arquitetural | 2 | Acesso a dados de todos os agregados |
| DTO | Arquitetural | 2 | Contratos de entrada e saída da API |
| Dependency Injection | Arquitetural | 2, 5 | `Depends()` e `composition_root.py` |
| Strategy | Comportamental | 3, 6, 8, 14 | Export, quebra de ciclos, política de XP, chunking |
| Registry | Criacional | 3, 8 | Exportadores, catálogo de badges |
| Protocol / Port | Estrutural | 3, 5 | Todas as interfaces de saída |
| Value Object | DDD | 4 | `Duration`, `StudyDate`, todos os IDs |
| Aggregate Root | DDD | 4 | `Subject`, `StudyPlan`, `StudySession`, `LearnerProgress` |
| Factory Method | Criacional | 4, 6 | `StudySession.start_from()`, `Note.create()` |
| Data Mapper | Arquitetural | 4 | `mappers.py` em cada módulo |
| Domain Service | DDD | 4 | `StudyPlanScheduler` |
| Use Case / Interactor | Arquitetural | 5 | Um arquivo por operação |
| Command | Comportamental | 5 | Entrada de cada use case |
| Unit of Work | Arquitetural | 5 | Controle transacional |
| Facade | Estrutural | 5 | `composition_root.py` |
| Null Object | Comportamental | 5, 7 | `NullEventPublisher` |
| State | Comportamental | 6 | Máquina de estados da sessão |
| Specification | Comportamental | 6, 8 | Agendamento e regras de badge |
| Snapshot | Integração | 6 | `PlanEntrySnapshot` entre contextos |
| Domain Event | DDD | 7 | Catálogo em `docs/eventos.md` |
| Observer / Pub-Sub | Comportamental | 7 | `InMemoryEventBus` |
| Mediator | Comportamental | 7 | Barramento de eventos |
| Read Model / CQRS-lite | Arquitetural | 8 | Queries de dashboard |
| Reverse Proxy / Gateway | Infraestrutural | 10 | Cloudflare na frente da origem |
| Edge Cache | Infraestrutural | 10 | Cache de borda para assets e read models públicos |
| Blue-Green / Preview Deploy | Infraestrutural | 10 | Cloudflare Pages preview por branch |
| Transactional Outbox | Integração | 12 | Entrega garantida |
| Idempotent Consumer | Integração | 12 | `processed_events` |
| Decorator | Estrutural | 12 | Cache sobre read models |
| Cache-Aside | Arquitetural | 12 | Leitura com Redis |
| Dead Letter Queue | Integração | 12 | Mensagens venenosas |
| Circuit Breaker | Resiliência | 13 | Chamadas a LLM |
| Retry com Backoff | Resiliência | 13 | Falhas transitórias |
| Bulkhead | Resiliência | 13 | Isolamento de pool |
| Anti-Corruption Layer | DDD | 14 | Adaptadores de LLM |
| Pipeline | Arquitetural | 14 | Ingestão RAG |
| Template Method | Comportamental | 14 | Geradores de conteúdo IA |

---

## Definition of Done (vale para toda fase)

Uma fase só está concluída quando **todos** estes itens são verdadeiros:

- [ ] Todos os critérios de aceite específicos da fase estão marcados
- [ ] **O Checkpoint Socrático da fase foi respondido por escrito** em `docs/checkpoints/fase-N.md`
- [ ] `ruff check` + `ruff format --check` passam
- [ ] `mypy --strict` passa sem `# type: ignore` novo
- [ ] `lint-imports` passa (a partir da Fase 5)
- [ ] `pytest` passa; cobertura do diretório `domain/` acima de 90%
- [ ] CI verde
- [ ] ADR escrito, se houve decisão de arquitetura
- [ ] `README.md` atualizado se a forma de rodar mudou
- [ ] Commits seguem Conventional Commits, separando refatoração de feature
- [ ] Tag no git: `git tag fase-N-concluida`
- [ ] **Você consegue explicar o conceito da fase em voz alta, sem olhar o código.** Se não consegue, você copiou em vez de aprender — e a Fase 5 vai desmoronar sobre a Fase 4 mal feita.

---

## Ordem recomendada, com marcos

```
Fase 0  ▸ Fundação                     [1-2 sessões]
Fase 1  ▸ Monólito ingênuo             [1 sessão]      🏁 MARCO: você tem dor documentada
Fase 2  ▸ Camadas                      [2-3 sessões]
Fase 3  ▸ SOLID                        [3-4 sessões]
Fase 4  ▸ DDD tático                   [4-6 sessões]   🏁 MARCO: domínio testável sem banco
Fase 5  ▸ Clean/Hexagonal              [4-5 sessões]   🏁 MARCO: arquitetura verificada por CI
─────────────────────────────────────────────────────  ⭐ FIM DA TRILHA DE ARQUITETURA BASE
Fase 6  ▸ Roadmap + Pomodoro           [5-7 sessões]   🏁 MARCO: o produto existe
Fase 7  ▸ Event-Driven                 [3-4 sessões]
Fase 8  ▸ Gamificação                  [3-5 sessões]   🏁 MARCO: MVP completo no backend
Fase 9  ▸ Frontend                     [6-10 sessões]
Fase 10 ▸ Infraestrutura e Deploy      [3-5 sessões]   🏁 MARCO: NO AR, DÁ PRA USAR ✨
─────────────────────────────────────────────────────  ⭐ AQUI VOCÊ COMEÇA A USAR NOS ESTUDOS
Fase 11 ▸ Dados e índices              [3-4 sessões]
Fase 12 ▸ Filas e cache                [4-5 sessões]
Fase 13 ▸ Observabilidade              [3-4 sessões]   🏁 MARCO: sistema operável
Fase 14 ▸ RAG e IA                     [6-10 sessões]  🏁 MARCO: o professor particular ✨
```

> 💡 **Se o tempo apertar:** as fases 0 a 10 são o caminho crítico para ter algo utilizável de verdade, no ar, no seu domínio. As fases 11 a 13 são melhorias de engenharia que você pode entremear com a 14. Mas **não pule 1 a 5** — elas são a fundação, e cada uma que você pular vai cobrar juros nas fases seguintes.

---

## Backlog futuro (fora do escopo das 14 fases)

Ideias para depois. **Não comece nenhuma antes da Fase 10.**

- **Agentes de IA com tool use** — um agente que lê seu progresso, identifica lacunas e **remarca seu roadmap sozinho**, usando as APIs das fases 6 e 8 como ferramentas. É a evolução natural do RAG da Fase 14 e merece um roadmap próprio.
- **Revisão espaçada integrada ao roadmap** — tópico estudado volta automaticamente ao calendário em D+1, D+3, D+7, D+21
- **Importação** de PDF de slides, transcrição de aula gravada (Whisper), foto de quadro branco (OCR)
- **Modo offline (PWA)** com sincronização e resolução de conflitos (CRDT ou last-write-wins)
- **Grafo de conhecimento** — links `[[wiki-style]]` entre anotações, visualizados como grafo
- **Multiusuário e autenticação própria** — só se você abrir para outras pessoas; enquanto for pessoal, o Cloudflare Access da Fase 10 resolve
- **App mobile** (React Native ou PWA) para consultar a agenda e iniciar o Pomodoro
- **Integração com calendário** (Google Calendar / CalDAV) para bloquear os horários de estudo
- **Relatórios** semanal e mensal em PDF
- **Modo colaborativo** — compartilhar decks de flashcards e roadmaps

---

## Estante de referência

### Livros — ordem de leitura sugerida

1. **Architecture Patterns with Python** — Percival & Gregory · *gratuito em cosmicpython.com*
   ↳ Fases 2, 4, 5, 7. **Comece por este.** É literalmente este roadmap em forma de livro, na sua stack.
2. **Domain-Driven Design Distilled** — Vaughn Vernon
   ↳ Fase 4. Curto, direto, a melhor porta de entrada para DDD.
3. **Clean Architecture** — Robert C. Martin
   ↳ Fases 3 e 5. Partes III (SOLID) e V (arquitetura).
4. **Implementing Domain-Driven Design** — Vaughn Vernon
   ↳ Fase 4, aprofundamento. Capítulo 10 (agregados) é o essencial.
5. **Designing Data-Intensive Applications** — Martin Kleppmann
   ↳ Fases 11 e 12, e toda a teoria de distribuídos. O livro mais denso da lista.
6. **Release It!** — Michael Nygard
   ↳ Fase 13. Patterns de resiliência com histórias reais de produção.
7. **Refactoring** (2ª ed.) — Martin Fowler
   ↳ Companheiro de todas as fases de refatoração (2, 3, 4, 5).
8. **Design Patterns** — GoF
   ↳ Referência de consulta. Não leia de capa a capa; consulte quando o roadmap citar um pattern.

### Material gratuito

- **cosmicpython.com** — Architecture Patterns with Python, completo e online
- **use-the-index-luke.com** — índices de banco de dados
- **martinfowler.com** — bliki: Aggregate, Domain Event, CQRS, Repository, Specification
- **microservices.io** — catálogo de patterns (Outbox, Saga, API Gateway)
- **refactoring.guru** — design patterns com exemplos em Python
- **Effective Aggregate Design** (Vaughn Vernon) — 3 PDFs gratuitos, essenciais para a Fase 4
- **developers.cloudflare.com** — documentação do Cloudflare, para a Fase 10

---

## Registro de progresso

Marque conforme avança. Anote a data — é seu próprio heatmap antes do app existir.

| Fase | Status | Início | Fim | ADR | Checkpoint | Notas |
|---|---|---|---|---|---|---|
| 0 — Fundação | ⬜ | | | 001,002,003 | ⬜ | |
| 1 — Monólito ingênuo | ⬜ | | | | ⬜ | |
| 2 — Camadas | ⬜ | | | | ⬜ | |
| 3 — SOLID | ⬜ | | | | ⬜ | |
| 4 — DDD tático | ⬜ | | | | ⬜ | |
| 5 — Clean/Hexagonal | ⬜ | | | 004 | ⬜ | |
| 6 — Roadmap + Pomodoro | ⬜ | | | | ⬜ | |
| 7 — Event-Driven | ⬜ | | | 005 | ⬜ | |
| 8 — Gamificação | ⬜ | | | | ⬜ | |
| 9 — Frontend | ⬜ | | | 006 | ⬜ | |
| 10 — Infra e Deploy | ⬜ | | | 008,009 | ⬜ | |
| 11 — Dados | ⬜ | | | 010 | ⬜ | |
| 12 — Filas e cache | ⬜ | | | | ⬜ | |
| 13 — Observabilidade | ⬜ | | | | ⬜ | |
| 14 — RAG | ⬜ | | | 007 | ⬜ | |

Legenda: ⬜ não iniciada · 🟨 em andamento · ✅ concluída

---

## Uma última coisa

O maior risco deste projeto não é técnico. É você passar seis meses construindo arquitetura e nunca usar o app para estudar.

**Por isso as fases 9 e 10 existem onde existem.** Assim que o frontend estiver de pé e no ar, comece a usar o Studyy nos seus estudos reais — mesmo feio, mesmo incompleto. As fases 11 a 14 ficam muito mais fáceis de priorizar quando você é o usuário que está sentindo falta das coisas.

E quando bater a vontade de reescrever tudo porque "agora eu sei fazer melhor": não reescreva. **Refatore.** É exatamente isso que este roadmap inteiro está te ensinando a fazer.
