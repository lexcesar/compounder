# 05 — Análise profunda: investigação que chega à causa

O protocolo operacional está na skill (`.claude/skills/analise-profunda/SKILL.md`); este guia é o
fundamento — por que cada passo existe e as táticas por situação. Saída padrão:
`docs/templates/analise.md`.

## As três leis da investigação

**1. Evidência antes de teoria.** O erro nº 1 é reconhecer um padrão ("isso parece aquele bug de
cache") e sair "corrigindo". Padrões geram HIPÓTESES, nunca conclusões. A conclusão exige evidência
LOCAL: deste código, desta execução, desta sessão. O modelo que pula essa etapa conserta o bug que
lembra, não o que existe.

**2. Uma mudança por vez.** Cada teste de hipótese muda UMA coisa e observa. Mudou três coisas e
funcionou? Você não sabe qual foi — e provavelmente introduziu duas mudanças supersticiosas que
alguém vai ter medo de remover para sempre. (Corolário: investigação não é hora de consertar nada
"de passagem" — cada mudança contamina a cena do crime.)

**3. O espaço se corta pela metade.** Investigação eficiente é busca binária, não varredura linear.
Cada verificação deveria eliminar ~metade do espaço restante. Se você está lendo arquivo por
arquivo "para ver se acha algo", não está investigando — está passeando.

## Táticas de bisseção, por eixo
- **Por camada:** o dado está certo na saída do banco? → metade eliminada. Na resposta da API? →
  outra metade. Fronteiras típicas: banco → repositório → domínio → serialização → rede → cliente.
- **Por tempo:** funcionava no commit X? `git bisect` (real ou mental sobre o `git log` da área
  tocada). Bug novo em código velho = mudança recente em código, dependência, config ou DADO.
- **Por dado:** qual é a MENOR entrada que ainda reproduz? Corte campos, linhas, flags até o bug
  sumir — o último pedaço removido aponta a causa. O caso mínimo também vira o teste de regressão.
- **Por ambiente:** só em produção? A diferença (env vars, versão, dados reais, concorrência,
  timezone) é a lista de suspeitos — enumere-a explicitamente em vez de "deve ser o ambiente".

## Hipóteses: o mecanismo anti-ancoragem
Escreva ≥ 2 ANTES de investigar a primeira (lei 7 dos princípios). O ponto sutil: defina o teste
discriminante ANTES de rodá-lo — "se H1, verei X; se H2, verei Y". Quem define o esperado depois
de ver o resultado sempre acha que o resultado confirma o que já pensava (é o p-hacking da
depuração). Hipótese morta é PROGRESSO: registre o que a falha provou e risque-a — espaço menor.

## A contabilidade de evidência
Três listas separadas, sempre:
- **Fatos** — com fonte: `comando → saída`, `arquivo:linha`. Imutáveis.
- **Inferências** — "de F1+F3 concluo que...". Válidas enquanto os fatos as sustentam.
- **Suposições** — o que você está assumindo SEM ter olhado ("presumo que o cron roda").
A lista de suposições é a mais valiosa: quando a investigação empaca, a causa está quase sempre
escondida numa suposição não testada. Empacou? Promova a suposição mais antiga a hipótese e teste-a.

## Sintoma → causa: o "por quê" em cadeia
`NullPointerException na linha 80` → por que nulo? → o repositório devolveu vazio → por quê? →
a query filtra por tenant e o tenant vai vazio → por quê? → o middleware não popula tenant em
requisições de webhook → **causa**: decisão de design que não previu webhooks. Pare no primário
(decisão/config/premissa). Consertar na linha 80 (`if null return`) esconderia o defeito real e o
deixaria livre para aparecer nos outros 12 lugares que dependem do tenant.

## Quando parar
- **Achou:** o teste discriminante confirmou e, idealmente, o caso mínimo reproduz → a correção o
  faz passar → a suite inteira continua verde. Entregue com confiança rotulada: "alta — reproduzi,
  corrigi, regressão coberta" vs "média — evidência aponta X, mas não consegui reproduzir
  localmente; validaria com Y".
- **Não achou (3 hipóteses mortas / orçamento estourado):** entregue a contabilidade de evidência,
  hipóteses testadas e mortas, suspeita ranqueada e o próximo teste que você faria. Isso vale MUITO:
  o próximo investigador (ou você amanhã) começa de onde você parou, não do zero. Flailing
  disfarçado de persistência — tentar coisas aleatórias por mais uma hora — vale menos que nada.

## Anti-padrões
| Anti-padrão | O que parece | O que é |
|---|---|---|
| Depuração-espingarda | "Vou mudando coisas até passar" | Destrói evidência; gera correção supersticiosa |
| Ancoragem | "Só pode ser o cache" | Uma hipótese virando conclusão sem discriminante |
| Correção-no-sintoma | `if (x != null)` onde estourou | Esconde a causa; espalha o defeito |
| Confiança-por-analogia | "Já vi esse erro, é sempre X" | Padrão sem evidência local |
| Log-cegueira | Ler só a última linha do erro | A primeira falha do log é a que importa |
| Investigação-passeio | Ler arquivos "para se familiarizar" | Nenhuma verificação corta o espaço |
