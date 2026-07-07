---
description: Gera documento de passagem para a próxima sessão (estado real, próximos passos, armadilhas)
argument-hint: [opcional - contexto extra para a passagem]
---

# /handoff — passagem de bastão

Contexto extra do usuário (se houver): `$ARGUMENTS`

A próxima sessão (você mesmo, amanhã, com contexto zerado) só saberá o que este documento disser.
Escreva para um colega competente que não viu NADA desta conversa. Use o template
`docs/templates/handoff.md` e grave em `docs/handoffs/AAAA-MM-DD-HHMM.md` (crie a pasta se preciso).

Regras de qualidade — o que separa um handoff útil de um inútil:
1. **Estado é o que É, não o que deveria ser.** "Testes: 47/49 passando; os 2 que falham são
   pré-existentes (nomes + evidência)" — nunca "testes ok".
2. **Feito só com evidência.** Cada item concluído cita a prova (comando rodado, arquivo, saída).
   Item sem prova vai para "em andamento", não para "feito".
3. **Próximo passo é executável em 1 minuto.** "Continuar a refatoração" é inútil.
   "Rodar `pnpm test src/billing` e corrigir o mock de relógio em `tests/helpers.ts:34`" é útil.
4. **Armadilhas valem ouro.** Tudo que custou tempo para descobrir e não está escrito em lugar
   nenhum: comando que precisa de env var, ordem de inicialização, teste flaky, API enganosa.
5. **Decisões pendentes com contexto completo** (formato do AUTONOMY.md §bloqueio): opções,
   consequências, sua recomendação — para o usuário decidir sem reconstruir a discussão.
6. **Não copie conteúdo de arquivos** — aponte `caminho:linha`. O documento é mapa, não mala.

Depois de gravar: mostre ao usuário o caminho do arquivo e um resumo de 3 linhas.
Se houver `docs/goals/ATIVO.md`, atualize o estado dos critérios nele também.
