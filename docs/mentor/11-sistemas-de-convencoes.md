# 11 — Sistemas de convenções que compõem

Destilado do `opten-conventions` — sistema criado do zero por Alexander Cesar para orientar
agentes de IA num time real (C#/Umbraco/TypeScript/SCSS), aqui generalizado para QUALQUER stack.
O que segue é o método por trás daquele repositório: como transformar convenções de equipe em
capacidade permanente de agentes. As lições valem para quem for construir o próximo sistema desses.

## As quinze leis (mineradas de um sistema que funcionou em produção)

**1. Minere regras de evidência, não de opinião.** As convenções vieram de análise de 40+ PRs
mesclados por 4 pessoas — não de um guia de estilo imaginado a priori. Regra sem lastro em
trabalho real vira burocracia; regra minerada de correções reais tem taxa de acerto comprovada.
Corolário: registre a ORIGEM da regra ("baseada em N ocorrências") — é o que justifica mantê-la.

**2. Feche o loop de composição.** O ciclo que dá nome à coisa: correção humana num PR → salva
como artefato de feedback → vira regra permanente no agente revisor → o próximo trabalho já nasce
sabendo. Uma correção paga uma vez; sem o loop, paga toda semana. (É o `/retro` deste kit aplicado
a convenções de equipe.)

**3. Três camadas de ativação para três necessidades.** O mesmo conhecimento se serve de três
formas: **skill** (conhecimento passivo, carrega junto enquanto se escreve — modo "conselho"),
**agente revisor** (julgamento ativo sobre trabalho pronto — modo "auditoria"), **comando**
(workflow multi-etapas disparado pelo usuário — modo "ação"). Não escolha uma: o padrão-espelho
codifica a MESMA regra como conselho E como auditoria — quem escreve não precisa lembrar de pedir
revisão para ser protegido.

**4. Toda regra com par contrastivo.** `CORRETO:` / `ERRADO:` lado a lado, mínimos, é a forma
mais rápida de tornar uma regra inequívoca para humano e para modelo. Prosa abstrata sem o par
é regra que cada leitor interpreta diferente.

**5. Shift-left: aplique no momento da ação.** Convenção aplicada no commit (comando que compõe
a mensagem certa) custa zero correção; a mesma convenção policiada na revisão custa um ciclo
inteiro. O revisor vira rede de segurança do que a automação não cobre, não a linha de frente.

**6. Avise, não bloqueie (por padrão).** Agente de governança "warn-only — report findings,
never block" preserva a autoridade humana e constrói confiança no sistema muito mais rápido que
um gate que trava trabalho. Bloqueio é opt-in explícito da organização, nunca default do autor.

**7. O orquestrador enxerga o que nenhum especialista vê.** O valor único de rodar revisores em
paralelo sob um coordenador: inconsistências ENTRE domínios (a marcação diz X, o script espera Y;
o estilo define classe que o comportamento não usa). Revisor de arquivo único jamais pega isso.

**8. Determinístico onde der, LLM onde precisar.** Na mesma passada de revisão: greps e scripts
para fatos objetivos ("o token existe na fonte de verdade?", "o componente está registrado?") e
agentes só para julgamento. Fato via busca de texto é mais barato E mais confiável.

**9. Regras fixas e heurísticas são skills separadas.** Domínio com resposta certa → tabela de
regras. Domínio com tradeoffs reais (estratégias de git, p.ex.) → matriz `situação → estratégia →
porquê` + anti-padrões com alternativa + o checklist dos 10 segundos antes de ação destrutiva:
"É reversível? Já foi pushado? Existe jeito mais simples?". Capturar JULGAMENTO ≠ capturar regra.

**10. Limiar numérico onde o julgamento seria vago.** "Se mais de N unidades atrasado, sugira X"
torna consistente e auditável o que "use bom senso" deixa ao acaso. Todo julgamento recorrente
merece seu limiar explícito.

**11. O sistema rege a própria manutenção.** Um meta-doc (o CLAUDE.md DO repositório de
convenções) com: checklist de release (versão, changelog, README sincronizado), template de
"como adicionar uma nova unidade de conhecimento". Sem isso, o sistema desvia do próprio padrão
na terceira contribuição.

**12. Curto sempre carregado; pesado sob demanda.** Todo tópico segue `SKILL.md` (enxuto, sempre
no contexto) + `references/*.md` (catálogos, diagramas — carregados só quando necessários).
É a mesma economia do guia 01 aplicada a plugins.

**13. Placeholder em tudo que é compartilhado.** Exemplos com `moduleXxx`, `MyController` —
NUNCA nome real de projeto/cliente na camada genérica. O específico vive só na camada de override
local do consumidor, que tem prioridade explícita sobre o plugin. (Dois ganhos: portabilidade e
zero vazamento de informação de cliente.)

**14. Não-objetivos ao lado dos objetivos.** Cada ferramenta declara o que deliberadamente NÃO
faz ("não dá push, não cria branch, não usa amend"). É a fronteira que evita scope creep e deixa
o usuário saber o que ainda é responsabilidade dele.

**15. Vacine o revisor contra inventar problema.** Instrução literal no agente: "se o código está
limpo, diga isso — não invente issues". O viés natural do LLM é sempre achar algo; sem a vacina,
o sistema treina o time a ignorar o revisor.

## Padrões estruturais que valem imitar
- Raiz separada por função: `agents/<propósito>/`, `commands/<namespace>/`, `skills/<tópico>/`, `docs/plans/`.
- Namespace-prefixo em todo artefato distribuído (`meutime-*`) — evita colisão em quem instala.
- Plano datado e tipado (`AAAA-MM-DD-tipo-slug-plan.md`) separado do changelog: o plano registra
  o RACIOCÍNIO, o changelog registra o RESULTADO.
- Esqueleto idêntico por tipo de artefato: todo revisor tem as mesmas seções (papel → processo →
  regras com pares → formato de saída → fechamento); adicionar um novo é preencher template.
- Identificar qual artefato é "a verdade que sobrevive" no fluxo do time (com squash-merge, é o
  título do PR) e concentrar o rigor ALI, não onde é cômodo.
- Isolar a armadilha mais cara numa seção própria ("CRITICAL: …"), fora da lista de regras
  menores — o erro de 4 horas não pode dividir parágrafo com o de 4 minutos.

## Relação com o resto do kit
Este guia é o 02-memoria + 07-retroalimentacao aplicados à escala de EQUIPE e empacotados como
produto instalável: a memória vira skills versionadas, o `/retro` vira o loop de feedback de PR,
os guardrails viram revisores. Quem dominar os guias 01–10 e este consegue construir, para
qualquer time e qualquer stack, o que o opten-conventions foi para o seu.
