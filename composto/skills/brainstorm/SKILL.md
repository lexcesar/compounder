---
name: brainstorm
description: Descobrir O QUÊ construir — perguntas certas em uma rodada, saída em doc de requisitos. Use antes de planejar features com escopo ou valor ainda nebulosos.
argument-hint: "[ideia ou problema em linguagem natural]"
---

# /brainstorm — o QUÊ, antes do COMO

Entrada: `$ARGUMENTS`

Objetivo: transformar uma ideia vaga em requisitos que um planejador executa sem adivinhar.
NÃO decida arquitetura nem arquivos aqui — isso é do `/plano`.

## Passo 0 — Vale a pena?
Pedido já pequeno e claro (1 comportamento, aceite óbvio)? Diga: "isto não precisa de brainstorm;
vou direto ao /plano" — e ofereça isso. Brainstorm de trivialidade é cerimônia, e cerimônia mata
o hábito de usar o funil quando ele importa.

## Passo 1 — Fundamento antes das perguntas (barato, obrigatório)
1. Olhe o repositório na área da ideia (ou despache 1 `pesquisador` se for amplo): o que já
   existe? algo parecido já foi feito/tentado?
2. Grep rápido em `docs/solutions/` e `docs/plans/` por termos da ideia; leia `CONCEPTS.md` se existir.
Perguntar o que o repo responde queima a paciência do usuário — cada pergunta sua deve ser algo
que SÓ ele sabe.

## Passo 2 — UMA rodada de perguntas (máx. 5)
Use a ferramenta de pergunta bloqueante (AskUserQuestion; sem ela, lista numerada no chat).
Todas de uma vez, cada uma com sua recomendação. Escolha as 5 com maior chance de mudar o design:
1. **Problema real:** que dor dispara isto? O que acontece hoje sem a feature?
2. **Usuário e frequência:** quem usa, quantas vezes, com que urgência?
3. **Sucesso:** como saberemos que funcionou (números, comportamento observável)?
4. **Não-objetivos:** o que estaria FORA mesmo parecendo relacionado?
5. **Restrições:** prazo, compatibilidade, dados sensíveis, o que não pode quebrar?
Respostas que contradizem o que você viu no repo → aponte a contradição AGORA (é o momento barato).

## Passo 3 — Escreva o doc de requisitos
`docs/plans/AAAA-MM-DD-<slug>-plano.md` (um artefato por feature; o `/plano` enriquece ESTE arquivo):
```markdown
---
etapa: requisitos
criado: AAAA-MM-DD
---
# <Feature em 1 frase>

## Problema
<a dor, com o que você viu no repo + o que o usuário respondeu>

## Comportamento desejado
- R1: <requisito observável, testável>
- R2: ...

## Critérios de sucesso
- <checável — número ou comportamento>

## Não-objetivos
- <explícitos — a cerca da deriva>

## Restrições e riscos conhecidos
- <...>

## Casos-limite levantados
- <vazio/nulo, concorrência, permissões, volumes — os que importam AQUI>

## Questões em aberto (para o plano ou para o usuário)
- <o que ficou sem resposta, e quem responde>
```
Requisito bom = alguém escreve um teste a partir dele. "Deve ser rápido" não é requisito;
"p95 < 300ms na busca" é.

## Passo 4 — Handoff
Mostre o resumo (problema + R's + não-objetivos) e encerre com:
"Requisitos em `<caminho>`. Próximo passo: `/plano <caminho>` — ou me diga o que ajustar."
