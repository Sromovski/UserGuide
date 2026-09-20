# [APP NAME] — Next.js front-end

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
