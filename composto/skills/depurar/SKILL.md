---
name: depurar
description: Investigação de causa raiz para bugs — reproduzir, hipóteses concorrentes, bisseção, correção com teste vermelho-verde. Use quando a entrada é comportamento quebrado, não uma feature.
argument-hint: "[descrição do bug | mensagem de erro | 'os testes X falham']"
---

# /depurar — do sintoma à causa, com prova

Entrada: `$ARGUMENTS`

**Se o projeto tiver a skill `analise-profunda` (kit de partida), invoque-a — ela é a doutrina
completa desta.** O método abaixo é a versão embutida para projetos sem o kit.

## Fase 1 — Investigação
1. **Reproduza** antes de teorizar. Não reproduziu → registre o tentado; "não reproduz" é dado
   central, não licença para chutar.
2. **Leia o erro INTEIRO** — mensagem, stack, e a PRIMEIRA falha do log (as outras são cascata).
3. **O que mudou?** `git log` da área, dependências, config, dados. Bug novo em código velho tem
   gatilho recente.
4. **≥2 hipóteses ANTES de investigar a primeira**, cada uma com teste discriminante definido
   ANTES de rodar ("se H1, verei X; se H2, verei Y"). Uma hipótese só = ancoragem.
5. **Bisseccione:** por camada (o dado está certo na fronteira N?), por tempo (commit que
   introduziu), por dado (menor entrada que ainda falha). Cada verificação corta ~metade.
6. **Uma mudança por vez** — e NENHUMA correção "de passagem" durante a investigação (contamina
   a evidência).
7. Mantenha 3 listas separadas: FATOS (com fonte), INFERÊNCIAS, SUPOSIÇÕES. Empacou? A causa está
   quase sempre numa suposição não testada — promova-a a hipótese.
8. **Causa ≠ sintoma:** pergunte "por quê" até bater em decisão/config/premissa. Consertar onde
   estourou (`if null` no local do crash) esconde o defeito e o espalha.

## Fase 2 — Correção (só depois da causa demonstrada)
1. **Teste que reproduz o bug** — veja-o VERMELHO (caso mínimo da bisseção = teste ideal).
2. **Correção mínima, na causa.**
3. **Verde** — o novo teste + a suite inteira (compare com baseline se conhecido).

## Fase 3 — Entrega
```
CAUSA RAIZ: <decisão/config/premissa> — evidência decisiva: <comando→saída | arquivo:linha>
Cadeia: <sintoma ← elo ← elo ← causa>
Correção: <o que mudou, N linhas> | Regressão: <teste novo> | Suite: <X/Y>
Prevenção: <o que impediria a reincidência: teste, guardrail, invariante — proposto ou aplicado>
Confiança: alta|média|baixa — <o que a derrubaria>
```
Se o pedido era só DIAGNÓSTICO: entregue a Fase 1 + correção PROPOSTA (diff em bloco, não
aplicado) e pare.

## Condições de parada
3 hipóteses mortas ou orçamento estourado → PARE e entregue as 3 listas + hipóteses testadas +
melhor suspeita ranqueada + próximo teste que faria. Isso é entregável valioso; flailing não é.
Bug raiz for de terceiro (lib, serviço) → evidência + workaround mínimo + onde reportar.

## Depois
Bug custou > 30 min ou vai reincidir → sugira `/compound` (a investigação está fresca — é agora
que ela vira patrimônio). Correção não-trivial → sugira `/revisar` antes de commitar.
