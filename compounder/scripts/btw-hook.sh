#!/bin/sh
# UserPromptSubmit hook of the compounder plugin.
# When the prompt starts with btw, in any capitalization, it points Claude at the btw skill.
# The skill holds the protocol. This script only matches fixed strings and prints one line.
# It never blocks: no match, or any error, exits 0 with no output.

if grep -qiF -e '"prompt":"btw"' -e '"prompt":"btw ' -e '"prompt":"btw:' -e '"prompt":"btw,' -e '"prompt": "btw"' -e '"prompt": "btw ' -e '"prompt": "btw:' -e '"prompt": "btw,'
then
	printf '%s\n' 'ASIDE DETECTED: the prompt starts with btw. Handle it with the btw skill of the compounder plugin, then resume the current task without abandoning it.'
fi

exit 0
