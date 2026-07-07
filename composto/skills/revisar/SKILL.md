---
name: revisar
description: Revisão multi-lente com verificação adversarial dos achados. Use após implementar, antes de commit/PR, ou quando o usuário pedir revisão de diff/branch/arquivos.
argument-hint: "[escopo: branch | arquivos | vazio = diff vs default] [aplicar]"
---

# /revisar — painel + tribunal

Entrada: `$ARGUMENTS` (token `aplicar` = além de reportar, aplicar correções de classe segura).

Dois estágios porque agentes revisores têm um veneno específico: achados PLAUSÍVEIS-MAS-FALSOS.
O painel acha; o tribunal mata os falsos. Só o que sobrevive chega ao usuário.

## Passo 0 — Escopo
Sem argumento: diff do branch atual vs default (`git diff <default>...HEAD` + working tree).
Com argumento: o que ele disser. Diff vazio → diga e pare. Anote: N arquivos, ~N linhas.
Diff gigante (>~1500 linhas): reviste por área em rodadas e diga que fez isso.

## Passo 1 — Painel (paralelo)
Despache os 4 revisores NUMA única mensagem (paralelo real), cada um com o escopo + o objetivo
da mudança (1 frase) + instrução de formato:
`revisor-correcao`, `revisor-seguranca`, `revisor-simplicidade`, `revisor-testes`.
Diff pequeno (<50 linhas, sem superfície de entrada externa): só correção + testes bastam — diga
que enxugou o painel. Sem ferramenta de subagentes: rode as 4 lentes você mesmo, em sequência,
uma passada por lente (não misture — lente única por vez é o que mantém o olho afiado).

## Passo 2 — Dedup e corroboração (você, sem agente)
Funda achados no mesmo `arquivo:linha`. Corroborado por 2+ revisores → severidade sobe 1 nível.
Descarte achados de estilo sem mudança de comportamento (não é papel deste painel).

## Passo 3 — Tribunal adversarial
Cada achado GRAVE/MÉDIO vai ao `verificador-adversarial` (paralelo, um por achado; muitos achados →
agrupe por arquivo) com a ordem: REFUTE isto — abra o código, monte o cenário de falha concreto,
procure o contraexemplo. Veredito: CONFIRMADO (cenário demonstrado) | REFUTADO (morre; some do
relatório) | INCONCLUSIVO (rebaixa para "suspeita"). MENORES pulam o tribunal (barato demais para
julgar — reporte como menores mesmo).

## Passo 4 — Relatório
```
VEREDITO: <aprovado | ressalvas | reprovado> — 1 frase
CONFIRMADOS (por severidade):
1. [GRAVE] arquivo:linha — <defeito> | Cenário: <entrada/estado → consequência> | Fix sugerido: <1 linha>
SUSPEITAS (inconclusivas): <...>
MENORES: <agrupados, 1 linha cada>
DESCARTADOS NO TRIBUNAL: <N achados refutados — não são problemas>
COBERTURA: <lentes rodadas + onde se procurou sem achar>
```
Sem token `aplicar`: PARE aqui — o parecer é o entregável; não toque no código.

## Passo 5 — Aplicação (só com `aplicar`)
Classifique cada CONFIRMADO:
- **Classe segura** (mecânica, local, comportamento coberto por teste existente ou trivialmente
  verificável): aplique, menor diff, rode a suite depois de CADA aplicação.
- **Classe insegura** (exige decisão de design, muda contrato, sem cobertura): NÃO aplique —
  devolva na lista com o porquê.
Relatório final: aplicados (com suite verde) vs devolvidos. Suite quebrou com um fix → reverta
AQUELE fix e devolva o achado com a observação.
