#!/bin/bash
# Test for count-tokens.sh: neither the API key nor the request body may appear in curl's argv.
# Uses a stub curl on PATH; never hits the network. Run: bash compounder/scripts/test_count_tokens.sh
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/bin"
cat > "$tmp/bin/curl" <<'EOF'
#!/bin/bash
printf '%s\n' "$@" > "$STUB_ARGV"
cat > "$STUB_STDIN"
for a in "$@"; do case "$a" in @-) ;; @*) cat "${a#@}" >> "$STUB_FILES" ;; esac; done
echo '{"input_tokens":42}'
EOF
chmod +x "$tmp/bin/curl"

printf 'SENTINEL-BODY-TEXT\n' > "$tmp/plan.md"
export STUB_ARGV="$tmp/argv" STUB_STDIN="$tmp/stdin" STUB_FILES="$tmp/files"
: > "$STUB_FILES"

fail=0

# Guard: without COMPOUNDER_SEND=1 the script refuses and curl is never invoked.
for send in "" "yes" "0" "true"; do
  rm -f "$STUB_ARGV"
  set +e
  err=$(PATH="$tmp/bin:$PATH" ANTHROPIC_API_KEY=sk-ant-SENTINEL-KEY COMPOUNDER_SEND="$send" \
    bash "$here/count-tokens.sh" "$tmp/plan.md" 2>&1 >/dev/null)
  code=$?
  set -e
  [ $code -eq 4 ] || { echo "FAIL guard: COMPOUNDER_SEND='$send' exited $code, expected 4"; fail=1; }
  [ ! -e "$STUB_ARGV" ] || { echo "FAIL guard: curl was invoked with COMPOUNDER_SEND='$send'"; fail=1; }
  grep -q 'COMPOUNDER_SEND=1' <<<"$err" || { echo "FAIL guard: refusal does not name COMPOUNDER_SEND=1"; fail=1; }
done

out=$(PATH="$tmp/bin:$PATH" ANTHROPIC_API_KEY=sk-ant-SENTINEL-KEY COMPOUNDER_SEND=1 bash "$here/count-tokens.sh" "$tmp/plan.md")

[ "$out" = "42	$tmp/plan.md" ] || { echo "FAIL output: $out"; fail=1; }
grep -q 'SENTINEL-KEY' "$STUB_ARGV" && { echo "FAIL key in curl argv"; fail=1; }
grep -q 'SENTINEL-BODY-TEXT' "$STUB_ARGV" && { echo "FAIL body in curl argv"; fail=1; }
grep -q 'SENTINEL-BODY-TEXT' "$STUB_STDIN" || { echo "FAIL body not on stdin"; fail=1; }
grep -q 'x-api-key: sk-ant-SENTINEL-KEY' "$STUB_FILES" || { echo "FAIL key header not passed via @file"; fail=1; }

[ $fail -eq 0 ] && echo "OK count-tokens.sh: refuses without COMPOUNDER_SEND=1; key and body off argv"
exit $fail
