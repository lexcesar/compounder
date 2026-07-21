# ROTAS.md — política de roteamento da linha de montagem

O orquestrador (modelo da sessão, contexto cheio) decide a rota ANTES de despachar trabalho.
Este arquivo é a política; ele é vivo — o `/retro` o corrige com evidência do log de despachos.

## Regras da mesa
1. Máximo **6 tipos** de tarefa. Taxonomia fina não converge com poucas amostras — para criar
   um tipo novo, funda dois existentes ou prove ~10 despachos que não couberam em nenhum.
2. Toda rota barata tem **QC obrigatório** — a economia se paga no gate, não na fé.
3. Rota é decisão consciente: na dúvida entre duas, a mais cara. Despacho errado para baixo
   custa retrabalho; para cima custa só tokens.
4. **Evidência de executor nunca é final.** O envelope reporta; a rodada que vale é a do QC
   (o `verificador-adversarial` reroda a verificação por conta própria). Executor obedece texto
   de plano — confiança nele é por cerca de ferramentas, não por fé no relato.
   Auditoria forense de fork: o transcript fica em
   `~/.claude/projects/<projeto>/<id-da-sessão>/subagents/agent-*.jsonl` e prova modelo usado,
   prompt recebido (variáveis já expandidas) e se o retorno chegou verbatim. Tipo de agente NÃO
   deixa registro — para provar a cerca, inclua no plano uma sonda de ferramenta (ex.: "tente
   WebFetch e reporte"): inexistente = cerca ativa.

## Tabela de rotas

| Tipo de tarefa | Rota | Modelo | QC obrigatório |
|---|---|---|---|
| Localizar código (onde X, quem chama Y, mapear área) | agente `explorador` | haiku | orquestrador confere amostra dos `file:line` |
| Pesquisa de fundamento (pré-plano/brainstorm) | agente `composto:pesquisador` | haiku | citações conferidas por amostra |
| Executar plano-pronto (unidades com verificação própria) | skill `/composto:trabalhar-fork` | sonnet | `composto:verificador-adversarial` sobre o envelope |
| Revisão de diff/branch | `/composto:revisar` (painel + tribunal) | sessão + painel sonnet | tribunal já embutido |
| Checar afirmações ("feito", "passa", "sem usos de Y") | agente `verificador` | sonnet | evidência executada é o próprio QC |
| Bug misterioso, arquitetura, escopo nebuloso | **INLINE — nunca despachar** | sessão | ciclo normal |

[AJUSTE: rotas para agentes pessoais/de outros plugins — ex. cavecrew-investigator no lugar de
explorador se o plugin caveman estiver instalado.]

## Dever de log (do orquestrador, logo após cada despacho)
Apêndice de 1 linha em `docs/pipeline/despachos.jsonl`:

```json
{"data":"AAAA-MM-DD","sessao":"<id curto da sessão>","tarefa":"1 frase","tipo":"<da tabela>","rota":"<agente/skill>","modelo":"<usado>","resultado":"completo|parcial|bloqueado|refutado","retrabalho":false,"notas":"opcional"}
```

- `resultado` vem do envelope/retorno do despachado; `refutado` = QC derrubou a entrega.
- `retrabalho: true` = o orquestrador (ou rota mais cara) teve que refazer/completar.
- Despacho sem envelope/retorno = rota quebrada: logue com `resultado:"bloqueado"` e diga em `notas`.
- Campos livres (`tarefa`/`notas`): nunca dado sensível — o arquivo é versionado.

## Auditoria (via /retro)
- **Gatilho de lição** (endereço único desta regra): `retrabalho:true`, `resultado:"refutado"`
  ou `resultado:"bloqueado"` → lição candidata no `/retro`.
- **Demissão de modelo:** mesmo tipo com ≥2 retrabalhos nos últimos ~10 despachos → sobe o
  modelo da rota (barato → sonnet → sessão) e registre a mudança aqui com data.
- **Promoção de economia:** tipo com ~10 despachos sem retrabalho → experimente um degrau mais
  barato, mantendo o QC.
- Rota sem uso em ~5 retros → candidata a remoção (poda).

## Registro de evolução
- 2026-07-21: criação — 6 tipos, rota fork para plano-pronto (spike U1 do plano
  `docs/plans/2026-07-21-linha-de-montagem-plano.md`).
- 2026-07-21: pós-revisão adversarial — executor dedicado `executor-fork` (sem WebFetch/Task),
  deny de canais de rede no settings.json, regra 4 (evidência de executor nunca é final).
  Motivo: camada `ask` provou não interceptar subagente; cerca dura é ferramenta + deny.
- 2026-07-21 (retro, sessão 45ed8dec): rota fork sai de "experimental" — primeiro despacho real
  como skill (linha 2 do despachos.jsonl): fork real, sonnet provado por transcript, envelope
  verbatim, cerca de tools confirmada por sonda. Regra 4 ganha a técnica de auditoria forense.
