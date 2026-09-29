#!/bin/bash
# Build an isolated clone for measuring a review run: default branch only, no remote, none of the
# commits that would give the answer away. A local clone shares every object by hardlink, so the
# fixes stay reachable by hash; --no-local transfers only what the branch reaches.
# Usage: clean-room.sh <source-repo> <dest-dir> --target <commit> [--forbid <commit>]...
#                      [--branch main] [--subagent-model <model-id>]
# Prints the launch line for each orchestrator. Runs are interactive, one fresh session each.
set -euo pipefail

src="${1:-}"; dest="${2:-}"
[ -n "$src" ] && [ -n "$dest" ] || { sed -n 5,6p "$0" >&2; exit 2; }
shift 2
target=""; branch="main"; sub=""; forbid=()
while [ $# -gt 0 ]; do
  case "$1" in
    --target) target="${2:-}"; shift 2 ;;
    --forbid) forbid+=("${2:-}"); shift 2 ;;
    --branch) branch="${2:-}"; shift 2 ;;
    --subagent-model) sub="${2:-}"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
[ -n "$target" ] || { echo "--target <commit> is required: the clone is checked against it" >&2; exit 2; }
[ ! -e "$dest" ] || { echo "destination exists: $dest (a reused room may hold a previous run's files)" >&2; exit 3; }

git clone -q --no-local --single-branch --branch "$branch" "$src" "$dest"
git -C "$dest" remote remove origin

drop() { rm -rf "$dest"; echo "$1" >&2; exit "$2"; }
git -C "$dest" cat-file -e "$target^{commit}" 2>/dev/null || drop "target $target is not in branch $branch" 6
if [ ${#forbid[@]} -gt 0 ]; then
  for c in "${forbid[@]}"; do
    if git -C "$dest" cat-file -e "$c^{commit}" 2>/dev/null; then drop "forbidden commit $c is reachable in the clone" 5; fi
  done
fi

abs=$(cd "$dest" && pwd)
echo "clean room ready: $abs"
echo "  branch $branch at $(git -C "$dest" rev-parse --short HEAD), target $(git -C "$dest" rev-parse --short "$target") present, ${#forbid[@]} forbidden commit(s) absent, no remote"
echo "one fresh terminal per run; inside the session: /compounder:review commit $(git -C "$dest" rev-parse --short "$target")"
for m in claude-sonnet-5-5 claude-opus-5-5 claude-fable-5-1; do
  if [ -n "$sub" ]; then
    echo "  cd $abs && CLAUDE_CODE_SUBAGENT_MODEL=$sub claude --model $m"
  else
    echo "  cd $abs && claude --model $m"
  fi
done
echo "after each run: never accept 'apply fixes' or 'record to file' in the room; check the reviewers' model with dispatch-cost.py"
