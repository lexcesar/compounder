# 06 — Delegação e subagentes: orquestrar sem perder o controle

## Por que delegar (as três razões válidas)
1. **Economia de contexto** — a razão dominante. Uma varredura de 40 arquivos custaria seu
   raciocínio inteiro; o subagente queima o contexto DELE e te devolve 20 linhas de conclusão.
   Você fica com o mapa, não com os arquivos.
2. **Paralelismo** — N investigações independentes ao mesmo tempo.
3. **Olhos frescos / papel adversarial** — um revisor sem o seu apego à sua própria solução
   encontra o que você não quer ver.

## Quando NÃO delegar
- Lookup único em local conhecido ("qual o tipo do campo X em models.py") — mais rápido você mesmo.
- Tarefa que exige o contexto acumulado da sessão inteira (o agente nasce sem ele).
- Tarefa cuja verificação custa mais que a execução — se para confiar no resultado você teria que
  refazê-lo, delegar foi teatro.
- E o inverso do teatro: **delegou → não refaça.** Duplicar trabalho delegado paga duas vezes.
  Espere, então verifique por amostragem (abaixo).

## A lei do briefing: o agente nasce amnésico
O erro nº 1 da delegação, disparado: assumir que o subagente sabe o que você sabe. Ele NÃO viu a
conversa, o objetivo, os arquivos que você abriu, as convenções combinadas. Briefing bom cabe neste
esqueleto — e o esforço vai todo nos itens 2 e 4:

```
OBJETIVO: <1 frase, resultado, não atividade>
CONTEXTO QUE VOCÊ NÃO TEM: <o essencial da sessão: o que é o projeto, o que já
  se descobriu, decisões já tomadas que limitam a resposta>
ESCOPO: dentro: <...> | fora: <o que NÃO fazer/tocar/propor>
RETORNO ESPERADO: <formato EXATO — lista caminho:linha, tabela, JSON, veredito+evidência.
  Seu texto final é dado para mim, não mensagem para humano.>
QUALIDADE: <o que invalida a resposta: "achado sem arquivo aberto não vale",
  "afirme 'não existe' só listando os padrões buscados">
```

Retorno sem formato pedido = ensaio de 3 páginas que você vai ter que reprocessar (pagando o
contexto que a delegação deveria poupar). O contrato de saída é metade do valor da delegação.

## Padrões de orquestração (do mais comum ao mais caro)
1. **Explorador único** — mapear área desconhecida antes de planejar. (Agente `explorador`.)
2. **Fan-out de frentes independentes** — N agentes, cada um numa dimensão (um por módulo; ou por
   modo de busca: por nome, por conteúdo, por config). Dispare TODOS juntos (paralelo), nunca em
   série. Só vale se as frentes forem realmente independentes.
3. **Pipeline por item** — cada item passa por estágios (achar → transformar → verificar) sem
   esperar os outros itens. Use quando os itens não conversam entre si.
4. **Achador → verificador adversarial** — achados do primeiro viram lista de claims; o segundo
   (agente `verificador`/`revisor-critico`) tenta DERRUBAR cada um. Filtra o
   plausível-mas-falso, que é o veneno específico de agentes: achados que soam certos.
5. **Painel de juízes** — para decisão de design: N agentes propõem abordagens com vieses
   diferentes (simplicidade-primeiro, risco-primeiro, performance-primeiro); você sintetiza do
   vencedor + melhores ideias dos outros. Caro; só para decisões que valem isso.

Barreiras de sincronização (esperar TODOS antes de seguir) só quando o próximo passo precisa do
conjunto completo (dedup entre achados, contagem total). Fora isso, pipeline — barreira
desnecessária desperdiça o tempo dos agentes rápidos esperando o lento.

## Confie, mas confira (o protocolo de recepção)
Resultado de subagente é INSUMO, não verdade:
1. **Cheque o formato** — veio no contrato? Itens com caminho:linha?
2. **Amostre** — abra 2–3 dos locais citados. Batem? Uma citação falsa = quarentena no lote
   inteiro (re-verifique tudo ou re-delegue com briefing corrigido).
3. **Cheque a cobertura** — o agente disse ONDE procurou e o que NÃO achou? "Não existe" sem lista
   de padrões buscados não é informação, é esperança.
4. **Nunca repasse cru** — conclusão de subagente só chega ao usuário depois de passar por você:
   filtrada, verificada por amostra e assinada por VOCÊ. "O subagente disse" não existe como
   atribuição de responsabilidade — quem reporta é você.

## Falhas e sanidade econômica
- Agente voltou vazio/errado UMA vez → conserte o BRIEFING (releia-o pelos olhos de quem não viu
  nada; a falha quase sempre está nele) e redelege UMA vez. Falhou de novo → faça você mesmo;
  redelegar 3× o mesmo briefing é a versão distribuída do "falhou 2× → repete a 3ª".
- Regra de bolso do custo: delegação tem overhead fixo (spawn + briefing + recepção). Vale quando
  o trabalho evitado ≫ overhead — varredura de 30 arquivos, sim; 3 greps, não. Agrupe miudezas
  em UM agente em vez de um agente por miudeza.
- Segredos e dados sensíveis NUNCA entram em briefing de agente (o briefing é um prompt; vaza
  como qualquer texto).

## Checklist antes de despachar
- [ ] O agente tem TODO o contexto necessário dentro do briefing (teste: um estranho executaria?).
- [ ] Formato de retorno especificado e verificável.
- [ ] Escopo negativo dito ("não proponha correções", "não toque em X").
- [ ] Frentes paralelas são de fato independentes.
- [ ] Plano de recepção: o que você vai amostrar para confiar no resultado.
