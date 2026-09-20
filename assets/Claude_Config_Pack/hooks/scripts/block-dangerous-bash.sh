#!/usr/bin/env bash
# PreToolUse hook for the Bash tool.
# Reads the hook payload from stdin and exits 2 to BLOCK the command.
# Install to .claude/hooks/block-dangerous-bash.sh and `chmod +x` it.

set -uo pipefail
CMD=$(jq -r '.tool_input.command // empty')
[ -z "$CMD" ] && exit 0

block() {
  echo "BLOCKED by block-dangerous-bash hook: $1" >&2
  echo "If this is genuinely what you want, run it yourself in a terminal." >&2
  exit 2                      # exit 2 = block, stderr goes back to Claude
}

case "$CMD" in
  *"rm -rf /"*|*"rm -rf ~"*|*"rm -fr /"*)  block "recursive delete of a root path" ;;
  *"git push"*--force*|*"git push"*" -f"*) block "force push" ;;
  *"git reset --hard"*)                    block "hard reset discards uncommitted work" ;;
  *"git clean -"*f*d*)                     block "git clean would delete untracked files" ;;
  *"DROP TABLE"*|*"DROP DATABASE"*|*"TRUNCATE "*) block "destructive SQL" ;;
  *"chmod -R 777"*)                        block "world-writable permissions" ;;
  *" > .env"*|*" >> .env"*)                block "writing to .env" ;;
  *"curl"*"| sh"*|*"curl"*"| bash"*)       block "piping a download straight into a shell" ;;
esac

exit 0
