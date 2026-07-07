# Kit de Partida: ensinando um modelo a trabalhar como um sênior

Este repositório é um **template de projeto em branco** cujo verdadeiro conteúdo não é código — é método.
Ele foi destilado por Claude Fable 5 para que modelos menores (Opus, Sonnet, Haiku) operem, dentro de um
projeto, com a disciplina de um engenheiro sênior: ler antes de escrever, verificar antes de afirmar,
decidir com critério, aprender com cada correção.

A premissa: **em tempo de execução, o único "treinamento" disponível é o contexto.** Um modelo menor com
regras concretas, checáveis e carregadas na hora certa supera um modelo maior operando no improviso.
Este kit é essas regras.

## Mapa do kit

| Caminho | O que é | Quem lê |
|---|---|---|
| `CLAUDE.md` | Contrato de operação do projeto (carregado toda sessão) | Modelo, sempre |
| `MEMORY.md` + `memory/` | Índice e arquivos de memória persistente | Modelo, início de sessão |
| `AUTONOMY.md` | Regras de autonomia e decisão (zonas verde/amarela/vermelha) | Modelo, ao decidir |
| `.claude/settings.json` | Guardrails duros (permissões de ferramentas) | Claude Code (mecânico) |
| `.claude/commands/goal.md` | `/goal` — transforma pedido em contrato verificável | Usuário invoca |
| `.claude/commands/retro.md` | `/retro` — colhe lições e grava regras novas | Usuário invoca |
| `.claude/commands/guardrails.md` | `/guardrails` — entrevista e gera limites sob medida | Usuário invoca |
| `.claude/commands/handoff.md` | `/handoff` — documento de passagem entre sessões | Usuário invoca |
| `.claude/skills/analise-profunda/` | Skill de investigação metódica de bugs | Modelo, quando investiga |
| `.claude/agents/` | Subagentes: explorador, revisor-crítico, verificador | Modelo delega |
| `docs/mentor/` | Os 12 guias de método (a "sabedoria" propriamente dita) | Modelo, sob demanda |
| `avatares/` | O Conselho — 15 avatares para decisões de vida, projeto e negócio | Humanos e modelo (`/conselho`) |
| `docs/templates/` | Templates de plano, análise, ADR, handoff | Ambos |
| `docs/goals/` | Contratos de objetivo (`ATIVO.md` gerado por `/goal`) | Ambos |

## Os 12 guias (`docs/mentor/`)

| Guia | Ensina |
|---|---|
| `00-principios.md` | As 14 leis que separam comportamento sênior de júnior |
| `01-anatomia-do-claude-md.md` | Como escrever e manter um CLAUDE.md que vale o que custa |
| `02-memoria-viva.md` | O que gravar, o que não gravar, como manter memória limpa |
| `03-autonomia-e-decisoes.md` | O raciocínio por trás do AUTONOMY.md, com casos reais |
| `04-planejamento.md` | Como planejar de verdade (contra a realidade, não contra a memória) |
| `05-analise-profunda.md` | Investigação: hipóteses, evidência, bisseção, quando parar |
| `06-delegacao-e-subagentes.md` | Briefing, paralelismo, verificação de resultados de agentes |
| `07-retroalimentacao-e-evolucao.md` | Como cada correção vira regra e como skills evoluem |
| `08-guardrails-e-boundaries.md` | Como ajudar o usuário a construir limites em camadas |
| `09-testes-e-mudancas.md` | Disciplina de teste, menor diff honesto, como propor mudanças |
| `10-contexto-e-comunicacao.md` | Economia de contexto e como reportar como um sênior |
| `11-sistemas-de-convencoes.md` | Como construir sistemas de convenções que compõem (destilado do opten-conventions de Alexander) |

## Como adotar

**Projeto novo:** copie o kit inteiro para o diretório do projeto e preencha os blocos `[AJUSTE: ...]`
do `CLAUDE.md`. Crie `src/`, `tests/`, `scripts/` conforme a stack (o kit é agnóstico de linguagem
de propósito: a estrutura de código vem da stack; a estrutura de método vem daqui).

**Projeto existente:** copie `.claude/`, `AUTONOMY.md`, `docs/mentor/`, `docs/templates/`, `MEMORY.md`
e `memory/`. Funda o `CLAUDE.md` daqui com o que já existe — mantendo o resultado curto
(veja `docs/mentor/01-anatomia-do-claude-md.md`).

**Primeira sessão (ritual):**
1. `/guardrails` — 5 minutos de entrevista; gera limites sob medida.
2. `/goal <o que você quer>` — nasce o contrato `docs/goals/ATIVO.md`.
3. Trabalhe normalmente.
4. `/retro` ao fechar — as lições viram regras gravadas.

## O volante de aprendizado

```
        trabalhar
       ↗         ↘
 regras            correções
 melhores          do usuário
       ↖         ↙
        /retro grava
```

Cada volta do ciclo torna a próxima sessão melhor que a anterior. Um modelo que roda este ciclo por
20 sessões acumula o que nenhum prompt inicial poderia conter. **O kit não deixa o modelo mais
inteligente; deixa a inteligência dele apontada para o lugar certo — e composta ao longo do tempo.**

## Plugin `composto/` — a pipeline de engenharia composta

Além do kit (método base), este repositório carrega o plugin **composto** — sucessor do
compound-engineering-plugin da Every, redesenhado para Claude Code moderno e para Opus/Sonnet/Haiku:
`/brainstorm → /plano → /trabalhar → /simplificar → /revisar → /compound`, com `/lfg` (autopilot),
`/slfg` (enxame) e `/btw` (apartes sem descarrilar). Instalação e comparação com o original:
`composto/README.md`.

Divisão de papéis: o **kit** ensina COMO PENSAR (princípios, autonomia, memória); o **plugin**
dá o TRILHO DE EXECUÇÃO (pipeline com gates). Eles se referenciam, mas cada um funciona sozinho.

## Princípio de manutenção

Todo arquivo deste kit é um organismo vivo: se uma regra nunca muda um comportamento, ela morre
(delete); se um erro se repete, nasce uma regra (grave). O `/retro` é o coração que bombeia isso.
