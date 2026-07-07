# 01 — Anatomia do CLAUDE.md ideal

## A economia fundamental
O CLAUDE.md é carregado em TODAS as sessões, para sempre. Cada linha paga aluguel de contexto
eternamente — e contexto gasto com instrução é contexto que falta para raciocínio. Disso segue tudo:

> **Uma linha só entra no CLAUDE.md se sua remoção piorar algum comportamento observável.**

Não é "informação útil sobre o projeto". É "instrução que muda ação". A diferença mata ou salva
o arquivo: "usamos PostgreSQL" não muda ação nenhuma (o modelo vê no docker-compose); "datas sempre
em UTC no banco; conversão só na borda" muda ações todos os dias.

## As seções, em ordem de valor por token

1. **Comandos** — o conteúdo de maior valor por token que existe. Um comando de teste errado
   desperdiça minutos por sessão; um certo economiza a descoberta toda vez. Inclua: testes (suite
   e arquivo único), lint/typecheck, build, rodar local. E a meta-regra: "nunca adivinhe; confirme
   na fonte" — porque comandos mudam e o CLAUDE.md fica velho.

2. **Invariantes** — as regras absolutas ("nunca X"). Poucas e realmente absolutas: um bloco de 20
   invariantes ensina o modelo a ignorar o bloco inteiro (se tudo é crítico, nada é). Máximo ~7,
   cada uma testável: "nunca editar migration mesclada" (checável) e não "cuidado com migrations" (vago).

3. **Mapa arquitetural em 30 segundos** — onde mora o quê e o fluxo típico de uma requisição/ação.
   NÃO é documentação de arquitetura: é o mínimo para o modelo abrir o arquivo certo na primeira
   tentativa em vez de na quarta.

4. **Convenções não-inferíveis** — só o que a leitura do código NÃO revela. "Usamos aspas simples"
   é inferível (e o linter já cuida); "o serviço X é gerado, edite o template em Y" não é.

5. **Ponteiros condicionais** — a técnica que resolve o dilema "quero dar muito contexto mas não
   posso pagar por ele": tabela `situação → leia tal arquivo`. O conhecimento profundo fica em
   `docs/`, custa zero por padrão, e carrega exatamente quando é relevante. É assim que este kit
   inteiro funciona (divulgação progressiva).

6. **Ciclo de trabalho** — uma linha com o loop esperado (entender → planejar → agir → verificar →
   reportar → aprender). Âncora barata que reduz os dois erros de fluxo mais comuns: agir sem
   entender e reportar sem verificar.

## Anti-padrões (cada um visto na natureza)

| Anti-padrão | Por que mata | Correção |
|---|---|---|
| Espelhar o que o código diz | Paga aluguel por informação grátis; e desatualiza | Delete; o modelo lê o código |
| Regra vaga ("escreva código limpo") | Não muda nenhuma decisão concreta | Torne testável ou delete |
| Essay de arquitetura (3 páginas) | Custa caro toda sessão; ninguém carrega 3 páginas na cabeça | Mapa de 6 linhas + ponteiro para docs/ |
| Changelog/histórico do projeto | História não é instrução | git log já existe |
| Tutorial de ferramenta pública ("como usar git") | O modelo sabe; treino cobriu | Delete |
| Regra morta (referencia coisa removida) | Pior que inútil: ensina que o arquivo mente | Poda via `/retro` |
| Tom implorativo ("POR FAVOR SEMPRE LEMBRE!!") | Ênfase inflacionada = tudo vira ruído | Imperativo seco; a força vem da clareza |

## Teste de qualidade do arquivo inteiro
1. **Teste da linha:** para cada linha — "se eu apagar, que comportamento piora?" Sem resposta → apague.
2. **Teste do tamanho:** passou de ~120 linhas → algo está no lugar errado (provavelmente devia ser
   ponteiro para docs/).
3. **Teste do recém-chegado:** um modelo competente que só leu este arquivo faz a primeira tarefa
   sem tropeçar em pegadinha conhecida? Se há pegadinha não coberta que JÁ causou retrabalho, falta linha.
4. **Teste da poeira:** alguma linha referencia arquivo/comando/pasta que não existe mais? O arquivo
   perdeu credibilidade inteiro — poda já.

## Manutenção: o arquivo é vivo
O CLAUDE.md ideal no dia 1 é razoável; no dia 90, afiado — SE o `/retro` alimentá-lo. Fluxo:
correção do usuário → regra destilada → "vale para o projeto inteiro e é estável?" → entra
(respeitando o teste da linha). E na direção inversa: regra que nunca dispara → sai. O tamanho
deve oscilar em torno do mesmo ponto; só crescer é sintoma de acúmulo, não de aprendizado.
