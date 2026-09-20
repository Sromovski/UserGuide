---
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
