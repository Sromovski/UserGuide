# [SERVICE NAME] — Node back-end

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
