---
name: simplificar
description: Passar a plaina no código recém-escrito preservando comportamento — YAGNI, duplicação, abstração prematura. Use entre implementar e revisar, ou sobre área que vive emperrando mudanças.
argument-hint: "[escopo: vazio = diff do branch | caminho específico]"
---

# /simplificar — a plaina

Entrada: `$ARGUMENTS`

Código recém-escrito carrega andaimes: generalidade especulativa, camadas que não pagaram o
ingresso, nomes de primeira tentativa. Esta skill remove andaime SEM mudar comportamento — roda
entre `/trabalhar` e `/revisar` para que a revisão julgue o código já limpo.

## Pré-condição dura
Rode a suite do escopo ANTES. Vermelha → PARE e reporte: simplificar sobre base quebrada mistura
"quebrei agora" com "já estava quebrado" e ninguém mais separa. (Falha pré-existente documentada
no baseline do `/trabalhar` → ok, prossiga excluindo-a do critério.)

## Escopo
Vazio → diff do branch vs default + working tree. Caminho → o que foi pedido, MAS só simplifique
o que a mudança recente tocou ou o que o usuário nomeou — plaina em código alheio estável é risco
sem mandato.

## Alvos, em ordem de valor
1. **Especulação (YAGNI):** parâmetro que só recebe um valor, branch que nunca executa, config
   para necessidade imaginada, hook "para o futuro". Corte.
2. **Abstração de uso único:** interface com 1 implementação, wrapper que só repassa, helper de
   3 linhas chamado 1 vez. Inline.
3. **Duplicação nova:** o diff reinventou utilitário que o projeto já tem → use o existente.
   (Duplicação 2× ainda é barata; regra de três: abstraia na 3ª ocorrência, não na 1ª.)
4. **Nomes de primeira tentativa:** renomeie para o que a coisa É agora (escopo local do diff).
5. **Código morto do diff:** import órfão, variável não lida, comentário que narra o óbvio.
6. **Profundidade gratuita:** aninhamento que early-return resolve; condição negativa dupla.

## Proibições
- Mudar comportamento (qualquer "já que estou aqui, conserto" → anote como resíduo, não faça).
- Reformatar o que não foi tocado.
- Abstrair "para ficar elegante" — a plaina REMOVE camada, não adiciona.
- Encostar em teste para acomodá-lo: teste que quebrou = comportamento mudou = reverta a
  simplificação (a exceção: teste acoplado a detalhe de implementação que o inline eliminou —
  ajuste o teste e DIGA isso no relatório).

## Pós-condição dura
Suite + typecheck do escopo DEPOIS, verdes iguais ao antes. Qualquer regressão → reverta a
simplificação culpada (bisseque se preciso) antes de reportar.

## Relatório
```
Simplificação: <N linhas removidas, N adicionadas> em <N arquivos>
- <alvo>: <o que saiu e por quê, 1 linha cada>
Comportamento: preservado — suite <X/Y> antes e depois | typecheck limpo
Resíduos anotados (não tocados): <melhorias que exigiriam mudança de comportamento, ou "nenhum">
```
Nada a simplificar? Diga isso em 2 linhas — plaina sem serviço é bom sinal, não fracasso.
