---
description: Transforma um pedido em contrato de objetivo verificável (docs/goals/ATIVO.md)
argument-hint: [objetivo em linguagem natural] | status | done
---

# /goal — contrato de objetivo

Entrada do usuário: `$ARGUMENTS`

Um objetivo sem critério de aceite é um desejo. Este comando transforma desejo em contrato.
O contrato vive em `docs/goals/ATIVO.md` e é a âncora de TODAS as decisões até ser fechado.

## Se a entrada for vazia ou `status`
Leia `docs/goals/ATIVO.md`. Reporte: objetivo em 1 frase, critérios de aceite com estado
(✅ atingido com evidência / ⬜ pendente / ⚠️ em risco), próximo passo concreto. Se não existir
arquivo, diga que não há objetivo ativo e peça um.

## Se a entrada for `done`
1. Releia `docs/goals/ATIVO.md` e verifique CADA critério de aceite de verdade (rode o teste,
   abra o arquivo, execute o comando). Nada de marcar ✅ de memória.
2. Critério não atingido → reporte quais e pergunte: encerrar mesmo assim (registrando como
   "não atingido") ou continuar trabalhando?
3. Tudo atingido → mova o arquivo para `docs/goals/arquivo/AAAA-MM-DD-<slug>.md` (crie a pasta
   se preciso), acrescente seção final `## Resultado` com evidências, e sugira rodar `/retro`.

## Caso geral: a entrada é um objetivo novo
1. Se já existe `docs/goals/ATIVO.md` não arquivado, avise e pergunte: substituir ou arquivar antes.
2. Faça o reconhecimento MÍNIMO necessário para escrever critérios reais (olhe o código citado,
   confirme que os alvos existem). Não comece a implementar.
3. Se houver ambiguidade que muda o resultado, pergunte — no máximo 3 perguntas, todas de uma vez,
   cada uma com sua recomendação. Ambiguidade que não muda o resultado: assuma o razoável e declare.
4. Escreva `docs/goals/ATIVO.md` neste formato:

```markdown
# Objetivo: <1 frase, verbo no infinitivo, resultado observável>
Criado: <AAAA-MM-DD> | Pedido original: "<verbatim do usuário>"

## Por quê (valor)
<1–2 frases: que problema resolve, para quem>

## Critérios de aceite
<!-- Cada um CHECÁVEL: um comando que roda, um comportamento que se observa, um arquivo que existe.
     Proibido critério vago tipo "código limpo", "funcionar bem". -->
- [ ] <critério> — verificação: <como provar>
- [ ] <critério> — verificação: <como provar>

## Não-objetivos (fora de escopo desta rodada)
- <o que NÃO será feito, para conter deriva de escopo>

## Restrições
- <limites técnicos, de tempo, de compatibilidade>

## Suposições declaradas
- <o que foi assumido sem confirmação do usuário>

## Riscos conhecidos
- <risco> → <mitigação ou "aceito">
```

5. Mostre o contrato ao usuário em resumo (objetivo + critérios) e comece o trabalho.

## Regra permanente enquanto houver ATIVO.md
Antes de qualquer decisão significativa, pergunte-se: **"isto serve ao contrato?"**
Trabalho que não serve a nenhum critério de aceite nem é pré-requisito de um → não faça,
ou proponha como adição explícita ao contrato.
