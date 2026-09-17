#!/bin/bash
# Count tokens of one or more files with the Claude token counting endpoint (free, model-specific).
# Usage: count-tokens.sh [--model claude-sonnet-5] <file>...
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
[ ${#files[@]} -gt 0 ] || { echo "usage: count-tokens.sh [--model M] <file>..." >&2; exit 2; }

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
  body=$(jq -n --arg model "$model" --rawfile text "$f" \
    '{model: $model, messages: [{role: "user", content: $text}]}')
  resp=$(curl -sS --fail-with-body https://api.anthropic.com/v1/messages/count_tokens \
    -H "x-api-key: $key" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$body") || { echo "request failed for $f: $resp" >&2; status=1; continue; }
  printf '%s\t%s\n' "$(jq -r '.input_tokens' <<<"$resp")" "$f"
done
exit $status
