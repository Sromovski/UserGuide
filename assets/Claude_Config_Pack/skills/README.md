# Skills

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
