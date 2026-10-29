#!/bin/bash
# UserPromptSubmit hook of the compounder plugin.
# If the prompt starts with "btw" (any capitalization), prints the aside protocol as
# additional context. Fail-open: no match or any error exits 0 with no output.
# Deliberately plain shell: fixed-string grep on stdin, printf of literal lines, no
# variables, no substitution, no patterns, no here-document, no other interpreter, so the
# plugin directory's validator can follow it without a reviewer.

if grep -qiF -e '"prompt":"btw"' -e '"prompt":"btw ' -e '"prompt":"btw:' -e '"prompt":"btw,' -e '"prompt": "btw"' -e '"prompt": "btw ' -e '"prompt": "btw:' -e '"prompt": "btw,'
then
	printf '%s\n' 'ASIDE DETECTED ("btw" prefix): handle it via the btw skill of the compounder plugin. Acknowledge in'
	printf '%s\n' '<=2 lines, classify (parallel now / right after / backlog / game changer), record in BTW.md when'
	printf '%s\n' 'applicable, and RESUME the current task. Do not abandon the work in progress without an explicit order.'
fi

exit 0
