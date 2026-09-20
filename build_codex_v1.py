#!/usr/bin/env python3
"""Codex Field Guide — Volume 1: Getting Started with Codex.

    python build_codex_v1.py

FACTS VERIFIED 2026-08-02 against learn.chatgpt.com/docs/codex and OpenAI pricing
coverage. Load-bearing and easy to get wrong:
  * usage limits run on a 5-HOUR ROLLING WINDOW, not a daily or monthly cap
  * per-message pricing was retired 2 April 2026 for Plus/Pro/Business — it is
    token-based credits now (input, cached input, output)
  * Pro 5x ($100) was added 9 April 2026; the old $200 Pro became "Pro 20x"
  * cloud task delegation starts at Plus. Go is light, local use only
Keep every price in ONE table on ONE page so a reprint is a single edit.
"""
import os

from fieldguide import CODEX, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Codex_Field_Guide_Volume_1_Getting_Started.pdf')

CHAPTERS = [
    (1, 'What Codex Is', 'An agent that finishes tasks, not an autocomplete', 3),
    (2, 'Where It Runs', 'Web, editor, terminal, phone — and what each is for', 8),
    (3, 'Plans & Limits', 'The 5-hour window, and what the tiers actually buy', 13),
    (4, 'Your First Task', 'Install, sign in, and get one real change done', 18),
    (5, 'Working With It', 'Habits that make the difference, and where it fails', 23),
]


def ch1(v):
    lbl = 'Chapter 1  ·  What Codex Is'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Not Autocomplete')
    y = p.body(MX, y - 6,
               'Codex is not a suggestion engine that finishes your line. You give it a '
               'task in plain English; it reads the repository, edits files across the '
               'project, runs the tests, reads the failures and tries again until it '
               'believes the job is done.')
    y -= 10
    y = p.table(MX, y, ['Autocomplete tools', 'Codex'], [
        ('Complete the line you are typing', 'Complete the task you described'),
        ('One file, at the cursor', 'Many files, wherever they are'),
        ('You review a suggestion', 'You review a finished change'),
        ('Instant', 'Minutes — it is working'),
        ('You stay in control throughout', 'You set the goal and check the result'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'THE LOOP', [
        'Read the task -> explore the code -> make changes -> run tests or linters',
        '-> read the output -> fix what broke -> repeat until done or blocked.',
        'That loop is the product. Everything else is where you watch it happen.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Which changes what a good prompt looks like', [
        'You are writing a brief, not a query. The single biggest determinant of the',
        'result is how precisely you described "done" — chapter 5, and Volume 3.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What It Is Good At')
    y -= 6
    y = p.table(MX, y, ['Works well', 'Why'], [
        ('Fixing a well-described bug', 'The failing test is the specification'),
        ('Writing a test suite', 'Clear finish line — they pass or they do not'),
        ('Mechanical refactors', 'Repetitive, verifiable, tedious for a person'),
        ('Migrating a pattern', 'One shape into another, many files'),
        ('Dependency and API upgrades', 'The compiler tells it when it is wrong'),
        ('Exploring unfamiliar code', 'It reads faster than you do'),
    ], [220, CW - 220])
    y -= 16
    y = p.table(MX, y, ['Goes badly', 'Why'], [
        ('Design and architecture', 'It will decide, not consult'),
        ('Your business rules', 'It cannot infer what it was never told'),
        ('Anything unverifiable', 'With no way to check, it stops at plausible'),
        ('Vague quality work', '"Improve the code" has no finish line'),
    ], [220, CW - 220])
    y -= 14
    p.warn_box(MX, y, 'It will not tell you it is unsure', [
        'A confident wrong answer looks exactly like a confident right one. The',
        'defence is a task with something to verify against — never the tone of',
        'the reply.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Trade You Are Making')
    y = p.body(MX, y - 6,
               'Handing over a whole task buys speed and costs oversight. Both halves of '
               'that are real, and pretending otherwise is how teams get hurt.')
    y -= 10
    y = p.table(MX, y, ['You gain', 'You give up'], [
        ('Whole tasks done while you do other work', 'Watching each decision'),
        ('Tedious work that would be deferred', 'Familiarity with the code it wrote'),
        ('A first draft of something you dreaded', 'The thinking that draft skipped'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'THE RULE THAT KEEPS THIS SAFE', [
        'Never merge code you do not understand. Not "did not write" — plenty of',
        'good code gets merged unwritten by the merger. Understand it. If reading',
        'it properly costs more than writing it would have, the task was wrong for',
        'an agent.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Start where you would not have bothered', [
        'The best first tasks are the ones you have been putting off — missing',
        'tests, a tidy-up, a dependency bump. Low risk, real value, and you learn',
        'the loop on something you were never going to do anyway.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE QUESTION THAT SORTS ANY TASK', [
        'Could you write down in one sentence how you would check whether it',
        'succeeded? If yes, it is an agent task. If the honest answer is "I would',
        'know it when I saw it", you are asking for judgement rather than work —',
        'and judgement is the thing it is worst at.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Who This Volume Is For')
    y = p.body(MX, y - 6,
               'You write code and you have heard Codex does something more than '
               'autocomplete. Nothing here assumes you have used an AI agent before, and '
               'nothing assumes a particular language or stack.')
    y -= 10
    y = p.info_panel(MX, y, 'YOU WILL NEED', [
        'A ChatGPT account on a plan that includes Codex — chapter 3.',
        'A terminal, and a repository you know well enough to judge the output.',
        'Git. Not optional: it is what makes a bad run recoverable.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'By the end of this volume you will')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Know what Codex is and honestly what it is not',
        'Know which surface to use — web, editor, terminal or phone',
        'Understand the 5-hour rolling window, and why it is not a monthly quota',
        'Have installed it and completed one real task end to end',
        'Know the habits that separate a good run from an expensive mess',
    ], step=22)
    y -= 6
    y = p.tip_box(MX, y, 'The rest of the series', [
        'Volume 2 — the CLI in depth.  Volume 3 — AGENTS.md, subagents and MCP.',
        'Volume 4 — delegation, review and cost.',
    ])
    y -= 12
    p.warn_box(MX, y, 'What this volume does not cover', [
        'Permission modes and the sandbox in depth (Volume 2), AGENTS.md and',
        'subagents (Volume 3), and delegated cloud work and code review (Volume 4).',
        'This one gets you installed, oriented, and through one real task.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'How It Compares')
    y = p.body(MX, y - 6,
               'If you already use another assistant, the shape will be familiar. The '
               'differences that matter in practice:')
    y -= 10
    y = p.table(MX, y, ['', 'Codex'], [
        ('Instruction file', 'AGENTS.md — plain markdown, hierarchical'),
        ('Where it runs', 'Web, VS Code, CLI, iOS, Bedrock'),
        ('Limits', 'A 5-hour rolling window, not a monthly pool'),
        ('Billing', 'Token-based credits since 2 April 2026'),
        ('Subagents', 'TOML files, and user-triggered by default'),
        ('Sandbox', 'Explicit permission modes and writable roots'),
    ], [140, CW - 140])
    y -= 16
    y = p.info_panel(MX, y, 'THE ROLLING WINDOW IS THE BIG ONE', [
        'Most tools give you a monthly allowance you can spend how you like. Codex',
        'limits reset on a 5-hour rolling basis, so heavy use is throttled by the',
        'hour rather than exhausted for the month. It changes how you pace work,',
        'and it is the thing people coming from other tools get wrong first.',
    ])
    y -= 12
    p.tip_box(MX, y, 'AGENTS.md is a shared convention', [
        'Other tools read it too. A repository with a good AGENTS.md is configured',
        'for more than one assistant, which matters if your team is not unanimous.',
    ])
    v.close()


def ch2(v):
    lbl = 'Chapter 2  ·  Where It Runs'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Five Surfaces')
    y -= 6
    y = p.table(MX, y, ['Surface', 'Best for'], [
        ('CLI', 'Real work in a repository you have checked out'),
        ('VS Code extension', 'The same, without leaving the editor'),
        ('Web', 'Delegated tasks, review, and work away from your machine'),
        ('iOS', 'Kicking off or checking a task from your phone'),
        ('Amazon Bedrock', 'Running it inside your own AWS account (June 2026)'),
    ], [170, CW - 170])
    y -= 16
    y = p.subheading(MX, y, 'Plus the integrations')
    y -= 4
    y = p.body(MX, y, 'GitHub integration brings automatic pull-request code review, and '
                      'there is a Slack integration for teams that live there. Those are '
                      'covered in Volume 4.')
    y -= 8
    y = p.info_panel(MX, y, 'ONE ACCOUNT, EVERY SURFACE', [
        'Your ChatGPT plan covers all of them. Install the CLI and the extension and',
        'sign in on the web — there is no per-surface cost, and tasks started in one',
        'place can be picked up in another.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Start with the CLI', [
        'It is the most complete surface and the easiest to reason about — you can',
        'see exactly what it changed with git. Everything in Volume 2 assumes it.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The CLI')
    y = p.body(MX, y - 6,
               'The terminal surface, and the one this series treats as primary. You run '
               'it inside a checked-out repository and it works on the files in front of '
               'you.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Install',
        'curl -fsSL https://chatgpt.com/codex/install.sh | sh',
        '',
        '# Run it in a project',
        'cd ~/code/my-project',
        'codex',
        '',
        '# First launch asks you to sign in — choose Sign in with ChatGPT',
    ])
    y -= 12
    y = p.table(MX, y, ['Strength', 'Detail'], [
        ('Full control', 'Permission modes, sandbox, writable roots'),
        ('Scriptable', 'codex exec runs non-interactively for automation'),
        ('Transparent', 'git diff tells you exactly what happened'),
        ('Resumable', 'codex resume reopens a recent conversation'),
    ], [140, CW - 140])
    y -= 14
    p.warn_box(MX, y, 'Read the install script before you pipe it to a shell', [
        'Curling a script straight into sh is convenient and is also how people get',
        'burned. Fetch it, read it, then run it — for this and for everything else.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Editor Extension and the Web')
    y -= 4
    y = p.subheading(MX, y, 'VS Code extension')
    y -= 4
    y = p.body(MX, y, 'The same agent, inside the editor, with the diff shown where you '
                      'already read diffs. If you live in VS Code this is the lowest '
                      'friction way in, and the review experience is better than the '
                      'terminal for large changes.')
    y -= 10
    y = p.subheading(MX, y, 'The web')
    y -= 4
    y = p.body(MX, y, 'Where delegated work lives. You describe a task, it runs remotely, '
                      'and you come back to a result — no terminal, and your machine can '
                      'be closed. This is the surface that changes how you work rather '
                      'than just where you type.')
    y -= 10
    y = p.info_panel(MX, y, 'DELEGATION STARTS AT PLUS', [
        'Cloud task delegation — the background-agent behaviour — is not in the Go',
        'tier. Go is for light, local use. If working-while-you-are-away is the',
        'reason you are here, Plus is the entry point.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'The phone is more useful than it sounds', [
        'Not for writing code. For starting a task on the way somewhere, and reading',
        'what it did before you sit down.',
    ])
    y -= 12
    p.table(MX, y, ['Surface', 'You are', 'It is'], [
        ('CLI / editor', 'Present', 'Working in front of you'),
        ('Web / iOS', 'Elsewhere', 'Working without you'),
    ], [140, 130, CW - 270])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing Between Them')
    y -= 6
    y = p.table(MX, y, ['You want to', 'Use'], [
        ('Work on code in front of you', 'CLI'),
        ('Same, but review diffs comfortably', 'VS Code extension'),
        ('Hand off a task and walk away', 'Web'),
        ('Automate it in a script or CI', 'codex exec'),
        ('Check on something from a cafe', 'iOS'),
        ('Keep everything inside your AWS', 'Bedrock'),
    ], [230, CW - 230])
    y -= 16
    y = p.subheading(MX, y, 'Most people end up using two')
    y -= 4
    y = p.body(MX, y, 'The CLI or the extension for work they want to steer, and the web '
                      'for work they want done while they do something else. The others '
                      'are situational.')
    y -= 8
    y = p.info_panel(MX, y, 'A NOTE ON BEDROCK', [
        'Running Codex through Amazon Bedrock keeps it inside your own AWS account,',
        'which is usually a procurement or data-residency requirement rather than a',
        'preference. If nobody has asked you for it, you do not need it.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Do not spread yourself across all five', [
        'Pick one for hands-on work and one for delegation, and learn those properly.',
        'People who install everything on day one tend to use none of it well.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Runs Where')
    y = p.body(MX, y - 6,
               'Worth being clear about, because it determines what Codex can reach and '
               'what happens if you close your laptop.')
    y -= 10
    y = p.table(MX, y, ['Surface', 'Executes on', 'If you disconnect'], [
        ('CLI', 'Your machine', 'It stops'),
        ('VS Code', 'Your machine', 'It stops'),
        ('Web / delegated', 'OpenAI infrastructure', 'It keeps going'),
        ('Bedrock', 'Your AWS account', 'Depends on your setup'),
    ], [130, 170, CW - 300])
    y -= 16
    y = p.warn_box(MX, y, 'Local means it has your machine\'s access', [
        'The CLI runs with your permissions, your environment variables and your',
        'credentials in reach. That is exactly why the sandbox and permission modes',
        'in Volume 2 matter more than any other setting in the product.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'And delegated means it does not', [
        'Remote runs are contained by construction. Different trade-off: safer',
        'blast radius, less access to whatever is special about your setup.',
    ])
    y -= 12
    p.info_panel(MX, y, 'A PRACTICAL CONSEQUENCE', [
        'If a task needs a local database, a VPN, or credentials that only exist on',
        'your laptop, it has to run locally. If it only needs the repository, it is',
        'a good candidate for delegation — and delegation is the one that keeps',
        'working after you close the lid.',
    ])
    v.close()


def ch3(v):
    lbl = 'Chapter 3  ·  Plans & Limits'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The 5-Hour Rolling Window')
    y = p.body(MX, y - 6,
               'This is the single most important thing to understand about Codex usage, '
               'and it is not how most tools work.')
    y -= 10
    y = p.info_panel(MX, y, 'LIMITS RESET ON A 5-HOUR ROLLING BASIS', [
        'Not daily. Not monthly. A heavy afternoon throttles you for a few hours,',
        'not for the rest of the month — and a quiet week does not bank anything.',
    ])
    y -= 12
    y = p.table(MX, y, ['This means', 'So'], [
        ('You cannot exhaust the month', 'A bad day is a few hours, not a disaster'),
        ('You cannot save it up', 'Light weeks do not fund a heavy one'),
        ('Bursts are what get throttled', 'Pace long sessions, or expect a pause'),
        ('Planning is per-session', 'Not a monthly budgeting exercise'),
    ], [220, CW - 220])
    y -= 14
    y = p.tip_box(MX, y, 'It rewards steady use over sprints', [
        'Three focused tasks across a day beats twelve in one sitting — same work,',
        'and you never meet the ceiling.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Coming from a monthly-quota tool? Unlearn that', [
        'There is nothing to ration and nothing to save. Do not eke it out across',
        'the month, and do not panic when you meet the ceiling — it clears in hours,',
        'and it will clear again tomorrow whatever you do today.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Plans')
    y = p.body(MX, y - 6, 'Verified August 2026. Pricing in this space moves — check '
                          'before committing a team.')
    y -= 8
    y = p.table(MX, y, ['Plan', 'Price', 'For'], [
        ('Go', '$8/mo', 'Light, LOCAL use only — no delegation'),
        ('Plus', '$20/mo', 'The entry point for real use'),
        ('Pro 5x', '$100/mo', 'Added 9 Apr 2026. Active daily use'),
        ('Pro 20x', '$200/mo', 'Was "Pro". 4x the headroom of Pro 5x'),
        ('Business / Edu / Enterprise', '—', 'Teams, admin and procurement'),
    ], [190, 90, CW - 280])
    y -= 16
    y = p.info_panel(MX, y, 'THE TWO FACTS THAT DECIDE IT FOR MOST PEOPLE', [
        'Cloud task delegation starts at PLUS. Go is local-only.',
        'Pro 20x is twice the price of Pro 5x for roughly four times the headroom —',
        'so if you are consistently hitting Pro 5x limits, the step up is better',
        'value than it looks.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Start at Plus', [
        'It includes delegation, which is the feature that changes how you work.',
        'Upgrade when you actually meet the ceiling, not in anticipation of it.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'How Billing Changed')
    y = p.body(MX, y - 6,
               'On 2 April 2026 OpenAI retired per-message pricing for Plus, Pro and '
               'Business, replacing it with token-based credits.')
    y -= 10
    y = p.table(MX, y, ['Before', 'Now'], [
        ('One message, one fixed cost', 'Input tokens, cached input, output tokens'),
        ('Easy to count', 'Tracks the size of the job'),
        ('A long task cost the same', 'A long task costs more'),
    ], [250, CW - 250])
    y -= 16
    y = p.subheading(MX, y, 'Why this matters to you')
    y -= 4
    y = p.body(MX, y, 'Consumption now scales with how much context a task drags in and '
                      'how much it writes. A tightly scoped task on three files is cheap; '
                      'the same request phrased vaguely, so it reads forty files first, '
                      'is not. Scope is the lever — exactly as it is for every other '
                      'agent in this series.')
    y -= 8
    y = p.warn_box(MX, y, 'Cached input is cheaper than fresh input', [
        'Which is a quiet argument for continuing a session rather than restarting',
        'it for every question — up to the point where the context gets confused.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE TENSION TO MANAGE', [
        'Long sessions are cheaper per turn and get worse as context fills. Short',
        'sessions stay sharp and re-read everything. The answer is one session per',
        'task — long enough to benefit from the cache, short enough to stay',
        'coherent — and a fresh one the moment the topic genuinely changes.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Making the Window Work For You')
    y -= 6
    y = p.step_card(MX, y, 1, 'Scope tasks tightly', [
        'The cheapest task is the one that did not need to read the whole repo.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Pick reasoning effort deliberately', [
        '/model sets both the model and the reasoning effort. High effort on a',
        'mechanical task is money for nothing.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Batch related work into one session', [
        'Cached context is cheaper than re-reading the same files fresh.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'But start fresh when it gets confused', [
        'A polluted session is expensive AND wrong. Know the difference.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Delegate the long ones', [
        'A cloud task runs without holding your terminal or your attention.',
    ])
    y -= 10
    p.info_panel(MX, y, 'IF YOU HIT THE LIMIT', [
        'It is hours, not weeks. Do something else, or switch to work that does not',
        'need the agent. The window is short by design.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Is It Worth It?')
    y = p.body(MX, y - 6,
               'The comparison that matters is against your own hourly cost, not against '
               'zero.')
    y -= 10
    y = p.info_panel(MX, y, 'THE ARITHMETIC', [
        'Plus is $20 a month. Against a working developer that is a small fraction',
        'of one hour. The bar is not "transformative" — it is "saves an hour a',
        'month", and most people clear that in the first week on tests alone.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'What actually justifies it')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Work that was being deferred indefinitely now gets done',
        'Test coverage that appears because writing tests got cheap',
        'Migrations and upgrades that used to eat a whole afternoon',
        'Exploring unfamiliar code without reading all of it first',
    ], step=22)
    y -= 6
    y = p.warn_box(MX, y, 'And what does not', [
        'Volume of code produced. If your team is shipping more and understanding',
        'less, the subscription is not the cost you should be worried about.',
    ])
    y -= 12
    p.info_panel(MX, y, 'A MEASURE THAT IS NOT NONSENSE', [
        'After a month, ask yourself whether you would give it up. A tool you would',
        'fight to keep is paying for itself. One you would shrug at is not, whatever',
        'the number of accepted suggestions says.',
    ])
    v.close()


def ch4(v):
    lbl = 'Chapter 4  ·  Your First Task'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Install and Sign In')
    y -= 6
    y = p.step_card(MX, y, 1, 'Install the CLI', [
        'Fetch the script, read it, then run it. Do not pipe it blind.',
    ])
    y -= 6
    y = p.code_block(MX, y, [
        '# Read it first',
        'curl -fsSL https://chatgpt.com/codex/install.sh -o install.sh',
        'less install.sh',
        'sh install.sh',
        '',
        '# Or, once you have decided you trust it:',
        'curl -fsSL https://chatgpt.com/codex/install.sh | sh',
    ])
    y -= 10
    y = p.step_card(MX, y, 2, 'Run it in a repository', [
        'cd into a project you know well, then run: codex',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Sign in with ChatGPT', [
        'First launch offers sign-in options. Use the account holding your plan.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Check the setup', [
        '/status shows the session — model, effort, sandbox and writable roots.',
    ])
    y -= 8
    p.tip_box(MX, y, 'Run /status before your first real task', [
        'Knowing the permission mode and which directories are writable before you',
        'start is much better than discovering both from a surprise.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Set Up Safely First')
    y = p.body(MX, y - 6,
               'Two minutes here turns every bad run from a problem into an inconvenience.')
    y -= 10
    y = p.code_block(MX, y, [
        '# A branch, and a commit to come back to',
        'git switch -c codex/first-task',
        'git add -A && git commit -m "checkpoint before codex"',
        '',
        '# Inside codex, check what it may do without asking',
        '/permissions',
        '/status',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'WHAT /permissions CONTROLS', [
        'When Codex may edit files or run commands without asking you first, and',
        'which directories it can write to. Start with it asking. Loosen only once',
        'you have watched it work a few times and know what to expect.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Git is the safety net, not the sandbox', [
        'The sandbox limits what it can touch. Git is what lets you undo what it did',
        'touch. You want both, and neither substitutes for the other.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Commit before every run, not just the first', [
        'It takes two seconds and it turns "what did it change?" into a diff you can',
        'read. The habit is worth more than any setting in this chapter.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Write the Task')
    y = p.body(MX, y - 6,
               'Everything about the result is downstream of this. A good task names its '
               'scope, says what done looks like, gives it something to verify against, '
               'and says what not to touch.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Weak — no scope, no finish line, nothing to check against',
        'Improve the tests.',
        '',
        '# Strong — all four parts',
        'Add unit tests for every public function in services/pricing.py.',
        'Cover the happy path, empty input, and the discount cap at 100.',
        'Match the style of tests/test_orders.py and use pytest.',
        'Run pytest and make sure everything passes.',
        'Do not change any file outside tests/.',
    ])
    y -= 12
    y = p.table(MX, y, ['A good task has', 'Because'], [
        ('A named scope', 'It stops reading the whole repository'),
        ('A definition of done', 'It knows when to stop'),
        ('Something to verify against', 'It can check itself instead of guessing'),
        ('Explicit exclusions', 'It stops improving things you did not ask about'),
    ], [190, CW - 190])
    y -= 14
    p.tip_box(MX, y, 'If you cannot say how you would check it', [
        'It is not a task yet — it is a conversation. Have the conversation first,',
        'then write the task it produces.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Watch, Then Review')
    y -= 6
    y = p.step_card(MX, y, 1, 'Watch the first thing it does', [
        'Which file did it open? That tells you whether it understood the task,',
        'and it is the cheapest possible moment to stop.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Let it reach verification', [
        'A good run ends by running the tests and reporting the result.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Use /review', [
        'It analyses the changes for issues — a cheap first pass before your own.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Read the diff yourself', [
        'git diff --stat first for the shape, then git diff for the detail.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Run the tests yourself', [
        '"I ran the tests" and "they pass here" are different claims.',
    ])
    y -= 8
    p.warn_box(MX, y, 'Tests passing is weak evidence', [
        'An agent that can edit the code and the tests can make any suite green.',
        'Read what they assert, not just the colour.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When It Goes Wrong')
    y -= 6
    y = p.table(MX, y, ['Symptom', 'Usually'], [
        ('Solved a different problem', 'The task was ambiguous — rewrite it'),
        ('Touched unrelated files', 'No exclusions in the task'),
        ('Says done, nothing works', 'Nothing to verify against'),
        ('Keeps retrying the same fix', 'Stuck. Stop and re-scope'),
        ('Huge unreviewable diff', 'Task was too big — split it'),
        ('Ran out of the usage window', 'Wait a few hours; it is rolling'),
    ], [220, CW - 220])
    y -= 16
    y = p.code_block(MX, y, [
        '# Getting back to safety',
        'git restore .                       # discard uncommitted changes',
        'git switch - && git branch -D codex/first-task',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'ALMOST EVERY FAILURE IS UPSTREAM', [
        'Not in the agent, in the task. It is fast, literal and tireless, and it',
        'cannot ask you a clarifying question halfway through. Ambiguity a colleague',
        'would resolve in ten seconds becomes twenty minutes in the wrong direction.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Rewrite the task, do not argue with the run', [
        'When it solves the wrong problem, the fix is upstream. Restating the task',
        'with the misunderstanding as an explicit constraint produces a much better',
        'second attempt than any amount of correcting the first.',
    ])
    v.close()


def ch5(v):
    lbl = 'Chapter 5  ·  Working With It'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Habits That Matter')
    y -= 6
    y = p.step_card(MX, y, 1, 'Commit before every run', [
        'One command, and every bad outcome becomes recoverable.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Give it something to run', [
        'A test, a linter, a build. Verification is what makes it converge.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Say what not to touch', [
        'One sentence of exclusion saves a large confusing diff.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Stop early when it is wrong', [
        'Two steps in costs nothing. Twenty minutes in costs the task.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Write AGENTS.md once', [
        'So you stop repeating your conventions. Volume 3.',
    ])
    y -= 8
    p.tip_box(MX, y, 'The two-attempt rule', [
        'If two focused attempts have not produced what you want, write it yourself.',
        'You will finish sooner and you will understand the result.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Reading a Session')
    y = p.body(MX, y - 6,
               'Knowing when a run is going well is a skill, and it is mostly about '
               'noticing when it is not.')
    y -= 10
    y = p.table(MX, y, ['Good sign', 'Bad sign'], [
        ('Opened the file you expected', 'Started searching broadly'),
        ('Small, purposeful edits', 'Rewriting whole files'),
        ('Ran the tests unprompted', 'Declared success without running anything'),
        ('Fixed one failure at a time', 'Same fix twice, worded differently'),
        ('Diff you could review', 'Diff you would not want to'),
    ], [240, CW - 240])
    y -= 16
    y = p.info_panel(MX, y, 'THE THRASHING TELL', [
        'Adding something, removing it, then adding it back differently means it',
        'never had a clear model of the problem. The end state may work by accident.',
        'Read that diff especially carefully — or discard and re-scope.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Stopping is not failure', [
        'It is the cheapest correction available, and it gets cheaper the earlier',
        'you do it. Restarting narrower usually beats rescuing.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE SUNK COST TRAP', [
        'It ran for fifteen minutes and produced three hundred lines. That is spent',
        'either way. The only live question is whether you want this code in your',
        'repository — and having watched it appear is not the same as having read it.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Command', 'Does'], [
        ('codex', 'Start a session in the current directory'),
        ('codex resume', 'Reopen a recent conversation'),
        ('codex exec', 'Run non-interactively, for scripts and CI'),
        ('codex mcp', 'Add and inspect MCP servers'),
        ('/init', 'Create an AGENTS.md for this project'),
        ('/status', 'Model, effort, sandbox and writable roots'),
        ('/permissions', 'What it may do without asking'),
        ('/model', 'Choose the model and reasoning effort'),
        ('/review', 'Analyse the current changes for issues'),
    ], [160, CW - 160])
    y -= 14
    y = p.table(MX, y, ['Fact', 'Value'], [
        ('Usage limits', 'A 5-hour ROLLING window'),
        ('Billing', 'Token-based credits since 2 Apr 2026'),
        ('Delegation', 'Starts at Plus — not in Go'),
        ('Instruction file', 'AGENTS.md, plain markdown'),
        ('Install', 'chatgpt.com/codex/install.sh'),
    ], [160, CW - 160])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('codex: command not found', 'Installer did not add it to PATH — restart shell'),
        ('Sign-in fails', 'Check the plan includes Codex — Go is limited'),
        ('Cannot delegate a task', 'Delegation starts at Plus'),
        ('Hit a usage limit', 'Rolling 5-hour window — wait, do not upgrade yet'),
        ('It will not edit anything', 'Permission mode — run /permissions'),
        ('Edits outside the project', 'Check writable roots in /status'),
        ('Ignores your conventions', 'Write AGENTS.md — Volume 3'),
        ('Runs are expensive', 'Scope tighter; lower reasoning effort'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 2 — The Codex CLI: permission modes and the sandbox in depth,',
        'every command, and codex exec for automation.',
    ])
    y -= 12
    p.tip_box(MX, y, 'More guides', [
        'etsy.com/shop/FranksMarketDesigns  ·  Unofficial and independent.',
        'Not affiliated with, endorsed by, or sponsored by OpenAI.',
    ])
    v.close()


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v = Volume(OUT, CODEX,
               title='Getting Started with Codex',
               subtitle='An agent that finishes tasks — install it and use it well',
               badge='VOLUME ONE',
               tagline='WHAT IT IS  ·  SURFACES  ·  PLANS  ·  FIRST TASK  ·  HABITS')
    total = 2 + 5 + 5 + 5 + 5 + 4
    # SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
    # and spliced in by rebuild_covers.py. This call is retained so a from-source
    # rebuild still produces a complete document; run rebuild_covers.py afterwards.
    v.cover(stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('5', 'SURFACES'),
                   ('2026', 'EDITION')],
            inside=[(n, t, b) for n, t, b, _ in CHAPTERS])
    v.contents([(n, t, b, s) for n, t, b, s in CHAPTERS])
    ch1(v); ch2(v); ch3(v); ch4(v); ch5(v)
    v.save()
    print('Saved: %s  (%d pages)' % (OUT, v.page_no))


if __name__ == '__main__':
    main()
