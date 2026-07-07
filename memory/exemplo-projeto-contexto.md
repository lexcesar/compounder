---
name: exemplo-projeto-contexto
description: EXEMPLO de memória type project — decisão de arquitetura com data, dono e motivo (o que o código não conta)
metadata:
  type: project
---

Decisão viva (EXEMPLO): em 2026-06-20 o usuário decidiu adiar a migração para monorepo até
fechar a release 2.0 (prevista para 2026-08). Até lá: nenhuma mudança estrutural de pastas,
mesmo que "melhore" o layout — PRs estruturais serão recusados.

**Por quê:** migração no meio da release já quebrou o deploy uma vez (relato do usuário).
**Como aplicar:** propostas de reorganização → registrar em `docs/decisions/` como ADR proposta
e esperar a 2.0. Relacionada: [[exemplo-feedback-gerenciador-pacotes]].
