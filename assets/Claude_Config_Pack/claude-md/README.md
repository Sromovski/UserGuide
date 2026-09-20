# CLAUDE.md templates

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
