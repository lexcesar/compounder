# 04 — Planejamento: como planejar de verdade

## Quando planejar (e quando não)
Plano tem custo. A régua:
- **Não planeje** (só faça): 1 arquivo, mudança óbvia, reversível. Planejar o trivial é
  procrastinação com aparência de rigor.
- **Planeje leve** (5 linhas no chat): 2–4 arquivos, caminho claro.
- **Planeje formal** (template `docs/templates/plano.md`, aprovação do usuário): muitos arquivos,
  decisão arquitetural, risco de quebrar algo em uso, ou você percebe que NÃO SABE o caminho.
Sinal de alarme na direção oposta: se você está no 4º arquivo editado de uma tarefa que "não
precisava de plano", precisava.

## A lei central: planeje contra a realidade, não contra a memória
Um plano escrito antes de abrir os arquivos é ficção com números de passo. O reconhecimento vem
ANTES do plano:
1. Abra os arquivos que serão tocados (ou mande o subagente `explorador` mapear).
2. Confirme que cada símbolo/rota/tabela que o plano cita EXISTE e é como você acha.
3. Descubra o que JÁ existe de aproveitável (metade dos planos ruins reinventa utilitário existente).
4. Identifique quem consome o que você vai mudar (grep nos chamadores) — é aí que mora a surpresa.

**Litmus:** todo passo do plano cita caminhos reais que você (ou seu explorador) abriu nesta
sessão. Passo com caminho genérico ("ajustar o serviço de autenticação") = reconhecimento não feito.

## Anatomia do plano que funciona

**1. Objetivo verificável.** Não "melhorar o login", mas "p95 do POST /login < 300ms, medido por
X". Se não dá para saber quando terminou, não é objetivo, é direção. (O `/goal` já faz isso.)

**2. Opções consideradas — no mínimo 2 para qualquer decisão não-óbvia.** Uma frase por opção +
por que a escolhida venceu + por que as outras perderam. Isso custa 3 linhas e compra: (a) você
realmente pensou; (b) quando alguém sugerir a rejeitada, a resposta está escrita; (c) se a
escolhida morrer na execução, o plano B está pronto.

**3. Passos com dono, mudança e PROVA.** Cada passo:
```
Passo N: <o que muda> em <arquivos reais>
  Verificação: <comando/observação que prova que ESTE passo funcionou>
  Risco: <o que pode dar errado aqui> (se relevante)
```
Passo sem verificação própria é convite para descobrir tudo quebrado só no final, sem saber
qual passo quebrou.

**4. Ordem por risco, não por conveniência.** A suposição mais arriscada se testa PRIMEIRO
(spike de 10 linhas, prova de conceito), porque é a que pode invalidar o plano inteiro — e o
momento barato de descobrir isso é antes dos outros passos existirem. Corolário: o passo
irreversível (se houver) vai o mais para o FIM possível, com checkpoint antes.

**5. Pré-mortem — 3 linhas que valem o plano inteiro.** "Se este plano falhar, terá sido
porque: 1)… 2)… 3)…" Para cada, uma mitigação ou um "aceito o risco". Isso força o cérebro a
atacar o próprio plano — o revisor mais barato que existe.

**6. Fora de escopo, por escrito.** O que você NÃO vai fazer (e vai anotar se encontrar).
É a cerca contra a deriva do meio da execução.

## Execução: o plano é vivo, e é um contrato
- Marque os passos conforme conclui (checkbox no próprio plano) — é seu fio de Ariadne quando o
  contexto ficar longo.
- **Desvio pequeno** (o passo 3 precisa tocar um arquivo a mais): anote no plano, siga.
- **Desvio estrutural** (a suposição do plano caiu): PARE. Voltar ao usuário com "o plano previa X,
  a realidade é Y, proponho Z" é execução correta do plano — seguir um plano morto por inércia é
  o erro. Nunca absorva silenciosamente uma mudança de rota que o usuário aprovou de outra forma.

## Anti-padrões
| Anti-padrão | Cheiro | Cura |
|---|---|---|
| Plano-teatro | Passos genéricos: "1. Entender o código 2. Implementar 3. Testar" | Reconhecimento primeiro; passos citam arquivos reais |
| Plano-romance | 5 páginas para renomear uma função | Régua do "quando planejar" |
| Plano-ficção | Cita símbolos/arquivos que não existem | Litmus do reconhecimento |
| Plano-túnel | Uma opção única, jamais comparada | Mínimo 2 opções em decisão não-óbvia |
| Plano-zumbi | Realidade mudou, plano segue sendo executado | Desvio estrutural → parar e replanejar à vista |
| Plano-otimista | Nenhum passo de verificação, nenhum risco listado | Prova por passo + pré-mortem |

## Checklist antes de apresentar um plano
- [ ] Cada passo cita arquivos que EU abri (ou meu explorador mapeou) nesta sessão.
- [ ] Cada passo tem verificação própria.
- [ ] A suposição mais arriscada é atacada no passo 1–2.
- [ ] Decisões não-óbvias mostram a alternativa rejeitada e o porquê.
- [ ] Pré-mortem com 3 causas prováveis de falha.
- [ ] Fora-de-escopo explícito.
- [ ] Critério de "terminado" checável por comando ou observação.
