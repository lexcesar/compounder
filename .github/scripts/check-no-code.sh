#!/bin/sh
# The plugin directory accepts from community (non-Verified) plugins only Markdown, text, JSON,
# YAML and PNG/JPEG/GIF/WebP/ICO images, none starting with #!, and no hooks.
# Fails listing every tracked file under compounder/ that breaks this.
cd "$(git rev-parse --show-toplevel)" || exit 1
bad=$(git ls-files compounder | while IFS= read -r f; do
	case "$f" in
		(*/hooks/*) echo "$f (hook)"; continue ;;
	esac
	if ! printf '%s\n' "$f" | grep -Eqi '\.(md|txt|json|ya?ml|png|jpe?g|gif|webp|ico)$'; then
		echo "$f (type)"
	elif [ "$(head -c2 "$f")" = '#!' ]; then
		echo "$f (starts with #!)"
	fi
done)
if [ -n "$bad" ]; then
	printf '::error::not accepted from community plugins:\n%s\n' "$bad"
	exit 1
fi
echo "plugin ships no code"
