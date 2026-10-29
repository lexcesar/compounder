#!/bin/bash
# Checks the btw hook: which prompts it answers, that it prints exactly one line, that it never fails.
hook="compounder/scripts/btw-hook.sh"
fail=0
cases=0
check() { # $1 = yes|no (should it answer), $2 = the hook's stdin
	cases=$((cases + 1))
	out=$(printf '%s' "$2" | sh "$hook")
	code=$?
	if [ "$code" -ne 0 ]; then echo "FAIL exit $code: $2"; fail=1; return; fi
	if [ "$1" = yes ] && [ "$(printf '%s\n' "$out" | grep -c '^ASIDE DETECTED')" != 1 ]; then echo "FAIL no aside line: $2"; fail=1; fi
	if [ "$1" = no ] && [ -n "$out" ]; then echo "FAIL unexpected output: $2"; fail=1; fi
}
check yes '{"session_id":"x","hook_event_name":"UserPromptSubmit","prompt":"btw can we also log this"}'
check yes '{"prompt":"BTW: another thing"}'
check yes '{"prompt":"btw,fast"}'
check yes '{"prompt":"btw"}'
check yes '{"prompt": "btw with a space after the colon"}'
check no '{"prompt":"between us"}'
check no '{"prompt":"btween"}'
check no '{"prompt":"fix the bug btw"}'
check no '{"prompt":"this mentions \"btw\" later"}'
check no 'not json'
check no ''
[ "$fail" -eq 0 ] && echo "btw hook: $cases cases pass"
exit "$fail"
