---
description: Entrevista o usuário e gera guardrails em camadas (settings.json, invariantes, autonomia)
argument-hint: [opcional - área específica, ex. "banco de dados"]
---

# /guardrails — construir limites sob medida

Foco pedido (se houver): `$ARGUMENTS`

Limites claros AUMENTAM a autonomia útil: quanto mais o usuário confia nas cercas, menos ele
precisa vigiar cada passo. Método completo: `docs/mentor/08-guardrails-e-boundaries.md`.

## Passo 1 — Reconhecimento (antes de perguntar)
Olhe o projeto e deduza o que puder sozinho: stack, scripts disponíveis, existência de `.env*`,
diretórios sensíveis aparentes (`migrations/`, `infra/`, `deploy/`), CI. Não pergunte o que o
repositório já responde.

## Passo 2 — Entrevista (uma rodada, no máximo 7 perguntas, agrupadas)
Use AskUserQuestion/perguntas diretas, sempre oferecendo um padrão recomendado:
1. **Intocáveis:** que caminhos/arquivos eu nunca devo modificar? (sugira os que deduziu)
2. **Segredos:** onde vivem? (`.env`? vault? outros)
3. **Comandos proibidos vs. com confirmação:** deploy? migrations? push? deleção recursiva?
4. **Ambientes:** existe risco de eu alcançar staging/produção daqui? Como distingo?
5. **Orçamento de autonomia:** posso instalar dev-dependencies? criar arquivos? deletar código morto?
6. **Dados sensíveis:** algo que nunca pode sair da máquina (nem em prompt de subagente/serviço)?
7. **Ritmo:** prefere que eu pergunte mais (segurança) ou avance mais (velocidade)?

## Passo 3 — Gerar em camadas
Para cada resposta, escolha a camada MAIS DURA que a comporta:
1. **`.claude/settings.json`** (`permissions.deny` / `ask` / `allow`) — mecânico, não depende
   de o modelo lembrar. Tudo que puder ser padrão de ferramenta, vai aqui.
2. **`CLAUDE.md` → Invariantes** — regras que exigem julgamento ("nunca editar migration mesclada").
   Frase testável: começa com "nunca"/"sempre" + condição observável.
3. **`AUTONOMY.md`** — ajustes das zonas (ex.: usuário liberou dev-deps → mover para 🟢;
   pediu mais confirmações → mover itens para 🔴).
4. **Hook** (opcional, só se o usuário quiser proteção programática) — proponha o snippet de
   `docs/mentor/08-guardrails-e-boundaries.md` §Hooks, explicando o que bloqueia.

## Passo 4 — Aplicar com transparência
Mostre TODOS os diffs propostos de uma vez (settings.json, CLAUDE.md, AUTONOMY.md). Aplique após
o ok. Termine com o resumo em 3 linhas: o que ficou proibido, o que pede confirmação, o que ficou
liberado — e a frase: "para revisar isso no futuro, rode `/guardrails` de novo; para evoluir a
partir de incidentes, o `/retro` alimenta estas mesmas camadas."
