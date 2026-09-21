# ADR-002: PostgreSQL como banco principal

- **Status:** aceito
- **Data:** 2026-09-21

## Contexto

O Studyy precisa de um banco desde a Fase 0. A tentação natural, num projeto
pessoal de um usuário só, é usar SQLite: é um arquivo, não precisa de servidor,
não precisa de Docker, funciona em qualquer lugar.

Mas a decisão de banco tem que olhar para onde o projeto vai, não só para onde
ele está:

- **Fase 11** prevê busca full-text nas anotações, com acento e stemming em
  português ("derivada" precisa encontrar "derivadas").
- **Fase 14** prevê busca semântica por embeddings para o RAG.
- Os metadados das anotações são semiestruturados e vão variar com o tempo.
- Há relacionamentos fortes em todo o domínio (matéria → tópico → anotação →
  sessão → XP) e invariantes que exigem transação.

## Decisão

Vamos usar **PostgreSQL 16** em todos os ambientes: container local no
desenvolvimento, service container no CI e Postgres gerenciado em produção a
partir da Fase 10.

Um banco só, cobrindo três modelos de dado: relacional, documento (`jsonb`) e
vetorial (`pgvector`).

## Alternativas consideradas

- **SQLite** — zero configuração, e honestamente suficiente para o volume de um
  usuário. Descartado pelo que falta: o FTS não tem stemming decente para
  português, não existe `jsonb` com índice, e não existe `pgvector`. Migrar na
  Fase 11 ou 14 seria retrabalho garantido, e migração de banco com dados reais
  dentro é das coisas mais caras que existem.

- **MySQL / MariaDB** — perfeitamente capaz do relacional. Descartado por não
  oferecer nenhuma vantagem sobre o Postgres neste caso e perder nos três
  pontos que decidem: full-text, `jsonb` e vetorial.

- **MongoDB** — descartado pelo perfil do domínio. O Studyy é fortemente
  relacional e tem invariantes que precisam de transação (concluir uma sessão e
  creditar XP). O caso "documento" que existe é só metadado variável, e isso o
  `jsonb` resolve dentro do próprio Postgres.

- **Banco vetorial dedicado** (Pinecone, Qdrant, Weaviate) — descartado por
  antecipação. Registrado em detalhe no ADR-007.

## Consequências

- ✅ Um banco só para operar, fazer backup e monitorar.
- ✅ Full-text em português nativo, com `tsvector` e índice GIN, sem
  Elasticsearch.
- ✅ Paridade dev / CI / produção: mesma imagem `postgres:16-alpine` nos três.
  Isso já se provou útil na Fase 0 — o teste de integração do `/health/ready`
  rodou contra um Postgres real no CI.
- ✅ Transações de verdade, que as Fases 7 e 12 vão precisar (Outbox Pattern).

- ❌ Preciso de um Postgres rodando para desenvolver. Nesta máquina isso
  significa subir o daemon do Docker dentro do WSL antes de trabalhar
  (`wsl -d Ubuntu -e sudo service docker start`) — uma fricção diária pequena,
  mas real.
- ❌ Mais peças no `docker-compose`, no CI e, a partir da Fase 10, uma
  dependência externa a mais para pagar e manter.

- 🔄 **Gatilho de reversão:** nenhum realista para o banco principal — as
  Fases 11 e 14 dependem de recursos que só o Postgres dá.

  O SQLite pode voltar, mas em outro papel, não como substituto: se eu for
  implementar o **modo offline** do backlog, ele seria o banco *local* do
  cliente, sincronizando com o Postgres. Nesse caso passariam a existir dois
  bancos com propósitos diferentes, e isso exigiria um ADR novo tratando de
  sincronização e resolução de conflito.
