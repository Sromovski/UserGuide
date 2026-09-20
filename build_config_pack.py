#!/usr/bin/env python3
"""Build the Claude Code Config Pack — real, runnable template files + an index PDF.

Everything here was verified against code.claude.com/docs (July 2026):
  * hooks live under the "hooks" key in .claude/settings.json
  * matcher filters on TOOL NAME; "Edit|Write" style alternation is supported
  * hooks receive JSON on stdin (tool_name, tool_input, cwd, ...)
  * EXIT CODE 2 blocks / feeds stderr back to Claude. Exit 1 is a non-blocking error.
  * CLAUDE_PROJECT_DIR is set in the hook environment
  * "shell": "powershell" is supported (and is the Windows default)

Run:  python build_config_pack.py
Outputs:
  assets/Claude_Config_Pack/...      the distributable file tree
  outputs/Claude_Config_Pack.zip     zipped for upload
  outputs/Claude_Config_Pack_Guide.pdf
"""
import os
import shutil
import zipfile

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

ROOT = r'C:\Projects\UserGuide'
PACK = os.path.join(ROOT, 'assets', 'Claude_Config_Pack')
OUTDIR = os.path.join(ROOT, 'outputs')

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX

BG     = HexColor('#0F0F1A')
OG     = HexColor('#E07A38')
OGL    = HexColor('#F5A66B')
CREAM  = HexColor('#F5F0E8')
LGR    = HexColor('#D4CFC7')
MGR    = HexColor('#9B9690')
PNL    = HexColor('#1C1C2E')
PNL2   = HexColor('#161625')
GRN    = HexColor('#5CB85C')
AMB    = HexColor('#F59E0B')
WHT    = HexColor('#FFFFFF')
DOG    = HexColor('#C86820')
DDOG   = HexColor('#B85C18')
DBGRN  = HexColor('#0D2B0D')
DBAMB  = HexColor('#2B1A00')
CODEBG = HexColor('#0A0A15')

GUIDE = 'Claude Code Config Pack'

# ============================================================ FILE CONTENTS

FILES = {}

FILES['README.md'] = r'''# Claude Code Config Pack

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
'''

FILES['claude-md/README.md'] = r'''# CLAUDE.md templates

`CLAUDE.md` is a plain markdown file in your repo root. Claude Code loads it into
context at the start of every session, so it is the cheapest way to stop repeating
yourself.

## Picking one

| File | Use it for |
|---|---|
| `CLAUDE.starter.md` | Any project. Start here if unsure. |
| `CLAUDE.nextjs-react.md` | Next.js / React front-ends |
| `CLAUDE.python-fastapi.md` | Python services and APIs |
| `CLAUDE.node-api.md` | Node/Express/Fastify back-ends |
| `CLAUDE.data-science.md` | Notebooks, pipelines, analysis repos |
| `CLAUDE.monorepo.md` | Multi-package repos with per-package rules |

## Rules that make CLAUDE.md actually work

1. **Keep it under ~150 lines.** It is re-read every session; long files get skimmed.
2. **Only write what you verified.** A wrong build command is worse than no build command.
3. **Commands must be copy-pasteable.** Not "run the tests" — `npm test -- --run`.
4. **State boundaries explicitly.** What Claude must never touch, and what needs asking first.
5. **Link out for detail.** Point to `docs/architecture.md` rather than inlining it.
6. **It is advisory, not enforced.** For rules that MUST hold, use a hook (see `../hooks/`).

## Locations

| Path | Scope |
|---|---|
| `~/.claude/CLAUDE.md` | Every project on your machine |
| `CLAUDE.md` (repo root) | This project, shared with the team |
| `.claude/CLAUDE.local.md` | This project, just you (gitignore it) |
| `subdir/CLAUDE.md` | Extra rules that apply inside that subdirectory |
'''

FILES['claude-md/CLAUDE.starter.md'] = r'''# [PROJECT NAME]

[One sentence: what this project is and who uses it.]

## Tech stack

- Language: [e.g. TypeScript 5.4]
- Framework: [e.g. Next.js 15]
- Database: [e.g. Postgres 16 via Prisma]
- Tests: [e.g. Vitest]
- Package manager: [npm | pnpm | yarn | uv | poetry]

## Commands

```bash
[npm install]          # install dependencies
[npm run dev]          # start the dev server
[npm test]             # run the test suite
[npm run lint]         # lint
[npm run build]        # production build
```

Always run [npm test && npm run lint] before telling me a change is done.

## Architecture

- `[src/app/]`     — [routes and pages]
- `[src/lib/]`     — [shared business logic]
- `[src/db/]`      — [schema and queries]
- `[tests/]`       — [test suite]

Data flows [describe the one path a newcomer needs: request -> handler -> service -> db].

## Conventions

- [Prefer named exports over default exports.]
- [Errors bubble to the route handler; do not swallow them.]
- [New code goes in TypeScript strict mode — no `any`.]
- [Tests live next to the file they test as `*.test.ts`.]
- Match the style of surrounding code over any rule listed here.

## Boundaries

Do NOT touch without asking:
- `[migrations/]` — schema changes need review
- `[.env]`, `[.env.*]` — never read or write secrets
- `[package.json]` dependencies — ask before adding a package

## Build rules

1. Plan before editing when a change spans more than [3] files.
2. Reproduce a bug with a failing test before fixing it.
3. Small, revertable commits — one logical change each.
4. If tests fail, say so and paste the output. Never describe unverified work as done.
5. Ask rather than guess when the requirement is ambiguous.
'''

FILES['claude-md/CLAUDE.nextjs-react.md'] = r'''# [APP NAME] — Next.js front-end

[One sentence describing the product.]

## Tech stack

- Next.js [15] (App Router), React [19], TypeScript strict
- Styling: [Tailwind CSS 4]
- State: [React Server Components + `useState`; no global store]
- Data: [Server Actions] / [tRPC] / [REST at `[API URL]`]
- Tests: [Vitest] + [Playwright] for e2e

## Commands

```bash
npm install
npm run dev            # http://localhost:3000
npm test               # unit tests
npm run test:e2e       # Playwright
npm run lint
npm run typecheck
npm run build          # must pass before any PR
```

Definition of done: `npm run typecheck && npm run lint && npm test` all green.

## Architecture

- `app/`            — routes. Server Components by default.
- `app/api/`        — route handlers
- `components/ui/`  — presentational, no data fetching
- `components/`     — feature components, may fetch
- `lib/`            — pure helpers, no React imports
- `hooks/`          — client hooks, all start with `use`

## Conventions

- Server Components by default. Add `'use client'` only when you need state,
  effects, or browser APIs — and say why in a comment.
- Fetch data in the Server Component, pass it down as props. No fetching in `useEffect`.
- No `any`. If a type is genuinely unknown, use `unknown` and narrow it.
- Tailwind classes only — no inline `style` and no CSS modules.
- Every interactive element needs an accessible name.
- Images go through `next/image`.

## Boundaries

- Do not add a dependency without asking.
- Do not edit `next.config.*` or `tailwind.config.*` without asking.
- Never read `.env*`.
- Do not modify anything in `[app/(billing)/]` — payment code is reviewed separately.

## Build rules

1. Plan first for anything touching routing or data flow.
2. New components need a test or a Storybook story.
3. Check both light and dark mode when changing visual code.
4. Run the build before claiming done — type errors often only surface there.
'''

FILES['claude-md/CLAUDE.python-fastapi.md'] = r'''# [SERVICE NAME] — Python API

[One sentence describing what this service does and who calls it.]

## Tech stack

- Python [3.12], FastAPI [0.115], Pydantic v2
- DB: [PostgreSQL] via [SQLAlchemy 2.0 async] + [Alembic] migrations
- Tests: pytest + httpx AsyncClient
- Env/deps: [uv] ([poetry] / [pip-tools])
- Lint/format: [ruff]

## Commands

```bash
uv sync                          # install
uv run uvicorn app.main:app --reload
uv run pytest -q                 # tests
uv run pytest --cov=app          # with coverage
uv run ruff check . && uv run ruff format --check .
uv run alembic upgrade head      # apply migrations
```

Done means: `uv run pytest -q` and `uv run ruff check .` both pass.

## Architecture

- `app/main.py`      — app factory and router registration
- `app/api/`         — routers, one module per resource. Thin: validate, delegate, return.
- `app/services/`    — business logic. No FastAPI imports in here.
- `app/models/`      — SQLAlchemy models
- `app/schemas/`     — Pydantic request/response models
- `app/db.py`        — session management
- `tests/`           — mirrors the `app/` layout

Request flow: router -> schema validation -> service -> repository -> DB.

## Conventions

- Type-annotate every function signature.
- Routers never touch the DB session directly — go through a service.
- Raise `HTTPException` only in the router layer; services raise domain errors.
- All I/O is `async`. Never call a blocking library inside an async handler.
- Pydantic schemas are the API contract — changing one is a breaking change.
- Log with structured fields, never f-strings containing user data.

## Boundaries

- Never edit files in `alembic/versions/` — generate a new migration instead.
- Never read or print `.env`, and never log secrets or full request bodies.
- Do not add a dependency without asking.
- `app/auth/` requires review — flag changes, do not silently refactor.

## Build rules

1. Write a failing test that reproduces the bug before fixing it.
2. Schema change => migration in the same commit.
3. Run the full test suite before saying done, and paste the output.
4. Keep functions under ~40 lines; extract rather than nest.
'''

FILES['claude-md/CLAUDE.node-api.md'] = r'''# [SERVICE NAME] — Node back-end

[One sentence: what this service owns.]

## Tech stack

- Node [22 LTS], TypeScript strict, [Express 5] / [Fastify 5]
- DB: [PostgreSQL] via [Prisma] / [Drizzle]
- Queue: [BullMQ + Redis]
- Tests: [Vitest] + supertest
- Package manager: [pnpm]

## Commands

```bash
pnpm install
pnpm dev                 # watch mode
pnpm test                # unit + integration
pnpm test -- --run       # single pass, use this in automation
pnpm lint
pnpm typecheck
pnpm db:migrate
pnpm build
```

## Architecture

- `src/routes/`      — HTTP layer only: parse, validate, call a service, serialise
- `src/services/`    — business logic, framework-free and unit-testable
- `src/repos/`       — all database access lives here
- `src/jobs/`        — background workers
- `src/lib/`         — shared utilities, no framework imports
- `src/config.ts`    — the ONLY place `process.env` is read

## Conventions

- Validate every request body with [zod] at the edge; the rest of the code trusts types.
- No `process.env` outside `config.ts`.
- Errors: throw typed domain errors from services; one error middleware maps them to
  status codes. Never `catch` and return a bare 500.
- Every route needs an integration test covering success, validation failure and auth failure.
- Use `async/await` — no raw promise chains, no callbacks.

## Boundaries

- Never read `.env*` or print secrets.
- Do not change the public API shape in `src/routes/` without flagging it as breaking.
- Migrations are additive — no destructive migration without asking.
- Do not add a dependency without asking.

## Build rules

1. Reproduce with a failing test, then fix.
2. Run `pnpm typecheck && pnpm test -- --run` before reporting done. Paste the output.
3. One logical change per commit.
4. If a change requires touching more than [5] files, plan it with me first.
'''

FILES['claude-md/CLAUDE.data-science.md'] = r'''# [PROJECT NAME] — analysis / data

[One sentence: the question this repo exists to answer.]

## Tech stack

- Python [3.12], pandas [2.2], [scikit-learn] / [polars]
- Notebooks: Jupyter, but production code lives in `src/`
- Env: [uv] / [conda]
- Tests: pytest

## Commands

```bash
uv sync
uv run jupyter lab
uv run python -m src.pipeline.run --config configs/[NAME].yaml
uv run pytest -q
uv run ruff check .
```

## Architecture

- `data/raw/`        — immutable source data. NEVER write here.
- `data/interim/`    — intermediate artefacts, safe to delete and regenerate
- `data/processed/`  — model-ready outputs
- `notebooks/`       — exploration only. Prefixed `NN-initials-topic.ipynb`.
- `src/`             — every function a notebook needs. Notebooks import, not define.
- `configs/`         — YAML config per experiment
- `reports/`         — generated figures and write-ups

## Conventions

- Notebooks explore; `src/` is the source of truth. Once a cell works, move it into `src/`.
- Every transformation is a pure function taking a DataFrame and returning a new one.
- No hardcoded paths — read them from the config.
- Set and record a random seed for anything stochastic.
- State units and time zones in column names or docstrings.
- Print row counts before and after any join or filter. Silent row loss is the number one bug.

## Boundaries

- Never modify anything in `data/raw/`.
- Never commit data files or `.ipynb` outputs — check the gitignore before adding files.
- Do not delete `reports/` artefacts; they are referenced externally.
- Do not silently drop rows to make a merge work. Surface the mismatch.

## Build rules

1. Before analysis, profile the data: dtypes, nulls, duplicates, ranges. Report what you find.
2. State assumptions explicitly in the output, not just in your head.
3. Any number that goes in a report must be reproducible from a committed script.
4. Show the sanity checks you ran, not just the conclusion.
'''

FILES['claude-md/CLAUDE.monorepo.md'] = r'''# [MONOREPO NAME]

[One sentence describing the product this monorepo builds.]

This file covers rules that apply everywhere. Each package has its own `CLAUDE.md`
with rules that apply only inside it — those take precedence for files in that package.

## Layout

```
apps/
  [web]/          [Next.js customer app]      -> apps/web/CLAUDE.md
  [admin]/        [internal dashboard]        -> apps/admin/CLAUDE.md
  [api]/          [backend service]           -> apps/api/CLAUDE.md
packages/
  [ui]/           [shared component library]
  [config]/       [eslint/ts/tailwind presets]
  [types]/        [shared TypeScript types]
```

## Tech stack

- [pnpm] workspaces + [Turborepo]
- TypeScript strict everywhere
- Node [22 LTS]

## Commands

Always run these from the repo root:

```bash
pnpm install
pnpm dev                          # all apps
pnpm --filter [web] dev           # one app
pnpm --filter [web] test
pnpm test                         # everything
pnpm lint
pnpm typecheck
pnpm build
```

## Conventions

- Cross-package imports use the workspace alias (`@repo/ui`), never a relative path
  that climbs out of the package.
- Shared types belong in `packages/types`. If two apps define the same shape, it moves.
- A change to `packages/*` affects every consumer — say which apps you checked.
- Version everything together; no independent package versioning.

## Boundaries

- Do not change `turbo.json`, root `tsconfig.json` or the pnpm workspace file without asking.
- Do not add a dependency to the root `package.json` — add it to the package that uses it.
- Do not create a new package without asking.
- Never read `.env*` in any package.

## Build rules

1. Say which package(s) you are working in before you start.
2. Changing a shared package? Run `pnpm build && pnpm typecheck` at the ROOT, not just
   in that package, and paste the result.
3. Keep changes inside one package per commit where possible.
4. Read the package's own CLAUDE.md before editing files in it.
'''

FILES['hooks/README.md'] = r'''# Hook recipes

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
'''

FILES['hooks/01-format-on-edit.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "statusMessage": "Formatting...",
            "timeout": 60,
            "command": "f=$(jq -r '.tool_input.file_path // empty'); [ -n \"$f\" ] && case \"$f\" in *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.md) npx --no-install prettier --write \"$f\" >/dev/null 2>&1;; esac; exit 0"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/01-format-on-edit.windows.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "statusMessage": "Formatting...",
            "timeout": 60,
            "command": "$j = ($input | Out-String | ConvertFrom-Json); $f = $j.tool_input.file_path; if ($f -and ($f -match '\\.(ts|tsx|js|jsx|json|css|md)$')) { npx --no-install prettier --write $f *> $null }; exit 0"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/02-block-dangerous-bash.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "timeout": 10,
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-dangerous-bash.sh"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/scripts/block-dangerous-bash.sh'] = r'''#!/usr/bin/env bash
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
'''

FILES['hooks/scripts/block-dangerous-bash.ps1'] = r'''# PreToolUse hook for the Bash tool (Windows / PowerShell).
# Reads the hook payload from stdin and exits 2 to BLOCK the command.
# Install to .claude\hooks\block-dangerous-bash.ps1

$ErrorActionPreference = 'Stop'
$payload = $input | Out-String
if (-not $payload.Trim()) { exit 0 }
$cmd = ($payload | ConvertFrom-Json).tool_input.command
if (-not $cmd) { exit 0 }

$patterns = @(
  @{ re = 'rm\s+-[rf]{2}\s+[/~]';        why = 'recursive delete of a root path' },
  @{ re = 'git\s+push\b.*(--force|\s-f)'; why = 'force push' },
  @{ re = 'git\s+reset\s+--hard';         why = 'hard reset discards uncommitted work' },
  @{ re = 'git\s+clean\s+-\w*[fd]';       why = 'git clean would delete untracked files' },
  @{ re = '(DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE\s+)'; why = 'destructive SQL' },
  @{ re = 'chmod\s+-R\s+777';             why = 'world-writable permissions' },
  @{ re = '>>?\s*\.env';                  why = 'writing to .env' },
  @{ re = 'curl[^|]*\|\s*(sh|bash)';      why = 'piping a download straight into a shell' }
)

foreach ($p in $patterns) {
  if ($cmd -match $p.re) {
    [Console]::Error.WriteLine("BLOCKED by block-dangerous-bash hook: $($p.why)")
    [Console]::Error.WriteLine("If this is genuinely what you want, run it yourself in a terminal.")
    exit 2                      # exit 2 = block, stderr goes back to Claude
  }
}
exit 0
'''

FILES['hooks/03-protect-paths.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Edit(./migrations/**)",
      "Edit(./.github/workflows/**)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "timeout": 10,
            "command": "PROTECTED='.env|secrets/|migrations/|.github/workflows/|package-lock.json|pnpm-lock.yaml'; f=$(jq -r '.tool_input.file_path // empty'); if [ -n \"$f\" ] && echo \"$f\" | grep -Eq \"$PROTECTED\"; then echo \"BLOCKED: $f is a protected path. Ask the human before changing it.\" >&2; exit 2; fi; exit 0"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/04-test-after-edit.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "statusMessage": "Running tests...",
            "timeout": 300,
            "command": "f=$(jq -r '.tool_input.file_path // empty'); case \"$f\" in *src/*|*app/*|*lib/*) ;; *) exit 0;; esac; cd \"$CLAUDE_PROJECT_DIR\" || exit 0; out=$(npm test --silent -- --run 2>&1) || { echo \"Tests failed after editing $f:\" >&2; echo \"$out\" | tail -40 >&2; exit 2; }; exit 0"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/05-notify-on-stop.macos.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "async": true,
            "timeout": 10,
            "command": "osascript -e 'display notification \"Claude finished\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/05-notify-on-stop.windows.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "async": true,
            "timeout": 10,
            "command": "[console]::beep(880,150); [console]::beep(1320,200)"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/05-notify-on-stop.linux.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "async": true,
            "timeout": 10,
            "command": "notify-send 'Claude Code' 'Claude finished'"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/06-session-context.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "_comment": "SessionStart stdout IS shown to Claude, so this injects live repo state into context at the start of every session. Cheaper and always-current versus writing it in CLAUDE.md.",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "timeout": 20,
            "command": "cd \"$CLAUDE_PROJECT_DIR\" 2>/dev/null || exit 0; echo '--- repo state ---'; echo \"branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null)\"; echo 'recent commits:'; git log --oneline -5 2>/dev/null; echo 'uncommitted files:'; git status --porcelain 2>/dev/null | head -20; exit 0"
          }
        ]
      }
    ]
  }
}
'''

FILES['hooks/combined-settings.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm test *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "timeout": 20,
            "command": "cd \"$CLAUDE_PROJECT_DIR\" 2>/dev/null || exit 0; echo \"branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null)\"; git log --oneline -5 2>/dev/null; exit 0"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "timeout": 10,
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-dangerous-bash.sh"
          }
        ]
      },
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "timeout": 10,
            "command": "PROTECTED='.env|secrets/|migrations/|.github/workflows/'; f=$(jq -r '.tool_input.file_path // empty'); if [ -n \"$f\" ] && echo \"$f\" | grep -Eq \"$PROTECTED\"; then echo \"BLOCKED: $f is protected.\" >&2; exit 2; fi; exit 0"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "shell": "bash",
            "statusMessage": "Formatting...",
            "timeout": 60,
            "command": "f=$(jq -r '.tool_input.file_path // empty'); [ -n \"$f\" ] && case \"$f\" in *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.md) npx --no-install prettier --write \"$f\" >/dev/null 2>&1;; esac; exit 0"
          }
        ]
      }
    ]
  }
}
'''

FILES['permissions/README.md'] = r'''# Permission defaults

`settings.safe-defaults.json` is a starting `.claude/settings.json`.

- **allow** rules remove the approval prompt for read-only commands you run constantly.
  Every entry here is non-destructive.
- **deny** rules block access to secrets outright, so they cannot be read into context
  by accident.

Permission rules **merge** across every settings file rather than overriding, so keep
this list narrow and add project-specific rules in the project's own settings file.

Add to the allow list as you go: when a prompt appears for a command you will approve
every time, put it here. Never allowlist a command that writes or deletes.
'''

FILES['permissions/settings.safe-defaults.json'] = r'''{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git branch *)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(npm run lint)",
      "Bash(npm run typecheck)",
      "Bash(npm test *)",
      "Bash(pnpm test *)",
      "Bash(uv run pytest *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./**/id_rsa)",
      "Read(./**/*.pem)",
      "Bash(curl * | sh)",
      "Bash(curl * | bash)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
'''

FILES['skills/README.md'] = r'''# Skills

A skill is a folder containing a `SKILL.md` file. Claude reads the `description`
field of every installed skill and pulls the full body into context only when the
request matches — so skills cost almost nothing until they fire.

## Where they go

| Path | Scope |
|---|---|
| `~/.claude/skills/<name>/SKILL.md` | available in every project |
| `.claude/skills/<name>/SKILL.md` | this project only, committed with the repo |

The folder name is the skill name. Run `/skills` in Claude Code to list what is loaded.

## The one thing that matters

The `description` field is the trigger. It is the only part Claude sees before
deciding whether to load the skill, so it must describe **when to use this**, not
what the skill contains.

Bad:  `description: Helps with pull requests`
Good: `description: Writes PR titles and descriptions from a git diff. Use when the
       user asks to open a PR, write a PR description, or summarise a branch.`

## Rules

1. Trigger words in the description, not just topic words.
2. Keep the body tight. It enters context every time the skill fires.
3. One job per skill. Two jobs means two skills with two descriptions.
4. Put long reference material in a sibling file and link to it from SKILL.md.
5. Test it: start a session, phrase a request the way you actually would, and check
   whether it fired.

## In this folder

- `SKILL.template.md` — copy this to start
- `pr-description/SKILL.md` — write a PR from the diff
- `release-notes/SKILL.md` — turn commits into release notes
- `test-writer/SKILL.md` — write tests that match the repo's conventions
'''

FILES['skills/SKILL.template.md'] = r'''---
name: [skill-name-in-kebab-case]
description: [What this does] Use when the user [asks for X], [mentions Y], or [wants Z]. Do not use for [the near-miss case you want to exclude].
---

# [Skill Name]

[One or two sentences: what this skill produces and for whom.]

## When this applies

- [Concrete situation 1]
- [Concrete situation 2]

Do not use this for [the thing people confuse it with] — [what to do instead].

## Steps

1. [First thing to gather or check — be specific about the command or file]
2. [The transformation or decision]
3. [How to present the result]

## Output format

[Show the exact shape you want. A template or a short worked example beats a
description of the format.]

## Rules

- [A constraint that is easy to get wrong]
- [Something to never do]
- [The quality bar: what "done" means here]
'''

FILES['skills/pr-description/SKILL.md'] = r'''---
name: pr-description
description: Writes a pull request title and description from the current branch's diff against the base branch. Use when the user asks to open a PR, write a PR description, summarise a branch, or prepare a change for review.
---

# PR description writer

Turns a branch diff into a PR title and body a reviewer can act on.

## Steps

1. Find the base branch: `git symbolic-ref refs/remotes/origin/HEAD` (fall back to `main`).
2. Read the actual change: `git diff <base>...HEAD --stat` then `git diff <base>...HEAD`.
3. Read the commit messages: `git log <base>..HEAD --oneline`.
4. Write the PR. Describe what changed and WHY — the diff already shows the what.

## Output format

```
<type>: <imperative summary under 70 chars>

## What changed
- <bullet per meaningful change, grouped by area not by file>

## Why
<the problem this solves, in 2-3 sentences>

## How to review
<the file or path to start with, and what to look for>

## Testing
<what was run and the actual result, or "not yet tested">
```

## Rules

- Never claim tests pass unless you ran them and saw the output.
- Do not list every file. Group by intent.
- Flag anything a reviewer would consider risky: schema changes, public API changes,
  deleted code, new dependencies.
- If the diff contains unrelated changes, say so rather than papering over it.
- No emoji unless the repo's existing PRs use them.
'''

FILES['skills/release-notes/SKILL.md'] = r'''---
name: release-notes
description: Turns commits between two git tags or refs into user-facing release notes. Use when the user asks for release notes, a changelog entry, "what shipped in this version", or is preparing a release.
---

# Release notes

Converts a commit range into notes written for users, not for developers.

## Steps

1. Determine the range. Default to `$(git describe --tags --abbrev=0)..HEAD` unless
   the user names two refs.
2. `git log <range> --oneline --no-merges`
3. For anything whose intent is unclear from the subject, read the diff for that commit.
4. Group by user impact, not by commit type.

## Output format

```markdown
## [version] — [YYYY-MM-DD]

### Added
- [Capability, described by what the user can now do]

### Changed
- [What behaves differently, and what to do about it]

### Fixed
- [The symptom the user saw, not the internal cause]

### Breaking
- [What breaks, and the exact migration step]
```

Omit any empty section.

## Rules

- Write from the user's point of view. "Fixed a null pointer in AuthService" becomes
  "Fixed sign-in failing for accounts created before 2024".
- Skip pure refactors, dependency bumps and CI changes unless they change behaviour.
- Breaking changes go first in the reader's attention and must include the migration.
- Never invent a version number or date — ask if it is not obvious.
'''

FILES['skills/test-writer/SKILL.md'] = r'''---
name: test-writer
description: Writes tests that match this repository's existing test conventions. Use when the user asks for tests, says code is untested, asks to reproduce a bug with a test, or asks to raise coverage.
---

# Test writer

Writes tests that look like they were written by whoever wrote the existing suite.

## Steps

1. **Read the neighbours first.** Find 2-3 existing test files near the code under test.
   Copy their framework, imports, naming, setup/teardown and assertion style.
2. Identify what the code under test actually promises: inputs, outputs, side effects,
   and the errors it is documented to raise.
3. Write tests in this order: happy path, boundaries, error cases, then regressions.
4. Run them. Paste the real output.

## Coverage checklist

- [ ] The normal case with realistic data
- [ ] Empty / zero / null input
- [ ] The boundary on each numeric or length limit
- [ ] Each error branch the code can take
- [ ] Anything async: rejection and timeout
- [ ] The specific bug, if this is a regression test

## Rules

- Match the existing suite's conventions over any preference of your own.
- One behaviour per test. A test name should read as a sentence about that behaviour.
- No assertions on internal implementation detail — test the contract.
- Never mock the thing under test. Mock its collaborators only.
- If a test needs a comment to explain what it does, rename the test instead.
- If reproducing a bug: the test must FAIL first. Show that, then fix the code.
'''

FILES['mcp/README.md'] = r'''# MCP server configs

MCP (Model Context Protocol) servers give Claude access to tools and data outside
the chat — your filesystem, a database, an API.

## Two different files

| Client | File | Notes |
|---|---|---|
| Claude Code, project scope | `.mcp.json` in the repo root | Committed. Claude Code asks for approval before using it. |
| Claude Code, user scope | `~/.claude.json` | Available in all your projects. Easiest via the CLI. |
| Claude Desktop | `claude_desktop_config.json` | Restart the app after editing. |

Claude Desktop config location:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Easier than editing JSON

Claude Code can add servers for you:

```bash
claude mcp add --scope project filesystem -- npx -y @modelcontextprotocol/server-filesystem [ABSOLUTE_PATH]
claude mcp add --transport http [NAME] --scope project [URL]
claude mcp list
claude mcp reset-project-choices     # re-prompt for .mcp.json approvals
```

## A note on server packages

The official reference servers under `@modelcontextprotocol/` are a small, stable
set — filesystem, memory, sequential-thinking, fetch, git, time, everything.

Many first-party integrations have moved to the vendor's own package or to a hosted
HTTP endpoint rather than a local npm package. Before wiring up a service, check that
vendor's current MCP docs rather than assuming an `@modelcontextprotocol/server-*`
package still exists for it. `.mcp.http.json` shows the hosted form.

## The files here

| File | For |
|---|---|
| `.mcp.json` | Claude Code, project scope. Three local stdio servers. |
| `.mcp.http.json` | The hosted/HTTP form — a `url` instead of a `command`. |
| `claude_desktop_config.json` | Claude Desktop. **Restart the app after editing.** |

On Windows, paths inside JSON need **double** backslashes:
`"C:\\Users\\YourName\\Documents\\Project"`.

## Security

An MCP server runs with your permissions and can read whatever you point it at.
Scope the filesystem server to a specific directory — never your home folder or `/`.
Keep tokens in environment variables, not inline in a committed `.mcp.json`.
'''

FILES['mcp/.mcp.json'] = r'''{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "[ABSOLUTE_PATH_TO_A_SPECIFIC_PROJECT_FOLDER]"
      ]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
'''

FILES['mcp/.mcp.http.json'] = r'''{
  "mcpServers": {
    "[vendor-name]": {
      "type": "http",
      "url": "[https://mcp.example.com/mcp]"
    },
    "[vendor-with-auth]": {
      "type": "http",
      "url": "[https://mcp.example.com/mcp]",
      "headers": {
        "Authorization": "Bearer ${[VENDOR_API_TOKEN]}"
      }
    }
  }
}
'''

FILES['mcp/claude_desktop_config.json'] = r'''{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "[C:\\Users\\YOUR_NAME\\Documents\\ProjectFolder]"
      ]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
'''


# =========================================================== PDF INDEX GUIDE

def wrap(text, size, width, font='Helvetica'):
    return simpleSplit(text, font, size, width)


def pg_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def hdr(c):
    c.setFillColor(OG)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)


def ftr(c, n):
    c.setFillColor(PNL)
    c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica', 8)
    c.drawString(MX, 7, 'Claude AI Field Guide Series  \u00b7  %s' % GUIDE)
    c.setFillColor(MGR)
    c.drawRightString(W - MX, 7, 'Page %d' % n)


def h2(c, y, text):
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y, text)
    return y - 22


def body(c, y, text, w=CW):
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    for line in wrap(text, 10, w):
        c.drawString(MX, y, line)
        y -= 15
    return y


def info_panel(c, x, y, heading, lines, w):
    pad = 12
    ph = len(lines) * 16 + pad * 2 + 22
    c.setFillColor(PNL)
    c.roundRect(x, y - ph, w, ph, radius=4, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(x + pad, y - pad - 12, heading)
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    ty = y - pad - 30
    for line in lines:
        c.drawString(x + pad, ty, line)
        ty -= 16
    return y - ph


def tip_box(c, x, y, heading, lines, w):
    pad = 10
    bh = len(lines) * 15 + pad * 2 + 20
    c.setFillColor(DBGRN)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(GRN)
    c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(GRN)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 14, y - pad - 10, 'TIP  %s' % heading)
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    ty = y - pad - 26
    for line in lines:
        c.drawString(x + 14, ty, line)
        ty -= 15
    return y - bh


def warn_box(c, x, y, heading, lines, w):
    pad = 10
    bh = len(lines) * 15 + pad * 2 + 20
    c.setFillColor(DBAMB)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(AMB)
    c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(AMB)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 14, y - pad - 10, 'WARNING  %s' % heading)
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    ty = y - pad - 26
    for line in lines:
        c.drawString(x + 14, ty, line)
        ty -= 15
    return y - bh


def code_block(c, x, y, lines, w):
    pad, lh = 10, 13
    bh = len(lines) * lh + pad * 2
    c.setFillColor(CODEBG)
    c.roundRect(x, y - bh, w, bh, radius=3, fill=1, stroke=0)
    c.setStrokeColor(OG)
    c.setLineWidth(0.5)
    c.roundRect(x, y - bh, w, bh, radius=3, fill=0, stroke=1)
    c.setFont('Courier', 9)
    ty = y - pad - 8
    for line in lines:
        c.setFillColor(MGR if line.strip().startswith('#') else GRN)
        c.drawString(x + pad, ty, line)
        ty -= lh
    return y - bh


def tbl(c, x, y, headers, rows, col_w):
    rh, pad = 22, 7
    tw = sum(col_w)
    c.setFillColor(OG)
    c.rect(x, y - rh, tw, rh, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 9)
    cx = x
    for i, hh in enumerate(headers):
        c.drawString(cx + pad, y - rh + 7, hh)
        cx += col_w[i]
    for ri, row in enumerate(rows):
        ry = y - rh * (ri + 2)
        c.setFillColor(PNL2 if ri % 2 == 0 else PNL)
        c.rect(x, ry, tw, rh, fill=1, stroke=0)
        cx = x
        for ci, cell in enumerate(row):
            c.setFillColor(OGL if ci == 0 else LGR)
            c.setFont('Helvetica-Bold' if ci == 0 else 'Helvetica', 9)
            c.drawString(cx + pad, ry + 7, str(cell))
            cx += col_w[ci]
    return y - rh * (len(rows) + 1)


def cover(c, nfiles):
    pg_bg(c)
    c.setFillColor(OG)
    c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    c.setFillColor(DOG)
    c.circle(W - 68, H - 48, 56, fill=1, stroke=0)
    c.circle(W - 140, H - 124, 30, fill=1, stroke=0)
    c.setFillColor(DDOG)
    c.circle(60, H - 126, 22, fill=1, stroke=0)

    c.setFillColor(DDOG)
    c.roundRect(MX, H - 66, 150, 24, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 10, H - 59, 'TEMPLATE FILE PACK')
    c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 92, 'CLAUDE AI FIELD GUIDE SERIES')
    c.setFont('Helvetica', 8)
    c.drawString(MX, H - 108, '2026 EDITION')

    y = H - 208
    c.setFillColor(CREAM)
    c.setFont('Helvetica-Bold', 30)
    c.drawString(MX, y, 'Claude Code')
    y -= 36
    c.drawString(MX, y, 'Config Pack')
    y -= 30
    c.setFillColor(OGL)
    c.setFont('Helvetica', 14)
    for line in wrap('Copy-paste CLAUDE.md, hooks, skills and MCP configs that work out of the box', 14, CW):
        c.drawString(MX, y, line)
        y -= 19

    y -= 18
    c.setFillColor(PNL)
    c.roundRect(MX, y - 52, CW, 52, radius=5, fill=1, stroke=0)
    stats = [(str(nfiles), 'FILES'), ('6', 'CLAUDE.MD'), ('6', 'HOOK RECIPES'), ('4', 'SKILLS')]
    colw = CW / len(stats)
    for i, (big, small) in enumerate(stats):
        cx = MX + colw * i + colw / 2
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 19)
        c.drawCentredString(cx, y - 27, big)
        c.setFillColor(MGR)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(cx, y - 42, small)
    y -= 52

    bullets = [
        '6 CLAUDE.md build-plan templates for real stacks',
        '6 hook recipes for .claude/settings.json (Mac + Windows)',
        'Guard scripts that block rm -rf and force pushes',
        'SKILL.md template plus 3 working example skills',
        'MCP configs for Claude Code and Claude Desktop',
        'Safe permission defaults that cut approval prompts',
    ]
    y -= 20
    ph = len(bullets) * 17 + 44
    c.setFillColor(PNL)
    c.roundRect(MX, y - ph, CW, ph, radius=5, fill=1, stroke=0)
    c.setFillColor(OG)
    c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 14, y - 22, "WHAT'S INSIDE")
    for i, b in enumerate(bullets):
        ty = y - 44 - i * 17
        c.setFillColor(GRN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 14, ty, 'v')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 10)
        c.drawString(MX + 28, ty, b)

    c.setFillColor(OG)
    c.rect(0, 0, W, 40, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 16, 'REAL FILES  \u00b7  NOT SCREENSHOTS  \u00b7  EDIT THE BRACKETS AND GO')
    c.showPage()


def page2(c):
    pg_bg(c)
    hdr(c)
    y = H - 30
    y = h2(c, y - 20, "What's in the pack, and where it goes")
    y = body(c, y, 'Unzip the pack anywhere. Nothing installs. Every file is plain text you copy '
                   'into your own project and edit — the bracketed blanks show you exactly what to change.')
    y -= 12
    y = tbl(c, MX, y, ['FOLDER', 'CONTENTS', 'INSTALL TO'],
            [['claude-md/', '6 build-plan templates', 'CLAUDE.md in repo root'],
             ['hooks/', '6 recipes + guard scripts', '.claude/settings.json'],
             ['skills/', 'template + 3 examples', '~/.claude/skills/<name>/'],
             ['mcp/', 'server configs', '.mcp.json / desktop config'],
             ['permissions/', 'safe defaults', '.claude/settings.json']],
            [95, 210, 213.4])
    y -= 18
    y = info_panel(c, MX, y, 'SETTINGS FILE PRECEDENCE (HIGHEST WINS)',
                   ['1  Managed / enterprise policy',
                    '2  Command-line flags',
                    '3  .claude/settings.local.json   personal, gitignored',
                    '4  .claude/settings.json         shared with the team',
                    '5  ~/.claude/settings.json       your global defaults'], CW)
    y -= 16
    y = tip_box(c, MX, y, 'Permission rules merge',
                ['Permission allow/deny lists combine across all five files rather than',
                 'overriding. Most other settings do not — the highest file wins outright.'], CW)
    y -= 16
    warn_box(c, MX, y, 'Read before you paste',
             ['Hooks run shell commands on your machine automatically, with your',
              'permissions. Read every command in this pack before installing it —',
              'and apply the same rule to any hook you find anywhere else.'], CW)
    ftr(c, 2)
    c.showPage()


def page3(c):
    pg_bg(c)
    hdr(c)
    y = H - 30
    y = h2(c, y - 20, 'CLAUDE.md — the file Claude reads every session')
    y = body(c, y, 'CLAUDE.md sits in your repo root and loads automatically at the start of every '
                   'session. It is the cheapest possible way to stop repeating yourself.')
    y -= 12
    y = tbl(c, MX, y, ['TEMPLATE', 'USE IT FOR'],
            [['CLAUDE.starter.md', 'Any project. Start here if unsure.'],
             ['CLAUDE.nextjs-react.md', 'Next.js / React front-ends'],
             ['CLAUDE.python-fastapi.md', 'Python services and APIs'],
             ['CLAUDE.node-api.md', 'Node / Express / Fastify back-ends'],
             ['CLAUDE.data-science.md', 'Notebooks, pipelines, analysis repos'],
             ['CLAUDE.monorepo.md', 'Multi-package repos with per-package rules']],
            [175, 343.4])
    y -= 18
    y = info_panel(c, MX, y, 'THE SIX RULES THAT MAKE IT WORK',
                   ['1  Under ~150 lines. It is re-read every session.',
                    '2  Only what you verified. A wrong build command is worse than none.',
                    '3  Commands must be copy-pasteable, not described.',
                    '4  State boundaries: what to never touch, what needs asking.',
                    '5  Link out for detail instead of inlining it.',
                    '6  It is advisory. For rules that MUST hold, use a hook.'], CW)
    y -= 16
    y = code_block(c, MX, y,
                   ['# where CLAUDE.md files can live',
                    '~/.claude/CLAUDE.md          # every project on this machine',
                    './CLAUDE.md                  # this project, shared with the team',
                    './.claude/CLAUDE.local.md    # this project, just you (gitignore it)',
                    './src/api/CLAUDE.md          # extra rules inside that folder only'], CW)
    ftr(c, 3)
    c.showPage()


def page4(c):
    pg_bg(c)
    hdr(c)
    y = H - 30
    y = h2(c, y - 20, 'Hooks — rules that always run')
    y = body(c, y, 'CLAUDE.md asks. Hooks enforce. A hook is a shell command Claude Code runs '
                   'automatically at a defined point, and it cannot be talked out of running.')
    y -= 12
    y = code_block(c, MX, y,
                   ['# .claude/settings.json  — the shape of every hook',
                    '{ "hooks": {',
                    '    "PostToolUse": [ {',
                    '        "matcher": "Edit|Write",',
                    '        "hooks": [ { "type": "command",',
                    '                     "command": "your-command",',
                    '                     "timeout": 60 } ] } ] } }'], CW)
    y -= 16
    y = info_panel(c, MX, y, 'TWO THINGS PEOPLE GET WRONG',
                   ['Your command gets JSON on STDIN, not arguments. Pull the file path',
                    'out with:   jq -r \'.tool_input.file_path\'',
                    '',
                    'EXIT CODE 2 blocks. Exit 1 does not — it is a non-blocking error.',
                    'On exit 2, stderr is fed back to Claude as the reason.'], CW)
    y -= 16
    y = tbl(c, MX, y, ['RECIPE', 'EVENT', 'WHAT IT DOES'],
            [['01 format-on-edit', 'PostToolUse', 'Prettier on every edited file'],
             ['02 block-dangerous', 'PreToolUse', 'Stops rm -rf, force push, drops'],
             ['03 protect-paths', 'PreToolUse', 'Blocks edits to .env, migrations'],
             ['04 test-after-edit', 'PostToolUse', 'Runs tests, feeds failures back'],
             ['05 notify-on-stop', 'Stop', 'Desktop alert when Claude finishes'],
             ['06 session-context', 'SessionStart', 'Injects git branch + recent commits']],
            [125, 105, 288.4])
    y -= 16
    tip_box(c, MX, y, 'Check what actually registered',
            ['Run /hooks inside Claude Code to see every hook it loaded. If a recipe',
             'does not appear, the JSON did not merge — check for a duplicate key.'], CW)
    ftr(c, 4)
    c.showPage()


def page5(c):
    pg_bg(c)
    hdr(c)
    y = H - 30
    y = h2(c, y - 20, 'Skills and MCP servers')
    y = body(c, y, 'A skill is a folder with a SKILL.md file. Claude reads only the description '
                   'field until a request matches — so skills cost almost nothing until they fire.')
    y -= 12
    y = code_block(c, MX, y,
                   ['# ~/.claude/skills/pr-description/SKILL.md',
                    '---',
                    'name: pr-description',
                    'description: Writes a PR title and body from the branch diff.',
                    '  Use when the user asks to open a PR, write a PR description,',
                    '  or summarise a branch.',
                    '---',
                    '',
                    '# PR description writer',
                    '...instructions go here...'], CW)
    y -= 16
    y = warn_box(c, MX, y, 'The description IS the trigger',
                 ['It is the only part Claude sees before deciding to load the skill.',
                  'Write when to use this, not what it contains. "Helps with pull',
                  'requests" will never fire reliably.'], CW)
    y -= 16
    y = body(c, y, 'MCP servers connect Claude to tools and data outside the chat. Claude Code '
                   'can write the config for you:')
    y -= 6
    y = code_block(c, MX, y,
                   ['# add a filesystem server, scoped to this project',
                    'claude mcp add --scope project filesystem -- \\',
                    '  npx -y @modelcontextprotocol/server-filesystem /path/to/folder',
                    '',
                    'claude mcp list                      # see what is connected',
                    'claude mcp reset-project-choices     # re-prompt for approvals'], CW)
    y -= 16
    tip_box(c, MX, y, 'Scope the filesystem server narrowly',
            ['Point it at one project folder, never your home directory or a drive',
             'root. An MCP server can read everything you give it access to.'], CW)
    ftr(c, 5)
    c.showPage()


def page6(c):
    pg_bg(c)
    hdr(c)
    y = H - 30
    y = h2(c, y - 20, 'Quick reference')
    y = tbl(c, MX, y, ['WHAT', 'WHERE'],
            [['Project memory', 'CLAUDE.md (repo root)'],
             ['Global memory', '~/.claude/CLAUDE.md'],
             ['Team settings + hooks', '.claude/settings.json'],
             ['Personal settings', '.claude/settings.local.json'],
             ['Global settings', '~/.claude/settings.json'],
             ['Skills', '~/.claude/skills/<name>/SKILL.md'],
             ['Subagents', '.claude/agents/<name>.md'],
             ['Project MCP servers', '.mcp.json (repo root)'],
             ['Desktop MCP (Win)', '%APPDATA%\\Claude\\claude_desktop_config.json']],
            [175, 343.4])
    y -= 16
    y = info_panel(c, MX, y, 'HOOK EXIT CODES',
                   ['0   success — stdout parsed for JSON directives',
                    '2   BLOCK — stderr is sent back to Claude as the reason',
                    'other   non-blocking error, logged, execution continues'], CW)
    y -= 16
    y = tbl(c, MX, y, ['PROBLEM', 'FIX'],
            [['Hook never fires', 'Run /hooks. Check the matcher spelling.'],
             ['Hook fires, nothing happens', 'Command needs stdin JSON, not $1'],
             ['Block not working', 'Use exit 2, not exit 1'],
             ['jq: command not found', 'Install jq, or use the .windows.json recipe'],
             ['MCP server not listed', 'Restart the client after editing config'],
             ['Skill never triggers', 'Description too vague — add trigger words'],
             ['Settings ignored', 'A higher-precedence file is overriding it']],
            [175, 343.4])
    y -= 18
    ph = 62
    c.setFillColor(PNL)
    c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
    c.setStrokeColor(OG)
    c.setLineWidth(1)
    c.roundRect(MX, y - ph, CW, ph, radius=4, fill=0, stroke=1)
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 14, y - 22, 'GOES WITH')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    c.drawString(MX + 14, y - 40, 'Guide 11 CLAUDE.md Files  \u00b7  Guide 12 Subagents & Hooks')
    c.drawString(MX + 14, y - 54, 'Guide 15 Installing MCP Servers  \u00b7  Guide 17 Claude Skills')
    ftr(c, 6)
    c.showPage()


# ==================================================================== BUILD

def write_tree():
    if os.path.isdir(PACK):
        shutil.rmtree(PACK)
    for rel, content in FILES.items():
        path = os.path.join(PACK, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
    return len(FILES)


def zip_pack():
    zpath = os.path.join(OUTDIR, 'Claude_Config_Pack.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, names in os.walk(PACK):
            for n in names:
                full = os.path.join(root, n)
                arc = os.path.join('Claude_Config_Pack', os.path.relpath(full, PACK))
                z.write(full, arc)
    return zpath


def build_pdf(nfiles):
    path = os.path.join(OUTDIR, 'Claude_Config_Pack_Guide.pdf')
    c = canvas.Canvas(path, pagesize=LETTER)
    c.setTitle('Claude Code Config Pack')
    c.setAuthor('Claude AI Field Guide Series')
    cover(c, nfiles)
    page2(c)
    page3(c)
    page4(c)
    page5(c)
    page6(c)
    c.save()
    return path


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    n = write_tree()
    pdf = build_pdf(n)
    z = zip_pack()
    print('%d files written to %s' % (n, PACK))
    print('%-36s %d KB' % (os.path.basename(pdf), os.path.getsize(pdf) / 1024))
    print('%-36s %d KB' % (os.path.basename(z), os.path.getsize(z) / 1024))


if __name__ == '__main__':
    main()
