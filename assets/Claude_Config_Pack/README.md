# Claude Code Config Pack

Ready-to-use configuration files for Claude Code. Copy the ones you want, edit the
bracketed blanks, done. Nothing here needs to be installed as a package.

Verified against the Claude Code docs, July 2026.

## What's in here

| Folder | What it is | Where it goes |
|---|---|---|
| `claude-md/` | 6 CLAUDE.md build-plan templates | `CLAUDE.md` in your repo root |
| `hooks/` | 6 hook recipes + helper scripts | `.claude/settings.json` |
| `skills/` | SKILL.md template + 3 worked examples | `~/.claude/skills/<name>/SKILL.md` |
| `mcp/` | MCP server configs | `.mcp.json` or `claude_desktop_config.json` |
| `permissions/` | Safe permission defaults | `.claude/settings.json` |

## Settings file precedence (highest wins)

1. Managed / enterprise policy
2. Command-line flags
3. `.claude/settings.local.json`  — personal, gitignored
4. `.claude/settings.json`        — shared with the team, committed
5. `~/.claude/settings.json`      — your global defaults

Permission rules MERGE across these files. Most other settings do not — the
highest-precedence file wins outright.

## Five-minute setup

1. Copy `claude-md/CLAUDE.starter.md` to your repo root as `CLAUDE.md` and fill it in.
2. Copy `permissions/settings.safe-defaults.json` to `.claude/settings.json`.
3. Pick one hook recipe from `hooks/` and merge its `hooks` key into that same file.
4. Start Claude Code and run `/hooks` to confirm it registered.

## A warning worth reading

Hooks run shell commands on your machine automatically, with your permissions.
Read every command before you paste it into your settings. That applies to these
files and to any hook you find online.
