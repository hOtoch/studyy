# Studyy

Sistema pessoal de estudos: anotacoes por materia/topico, roadmap com agendamento
diario, Pomodoro acoplado ao plano, gamificacao e — no futuro — RAG sobre as
proprias anotacoes.

📍 **Plano completo:** [`ROADMAP.md`](ROADMAP.md) · **Como o Claude me guia:** [`CLAUDE.md`](CLAUDE.md)

**Fase atual:** 0 — Fundação

---

## Rodando local

Pre-requisitos: [uv](https://docs.astral.sh/uv/), Python 3.12+, Docker.

```bash
# 1. dependencias
uv sync --all-groups

# 2. configuracao
cp .env.example .env

# 3. banco (neste ambiente o Docker vive dentro do WSL)
wsl -d Ubuntu -e sudo service docker start
wsl -d Ubuntu --cd "$(pwd)" -e docker compose up -d --wait

# 4. aplicacao
uv run uvicorn studyy.main:create_app --factory --reload
```

Swagger em http://localhost:8000/docs

## Qualidade

Os mesmos quatro comandos que o CI roda, na mesma ordem — o mais rapido falha primeiro:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

Testes marcados como `integration` exigem Postgres de pe. Para rodar so os que nao exigem:

```bash
uv run pytest -m "not integration"
```

## Estrutura

```
src/studyy/
├── config.py      # a unica porta por onde o ambiente entra
├── database.py    # tudo que sabe que existe um banco
└── main.py        # fabrica da app + healthchecks

docs/
├── adr/           # decisoes de arquitetura e o porque delas
└── checkpoints/   # respostas dos Checkpoints Socraticos
```

## Healthchecks

| Rota | Pergunta | Consulta o banco |
|---|---|---|
| `/health/live` | O processo esta vivo? | nao |
| `/health/ready` | Consigo atender agora? | sim |
