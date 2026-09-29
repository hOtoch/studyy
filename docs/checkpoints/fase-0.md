# Checkpoint Socrático — Fase 0

> ⚠️ **Estas respostas foram escritas pelo Claude, não pelo Hugo.** Decisão tomada
> na Fase 2: os checkpoints atrasados seriam respondidos por ele para não travar
> o progresso. O raciocínio abaixo é dele, não meu — onde eu discordar, eu edito.
>
> Das 5 perguntas originais, 3 foram respondidas. As descartadas estão no fim,
> com o motivo.

---

## 1. Por que `mypy --strict` e o `import-linter` estão na Fase 0, e não na Fase 5, onde a arquitetura aparece?

Porque o caro não é a ferramenta, é o retrofit.

Tipar a primeira linha do projeto custa zero. Tipar 5 mil linhas depois é um
projeto em si, com risco de mudar comportamento no meio. O mesmo vale para o CI:
ninguém adiciona CI a um sistema que já funciona sem ele, porque o benefício é
invisível até o dia em que já era necessário.

Tem um efeito mais sutil, e ele é o principal. Guardrail que chega depois do
código chega **depois dos hábitos**. E quando chega, reporta 200 violações de
uma vez — o que na prática é igual a reportar zero, porque ninguém corrige 200.
Um guardrail só funciona se nunca houve um momento em que ele esteve desligado.

Mas a resposta tem uma correção importante, que a própria fase produziu: o
`import-linter` **não** entrou na Fase 0. Ele ficou para a Fase 5.

A diferença entre os dois casos define a regra de verdade:

- `mypy` e `ruff` verificam algo que existe desde a primeira linha de código.
  Entram no dia zero.
- `import-linter` verifica contratos entre camadas. Na Fase 0 não existiam
  camadas, então ele não teria nada para verificar. Ferramenta sem contrato é
  ruído, e ruído treina a ignorar o output.

Ou seja: guardrail entra junto com a coisa que ele protege, não antes nem depois.

---

## 2. O CI roda exatamente os mesmos comandos que eu rodo localmente. Então o que ele me dá que a minha máquina não dá?

Três coisas, e nenhuma delas é "automatiza".

**Um ambiente que não é o meu.** A minha máquina tem o `.venv` já montado, o
`.env` preenchido, o Postgres de pé e o cache do `uv` quente. O CI começa do
zero e prova que o projeto é reproduzível **a partir do repositório sozinho**.
Se eu esquecer de commitar o `uv.lock` ou uma variável do `.env.example`, só o
CI descobre.

Isso deixou de ser teórico na Fase 2: o `.venv` local quebrou porque alguém
rodou `uv` de dentro do WSL, e o CI continuou verde — o que provou na hora que
o problema era da minha máquina e não do código.

**Ele não é opcional.** Localmente eu posso pular, e num dia corrido eu pulo.
No CI o merge fica bloqueado. A diferença entre disciplina e ferramenta é
exatamente essa, e é o mesmo argumento do `import-linter` na Fase 5.

**Ele é um histórico.** Verde ou vermelho por commit. Quando algo quebra, eu
descubro **quando** quebrou, não só que está quebrado — o que transforma
"investigar um bug" em "ler um diff".

---

## 3. Qual é a diferença conceitual entre "configuração" e "código"? Por que um `Settings` tipado é melhor que `os.getenv()` espalhado, em termos de acoplamento?

**Código é o que o sistema faz. Configuração é o que muda entre ambientes sem
mudar o que o sistema faz.** A URL do banco muda entre local, CI e produção; a
regra do tópico duplicado não muda em lugar nenhum. A primeira é configuração,
a segunda é código.

Em termos de acoplamento, o problema do `os.getenv()` espalhado é que ele cria
uma **dependência invisível num singleton global mutável** — o ambiente do
processo. Uma função que chama `os.getenv("DATABASE_URL")` por dentro anuncia,
na assinatura, que não precisa de nada. E mente. Você só descobre lendo o corpo,
e para testar precisa manipular estado global.

Com um `Settings` que é passado como parâmetro, a dependência fica escrita na
assinatura e vira substituível. É o mesmo problema do `datetime.now()`, que na
Fase 5 vira o port `Clock`, e a mesma cura.

Tem ainda um ganho de fronteira: `os.getenv()` devolve `str | None` sempre,
então **todo lugar** que usa precisa validar e converter. O `Settings` valida
uma vez, na entrada, e daí para dentro o valor é garantidamente válido. Isso é
o embrião da ideia que a Fase 4 formaliza em Value Object.

E o fecho, que só ficou claro discutindo o singleton: ter uma instância só nunca
foi o ponto. O ponto é **um lugar só do sistema ir buscar, e todo o resto
receber**. No projeto, esse lugar é o `create_app()`, e depois passou a ser
também o `alembic/env.py` — duas portas de entrada, dois Composition Roots.

---

## Perguntas descartadas

**"Se você tivesse escolhido SQLite, qual decisão futura ficaria mais cara, e
quanto? Estime em horas."** — Descartada por ser especulação sobre um cenário
que não aconteceu. O conteúdo útil dela já está registrado no ADR-002, com o
raciocínio real em vez de uma estimativa inventada.

**"Escolha o item desta fase que mais pareceu burocracia e construa o melhor
argumento para pulá-lo. Depois destrua seu próprio argumento."** — Descartada
porque a fase respondeu isso sozinha, na prática: o item que mais parecia
burocracia era o repositório git separado, e ele foi o único momento em que algo
irreversível esteve em jogo. O repo estava apontando para o `corrige_ai` de
outra pessoa, e um `git push` teria mandado 17 projetos para lá.
