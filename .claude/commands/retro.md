---
description: Colhe as lições da sessão e grava cada uma no lugar certo (memória, CLAUDE.md, skill, AUTONOMY)
argument-hint: [opcional - lição específica a registrar]
---

# /retro — retroalimentação que vira regra

Entrada do usuário (lição específica, se houver): `$ARGUMENTS`

Uma correção que não vira regra gravada será repetida. Este comando é o mecanismo de evolução
do sistema inteiro. Método completo: `docs/mentor/07-retroalimentacao-e-evolucao.md`.

## Passo 1 — Colheita (varra a sessão atual)
Liste com honestidade, citando o momento em que aconteceu:
1. **Correções explícitas** — o usuário disse "não", "não é assim", "prefiro X", desfez algo seu.
2. **Correções silenciosas** — o usuário refez ou ajustou o que você entregou.
3. **Seus erros autodetectados** — becos sem saída, hipóteses erradas, comandos adivinhados,
   tempo perdido por não ter lido algo antes.
4. **Acertos confirmados** — abordagens que o usuário aceitou sem mudanças (também são sinal:
   confirmam regras existentes).
5. **Despachos da linha de montagem** — se `docs/pipeline/despachos.jsonl` existir, leia as
   linhas desta sessão (campo `sessao`) e aplique o gatilho de lição e as regras de
   promoção/demissão definidos em `ROTAS.md` (seção Auditoria — endereço único delas).

Sessão sem nada nos itens 1–3? Diga isso e encerre — retro vazio não inventa lição.

## Passo 2 — Destilação (o passo que separa sênior de júnior)
Para cada item, extraia a REGRA GERAL, não o incidente:
- ❌ Incidente: "usei npm mas o projeto usa pnpm."
- ✅ Regra: "antes de qualquer comando de pacote, detectar o gerenciador pelo lockfile."
Teste da boa regra: começaria com "sempre" ou "nunca", e um terceiro entenderia sem conhecer o incidente.

## Passo 3 — Destino (tabela de decisão)
| A lição vale para... | Grave em |
|---|---|
| Este projeto, qualquer sessão, qualquer pessoa | `CLAUDE.md` (respeitando o limite: linha só entra se mudar comportamento) |
| Este usuário, entre projetos (preferência, estilo) | `memory/` novo arquivo + linha no `MEMORY.md` |
| Método em geral, valeria em QUALQUER projeto | Doutrina upstream — o kit/plugin de método que o usuário mantém: proponha a promoção (a lição morre se ficar só na memória do projeto). Sem upstream → `memory/` |
| Limite de permissão ou decisão de autonomia | `AUTONOMY.md` (zonas) ou `.claude/settings.json` |
| Procedimento repetível com passos | Skill/comando: patch no existente ou proposta de novo |
| Rota/modelo errado para tipo de tarefa despachada | `ROTAS.md` (tabela de rotas + registro de evolução) |
| Só valia para a tarefa de hoje | **Não grave.** Ruído acumulado mata o sistema. |

## Passo 4 — Aplicação
1. Mostre ao usuário: lição → regra destilada → arquivo de destino → diff proposto.
2. Aplique o que ele aprovar (edições em arquivos do kit são zona 🟡: aja e anuncie; se a regra
   restringe VOCÊ, pode aplicar direto).
3. **Regra dos dois strikes:** mesmo erro pela 2ª vez entre sessões → gravação é obrigatória,
   não opcional — e mencione no resumo que era reincidência.

## Passo 5 — Poda (a cada ~5 retros ou quando notar)
Regras gravadas que nunca mais dispararam, contradizem feedback mais novo ou referenciam coisas
que não existem mais → proponha deletar. Memória suja é pior que memória vazia: mente com confiança.
Inclui rotas: aplique o critério de poda de rotas definido no próprio `ROTAS.md` (Auditoria).
