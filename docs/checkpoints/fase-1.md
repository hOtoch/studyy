# Checkpoint Socrático — Fase 1

> Responda **sem pesquisar e sem perguntar a uma IA**. Resposta errada escrita
> com convicção vale mais que resposta certa copiada, porque mostra onde o
> modelo mental está torto.
>
> Se não souber, escreva **"não sei, e o que me confunde é X"**. É uma resposta
> válida e a mais útil de todas.
>
> Você vai responder estas mesmas 5 perguntas de novo ao final da Fase 5.
> A comparação entre as duas versões é o registro mais honesto do seu progresso.

O objeto de estudo é `src/studyy/main.py`, 408 linhas.

---

## 1. Para testar a regra "não pode haver dois tópicos com o mesmo título na mesma matéria", eu preciso de um banco de dados rodando?

Por quê? E se precisa, o que exatamente na forma como o código está escrito obriga isso?

**Resposta original:** Precisa, pois abrimos uma nova sessao de pools com o banco de
dados e rodamos uma query nele para conseguir ter acesso a todos os topicos criados da
materia em questão e verificar se alguma ja possui o titulo que foi enviado como
parametro para a requisição.

**Depois da arguição:** Não precisa, pois para um teste, so precisamos fazer uma
comparaçao de duas strings.

---

## 2. Se eu quisesse trocar o Postgres por outro banco, quantos arquivos e quantas linhas eu tocaria?

Não chute. Abra o arquivo e conte.

**Resposta original:** Acho que eu so teria que trocar o DATABASE_URL do .env.

**Depois da arguição:** Se for para outro banco de dados SQL, teria que trocar o
DATABASE_URL do .env. Se for para um NoSQL, teria que alterar todas as linhas que
utilizam os metodos do SQLAlchemy, que no total sao 65.

---

## 3. Se eu quisesse expor a mesma funcionalidade por uma CLI, além da API HTTP, quanto código eu duplicaria?

O que especificamente eu conseguiria reaproveitar, e o que teria que reescrever?

**Resposta original:** Nao sei como funcionanaria por CLI.

**Depois da arguição:** Para toda requisicao HTTP teriamos que reescrever para que, ao
inves de utilizar o objeto Request para abrir uma sessao com o banco de dados,
utilizariamos os args do comando enviado.

---

## 4. Quantas responsabilidades diferentes existem dentro de uma única função de rota?

Pegue a `create_topic` e liste tudo que ela faz, passo a passo. Não resuma.

1. Verifica se parametro nao esta vazio.
2. Abre uma nova sessao com o banco de dados.
3. Aplica regra de negocio, quando necessario.
4. Cria/Atualiza/Deleta/Retorna o objeto.
5. Atualiza o banco de dados.
6. Valida schema do objeto retornado.

---

## 5. Se a regra do tópico duplicado mudar, onde eu procuro?

E quantos lugares eu preciso alterar para que a mudança valha em todo o sistema?

Procuraria e atualizaria nos metodos HTTP de criação/atualização de topicos.

---

## Observação livre

Qualquer outra coisa que te incomodou ao ler o arquivo, mesmo que você não
saiba nomear ainda.

Aplicativo muito extenso para pouca funcionalidade.
