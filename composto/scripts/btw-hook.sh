#!/bin/bash
# Hook UserPromptSubmit do plugin composto.
# Se o prompt começa com "btw" (qualquer capitalização), injeta o protocolo de aparte
# como contexto adicional. Fail-open: qualquer erro sai 0 sem contexto — nunca bloqueia a sessão.

input=$(cat 2>/dev/null) || exit 0

prompt=$(printf '%s' "$input" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get("prompt", ""))
except Exception:
    pass
' 2>/dev/null) || exit 0

case "$(printf '%.4s' "$prompt" | tr "[:upper:]" "[:lower:]")" in
  btw|btw\ |btw:|btw,)
    cat <<'EOF'
APARTE DETECTADO (prefixo "btw"): trate pela skill btw do plugin composto — acuse em <=2 linhas,
classifique (paralelo agora / em seguida / backlog / muda o jogo), registre em BTW.md quando
aplicável e RETOME a tarefa corrente. Não abandone o trabalho em andamento salvo ordem explícita.
EOF
    ;;
esac

exit 0
