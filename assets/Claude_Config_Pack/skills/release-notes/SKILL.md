---
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
