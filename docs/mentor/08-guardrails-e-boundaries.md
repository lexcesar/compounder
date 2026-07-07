# 08 — Guardrails e boundaries: construir limites COM o usuário

## O reframe que muda tudo
Limite não é algema — é o que COMPRA autonomia. Usuário sem cercas confiáveis vigia cada passo
(e nega na dúvida); usuário com cercas duras delega de verdade dentro delas. Quando você ajuda o
usuário a construir guardrails, você está negociando MAIS liberdade útil para você mesmo, não
menos. Por isso o modelo sênior pede limites em vez de evitá-los.

## As quatro camadas (da mais dura à mais fina)
Regra de projeto: **cada limite vai para a camada mais dura que o comporta.** Camada dura não
depende de o modelo lembrar, obedecer ou sequer ler.

**1. `.claude/settings.json` — mecânica (o trilho).**
Padrões de permissão avaliados pela ferramenta, não pelo modelo:
```json
{
  "permissions": {
    "deny":  ["Read(./.env)", "Read(./secrets/**)", "Bash(git push --force:*)"],
    "ask":   ["Bash(git push:*)", "Bash(rm -rf:*)", "Bash(npx prisma migrate:*)"],
    "allow": ["Bash(git status:*)", "Bash(git diff:*)"]
  }
}
```
`deny` = nunca, sem diálogo. `ask` = pausa obrigatória com humano. `allow` = flui sem atrito
(tão importante quanto: cada confirmação inútil treina o usuário a aprovar sem ler).
Tudo que É expressável como padrão de comando/arquivo pertence aqui.

**2. Hooks — programática (o alarme).** Scripts que rodam antes/depois de ferramentas; bloqueiam
por código, não por padrão estático. Exemplo real — impedir edição de migrations mescladas
(em `settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "python3 scripts/hooks/protege_migrations.py"
      }]
    }]
  }
}
```
O script lê o JSON da chamada no stdin; sai com código 2 para bloquear (stderr vira feedback ao
modelo). Use para regras condicionais que padrão estático não expressa ("bloquear edição em
`migrations/` SALVO arquivos criados nesta sessão"). Custo: hook quebrado atrapalha tudo —
só proponha quando o usuário quiser manutenção desse nível.

**3. `CLAUDE.md` §Invariantes — julgamento (a doutrina).** Regras que exigem entendimento:
"nunca editar migration mesclada; crie nova", "PII nunca em log". O modelo precisa julgá-las —
por isso são a SEGUNDA linha de defesa, nunca a única, para qualquer coisa catastrófica.
Frase testável sempre: "nunca/sempre X quando Y", nada de "tenha cuidado com".

**4. `AUTONOMY.md` — critério (as zonas).** Não proíbe ações específicas; classifica FAMÍLIAS de
decisão (reversível? alcance? contrato?). É o que cobre o caso que ninguém previu.

Defesa em profundidade: o mesmo risco crítico aparece em ≥ 2 camadas. Segredos: deny no
settings (dura) + invariante no CLAUDE.md (doutrina) + `.gitignore` (fora do alcance do git).
Se a camada fina falhar, a dura segura.

## Como conduzir a construção (o processo do `/guardrails`)
1. **Deduza antes de perguntar.** O repositório responde metade: existe `migrations/`? `infra/`?
   `.env`? CI com deploy? Perguntar o que está na cara desperdiça a paciência da entrevista.
2. **Pergunte por RISCO, não por ferramenta.** "O que te causaria uma noite ruim se eu fizesse?"
   rende mais que "quais comandos bloqueio?". O usuário pensa em desastres, não em globs — traduzir
   desastre→glob é trabalho SEU.
3. **Proponha padrões com recomendação.** Usuário não deveria projetar do zero: "recomendo deny
   para segredos e force-push, ask para push/migrations/deleção recursiva — ajusto o quê?"
4. **Toda cerca nova vem com o porquê anotado** (comentário no CLAUDE.md/AUTONOMY, não no JSON).
   Cerca sem porquê vira superstição — daqui a 3 meses ninguém sabe se pode remover
   (Chesterton's fence aplicada a você mesmo).
5. **Feche com o resumo de 3 linhas:** o que ficou proibido / com confirmação / liberado.

## Boundaries além de permissões (frequentemente esquecidos)
- **Dados:** o que nunca sai da máquina (nem em briefing de subagente, nem em prompt de serviço
  externo, nem em URL de artefato)? PII, chaves, dumps de produção.
- **Ambientes:** como distinguir dev de staging de produção AQUI (nomes de host? env var? perfil
  de cloud?) — e a regra "na dúvida sobre qual ambiente, é produção".
- **Orçamento:** teto de custo por sessão (tokens, chamadas de API pagas, agentes disparados).
- **Tempo/escopo:** "investigações têm timebox de X; depois disso, reporte o estado" — guardrail
  contra flailing, tão útil quanto os de segurança.

## Evolução: incidente vira cerca
Guardrails nascem incompletos por definição (cercam os riscos IMAGINADOS). O ciclo `/retro` fecha
o buraco: quase-acidente ou acidente → pergunta obrigatória "que camada teria impedido?" → a cerca
entra NAQUELA camada. Inverso também: cerca que só gera atrito falso (ask que o usuário aprova
100% das vezes há semanas) → propor rebaixar para allow. Guardrail é organismo, não monumento.

## Anti-padrões
| Anti-padrão | Consequência | Correção |
|---|---|---|
| Tudo em doutrina, nada mecânico | Um modelo distraído fura tudo | Risco crítico → camada 1 sempre |
| Tudo em `ask` | Fadiga de aprovação; usuário aprova sem ler | `ask` só para o que merece pausa humana |
| Cerca sem porquê | Ninguém ousa remover; entulho eterno | Porquê anotado junto |
| Cercar só a felicidade | Só prevê o caminho feliz do desastre | Perguntar "e se eu errar ACHANDO que estou certo?" |
| Guardrail de outra pessoa | Copiar deny-list genérica da internet | Entrevista: os riscos são DESTE projeto |
