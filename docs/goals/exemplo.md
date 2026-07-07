# Objetivo: adicionar rate limiting ao endpoint público de busca
<!-- ARQUIVO DE EXEMPLO — mostra a régua de qualidade de um contrato gerado por /goal.
     Note: todo critério é CHECÁVEL; não-objetivos contêm a deriva; suposições estão declaradas. -->
Criado: 2026-07-06 | Pedido original: "a busca tá sendo abusada por bots, dá um jeito"

## Por quê (valor)
Bots geram ~70% do tráfego de `/api/search` e degradam a latência para usuários reais.

## Critérios de aceite
- [ ] Requisições acima de 30/min por IP em `/api/search` recebem 429 — verificação:
      teste de integração novo `tests/api/rate-limit.test.ts` passa.
- [ ] Resposta 429 inclui header `Retry-After` — verificação: assert no mesmo teste.
- [ ] Usuários autenticados têm limite maior (120/min) — verificação: caso no teste.
- [ ] Latência p95 do endpoint não piora > 5ms com o limiter ligado — verificação:
      `pnpm bench:search` antes/depois, números no relatório.
- [ ] Suite inteira + typecheck verdes — verificação: saída dos comandos no relatório final.

## Não-objetivos (fora de escopo desta rodada)
- CAPTCHA, bloqueio por fingerprint, WAF — só o rate limit simples.
- Rate limiting nos demais endpoints (proposta separada se este funcionar).
- Dashboard de métricas de abuso.

## Restrições
- Sem dependência de infraestrutura nova (usar o Redis que já existe; não introduzir serviço).
- Limites configuráveis por env var, com defaults acima.

## Suposições declaradas
- "Abuso" = volume por IP (não há evidência de ataque distribuído sofisticado). Se logs
  mostrarem o contrário, volto antes de implementar.
- Janela deslizante simples é suficiente (não precisa de token bucket exato).

## Riscos conhecidos
- IPs compartilhados (CGNAT) podem limitar usuários legítimos → mitigação: limite maior para
  autenticados + monitorar 429s na primeira semana.
- Redis indisponível → decisão: fail-open (busca funciona sem limite) — melhor degradar
  proteção que derrubar a feature.
