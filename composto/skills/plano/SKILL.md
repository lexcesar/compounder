---
name: plano
description: Decidir COMO construir — reconhecimento real do código, opções comparadas, unidades com verificação própria. Use para planejar implementação a partir de requisitos ou descrição.
argument-hint: "[caminho de requisitos | descrição da tarefa]"
---

# /plano — o COMO, contra a realidade

Entrada: `$ARGUMENTS`

Lei central: **plano escrito antes de abrir os arquivos é ficção com número de passos.**
Se existir `docs/mentor/04-planejamento.md` no projeto, ele é a doutrina completa; esta skill é a
execução. Saída: plano que um implementador (você amanhã, ou um Haiku) executa sem adivinhar.

## Passo 0 — Entrada e artefato
- Entrada é doc com `etapa: requisitos` → você vai ENRIQUECER esse arquivo no lugar (um artefato
  por feature, requisitos preservados no topo).
- Entrada é descrição solta → crie `docs/plans/AAAA-MM-DD-<slug>-plano.md`; derive requisitos
  mínimos (R1..Rn) da descrição e declare suposições. Ambiguidade que muda o resultado → pergunte
  (uma rodada, com recomendações) — exceto em chamada de pipeline (lfg/slfg): assuma o razoável
  e registre em "Suposições".
- Tarefa trivial (1–2 arquivos, caminho óbvio)? Diga que plano formal é overhead e proponha
  executar direto com um plano-de-5-linhas no chat.

## Passo 1 — Reconhecimento (o passo que separa plano de ficção)
1. ABRA os arquivos que serão tocados (área pequena) ou despache 1 `pesquisador` (área ampla).
2. Grep nos CONSUMIDORES do que vai mudar — a surpresa mora em quem chama.
3. O que já existe de aproveitável? (utilitário, padrão, teste-modelo a imitar)
4. Memória institucional: grep `docs/solutions/` por termos da área; `CONCEPTS.md` para vocabulário.
5. **Trabalho em voo:** branches/PRs abertos tocando os mesmos arquivos (`git fetch` + `gh pr list`).
   Conflito à vista → declare o sequenciamento no plano ("começar após merge de X" ou "aceito
   resolver conflito") e anote que âncoras de linha podem deslocar até a execução.
**Litmus antes de prosseguir:** cada arquivo que o plano vai citar foi visto NESTA sessão (por
você ou pelo dossiê do pesquisador, com amostra conferida).

## Passo 2 — Decisões
Para cada decisão não-óbvia: ≥2 opções, 1 frase cada, vencedora + porquê, perdedora + porquê.
Cole no plano (seção "Decisões"). Decisão sem alternativa registrada = reflexo, não escolha.

## Passo 3 — Unidades de implementação
Quebre em U1..Un, cada uma entregável e verificável sozinha:
```markdown
### U<N>: <o que muda, em 1 frase>
- Arquivos: `caminho`, `caminho` (reais, vistos no reconhecimento)
- Mudança: <2–4 linhas de intenção — decisões, não código pronto>
- Testes: <cenários enumerados — o implementador não inventa cobertura>
- Verificação: <comando/observação que prova ESTA unidade>
- Risco: <o que pode dar errado aqui, se relevante>
- Depende de: <U<M> | nada>
```
Ordene por RISCO: a suposição mais perigosa vira U1 (spike barato que pode invalidar o resto).
Passo irreversível (migration, contrato público): o mais tarde possível, com checkpoint antes.

## Passo 4 — Blindagem
No fim do arquivo:
- **Pré-mortem:** "se falhar, terá sido porque: 1) 2) 3)" + mitigação ou "aceito".
- **Fora de escopo:** o que NÃO entra (herde os não-objetivos dos requisitos).
- **Deferido à execução:** perguntas que só o código rodando responde — nomeadas, não escondidas.
- **Done:** critérios finais checáveis + "suite e typecheck verdes contra o baseline".
Atualize o frontmatter: `etapa: plano-pronto`.

## Passo 5 — Gate de qualidade (auto-aplicado antes de entregar)
- [ ] Toda unidade tem verificação própria e arquivos reais.
- [ ] Cenários de teste enumerados nas unidades com comportamento.
- [ ] Decisões têm alternativa rejeitada registrada.
- [ ] Nenhum caminho absoluto (sempre relativo ao repo).
Qualquer ❌ → conserte antes de mostrar.

## Passo 6 — Handoff
Resumo no chat: objetivo, nº de unidades, U1 (o spike de risco), decisões-chave. Feche com:
"Plano em `<caminho>`. Próximo: `/trabalhar <caminho>` — ou aponte o que mudar."
(Em pipeline: retorne o caminho e pare.)
