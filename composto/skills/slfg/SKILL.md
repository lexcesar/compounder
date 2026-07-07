---
name: slfg
description: Let the swarms fucking go — o pipeline do /lfg com pesquisa, revisão e verificação em ENXAME paralelo.
disable-model-invocation: true
argument-hint: "[descrição da feature] [enviar:pr] [orcamento:liberado]"
---

# /slfg — o enxame

Entrada: `$ARGUMENTS`

Mesmos contratos, gates e regra de fechamento do `/lfg` (leia a skill `lfg` antes — ela é a
constituição; esta skill só troca o MOTOR de execução por paralelismo). Diferenças abaixo.

## Custo e consentimento
Enxame custa 3–10× o `/lfg`. Se `$ARGUMENTS` não contém `orcamento:liberado`, anuncie a estimativa
("~N agentes: pesquisa 3, revisão 4–6, verificação 1 por achado") e peça um ok ANTES de disparar.

## Capacidades: detecte e degrade com elegância
1. **Melhor caso** — ferramenta `Workflow` disponível (orquestração determinística): use-a para
   os fan-outs abaixo (pipeline por item, sem barreiras desnecessárias).
2. **Caso normal (Opus/Sonnet/Haiku)** — ferramenta de subagentes (`Task`/`Agent`): dispare os
   agentes de cada onda NUMA ÚNICA mensagem (várias chamadas juntas = paralelo real). Nunca em série.
3. **Sem subagentes** — vire `/lfg` sequencial e avise.

## Fase 1' — Pesquisa em enxame (antes do plano)
3 `pesquisador` em paralelo, lentes distintas e independentes:
- A: padrões do codebase na área (arquivos, convenções, utilitários existentes).
- B: memória institucional — `docs/solutions/`, `CONCEPTS.md`, `docs/plans/` anteriores, memórias.
- C: contratos e consumidores — quem chama o que vai mudar, testes existentes, superfícies de API.
Cada um devolve dossiê ≤40 linhas com `arquivo:linha`. O plano da Fase 1 é escrito a partir dos
3 dossiês (cite-os). Amostre 2 citações de cada antes de confiar (uma falsa → refaça aquela lente).

## Fase 2' — Trabalho
Unidades do plano são executadas EM SEQUÊNCIA por padrão (edições paralelas colidem). Paralelize
somente se o plano declarar unidades sem interseção de arquivos E houver isolamento real
(worktrees); na dúvida, sequencial — enxame é para LER e JULGAR em paralelo, não para escrever.

## Fase 4' — Revisão em enxame
Onda 1 (paralela): 4 revisores (`revisor-correcao`, `revisor-seguranca`, `revisor-simplicidade`,
`revisor-testes`) sobre o mesmo diff.
Dedup (você, sem agente): funda achados no mesmo `arquivo:linha`; corroboração entre revisores
sobe a severidade em 1 nível.
Onda 2 (paralela): cada achado GRAVE/MÉDIO vai a um `verificador-adversarial` instruído a REFUTÁ-LO.
Sobrevive = confirmado; refutado = morre. (Isto filtra o plausível-mas-falso — o veneno específico
de revisão por agentes.)
Aplicação: como no `/lfg` Fase 4 (classe segura + suite).

## Fase 5'/6' — idênticas ao /lfg
Fechamento local por padrão; compound-lite no relatório.

## Relatório: acrescente a linha de enxame
```
Enxame: <N agentes: pesquisa X, revisão Y, verificação Z> | refutados na Onda 2: <N>
```
Achado refutado NÃO aparece como problema no relatório — no máximo como "descartado na verificação".

## Regras de ouro do enxame
1. Briefing completo em cada agente (ele nasce sem a sua conversa): objetivo, contexto, escopo
   negativo, formato de retorno. Agente que voltou lixo 1× → conserte o briefing, não o agente.
2. Ondas paralelas só de trabalho INDEPENDENTE; resultados que se alimentam = fases distintas.
3. Nada de segredo em briefing.
4. Você é o gargalo de síntese: agentes coletam e julgam; quem integra, decide e ASSINA é você.
   "O agente disse" não existe no relatório final.
