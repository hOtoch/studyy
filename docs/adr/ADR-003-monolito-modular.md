# ADR-003: Monólito modular, não microsserviços

- **Status:** aceito
- **Data:** 2026-09-21

## Contexto

Microsserviços estão na minha lista de temas a estudar, e a tentação de aplicar
no Studyy é grande — é o assunto mais falado da área e parece ser o destino
natural de um sistema "bem arquitetado".

O domínio, de fato, já se divide em cinco contextos com fronteiras claras:
`content`, `planning`, `execution`, `progression` e, futuramente, `assistant`.
Tecnicamente, dava para transformar cada um num serviço.

Mas o contexto real do projeto é:

- Um desenvolvedor, em tempo parcial.
- Um usuário.
- Sou iniciante em arquitetura e ainda não sei se as fronteiras que desenhei
  estão certas.

## Decisão

Vamos construir um **monólito modular**: um único processo e um único deploy,
internamente dividido em Bounded Contexts com fronteiras reais, verificadas
automaticamente pelo `import-linter` no CI a partir da Fase 5.

Os contextos não se importam diretamente. Comunicam-se por eventos de domínio
ou por portas de leitura estreitas.

## Alternativas consideradas

- **Microsserviços desde o início** — descartado. Microsserviços resolvem um
  problema **organizacional**: vários times fazendo deploy sem se coordenar.
  Eu não tenho esse problema. O que eu teria são todos os custos — rede não
  confiável, transações distribuídas, observabilidade distribuída, versionamento
  de contrato, orquestração — sem nenhum dos benefícios.

  E há um argumento mais forte, que é sobre aprendizado: microsserviços exigem
  que as fronteiras de domínio **já estejam certas**. Como eu ainda não sei se
  as minhas estão, o que eu preciso é justamente da liberdade de errar barato.
  Corrigir uma fronteira num monólito modular custa horas; em microsserviços,
  custa meses.

- **Monólito sem modularização** (camadas técnicas apenas: `routers/`,
  `services/`, `models/`) — descartado porque é o caminho mais curto para o
  *big ball of mud*. Organizar por tipo técnico em vez de por domínio faz com
  que toda feature toque todas as pastas, e as fronteiras nunca aparecem.

## Consequências

- ✅ Um deploy, um log, um banco, uma transação. Toda a complexidade que
  sobrar é do domínio, não da infraestrutura.
- ✅ Errar uma fronteira é barato. Isso importa muito para quem está
  aprendendo a desenhar fronteiras.
- ✅ Consistência forte de graça: concluir uma sessão e creditar XP podem ser
  atômicos se eu quiser. Em serviços separados, isso viraria saga.

- ❌ Não vou exercitar operação distribuída na prática — deploy independente,
  descoberta de serviço, contrato versionado entre serviços.
  **Mitigação:** a Fase 13 tem um exercício opcional de extrair o contexto
  `progression` para um processo separado, sentir a dor, e reverter. O
  aprendizado é o entregável, não a arquitetura resultante.
- ❌ As fronteiras podem apodrecer, porque nada na linguagem as impõe (ver
  ADR-001). **Mitigação:** contratos do `import-linter` rodando no CI, com
  falha bloqueando merge.
- ❌ Um módulo pesado pode degradar os outros, já que compartilham processo.
  Isso é exatamente o que o gatilho abaixo observa.

- 🔄 **Gatilho de reversão:** vou considerar extrair um módulo para serviço
  próprio quando **qualquer uma** destas for verdade:

  1. **Organizacional** — existir mais de uma pessoa fazendo deploy, com ciclos
     que precisem ser independentes. (Hoje: 1.)
  2. **Perfil de recurso** — um módulo tiver necessidade de recurso
     radicalmente diferente dos outros. O candidato concreto é a ingestão do
     RAG na Fase 14: se ela saturar CPU e a latência p95 da API passar de
     500 ms por causa disso, ela sai primeiro.
  3. **Escala** — o Studyy deixar de ser pessoal e passar de algumas centenas
     de usuários ativos.

  E mesmo quando o gatilho disparar, a resposta é **extrair aquele módulo**,
  não fatiar o sistema inteiro. A extração vai ser viável exatamente porque a
  fronteira já existia e era verificada.
