#!/usr/bin/env python3
"""Copilot Field Guide — Volume 2: Chat & Agent Mode.

    python build_copilot_v2.py

The metered half of Copilot. Volume 1 covered the free half (completions and Next Edit
Suggestions); everything here draws on AI Credits, which is why cost discipline runs
through the whole volume rather than sitting in one chapter.

FACTS VERIFIED 2026-08-02 against code.visualstudio.com/docs/copilot and
docs.github.com. VS Code's chat surface moves fast — slash commands and tool names in
particular. Keep the command/tool tables on their own pages so a reprint is contained.
"""
import os

from fieldguide import COPILOT, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Copilot_Field_Guide_Volume_2_Chat_and_Agents.pdf')

CHAPTERS = [
    (1, 'The Three Modes', 'Ask, edit and agent — and when each is the right tool', 3),
    (2, 'Talking to Chat', 'Slash commands, participants and context references', 7),
    (3, 'Agent Mode', 'Delegating work, approving tools, keeping it on a leash', 13),
    (4, 'Reviewing What It Wrote', 'Multi-file diffs, and what to check before accepting', 19),
    (5, 'Getting Good Results', 'Prompting patterns, cost discipline, knowing when to stop', 23),
]


# ══════════════════════════════════════════════════════ CH 1 — THREE MODES

def ch1(v):
    lbl = 'Chapter 1  ·  The Three Modes'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Ask, Edit, Agent')
    y = p.body(MX, y - 6,
               'Chat is not one thing. It has three modes, and picking the wrong one is '
               'the most common reason people conclude Copilot "does not work". They '
               'differ in how much they change, and how much you review.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Ask — it answers, you type', [
        'A conversation. It explains, suggests and writes snippets into the panel.',
        'Changes nothing on disk. Safest, and the right default when learning.',
        'Cheapest of the three.',
    ])
    y -= 8
    y = p.step_card(MX, y, 2, 'Edit — it changes files, you approve each', [
        'You name the files. It proposes coordinated edits across them.',
        'You see a diff per file and accept or reject individually.',
        'Right when you know what needs changing and where.',
    ])
    y -= 8
    y = p.step_card(MX, y, 3, 'Agent — it decides, acts, and checks its own work', [
        'You give a goal. It plans, finds the files itself, edits, runs commands,',
        'reads the output and iterates until it believes the task is done.',
        'Most capable, most expensive, and the one that needs supervision.',
    ])
    y -= 10
    p.tip_box(MX, y, 'Start one rung lower than you think you need', [
        'Ask before edit, edit before agent. Reaching straight for agent mode on a',
        'task you could have described precisely is how credits disappear.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Where Each One Lives')
    y -= 6
    y = p.table(MX, y, ['Surface', 'Open with', 'Best for'], [
        ('Chat view', 'Ctrl+Alt+I', 'Multi-turn conversation, side by side'),
        ('Inline chat', 'Ctrl+I', 'A change right here, without leaving flow'),
        ('Quick chat', 'Ctrl+Shift+Alt+L', 'One question, then get out of the way'),
        ('Agents mode', 'Ctrl+Shift+I', 'Delegated, multi-file work'),
        ('Terminal inline', 'Ctrl+I in terminal', 'Explain or build a shell command'),
    ], [120, 130, CW - 250])
    y -= 16
    y = p.subheading(MX, y, 'Inline chat is the underused one')
    y -= 4
    y = p.body(MX, y, 'Select a few lines, press Ctrl+I, and describe the change. The '
                      'diff appears in place. For small, local edits this beats the chat '
                      'panel every time — the selection is the context, so you barely '
                      'need to explain anything.')
    y -= 8
    y = p.info_panel(MX, y, 'SESSION HOUSEKEEPING', [
        'Ctrl+N          start a new chat — do this more often than you think',
        '/clear          wipe the current conversation',
        '/compact        summarise a long conversation to reclaim context',
        '/fork           branch a new session keeping the history so far',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Why new sessions matter')
    y -= 4
    y = p.body(MX, y, 'Chat carries the whole conversation forward on every turn. A '
                      'session that started with an unrelated question is still paying '
                      'for it twenty turns later — in context space and in credits. '
                      'One task, one session.')
    y -= 8
    p.tip_box(MX, y, 'Ctrl+N is the cheapest fix in the product', [
        'When answers start drifting, a fresh session fixes it more reliably than',
        'any amount of rephrasing — and it costs nothing to try.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Every One of These Costs Credits')
    y = p.body(MX, y - 6,
               'Volume 1 drew the line: completions and Next Edit Suggestions are never '
               'metered. Everything in this volume is. That is not a reason to avoid it '
               '— it is a reason to choose the mode deliberately.')
    y -= 10
    y = p.table(MX, y, ['Mode', 'Rough relative cost'], [
        ('Ask, short question', 'Very low'),
        ('Ask, over a large file', 'Low to moderate'),
        ('Edit, two or three named files', 'Moderate'),
        ('Agent, tightly scoped task', 'Moderate'),
        ('Agent, vague goal on a big repo', 'The expensive one'),
    ], [260, CW - 260])
    y -= 16
    y = p.subheading(MX, y, 'Why agent mode costs so much more')
    y -= 4
    y = p.body(MX, y, 'An agent reads before it writes. On a vague goal it will search '
                      'the codebase, open files, run commands and read output — each of '
                      'which is model usage — before it makes a single edit. Scope is '
                      'the price lever, not the model picker.')
    y -= 8
    y = p.warn_box(MX, y, 'The most expensive prompt is a vague one', [
        '"Improve the error handling" makes it read everything looking for work.',
        '"Replace the bare excepts in api/orders.py" makes it read one file.',
        'Same feature, order-of-magnitude difference in what it costs you.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Three questions before you open agent mode')
    y -= 4
    p.bullets(MX + 4, y, [
        'Could I name the files this should touch? If yes, use edit mode instead',
        'Could I describe how to check it worked? If not, it is not ready yet',
        'Am I reaching for it because it is genuinely faster, or because it is there?',
    ], step=24)
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing the Model')
    y = p.body(MX, y - 6,
               'Chat lets you pick which model answers. Bigger models reason better on '
               'hard problems and cost proportionally more — credits track model usage, '
               'so the picker is a price dial as much as a quality dial.')
    y -= 10
    y = p.table(MX, y, ['Task', 'Reach for'], [
        ('Explain this code', 'The smallest available model'),
        ('Write tests for a known function', 'Small to mid'),
        ('Mechanical refactor across files', 'Mid'),
        ('A bug you genuinely cannot see', 'The strongest one'),
        ('Architecture and trade-offs', 'The strongest one'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'A HABIT WORTH FORMING', [
        'Default to a small model. Escalate when it visibly struggles, rather than',
        'starting at the top "to be safe" — that habit multiplies every interaction',
        'you have for the rest of the month.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'The model rarely fixes a bad prompt', [
        'If a strong model and a weak model both misunderstand you, the problem is',
        'the prompt. Chapter 5 is about fixing that rather than paying more.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Two things the picker does not change')
    y -= 4
    p.table(MX, y, ['Still true on any model', 'Why'], [
        ('It cannot see code you did not attach', 'Context is a choice you make, not a model feature'),
        ('It does not know your domain rules', 'Nothing in training covers your business'),
        ('It will not tell you it is unsure', 'Fluency is constant across model sizes'),
    ], [260, CW - 260])
    v.close()


# ══════════════════════════════════════════════════════ CH 2 — TALKING TO CHAT

def ch2(v):
    lbl = 'Chapter 2  ·  Talking to Chat'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Three Symbols Worth Learning')
    y = p.body(MX, y - 6,
               'Most of the skill of using chat is telling it what to look at. Three '
               'characters do almost all of that work, and typing any of them in the '
               'chat box shows you the full live list for your version.')
    y -= 10
    y = p.table(MX, y, ['Type', 'Gives you', 'Example'], [
        ('/', 'A command or skill', '/tests'),
        ('@', 'A participant — a specialist', '@terminal'),
        ('#', 'Context or a tool', '#selection'),
    ], [60, 220, CW - 280])
    y -= 16
    y = p.subheading(MX, y, 'Why this matters more than phrasing')
    y -= 4
    y = p.body(MX, y, 'Chat answers from a limited window of context. A beautifully '
                      'worded question about code it cannot see produces a confident '
                      'guess. A blunt question with the right # reference produces a '
                      'correct answer. Reach for the symbol before the adjectives.')
    y -= 8
    y = p.tip_box(MX, y, 'When in doubt, type the symbol', [
        'Typing / or @ or # opens a live list from your actual installation. That is',
        'always more current than any printed table, including the ones overleaf.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'The same question, three ways')
    y -= 4
    p.code_block(MX, y, [
        '# Vague — it guesses, and guesses fluently',
        'why is my authentication broken?',
        '',
        '# Better — it can see the code',
        'why is this broken? #selection',
        '',
        '# Best — it can see the code AND the actual failure',
        'why is this broken? #selection #read/problems #read/terminalLastCommand',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Slash Commands — The Everyday Ones')
    y -= 6
    y = p.table(MX, y, ['Command', 'Does'], [
        ('/explain', 'Explain the selected code or a concept'),
        ('/fix', 'Propose a fix for an error or failing lint'),
        ('/tests', 'Generate unit tests for the selection'),
        ('/setupTests', 'Set up a testing framework for the project'),
        ('/doc', 'Write documentation comments'),
        ('/new', 'Scaffold a new project or file'),
        ('/newNotebook', 'Create a Jupyter notebook'),
        ('/plan', 'Produce an implementation plan before any code'),
        ('/search', 'Turn a description into a workspace search'),
        ('/startDebugging', 'Set up a debug configuration'),
    ], [150, CW - 150])
    y -= 16
    y = p.subheading(MX, y, '/plan is the one people skip')
    y -= 4
    y = p.body(MX, y, 'On anything non-trivial, ask for the plan first. You get a cheap, '
                      'readable statement of what it intends to do — and correcting a '
                      'plan costs a fraction of correcting the code it would have '
                      'written from a misunderstanding.')
    y -= 8
    p.info_panel(MX, y, 'SESSION COMMANDS', [
        '/clear       start over        /compact   summarise to reclaim context',
        '/fork        branch this session, keeping the history so far',
        '/debug       open the chat debug view',
        '/troubleshoot   analyse agent logs when a run went wrong',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Participants — Asking a Specialist')
    y = p.body(MX, y - 6,
               'An @ participant routes your question to something that knows a '
               'particular domain, and has its own tools for it.')
    y -= 10
    y = p.table(MX, y, ['Participant', 'Knows about'], [
        ('@github', 'Your repositories, issues, pull requests, GitHub skills'),
        ('@terminal', 'The integrated terminal and shell commands'),
        ('@vscode', 'VS Code itself — settings, commands, extension APIs'),
    ], [130, CW - 130])
    y -= 16
    y = p.subheading(MX, y, 'The two that save the most time')
    y -= 4
    y = p.body(MX, y, '@vscode answers "how do I make the editor do X" without a trip to '
                      'the settings search. @terminal turns a description into the '
                      'command, and — more usefully — explains a command before you run '
                      'it.')
    y -= 8
    y = p.code_block(MX, y, [
        '@vscode how do I stop it formatting on save for Markdown only?',
        '@terminal what does this actually delete?',
        '@github what changed in this repo since Friday?',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Participants are context, not personality', [
        'Adding @terminal does not make it "act like" a shell expert — it gives the',
        'model access to your terminal state. The gain is information, not tone.',
    ])
    y -= 14
    y = p.warn_box(MX, y, 'Always @terminal before you run something destructive', [
        'Asking what a command does costs a fraction of a credit. Running an rm or a',
        'force-push you did not fully understand costs considerably more.',
    ])
    y -= 12
    p.info_panel(MX, y, 'PARTICIPANTS ARE EXTENSIBLE', [
        'Extensions can add their own participants and skills, so the @ list on your',
        'machine may be longer than the three above. Type @ to see yours.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Context References — The Important Ones')
    y = p.body(MX, y - 6,
               'A # reference tells chat exactly what to look at. This is the single '
               'highest-leverage habit in the volume.')
    y -= 10
    y = p.table(MX, y, ['Reference', 'Adds'], [
        ('#selection', 'Whatever is highlighted in the editor'),
        ('#<filename>', 'A specific file — start typing the name'),
        ('#<folder>', 'A whole folder'),
        ('#<symbol>', 'A function, class or method by name'),
        ('#changes', 'Your current source-control changes'),
        ('#search/codebase', 'Lets it search the project for relevant code'),
        ('#read/problems', 'Everything in the Problems panel'),
        ('#read/terminalLastCommand', 'The last command you ran and its output'),
        ('#session', 'A previous chat session'),
    ], [200, CW - 200])
    y -= 16
    y = p.info_panel(MX, y, 'THE PATTERN THAT FIXES MOST BAD ANSWERS', [
        'Bad:   "why is my test failing?"',
        'Good:  "why is this failing? #read/problems #read/terminalLastCommand"',
        '',
        'Same question. The second one can actually see the failure.',
    ])
    y -= 14
    y = p.subheading(MX, y, '#search/codebase is not free')
    y -= 4
    p.body(MX, y, 'Letting it search the project is powerful and is exactly what makes '
                  'agent runs expensive. When you already know which file matters, name '
                  'the file — it is cheaper, faster and more accurate than asking it to '
                  'go looking. Save codebase search for when you genuinely do not know '
                  'where something lives.')
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Tools — What It Is Allowed To Do')
    y = p.body(MX, y - 6,
               'Recent versions group capabilities into named tools under a namespace. '
               'You rarely need to name these by hand in ask mode — they matter because '
               'they are what agent mode draws on, and what it asks permission for.')
    y -= 10
    y = p.table(MX, y, ['Namespace', 'Covers'], [
        ('#read', 'Reading files, notebook output, terminal state, problems'),
        ('#search', 'Codebase search, text and file search, usages, changes'),
        ('#edit', 'Creating files and directories, applying edits'),
        ('#execute', 'Running commands, tasks, notebook cells, reading output'),
        ('#web', 'Fetching web content'),
        ('#browser', 'Driving an integrated browser and taking screenshots'),
        ('#agent', 'Delegating to other agents or an isolated subagent'),
        ('#todos', 'Tracking progress through a multi-step task'),
    ], [110, CW - 110])
    y -= 16
    y = p.subheading(MX, y, 'Read the namespaces as a risk ladder')
    y -= 4
    y = p.body(MX, y, '#read and #search only look. #edit changes your files. #execute '
                      'runs commands on your machine. That ordering is exactly how '
                      'carefully you should read an approval prompt for each.')
    y -= 10
    y = p.table(MX, y, ['Namespace', 'Worst case if it goes wrong'], [
        ('#read / #search', 'It wastes credits reading the wrong thing'),
        ('#web / #browser', 'It pulls in content you did not vet'),
        ('#edit', 'Your files change — recoverable if you committed first'),
        ('#execute', 'Arbitrary commands run on your machine'),
    ], [160, CW - 160])
    y -= 14
    p.warn_box(MX, y, '#execute is the one to read carefully', [
        'Everything else is recoverable with git. A command that touches something',
        'outside the repository is not. This is why chapter 3 spends a page on',
        'approval settings rather than a paragraph.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Putting It Together')
    y = p.body(MX, y - 6,
               'A good chat prompt is usually a command, a reference and one sentence — '
               'not a paragraph of polite preamble.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Explain something you are looking at',
        '/explain #selection',
        '',
        '# Tests, with the conventions of a file you already like',
        '/tests #selection  match the style in #tests/test_orders.py',
        '',
        '# Debug with the actual evidence attached',
        'Why does this fail? #read/problems #read/terminalLastCommand',
        '',
        '# Scoped change, named files only',
        'Add retries to the two network calls in #api/client.py. Nothing else.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'Three habits')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Attach evidence with # before you describe the problem in words',
        'Name the files you want touched — and say "nothing else"',
        'Ask for a plan before a change you cannot easily undo',
    ], step=22)
    y -= 8
    p.info_panel(MX, y, 'WHAT A GOOD PROMPT IS NOT', [
        'It is not polite, long, or carefully worded. "Please could you kindly help',
        'me understand why my code might not be working as expected" carries less',
        'information than "/explain #selection" and costs more to process.',
        'Precision beats courtesy — the model is not keeping score.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 3 — AGENT MODE

def ch3(v):
    lbl = 'Chapter 3  ·  Agent Mode'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Actually Happens')
    y = p.body(MX, y - 6,
               'Agent mode is a loop, not a single answer. Understanding the loop is what '
               'lets you predict both the result and the bill.')
    y -= 10
    y = p.step_card(MX, y, 1, 'It plans', [
        'Turns your goal into steps, often surfaced as a visible todo list.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'It gathers context', [
        'Searches the codebase, opens files, reads terminal output.',
        'This is the part that costs money on a vague goal.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'It acts', [
        'Edits files, creates them, runs commands — asking approval as configured.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'It verifies', [
        'Runs tests or the build, reads the output, and decides whether it worked.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'It iterates or stops', [
        'Failure feeds back into the loop. Success ends it.',
    ])
    y -= 8
    p.tip_box(MX, y, 'Give it a way to check itself', [
        'A task with a test to run converges. A task with no way to verify just',
        'produces something plausible and stops. "Make the failing test pass" is a',
        'far better instruction than "fix the bug".',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Writing a Task It Can Finish')
    y = p.body(MX, y - 6,
               'The difference between a good agent run and an expensive mess is almost '
               'entirely in the task description.')
    y -= 10
    y = p.table(MX, y, ['A good task has', 'Because'], [
        ('A named scope', 'It stops searching the whole repo'),
        ('A definition of done', 'It knows when to stop'),
        ('A way to verify', 'It can check itself rather than guess'),
        ('Explicit exclusions', 'It does not "improve" things you did not ask about'),
    ], [180, CW - 180])
    y -= 16
    y = p.code_block(MX, y, [
        '# Weak — no scope, no finish line, nothing to verify against',
        'Improve the test coverage of this project.',
        '',
        '# Strong — all four',
        'Add unit tests for every public function in services/pricing.py.',
        'Cover happy path, empty input and the discount boundary at 100.',
        'Use pytest and match the style of tests/test_orders.py.',
        'Run pytest and make sure everything passes.',
        'Do not modify any file outside tests/.',
    ])
    y -= 12
    y = p.warn_box(MX, y, '"Do not modify anything else" earns its place', [
        'Agents are helpful by default and will tidy things you did not ask about.',
        'One sentence of exclusion saves a large and confusing diff.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Reuse your good task descriptions', [
        'A task description that worked is worth keeping. Volume 4 covers prompt',
        'files, which turn a good one-off instruction into a reusable command.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Approving Tools')
    y = p.body(MX, y - 6,
               'When an agent wants to run a command or edit a file, it asks. How much it '
               'asks is configurable, and this is the most consequential setting in the '
               'whole product.')
    y -= 10
    y = p.table(MX, y, ['Setting', 'Behaviour'], [
        ('Approve each time', 'Safest. Slow on a long task, and correct while learning'),
        ('Approve for this session', 'Reasonable middle ground once you trust the task'),
        ('/yolo  or  /autoApprove', 'Global auto-approval. It stops asking entirely'),
        ('/disableYolo', 'Turns global auto-approval back off'),
    ], [200, CW - 200])
    y -= 16
    y = p.warn_box(MX, y, 'Understand what auto-approval means before you enable it', [
        'It approves shell commands too. An agent that decides the way to fix your',
        'failing build is to delete and reinstall something will simply do it, and',
        'tell you afterwards. Use it on a branch, in a repo you can throw away, and',
        'never on anything with credentials or production access in reach.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'A safer default', [
        'Work on a branch and commit before you start. Then a bad run is one',
        'git reset away rather than an archaeology exercise.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHERE AUTO-APPROVAL IS ACTUALLY REASONABLE', [
        'A scratch repository you would not mind losing. A container or VM. A',
        'branch with everything committed, on a machine with no production',
        'credentials in the environment. Outside those, the time it saves is not',
        'worth the class of mistake it enables.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Keeping It On A Leash')
    y = p.body(MX, y - 6,
               'A long agent run is where credits go, and where results get worse rather '
               'than better — context fills up, and it starts forgetting the early part '
               'of its own plan.')
    y -= 10
    y = p.subheading(MX, y, 'Signals to stop and restart')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'It has tried the same fix twice with different wording',
        'It starts editing files that have nothing to do with the task',
        'The todo list is growing rather than shrinking',
        'It is explaining more than it is changing',
        'You no longer understand what it is doing',
    ], step=22)
    y -= 8
    y = p.info_panel(MX, y, 'WHAT TO DO INSTEAD', [
        'Stop the run. Keep whatever is genuinely good, discard the rest, and start',
        'a fresh session with a narrower task informed by what you just learned.',
        'A second small run beats rescuing a large confused one, and usually costs',
        'less than letting the first one continue.',
    ])
    y -= 12
    y = p.tip_box(MX, y, '/compact before a long session gets confused', [
        'Summarising the conversation reclaims context without losing the thread.',
        'Cheaper and more effective than hoping it remembers.',
    ])
    y -= 12
    p.table(MX, y, ['Run length', 'What usually happens'], [
        ('A few steps', 'Focused, cheap, easy to review'),
        ('A dozen steps', 'Still good if the task was well scoped'),
        ('Many steps, growing todos', 'Context filling; quality starting to drop'),
        ('Long and still going', 'Stop. Restart narrower with what you learned'),
    ], [200, CW - 200])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Agent Mode Is Genuinely Good At')
    y -= 6
    y = p.table(MX, y, ['Works well', 'Why'], [
        ('Mechanical multi-file changes', 'Repetitive, verifiable, tedious for you'),
        ('Writing a test suite', 'A clear finish line — the tests run or they do not'),
        ('Migrating a pattern', 'Rename, restructure, one shape into another'),
        ('Wiring up boilerplate', 'Config, scaffolding, plumbing between known pieces'),
        ('Fixing a failing build', 'The error message is the specification'),
    ], [220, CW - 220])
    y -= 16
    y = p.table(MX, y, ['Goes badly', 'Why'], [
        ('Design decisions', 'It will pick one and defend it, not raise the trade-off'),
        ('Anything undefined', 'Without a finish line it produces plausible sprawl'),
        ('Domain rules', 'It cannot infer what it was never told'),
        ('Large vague refactors', 'Context runs out halfway and coherence goes'),
    ], [220, CW - 220])
    y -= 14
    y = p.info_panel(MX, y, 'THE TEST', [
        'Could you write down, in one sentence, how you would check whether it',
        'succeeded? If not, it is not an agent task yet — it is a conversation.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Turn a bad agent task into a good one', [
        'Take the vague version to ask mode first. Two minutes of conversation',
        'usually produces the specific, checkable task you should have written —',
        'at a fraction of what the agent would have spent working it out.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Worked Example')
    y = p.body(MX, y - 6, 'A realistic run, start to finish, on a task agent mode suits.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Commit first', [
        'git switch -c copilot/pricing-tests && git commit -am "wip"',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'State the task with all four parts', [
        'Scope, definition of done, verification, exclusions. See page 14.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Watch the first two tool approvals', [
        'They tell you whether it understood. Wrong file? Stop immediately —',
        'you have spent almost nothing at this point.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Let it run to verification', [
        'It should end by running the tests and reporting the result.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Review the diff yourself', [
        'Chapter 4. "The tests pass" is not the same as "the tests are good".',
    ])
    y -= 8
    p.warn_box(MX, y, 'The first two approvals are the cheap exit', [
        'Most bad runs are visibly wrong within two steps. Stopping there costs',
        'almost nothing; letting it finish out of politeness costs the whole task.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 4 — REVIEWING

def ch4(v):
    lbl = 'Chapter 4  ·  Reviewing What It Wrote'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Step Everyone Rushes')
    y = p.body(MX, y - 6,
               'Edit and agent modes hand you a set of changes across several files. The '
               'temptation is to skim, see green tests, and accept. That is where the '
               'defects that survive into production come from.')
    y -= 10
    y = p.table(MX, y, ['Control', 'Does'], [
        ('Accept file', 'Applies this file\'s changes'),
        ('Discard file', 'Rejects this file, keeps the rest'),
        ('Accept all', 'Applies everything — use it last, not first'),
        ('Discard all', 'Throws the whole set away'),
        ('Undo', 'Reverses an applied edit'),
    ], [140, CW - 140])
    y -= 16
    y = p.subheading(MX, y, 'Review per file, not per set')
    y -= 4
    y = p.body(MX, y, 'The per-file accept exists because a change set is rarely uniformly '
                      'good. Taking the two files it got right and rejecting the third is '
                      'normal, and far better than accepting all and repairing.')
    y -= 8
    y = p.tip_box(MX, y, 'Read the smallest diff first', [
        'A one-line change in a file you did not expect it to touch is the single',
        'most informative thing in the set. Start there, not with the big file.',
    ])
    y -= 12
    p.info_panel(MX, y, 'REVIEW IT LIKE SOMEONE ELSE WROTE IT', [
        'You watched it work, which makes the change feel familiar and reviewed',
        'when it is neither. The useful frame is a pull request from a fast,',
        'confident colleague who has never read your codebase before — helpful,',
        'productive, and entirely without judgement about your conventions.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What To Actually Look For')
    y -= 6
    y = p.table(MX, y, ['Check', 'Looking for'], [
        ('Files you did not expect', 'Scope creep — the clearest warning sign'),
        ('Deletions', 'Removed code is easy to miss and expensive to lose'),
        ('New dependencies', 'Does the package exist? Do you want it?'),
        ('Error handling', 'Exceptions silently swallowed to make tests pass'),
        ('Tests that assert nothing', 'assert True, or asserting the mock was called'),
        ('Changed behaviour', 'A "refactor" that quietly does something different'),
        ('Secrets and config', 'Hard-coded values that should not be in the file'),
    ], [200, CW - 200])
    y -= 16
    y = p.warn_box(MX, y, 'Tests passing is weak evidence', [
        'An agent that can edit both the code and the tests can make any suite pass.',
        'Read what the tests assert, not just whether they are green — this is the',
        'single most common way a confident agent run goes wrong.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'A CHEAP EXTRA CHECK', [
        'git diff --stat before you commit. If the shape of that summary surprises',
        'you, the change set is not what you thought you approved.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Run the tests yourself', [
        'Not because it lied, but because "I ran the tests" and "the tests pass on',
        'your machine, in your environment" are different claims. It takes seconds.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Working With Version Control')
    y = p.body(MX, y - 6,
               'Git is what makes all of this safe. Without it, reviewing a multi-file '
               'agent change is genuinely risky; with it, the worst case is a discarded '
               'branch.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Before you start anything agentic',
        'git switch -c copilot/the-task',
        'git commit -am "checkpoint before agent run"',
        '',
        '# After — see the shape before you read the detail',
        'git diff --stat',
        'git diff                      # then the detail',
        '',
        '# If it went badly',
        'git restore .                 # discard uncommitted changes',
        'git switch - && git branch -D copilot/the-task',
    ])
    y -= 12
    y = p.subheading(MX, y, 'Commit in small pieces')
    y -= 4
    y = p.body(MX, y, 'Accept and commit one coherent part at a time rather than the whole '
                      'set at once. It costs you nothing and turns "something in here '
                      'broke it" into a two-minute bisect.')
    y -= 8
    y = p.tip_box(MX, y, '#changes puts your diff back in the conversation', [
        'Ask chat to review its own change set with #changes attached. It catches a',
        'surprising amount, and costs a fraction of what producing it did.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Self-review is a filter, not an approval', [
        'It will find real problems, and it will also miss the ones caused by the',
        'misunderstanding that produced the change in the first place. It narrows',
        'what you have to read. It does not replace reading.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When To Reject Everything')
    y = p.body(MX, y - 6,
               'Discarding a whole change set feels wasteful after watching it work. It '
               'is usually the cheapest decision available.')
    y -= 10
    y = p.subheading(MX, y, 'Reject the set if')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'You do not understand a substantial part of it',
        'It touched files well outside the stated scope',
        'It changed tests you did not ask it to change',
        'The approach is wrong, even though the code works',
        'You would not approve this in a colleague\'s pull request',
    ], step=22)
    y -= 8
    y = p.info_panel(MX, y, 'THE SUNK COST TRAP', [
        'Credits already spent are spent whether you accept the change or not.',
        'Accepting code you do not understand to justify the cost is how a saving',
        'becomes a liability. The money is gone either way — only the code is still',
        'your decision.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Rejecting is data', [
        'Note why it was wrong, then restate the task with that as an explicit',
        'constraint. The second attempt is usually much better and much cheaper.',
    ])
    y -= 12
    p.info_panel(MX, y, 'PARTIAL ACCEPTANCE IS THE COMMON CASE', [
        'Most change sets are not all good or all bad. Take the files it got right,',
        'discard the rest, and restate the remainder as a smaller task. That is a',
        'normal outcome and a good one — not a failed run.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 5 — GOOD RESULTS

def ch5(v):
    lbl = 'Chapter 5  ·  Getting Good Results'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Patterns That Reliably Work')
    y -= 6
    y = p.step_card(MX, y, 1, 'Show, then ask', [
        'Point at code you already like and ask for more in that shape.',
        '"Like #api/users.py" outperforms three sentences of description.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Constrain the output', [
        '"Only the function, no explanation" or "reply with a diff".',
        'You get less to read and fewer credits spent producing prose.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Ask for the plan first', [
        '/plan on anything non-trivial. Correcting a plan is cheap.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Attach the evidence', [
        '#read/problems and #read/terminalLastCommand instead of describing an error.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Say what not to do', [
        'Exclusions are as useful as instructions, and much shorter.',
    ])
    y -= 8
    p.tip_box(MX, y, 'One change at a time', [
        'Two unrelated requests in one prompt reliably produces one good answer and',
        'one bad one, and you cannot tell which is which without checking both.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When It Is Not Working')
    y = p.body(MX, y - 6,
               'The instinct on a bad answer is to rephrase and try again. Usually the '
               'problem is not the wording.')
    y -= 10
    y = p.table(MX, y, ['Symptom', 'Usually means'], [
        ('Confident, wrong specifics', 'It cannot see the code — add a # reference'),
        ('Ignores your conventions', 'Show it a file that follows them'),
        ('Invents functions', 'Not enough context; it is filling gaps'),
        ('Answer too generic', 'Question too generic — name files and constraints'),
        ('Keeps missing the point', 'Start a new session; context is polluted'),
        ('Right idea, wrong details', 'Good — narrow it and ask again, do not restart'),
    ], [200, CW - 200])
    y -= 16
    y = p.info_panel(MX, y, 'THE TWO-ATTEMPT RULE', [
        'If two focused attempts have not produced what you want, stop and write it',
        'yourself. You will finish sooner, you will understand the result, and you',
        'will stop paying for iterations that are not converging.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Polluted context is real', [
        'A long session that went wrong early keeps referring back to the wrong turn.',
        'Ctrl+N costs nothing and fixes more than any amount of rephrasing.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Keep what worked', [
        'When a prompt produces a genuinely good result, save it. Most people',
        'rediscover the same three or four phrasings every week — Volume 4 turns',
        'those into prompt files you can invoke by name.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Shortcut', 'Opens'], [
        ('Ctrl+Alt+I', 'Chat view'),
        ('Ctrl+I', 'Inline chat (editor or terminal)'),
        ('Ctrl+Shift+I', 'Agents mode'),
        ('Ctrl+Shift+Alt+L', 'Quick chat'),
        ('Ctrl+N', 'New chat session'),
    ], [150, CW - 150])
    y -= 14
    y = p.table(MX, y, ['Symbol / command', 'Use'], [
        ('/explain  /fix  /tests', 'The everyday three'),
        ('/plan', 'Before anything non-trivial'),
        ('/compact  /clear  /fork', 'Session hygiene'),
        ('/yolo  /disableYolo', 'Global auto-approval on / off'),
        ('@github  @terminal  @vscode', 'Specialists'),
        ('#selection  #<file>  #changes', 'The context you attach most'),
        ('#read/problems', 'The Problems panel'),
        ('#read/terminalLastCommand', 'Last command and its output'),
        ('#search/codebase', 'Let it search the project'),
    ], [220, CW - 220])
    y -= 14
    p.info_panel(MX, y, 'THE FIVE THINGS WORTH MEMORISING', [
        'Ctrl+N when answers drift.  /plan before anything non-trivial.',
        '#selection to attach what you are looking at.  Name the files, and say',
        '"nothing else".  Review per file, never accept-all first.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('Chat refuses to answer', 'Out of credits — completions still work'),
        ('Answers ignore my code', 'Attach #selection or the file explicitly'),
        ('Agent edits the wrong files', 'Name the scope and add "nothing else"'),
        ('Agent never finishes', 'No definition of done — give it something to verify'),
        ('It keeps asking approval', 'Approve for the session, or narrow the task'),
        ('It stopped asking approval', 'Auto-approval is on — /disableYolo'),
        ('Lost track of a long session', '/compact, or Ctrl+N and restate'),
        ('Slash command missing', 'Type / to see the live list for your version'),
        ('Costs more than expected', 'Agent mode on vague goals — see chapter 1'),
    ], [200, CW - 200])
    y -= 18
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 3 — Copilot CLI & the Coding Agent: Copilot in the terminal, and',
        'handing an issue to an agent that opens the pull request itself.',
    ])
    y -= 12
    p.tip_box(MX, y, 'More guides', [
        'etsy.com/shop/FranksMarketDesigns  ·  Unofficial and independent.',
        'Not affiliated with, endorsed by, or sponsored by GitHub or Microsoft.',
    ])
    v.close()


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v = Volume(OUT, COPILOT,
               title='Chat & Agent Mode',
               subtitle='The metered half of Copilot — and how to get work out of it',
               badge='VOLUME TWO',
               tagline='ASK  ·  EDIT  ·  AGENT  ·  REVIEW  ·  COST DISCIPLINE')

    total = 2 + 4 + 6 + 6 + 4 + 4
    v.cover(
        stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('3', 'MODES'), ('2026', 'EDITION')],
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
