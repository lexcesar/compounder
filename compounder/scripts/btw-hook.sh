#!/bin/bash
# UserPromptSubmit hook of the compounder plugin.
# If the prompt starts with "btw" (any capitalization), prints the aside protocol as
# additional context. Fail-open: no match or any error exits 0 with no output.
# Written as plain shell on purpose: no command substitution, no here-document, no
# other program, so the plugin directory's validator can follow it without a reviewer.

if grep -qiE '"prompt" *: *"btw( |:|,|")' ; then
	printf '%s\n' \
		'ASIDE DETECTED ("btw" prefix): handle it via the compounder plugin'"'"'s btw skill — acknowledge in' \
		'<=2 lines, classify (parallel now / right after / backlog / game changer), record in BTW.md when' \
		'applicable, and RESUME the current task. Do not abandon the work in progress without an explicit order.'
fi

exit 0
