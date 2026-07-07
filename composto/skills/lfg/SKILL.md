---
name: lfg
description: Pipeline autônomo completo — plano, execução, simplificação, revisão e fechamento local com gates adversariais.
disable-model-invocation: true
argument-hint: "[descrição da feature | caminho de plano] [enviar:pr]"
---

# /lfg — autopilot com gates de verdade

Entrada: `$ARGUMENTS`

Execute as fases EM ORDEM. Nenhum gate é auto-atestado: gate = comando executado ou agente
verificador — nunca "confio que está ok". Entre fases, narre em 1 linha o que fechou e o que abre.

**Regra de fechamento (lida antes de começar):** entrega é LOCAL. Commit local apenas se o usuário
autorizou commits (AUTONOMY.md/CLAUDE.md ou pedido). Push/PR SOMENTE se `$ARGUMENTS` contém
`enviar:pr` ou o usuário mandou explicitamente nesta sessão. Sem autorização: deixe o diff no
working tree e reporte. Nunca contorne isto.

## Fase 0 — Contrato (2 min, não pule)
- Existe `docs/goals/ATIVO.md`? Use-o como contrato.
- Senão: derive dos argumentos um mini-contrato (objetivo em 1 frase + 2–5 critérios de aceite
  CHECÁVEIS + não-objetivos) e grave em `docs/goals/ATIVO.md`. Ambiguidade que muda o resultado
  em pipeline autônomo → escolha o razoável, DECLARE no contrato em "Suposições declaradas".
- Argumento é caminho de plano pronto? Valide o gate da Fase 1 e pule para a Fase 2.

## Fase 1 — Plano
Invoque a skill `plano` com o contrato/descrição (headless: sem menus).
**GATE 1:** o arquivo do plano existe em `docs/plans/` E toda unidade tem verificação própria E os
caminhos citados existem (`ls` neles). Falhou → invoque `plano` de novo apontando a lacuna exata.
Falhou 2× → PARE e reporte o que está faltando; não improvise implementação sem plano.

## Fase 2 — Trabalho
Invoque a skill `trabalhar` com o caminho do plano (`modo:retornar` — sem cauda de entrega).
**GATE 2 (adversarial):** despache o agente `verificador-adversarial` com o envelope de retorno
(afirmações de "feito" + evidências citadas). Ele confirma por execução: suite roda? unidades
marcadas feitas têm o comportamento? Qualquer REFUTADO → volte a `trabalhar` com a lista de
refutações (1 retry). Persistindo → PARE, reporte estado real + handoff.

## Fase 3 — Simplificação
Pule se: diff < 10 linhas OU só docs/config. Senão invoque `simplificar` (preserva comportamento,
suite verde antes/depois). Não commite aqui.

## Fase 4 — Revisão
Invoque `revisar` em modo `aplicar` sobre o diff completo. Ela aplica só correções de classe
segura e reroda a suite; achados GRAVES não-aplicáveis retornam na lista.
**GATE 3:** sobrou achado GRAVE confirmado e não aplicado → não siga ao fechamento: registre os
achados em `docs/plans/<plano>-residuos.md`, reporte e PARE (decisão é do usuário).

## Fase 5 — Fechamento
1. Confira o contrato: cada critério de aceite verificado AGORA (comando/observação), não de memória.
2. Aplique a Regra de fechamento (topo). Com `enviar:pr` autorizado: branch nomeado, commit(s)
   com mensagem clara, push, PR citando contrato + evidências; depois `gh pr checks --watch`,
   até 3 ciclos de correção de CI (conserte a causa, nunca enfraqueça teste); CI vermelho após
   3 → registre no PR e pare.
3. Arquive o contrato (`docs/goals/arquivo/`), seção `## Resultado` com evidências.

## Fase 6 — Compound-lite
Não rode a captura completa sozinho (cara). Liste 1–3 candidatos a aprendizado em 1 linha cada
("X custou tempo porque Y — vale documentar?") no relatório final, sugerindo `/compound`.

## Relatório final (formato)
```
RESULTADO: <entregue local | PR aberto | parado na fase N>
Contrato: <critério → ✅/❌ + evidência (comando → saída resumida)>
Diff: <N arquivos, ~N linhas> | Suite: <antes → depois> | Não testado: <ou "nada">
Resíduos: <achados/riscos pendentes ou "nenhum">
Aprendizados candidatos: <1–3 linhas>
```

## Protocolo de falha (vale em toda fase)
Mesma falha 2× → hipótese nova, nunca 3ª tentativa igual. 3 hipóteses mortas ou bloqueio externo →
PARE: estado real + o que cada falha provou + próximo passo recomendado. Pipeline que empaca e
reporta bem é sucesso parcial; pipeline que finge terminar é fracasso total.
