#!/bin/bash
# Count tokens of one or more files with the Claude token counting endpoint (free, model-specific).
# Usage: COMPOUNDER_SEND=1 count-tokens.sh [--model claude-sonnet-5] <file>...
# Prints "<input_tokens>\t<file>" per file. Key: ANTHROPIC_API_KEY env, else Keychain item of that name.
set -euo pipefail

model="claude-sonnet-5"
files=()
while [ $# -gt 0 ]; do
  case "$1" in
    --model) model="$2"; shift 2 ;;
    -h|--help) sed -n 2,4p "$0"; exit 0 ;;
    *) files+=("$1"); shift ;;
  esac
done
[ ${#files[@]} -gt 0 ] || { echo "usage: COMPOUNDER_SEND=1 count-tokens.sh [--model M] <file>..." >&2; exit 2; }

# This script sends the whole file to api.anthropic.com. It refuses unless the caller opts in,
# because no command-text fence sees a network call made from inside a script (fence probes,
# 2026-09-29): an agent that reaches for it by mistake must send nothing.
[ "${COMPOUNDER_SEND:-}" = "1" ] || {
  echo "refusing to send file content to api.anthropic.com: set COMPOUNDER_SEND=1 to allow" >&2; exit 4; }

key="${ANTHROPIC_API_KEY:-}"
if [ -z "$key" ]; then
  key=$(security find-generic-password -s ANTHROPIC_API_KEY -w 2>/dev/null || true)
fi
[ -n "$key" ] || { echo "no ANTHROPIC_API_KEY in env or Keychain" >&2; exit 3; }

status=0
for f in "${files[@]}"; do
  if [ ! -r "$f" ]; then
    echo "unreadable: $f" >&2; status=1; continue
  fi
  # Key via `-H @file` (process substitution) and body via stdin: neither reaches curl's argv,
  # which `ps` exposes to every local user, and the body no longer hits ARG_MAX (1 MiB).
  resp=$(jq -n --arg model "$model" --rawfile text "$f" \
      '{model: $model, messages: [{role: "user", content: $text}]}' |
    curl -sS --fail-with-body https://api.anthropic.com/v1/messages/count_tokens \
      -H @<(printf 'x-api-key: %s' "$key") \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      --data-binary @-) || { echo "request failed for $f: $resp" >&2; status=1; continue; }
  printf '%s\t%s\n' "$(jq -r '.input_tokens' <<<"$resp")" "$f"
done
exit $status
