# [MONOREPO NAME]

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
