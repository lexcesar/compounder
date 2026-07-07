# composto — engenharia composta, versão 2

Sucessor espiritual do [compound-engineering-plugin](https://github.com/everyinc/compound-engineering-plugin)
da Every, redesenhado do zero por Claude Fable 5 para a realidade do Claude Code moderno e para rodar
bem em **Opus, Sonnet e Haiku**. Mesma filosofia — *cada unidade de trabalho deve tornar a próxima mais
fácil* — com outra engenharia por baixo.

## Instalação (local)

```
/plugin marketplace add /Users/alexander/Projetos/fable-5-start-project
/plugin install composto
```

(Ou publique o diretório num repositório GitHub e use `/plugin marketplace add usuario/repo`.)

## O que mudou em relação ao original — e por quê

| Original (CE) | composto | Por quê |
|---|---|---|
| Skills de 400–800 linhas com dezenas de modos, flags e menus | Skills de ~100 linhas, um caminho feliz, decisões no modelo | Modelo pequeno afoga em árvore de flags; instrução enxuta e concreta é o que Haiku/Sonnet executam bem |
| Gates do `/lfg` em prosa ("verifique o retorno estruturado") | Gates executados por um agente `verificador-adversarial` que tenta REFUTAR a evidência | Auto-atestado é o modo de falha nº 1 de pipeline autônomo; gate de verdade é adversarial |
| Orquestração descrita em texto, 0 agentes standalone (portabilidade multi-plataforma) | 6 agentes reais (`agents/`) + uso nativo de paralelismo do Claude Code | Alvo único (Claude Code) permite usar a plataforma de verdade em vez do mínimo denominador comum |
| `/slfg` removido | **`/slfg` ressuscitado** — enxame com fan-out de pesquisa, painel de revisores e verificação adversarial em paralelo; degrada com elegância quando só há a ferramenta de subagentes | Era a feature que valia o preço; a plataforma de hoje aguenta |
| Push/PR por padrão no autopilot | **Local por padrão** — commit local só se autorizado; push/PR só com `enviar:pr` ou ordem explícita | Autopilot que publica sozinho viola a regra reversível/irreversível (AUTONOMY.md) |
| `ce-compound` de 727 linhas, multi-agente para escrever um doc | `/compound` destila e ROTEIA: solução técnica → `docs/solutions/`; regra de projeto → CLAUDE.md; preferência → memória; vocabulário → CONCEPTS.md; efêmero → lixeira | O valor está na destilação e no endereço certo, não na cerimônia; captura cara = captura pulada |
| Sem mecanismo de apartes | **`/btw`** + hook de interceptação: fale no meio do trabalho sem descarrilar nada | Conversa durante execução é como humanos trabalham; formalizar o aparte destrava paralelismo real |
| Config YAML própria, modos headless por flag | Convenção sobre configuração: `docs/plans/`, `docs/solutions/`, `BTW.md`, `CONCEPTS.md`; headless = decisão de quem chama | Menos superfície para quebrar e menos tokens para carregar |

O que foi **preservado** do original, porque é excelente: o loop brainstorm → plano → trabalho →
simplificar → revisar → compound; a separação O QUÊ (requisitos) / COMO (plano); aprendizados como
artefatos buscáveis com frontmatter; `CONCEPTS.md` como vocabulário vivo; a regra de que pesquisa
se faz na fase que precisa dela e flui para a seguinte.

## Comandos

| Comando | Papel |
|---|---|
| `/brainstorm <ideia>` | Descobrir O QUÊ: perguntas certas → doc de requisitos |
| `/plano [requisitos\|descrição]` | Decidir COMO: reconhecimento real → plano com unidades verificáveis |
| `/trabalhar [plano]` | Executar com baseline, rastreio de tarefas e evidência por unidade |
| `/simplificar` | Passar a plaina no diff recém-escrito (preservando comportamento) |
| `/revisar [escopo]` | Painel de 4 revisores em paralelo + verificação adversarial dos achados |
| `/depurar <bug>` | Investigação de causa raiz (usa a skill `analise-profunda` do kit, se presente) |
| `/compound [contexto]` | Destilar aprendizados e gravar cada um no endereço certo; `refresh` para podar |
| `/lfg <feature>` | Pipeline inteiro, autônomo, com gates adversariais — entrega local |
| `/slfg <feature>` | O mesmo, em ENXAME: pesquisa, revisão e verificação em paralelo |
| `/btw <mensagem>` | Aparte no meio do trabalho: registrado, classificado, sem descarrilar |

Fluxo típico: `/brainstorm` → `/plano` → `/trabalhar` → `/simplificar` → `/revisar` → `/compound`.
Com pressa e confiança: `/lfg descrição da feature`. Com pressa, confiança e orçamento: `/slfg`.

## Integração com o kit de partida

Este plugin foi desenhado para conviver com o kit (`CLAUDE.md`, `AUTONOMY.md`, `/goal`, `/retro`,
`docs/mentor/`): quando esses arquivos existem, as skills os respeitam e citam (ex.: `/lfg` obedece
às zonas do AUTONOMY.md; `/compound` usa a tabela de roteamento do `/retro`). Sem o kit, o plugin
funciona sozinho com defaults seguros embutidos.

Linha recomendada no CLAUDE.md do projeto:

> Mensagens que chegarem enquanto trabalho: tratar pelo protocolo /btw — acusar em 1 linha,
> classificar (paralelizo agora / faço em seguida / registro em BTW.md), e só abandonar a tarefa
> corrente se a mensagem mandar parar explicitamente.

## Anatomia

```
composto/
├── .claude-plugin/plugin.json
├── skills/            # 10 skills enxutas (~100 linhas cada)
├── agents/            # pesquisador, 4 revisores, verificador-adversarial
├── hooks/hooks.json   # intercepta prompts "btw ..." e injeta o protocolo de aparte
└── scripts/btw-hook.sh
```
