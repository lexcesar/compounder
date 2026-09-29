#!/bin/bash
# Test for clean-room.sh: the clone must hold the default branch only, no remote, and none of
# the commits named as forbidden. Works on throwaway repositories under a temp dir.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
g() { git -C "$1" -c user.name=t -c user.email=t@t -c commit.gpgsign=false "${@:2}"; }

mkdir "$tmp/src" && g "$tmp/src" init -q -b main
echo a > "$tmp/src/a" && g "$tmp/src" add a && g "$tmp/src" commit -qm target
target=$(g "$tmp/src" rev-parse HEAD)
echo b > "$tmp/src/b" && g "$tmp/src" add b && g "$tmp/src" commit -qm later
head=$(g "$tmp/src" rev-parse HEAD)
g "$tmp/src" switch -qc fix && echo spoiler > "$tmp/src/s" && g "$tmp/src" add s && g "$tmp/src" commit -qm spoiler
spoiler=$(g "$tmp/src" rev-parse HEAD)
g "$tmp/src" switch -q main

fail=0
out=$(bash "$here/clean-room.sh" "$tmp/src" "$tmp/room" --target "$target" --forbid "$spoiler" --subagent-model claude-sonnet-5-5)
[ "$(git -C "$tmp/room" rev-parse HEAD)" = "$head" ] || { echo "FAIL head is not main"; fail=1; }
git -C "$tmp/room" cat-file -e "$spoiler" 2>/dev/null && { echo "FAIL spoiler commit reachable"; fail=1; }
[ -z "$(git -C "$tmp/room" remote)" ] || { echo "FAIL remote left in place"; fail=1; }
[ ! -e "$tmp/room/s" ] || { echo "FAIL spoiler file present"; fail=1; }
grep -q 'CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5-5' <<<"$out" || { echo "FAIL launch line lacks the pinned subagent model"; fail=1; }
grep -q -- '-p\b\|--print' <<<"$out" && { echo "FAIL launch line is headless"; fail=1; }

set +e
if bash "$here/clean-room.sh" "$tmp/src" "$tmp/room" --target "$target" >/dev/null 2>&1; then echo "FAIL existing destination accepted"; fail=1; fi
bash "$here/clean-room.sh" "$tmp/src" "$tmp/room2" --target "$target" --forbid "$head" >/dev/null 2>&1; code=$?
[ $code -eq 5 ] || { echo "FAIL forbidden commit present, exit $code, expected 5"; fail=1; }
[ ! -e "$tmp/room2" ] || { echo "FAIL tainted clone left on disk"; fail=1; }
bash "$here/clean-room.sh" "$tmp/src" "$tmp/room3" --target 0000000000000000000000000000000000000000 >/dev/null 2>&1; code=$?
[ $code -eq 6 ] || { echo "FAIL missing target, exit $code, expected 6"; fail=1; }
bash "$here/clean-room.sh" "$tmp/src" "$tmp/room4" >/dev/null 2>&1; code=$?
[ $code -eq 2 ] || { echo "FAIL missing --target, exit $code, expected 2"; fail=1; }
set -e

[ $fail -eq 0 ] && echo "OK clean-room.sh: default branch only, no remote, forbidden commits absent"
exit $fail
