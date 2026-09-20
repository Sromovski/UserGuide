#!/usr/bin/env python3
"""Codex Field Guide — Volume 3: AGENTS.md, Subagents & MCP.

    python build_codex_v3.py

FACTS VERIFIED 2026-08-02 against learn.chatgpt.com/docs.
AGENTS.md: plain markdown, no required schema or frontmatter; hierarchical from
~/.codex/AGENTS.md down to nested project files; the CLOSEST file to the work takes
precedence and an explicit prompt overrides everything; /init drafts one.
Subagents: standalone TOML in ~/.codex/agents/ (personal) or .codex/agents/ (project);
required fields name / description / developer_instructions; optional model,
model_reasoning_effort, sandbox_mode, mcp_servers, skills.config. They run in parallel to
keep noisy work off the main thread, are USER-TRIGGERED (Codex does not spawn them by
itself at most levels), and INHERIT the parent's sandbox policy and permission mode.
MCP: `codex mcp` adds local or remote servers and inspects available tools.
"""
import os

from fieldguide import CODEX, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Codex_Field_Guide_Volume_3_AGENTS_Subagents_MCP.pdf')

CHAPTERS = [
    (1, 'AGENTS.md', 'The file that stops you repeating yourself', 3),
    (2, 'Writing a Good One', 'What earns its place, and what is dead weight', 8),
    (3, 'Subagents', 'Parallel work, and keeping the main thread clean', 13),
    (4, 'MCP Servers', 'Giving Codex your own tools and data', 18),
    (5, 'Putting It Together', 'A working setup, and what to adopt first', 23),
]


def ch1(v):
    lbl = 'Chapter 1  ·  AGENTS.md'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Say It Once')
    y = p.body(MX, y - 6,
               'AGENTS.md is a plain markdown file in your repository that tells Codex how '
               'this project works. Where a README explains the project to people, '
               'AGENTS.md explains it to an agent.')
    y -= 10
    y = p.info_panel(MX, y, 'DELIBERATELY MINIMAL', [
        'No required schema. No YAML frontmatter. No special syntax. It is markdown',
        'with headings and bullets, and that is the whole format.',
    ])
    y -= 12
    y = p.step_card(MX, y, 1, 'Create it', [
        'Run /init inside Codex and it drafts one from your codebase.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Cut it down', [
        'The generated draft will be too long. Chapter 2 is about what to keep.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Commit it', [
        'It is project configuration. Everyone on the team gets it automatically.',
    ])
    y -= 10
    p.tip_box(MX, y, 'It is a shared convention, not a Codex one', [
        'Other agents read AGENTS.md too. A repository with a good one is configured',
        'for more than one assistant — which matters if your team is not unanimous',
        'about tooling.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Hierarchy')
    y = p.body(MX, y - 6,
               'Codex reads AGENTS.md hierarchically — from your personal file down to '
               'nested files inside the project.')
    y -= 10
    y = p.code_block(MX, y, [
        '~/.codex/AGENTS.md            # personal, every project you work on',
        '',
        'my-repo/',
        '  AGENTS.md                   # the whole project',
        '  services/',
        '    AGENTS.md                 # just this service',
        '  frontend/',
        '    AGENTS.md                 # different stack, different rules',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THE CLOSEST FILE WINS', [
        'The AGENTS.md nearest the work being done takes precedence. And an explicit',
        'instruction in your prompt overrides all of them — which is what you want,',
        'because sometimes this task really is the exception.',
    ])
    y -= 12
    y = p.table(MX, y, ['Level', 'Put here'], [
        ('~/.codex/AGENTS.md', 'How YOU like to be worked with'),
        ('Repository root', 'How the PROJECT works'),
        ('Subdirectory', 'Where one area genuinely differs'),
    ], [190, CW - 190])
    y -= 14
    p.warn_box(MX, y, 'Nested files are for real differences', [
        'A monorepo with a Python service and a TypeScript frontend earns two files.',
        'Three files saying slightly different versions of the same thing does not',
        'help anybody, and the closest-wins rule makes the conflict silent.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Changes Immediately')
    y = p.body(MX, y - 6,
               'The effect is not dramatic on any single request. It is that a whole '
               'category of small friction stops happening.')
    y -= 10
    y = p.table(MX, y, ['Without it', 'With it'], [
        ('Suggests the framework you dropped', 'Uses the one you actually use'),
        ('Guesses how to run the tests', 'Runs them, unprompted'),
        ('Invents a folder layout', 'Follows yours'),
        ('You restate conventions every task', 'You describe only this job'),
        ('New joiners re-explain everything', 'The file does it'),
    ], [240, CW - 240])
    y -= 16
    y = p.info_panel(MX, y, 'THE HIGHEST-LEVERAGE LINE IN THE FILE', [
        'The build, test and lint commands. If they are listed, Codex will run them',
        'without being asked — which turns "it thinks it is done" into "the tests',
        'pass". Make them copy-pasteable, exactly as you would type them.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'That one section is worth writing the file for', [
        'If you do nothing else, list the exact commands to install, build, test and',
        'lint. Everything else in this volume is a smaller win than that.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHY IT MATTERS SO MUCH MORE THAN THE REST', [
        'An agent that cannot run your tests cannot check its own work, so it stops',
        'at plausible and tells you it is done. One that can, iterates until the',
        'suite is green. That is the difference between a suggestion and a result,',
        'and it costs you four lines.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Minimal Example')
    y -= 6
    y = p.code_block(MX, y, [
        '# AGENTS.md',
        '',
        '## Project',
        'Order processing service. Python 3.12, FastAPI, PostgreSQL.',
        '',
        '## Commands',
        '  install   uv sync',
        '  test      pytest',
        '  lint      ruff check .',
        '  types     mypy services/',
        '',
        '## Conventions',
        '- Type hints on every public function.',
        '- Specific exceptions, never bare except.',
        '- Tests use pytest, arrange-act-assert. No unittest.',
        '- Money is Decimal, never float.',
        '',
        '## Boundaries',
        '- Never edit anything under generated/ or migrations/.',
        '- Do not add dependencies without saying so explicitly.',
    ])
    y -= 12
    p.info_panel(MX, y, 'TWENTY LINES IS PLENTY', [
        'That file would meaningfully improve most sessions in that repository, and',
        'it took five minutes. Length is not the goal — being true is.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Keeping It True')
    y = p.body(MX, y - 6,
               'The failure mode is not writing a bad file. It is writing a good one and '
               'never touching it again.')
    y -= 10
    y = p.warn_box(MX, y, 'A stale AGENTS.md is worse than none', [
        'It is applied silently on every request. A file describing the framework you',
        'migrated away from eighteen months ago is actively steering the agent wrong,',
        'and it is the last place anyone thinks to look.',
    ])
    y -= 12
    y = p.step_card(MX, y, 1, 'Change it in the same PR as the convention', [
        'Or it starts lying immediately.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Review changes to it properly', [
        'It shapes every future suggestion. Treat a diff to it like a diff to',
        'the linter config, not like a docs tweak.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Delete rules nobody follows', [
        'An aspiration in this file is a lie the agent believes.',
    ])
    y -= 8
    p.tip_box(MX, y, 'Put it on the same cadence as dependency updates', [
        'Whatever rhythm you already have for keeping things current — this belongs',
        'in it. Nobody remembers to review a file that never breaks anything loudly.',
    ])
    v.close()


def ch2(v):
    lbl = 'Chapter 2  ·  Writing a Good One'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Earns Its Place')
    y -= 6
    y = p.table(MX, y, ['Section', 'Why it pays'], [
        ('Project snapshot', 'One to three sentences of orientation'),
        ('Setup commands', 'Exact strings — uv sync, pnpm install'),
        ('Build / test / lint', 'THE highest-leverage section'),
        ('Conventions', 'What a newcomer would get wrong'),
        ('Boundaries', 'Directories and files to leave alone'),
        ('Decisions made', 'So it stops re-proposing the alternative'),
    ], [180, CW - 180])
    y -= 16
    y = p.subheading(MX, y, 'Make the commands copy-pasteable')
    y -= 4
    y = p.body(MX, y, 'Write the literal string you would type. "Run the tests with '
                      'pytest" is worse than "pytest -q". The agent will execute what you '
                      'wrote, and a command that needs interpreting is a command it might '
                      'interpret wrongly.')
    y -= 8
    y = p.info_panel(MX, y, 'IF IT IS NOT LISTED, IT WILL NOT RUN', [
        'An agent that does not know how to run your tests cannot verify its own',
        'work — so it stops at plausible. Listing the command is the difference',
        'between a guess and a checked answer.',
    ])
    y -= 12
    p.code_block(MX, y, [
        '## Commands',
        '  install   uv sync',
        '  test      pytest -q',
        '  lint      ruff check .',
        '  types     mypy services/',
        '',
        '# Literal strings. Not "run the tests with pytest".',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Specific Beats Comprehensive')
    y -= 6
    y = p.table(MX, y, ['Write this', 'Not this'], [
        ('"pytest -q, from the repo root"', '"Write good tests"'),
        ('"Raise specific exceptions"', '"Handle errors properly"'),
        ('"Money is Decimal, never float"', '"Be careful with numbers"'),
        ('"Never edit generated/"', '"Be careful with generated code"'),
        ('"snake_case functions"', '"Follow naming conventions"'),
        ('"Prefer composition"', '"Write clean code"'),
    ], [240, CW - 240])
    y -= 16
    y = p.warn_box(MX, y, 'Every line is sent on every request', [
        'This file is context. A thousand lines of aspiration is paid for on every',
        'single turn, forever, and dilutes the lines that actually matter. Keep only',
        'what visibly changes the output.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'The test for a line', [
        'Would the agent get this wrong without it? If not, delete it. "Uses Python"',
        'is not earning its place in a repository full of .py files.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE DECISIONS SECTION IS UNDERRATED', [
        'A line saying "we evaluated X and chose Y, do not re-propose X" saves the',
        'same argument every few weeks. Agents are relentlessly helpful about',
        'suggesting the alternative you already rejected, and they have no memory',
        'of the meeting where you rejected it.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What To Leave Out')
    y -= 6
    y = p.table(MX, y, ['Do not include', 'Because'], [
        ('Anything obvious from the code', 'It can already see the code'),
        ('Long architectural essays', 'It needs rules, not history'),
        ('Aspirations nobody follows', 'It will follow them and confuse everyone'),
        ('Onboarding prose for humans', 'That is what the README is for'),
        ('Secrets, keys, internal URLs', 'It goes into requests'),
    ], [230, CW - 230])
    y -= 16
    y = p.warn_box(MX, y, 'Nothing sensitive in this file', [
        'It is prepended to requests. Treat it exactly as you would treat something',
        'you were about to paste into a chat window — because that is what it is.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THE README TEST', [
        'If a new human colleague would want to read it, it is README material.',
        'If only a machine about to edit the code needs it, it is AGENTS.md.',
        'The two documents overlap far less than people expect.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Do not link the README from it either', [
        'It will not follow the link the way you imagine, and you have spent a line',
        'saying so. Put the fact in the file, or leave it out.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Monorepos')
    y = p.body(MX, y - 6,
               'Where the hierarchy earns its keep: one root file for what is true '
               'everywhere, and nested files where a package genuinely differs.')
    y -= 10
    y = p.code_block(MX, y, [
        'monorepo/',
        '  AGENTS.md                 # shared: git conventions, PR rules, boundaries',
        '  packages/',
        '    api/',
        '      AGENTS.md             # Python, pytest, ruff',
        '    web/',
        '      AGENTS.md             # TypeScript, vitest, biome',
        '    shared/',
        '      AGENTS.md             # published package — breaking changes matter',
    ])
    y -= 12
    y = p.table(MX, y, ['Put in the root', 'Put in the package'], [
        ('Commit and PR conventions', 'Language and framework'),
        ('Directories nobody may touch', 'Test and lint commands'),
        ('Cross-cutting rules', 'Package-specific gotchas'),
    ], [250, CW - 250])
    y -= 14
    y = p.tip_box(MX, y, 'Do not repeat the root file in every package', [
        'The hierarchy composes. Duplication is how the files drift apart, and the',
        'closest-wins rule means the drift is silent.',
    ])
    y -= 12
    p.warn_box(MX, y, 'A nested file is a commitment', [
        'Every AGENTS.md is another file that has to stay true. In a monorepo with',
        'twelve packages, twelve instruction files is eleven more than most teams',
        'will maintain. Add one where the stack genuinely differs — not per package.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Checklist')
    y -= 6
    y = p.bullets(MX + 4, y, [
        'Can someone run the tests using only what is written here?',
        'Are the commands literal strings, not descriptions?',
        'Is every convention something the agent would get wrong without it?',
        'Are the off-limits directories named explicitly?',
        'Is anything in here no longer true?',
        'Is it under about forty lines?',
        'Is there anything sensitive in it?',
    ], step=24)
    y -= 8
    y = p.info_panel(MX, y, 'IF YOU ANSWER THOSE HONESTLY', [
        'You will end up with a shorter file than the one /init generated, and it',
        'will work better. Almost every AGENTS.md improvement is a deletion.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Then stop', [
        'Chapters 3 and 4 exist for specific problems. If AGENTS.md solved yours,',
        'you are done — subagents and MCP are not a natural next step, they are',
        'answers to questions you may not have.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE HONEST SPLIT', [
        'AGENTS.md delivers most of the value in this volume for most repositories,',
        'and it is the cheapest of the three to write and to maintain. If you read',
        'only two chapters of this book, read the two you just finished.',
    ])
    v.close()


def ch3(v):
    lbl = 'Chapter 3  ·  Subagents'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What They Are For')
    y = p.body(MX, y - 6,
               'Subagents are specialised agents that run in parallel on independent work. '
               'The reason they exist is less obvious than the parallelism: they keep '
               'noisy intermediate work off the main thread.')
    y -= 10
    y = p.info_panel(MX, y, 'CONTEXT POLLUTION IS THE REAL PROBLEM', [
        'Exploring a codebase, running tests and reading output fills the main',
        'conversation with detail that stops being useful the moment it is consumed.',
        'Pushing that into a subagent lets the primary agent stay focused on the',
        'requirements and the decisions, which is what it is actually good at.',
    ])
    y -= 12
    y = p.table(MX, y, ['Good subagent work', 'Why'], [
        ('Exploring unfamiliar code', 'Lots of reading, one conclusion'),
        ('Running and interpreting tests', 'Noisy output, small answer'),
        ('Analysing several options', 'Genuinely parallel'),
        ('Independent investigations', 'They do not need each other'),
    ], [220, CW - 220])
    y -= 14
    y = p.warn_box(MX, y, 'Not for splitting one edit across agents', [
        'Parallel agents editing the same area produce conflicts and confusion.',
        'Parallelise investigation, not modification.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE SHAPE THAT WORKS', [
        'Many agents reading, one agent writing. Send the exploration out in',
        'parallel, bring back conclusions rather than transcripts, and let the main',
        'thread make the decision and the change. That keeps the expensive context',
        'clean and the edits coherent.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'You Trigger Them')
    y = p.body(MX, y - 6,
               'This is the thing people get wrong: Codex does not spawn subagents by '
               'itself at most intelligence levels. You ask for delegation, or your '
               'AGENTS.md or a skill asks for it.')
    y -= 10
    y = p.table(MX, y, ['Triggered by', 'Looks like'], [
        ('An explicit request', '"Spawn one agent per option and compare"'),
        ('AGENTS.md instructions', 'The file tells it when to delegate'),
        ('Skill instructions', 'A skill that requests delegation'),
        ('Proactive (Ultra only)', 'It delegates suitable work by itself'),
    ], [200, CW - 200])
    y -= 16
    y = p.code_block(MX, y, [
        '# Explicit delegation, in a prompt',
        'Investigate three approaches to caching this endpoint. Spawn one',
        'subagent per approach. Each should report the trade-offs and a',
        'rough implementation sketch. Do not change any code.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Which makes them predictable', [
        'Nothing happens behind your back. If you did not ask for parallel work and',
        'nothing in your configuration asked for it, you are running one agent.',
    ])
    y -= 12
    p.warn_box(MX, y, 'And it means nothing happens if you never ask', [
        'People install subagents, never phrase a request that triggers one, and',
        'conclude the feature does nothing. If you want parallel work, say so —',
        'or put the instruction to delegate into AGENTS.md so it is automatic.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Defining One')
    y = p.body(MX, y - 6,
               'Custom agents are standalone TOML files. Personal ones live in '
               '~/.codex/agents/, project ones in .codex/agents/ so they can be committed '
               'and shared.')
    y -= 10
    y = p.code_block(MX, y, [
        '# .codex/agents/explorer.toml',
        '',
        'name = "explorer"',
        'description = "Read-only investigation of unfamiliar code. Never edits."',
        'developer_instructions = """',
        'You investigate and report. You never modify files.',
        'Answer with: what you found, where it lives, and what surprised you.',
        'If the question is ambiguous, say so rather than guessing.',
        '"""',
        '',
        'model = "gpt-5.6"',
        'model_reasoning_effort = "low"',
        'sandbox_mode = "read-only"',
    ])
    y -= 12
    y = p.table(MX, y, ['Field', 'Required?'], [
        ('name', 'Yes — the identifier'),
        ('description', 'Yes — guidance on when to use it'),
        ('developer_instructions', 'Yes — the core behaviour'),
        ('model, model_reasoning_effort', 'Optional overrides'),
        ('sandbox_mode, mcp_servers', 'Optional'),
    ], [230, CW - 230])
    y -= 14
    p.tip_box(MX, y, 'The description is what makes it usable', [
        'It is guidance on WHEN to use this agent. Vague descriptions produce agents',
        'nobody reaches for, including the primary agent deciding what to delegate.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Effort and Model per Agent')
    y = p.body(MX, y - 6,
               'A subagent can set its own model and reasoning effort — which is how you '
               'stop paying for deep reasoning on shallow work.')
    y -= 10
    y = p.table(MX, y, ['Agent', 'Sensible setting'], [
        ('Explorer / reader', 'Low effort, small model'),
        ('Test runner', 'Low effort'),
        ('Option analyser', 'Medium to high — it is genuinely thinking'),
        ('Reviewer', 'Medium'),
        ('Implementer', 'Match the difficulty of the code'),
    ], [200, CW - 200])
    y -= 16
    y = p.info_panel(MX, y, 'HOW SETTINGS RESOLVE', [
        'A value in the agent file wins. Otherwise Codex resolves each setting',
        'independently — an explicit spawn value first, then the [agents] default,',
        'then the parent\'s value. So an unset field inherits rather than resetting.',
    ])
    y -= 12
    p.tip_box(MX, y, 'This is the cheapest optimisation available', [
        'Most delegated work is reading and reporting. Setting those agents to low',
        'effort costs nothing in quality and noticeably less in consumption.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Security')
    y = p.body(MX, y - 6,
               'Subagents inherit the parent\'s sandbox policy and permission mode, and '
               'Codex reapplies the parent turn\'s live runtime overrides when it spawns '
               'a child. Delegation does not quietly widen what is allowed.')
    y -= 10
    y = p.info_panel(MX, y, 'THAT IS THE GUARANTEE THAT MATTERS', [
        'A subagent cannot escape the constraints you set on the parent. Delegation',
        'moves work off the main thread; it does not move it outside the sandbox.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'But put hard constraints in BOTH places', [
        'If a subagent must obey something — no PII in logs, never git push --force —',
        'state it in the parent\'s AGENTS.md AND in the subagent\'s own instructions.',
        'Belt and braces, because a constraint that exists in only one of them is a',
        'constraint that depends on inheritance working the way you assumed.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Read-only subagents are the safe default', [
        'Most delegation is investigation. An agent with sandbox_mode read-only',
        'cannot damage anything, which makes it the right shape for the majority',
        'of the work you would want to parallelise.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE PRINCIPLE, ONCE MORE', [
        'Narrow the role, narrow the tools, narrow the sandbox. Three cheap',
        'constraints, and together they mean you can reason about what a subagent',
        'is capable of rather than hoping about what it will choose to do.',
    ])
    v.close()


def ch4(v):
    lbl = 'Chapter 4  ·  MCP Servers'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Giving It Your Own Tools')
    y = p.body(MX, y - 6,
               'AGENTS.md changes what Codex knows. MCP servers change what it can reach '
               '— your database, your ticket system, your internal services.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Add, authenticate and inspect servers',
        'codex mcp',
        '',
        '# It handles local servers and remote ones, prompts for auth where',
        '# needed, and shows the tools available to the current session.',
    ])
    y -= 12
    y = p.table(MX, y, ['Connect', 'So it can'], [
        ('A database, read-only', 'Read the real schema instead of inventing columns'),
        ('Your issue tracker', 'See the requirement, not your paraphrase of it'),
        ('Internal docs', 'Follow your conventions, not generic ones'),
        ('Observability', 'Look at the actual error it is fixing'),
    ], [200, CW - 200])
    y -= 14
    y = p.warn_box(MX, y, 'An MCP server is a permission grant', [
        'You are giving a model the ability to query real systems. Be as deliberate',
        'about it as you would be issuing credentials to a contractor — because in',
        'every meaningful sense that is what you are doing.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE CATEGORY CHANGE', [
        'AGENTS.md and subagents both shape behaviour inside your repository. MCP is',
        'the first thing in this volume that lets Codex touch something outside it.',
        'That is not another feature on the list — it is a different kind of',
        'decision, and it deserves a different level of thought.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Is Worth Connecting')
    y -= 6
    y = p.table(MX, y, ['High value', 'Why'], [
        ('Read-only schema', 'Kills a whole class of invented columns'),
        ('Issue tracker, read-only', 'It reads the ticket itself'),
        ('Component library', 'Stops it inventing components'),
        ('Log or error search', 'Debugging with evidence, not guesses'),
    ], [210, CW - 210])
    y -= 14
    y = p.table(MX, y, ['Think much harder about', 'Why'], [
        ('Write access to anything', 'Blast radius leaves your repository'),
        ('Production systems', 'A confident wrong query is still a query'),
        ('Customer data', 'It ends up in requests — know your obligations'),
    ], [210, CW - 210])
    y -= 14
    y = p.info_panel(MX, y, 'THE PATTERN THAT WORKS', [
        'Read-only, non-production, one system at a time, two weeks apart. Nearly',
        'all the value is in reading — a model that can see your real schema is',
        'transformed. A model that can alter it is a risk taken for very little.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Start with the schema server', [
        'Read-only, no sensitive data, and it removes the single most common wrong',
        'suggestion: columns and tables that do not exist.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'MCP and Subagents Together')
    y = p.body(MX, y - 6,
               'A subagent definition can specify its own mcp_servers, which is more '
               'useful than it first sounds: it lets you give a narrow tool to a narrow '
               'agent rather than to everything.')
    y -= 10
    y = p.code_block(MX, y, [
        '# .codex/agents/schema-checker.toml',
        '',
        'name = "schema-checker"',
        'description = "Answers questions about the live database schema."',
        'developer_instructions = """',
        'You answer questions about the database schema using the connected',
        'server. You never write SQL that modifies data, and you never edit files.',
        '"""',
        'sandbox_mode = "read-only"',
        'mcp_servers = ["postgres-readonly"]',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'SCOPING TOOLS TO ROLES', [
        'The main agent does not need database access to write a function. The',
        'agent answering schema questions does. Separating them means the tool is',
        'available where it is needed and absent everywhere else — which is a much',
        'better default than granting it globally and hoping.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Same idea as read-only subagents', [
        'Narrow the role, narrow the tools, narrow the sandbox. Three cheap',
        'constraints that compose into something you can actually reason about.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Before You Connect Anything')
    y -= 6
    y = p.step_card(MX, y, 1, 'Ask what it can reach', [
        'Not what you intend to use it for. What it CAN do if asked.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Prefer a read-only credential', [
        'If the server supports one, use it. Most of the value is in reading.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Point it at non-production', [
        'A staging schema teaches it the same shape with none of the risk.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Know what data will end up in requests', [
        'Whatever it reads becomes context. That is a compliance question in',
        'some organisations, not a technical one.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Add one, then wait', [
        'Two weeks with each before adding the next.',
    ])
    y -= 8
    p.warn_box(MX, y, 'Third-party servers run code you did not write', [
        'The same trust decision as any dependency, with more access. Read what you',
        'are installing.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing Between the Three')
    y = p.body(MX, y - 6,
               'AGENTS.md, subagents and MCP solve different problems. Reaching for the '
               'wrong one is the commonest mistake in this volume.')
    y -= 10
    y = p.table(MX, y, ['You want', 'Use'], [
        ('It to follow your conventions', 'AGENTS.md'),
        ('It to know how to run your tests', 'AGENTS.md'),
        ('Noisy exploration off the main thread', 'A subagent'),
        ('Several options investigated at once', 'Subagents'),
        ('A role that cannot edit files', 'A subagent with read-only sandbox'),
        ('It to see real data', 'An MCP server'),
        ('A tool only one role should have', 'MCP scoped to that subagent'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'IN ORDER OF WHAT MOST PEOPLE NEED', [
        'AGENTS.md — nearly everyone, immediately.  Subagents — when sessions get',
        'noisy or work is genuinely parallel.  MCP — when the agent is guessing at',
        'something a system could tell it. Most repositories never need the third.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Adopt because something hurts', [
        'Each of these is a file somebody has to keep true. Configuration adopted',
        'because it exists, rather than because it solved a problem, becomes stale',
        'configuration nobody understands.',
    ])
    v.close()


def ch5(v):
    lbl = 'Chapter 5  ·  Putting It Together'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Working Setup')
    y = p.body(MX, y - 6,
               'What a well-configured repository actually looks like once the novelty '
               'has worn off and only the useful parts survive.')
    y -= 10
    y = p.code_block(MX, y, [
        'my-repo/',
        '  AGENTS.md                       # ~25 lines. Commands, conventions,',
        '                                  # boundaries. The load-bearing file.',
        '  .codex/',
        '    agents/',
        '      explorer.toml               # read-only investigation, low effort',
        '      reviewer.toml               # critique a diff, medium effort',
        '    tasks/',
        '      weekly-tidy.md              # a task file for codex exec',
        '',
        '~/.codex/',
        '  AGENTS.md                       # how YOU like to be worked with',
        '  agents/                         # your personal agents, every project',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THAT IS THE WHOLE THING', [
        'One instruction file, two subagents, a task file. No MCP server until',
        'something in this repository is genuinely being guessed at. Most teams',
        'never need more than this, and the ones that add more rarely maintain it.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Commit all of it', [
        'These files are how your team works, in a form a machine reads. They belong',
        'in version control and in review.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What To Adopt, In Order')
    y -= 6
    y = p.step_card(MX, y, 1, 'Week one — AGENTS.md', [
        '/init, cut it down hard, commit. Twenty lines. Get the commands right.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Week two — live with it', [
        'Notice what it still gets wrong. Those are your missing lines.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'When sessions get noisy — a read-only explorer', [
        'The first subagent worth having, and it cannot break anything.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'When it guesses at real data — one MCP server', [
        'Read-only, non-production. Usually the schema.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Review the lot quarterly', [
        'Delete what is no longer true. Most improvements are deletions.',
    ])
    y -= 8
    p.warn_box(MX, y, 'Do not do all of this in week one', [
        'A repository that arrives with three subagents, two MCP servers and a',
        'forty-line instruction file, none of which anyone has needed yet, is',
        'configuration nobody understands and nobody will maintain.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['File', 'Where', 'What'], [
        ('AGENTS.md', 'Repo root', 'Always-on project rules'),
        ('AGENTS.md', 'Subdirectory', 'Overrides, closest wins'),
        ('AGENTS.md', '~/.codex/', 'Your personal preferences'),
        ('*.toml', '.codex/agents/', 'Project subagents'),
        ('*.toml', '~/.codex/agents/', 'Personal subagents'),
    ], [110, 150, CW - 260])
    y -= 14
    y = p.table(MX, y, ['Subagent field', 'Notes'], [
        ('name', 'Required'),
        ('description', 'Required — when to use it'),
        ('developer_instructions', 'Required — how it behaves'),
        ('model / model_reasoning_effort', 'Optional; unset inherits'),
        ('sandbox_mode / mcp_servers', 'Optional; narrow both'),
    ], [230, CW - 230])
    y -= 14
    p.info_panel(MX, y, 'THE RULES THAT MATTER', [
        'Closest AGENTS.md wins; an explicit prompt overrides all of them.',
        'Subagents are user-triggered and inherit the parent sandbox and permissions.',
        'Hard constraints go in the parent AGENTS.md AND the subagent instructions.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('AGENTS.md seems ignored', 'Too long or too vague — cut to specifics'),
        ('Wrong rules applied', 'A nested file is closer to the work'),
        ('It will not run the tests', 'The command is not listed, or not literal'),
        ('Never delegates', 'Subagents are user-triggered — ask explicitly'),
        ('Subagent edited files', 'Set sandbox_mode read-only in its TOML'),
        ('Subagent ignored a constraint', 'Put it in BOTH parent and subagent'),
        ('MCP tools not available', 'codex mcp — check it is added and authed'),
        ('Costs went up after subagents', 'Set low effort on the reading agents'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 4 — Delegation, Review & Cost: cloud tasks, automated code review,',
        'and keeping the whole thing inside the usage window.',
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
               title='AGENTS.md, Subagents & MCP',
               subtitle='Stop repeating your conventions, and give Codex your tools',
               badge='VOLUME THREE',
               tagline='AGENTS.MD  ·  HIERARCHY  ·  SUBAGENTS  ·  MCP  ·  SETUP')
    total = 2 + 5 + 5 + 5 + 5 + 4
    v.cover(stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('3', 'MECHANISMS'),
                   ('2026', 'EDITION')],
            inside=[(n, t, b) for n, t, b, _ in CHAPTERS])
    v.contents([(n, t, b, s) for n, t, b, s in CHAPTERS])
    ch1(v); ch2(v); ch3(v); ch4(v); ch5(v)
    v.save()
    print('Saved: %s  (%d pages)' % (OUT, v.page_no))


if __name__ == '__main__':
    main()
