---
name: analise-profunda
description: Investigação metódica de bugs e comportamentos misteriosos. Use quando o usuário reporta erro sem causa óbvia, comportamento inesperado, "funcionava ontem", divergência entre ambientes, ou pede diagnóstico/análise de causa raiz.
---

# Análise profunda — protocolo de investigação

Objetivo: chegar à CAUSA (não ao sintoma) com evidência, e dizer com que confiança.
Fundamentos e táticas por camada: `docs/mentor/05-analise-profunda.md`.
Saída final no formato de `docs/templates/analise.md`.

## Sequência obrigatória

**1. Reproduza antes de teorizar.**
Rode o que falha e veja com os próprios olhos. Não conseguiu reproduzir? Registre exatamente o que
tentou e trate "não reproduz" como dado central — não siga adiante fingindo que reproduziu.

**2. Leia o erro inteiro. Literalmente inteiro.**
Mensagem, stack completa, a PRIMEIRA falha do log (as seguintes costumam ser cascata). A resposta
está no texto do erro com frequência humilhante. Copie o trecho decisivo para a análise.

**3. Pergunte "o que mudou?"**
`git log` recente, dependências atualizadas, config, dados, ambiente. Bug novo em código velho
quase sempre tem uma mudança recente como gatilho.

**4. Escreva ≥ 2 hipóteses ANTES de investigar a primeira.**
Uma hipótese só = ancoragem garantida. Para cada uma, defina o teste discriminante ANTES de
executá-lo: "se H1 é verdade, verei X; se falsa, verei Y." Tabela:

| # | Hipótese | Se verdadeira, verei | Teste | Status |
|---|---|---|---|---|

**5. Rastreie o dado, não a vibração.**
Siga o valor real pelas camadas (entrada → transformação → saída). Imprima/inspecione nas
fronteiras. "Acho que aqui ele já está errado" não vale; mostrar o valor errado na fronteira vale.

**6. Bisseccione o espaço.**
Cada verificação deve cortar o espaço de busca pela metade: por camada (front/API/domínio/banco),
por tempo (`git bisect` mental ou real), por dado (qual entrada mínima ainda falha?). Reduza ao
menor caso que reproduz.

**7. Sintoma ≠ causa: pergunte "por quê" até bater em algo primário.**
Onde o erro APARECE raramente é onde ele NASCE. Pare de perguntar quando chegar a uma decisão,
config ou premissa — não a outro efeito.

## Contabilidade de evidência (obrigatória na saída)
Mantenha três listas SEPARADAS — misturá-las é o erro nº 1 de investigação:
- **Fatos** — observados nesta sessão, com fonte (comando + saída, arquivo:linha).
- **Inferências** — deduções a partir dos fatos (diga de quais).
- **Suposições** — o que você está assumindo sem ter olhado.

## Condições de parada
- **Causa encontrada:** demonstre-a (o teste discriminante confirmou; idealmente, um caso mínimo
  reproduz e a correção o faz passar). Entregue: causa raiz + evidência + correção proposta +
  prevenção + confiança (alta/média/baixa + o que a elevaria).
- **3 hipóteses mortas / orçamento esgotado:** pare e entregue a contabilidade de evidência com
  sua melhor suspeita ranqueada. Isso É um entregável valioso — nunca estique com tentativas aleatórias.

## Proibições
- Corrigir "de passagem" durante a investigação (mudar o sistema contamina a evidência).
- Duas mudanças simultâneas para testar uma hipótese.
- Concluir causa por semelhança com bug conhecido, sem evidência local que a confirme.
- Se o pedido era DIAGNÓSTICO: entregue o parecer e PARE. Aplicar a correção é outro pedido.
