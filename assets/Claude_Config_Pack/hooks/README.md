# Hook recipes

Hooks are shell commands Claude Code runs automatically at defined points. Unlike
CLAUDE.md (advisory), hooks are deterministic — they always run.

## Where they go

`.claude/settings.json` in your project (shared), or `.claude/settings.local.json`
(personal, gitignored), or `~/.claude/settings.json` (global).

Merge the `"hooks"` key from a recipe into your existing settings file. Do not
overwrite the whole file unless it is empty.

## The shape

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "your-command-here", "timeout": 60 }
        ]
      }
    ]
  }
}
```

- `matcher` filters on **tool name** for tool events. `"Edit|Write"` matches either.
  `"*"` or omitting it matches everything. Anything with regex characters is treated
  as an unanchored JavaScript regex, e.g. `"mcp__.*"`.
- Events that never take a matcher: `UserPromptSubmit`, `Stop`, and others that are
  not tied to a tool.
- `"shell": "powershell"` is available (and is the default on Windows).

## What your command receives

JSON on **stdin**, not arguments. For a `PostToolUse` on an edit that looks like:

```json
{
  "session_id": "abc123",
  "cwd": "/path/to/project",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": { "file_path": "/path/to/project/src/index.ts" }
}
```

So you pull the path out with `jq -r '.tool_input.file_path'` (or `ConvertFrom-Json`
in PowerShell). `$CLAUDE_PROJECT_DIR` is also set in the environment.

## Exit codes — the part people get wrong

| Exit | Meaning |
|---|---|
| `0` | Success. stdout is parsed for JSON directives. |
| `2` | **Blocking.** stderr is fed back to Claude. `PreToolUse` blocks the tool, `Stop` prevents stopping, `PostToolUse` reports the problem back. |
| anything else | Non-blocking error — logged, execution continues. |

Use **exit 2** to block. Exit 1 does not block.

## The recipes

| File | Event | What it does |
|---|---|---|
| `01-format-on-edit.json` | PostToolUse | Runs Prettier on every file Claude edits |
| `01-format-on-edit.windows.json` | PostToolUse | Same, PowerShell — no `jq` needed |
| `02-block-dangerous-bash.json` | PreToolUse | Blocks `rm -rf`, force-push, destructive SQL |
| `03-protect-paths.json` | PreToolUse | Blocks edits to `.env`, migrations, workflows |
| `04-test-after-edit.json` | PostToolUse | Runs tests and feeds failures back to Claude |
| `05-notify-on-stop.*.json` | Stop | Desktop alert — one file per OS |
| `06-session-context.json` | SessionStart | Injects git branch + recent commits into context |
| `combined-settings.json` | — | Recipes 01, 02, 03 and 06 in one settings file |

## Notes on individual recipes

- **01** — the bash version needs `jq`. On Windows use `01-format-on-edit.windows.json`,
  which parses the payload with `ConvertFrom-Json` instead.
- **02** — expects the guard script at `.claude/hooks/block-dangerous-bash.sh`. Copy it
  from `scripts/` and `chmod +x` it. Windows users: use `block-dangerous-bash.ps1` and
  set `"shell": "powershell"` on the hook.
- **03** — belt and braces. The `permissions.deny` rules stop access outright; the hook
  catches anything that slips past. Edit the `PROTECTED` list to match your repo.
- **04** — swap `npm test --silent -- --run` for your own test command. On failure it
  exits 2, which feeds the output back so Claude fixes the break in the same turn.
  Raise the `timeout` if your suite is slow.
- **06** — `SessionStart` stdout is shown to Claude, which is why this works. It keeps
  repo state current without you writing it into CLAUDE.md.
- **combined-settings.json** — assumes the bash guard script is installed and executable.
  Delete any block you do not want.

## Before you paste anything

Every recipe here runs a command on your machine automatically. Read it first.
Then run `/hooks` inside Claude Code to confirm what is registered.
