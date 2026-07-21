---
etapa: plano-pronto
data: 2026-07-21
slug: linha-de-montagem
---

# Linha de montagem auditada — roteamento de tarefas por rota/modelo com retroalimentação

## Requisitos (derivados da conversa)

- R1: O orquestrador (modelo da sessão, contexto cheio) consulta uma **política de roteamento
  explícita** antes de despachar trabalho a subagente/fork, em vez de decidir ad hoc.
- R2: Cada despacho deixa **trilha auditável** (1 linha em log estrutural): rota, modelo,
  resultado, retrabalho.
- R3: `/retro` **minera o log** e propõe correções na política — a tabela de rota é artefato
  vivo, corrigido por evidência, não doutrina congelada.
- R4: Existe ao menos **uma rota barata real** para carga pesada: executar plano-pronto em
  subagente com modelo menor (`context: fork` + `model` no frontmatter da skill).
- Suposições declaradas: (a) foco é eficiência de token/contexto, não velocidade (dito pelo
  usuário); (b) artefatos entram no kit como template (com `[AJUSTE]`), não só no uso pessoal;
  (c) taxonomia de tarefas limitada a ~6 tipos — estatística com baixo volume não converge com
  taxonomia fina.

## Reconhecimento (visto nesta sessão)

- `composto/skills/trabalhar/SKILL.md` — já tem `modo:retornar` com envelope estruturado
  (Passo 4): é o contrato de retorno que um fork precisa. Frontmatter atual mínimo.
- `composto/skills/lfg/SKILL.md` — pipeline já despacha `plano → trabalhar → simplificar →
  revisar` com gates adversariais; é o consumidor natural futuro das rotas (fora de escopo aqui).
- `.claude/commands/retro.md` — Passo 1 (colheita) e Passo 3 (tabela de destino) são os pontos
  de enxerto; Passo 5 (poda) já cobre o ciclo de vida das regras.
- `composto/agents/` — pesquisador, 4 revisores, verificador-adversarial: rotas já existentes.
- Frontmatter de skill suportado (doc oficial, conferida hoje): `context: fork`, `agent`,
  `model` (override só durante a execução da skill), `effort`, `${CLAUDE_SKILL_DIR}`.
- `docs/pipeline/` e `ROTAS.md` não existem — nomes livres.

## Decisões

1. **Onde mora a política de rota.**
   - (a) Seção no CLAUDE.md — sempre em contexto, mas infla toda sessão e fere a regra "linha
     só entra se mudar comportamento".
   - (b) **`ROTAS.md` na raiz (vencedora)** — mesmo padrão do `AUTONOMY.md`: arquivo próprio,
     lido sob demanda (linha nova na tabela "Leia sob demanda" do CLAUDE.md), editável pelo
     `/retro` sem tocar no CLAUDE.md.
   - (c) Skill `rotear` — rejeitada: roteamento é política consultada, não procedimento invocável.
2. **Formato do log.**
   - (a) Tabela markdown — legível, mas append concorrente e mineração são piores.
   - (b) **JSONL em `docs/pipeline/despachos.jsonl` (vencedora)** — append-only, `jq`/grep na
     mineração, 1 linha por despacho.
3. **Como a rota barata executa o protocolo do `/trabalhar` sem duplicar o texto.**
   - (a) Copiar o corpo da skill para a variante fork — rejeitada: duas fontes de verdade divergem.
   - (b) **Fork lê o protocolo do disco (vencedora)** — corpo da `trabalhar-fork` instrui:
     "leia `${CLAUDE_SKILL_DIR}/../trabalhar/SKILL.md` e execute em `modo:retornar`".
4. **Quem escreve o log.** Orquestrador, por instrução no próprio `ROTAS.md` (que ele acabou de
   ler para despachar). Hook automático rejeitado NESTA versão: infra > disciplina para validar
   o conceito primeiro (pré-mortem 1 cobre o risco).

## Unidades

### U1: Spike — skill `trabalhar-fork` (a suposição mais perigosa primeiro)
- Arquivos: `composto/skills/trabalhar-fork/SKILL.md` (novo)
- Mudança: frontmatter `context: fork`, `agent: general-purpose`, `model: sonnet`,
  `argument-hint: "[caminho do plano]"`, `disable-model-invocation: true` (rota é decisão do
  orquestrador/usuário, não auto-invocação). Corpo curto: leia
  `${CLAUDE_SKILL_DIR}/../trabalhar/SKILL.md`, execute o protocolo em `modo:retornar` sobre o
  plano em `$ARGUMENTS`, retorne SÓ o envelope do Passo 4.
- Testes: plano-brinquedo com 1 unidade trivial (ex.: criar arquivo com conteúdo fixo +
  verificação por `cat`) em `docs/plans/` temporário.
- Verificação: invocar `/composto:trabalhar-fork <plano-brinquedo>`; provar que (a) rodou em
  subagente (contexto principal recebe só envelope), (b) modelo menor foi usado, (c) envelope
  tem STATUS/Unidades/Suite. Falha de campo de frontmatter na versão instalada do CLI →
  registrar exatamente qual campo e abortar as unidades dependentes (U2 muda a rota para
  "Agent tool manual").
- Risco: `model`/`context` não suportados na versão local; `${CLAUDE_SKILL_DIR}` não resolver
  dentro de fork (deferido à execução).
- Depende de: nada.

### U2: `ROTAS.md` — política de roteamento (template do kit)
- Arquivos: `ROTAS.md` (novo, raiz), `CLAUDE.md` (1 linha)
- Mudança: tabela com ≤6 tipos de tarefa → rota → modelo → gate obrigatório. Linhas iniciais:
  localizar código → `explorador`/haiku; executar plano-pronto → `trabalhar-fork` (U1);
  pesquisa de fundamento → `pesquisador`; revisão → painel + tribunal; bug misterioso →
  inline modelo da sessão (nunca despachar); `[AJUSTE: rotas de agentes pessoais]`. Cada rota
  barata declara seu QC (verificador-adversarial ou verificação executável). Seções: "Dever de
  log" (formato da linha JSONL, quando gravar) e "Auditoria" (como o `/retro` minera; regra de
  promoção/demissão de modelo por taxa de retrabalho). No CLAUDE.md, linha nova na tabela
  "Leia sob demanda": "Vai despachar trabalho a subagente/fork | `ROTAS.md`".
- Testes: n/a (doc); litmus — toda rota citada existe (`composto/agents/`, agentes built-in ou U1).
- Verificação: `grep` das rotas contra `ls composto/agents/` + lista de built-ins; CLAUDE.md
  diff de 1 linha.
- Depende de: U1 (define se a rota de plano-pronto é fork ou fallback).

### U3: Log de despacho — schema + semente
- Arquivos: `docs/pipeline/despachos.jsonl` (novo), schema documentado dentro do `ROTAS.md` (U2)
- Mudança: campos `{"data","tarefa","tipo","rota","modelo","resultado","retrabalho","notas"}`
  (`resultado`: completo|parcial|bloqueado|refutado; `retrabalho`: bool). Semente: a linha real
  do despacho da U1 (o spike é o primeiro registro auditado — dogfood imediato).
- Testes: n/a.
- Verificação: `jq -c . docs/pipeline/despachos.jsonl` parseia todas as linhas sem erro.
- Depende de: U1 (gera a linha-semente), U2 (schema documentado).

### U4: `/retro` minera despachos
- Arquivos: `.claude/commands/retro.md`
- Mudança: (a) Passo 1 ganha item 5 — "Despachos: se `docs/pipeline/despachos.jsonl` existe,
  leia as linhas da sessão; rota com `retrabalho:true` ou `refutado` vira lição candidata";
  (b) tabela do Passo 3 ganha linha — "Rota/modelo errado para o tipo de tarefa → `ROTAS.md`";
  (c) Passo 5 (poda) menciona rotas: rota sem uso em ~5 retros → candidata a remoção.
- Testes: n/a (doc de procedimento).
- Verificação: diff mostra os 3 enxertos; leitura completa do retro.md confirma que não
  contradiz os passos existentes.
- Depende de: U2, U3 (nomes de arquivo citados precisam existir).

## Pré-mortem
Se falhar, terá sido porque:
1. **Ninguém escreve o log** (disciplina, não automação). Mitigação: dever de log mora no
   `ROTAS.md`, o arquivo que o orquestrador acabou de ler para despachar; se após ~3 sessões o
   log estiver vazio com despachos ocorrendo → promover a hook (fase 2, fora de escopo aqui).
2. **Taxonomia fina demais, estatística nunca converge.** Mitigação: cap de 6 tipos escrito
   como regra no próprio `ROTAS.md`.
3. **Frontmatter fork/model não funciona na versão local do CLI.** Mitigação: U1 é spike
   barato e primeiro; fallback declarado (rota via Agent tool com `model` explícito).

## Fora de escopo
- Hooks de logging automático; dashboard/visualização do log.
- Alterar `lfg`/`slfg` para usar as rotas (fase 2, depois de estatística mínima existir).
- Roteamento sem orquestrador consciente (auto-invocação da `trabalhar-fork` fica desligada).
- Rotas para agentes pessoais de fora do kit (cavecrew etc.) — entram como `[AJUSTE]`.

## Deferido à execução — resolvido no teste real (2026-07-21, sessão 45ed8dec)
- Alias de modelo no frontmatter: PROVADO — `model: sonnet` resolveu para `claude-sonnet-5`
  (campo `model` no transcript do subagente).
- `${CLAUDE_SKILL_DIR}` em `context: fork`: PROVADO — substituída ANTES do corpo chegar ao
  fork, expandindo para o caminho do working tree (marketplace directory). O fork leu o
  protocolo pelo caminho da variável; o fallback relativo nunca foi exercitado e foi podado
  do corpo da skill. Nota: a substituição também reescreve o texto-guarda do fallback
  ("o texto literal `${CLAUDE_SKILL_DIR}` aparecer acima" vira o caminho expandido),
  tornando-o sem sentido — mais um motivo da poda.
- Envelope do fork: PROVADO íntegro — texto final do transcript do fork é byte a byte igual
  ao que o orquestrador recebeu.

## Done
- [x] U1: fork executou plano-brinquedo com envelope válido e modelo menor — primeiro via
      simulação equivalente (Agent tool); depois validado com a skill real
      `/composto:trabalhar-fork` em 2026-07-21 (sessão 45ed8dec, plugin 1.1.1): fork real,
      sonnet provado, envelope verbatim, cerca de tools ativa (linha 2 do despachos.jsonl).
- [x] `ROTAS.md` na raiz com ≤6 tipos, todos apontando para agentes existentes (litmus por
      `ls` na sessão de execução, reconfirmado pela lente de testes); ponteiro no CLAUDE.md.
- [x] `despachos.jsonl` com ≥1 linha real, `jq` parseia (JQ_OK).
- [x] `retro.md` com colheita/destino/poda cientes do log (3 enxertos conferidos na revisão).
- [x] Suite/typecheck: n/a (kit é markdown puro) — verificação foi o litmus de cada unidade.
