---
name: compound
description: Capturar o aprendizado da sessão e gravar cada lição no endereço certo (docs/solutions/, CLAUDE.md, memória, CONCEPTS.md). Use após resolver algo que custou tempo. Modo refresh para podar o acervo.
argument-hint: "[contexto do aprendizado | refresh]"
---

# /compound — juros sobre conhecimento

Entrada: `$ARGUMENTS`

A tese do composto: a primeira solução custa investigação; documentada NO ENDEREÇO CERTO, a
próxima ocorrência custa minutos. O erro clássico é capturar caro (cerimônia → captura pulada)
ou capturar tudo (ruído → acervo ilegível). Esta skill destila e roteia. Barata o bastante para
rodar SEMPRE que algo custou tempo.

## Modo `refresh` (entrada = "refresh")
Varra `docs/solutions/**/*.md`: para cada doc, os caminhos/símbolos citados ainda existem
(grep rápido)? A solução ainda é como o projeto faz? → Proponha por doc: manter / atualizar
(diff) / aposentar (mover para `docs/solutions/arquivo/` com nota de motivo). Aplique após ok.
Acervo que mente é pior que acervo vazio. Fim.

## Passo 1 — Colheita (com `$ARGUMENTS` como pista; senão, varra a sessão)
O que nesta sessão: custou > 15 min para descobrir? surpreendeu (o sistema não era como parecia)?
foi correção do usuário? vai reincidir se não for escrito? Liste candidatos em 1 linha cada.
Nada qualificado → diga isso e encerre. Compound vazio não inventa lição.

## Passo 2 — Régua de valor (por candidato)
Grave SÓ se: (a) economizará tempo real numa ocorrência futura plausível E (b) não está derivável
do código/git E (c) você consegue escrever "quando X, faça Y porque Z". Falhou qualquer um → lixeira.

## Passo 3 — Roteamento (um endereço por lição)
| A lição é... | Endereço | Forma |
|---|---|---|
| Solução técnica reutilizável (bug resolvido, pegadinha de lib, padrão que funcionou) | `docs/solutions/<categoria>/<slug>.md` | Doc de solução (abaixo) |
| Regra estável do projeto ("nunca X aqui") | `CLAUDE.md` | 1 linha, teste-da-linha: só entra se mudar comportamento |
| Preferência/estilo do usuário | Memória (`memory/` + índice) | Regra destilada + Por quê + Como aplicar |
| Termo de domínio com significado local | `CONCEPTS.md` (crie se não existir) | Termo + definição em 1–3 frases |
| Procedimento repetível multi-passo | Patch em skill/comando existente, ou proposta de novo | Diff proposto |
Categorias de solutions: `bugs/`, `integracao/`, `performance/`, `convencoes/`, `infra/` (crie
sob demanda; não crie taxonomia vazia).

## Passo 4 — Anti-duplicata (antes de escrever)
Grep em `docs/solutions/` por termos da lição. Já existe doc do assunto → ATUALIZE-o (e anote
`atualizado: AAAA-MM-DD`). Duplicata diverge e passa a mentir.

## Doc de solução (formato fixo, ~20 linhas — cabe na cabeça de quem busca)
```markdown
---
titulo: <1 frase orientada a sintoma — como alguém procuraria isto>
data: AAAA-MM-DD
categoria: bugs|integracao|performance|convencoes|infra
tags: [<módulo>, <lib>, <sintoma>]
---
## Sintoma
<o que se observa — cole o erro literal se houver (é o que o futuro vai grepar)>
## Causa
<a causa primária, 2–4 linhas>
## Solução
<o que resolve, com arquivo:linha ou comando>
## Prevenção
<teste/guardrail/regra que evita reincidência — ou "nenhuma viável">
## Referências
<commits, PRs, links, docs relacionados>
```

## Passo 5 — Fechar o ciclo
1. Mostre: lição → endereço → texto proposto. Aplique o aprovado (regras que restringem só a
   você: aplique direto e anuncie).
2. O composto só compõe se for LIDO: confirme que os consumidores existem — `/brainstorm`,
   `/plano` e `/depurar` deste plugin já grepam `docs/solutions/` e `CONCEPTS.md`. Se o CLAUDE.md
   do projeto ainda não menciona `docs/solutions/`, proponha a linha de descoberta:
   "Antes de investigar erro ou planejar em área nova: grep em `docs/solutions/` (acervo de
   soluções) e veja `CONCEPTS.md` (vocabulário)."
3. Reincidência de lição já gravada que NÃO foi consultada → o problema é descoberta, não
   conteúdo: melhore `titulo`/`tags` (orientados a sintoma) em vez de escrever outro doc.
