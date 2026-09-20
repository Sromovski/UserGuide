# Permission defaults

`settings.safe-defaults.json` is a starting `.claude/settings.json`.

- **allow** rules remove the approval prompt for read-only commands you run constantly.
  Every entry here is non-destructive.
- **deny** rules block access to secrets outright, so they cannot be read into context
  by accident.

Permission rules **merge** across every settings file rather than overriding, so keep
this list narrow and add project-specific rules in the project's own settings file.

Add to the allow list as you go: when a prompt appears for a command you will approve
every time, put it here. Never allowlist a command that writes or deletes.
