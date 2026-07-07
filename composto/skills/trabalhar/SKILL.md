---
name: trabalhar
description: Executar um plano com baseline, rastreio por unidade e evidência real. Use para implementar planos de docs/plans/ ou pedidos de build claros.
argument-hint: "[caminho do plano | descrição] [modo:retornar]"
---

# /trabalhar — execução com evidência

Entrada: `$ARGUMENTS` (token `modo:retornar` = chamado por pipeline: sem menus, sem cauda de
entrega, termina no envelope estruturado).

## Passo 0 — Triagem
- Caminho de plano → leia frontmatter: `etapa: plano-pronto` → siga. `etapa: requisitos` → pare:
  "isto precisa de `/plano` antes" (em pipeline, retorne esse erro).
- Vazio → pegue o plano-pronto mais recente de `docs/plans/` e CONFIRME com o usuário.
- Descrição solta → escopo pequeno e claro: plano-de-5-linhas no chat e execute; grande/nebuloso:
  recomende `/brainstorm` ou `/plano` (o usuário decide).

## Passo 1 — Preparação (nunca pule)
1. **Baseline:** descubra os comandos do projeto (CLAUDE.md → package.json/Makefile; nunca
   adivinhe) e RODE a suite da área + typecheck. Registre: "baseline: X/Y, falhas pré-existentes: ...".
2. **Branch:** na default e commits autorizados → crie branch com nome significativo. Commits não
   autorizados → trabalhe no working tree e diga isso.
3. **Rastreio:** crie uma tarefa (TaskCreate; sem a ferramenta, checklist no chat) por unidade U1..Un.
4. Leia do plano: "Deferido à execução" (suas perguntas a resolver) e "Fora de escopo" (sua cerca).

## Passo 2 — Loop por unidade (U1 → Un, ordem do plano)
Para cada unidade: marque em andamento → releia a seção U<N> → implemente o MENOR diff honesto
seguindo o dialeto local → cenários de teste da unidade viram testes reais (novo comportamento:
veja o teste FALHAR antes da implementação quando o custo permitir) → rode a VERIFICAÇÃO da
unidade (a do plano) → passou: marque concluída com evidência em 1 linha; narre no chat
("U2 ✅ — 3 arquivos, teste X verde").
- **Plano não bate com a realidade** (arquivo mudou, premissa caiu): desvio pequeno → anote na
  sua nota de execução e siga; desvio ESTRUTURAL → pare a unidade e reporte "plano previa X,
  realidade é Y, proponho Z" (em pipeline: registre e escolha o razoável se reversível; senão pare).
- **Falha 2× igual → hipótese nova.** 3 hipóteses mortas na mesma unidade → unidade vira BLOQUEIO
  no envelope; siga para a próxima unidade independente, se houver.
- **NUNCA:** editar o plano como se fosse estado; deletar/pular teste para passar; "aproveitar"
  para refatorar fora do escopo (anote como resíduo).

## Passo 3 — Verificação final
Suite INTEIRA + typecheck/lint + build (se existir). Compare com o baseline: regressão SUA →
conserte antes de reportar. Limpe a cena: debug prints, imports órfãos, arquivos de rascunho.

## Passo 4 — Envelope de retorno (obrigatório, os dois modos)
```
STATUS: completo | parcial | bloqueado
Unidades: U1 ✅ <evidência 1 linha> | U2 ✅ ... | U3 ❌ <bloqueio: o que cada tentativa provou>
Arquivos: <lista> (~N linhas)
Suite: baseline X/Y → agora X'/Y' | typecheck: <estado>
Não testado: <o quê + por quê + risco> | Resíduos/anotações: <...>
Desvios do plano: <ou "nenhum">
```
Modo normal: envelope + "próximo: `/simplificar` e `/revisar`". `modo:retornar`: envelope e PARE
(sem commit, sem menu — a cauda é de quem chamou).
Regra de honestidade acima de tudo: STATUS `completo` exige toda unidade com verificação executada
NESTA sessão. Parcial bem reportado > completo falso — sem exceção.
