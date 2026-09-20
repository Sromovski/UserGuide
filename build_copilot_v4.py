#!/usr/bin/env python3
"""Copilot Field Guide — Volume 4: Customisation.

    python build_copilot_v4.py

How to stop re-explaining your conventions on every single request.

FACTS VERIFIED 2026-08-02 against code.visualstudio.com/docs/copilot/customization.
Seven customisation types, each with an exact naming convention — those conventions are
the load-bearing content, so they live in tables that are cheap to reprint.

Worth knowing for the series: VS Code Copilot also reads CLAUDE.md (using `paths` rather
than `applyTo`), so a repository configured for one tool is partly configured for both.
"""
import os

from fieldguide import COPILOT, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Copilot_Field_Guide_Volume_4_Customisation.pdf')

CHAPTERS = [
    (1, 'Instruction Files', 'Say it once, and stop repeating yourself', 3),
    (2, 'Prompt Files', 'Turn a good prompt into a slash command', 8),
    (3, 'Custom Agents & Skills', 'Focused roles, and capabilities it loads itself', 13),
    (4, 'MCP Servers & Hooks', 'Your own tools, and deterministic guardrails', 18),
    (5, 'Rolling It Out', 'Plugins, precedence, and what to adopt first', 23),
]


# ══════════════════════════════════════════════════════ CH 1 — INSTRUCTIONS

def ch1(v):
    lbl = 'Chapter 1  ·  Instruction Files'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The One Everybody Should Do')
    y = p.body(MX, y - 6,
               'If you take one thing from this volume, take this. An instruction file '
               'states your conventions once, in the repository, and Copilot applies them '
               'to every request from then on — for you and for everyone else on the team.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Create the file', [
        '.github/copilot-instructions.md at the root of your repository.',
        'Or let Copilot draft it for you: run /init in chat.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Write your conventions in plain markdown', [
        'No special syntax required. Headings and bullets are enough.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Commit it', [
        'It is repository configuration — it belongs in version control,',
        'and everyone on the team gets it automatically.',
    ])
    y -= 10
    y = p.info_panel(MX, y, 'WHAT CHANGES IMMEDIATELY', [
        'It stops suggesting the test framework you migrated away from. It matches',
        'your error-handling style without being asked. It stops proposing the',
        'folder layout you abandoned two years ago. Small things, on every request.',
    ])
    y -= 12
    p.tip_box(MX, y, '/init writes a first draft from your codebase', [
        'It reads the project and proposes an instructions file. Treat it as a',
        'starting point to edit down, not a finished artefact — it will be too long.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Four Files It Reads')
    y -= 6
    y = p.table(MX, y, ['File', 'Where', 'Applies'], [
        ('copilot-instructions.md', '.github/', 'Always'),
        ('*.instructions.md', '.github/instructions/', 'By glob or match'),
        ('AGENTS.md', 'Repository root', 'Always'),
        ('CLAUDE.md', 'Root, .claude/, ~/.claude/', 'Always'),
    ], [170, 170, CW - 340])
    y -= 16
    y = p.subheading(MX, y, 'CLAUDE.md is read too')
    y -= 4
    y = p.body(MX, y, 'If you already configured a repository for Claude Code, Copilot '
                      'picks up that file as well — note it uses `paths` for globs where '
                      'the Copilot files use `applyTo`. A repository set up for one tool '
                      'is partly set up for both, which matters if your team uses more '
                      'than one assistant.')
    y -= 8
    y = p.info_panel(MX, y, 'WHICH TO USE', [
        'Use .github/copilot-instructions.md unless you have a reason not to. AGENTS.md',
        'is the more portable convention across tools; nested variants in subfolders',
        'are experimental. Pick one always-on file and stick to it — two files saying',
        'slightly different things is worse than either alone.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Do not maintain the same rules in three places', [
        'They will drift, and the model will be handed contradictory instructions.',
        'One always-on file, plus targeted files for genuine per-language differences.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Targeted Instructions')
    y = p.body(MX, y - 6,
               'A *.instructions.md file applies only where you say. This is how you give '
               'your Python and your TypeScript different conventions without one leaking '
               'into the other.')
    y -= 10
    y = p.code_block(MX, y, [
        '# .github/instructions/python.instructions.md',
        '---',
        'name: Python Standards',
        'description: Conventions for Python files',
        'applyTo: "**/*.py"',
        '---',
        '',
        '- Type hints on every public function.',
        '- Raise specific exceptions, never bare except.',
        '- Tests use pytest, arrange-act-assert, no unittest.',
        '- Format with ruff. Do not argue with the formatter.',
    ])
    y -= 12
    y = p.table(MX, y, ['Field', 'Does'], [
        ('applyTo', 'Glob of files it applies to, relative to the repo root'),
        ('name', 'Display name — defaults to the filename'),
        ('description', 'Short summary, shown on hover'),
    ], [110, CW - 110])
    y -= 14
    p.tip_box(MX, y, 'Globs take a comma-separated list', [
        'applyTo: "**/*.ts,**/*.tsx" covers both. And applyTo: "**" makes a file',
        'always-on, which is how the project-wide file behaves by default.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Writing Instructions That Work')
    y = p.body(MX, y - 6,
               'The failure mode is a long, aspirational document nobody follows — '
               'including the model. Short, specific and true beats comprehensive.')
    y -= 10
    y = p.table(MX, y, ['Write this', 'Not this'], [
        ('"Use pytest, not unittest"', '"Write good tests"'),
        ('"Raise specific exceptions"', '"Handle errors properly"'),
        ('"snake_case for functions"', '"Follow naming conventions"'),
        ('"Never edit files in vendor/"', '"Be careful with dependencies"'),
        ('"Prefer composition to inheritance"', '"Write clean code"'),
    ], [240, CW - 240])
    y -= 16
    y = p.subheading(MX, y, 'What belongs in there')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'The stack and the versions you are actually on',
        'How to run the tests, the build and the linter',
        'Conventions a newcomer would get wrong',
        'Directories that are off limits',
        'Decisions already made, so it stops re-proposing the alternative',
    ], step=22)
    y -= 6
    p.warn_box(MX, y, 'It costs tokens on every single request', [
        'This file is prepended to your requests. A thousand lines of aspiration is',
        'paid for on every turn, forever. Keep it to what actually changes output.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Precedence')
    y = p.body(MX, y - 6,
               'When several instruction sources apply, all of them are provided. Where '
               'they conflict, the higher priority wins.')
    y -= 10
    y = p.table(MX, y, ['Priority', 'Source'], [
        ('1 — highest', 'Personal instructions (your user profile)'),
        ('2', 'Repository instructions (copilot-instructions.md, AGENTS.md)'),
        ('3 — lowest', 'Organization instructions'),
    ], [130, CW - 130])
    y -= 16
    y = p.info_panel(MX, y, 'PERSONAL INSTRUCTIONS BEAT THE REPOSITORY', [
        'Which is worth knowing before you debug why a teammate gets different',
        'suggestions to you on the same codebase. Personal preferences live in your',
        'user profile and follow you between projects — useful for "explain briefly,',
        'I am experienced", less useful for anything the team should share.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'A rule of thumb')
    y -= 4
    y = p.body(MX, y, 'Anything about the CODE goes in the repository, so the team gets '
                      'it. Anything about HOW YOU LIKE TO BE TALKED TO goes in your '
                      'personal instructions. Putting a personal style preference in the '
                      'shared file is how teams end up arguing about tooling.')
    y -= 10
    p.table(MX, y, ['Belongs where', 'Example'], [
        ('Repository', '"Use pytest, not unittest"'),
        ('Repository', '"Never edit files under generated/"'),
        ('Personal', '"Explain briefly — I am experienced"'),
        ('Personal', '"Show me the diff, not a description of it"'),
        ('Organization', '"All new services must emit structured logs"'),
    ], [140, CW - 140])
    v.close()


# ══════════════════════════════════════════════════════ CH 2 — PROMPT FILES

def ch2(v):
    lbl = 'Chapter 2  ·  Prompt Files'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Good Prompt, Saved')
    y = p.body(MX, y - 6,
               'Volume 2 ended by telling you to keep the prompts that worked. A prompt '
               'file is where they go — a *.prompt.md file becomes a slash command you '
               'invoke by name.')
    y -= 10
    y = p.code_block(MX, y, [
        '# .github/prompts/new-endpoint.prompt.md',
        '---',
        'description: Scaffold a REST endpoint the way we do it',
        '---',
        '',
        'Create a new endpoint in api/routes/.',
        '',
        '- Follow the structure of api/routes/orders.py exactly.',
        '- Validate input with the existing pydantic schema pattern.',
        '- Return our standard error envelope on failure.',
        '- Add a test in tests/routes/ covering success, bad input and 404.',
        '- Do not modify any existing route.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THEN, IN CHAT', [
        '/new-endpoint    — and it does the whole thing, the same way, every time.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'The test for whether something should be a prompt file', [
        'Have you typed roughly this three times? Then it is a prompt file. If you',
        'have typed it once, it is just a prompt.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHY THIS BEATS A SNIPPET IN YOUR NOTES', [
        'A prompt saved in a scratch file is one you have to find, remember and',
        'paste. A prompt file is a slash command your whole team can use without',
        'knowing it exists — they just see /new-endpoint in the list and try it.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Instructions vs Prompts')
    y = p.body(MX, y - 6,
               'These are the two people confuse, and the distinction is simple once '
               'stated.')
    y -= 10
    y = p.table(MX, y, ['', 'Instruction file', 'Prompt file'], [
        ('Applies', 'Automatically', 'When you invoke it'),
        ('Answers', '"How do we do things?"', '"Do this specific job"'),
        ('Contains', 'Standards and constraints', 'A task'),
        ('Invoked', 'Never — it is ambient', '/name'),
        ('Cost', 'Tokens on every request', 'Only when used'),
    ], [90, 200, CW - 290])
    y -= 16
    y = p.subheading(MX, y, 'They compose')
    y -= 4
    y = p.body(MX, y, 'A prompt file does not need to restate your conventions — the '
                      'instruction file is already there. That is why prompt files stay '
                      'short: they describe the job, and the ambient instructions supply '
                      'the house style.')
    y -= 8
    y = p.warn_box(MX, y, 'Do not put standing rules in a prompt file', [
        'A rule that only applies when you remember to invoke it is not a rule.',
        'Anything that should always be true belongs in the instruction file.',
    ])
    y -= 12
    y = p.tip_box(MX, y, '/create-prompt writes one for you', [
        'Had a conversation that went well? /create-prompt turns it into a reusable',
        'prompt file. Same for /create-instruction, /create-skill and /create-agent.',
    ])
    y -= 12
    p.info_panel(MX, y, 'A QUICK WAY TO TELL THEM APART', [
        'Read the file out loud. If it starts "we always..." it is an instruction',
        'file. If it starts "create..." or "review..." it is a prompt file. Files',
        'that do both are the ones that end up confusing everybody.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Prompt Files Worth Having')
    y -= 6
    y = p.table(MX, y, ['Prompt file', 'Does'], [
        ('/new-endpoint', 'Scaffold a route the way this project does it'),
        ('/add-tests', 'Tests in your framework, your layout, your naming'),
        ('/review', 'Review a diff against your actual checklist'),
        ('/migrate-component', 'Move one component to the new pattern'),
        ('/changelog', 'Write the entry in your house format'),
        ('/explain-for-review', 'Summarise a diff for a PR description'),
    ], [180, CW - 180])
    y -= 16
    y = p.subheading(MX, y, 'Where to keep them')
    y -= 4
    y = p.body(MX, y, 'In the repository, committed, alongside the instruction files. A '
                      'prompt file that only exists on your machine helps one person; the '
                      'same file committed makes the whole team consistent, and makes '
                      'onboarding a matter of reading the prompts directory.')
    y -= 8
    y = p.info_panel(MX, y, 'THEY DOUBLE AS DOCUMENTATION', [
        'A prompts directory is an unusually honest description of how a team',
        'actually works — the tasks they do often enough to have automated. New',
        'joiners learn more from reading it than from most onboarding documents.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Name them the way you would say them', [
        '/add-tests, not /test-generation-workflow. They appear in the slash command',
        'list and get picked by whoever recognises the name fastest — which means a',
        'clear name gets used and a clever one does not.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Managing Them')
    y -= 6
    y = p.table(MX, y, ['Command', 'Does'], [
        ('/prompts', 'Manage prompt files'),
        ('/instructions', 'Manage instruction files'),
        ('/skills', 'Configure agent skills'),
        ('/agents', 'Configure custom agents'),
        ('/hooks', 'Configure hooks'),
        ('/create-prompt', 'Generate a prompt file from this conversation'),
        ('/create-instruction', 'Generate an instruction file'),
        ('/create-skill', 'Generate a skill'),
        ('/create-agent', 'Generate a custom agent'),
        ('/create-hook', 'Generate a hook'),
    ], [180, CW - 180])
    y -= 16
    y = p.info_panel(MX, y, 'THE /create-* FAMILY IS THE SHORTCUT', [
        'You do not have to learn the file formats to get started. Have the',
        'conversation, then ask Copilot to turn it into the right kind of file.',
        'Read what it produces before committing it — but it saves the blank page.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Review generated customisations like code', [
        'They are configuration that changes every future suggestion. A wrong line',
        'in an instruction file is subtly wrong output forever, and it is the last',
        'place anyone thinks to look.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Realistic Starting Set')
    y = p.body(MX, y - 6,
               'You do not need all seven customisation types. Most teams get most of the '
               'value from two files.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Week one — one instruction file', [
        '.github/copilot-instructions.md. Run /init, cut it down, commit it.',
        'Twenty lines is plenty to start.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Week two — one prompt file', [
        'The task you type most often. /create-prompt from a conversation that',
        'went well, then edit it.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Later, only if you need them', [
        'Targeted instruction files when languages genuinely differ.',
        'Custom agents when one role keeps recurring.',
        'MCP and hooks when there is a specific thing to connect or enforce.',
    ])
    y -= 10
    y = p.info_panel(MX, y, 'THE DOCUMENTATION SAYS THIS TOO', [
        'Adopt customisations gradually rather than all at once: start with project',
        'instructions and add specialised pieces as needs emerge. A repository that',
        'arrives with seven customisation types and no history of using them is',
        'configuration nobody understands or maintains.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Delete what you stop using', [
        'Stale customisation is worse than none — it silently shapes every answer',
        'according to rules the team abandoned months ago.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 3 — AGENTS & SKILLS

def ch3(v):
    lbl = 'Chapter 3  ·  Custom Agents & Skills'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Custom Agents')
    y = p.body(MX, y - 6,
               'A custom agent gives the assistant a focused role — its own instructions, '
               'its own allowed tools, and its own model. A read-only planner. A security '
               'reviewer. A documentation writer that cannot touch source.')
    y -= 10
    y = p.code_block(MX, y, [
        '# .github/agents/planner.agent.md',
        '---',
        'description: Read-only planner. Proposes, never edits.',
        'tools: [read, search]',
        '---',
        '',
        'You produce implementation plans. You never edit files.',
        '',
        'For any request, output:',
        '  1. What you would change, file by file',
        '  2. What could break',
        '  3. How to verify it worked',
        '',
        'If the request is ambiguous, list the questions instead of guessing.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THE POWER IS IN THE TOOL LIST', [
        'An agent given only read and search CANNOT edit your files — not "is asked',
        'not to", cannot. That is a structural guarantee rather than a polite',
        'request, and it is the most useful thing about custom agents.',
    ])
    y -= 12
    p.tip_box(MX, y, 'A read-only planner is the best first custom agent', [
        'It is genuinely useful, it is impossible for it to break anything, and it',
        'teaches you the format on a task with no downside.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Agents Worth Defining')
    y -= 6
    y = p.table(MX, y, ['Agent', 'Tools', 'For'], [
        ('Planner', 'read, search', 'Think before touching anything'),
        ('Reviewer', 'read, search', 'Critique a diff against your standards'),
        ('Test writer', 'read, edit, execute', 'Tests only, and run them'),
        ('Docs writer', 'read, edit', 'Documentation, never source'),
        ('Migrator', 'read, edit, search', 'One mechanical pattern change'),
    ], [110, 160, CW - 270])
    y -= 16
    y = p.subheading(MX, y, 'They can be shared')
    y -= 4
    y = p.body(MX, y, 'A custom agent can be defined in your repository, your organisation '
                      'or your enterprise — and the cloud coding agent from Volume 3 can '
                      'be pointed at one. A "security reviewer" agent defined once at the '
                      'organisation level is available everywhere.')
    y -= 8
    y = p.warn_box(MX, y, 'Restricting tools is a real control, not theatre', [
        'It is also the difference between "the docs agent should not change code"',
        'and "the docs agent cannot change code". Prefer the second.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE MODEL FIELD MATTERS FOR COST', [
        'A planner that only reads and reasons can justify a strong model. A',
        'mechanical migrator does not need one. Setting the model per agent bakes',
        'the Volume 2 cost discipline into the configuration.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Agent Skills')
    y = p.body(MX, y - 6,
               'A skill teaches a repeatable capability, bundled with the scripts, '
               'examples and resources it needs — and the assistant loads it on its own '
               'when the situation calls for it.')
    y -= 10
    y = p.table(MX, y, ['', 'Custom agent', 'Skill'], [
        ('Is', 'A role', 'A capability'),
        ('You', 'Select it', 'Do nothing — it loads itself'),
        ('Contains', 'Instructions, tools, model', 'Instructions plus files and scripts'),
        ('File', '*.agent.md', 'SKILL.md'),
    ], [90, 175, CW - 265])
    y -= 16
    y = p.subheading(MX, y, 'The description is the trigger')
    y -= 4
    y = p.body(MX, y, 'A skill is loaded on demand based on what it says it does. A vague '
                      'description means it never fires; a specific one naming the '
                      'concrete nouns and verbs a user would type means it fires when it '
                      'should. This is the single thing that makes a skill work or not.')
    y -= 8
    y = p.code_block(MX, y, [
        '# Vague — will rarely trigger',
        'description: Helps with database things',
        '',
        '# Specific — triggers when it should',
        'description: Write and run Alembic migrations for this project,',
        '  including the downgrade path and a check against the staging schema.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Skills carry files, prompt files do not', [
        'If your repeatable task needs a script, a template or a reference document',
        'alongside the instructions, it is a skill rather than a prompt file.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing Between Them')
    y = p.body(MX, y - 6,
               'Four mechanisms overlap enough to be confusing. This is the decision in '
               'one table.')
    y -= 10
    y = p.table(MX, y, ['You want', 'Use'], [
        ('Rules applied to everything, always', 'Instruction file'),
        ('Rules for certain files only', '*.instructions.md with applyTo'),
        ('A task you run often, on demand', 'Prompt file'),
        ('A role with restricted tools', 'Custom agent'),
        ('A capability it should load itself', 'Skill'),
        ('Access to an external system', 'MCP server (chapter 4)'),
        ('Something that must always happen', 'Hook (chapter 4)'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'IF IN DOUBT', [
        'Instruction file for how you work. Prompt file for what you do. Everything',
        'else is for a specific problem you will recognise when you have it — and',
        'if you cannot name the problem, you do not need the mechanism yet.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Every mechanism is maintenance', [
        'Each of these is a file someone has to keep true as the codebase changes.',
        'Adopt them because something hurts, not because they exist.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Where They All Live')
    y -= 6
    y = p.code_block(MX, y, [
        'your-repo/',
        '  AGENTS.md                       # always-on, portable convention',
        '  CLAUDE.md                       # read by Copilot too (uses `paths`)',
        '  .github/',
        '    copilot-instructions.md       # always-on, Copilot convention',
        '    instructions/',
        '      python.instructions.md      # applyTo: "**/*.py"',
        '      frontend.instructions.md    # applyTo: "**/*.tsx"',
        '    prompts/',
        '      new-endpoint.prompt.md      # invoked as /new-endpoint',
        '      add-tests.prompt.md         # invoked as /add-tests',
        '    agents/',
        '      planner.agent.md            # read-only role',
        '      reviewer.agent.md',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'USER-LEVEL LOCATIONS TOO', [
        'Personal instruction files live in your user profile — ~/.copilot/',
        'instructions/ or ~/.claude/rules/ — and follow you between projects.',
        'Remember from chapter 1 that these outrank the repository.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Commit all of it', [
        'These files are how your team works, expressed in a form a machine reads.',
        'They belong in version control, in review, and in the same PR as the',
        'convention change they describe.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 4 — MCP & HOOKS

def ch4(v):
    lbl = 'Chapter 4  ·  MCP Servers & Hooks'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'MCP — Connecting Your Own Tools')
    y = p.body(MX, y - 6,
               'Everything so far shapes what Copilot knows. MCP servers change what it '
               'can reach — your database, your ticket system, your internal services — '
               'so it can work with real project data instead of guessing at it.')
    y -= 10
    y = p.table(MX, y, ['Connect', 'So it can'], [
        ('A database', 'Read the actual schema instead of inferring it'),
        ('Your issue tracker', 'Read the ticket it is implementing'),
        ('Internal docs', 'Follow your real conventions, not generic ones'),
        ('Observability', 'Look at the error it is being asked to fix'),
        ('A design system', 'Use components that exist'),
    ], [180, CW - 180])
    y -= 16
    y = p.info_panel(MX, y, 'WHERE IT IS CONFIGURED', [
        'MCP servers are set up through the Agent Customizations editor. The cloud',
        'coding agent from Volume 3 can also be given broader repository access via',
        'MCP settings — which is the documented way past its single-repo default.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'An MCP server is a permission grant', [
        'You are giving a model the ability to query real systems. Start read-only,',
        'start with non-production, and be as deliberate about it as you would be',
        'issuing credentials to a new contractor — because that is what it is.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE SHIFT THIS REPRESENTS', [
        'Instructions, prompts and agents all change how Copilot behaves inside your',
        'editor. MCP is the first thing in this volume that lets it touch something',
        'outside the repository. That is a category change, not another feature, and',
        'it deserves a different level of thought.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What MCP Is Worth Doing')
    y -= 6
    y = p.table(MX, y, ['High value', 'Why'], [
        ('Read-only database schema', 'Removes a whole class of invented columns'),
        ('Issue tracker, read-only', 'It sees the requirement, not your summary'),
        ('Internal component library', 'Stops it inventing components'),
        ('Log or error search', 'Debugging with evidence rather than guesses'),
    ], [220, CW - 220])
    y -= 14
    y = p.table(MX, y, ['Think harder about', 'Why'], [
        ('Write access to anything', 'The blast radius is no longer your repository'),
        ('Production systems', 'A confident wrong query is still a query'),
        ('Anything with customer data', 'It ends up in prompts; know your obligations'),
    ], [220, CW - 220])
    y -= 14
    y = p.subheading(MX, y, 'The pattern that works')
    y -= 4
    y = p.body(MX, y, 'Read-only, non-production, one system at a time. Live with each '
                      'one for a fortnight before adding the next. The value is real, and '
                      'it is almost all in the reading rather than the writing — a model '
                      'that can see your actual schema is transformed; a model that can '
                      'alter it is a risk you took for very little extra.')
    y -= 12
    y = p.warn_box(MX, y, 'Whatever it reads ends up in a prompt', [
        'An MCP server that can query customer records will put customer records',
        'into requests. Know what your obligations are before you connect it, not',
        'after somebody asks.',
    ])
    y -= 12
    p.tip_box(MX, y, 'The schema server is the one to try first', [
        'Read-only, no sensitive data, and it removes the single most common class',
        'of wrong suggestion — columns and tables that do not exist.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Hooks — Making Something Certain')
    y = p.body(MX, y - 6,
               'Everything else in this volume is advisory. The model reads it and usually '
               'complies. A hook runs your own command at a point in the agent loop, and '
               'it runs whether the model agrees or not.')
    y -= 10
    y = p.table(MX, y, ['Instruction file', 'Hook'], [
        ('"Always format after editing"', 'Formatter runs after every edit'),
        ('Usually followed', 'Always executed'),
        ('Costs tokens', 'Costs nothing'),
        ('Model decides', 'You decide'),
    ], [250, CW - 250])
    y -= 16
    y = p.subheading(MX, y, 'What hooks are for')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Formatting after every edit, so style never enters the conversation',
        'Running the linter and feeding failures back automatically',
        'Blocking edits to paths that must not change',
        'Logging what an agent did, for audit',
    ], step=22)
    y -= 6
    y = p.tip_box(MX, y, 'The rule from the Claude series applies here too', [
        'If it is genuinely critical, do not ask the model — enforce it with a hook.',
        'Instructions persuade; hooks guarantee.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THEY ALSO SAVE TOKENS', [
        'Every rule you move from the instruction file into a hook is a rule you',
        'stop paying for on every request. "Always run the formatter" costs nothing',
        'as a hook and costs a line of context forever as an instruction.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Instructions or a Hook?')
    y = p.body(MX, y - 6,
               'The question is what happens on the day the model ignores you.')
    y -= 10
    y = p.table(MX, y, ['If ignoring it means', 'Use'], [
        ('Slightly untidy code', 'Instruction file'),
        ('An inconsistent style', 'Instruction file — or a formatter hook'),
        ('A failing build', 'Hook'),
        ('A secret in the repository', 'Hook'),
        ('A production incident', 'Hook, and a review gate'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'MOST THINGS ARE INSTRUCTIONS', [
        'Hooks are for the small number of rules where "usually" is not good enough.',
        'A repository with fifteen hooks is one where somebody tried to make the',
        'model deterministic — that is not what it is, and the result is slow, brittle',
        'and no more correct than a shorter list of well-chosen ones.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Hooks run on your machine', [
        'Everything a hook does happens with your permissions. Read one before you',
        'install it from anywhere you did not write yourself.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Start with exactly one', [
        'The formatter. It is uncontroversial, it removes an entire category of',
        'discussion with the model, and it fails visibly if you get it wrong —',
        'which makes it the right place to learn how hooks behave.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Working Setup')
    y = p.body(MX, y - 6,
               'What a well-configured repository actually looks like, once the novelty '
               'has worn off and only the useful parts survive.')
    y -= 10
    y = p.step_card(MX, y, 1, 'One always-on instruction file', [
        'Twenty to forty lines. Stack, commands, conventions, boundaries.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Two or three prompt files', [
        'The tasks the team genuinely repeats.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'One read-only planner agent', [
        'For thinking about a change before making it.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'One formatting hook', [
        'So style never has to be discussed with a model again.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Maybe one read-only MCP server', [
        'The schema, or the issue tracker. Rarely both on day one.',
    ])
    y -= 10
    p.info_panel(MX, y, 'THAT IS THE WHOLE THING', [
        'Five files and a server. Everything else in this volume exists for teams',
        'with a specific problem the basics did not solve.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 5 — ROLLING OUT

def ch5(v):
    lbl = 'Chapter 5  ·  Rolling It Out'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Agent Plugins')
    y = p.body(MX, y - 6,
               'A plugin is a ready-made bundle of everything in this volume — skills, '
               'tools, hooks and MCP servers — installed from a marketplace through the '
               'Extensions view. It is in preview.')
    y -= 10
    y = p.table(MX, y, ['Good for', 'Careful about'], [
        ('Adopting a proven workflow', 'You inherit rules you did not write'),
        ('A stack someone else configured', 'Hooks in it run on your machine'),
        ('Trying an approach quickly', 'MCP servers in it get real access'),
    ], [230, CW - 230])
    y -= 16
    y = p.warn_box(MX, y, 'Read a plugin before installing it', [
        'A plugin can contain hooks that execute commands and MCP servers that reach',
        'external systems. That is exactly the same trust decision as installing any',
        'other extension, and the same care applies.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Build yours before you install someone else\'s', [
        'Writing your own instruction file first teaches you what a plugin is doing',
        'and whether you actually want it. Otherwise you are adopting conventions',
        'you cannot evaluate.',
    ])
    y -= 12
    p.info_panel(MX, y, 'IT IS IN PREVIEW', [
        'Which means the format, the marketplace and the behaviour can all change.',
        'Fine for experimenting; think twice before making your team depend on one',
        'for something they cannot work without.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Getting a Team To Use It')
    y = p.body(MX, y - 6,
               'Customisation only pays off if the files are shared, current and trusted. '
               'That is a team problem more than a technical one.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Commit everything', [
        'Instruction, prompt and agent files are repository configuration.',
        'A file on one laptop helps one person.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Review changes to them', [
        'They change every future suggestion. Treat a diff to the instruction',
        'file with the seriousness of a diff to the linter config.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Update them with the convention', [
        'Change the convention and the instruction file in the same PR, or the',
        'file quietly starts lying.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Delete what is stale', [
        'A rule nobody follows any more is actively harmful — it is applied',
        'silently on every request.',
    ])
    y -= 10
    p.info_panel(MX, y, 'THE HONEST FAILURE MODE', [
        'Most teams write an instructions file once, never revisit it, and eighteen',
        'months later it describes a codebase that no longer exists. It is still',
        'being applied to every request. Put it on whatever cadence you already use',
        'for dependency updates.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['File', 'Location', 'What it is'], [
        ('copilot-instructions.md', '.github/', 'Always-on rules'),
        ('*.instructions.md', '.github/instructions/', 'Rules by glob'),
        ('AGENTS.md', 'Repo root', 'Always-on, portable'),
        ('CLAUDE.md', 'Root or .claude/', 'Also read by Copilot'),
        ('*.prompt.md', '.github/prompts/', 'A slash command'),
        ('*.agent.md', '.github/agents/', 'A role with set tools'),
        ('SKILL.md', 'Skill folder', 'A self-loading capability'),
    ], [160, 160, CW - 320])
    y -= 14
    y = p.table(MX, y, ['Command', 'Does'], [
        ('/init', 'Draft an instructions file from the codebase'),
        ('/instructions  /prompts', 'Manage those files'),
        ('/agents  /skills  /hooks', 'Manage those'),
        ('/create-instruction', 'Turn this conversation into a file'),
        ('/create-prompt  /create-agent', 'Same, for those types'),
    ], [200, CW - 200])
    y -= 14
    p.info_panel(MX, y, 'PRECEDENCE', [
        'Personal  >  Repository  >  Organization.  All are provided; the higher',
        'one wins a conflict.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('Instructions seem ignored', 'Too long or too vague — cut to specifics'),
        ('Teammate gets different answers', 'Personal instructions outrank the repo'),
        ('Targeted file never applies', 'Check applyTo glob is relative to repo root'),
        ('Prompt file not in the / list', 'Wrong extension — must be *.prompt.md'),
        ('Skill never triggers', 'Description too vague — name concrete tasks'),
        ('Agent edits despite instructions', 'Restrict its tools instead of asking'),
        ('Rules contradict each other', 'Two always-on files — consolidate to one'),
        ('Everything got slower', 'Instruction file too long; it is sent every turn'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 5 — Credits, Cost & Teams: budgets and overage, what actually',
        'consumes credits at scale, and administering Copilot across an organisation.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'If you do one thing', [
        'Write .github/copilot-instructions.md. Twenty lines. Commit it. That single',
        'file delivers more of the value in this volume than everything else in it',
        'put together.',
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
               title='Customisation',
               subtitle='Stop re-explaining your conventions on every request',
               badge='VOLUME FOUR',
               tagline='INSTRUCTIONS  ·  PROMPTS  ·  AGENTS  ·  SKILLS  ·  MCP  ·  HOOKS')

    total = 2 + 5 + 5 + 5 + 5 + 4
    v.cover(
        stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('7', 'FILE TYPES'),
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
