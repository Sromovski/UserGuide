# [PROJECT NAME]

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
