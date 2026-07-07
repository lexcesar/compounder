# 02 — Memória viva

## O modelo mental
Você acorda amnésico toda sessão. A memória (`MEMORY.md` + `memory/`) é a carta que o você-de-ontem
deixou para o você-de-hoje. Duas implicações:
1. Escreva para quem não viu a conversa — sem contexto implícito, sem "o problema de hoje".
2. A carta compete com todo o resto pelo seu tempo de leitura — cada memória inútil dilui as úteis.

Arquitetura: `MEMORY.md` é o ÍNDICE (uma linha por memória; carregado/lido no início da sessão);
`memory/*.md` são os fatos (um arquivo = um fato; aberto só quando relevante). Nunca inverta:
conteúdo no índice incha o custo fixo de toda sessão.

## Formato do arquivo de memória
```markdown
---
name: slug-curto-em-kebab
description: uma frase — usada para decidir relevância sem abrir o arquivo
metadata:
  type: user | feedback | project | reference
---

O fato, em 1–5 linhas, datas absolutas.

**Por quê:** o que aconteceu que gerou esta memória (a evidência).
**Como aplicar:** a mudança de comportamento concreta.
```
A `description` é o campo mais importante: é por ela que o você-futuro decide abrir ou não.
Descrição vaga = memória invisível.

## Os quatro tipos e a régua de cada um
- **user** — quem é o usuário: papel, expertise, preferências de comunicação e decisão.
  Régua: ajudaria a calibrar QUALQUER resposta futura? ("prefere diffs a explicações longas").
- **feedback** — correções e confirmações sobre COMO trabalhar. O tipo mais valioso. Sempre com
  **Por quê** e **Como aplicar**. Grave a regra destilada, não o incidente
  (ver `docs/mentor/07-retroalimentacao-e-evolucao.md`).
- **project** — estado e decisões do projeto que NÃO estão derramados no código/git: objetivos de
  longo prazo, restrições combinadas verbalmente, quem decide o quê.
- **reference** — ponteiros externos: URLs de dashboards, tickets, docs internas. Só o ponteiro
  e quando foi visto; conteúdo externo muda.

## O que NUNCA gravar
- **O que o repositório já registra** — estrutura de código, correções feitas (git log), conteúdo
  de CLAUDE.md. Memória duplicada DESATUALIZA e passa a mentir.
- **Efêmero da tarefa** — "o teste X está falhando hoje". Amanhã é mentira; é assunto de
  `/handoff`, não de memória.
- **Segredos** — nunca, em nenhuma forma.
- **Trivialidades** — "usuário disse oi em português". A tentação de gravar muito é o modo de
  falha nº 1: memória é sinal, e sinal se define pelo que se recusa a incluir.

## Disciplina de escrita (nesta ordem, sempre)
1. **Procure antes de criar.** Já existe memória sobre o assunto? ATUALIZE-a (e sua description).
   Duplicata é pior que ausência: duas versões divergem e você não sabe em qual crer.
2. **Datas absolutas.** "Semana passada" apodrece; "2026-07-06" não.
3. **Linke relacionadas** com `[[slug]]` — teia recupera melhor que lista.
4. **Indexe.** Arquivo sem linha no `MEMORY.md` não existe.

## Disciplina de leitura
- Início de sessão: leia o ÍNDICE; abra só as memórias cuja description toca a tarefa.
- Memória recuperada é hipótese, não fato atual: registra o que era verdade QUANDO ESCRITA.
  Se ela aponta comando/arquivo/decisão, confirme que ainda existe antes de agir em cima.

## Morte de memória (tão importante quanto nascimento)
Delete (arquivo + linha do índice) quando: a memória se provou errada; o feedback foi substituído
por outro mais novo; o que ela aponta não existe mais. Na dúvida entre podar e manter uma memória
suspeita: verifique-a agora ou delete — manter "por via das dúvidas" é como nascem os índices de
40 linhas onde ninguém acha nada.

## Exemplo — ruim vs. bom
❌ `memory/bug-de-hoje.md`: "Corrigi o bug do parser adicionando trim() na linha 42."
(Efêmero, já registrado no git, sem regra geral.)

✅ `memory/feedback-parser-entradas-reais.md`, type feedback:
"Entradas do parser vêm de planilhas de clientes: espaços, BOM e encoding misto são o caso NORMAL,
não a exceção. **Por quê:** 2026-07-06, correção aceita só depois de cobrir esses casos; a primeira
versão 'limpa' foi rejeitada. **Como aplicar:** ao tocar parsing/validação neste projeto, testar
com amostra real de `fixtures/` antes de declarar pronto."
