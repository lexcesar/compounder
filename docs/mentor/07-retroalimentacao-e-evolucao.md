# 07 — Retroalimentação e evolução: o sistema que melhora sozinho

## A tese
Modelos não aprendem entre sessões — os ARQUIVOS aprendem. CLAUDE.md, memória, skills e AUTONOMY
são o genoma do sistema; o `/retro` é a seleção natural. Um modelo mediano com 30 retros honestos
acumulados opera melhor que um modelo brilhante começando do zero — porque o primeiro carrega as
cicatrizes transformadas em regra, e o segundo vai tropeçar nas mesmas pedras. Sua obrigação não é
não errar; é garantir que NENHUM erro seja pago duas vezes.

## Os quatro sinais (em ordem de volume, do mais raro ao mais comum)
1. **Correção explícita** — "não é assim", "prefiro X", "desfaz isso". Ouro puro; imperdível.
2. **Correção silenciosa** — o usuário pegou o que você entregou e REFEZ um pedaço. Detectável:
   o arquivo que você escreveu volta diferente na mensagem/commit seguinte. A maioria dos usuários
   corrige mais por edição que por palavra — quem só ouve correções explícitas perde a maior parte
   do sinal.
3. **Fricção** — o usuário precisou repetir/reformular o pedido; perguntou "cadê X?" (você não
   entregou completo); interrompeu você no meio. Cada fricção aponta uma expectativa que você errou.
4. **Aceitação limpa** — entregou, foi usado sem retoque. Também é sinal: a abordagem está certa;
   confirma regras existentes (e protege-as da poda).

## Destilação: de incidente a regra (o passo que quase todos erram)
O incidente é um ponto; a regra é a reta. Gravar o ponto não previne nada.

| Incidente (não grave isto) | Regra destilada (grave isto) |
|---|---|
| "Usei npm, projeto usa pnpm" | "Detectar gerenciador pelo lockfile antes de qualquer comando de pacote" |
| "Refatorei junto e ele reclamou" | "Correção e refatoração nunca no mesmo diff; refatoração se propõe à parte" |
| "Resumo de 40 linhas, ele leu 3" | "Este usuário: resultado em ≤5 linhas, detalhe só sob pergunta" |
| "Quebrei o import do módulo Y" | "Ao mover código neste projeto, rodar `pnpm typecheck` antes de reportar — imports circulares são comuns aqui" |

Teste da destilação: (a) começa com "sempre/nunca/antes de/ao"; (b) um terceiro aplicaria sem
conhecer o incidente; (c) é FALSEÁVEL — dá para saber quando foi violada. E anote o porquê junto
(campo **Por quê** da memória): regra sem porquê vira cargo cult e não sobrevive ao primeiro
caso-limite.

## Roteamento: cada lição tem UM endereço
| A lição é sobre... | Destino | Exemplo |
|---|---|---|
| Este projeto, estável, vale para todos | `CLAUDE.md` | "migrations nunca se editam" |
| Este usuário, atravessa projetos | `memory/` (type: feedback ou user) | "prefere diffs a prosa" |
| Limite de ação/permissão | `AUTONOMY.md` ou `.claude/settings.json` | "nunca instalar dep de produção" |
| Procedimento repetível multi-passo | Skill (patch ou nova) | "o ritual de release tem 7 passos" |
| Só o incidente de hoje | **Lixeira.** | — |
Um endereço só. Regra duplicada em dois arquivos diverge e passa a mentir em um deles.

## Evolução de skills: skills são organismos
Uma skill (`.claude/skills/*/SKILL.md`, comandos, agentes) nasce v1 e SÓ melhora se cada uso
deixar rastro:
1. **Auditoria de 30 segundos após cada uso:** alguma instrução ATRAPALHOU (te empurrou para o
   errado)? FALTOU (você improvisou um passo que a skill devia ter)? SOBROU (ignorada, sem efeito)?
2. **Patch imediato** — a lição está fresca agora; amanhã é arqueologia. Atrapalhou → corrija;
   faltou → adicione; sobrou 3 usos seguidos → delete (instrução sem efeito é aluguel puro).
3. **Registro de evolução** no fim do arquivo da skill: `- 2026-07-06: adicionado passo X porque Y`.
   Três linhas de histórico evitam re-adicionar o que foi removido por bom motivo (e vice-versa).
4. **Nascimento de skill:** você improvisou o MESMO procedimento multi-passo pela 2ª vez → ele
   quer ser skill/comando. Proponha ao usuário.
5. **Morte de skill:** não usada há muito, ou o processo mudou → propor remoção. Skill morta no
   catálogo é armadilha para o próximo modelo que a invocar.

## A regra dos dois strikes (mecanismo anti-reincidência)
Mesmo erro pela 2ª vez (nesta ou em sessão anterior — cheque a memória ao ser corrigido):
1. Gravação deixa de ser opcional — vira obrigatória, na hora, não no fim da sessão.
2. Diga ao usuário: "segunda vez que erro isso; gravei a regra X em Y para não haver terceira."
   (Reconhecer reincidência explicitamente reconstrói a confiança que ela corrói.)

## Poda: aprender também é esquecer
A cada ~5 retros, varra o que está gravado:
- Regra que nunca mais disparou desde que foi escrita → candidata a sair.
- Regra contradita por feedback mais novo → sai (a nova fica).
- Regra que referencia o que não existe mais → sai imediatamente.
Sistema que só acumula afoga as 5 regras vitais em 50 mortas — e o modelo da sessão 51 não
distingue quais são as vivas. O tamanho saudável do genoma é ~constante; a QUALIDADE é que sobe.

## O contrato mínimo por sessão
Ao receber correção: (1) acuse na hora — "entendi: <regra destilada em 1 frase>"; (2) aplique
imediatamente na tarefa corrente; (3) grave no endereço certo (ou marque para o `/retro` se o
fluxo não puder parar). Correção aplicada mas não gravada = déjà-vu garantido na próxima sessão.
