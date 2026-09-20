#!/usr/bin/env python3
"""Copilot Field Guide — Volume 3: The CLI & the Coding Agent.

    python build_copilot_v3.py

Copilot outside the editor: in your terminal, and running on GitHub's own infrastructure
while you do something else.

FACTS VERIFIED 2026-08-02 against docs.github.com/copilot. Load-bearing numbers, all from
the docs rather than secondary write-ups: the cloud agent runs in an ephemeral GitHub
Actions environment, has a HARD 59-minute execution limit, and is confined to ONE repo,
ONE branch and ONE pull request per task. Its PRs require human approval before CI runs.
"""
import os

from fieldguide import COPILOT, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Copilot_Field_Guide_Volume_3_CLI_and_Coding_Agent.pdf')

CHAPTERS = [
    (1, 'Copilot in the Terminal', 'The CLI — explain, suggest, and when not to trust it', 3),
    (2, 'The Cloud Coding Agent', 'What it is, and how it differs from agent mode', 8),
    (3, 'Handing It Work', 'Issues, @copilot mentions, the agents panel, workflows', 13),
    (4, 'The Pull Request', 'Draft PRs, session logs, steering it mid-run, reviewing', 18),
    (5, 'Review & Guardrails', 'Automated review, branch protection, what to lock down', 23),
]


# ══════════════════════════════════════════════════════ CH 1 — THE CLI

def ch1(v):
    lbl = 'Chapter 1  ·  Copilot in the Terminal'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Installing the CLI')
    y = p.body(MX, y - 6,
               'The CLI is a GitHub CLI extension. If you already have gh installed and '
               'authenticated, it is one command away.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Prerequisite — the GitHub CLI itself',
        'gh auth status              # already signed in?',
        'gh auth login               # if not',
        '',
        '# The Copilot extension',
        'gh extension install github/gh-copilot',
        'gh copilot --version',
        '',
        '# Keep it current',
        'gh extension upgrade gh-copilot',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'WHAT YOU NEED', [
        'An active paid Copilot plan — the same one your editor uses.',
        'The GitHub CLI (gh), authenticated to the account holding that plan.',
        'Nothing else. There is no separate CLI subscription.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Everything the CLI does is metered', [
        'Editor completions are free. The CLI is not — every explain and suggest',
        'draws on AI Credits. It is a convenience, not the free part of Copilot.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Two Copilots in a terminal')
    y -= 4
    p.table(MX, y, ['This volume', 'What it is'], [
        ('gh copilot (chapter 1)', 'Answers about commands, on your machine'),
        ('The cloud agent (chapters 2-5)', 'Writes code on GitHub, opens a PR'),
    ], [220, CW - 220])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Two Commands')
    y -= 6
    y = p.subheading(MX, y, 'explain — what does this do?')
    y -= 4
    y = p.body(MX, y, 'Paste in a command you do not recognise and get it broken down '
                      'flag by flag. This is the one worth building a habit around.')
    y -= 6
    y = p.code_block(MX, y, [
        'gh copilot explain "tar -xzvf archive.tar.gz -C /opt"',
        'gh copilot explain "git reset --hard origin/main"',
        'gh copilot explain "find . -mtime +30 -delete"',
    ])
    y -= 14
    y = p.subheading(MX, y, 'suggest — what is the command for...?')
    y -= 4
    y = p.body(MX, y, 'Describe the outcome and get a command back. It asks whether you '
                      'want a shell command, a gh command, or a git command.')
    y -= 6
    y = p.code_block(MX, y, [
        'gh copilot suggest "find every file over 100MB in this directory"',
        'gh copilot suggest "undo my last commit but keep the changes"',
        'gh copilot suggest "list open PRs assigned to me"',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'explain before you run, not after it breaks', [
        'A fraction of a credit to understand a command beats an afternoon undoing',
        'one. This is the single highest-value habit in the chapter.',
    ])
    y -= 14
    p.info_panel(MX, y, 'IT ANSWERS, IT DOES NOT ACT', [
        'Neither command runs anything. suggest hands you a command to copy; explain',
        'describes one you already have. Every execution is still a deliberate act by',
        'you — which is the whole reason the CLI is safe to use casually.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Where the CLI Genuinely Wins')
    y -= 6
    y = p.table(MX, y, ['Use it for', 'Rather than'], [
        ('A flag you use twice a year', 'Ten minutes in a man page'),
        ('Understanding before running', 'Running it and finding out'),
        ('Long pipelines of standard tools', 'Trial and error in the shell'),
        ('Git commands you half-remember', 'A search engine and three wrong answers'),
        ('gh subcommands you never learned', 'Reading the whole gh help tree'),
    ], [250, CW - 250])
    y -= 16
    y = p.table(MX, y, ['Do NOT use it for', 'Why'], [
        ('Anything destructive, unread', 'It will confidently suggest rm and dd'),
        ('Production commands', 'A plausible-looking flag can be very wrong'),
        ('Anything with credentials', 'Do not paste secrets into a prompt'),
        ('Learning a tool properly', 'It gives answers, not understanding'),
    ], [250, CW - 250])
    y -= 14
    y = p.warn_box(MX, y, 'Read every suggestion before you run it', [
        'The CLI suggests; it does not execute without you. That boundary is the',
        'entire safety model, and it only works if you actually read the output.',
    ])
    y -= 14
    p.info_panel(MX, y, 'THE COMMANDS WORTH EXPLAINING EVERY TIME', [
        'Anything with rm, dd, mkfs, chmod -R, or a redirect into a file that',
        'already exists. Anything with --force or --hard. Anything you copied out',
        'of a forum post. The cost of checking is a rounding error; the cost of not',
        'checking is occasionally your afternoon.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Working It Into Your Shell')
    y = p.body(MX, y - 6,
               'Two short aliases remove enough friction that you will actually use it.')
    y -= 10
    y = p.code_block(MX, y, [
        '# ~/.zshrc or ~/.bashrc',
        'alias cx="gh copilot explain"',
        'alias cs="gh copilot suggest"',
        '',
        '# then:',
        'cx "awk \'{print $3}\' access.log | sort | uniq -c"',
        'cs "compress this folder but skip node_modules"',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'ALIAS THE EXPLAIN ONE FIRST', [
        'Most people install the CLI, use suggest twice, and forget it exists.',
        'The habit that sticks is explain — because you meet commands you do not',
        'recognise far more often than you fail to think of one.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Inline chat in the editor terminal is a third option', [
        'Ctrl+I inside VS Code\'s integrated terminal gives you the same help without',
        'leaving the editor. Same credits, one less context switch.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Which to reach for')
    y -= 4
    p.table(MX, y, ['You are', 'Use'], [
        ('In a terminal, outside the editor', 'gh copilot'),
        ('In the editor\'s integrated terminal', 'Ctrl+I inline chat'),
        ('Wanting it to change files', 'Neither — that is agent mode, Volume 2'),
    ], [250, CW - 250])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'CLI Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('gh: command not found', 'Install the GitHub CLI first — gh is the host'),
        ('unknown command "copilot"', 'gh extension install github/gh-copilot'),
        ('Authentication errors', 'gh auth status, then gh auth login'),
        ('Works in editor, not CLI', 'gh is authed as a different account'),
        ('Refuses with a quota message', 'Out of credits — see Volume 1 chapter 2'),
        ('Suggestions feel stale', 'gh extension upgrade gh-copilot'),
        ('Nothing happens on a proxy', 'gh needs outbound HTTPS; check proxy config'),
    ], [220, CW - 220])
    y -= 16
    y = p.subheading(MX, y, 'The account trap')
    y -= 4
    y = p.body(MX, y, 'The most common confusion by far: your editor is signed in as one '
                      'GitHub account and gh as another. The editor works, the CLI does '
                      'not, and nothing in the error makes that obvious. Check '
                      'gh auth status before anything else.')
    y -= 8
    y = p.info_panel(MX, y, 'NEXT', [
        'That is Copilot in your terminal, running on your machine, one command at a',
        'time. The rest of this volume is Copilot running on GitHub\'s machines,',
        'unattended, for up to an hour at a stretch.',
    ])
    y -= 14
    p.tip_box(MX, y, 'The CLI is the low-stakes way in', [
        'If the cloud agent feels like a lot of trust to extend, spend a week on the',
        'CLI first. It costs almost nothing, it changes nothing, and it builds the',
        'habit of reading what a machine suggests before acting on it — which is the',
        'skill the rest of this volume depends on.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 2 — CLOUD AGENT

def ch2(v):
    lbl = 'Chapter 2  ·  The Cloud Coding Agent'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Different Thing To Agent Mode')
    y = p.body(MX, y - 6,
               'Volume 2 covered agent mode: an agent running in your editor, on your '
               'machine, while you watch. The cloud coding agent runs on GitHub\'s '
               'infrastructure, without you, and hands back a pull request.')
    y -= 10
    y = p.table(MX, y, ['', 'Agent mode (V2)', 'Cloud agent'], [
        ('Runs on', 'Your machine', 'GitHub Actions'),
        ('You are', 'Watching', 'Elsewhere'),
        ('Approval', 'Per tool call', 'At the pull request'),
        ('Output', 'Edits in your editor', 'A draft PR'),
        ('Good for', 'Work you want to steer', 'Work you can describe and leave'),
    ], [90, 175, CW - 265])
    y -= 16
    y = p.info_panel(MX, y, 'THE ENVIRONMENT', [
        'Ephemeral, powered by GitHub Actions. It can explore the code, make',
        'changes, run tests and run linters — then it is torn down. Nothing',
        'persists between sessions except the commits it pushed.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'The mental model that works', [
        'Treat it as a capable contractor you brief in writing and review on the way',
        'out — not as a pair programmer. You do not get to correct it mid-thought.',
    ])
    y -= 14
    p.info_panel(MX, y, 'WHY THIS ONE IS DIFFERENT TO EVERYTHING SO FAR', [
        'Completions, chat and agent mode all keep you in the loop by the second.',
        'This does not. The quality of what comes back is set almost entirely before',
        'it starts — by how well you described the job. That is why chapter 2 ends',
        'with a page on writing the issue rather than a page on using the tool.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Hard Limits')
    y = p.body(MX, y - 6,
               'These are documented constraints, not guidance. Designing a task that '
               'violates one guarantees a failed run.')
    y -= 10
    y = p.table(MX, y, ['Limit', 'Consequence'], [
        ('59 minutes maximum', 'A hard stop. Long tasks simply do not finish'),
        ('One repository per session', 'No cross-repo changes, at all'),
        ('One branch per task', 'It cannot work two branches at once'),
        ('One pull request per task', 'Everything lands in a single PR'),
        ('GitHub-hosted repos only', 'Self-hosted or mirrored elsewhere will not work'),
    ], [200, CW - 200])
    y -= 16
    y = p.warn_box(MX, y, 'The 59-minute limit shapes everything', [
        'It is a ceiling, not a target. A task that needs 50 minutes is a task that',
        'was scoped too big — split it. Work that runs out of time does not fail',
        'gracefully into something useful; you get an unfinished branch.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'BY DEFAULT IT SEES ONE REPOSITORY', [
        'Context is limited to the repository you pointed it at. Broader access can',
        'be configured through MCP settings, but the default is deliberately narrow',
        'and that default is usually the right one.',
    ])
    y -= 14
    p.tip_box(MX, y, 'Design tasks that finish in twenty minutes', [
        'Not because the limit is twenty, but because a task that would take fifty',
        'has no margin for the exploration it will inevitably do first. Aim well',
        'inside the ceiling and the ceiling stops mattering.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Who Can Use It')
    y -= 6
    y = p.table(MX, y, ['Plan', 'Availability'], [
        ('Free', 'No'),
        ('Pro / Pro+ / Max', 'Yes'),
        ('Business', 'Yes — an administrator must enable it'),
        ('Enterprise', 'Yes — an administrator must enable it'),
    ], [180, CW - 180])
    y -= 16
    y = p.subheading(MX, y, 'If you are on a team and it is missing')
    y -= 4
    y = p.body(MX, y, 'It is almost always a policy setting rather than a bug. Copilot '
                      'features on Business and Enterprise are administrator-controlled, '
                      'and the coding agent is one an organisation may deliberately have '
                      'switched off. Ask before you debug.')
    y -= 8
    y = p.info_panel(MX, y, 'IT DRAWS ON CREDITS', [
        'Like everything in Volume 2, the cloud agent is metered. A run that explores',
        'a large repository for the best part of an hour is not a cheap operation —',
        'scope it as carefully as you would an editor agent task, and more so.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Try it on something small first', [
        'A typo fix, a missing test, a dependency bump. You learn the whole loop —',
        'assign, watch, review, merge — for almost nothing.',
    ])
    y -= 14
    p.info_panel(MX, y, 'A GOOD FIRST TASK', [
        'Find an issue in your backlog that is genuinely well written, genuinely',
        'small, and that you would be mildly relieved not to do yourself. If nothing',
        'in your backlog fits that description, that is worth knowing too — it means',
        'the issues are the thing to fix before the tooling.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What To Give It')
    y = p.body(MX, y - 6,
               'The cloud agent suits work that is well defined, self-contained, and '
               'boring enough that you would rather not do it.')
    y -= 10
    y = p.table(MX, y, ['Good candidates', 'Why it works'], [
        ('Fixing a well-described bug', 'The report is the specification'),
        ('Adding tests to one module', 'Clear finish line — they pass or they do not'),
        ('Dependency bumps', 'Mechanical, verifiable by CI'),
        ('Applying a lint rule repo-wide', 'Repetitive and tedious for a person'),
        ('Small, isolated features', 'If you can describe it fully in an issue'),
        ('Documentation from code', 'Bounded, low risk if imperfect'),
    ], [220, CW - 220])
    y -= 16
    y = p.table(MX, y, ['Bad candidates', 'Why it fails'], [
        ('Anything spanning repos', 'A hard limit, not a difficulty'),
        ('Architecture decisions', 'It will choose, not consult'),
        ('Vague quality work', 'No finish line inside 59 minutes'),
        ('Anything security-sensitive', 'You want a human on that diff first'),
    ], [220, CW - 220])
    y -= 16
    y = p.subheading(MX, y, 'The question that sorts them')
    y -= 4
    p.body(MX, y, 'Could you hand this to a competent contractor who has never seen your '
                  'product, with no chance to ask you anything, and expect something '
                  'useful back? If yes, it is a cloud agent task. If the honest answer is '
                  '"they would need to ask me two or three things first", it belongs in '
                  'the editor where you can answer them.')
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Writing an Issue It Can Finish')
    y = p.body(MX, y - 6,
               'The issue IS the prompt. Everything Volume 2 said about scoping agent '
               'tasks applies, but harder — nobody is watching to catch a '
               'misunderstanding in the first two steps.')
    y -= 10
    y = p.code_block(MX, y, [
        '## Problem',
        'discount_for() returns a negative price when quantity exceeds 100.',
        '',
        '## Expected',
        'The discount caps at 40%. Price never goes below zero.',
        '',
        '## Where',
        'services/pricing.py, function discount_for()',
        '',
        '## How to verify',
        'pytest tests/test_pricing.py must pass, including a new case for',
        'quantity=500 asserting the cap.',
        '',
        '## Out of scope',
        'Do not change the tax calculation or touch any other module.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Five headings, every time', [
        'Problem, expected, where, how to verify, out of scope. An issue with all',
        'five is one an agent can finish. An issue missing "how to verify" is one',
        'it will declare finished without either of you being sure.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THIS MAKES YOUR ISSUES BETTER FOR PEOPLE TOO', [
        'Every one of those headings is something a human picking up the ticket also',
        'wanted and usually had to ask for. Teams that adopt agent-ready issues tend',
        'to find their human-assigned tickets improve as a side effect.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 3 — HANDING WORK

def ch3(v):
    lbl = 'Chapter 3  ·  Handing It Work'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Five Ways To Start It')
    y -= 6
    y = p.table(MX, y, ['Route', 'Use when'], [
        ('Assign an issue', 'The work is already written up — the common case'),
        ('The agents panel on github.com', 'Research, planning or a change with no issue'),
        ('From VS Code', 'You are in the editor and want it to run elsewhere'),
        ('@copilot in a PR comment', 'Follow-up work on a PR that already exists'),
        ('An automated workflow', 'On a schedule, or triggered by an event'),
    ], [230, CW - 230])
    y -= 16
    y = p.subheading(MX, y, 'Assigning an issue is the one to learn')
    y -= 4
    y = p.body(MX, y, 'You assign the issue to Copilot exactly as you would assign it to '
                      'a colleague — on github.com, in GitHub Mobile, or through the '
                      'GitHub CLI. Nothing new to learn, which is the point.')
    y -= 8
    y = p.code_block(MX, y, [
        '# From the terminal',
        'gh issue create --title "Cap discount at 40%" --body-file issue.md',
        'gh issue edit 482 --add-assignee copilot',
        '',
        '# Then watch for the draft PR it opens',
        'gh pr list --draft',
    ])
    y -= 12
    p.info_panel(MX, y, 'SECURITY ALERTS TOO', [
        'Alerts from security campaigns can be assigned to the agent, which makes',
        'routine dependency and vulnerability remediation something you triage',
        'rather than something you do by hand.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Agents Panel')
    y = p.body(MX, y - 6,
               'On github.com the agents panel starts work without an issue — useful for '
               'research and planning, not only code changes. Ask it to investigate '
               'something and report back, and you get an answer rather than a PR.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Pick the repository', [
        'One repo per session. This is a hard limit, not a default.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Describe the task', [
        'The same five headings from chapter 2. Vague in, unfinished out.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Choose the agent', [
        'You can select a custom agent defined in your repository, organisation',
        'or enterprise — with its own behaviour and its own tools.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Start it and go away', [
        'It pushes commits as it works. There is nothing to watch in real time.',
    ])
    y -= 10
    p.tip_box(MX, y, 'Custom agents are Volume 4 territory', [
        'A custom agent bundles instructions, tools and behaviour so a task type you',
        'run often does not need re-describing each time.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Triggering It From Automation')
    y = p.body(MX, y - 6,
               'The agent can be started by a schedule or a repository event, which turns '
               'it from a tool you invoke into background maintenance that happens '
               'whether or not anyone remembers.')
    y -= 10
    y = p.table(MX, y, ['Pattern', 'Shape'], [
        ('Weekly dependency sweep', 'Schedule → agent → draft PR → you review Monday'),
        ('Label-triggered', 'Add "copilot" label to an issue → it picks it up'),
        ('Post-incident', 'Alert fires → agent drafts the fix for review'),
        ('Docs drift', 'Schedule → regenerate docs from code → PR'),
    ], [190, CW - 190])
    y -= 16
    y = p.warn_box(MX, y, 'Automation multiplies both value and cost', [
        'A weekly agent run is a weekly credit charge whether or not there was any',
        'work to do. Trigger on a condition — new advisories exist, tests are',
        'failing — rather than on a bare calendar schedule.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'AND MULTIPLIES REVIEW LOAD', [
        'Five automated PRs a week that nobody reviews is worse than none: they rot,',
        'they conflict, and eventually someone merges one unread. Only automate what',
        'you have actually committed to reviewing.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Start with one trigger, not four', [
        'Pick the single most tedious recurring job, automate that, and live with it',
        'for a month. If the PRs are still getting reviewed after four weeks, add',
        'another. Review capacity is the constraint, not agent capacity.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Steering It While It Works')
    y = p.body(MX, y - 6,
               'You are not locked out once it starts. Mentioning @copilot in a comment '
               'gives it new instructions mid-run — the closest thing to looking over '
               'its shoulder.')
    y -= 10
    y = p.code_block(MX, y, [
        '# In a comment on the draft PR, while it is still working:',
        '',
        '@copilot the fix belongs in discount_for(), not in the caller.',
        'Please revert the change to orders.py.',
        '',
        '@copilot add a test for quantity=0 as well.',
        '',
        '@copilot stop changing the formatting — keep the diff minimal.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'When to step in')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'The first commits touch files you did not expect',
        'It is solving a different problem to the one you described',
        'The diff is growing far beyond the scope of the issue',
    ], step=22)
    y -= 6
    y = p.tip_box(MX, y, 'Watch the first commit, then leave', [
        'The first commit tells you whether it understood the issue. That is the',
        'cheap moment to redirect it — and usually the only one that matters.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Do not micromanage it to a standstill', [
        'A comment every two minutes wastes the entire point of an unattended agent,',
        'and each redirection costs credits. Correct a misunderstanding; do not',
        'supervise an implementation. If you want that, use agent mode in the editor.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What It Cannot Be Told To Do')
    y -= 6
    y = p.table(MX, y, ['Request', 'Why it will not work'], [
        ('"Also update the sister repo"', 'One repository per session, hard limit'),
        ('"Do this on both branches"', 'One branch per task'),
        ('"Split this into three PRs"', 'One pull request per task'),
        ('"Deploy it when tests pass"', 'Its PRs need human approval before CI runs'),
        ('"Just merge it if it is green"', 'Merging is yours, by design'),
    ], [230, CW - 230])
    y -= 16
    y = p.subheading(MX, y, 'These are features')
    y -= 4
    y = p.body(MX, y, 'Every one of those limits is a containment boundary. An agent that '
                      'could span repositories, branch freely and trigger deploys would '
                      'be considerably more useful and enormously more dangerous. The '
                      'shape of the tool is the safety model.')
    y -= 8
    y = p.info_panel(MX, y, 'IF A LIMIT IS BLOCKING YOU', [
        'Split the work. Three well-scoped single-repo tasks beat one that cannot',
        'run — and they review far more easily than one enormous cross-cutting PR',
        'would have done.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Sequence, do not parallelise', [
        'For a change that spans three repositories, do the one the others depend on',
        'first, merge it, then start the next. Trying to coordinate three agent',
        'sessions against a moving target is worse than doing it by hand.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 4 — THE PR

def ch4(v):
    lbl = 'Chapter 4  ·  The Pull Request'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'It Opens a Draft')
    y = p.body(MX, y - 6,
               'The agent pushes commits to a draft pull request as it works, so you can '
               'watch progress arrive rather than waiting for a finished lump. Draft is '
               'the important word — it is not asking to be merged yet.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Commits appear as it goes', [
        'Each step is a commit. The history is the working record.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Session logs show the reasoning', [
        'What it decided and why, alongside what it changed.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'It marks the PR ready when done', [
        'Or runs out of time — check, rather than assuming completion.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'You review it like any other PR', [
        'Because that is exactly what it is.',
    ])
    y -= 10
    y = p.info_panel(MX, y, 'CI DOES NOT RUN AUTOMATICALLY', [
        'The agent\'s pull requests require human approval before any CI/CD workflow',
        'runs. That is a deliberate control: it stops an agent-authored change from',
        'reaching your build and deployment environment without a person deciding.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Read the session log before the diff', [
        'The log tells you what it thought it was doing. If that is already wrong,',
        'you can stop without reading a line of code.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Reviewing an Agent PR')
    y = p.body(MX, y - 6,
               'Everything from Volume 2 chapter 4 applies. Two things change: nobody '
               'watched it work, and the diff arrives complete rather than growing under '
               'your eye.')
    y -= 10
    y = p.table(MX, y, ['Check', 'Because'], [
        ('Scope against the issue', 'Did it solve the thing you asked for?'),
        ('Files outside the stated area', 'The clearest signal it misunderstood'),
        ('Tests — what they assert', 'Green is not the same as correct'),
        ('New dependencies', 'Does it exist, and do you want it?'),
        ('Deletions', 'Easy to miss in a large diff, expensive to lose'),
        ('The commit history', 'Thrashing means it was guessing'),
    ], [220, CW - 220])
    y -= 16
    y = p.warn_box(MX, y, 'A thrashing history is the tell', [
        'Commits that add something, remove it, and add it back differently mean it',
        'never had a clear model of the problem. The final state may work by',
        'accident. Read that diff especially carefully, or reject and re-scope.',
    ])
    y -= 12
    p.info_panel(MX, y, 'YOU ARE THE AUTHOR NOW', [
        'Once you merge it, it is your code — reviewed by you, in your repository,',
        'under your name in the blame. "The agent wrote it" is not a defence that',
        'survives contact with an incident.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Iterating On The PR')
    y = p.body(MX, y - 6,
               'You do not have to accept or reject wholesale. Comment on the PR and it '
               'will keep working — the same @copilot mention that steers it mid-run also '
               'works as review feedback.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Review comments the agent will act on:',
        '',
        '@copilot this needs a test for the empty-cart case.',
        '',
        '@copilot you changed the public signature — keep it and add an',
        'optional parameter instead.',
        '',
        '@copilot revert the changes to README.md, they were out of scope.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'When to iterate and when to close')
    y -= 4
    y = p.table(MX, y, ['Situation', 'Do'], [
        ('Right approach, details wrong', 'Iterate — this is what it is good at'),
        ('Missing a case you spotted', 'Iterate'),
        ('Wrong approach entirely', 'Close it. Rewrite the issue and start again'),
        ('You do not understand the diff', 'Close it — do not merge to save the work'),
    ], [230, CW - 230])
    y -= 14
    y = p.tip_box(MX, y, 'Rewriting the issue beats arguing with the PR', [
        'If the approach is wrong, the issue was ambiguous. Fixing that gives you a',
        'better second attempt and a better issue for next time.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE SUNK COST TRAP, AGAIN', [
        'It ran for forty minutes and produced four hundred lines. That is spent',
        'whether you merge it or close it. The only live question is whether you',
        'want this code in your repository — and watching it be produced is not',
        'the same as having reviewed it.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When It Fails')
    y = p.body(MX, y - 6,
               'Runs fail. Usually for one of a small number of reasons, and most of them '
               'are fixable in the issue rather than the code.')
    y -= 10
    y = p.table(MX, y, ['Symptom', 'Usually'], [
        ('Ran out of time', 'Task too big — split it'),
        ('PR never opened', 'Rulesets blocked it; see chapter 5'),
        ('Says done, nothing works', 'No verification step in the issue'),
        ('Solved the wrong problem', 'Ambiguous issue — the fix is upstream'),
        ('Touched unrelated files', 'No "out of scope" section'),
        ('Cannot start at all', 'Plan or org policy — check with an admin'),
    ], [200, CW - 200])
    y -= 16
    y = p.info_panel(MX, y, 'THE PATTERN IN ALL OF THAT', [
        'Almost every failure traces back to the issue rather than the agent. It is',
        'a fast, literal, tireless contractor with no ability to ask a clarifying',
        'question halfway through. Ambiguity that a colleague would resolve over a',
        'desk becomes an hour of confident work in the wrong direction.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Keep the issues that worked', [
        'An issue that produced a clean PR is a template. The five headings plus',
        'your own conventions is a reusable asset, not a one-off.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Full Cycle')
    y -= 6
    y = p.step_card(MX, y, 1, 'Write the issue with all five headings', [
        'Problem, expected, where, how to verify, out of scope.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Assign it to Copilot', [
        'gh issue edit <n> --add-assignee copilot',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Check the first commit', [
        'Right file? Right idea? If not, comment now — it is cheap at this point.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Read the session log, then the diff', [
        'Reasoning first. If the reasoning is wrong the code does not matter.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Approve CI, or iterate, or close', [
        'CI needs your approval. Nothing runs until you say so.',
    ])
    y -= 6
    y = p.step_card(MX, y, 6, 'Merge it yourself', [
        'And own it, the same as any code you merge.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 5 — GUARDRAILS

def ch5(v):
    lbl = 'Chapter 5  ·  Review & Guardrails'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Automated Code Review')
    y = p.body(MX, y - 6,
               'Copilot can review pull requests — including ones people wrote. It '
               'gathers project context before suggesting changes, and its suggestions '
               'can be handed straight to the coding agent to produce a fix PR.')
    y -= 10
    y = p.table(MX, y, ['Good at catching', 'Weak at'], [
        ('Obvious bugs and typos', 'Whether the feature is right at all'),
        ('Missing null and edge cases', 'Domain rules it was never told'),
        ('Inconsistent conventions', 'Architectural judgement'),
        ('Missing tests', 'Whether the tests are meaningful'),
        ('Small security smells', 'Threat modelling'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'USE IT AS A FIRST PASS, NOT A GATE', [
        'It clears the mechanical objections before a human reads the PR, which',
        'makes human review faster and more focused. It does not replace the human,',
        'and a team that treats it as approval will ship things nobody read.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Review-to-fix is a genuine time saver', [
        'Passing review comments to the coding agent to generate the fix PR closes',
        'the loop on exactly the tedious, mechanical feedback you least want to',
        'apply by hand.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Watch for the loop closing on itself', [
        'An agent reviewing an agent\'s PR and generating an agent\'s fix, merged by',
        'a human who skimmed it, is a pipeline with no actual review in it. Somewhere',
        'in that chain a person has to genuinely read the code.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Branch Protection and Rulesets')
    y = p.body(MX, y - 6,
               'Your existing protections still apply to the agent — it is a contributor '
               'like any other. That is mostly what you want, and occasionally what '
               'blocks it.')
    y -= 10
    y = p.table(MX, y, ['Rule', 'Effect on the agent'], [
        ('Required reviews', 'Applies — someone must approve'),
        ('Required status checks', 'Applies — but CI needs your approval first'),
        ('Restrictions on commit authors', 'May block it outright'),
        ('Signed commits required', 'May block it, depending on configuration'),
        ('Protected paths', 'Applies — it cannot bypass them'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'IF A RULESET BLOCKS IT', [
        'Copilot can be added as a bypass actor in a ruleset. Do this deliberately',
        'and narrowly — a bypass added to unblock one task tends to outlive the',
        'task, and you will not remember it is there.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Never bypass required review', [
        'Bypassing a commit-author restriction to let the agent open a PR is',
        'reasonable. Bypassing the rule that a human approves the merge removes the',
        'only control that makes any of this safe.',
    ])
    y -= 12
    p.info_panel(MX, y, 'A SENSIBLE STARTING POSTURE', [
        'Agent enabled on one repository, not the whole organisation. Required human',
        'review kept in place. CI approval left as it is. No bypass actors. Loosen',
        'from there once you have seen a dozen of its pull requests and know what',
        'they actually look like.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Command', 'Does'], [
        ('gh extension install github/gh-copilot', 'Install the CLI'),
        ('gh copilot explain "<cmd>"', 'Explain a command'),
        ('gh copilot suggest "<goal>"', 'Suggest a command'),
        ('gh issue edit <n> --add-assignee copilot', 'Hand an issue to the agent'),
        ('gh pr list --draft', 'Find the draft PR it opened'),
        ('@copilot <instruction>', 'Steer it, in an issue or PR comment'),
    ], [270, CW - 270])
    y -= 14
    y = p.table(MX, y, ['Cloud agent limit', 'Value'], [
        ('Maximum run time', '59 minutes, hard'),
        ('Repositories per session', 'One'),
        ('Branches per task', 'One'),
        ('Pull requests per task', 'One'),
        ('Repository hosting', 'GitHub-hosted only'),
        ('CI on its PRs', 'Requires human approval'),
        ('Plans', 'All paid; admin must enable on Business/Enterprise'),
    ], [220, CW - 220])
    y -= 14
    p.info_panel(MX, y, 'THE FIVE ISSUE HEADINGS', [
        'Problem  ·  Expected  ·  Where  ·  How to verify  ·  Out of scope',
        '',
        'If you take one page from this volume, take that line. Everything else',
        'here is downstream of writing the task down properly.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('Cannot assign an issue to Copilot', 'Plan does not include it, or admin disabled'),
        ('No draft PR appeared', 'A ruleset blocked it — check commit-author rules'),
        ('Run hit the time limit', 'Split the task; 59 minutes is a hard stop'),
        ('CI never ran', 'Working as designed — approve it yourself'),
        ('It ignored my comment', 'Mention @copilot explicitly in the comment'),
        ('Wrong problem solved', 'The issue was ambiguous — rewrite and reassign'),
        ('CLI works, agent does not', 'Different things; check plan and org policy'),
        ('Costs more than expected', 'Long exploratory runs — scope harder'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 4 — Customisation: instruction files, prompt files, custom agents and',
        'MCP servers. How to stop re-explaining your conventions every single time.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Before you go', [
        'The agent is fast, literal and tireless, and it cannot ask you a question',
        'halfway through. Everything good about using it follows from writing the',
        'task down properly before you press go.',
    ])
    y -= 12
    p.info_panel(MX, y, 'MORE GUIDES', [
        'etsy.com/shop/FranksMarketDesigns',
        '',
        'Unofficial and independent. Not affiliated with, endorsed by, or sponsored',
        'by GitHub or Microsoft.',
    ])
    v.close()


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v = Volume(OUT, COPILOT,
               title='The CLI & the Coding Agent',
               subtitle='Copilot in your terminal, and running without you on GitHub',
               badge='VOLUME THREE',
               tagline='CLI  ·  CLOUD AGENT  ·  ISSUES  ·  PULL REQUESTS  ·  GUARDRAILS')

    total = 2 + 5 + 5 + 5 + 5 + 4
    # SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
    # and spliced in by rebuild_covers.py. This call is retained so a from-source
    # rebuild still produces a complete document; run rebuild_covers.py afterwards.
    v.cover(
        stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('59', 'MIN LIMIT'),
               ('2026', 'EDITION')],
        inside=[(n, t, b) for n, t, b, _ in CHAPTERS],
    )
    v.contents([(n, t, b, s) for n, t, b, s in CHAPTERS])
    ch1(v)
    ch2(v)
    ch3(v)
    ch4(v)
    ch5(v)
    v.save()
    print('Saved: %s  (%d pages)' % (OUT, v.page_no))


if __name__ == '__main__':
    main()
