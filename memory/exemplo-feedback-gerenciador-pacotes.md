---
name: exemplo-feedback-gerenciador-pacotes
description: EXEMPLO de memória type feedback — detectar gerenciador de pacotes pelo lockfile antes de qualquer comando
metadata:
  type: feedback
---

Antes de qualquer comando de instalação/execução de pacotes, detectar o gerenciador pelo
lockfile: `pnpm-lock.yaml` → pnpm; `yarn.lock` → yarn; `package-lock.json` → npm;
`bun.lockb` → bun. Nunca assumir npm por padrão.

**Por quê:** 2026-07-06 — rodei `npm install` num projeto pnpm; gerou `package-lock.json`
espúrio e divergência de versões; usuário teve que limpar.
**Como aplicar:** primeiro comando de pacote da sessão → olhar o lockfile antes. Vale para
scripts também (`pnpm test`, não `npm test`). Relacionada: [[exemplo-projeto-contexto]].
