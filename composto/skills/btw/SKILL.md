---
name: btw
description: Aparte no meio do trabalho — registra, classifica e agenda a mensagem sem descarrilar a tarefa corrente. Use também ao receber mensagem do usuário durante execução de outra tarefa.
argument-hint: "[mensagem | vazio para revisar a caixa de apartes]"
---

# /btw — conversa sem descarrilar

Entrada: `$ARGUMENTS`

O usuário pensa falando. Cada aparte é valioso — e o modo de falha é duplo: IGNORAR (perde o
pedido) ou DESCARRILAR (abandona a tarefa no meio para atender). Este protocolo evita os dois.

## Se a entrada está vazia: revisão da caixa
Leia `BTW.md` (raiz). Para cada item em "Aberto": ainda vale? → proponha: fazer agora / virar
`/goal` próprio / arquivar em "Feito" / descartar (com um porquê de 1 linha). Não existe `BTW.md` →
diga que a caixa está vazia e explique o uso em 2 linhas.

## Caso geral: chegou um aparte
**Passo 1 — Acuse em ≤2 linhas.** Mostre que leu e entendeu: "Anotado: <resumo em ½ linha> → <destino>."
Nunca gaste mais que isso antes de voltar ao trabalho.

**Passo 2 — Classifique e roteie (uma de quatro):**
| Classe | Teste | Ação |
|---|---|---|
| **Paralelo agora** | Independente da tarefa corrente E delegável com briefing curto E somente-leitura ou efeito trivial | Despache um subagente em background JÁ (briefing completo; formato de retorno definido); registre em `BTW.md` como `[em execução]`; integre o resultado quando chegar |
| **Em seguida** | Rápido mas conflita com o que você está editando/raciocinando agora | Fila "Aberto" do `BTW.md` com marcador `[nesta sessão]`; execute ANTES de encerrar o turno/tarefa |
| **Backlog** | Precisa de decisão sua com contexto, ou é tarefa grande | `BTW.md` "Aberto" com data; mencione no relatório final da tarefa corrente |
| **Muda o jogo** | A mensagem contém ordem de parar/trocar prioridade ("para", "esquece isso", "antes disso, faça X") ou invalida a premissa da tarefa corrente | AÍ SIM interrompa: feche o estado em 2 linhas (o que fica meio-feito) e atenda |

Na dúvida entre classes: pergunte em UMA linha ("isso fura a fila ou pode esperar eu terminar X?")
e continue trabalhando enquanto espera.

**Passo 3 — Volte à tarefa corrente** exatamente de onde parou. O aparte não altera o contrato
vigente salvo classe "Muda o jogo".

## Formato do BTW.md
```markdown
# BTW — caixa de apartes
## Aberto
- [ ] 2026-07-06 — <resumo> `[em execução|nesta sessão|backlog]` — contexto: <½ linha>
## Feito
- [x] 2026-07-06 — <resumo> → <o que foi feito / onde>
```

## Regra permanente (vale sem invocar a skill)
Mensagem que chega ENQUANTO você executa outra coisa = aparte implícito: aplique este protocolo
(acuse em 1–2 linhas na próxima fronteira de ferramenta, classifique, siga). O harness entrega
essas mensagens entre chamadas de ferramenta — você nunca as perde; o que está em jogo é só a
disciplina de não descarrilar. E converse: uma linha de narração a cada fase ("fechei X, abrindo
Y") dá ao usuário os ganchos para apartes bem colocados — trabalho a portas fechadas gera apartes
atrasados e retrabalho.

## No fim de cada tarefa
Antes do relatório final: varra `BTW.md` "Aberto" → execute os `[nesta sessão]`, reporte os
`[em execução]` (com resultado integrado) e liste os `backlog` pendentes em 1 linha cada.
