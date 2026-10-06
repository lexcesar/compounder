#!/usr/bin/env bash
# Writes the facts the plugin owns (version, counts, skill length) into every
# data-stamp="<key>" element of site/index.html, and refuses to ship a page whose
# hand-written parts disagree with the plugin. pages.yml runs it before the upload.
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
plugin="$root/compounder"
page="$root/site/index.html"

fail() { echo "stamp-site: $*" >&2; exit 1; }
count() { { grep -o -- "$1" "$page" || true; } | wc -l | tr -d ' '; }

version="$(jq -er .version "$plugin/.claude-plugin/plugin.json")" || fail "no version in compounder/.claude-plugin/plugin.json"
skills="$(find "$plugin/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
agents="$(find "$plugin/agents" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
read -r avg max < <(
	find "$plugin/skills" -mindepth 2 -maxdepth 2 -name SKILL.md -exec wc -l {} + |
		awk '$2 != "total" { sum += $1; n++; if ($1 > max) max = $1 } END { printf "%.0f %d\n", sum / n, max }'
)

# Cards and agent boxes carry copy, so they cannot be generated: a mismatch stops the deploy.
cards="$(count 'class="grid__cmd"')"
boxes="$(count 'class="roster__agent[ "]')"
[ "$cards" = "$skills" ] || fail "the page has $cards skill cards, the plugin has $skills skills — update #pipeline (cards and headline)"
[ "$boxes" = "$agents" ] || fail "the page draws $boxes agents, the plugin has $agents — update #agents (diagram and headline)"

stamp() {
	KEY="$1" VAL="$2" perl -pi -e 's{(data-stamp="\Q$ENV{KEY}\E"[^>]*>)[^<]*}{$1$ENV{VAL}}g' "$page"
	local marked stamped
	marked="$(count "data-stamp=\"$1\"")"
	stamped="$(count "data-stamp=\"$1\"[^>]*>$2<")"
	[ "$marked" -gt 0 ] && [ "$marked" = "$stamped" ] || fail "\"$1\": $marked markers on the page, $stamped carry \"$2\""
}

# The changelog page is rendered from the plugin's CHANGELOG.md; a version without its entry stops the deploy.
changelog="$plugin/CHANGELOG.md"
build="$root/.github/scripts/build-changelog.py"
tests_log="$(mktemp)"
python3 "$root/.github/scripts/test_build_changelog.py" >"$tests_log" 2>&1 || { cat "$tests_log" >&2; fail "build-changelog tests fail (output above)"; }
top="$(python3 "$build" --version "$changelog")" || fail "compounder/CHANGELOG.md does not parse (see the error above)"
[ "$top" = "$version" ] || fail "CHANGELOG.md tops out at $top, plugin.json says $version — add the [$version] entry"
python3 "$build" "$changelog" "$root/site/changelog/index.html" || fail "could not render site/changelog/index.html"

stamp version "v$version"
stamp skills "$skills"
stamp agents "$agents"
stamp avg-lines "$avg"
stamp max-lines "$max"

echo "stamp-site: v$version · $skills skills · $agents agents · $avg lines on average, $max at most · changelog rendered"
