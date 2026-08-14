#!/bin/bash
# UserPromptSubmit hook of the compounder plugin.
# If the prompt starts with "btw" (any capitalization), injects the aside protocol
# as additional context. Fail-open: any error exits 0 with no context — never blocks the session.

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
ASIDE DETECTED ("btw" prefix): handle it via the compounder plugin's btw skill — acknowledge in
<=2 lines, classify (parallel now / right after / backlog / game changer), record in BTW.md when
applicable, and RESUME the current task. Do not abandon the work in progress without an explicit order.
EOF
    ;;
esac

exit 0
