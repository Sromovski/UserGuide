#!/usr/bin/env python3
"""Codex Field Guide — Volume 2: The Codex CLI.

    python build_codex_v2.py

FACTS VERIFIED 2026-08-02 against learn.chatgpt.com/docs/codex/cli.
Documented: install via chatgpt.com/codex/install.sh · sign in with ChatGPT ·
/permissions controls when Codex may edit or run without asking and shows the active
sandbox and writable roots · /init creates AGENTS.md · /status shows session setup ·
/model sets model and reasoning effort · /review analyses changes · codex resume reopens
recent chats · codex exec runs non-interactively · codex mcp manages MCP servers.
"""
import os

from fieldguide import CODEX, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Codex_Field_Guide_Volume_2_The_CLI.pdf')

CHAPTERS = [
    (1, 'Install & First Run', 'Getting set up without piping scripts blindly', 3),
    (2, 'Permissions & Sandbox', 'The most consequential setting in the product', 8),
    (3, 'The Commands', 'Everything you can type, and when each earns its place', 13),
    (4, 'codex exec & Automation', 'Codex in scripts, pipelines and CI', 18),
    (5, 'Sessions & Models', 'Reasoning effort, resuming work, and staying coherent', 23),
]


def ch1(v):
    lbl = 'Chapter 1  ·  Install & First Run'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Installing')
    y = p.body(MX, y - 6,
               'One installer, any platform. The documented route pipes a script into a '
               'shell — convenient, and worth one extra step first.')
    y -= 10
    y = p.code_block(MX, y, [
        '# The careful way',
        'curl -fsSL https://chatgpt.com/codex/install.sh -o install.sh',
        'less install.sh          # read what it will do',
        'sh install.sh',
        '',
        '# The documented one-liner, once you have decided you trust it',
        'curl -fsSL https://chatgpt.com/codex/install.sh | sh',
        '',
        '# Verify',
        'codex --version',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Piping to a shell is a trust decision', [
        'You are running whatever that URL returns, with your permissions, right',
        'now. It is fine for a vendor you have chosen to trust — but read it once,',
        'and never do it for a URL somebody pasted at you.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'If codex is not found afterwards', [
        'The installer put it somewhere not yet on your PATH. Open a new shell',
        'first — that fixes it far more often than anything else.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHAT YOU NEED BEFORE ANY OF THIS', [
        'A ChatGPT account on a plan that includes Codex. Git, and a repository you',
        'know well enough to judge the output. A terminal you are comfortable in.',
        'Nothing else — there is no separate Codex subscription and no API key to',
        'manage for the CLI.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Signing In')
    y = p.body(MX, y - 6,
               'Run codex inside a project. On first launch it offers sign-in options; '
               'choose Sign in with ChatGPT and use the account that holds your plan.')
    y -= 10
    y = p.code_block(MX, y, [
        'cd ~/code/my-project',
        'codex',
        '',
        '# then, once you are in:',
        '/status                  # what am I actually signed in as?',
    ])
    y -= 12
    y = p.table(MX, y, ['Problem', 'Usually'], [
        ('Sign-in loops', 'Wrong account — one without a Codex plan'),
        ('Works on web, not CLI', 'Two different accounts signed in'),
        ('Cannot delegate', 'The plan is Go — delegation starts at Plus'),
        ('Nothing happens on a proxy', 'Needs outbound HTTPS; check proxy config'),
    ], [180, CW - 180])
    y -= 14
    y = p.info_panel(MX, y, 'RUN IT FROM THE PROJECT ROOT', [
        'Codex works relative to where you started it. Launching from a',
        'subdirectory narrows what it can see, which is occasionally useful and',
        'more often just confusing when it cannot find the tests.',
    ])
    y -= 12
    p.tip_box(MX, y, '/status is the first thing to type', [
        'Account, model, reasoning effort, sandbox and writable roots — the whole',
        'session in one screen. Check it before your first real task, every time.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Before Your First Task')
    y = p.body(MX, y - 6,
               'Three minutes of setup that turns every bad run into an inconvenience '
               'rather than an incident.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Get on a branch', [
        'git switch -c codex/the-task',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Commit everything', [
        'git add -A && git commit -m "checkpoint"',
        'Uncommitted work is the only thing Codex can genuinely lose for you.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Check the permission mode', [
        '/permissions — decide before it matters, not during.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Write AGENTS.md', [
        '/init drafts one from your codebase. Volume 3 covers editing it down.',
    ])
    y -= 10
    y = p.info_panel(MX, y, 'WHY THE COMMIT MATTERS MORE THAN THE SANDBOX', [
        'The sandbox stops it reaching outside the project. Git is what lets you',
        'discard what it did inside the project. Most bad runs are the second kind,',
        'and git restore fixes them in one command.',
    ])
    y -= 12
    p.tip_box(MX, y, 'A branch per task, not per day', [
        'It makes the diff reviewable and the abandonment cheap. Branch names are',
        'free.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What a Session Looks Like')
    y = p.body(MX, y - 6,
               'You type a task in plain English. It reads, edits, runs things and '
               'reports. You steer between turns.')
    y -= 10
    y = p.code_block(MX, y, [
        '$ codex',
        '',
        '> Add unit tests for every public function in services/pricing.py.',
        '  Cover happy path, empty input, and the discount cap at 100.',
        '  Match the style of tests/test_orders.py. Run pytest and make it pass.',
        '  Do not change anything outside tests/.',
        '',
        '  [reads services/pricing.py]',
        '  [reads tests/test_orders.py]',
        '  [creates tests/test_pricing.py]',
        '  [runs pytest]  ->  1 failed',
        '  [edits tests/test_pricing.py]',
        '  [runs pytest]  ->  all passed',
    ])
    y -= 12
    y = p.subheading(MX, y, 'The two moments that matter')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'The first file it opens — did it understand the task?',
        'The verification step — did it actually run anything, or just claim success?',
    ], step=22)
    y -= 6
    y = p.warn_box(MX, y, 'A run with no verification step is a warning', [
        'If it never ran the tests, it does not know whether it worked either.',
    ])
    y -= 12
    p.info_panel(MX, y, 'YOU CAN INTERRUPT AT ANY POINT', [
        'Between turns you can redirect it, narrow the task, or stop entirely. The',
        'cheapest correction is always the earliest one — two steps in costs almost',
        'nothing, and twenty minutes in costs the whole task.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Reviewing What It Did')
    y -= 6
    y = p.code_block(MX, y, [
        '# Inside codex — a cheap first pass',
        '/review',
        '',
        '# Outside — the shape, then the detail',
        'git diff --stat',
        'git diff',
        '',
        '# Run the tests yourself. "It said they passed" is not the same claim.',
        'pytest',
        '',
        '# If it went badly',
        'git restore .',
    ])
    y -= 12
    y = p.table(MX, y, ['Check', 'Looking for'], [
        ('Files you did not expect', 'Scope creep — the clearest warning sign'),
        ('Deletions', 'Easy to miss, expensive to lose'),
        ('What the tests assert', 'assert True, or asserting a mock was called'),
        ('New imports', 'Packages that may not exist'),
    ], [200, CW - 200])
    y -= 14
    p.info_panel(MX, y, 'YOU ARE THE AUTHOR ONCE YOU COMMIT', [
        'It is your name in the blame and your problem at 3am. "The agent wrote it"',
        'has never survived contact with an incident review.',
    ])
    v.close()


def ch2(v):
    lbl = 'Chapter 2  ·  Permissions & Sandbox'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Setting That Matters Most')
    y = p.body(MX, y - 6,
               'The CLI runs on your machine, with your permissions, your environment '
               'variables and your credentials within reach. /permissions is what decides '
               'how much of that it may use without asking.')
    y -= 10
    y = p.code_block(MX, y, [
        '/permissions      # choose when Codex may edit files or run commands',
        '                  # without asking, and inspect the active sandbox',
        '                  # and the writable roots',
        '/status           # shows the same thing as part of the session summary',
    ])
    y -= 12
    y = p.table(MX, y, ['The two things it controls', 'Meaning'], [
        ('When it asks', 'Every action, once per session, or not at all'),
        ('Writable roots', 'Which directories it may write to at all'),
    ], [220, CW - 220])
    y -= 14
    y = p.warn_box(MX, y, 'These are different guarantees', [
        'Approval is a question you can answer wrongly at 5pm on a Friday. A',
        'writable root is a boundary it cannot cross regardless of what either of',
        'you decides. Prefer the boundary where you can have one.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Start with it asking', [
        'The first few sessions teach you what it actually tries to do. That is',
        'worth far more than the clicks it costs.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing a Posture')
    y -= 6
    y = p.table(MX, y, ['Posture', 'Right when'], [
        ('Ask every time', 'Learning, or working somewhere that matters'),
        ('Ask once per session', 'You trust the task and want it to flow'),
        ('Do not ask', 'A scratch repo, a container, or a VM you can discard'),
    ], [200, CW - 200])
    y -= 16
    y = p.info_panel(MX, y, 'WHERE "DO NOT ASK" IS ACTUALLY REASONABLE', [
        'A throwaway repository. A container or VM. A branch with everything',
        'committed, on a machine with no production credentials in the environment.',
        'Outside those, the time it saves is not worth the class of mistake it',
        'enables — and the mistakes are the ones that run commands, not edit files.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'The asymmetry to keep in mind')
    y -= 4
    y = p.body(MX, y, 'An edit inside the repository is recoverable with git. A command '
                      'that touches something outside it may not be. That is why the '
                      'approval prompt for running a command deserves more attention than '
                      'the one for changing a file, even though they look identical.')
    y -= 12
    y = p.table(MX, y, ['It wants to', 'Recoverable?'], [
        ('Edit a file in the repo', 'Yes — git restore'),
        ('Create a file in the repo', 'Yes — git clean'),
        ('Run the test suite', 'Nothing to recover'),
        ('Install a package', 'Usually, with effort'),
        ('Run something outside the repo', 'Maybe not'),
    ], [250, CW - 250])
    y -= 12
    p.tip_box(MX, y, 'Read the bottom two rows twice', [
        'They are where the difference between an inconvenience and an incident is.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Writable Roots')
    y = p.body(MX, y - 6,
               'The sandbox limits where Codex can write. Knowing what is in scope before '
               'you start prevents the most alarming category of surprise.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Check them', [
        '/status lists the active writable roots for this session.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Keep them tight', [
        'The project directory is almost always the right answer.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Be deliberate about widening', [
        'A task that needs to write outside the project is a task worth',
        'thinking about twice before you run it.',
    ])
    y -= 10
    y = p.table(MX, y, ['In scope', 'Think hard about'], [
        ('The repository you are in', 'Your home directory'),
        ('A build or output directory', 'Anything with dotfiles and credentials'),
        ('A temp directory', 'System paths'),
    ], [230, CW - 230])
    y -= 14
    p.warn_box(MX, y, 'Environment variables are not sandboxed', [
        'A command it runs inherits your environment. If your shell has an API key',
        'in it, so does anything Codex executes. That is a good reason not to keep',
        'long-lived production secrets exported in your everyday shell.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What to Never Let It Near')
    y -= 6
    y = p.table(MX, y, ['Do not', 'Because'], [
        ('Run it in your home directory', 'Everything becomes in scope'),
        ('Give it production credentials', 'A confident wrong command is still a command'),
        ('Auto-approve on a live system', 'The one place a mistake is not recoverable'),
        ('Point it at a repo you cannot lose', 'Commit first, or do not start'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'A REASONABLE DEFAULT SETUP', [
        'Run it inside one repository. Writable root is that repository. Approval on',
        'for commands, and a branch with everything committed. That configuration',
        'makes essentially every failure a git restore away.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Containers make "do not ask" safe', [
        'If you want it working without interruption, the answer is to constrain the',
        'environment rather than to trust the agent more. A container it cannot',
        'escape beats a permission dialogue you will click through anyway.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE PRINCIPLE UNDERNEATH ALL OF THIS', [
        'Do not rely on the agent being careful, and do not rely on yourself being',
        'attentive at 6pm. Rely on the environment making the bad outcome impossible.',
        'Every recommendation in this chapter is a version of that one idea.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Reading an Approval Prompt')
    y = p.body(MX, y - 6,
               'When it asks, the question is not "do I trust Codex" but "do I '
               'understand this specific action".')
    y -= 10
    y = p.table(MX, y, ['It wants to', 'Ask yourself'], [
        ('Edit a file in scope', 'Is that the file I expected?'),
        ('Create a file', 'In the right place?'),
        ('Run the test suite', 'Fine — this is the point'),
        ('Run an install command', 'Do I know this package?'),
        ('Run something with sudo', 'Why? Almost never a good sign'),
        ('Touch a dotfile or config', 'Was that in the task?'),
    ], [200, CW - 200])
    y -= 16
    y = p.warn_box(MX, y, 'The dangerous prompts look boring', [
        'Nobody clicks approve on something alarming. They click approve on the',
        'fortieth prompt of an afternoon because the first thirty-nine were fine.',
        'That is exactly why "ask every time" stops being protective on long runs —',
        'and why constraining the environment beats relying on your attention.',
    ])
    y -= 12
    p.tip_box(MX, y, 'If you are clicking without reading, change the setup', [
        'Either narrow the task so there are fewer prompts, or move to a container',
        'and turn them off honestly. Pretending to review is the worst of both.',
    ])
    v.close()


def ch3(v):
    lbl = 'Chapter 3  ·  The Commands'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'In-Session Commands')
    y -= 6
    y = p.table(MX, y, ['Command', 'Does'], [
        ('/init', 'Create an AGENTS.md for this project'),
        ('/status', 'Session setup — model, effort, sandbox, writable roots'),
        ('/permissions', 'When it may act without asking; inspect the sandbox'),
        ('/model', 'Choose the model and the reasoning effort'),
        ('/review', 'Analyse the current changes for issues'),
    ], [150, CW - 150])
    y -= 16
    y = p.subheading(MX, y, 'The two people skip')
    y -= 4
    y = p.body(MX, y, '/init, because writing AGENTS.md feels like a chore until the first '
                      'time it stops re-suggesting a framework you dropped. And /review, '
                      'because the run just told you it worked — which is exactly when a '
                      'second opinion is worth the least effort and the most.')
    y -= 8
    y = p.info_panel(MX, y, '/review IS CHEAPER THAN YOUR ATTENTION', [
        'It costs a fraction of what producing the change did, and it catches the',
        'mechanical problems before you spend your own reading on the interesting',
        'ones. It is a filter, not an approval.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Type / to see what your version has', [
        'The command set moves. The live list beats any printed table, including',
        'this one.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Shell Commands')
    y -= 6
    y = p.table(MX, y, ['Command', 'Does'], [
        ('codex', 'Start a session in the current directory'),
        ('codex resume', 'Reopen a recent conversation'),
        ('codex exec', 'Run non-interactively — chapter 4'),
        ('codex mcp', 'Add local or remote MCP servers, inspect tools'),
    ], [160, CW - 160])
    y -= 16
    y = p.subheading(MX, y, 'codex resume is underused')
    y -= 4
    y = p.body(MX, y, 'Coming back to a task after lunch does not have to mean explaining '
                      'it again. Resuming keeps the context you already paid for, which '
                      'is both cheaper and better than reconstructing it.')
    y -= 8
    y = p.code_block(MX, y, [
        '# Pick up where you left off',
        'codex resume',
        '',
        '# Manage MCP servers — Volume 3 covers what to connect',
        'codex mcp',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Resume the right session, not the newest', [
        'Resuming a session about a different task pollutes it with irrelevant',
        'context, which is the main way sessions start producing worse answers.',
    ])
    y -= 12
    p.info_panel(MX, y, 'codex exec IS THE ONE THAT CHANGES THINGS', [
        'Everything else here is a nicer way to do what you were already doing.',
        'exec turns Codex from a tool you use into a tool that runs — in a script,',
        'on a schedule, in CI. That is chapter 4, and it carries the most risk',
        'because nobody is there to say no.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing Model and Effort')
    y = p.body(MX, y - 6,
               '/model sets both the model and the reasoning effort. Effort is the dial '
               'most people never touch, and it is the one that matters most for the '
               'balance between quality and consumption.')
    y -= 10
    y = p.table(MX, y, ['Task', 'Effort'], [
        ('Rename something across files', 'Low'),
        ('Write tests for a known function', 'Low to medium'),
        ('Implement a described feature', 'Medium'),
        ('A bug you genuinely cannot find', 'High'),
        ('Architecture or a subtle race', 'High or above'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'HIGH EFFORT ON A MECHANICAL TASK IS WASTE', [
        'It will think carefully about a rename and produce the same rename. Match',
        'the dial to the difficulty, and default low — you will notice quickly when',
        'something needs more, and escalating is one command.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Effort rarely rescues a bad task description', [
        'If low and high effort both misunderstand you, the problem is the brief.',
        'More thinking applied to the wrong question is just a more expensive',
        'wrong answer.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Writing the Task')
    y = p.body(MX, y - 6,
               'The same four parts as every agent in this series. Worth repeating '
               'because it is the whole game.')
    y -= 10
    y = p.table(MX, y, ['Part', 'Without it'], [
        ('Scope — which files', 'It reads the whole repository'),
        ('Definition of done', 'It does not know when to stop'),
        ('How to verify', 'It stops at plausible'),
        ('Out of scope', 'It improves things you did not ask about'),
    ], [190, CW - 190])
    y -= 16
    y = p.code_block(MX, y, [
        '# All four, in one paragraph',
        'In api/client.py, add retries with exponential backoff to the two',
        'network calls. Max three attempts. Do not change the public signature.',
        'Add tests in tests/test_client.py covering success, retry-then-success,',
        'and permanent failure. Run pytest and make it pass.',
        'Do not modify any other file.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Put the conventions in AGENTS.md instead', [
        'Then the task only has to say what is different about THIS job. That is',
        'Volume 3, and it makes every task you write shorter.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Length is not precision', [
        'A long, polite, carefully worded request is not clearer than a short one',
        'that names the file and states the finish line. Precision is about which',
        'facts you supply, not how many words you use supplying them.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['In session', 'Does'], [
        ('/init', 'Create AGENTS.md'),
        ('/status', 'Model, effort, sandbox, writable roots'),
        ('/permissions', 'When it acts without asking'),
        ('/model', 'Model and reasoning effort'),
        ('/review', 'Analyse the current changes'),
    ], [150, CW - 150])
    y -= 14
    y = p.table(MX, y, ['Shell', 'Does'], [
        ('codex', 'Start here'),
        ('codex resume', 'Reopen a recent conversation'),
        ('codex exec', 'Non-interactive, for automation'),
        ('codex mcp', 'Manage MCP servers'),
    ], [150, CW - 150])
    y -= 14
    y = p.info_panel(MX, y, 'THE THREE-COMMAND HABIT', [
        '/status before you start.  /review before you read the diff.',
        'git diff before you commit.  Almost everything that goes wrong is caught',
        'by one of those three.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Type / to see your version\'s list', [
        'Commands change between releases. The live list is always more current than',
        'a printed table — including the one above.',
    ])
    v.close()


def ch4(v):
    lbl = 'Chapter 4  ·  codex exec & Automation'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Running It Without a Human')
    y = p.body(MX, y - 6,
               'codex exec runs a task non-interactively — no prompts, no conversation, '
               'suitable for scripts, pipelines and CI. It is the difference between a '
               'tool you use and a tool that runs.')
    y -= 10
    y = p.code_block(MX, y, [
        '# The shape of it',
        'codex exec "update the CHANGELOG from commits since the last tag"',
        '',
        '# In a script',
        '#!/usr/bin/env bash',
        'set -euo pipefail',
        'git switch -c chore/changelog',
        'codex exec "regenerate CHANGELOG.md from git log since the last tag"',
        'git diff --stat',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Non-interactive means nobody says no', [
        'Every approval prompt that would have protected you is gone. Anything you',
        'run this way should be constrained by the environment instead — a branch,',
        'a container, tight writable roots, and no production credentials in scope.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Automate the output, not the merge', [
        'Let it produce a branch or a diff. Keep a person on the merge. That single',
        'boundary makes automation safe enough to be worth doing.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE TASK TEXT BELONGS IN A FILE', [
        'A task embedded in a shell string is unreviewable and unversioned. Keep it',
        'in the repository — .codex/tasks/weekly-tidy.md — and it becomes something',
        'you can improve, review in a pull request, and blame when it misbehaves.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Is Worth Automating')
    y -= 6
    y = p.table(MX, y, ['Good candidate', 'Why'], [
        ('Changelog from commits', 'Mechanical, verifiable, nobody enjoys it'),
        ('Dependency bumps', 'CI tells you immediately if it broke'),
        ('Documentation from code', 'Bounded, low risk if imperfect'),
        ('Applying a lint rule repo-wide', 'Repetitive and tedious'),
        ('Draft release notes', 'A first draft is most of the work'),
    ], [230, CW - 230])
    y -= 14
    y = p.table(MX, y, ['Do not automate', 'Why'], [
        ('Anything that merges itself', 'Removes the only human control'),
        ('Anything touching production', 'Blast radius outside the repo'),
        ('Vague quality passes', 'No finish line, unbounded consumption'),
        ('Anything you will not review', 'Unreviewed PRs rot and then get merged'),
    ], [230, CW - 230])
    y -= 14
    p.info_panel(MX, y, 'THE REVIEW BOTTLENECK IS REAL', [
        'Automation multiplies output, not review capacity. Five generated branches',
        'a week that nobody reads is worse than none — they conflict, they go stale,',
        'and eventually somebody merges one unread. Only automate what you have',
        'actually committed to reviewing.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Safe Automation Pattern')
    y -= 6
    y = p.step_card(MX, y, 1, 'Run on a schedule or an event', [
        'Prefer a condition — new advisories exist, the build broke — over a',
        'bare calendar trigger that fires whether or not there is work.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Always on a fresh branch', [
        'Never on main. The branch is the containment.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Constrain the environment', [
        'Container, tight writable roots, no production secrets exported.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Let CI check it', [
        'The build and the tests are the automated reviewer.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'A person merges', [
        'Non-negotiable. This is the control the rest of it rests on.',
    ])
    y -= 8
    p.tip_box(MX, y, 'Start with exactly one automation', [
        'The most tedious recurring job, and live with it for a month. Add another',
        'only if the first one is still being reviewed after four weeks.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'In CI')
    y = p.body(MX, y - 6,
               'The same rules apply, with one addition: a CI runner is a machine nobody '
               'is watching, which makes environment constraint the only real control.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Sketch — a scheduled maintenance job',
        'name: codex-maintenance',
        'on:',
        '  schedule: [{ cron: "0 6 * * 1" }]',
        'jobs:',
        '  tidy:',
        '    runs-on: ubuntu-latest',
        '    steps:',
        '      - uses: actions/checkout@v4',
        '      - run: |',
        '          git switch -c chore/weekly-tidy',
        '          codex exec "$(cat .codex/tasks/weekly-tidy.md)"',
        '          git push -u origin chore/weekly-tidy',
        '      # a person opens and reviews the PR',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Secrets in CI are secrets in reach', [
        'Whatever the runner has, the agent has. Scope the job to the minimum, and',
        'never give a maintenance task deploy credentials because it was convenient.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Keep the task text in the repository', [
        'A task in a file is reviewable, versioned and improvable. A task embedded',
        'in a YAML string is none of those.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When Automation Goes Wrong')
    y -= 6
    y = p.table(MX, y, ['Symptom', 'Cause'], [
        ('Empty diffs every week', 'Trigger fires with nothing to do — add a condition'),
        ('Enormous unreviewable branch', 'Task too broad for an unattended run'),
        ('Branches piling up', 'Nobody is reviewing — stop the automation'),
        ('It changed the wrong thing', 'No exclusions in the task file'),
        ('Consumed the usage window', 'Scheduled too often, or scoped too wide'),
        ('Fails silently in CI', 'Check the exit code and the logs, not the PR'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'THE HONEST TEST FOR ANY AUTOMATION', [
        'If it stopped running tomorrow, would anyone notice? If not, it is',
        'generating work rather than saving it — and quietly consuming your usage',
        'window doing so.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Review the automation monthly', [
        'The same discipline you would apply to any cron job. Automation that',
        'nobody owns is how repositories fill with branches nobody understands.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Turn it off rather than letting it rot', [
        'An automation producing branches nobody reads is not neutral — it consumes',
        'your usage window, creates merge conflicts, and trains the team to ignore',
        'a class of pull request. Deleting it is a real improvement.',
    ])
    v.close()


def ch5(v):
    lbl = 'Chapter 5  ·  Sessions & Models'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Keeping a Session Coherent')
    y = p.body(MX, y - 6,
               'Long sessions get cheaper per turn and worse per answer. Knowing when to '
               'continue and when to start fresh is most of the skill.')
    y -= 10
    y = p.table(MX, y, ['Continue when', 'Start fresh when'], [
        ('Same task, next step', 'The topic genuinely changed'),
        ('It is building on what it read', 'It keeps referring to an early mistake'),
        ('You are iterating on one file', 'Answers are drifting or repeating'),
        ('The context is helping', 'You are explaining more than it is doing'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'ONE SESSION PER TASK', [
        'Long enough to benefit from cached context, short enough to stay coherent.',
        'A session that started with an unrelated question is still carrying it',
        'twenty turns later — in confusion and in tokens.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'codex resume beats re-explaining', [
        'Coming back to the same task tomorrow? Resume it. Starting something else?',
        'Do not.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE SIGNS A SESSION HAS GONE STALE', [
        'It reintroduces a bug you already had it fix. It cites a file you removed',
        'from the plan. It answers a question you asked twenty turns ago rather than',
        'the one you just asked. All three mean start fresh — rephrasing will not',
        'clear context that is already crowded.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Getting Better Results')
    y -= 6
    y = p.step_card(MX, y, 1, 'Point at code you already like', [
        '"Match the style of tests/test_orders.py" beats three sentences of',
        'description, every time.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Give it something to run', [
        'A test or a linter turns guessing into iterating.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Constrain the output', [
        '"Only the function, no explanation" — less to read, less consumed.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Say what not to touch', [
        'Shorter than describing what to do, and often more effective.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'One change at a time', [
        'Two unrelated requests reliably produce one good answer and one bad one.',
    ])
    y -= 8
    p.tip_box(MX, y, 'And the two-attempt rule', [
        'Two focused attempts that have not worked means write it yourself. You',
        'will finish sooner and understand the result.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Do this', 'With'], [
        ('Install', 'chatgpt.com/codex/install.sh'),
        ('Start', 'codex, from the project root'),
        ('Check the session', '/status'),
        ('Set what it may do', '/permissions'),
        ('Set model and effort', '/model'),
        ('Create AGENTS.md', '/init'),
        ('Review changes', '/review'),
        ('Continue yesterday', 'codex resume'),
        ('Automate', 'codex exec'),
        ('Connect tools', 'codex mcp'),
    ], [180, CW - 180])
    y -= 14
    y = p.info_panel(MX, y, 'THE SAFE DEFAULT SETUP', [
        'One repository. Writable root = that repository. Approval on for commands.',
        'A branch, with everything committed. Reasoning effort low until something',
        'needs more. That configuration makes nearly every failure recoverable with',
        'a single git restore.',
    ])
    y -= 12
    p.tip_box(MX, y, 'And the four-part task', [
        'Scope, definition of done, how to verify, out of scope. Every chapter in',
        'this volume eventually reduces to writing that down before you press enter.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('codex: command not found', 'Open a new shell — PATH was updated'),
        ('Signed in but limited', 'Go is local-only; delegation starts at Plus'),
        ('It will not edit anything', '/permissions — approval or writable roots'),
        ('Edits outside the project', 'Writable roots too wide — check /status'),
        ('Answers drifting', 'Session polluted — start a fresh one'),
        ('Expensive runs', 'Scope tighter, drop the reasoning effort'),
        ('Hit the usage window', 'Rolling 5 hours — wait rather than upgrade'),
        ('exec did something unexpected', 'No approvals in non-interactive mode'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 3 — AGENTS.md, subagents and MCP: how to stop repeating your',
        'conventions, and how to give Codex your own tools.',
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
               title='The Codex CLI',
               subtitle='Permissions, commands and automation in the terminal',
               badge='VOLUME TWO',
               tagline='INSTALL  ·  SANDBOX  ·  COMMANDS  ·  EXEC  ·  SESSIONS')
    total = 2 + 5 + 5 + 5 + 5 + 4
    # SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
    # and spliced in by rebuild_covers.py. This call is retained so a from-source
    # rebuild still produces a complete document; run rebuild_covers.py afterwards.
    v.cover(stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('9', 'COMMANDS'),
                   ('2026', 'EDITION')],
            inside=[(n, t, b) for n, t, b, _ in CHAPTERS])
    v.contents([(n, t, b, s) for n, t, b, s in CHAPTERS])
    ch1(v); ch2(v); ch3(v); ch4(v); ch5(v)
    v.save()
    print('Saved: %s  (%d pages)' % (OUT, v.page_no))


if __name__ == '__main__':
    main()
