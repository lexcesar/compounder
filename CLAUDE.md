# [AJUSTE: Nome do Projeto]

[AJUSTE: uma frase — o que este projeto é e para quem. Exemplo: "API de cobrança recorrente para o produto X; consumida pelo app mobile e pelo painel admin."]

## Início de sessão
1. Leia `MEMORY.md` (índice; abra só as memórias relevantes à tarefa).
2. Se existir `docs/goals/ATIVO.md`, leia — é o contrato vigente da sessão.
3. Decisões seguem `AUTONOMY.md` (zonas verde/amarela/vermelha).

## Comandos
Nunca adivinhe comandos: confirme em `package.json` / `Makefile` / CI antes do primeiro uso.

- Testes: `[AJUSTE: ex. pnpm test]`
- Teste único: `[AJUSTE: ex. pnpm test -- caminho/arquivo]`
- Lint + tipos: `[AJUSTE: ex. pnpm lint && pnpm typecheck]`
- Build: `[AJUSTE]`
- Rodar local: `[AJUSTE]`

## Arquitetura em 30 segundos
[AJUSTE: 3–6 linhas. Onde mora o quê. Exemplo:]
- `src/domain/` — regras de negócio puras (sem I/O).
- `src/adapters/` — banco, filas, HTTP externo.
- `src/api/` — rotas e validação de entrada.
- Fluxo típico: rota → caso de uso em domain → adapter.

## Convenções não-óbvias
[AJUSTE: só o que não dá para inferir lendo o código. Exemplos:]
- Migrations nunca são editadas depois de mescladas; crie uma nova.
- Datas sempre em UTC no banco; conversão só na borda.

## Invariantes — violação = pare e pergunte
- Nunca leia ou grave segredos (`.env*`, `secrets/`, chaves privadas).
- Nunca `git push`, deploy, migration ou operação em produção sem ordem explícita nesta sessão.
- Nunca reporte "feito" sem verificação executada nesta sessão (teste, build ou execução real).
- Nunca contorne uma permissão negada por outro caminho — negação é resposta, não obstáculo.
- Nunca delete ou pule um teste que falha para "ficar verde".
- [AJUSTE: invariantes do projeto — ex. "nunca tocar em `legacy/`".]

## Ciclo de trabalho
**Entender → Planejar (se ≥ 2 arquivos ou risco) → Agir → Verificar → Reportar com evidência → Aprender.**
Nunca pule o primeiro nem os dois últimos.

## Leia sob demanda (não antecipadamente)
| Situação | Leia |
|---|---|
| Tarefa não-trivial, vai planejar | `docs/mentor/04-planejamento.md` |
| Bug misterioso, investigação | `docs/mentor/05-analise-profunda.md` |
| Vai delegar a subagentes | `docs/mentor/06-delegacao-e-subagentes.md` |
| Vai escrever/alterar testes ou propor mudança | `docs/mentor/09-testes-e-mudancas.md` |
| Dúvida se pode agir sozinho | `AUTONOMY.md` |
| Usuário te corrigiu | `docs/mentor/07-retroalimentacao-e-evolucao.md` |
| Sessão longa, contexto pesado | `docs/mentor/10-contexto-e-comunicacao.md` |
| Vai criar convenções/plugin de conhecimento p/ time | `docs/mentor/11-sistemas-de-convencoes.md` |
| Decisão de vida/negócio/projeto do usuário | `/conselho` (avatares em `avatares/`) |

## Regras de ouro (versão completa: `docs/mentor/00-principios.md`)
1. Nunca edite o que não leu.
2. Nunca afirme o que não verificou — rotule: `[verificado]` / `[inferido]` / `[suposição]`.
3. Menor diff honesto; escopo é contrato — nem mais, nem menos que o combinado.
4. Reversível → aja e anote. Irreversível → pergunte.
5. Falhou 2× do mesmo jeito → formule hipótese nova antes da 3ª tentativa.
6. Correção do usuário → vira regra gravada (memória ou este arquivo, via `/retro`).

<!-- Manutenção deste arquivo: cada linha custa contexto em TODAS as sessões, para sempre.
     Teste antes de adicionar: "se eu apagar esta linha, algum comportamento piora?"
     Se a resposta é não, ela não entra. Regras: docs/mentor/01-anatomia-do-claude-md.md -->
