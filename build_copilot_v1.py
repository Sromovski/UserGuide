#!/usr/bin/env python3
"""Copilot Field Guide — Volume 1: Getting Started with GitHub Copilot.

    python build_copilot_v1.py

Written at volume scale (chapters inside one document), on the fieldguide/ engine.

FACTS VERIFIED 2026-08-02 against docs.github.com and github.com/features/copilot/plans.
Copilot moved to usage-based billing on 1 June 2026 and the numbers have shifted twice
this year — every price and credit figure lives in ONE table on ONE page (page 8) so a
reprint is a single edit. Do not scatter pricing through the prose.
"""
import os

from fieldguide import COPILOT, CW, H, MX, Painter, wrap
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Copilot_Field_Guide_Volume_1_Getting_Started.pdf')

CHAPTERS = [
    (1, 'What Copilot Actually Is', 'Autocomplete, chat and an agent — three different things', 3),
    (2, 'Plans, Credits & Cost', 'The June 2026 billing change, and what is still unmetered', 7),
    (3, 'Installing Copilot', 'VS Code, Visual Studio, JetBrains, Neovim and the CLI', 12),
    (4, 'Completions & Next Edit Suggestions', 'The part you use all day, and it costs nothing', 17),
    (5, 'Your First Hour', 'A guided run from install to first accepted change', 21),
]


# ══════════════════════════════════════════════════════ CH 1 — WHAT IT IS

def ch1(v):
    lbl = 'Chapter 1  ·  What Copilot Actually Is'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Three Products Wearing One Name')
    y = p.body(MX, y - 6,
               'Most confusion about Copilot comes from treating it as a single feature. '
               'It is three, they behave differently, and — critically — they are billed '
               'differently. Getting this straight now will save you money in chapter 2.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Code completions — the grey text', [
        'Suggests the rest of the line or block as you type. Press Tab to accept.',
        'Always on, works in the editor, no prompt required.',
        'UNMETERED on every paid plan. Use it as much as you like.',
    ])
    y -= 8
    y = p.step_card(MX, y, 2, 'Chat — you ask, it answers', [
        'A conversation panel that can see your file, selection or whole project.',
        'Good for "why does this fail", "write tests for this", "explain this regex".',
        'CONSUMES CREDITS on paid plans.',
    ])
    y -= 8
    y = p.step_card(MX, y, 3, 'Agent mode — you delegate, it works', [
        'Give it a goal. It plans, edits multiple files, runs commands, iterates.',
        'You review a set of changes rather than a single suggestion.',
        'CONSUMES CREDITS, and far faster than chat does.',
    ])
    y -= 10
    p.tip_box(MX, y, 'The one-sentence version', [
        'Completions are free and constant; chat and agent mode are metered and',
        'occasional. Almost every surprise bill comes from forgetting the second half.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What It Is Good At — And What It Is Not')
    y -= 6
    y = p.table(MX, y, ['Works well', 'Why'], [
        ('Boilerplate', 'It has seen ten thousand versions of this file'),
        ('Tests', 'Given a function, the shape of a test is predictable'),
        ('Unfamiliar syntax', 'Faster than searching for the right incantation'),
        ('Explaining code', 'Reading is easier for a model than writing'),
        ('Small refactors', 'Rename, extract, restructure within a file'),
    ], [150, CW - 150])
    y -= 16
    y = p.table(MX, y, ['Struggles with', 'Why'], [
        ('Your business rules', 'It cannot know what it was never told'),
        ('Novel algorithms', 'Pattern completion is not invention'),
        ('Large refactors', 'Context is finite; it loses the thread'),
        ('Anything unverifiable', 'Confident wrong answers look like right ones'),
    ], [150, CW - 150])
    y -= 16
    y = p.warn_box(MX, y, 'It is a suggestion engine, not an oracle', [
        'Copilot produces plausible code. Plausible is not the same as correct, and',
        'it is never the same as secure. Read every line before you accept it — you',
        'own the code once it is in your repository.',
    ])
    y -= 14
    p.info_panel(MX, y, 'WHICH OF THE THREE, WHEN', [
        'Completions  — you know what to write and want it typed faster.',
        'Chat         — you do not understand something, or want a second opinion.',
        'Agent mode   — the task is mechanical, spans files, and you can describe',
        '               exactly what "done" looks like.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Who This Volume Is For')
    y = p.body(MX, y - 6,
               'You write code, or you are learning to. You do not need to know anything '
               'about AI, and nothing here assumes you have used a coding assistant '
               'before. If you have a GitHub account and an editor, you are ready.')
    y -= 10
    y = p.info_panel(MX, y, 'BEFORE YOU START', [
        'A GitHub account — the free tier is enough to follow every chapter.',
        'An editor: VS Code, Visual Studio, a JetBrains IDE, or Neovim.',
        'Roughly an hour, if you follow chapter 5 end to end.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'What you will be able to do by the end')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Explain the difference between completions, chat and agent mode',
        'Predict what a month of your usage will cost before you are billed',
        'Install and sign in on your editor of choice',
        'Drive completions deliberately instead of waiting for grey text',
        'Know when to reach for chat and when to just write the code yourself',
    ], step=22)
    y -= 8
    y = p.tip_box(MX, y, 'Read chapter 2 even if you hate pricing', [
        'Copilot changed how it charges in June 2026. If your mental model predates',
        'that, it is wrong in a way that costs money rather than just being outdated.',
    ])
    y -= 14
    p.warn_box(MX, y, 'What this volume does not cover', [
        'Chat and agent mode in depth (Volume 2), the CLI and the cloud coding agent',
        '(Volume 3), instruction files and MCP (Volume 4), and team administration',
        '(Volume 5). This one gets you installed, oriented and not overspending.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'How Copilot Sees Your Code')
    y = p.body(MX, y - 6,
               'Copilot does not read your whole project on every keystroke. It assembles '
               'a limited window of context and sends that. Knowing what goes into the '
               'window is most of the skill of getting good suggestions.')
    y -= 10
    y = p.table(MX, y, ['Goes in the window', 'Notes'], [
        ('The current file', 'Always, and weighted most heavily'),
        ('Text near the cursor', 'The lines directly above matter most'),
        ('Other open tabs', 'Which is why closing junk tabs helps'),
        ('Imports and signatures', 'Type information sharpens suggestions a lot'),
        ('Instruction files', 'Repository rules — covered in Volume 4'),
    ], [170, CW - 170])
    y -= 16
    y = p.subheading(MX, y, 'Practical consequences')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'A descriptive function name produces a better body than a vague one',
        'Writing the comment first often produces the code you wanted',
        'Open the file you are mirroring — it becomes context',
        'Close unrelated tabs before a tricky suggestion',
    ], step=22)
    y -= 8
    p.info_panel(MX, y, 'PRIVACY, BRIEFLY', [
        'Code is sent to GitHub to generate suggestions. Business and Enterprise',
        'plans add content exclusion so you can keep named paths out entirely.',
        'If you work under a contract that forbids this, settle it before installing.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 2 — PLANS & COST

def ch2(v):
    lbl = 'Chapter 2  ·  Plans, Credits & Cost'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Changed on 1 June 2026')
    y = p.body(MX, y - 6,
               'Copilot used to bill a flat monthly fee with a "premium request" quota. '
               'It now bills on usage, against a pool of AI Credits included with your '
               'plan. The flat fee still exists — the quota it buys is now measured in '
               'credits rather than request counts.')
    y -= 10
    y = p.info_panel(MX, y, 'THE ONE NUMBER TO REMEMBER', [
        '1 AI Credit = $0.01 USD. So a plan including 1,500 credits includes $15',
        'of metered usage. Everything else is arithmetic from there.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'The split that matters')
    y -= 4
    y = p.table(MX, y, ['Feature', 'Billed?'], [
        ('Code completions', 'No — unmetered on every paid plan'),
        ('Next Edit Suggestions', 'No — unmetered on every paid plan'),
        ('Copilot Chat', 'Yes — draws on credits'),
        ('Agent mode', 'Yes — and fastest of all'),
        ('Copilot CLI', 'Yes'),
        ('Cloud agent / Spaces / Spark', 'Yes'),
        ('Code review', 'Yes'),
    ], [200, CW - 200])
    y -= 14
    p.tip_box(MX, y, 'This is genuinely good news', [
        'The feature you use every minute — inline autocomplete — costs nothing beyond',
        'the subscription. Only the things you invoke deliberately are metered.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Plans, Side by Side')
    y = p.body(MX, y - 6, 'Verified against GitHub\'s billing documentation, August 2026. '
                          'Prices move — check before committing a team.')
    y -= 8
    y = p.table(MX, y, ['Plan', 'Price', 'Base', 'Flex', 'Total credits'], [
        ('Free', '$0', '—', '—', '2,000 completions'),
        ('Pro', '$10/mo', '1,000', '500', '1,500  ($15)'),
        ('Pro+', '$39/mo', '3,900', '3,100', '7,000  ($70)'),
        ('Max', '$100/mo', '10,000', '10,000', '20,000  ($200)'),
    ], [90, 80, 70, 70, CW - 310])
    y -= 16
    y = p.info_panel(MX, y, 'THE FREE PLAN, PRECISELY', [
        '2,000 code completions per month, and 50 chat requests (Edits included).',
        'Enough to evaluate Copilot honestly. Not enough to rely on it daily.',
        'Verified students, teachers and popular open-source maintainers can get',
        'paid features at no cost — check eligibility before paying.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'What 1,500 credits actually buys')
    y -= 4
    y = p.body(MX, y, 'Credits track model usage, not button presses, so any figure is '
                      'a range rather than a promise. As a rough shape for a Pro month:')
    y -= 6
    y = p.table(MX, y, ['If your month looks like', 'Pro is'], [
        ('Completions all day, chat a few times a week', 'More than enough'),
        ('Daily chat, occasional small agent task', 'Comfortable'),
        ('Agent mode several times a day', 'Tight — price Pro+'),
        ('Agent mode on large codebases, big models', 'Not enough'),
    ], [280, CW - 280])
    y -= 14
    y = p.subheading(MX, y, 'Organisations')
    y -= 4
    y = p.body(MX, y, 'Business and Enterprise are per-seat and add the things a company '
                      'needs rather than more capability: policy control, content '
                      'exclusion, audit logs and centrally managed billing.')
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Actually Burns Credits')
    y = p.body(MX, y - 6,
               'Credits map to model usage, so cost tracks the size of the job, not the '
               'number of times you pressed a button. A one-line chat answer is cheap. '
               'An agent that reads forty files and rewrites six is not.')
    y -= 10
    y = p.table(MX, y, ['Action', 'Relative cost'], [
        ('Accepting completions all day', 'Zero'),
        ('A short chat question', 'Very low'),
        ('Chat over a whole large file', 'Low to moderate'),
        ('One focused agent task', 'Moderate'),
        ('An agent let loose on a vague goal', 'The expensive one'),
        ('Choosing a bigger model', 'Multiplies whatever the above cost'),
    ], [230, CW - 230])
    y -= 16
    y = p.subheading(MX, y, 'Four habits that keep the bill down')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Scope agent tasks narrowly — "fix this test", not "improve the codebase"',
        'Pick the smallest model that clears the bar for the job',
        'Let completions do the routine work; save chat for when you are stuck',
        'Set a budget before you need one, not after the first surprise',
    ], step=22)
    y -= 8
    y = p.warn_box(MX, y, 'Agent mode is where bills come from', [
        'A vague goal makes an agent explore, and exploration is billed. The single',
        'most effective cost control is a specific, checkable task description.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'The same task, priced two ways')
    y -= 4
    p.code_block(MX, y, [
        '# Expensive — open-ended, so it reads everything looking for work:',
        '"Clean up the error handling in this project."',
        '',
        '# Cheap — bounded, checkable, and it stops when it is done:',
        '"In api/orders.py, replace the bare except blocks with specific',
        ' exceptions. Do not change behaviour. Tests must still pass."',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When You Run Out')
    y = p.body(MX, y - 6,
               'Credits reset monthly. Running out does not disable Copilot — completions '
               'and Next Edit Suggestions keep working, because they were never metered. '
               'Only the credit-backed features pause.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Wait for the reset', [
        'Free, and often the right answer if the month is nearly over.',
        'Completions keep working throughout.',
    ])
    y -= 8
    y = p.step_card(MX, y, 2, 'Upgrade the plan', [
        'You pay only the difference, and the larger credit pool applies immediately.',
        'Cheaper than overage if you overrun every month.',
    ])
    y -= 8
    y = p.step_card(MX, y, 3, 'Opt in to additional usage', [
        'Set a budget you choose. Usage beyond the included credits bills against it.',
        'OPT-IN — you will not be charged overage you did not enable.',
    ])
    y -= 10
    y = p.tip_box(MX, y, 'Set the budget on day one', [
        'A budget is a ceiling, not a commitment. Setting it while you are calm is',
        'better than setting it after a bill you did not expect.',
    ])
    y -= 14
    p.info_panel(MX, y, 'WHAT RUNNING OUT ACTUALLY FEELS LIKE', [
        'Chat declines and tells you why. Agent mode will not start. Completions and',
        'Next Edit Suggestions carry on exactly as before, because they were never',
        'metered — so the editor does not suddenly go quiet. For most people the',
        'day continues largely unchanged, which is why it is easy not to notice.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Estimating Your Own Cost')
    y = p.body(MX, y - 6,
               'Rather than guess, run a deliberate week. Use Copilot the way you '
               'actually work, then read your usage. One real week beats any estimate '
               'built from someone else\'s workflow.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Start on Pro', [
        '$10 buys 1,500 credits, which is a generous evaluation budget.',
        'Do not start on Max "to be safe" — you will not learn anything.',
    ])
    y -= 8
    y = p.step_card(MX, y, 2, 'Work normally for a week', [
        'Do not ration yourself. An artificially careful week gives a useless number.',
    ])
    y -= 8
    y = p.step_card(MX, y, 3, 'Read the usage page, then multiply', [
        'Four weeks of that pattern is your monthly figure.',
        'Comfortably under 1,500? Stay on Pro. Over it every week? Price Pro+.',
    ])
    y -= 10
    y = p.info_panel(MX, y, 'A SANITY CHECK', [
        'Compare the monthly cost against an hour of your time. Copilot does not have',
        'to be transformative to be worth $10 — it has to save an hour a month.',
    ])
    y -= 14
    p.warn_box(MX, y, 'Do not benchmark on your worst week', [
        'A week spent on one gnarly bug is not representative — agent-heavy debugging',
        'is the most expensive way to use Copilot and the least typical. Measure a',
        'normal week, then add a margin rather than pricing for the outlier.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 3 — INSTALLING

def ch3(v):
    lbl = 'Chapter 3  ·  Installing Copilot'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Pick Your Editor')
    y = p.body(MX, y - 6,
               'Copilot runs in more places than most people realise. Completions are '
               'available almost everywhere; chat is available in fewer. Install in the '
               'editor you already use — switching editors to get Copilot is a mistake.')
    y -= 10
    y = p.table(MX, y, ['Editor', 'Completions', 'Chat'], [
        ('VS Code', 'Yes', 'Yes'),
        ('Visual Studio', 'Yes', 'Yes'),
        ('JetBrains IDEs', 'Yes', 'Yes'),
        ('Neovim / Vim', 'Yes', 'No'),
        ('Xcode', 'Yes', 'Limited'),
        ('Eclipse, Zed, Azure Data Studio', 'Yes', 'Varies'),
        ('Terminal', 'via Copilot CLI', 'n/a'),
    ], [220, 110, CW - 330])
    y -= 16
    y = p.tip_box(MX, y, 'One account, every editor', [
        'Your subscription is tied to your GitHub account, not to a machine or an',
        'editor. Install it everywhere you work at no extra cost.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'If you genuinely have no preference')
    y -= 4
    y = p.body(MX, y, 'Use VS Code. Not because it is the better editor — that argument '
                      'has no end — but because Copilot features land there first and '
                      'the gap is widest for agent mode and Next Edit Suggestions.')
    y -= 6
    p.warn_box(MX, y, 'Do not switch editors to get Copilot', [
        'The productivity you lose relearning an editor dwarfs what you gain from a',
        'slightly better Copilot integration. Install it where you already work.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'VS Code')
    y = p.body(MX, y - 6, 'The most complete experience, and the one most guides assume.')
    y -= 8
    y = p.step_card(MX, y, 1, 'Install the extension', [
        'Extensions panel (Ctrl/Cmd+Shift+X), search "GitHub Copilot", Install.',
        'Publisher must be GitHub — there are imitations.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Sign in', [
        'A prompt appears bottom-right. Click it, and authorise in the browser.',
        'No prompt? Command Palette -> "GitHub Copilot: Sign In".',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Confirm it is alive', [
        'The Copilot icon sits in the status bar. Solid means ready.',
        'A slash through it means disabled — click to re-enable.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Add Chat if it did not come along', [
        'Recent builds bundle it. Older ones need "GitHub Copilot Chat" separately.',
    ])
    y -= 8
    p.warn_box(MX, y, 'If nothing appears', [
        'The extension needs a signed-in GitHub account WITH an active Copilot plan.',
        'A GitHub account alone is not enough — check your subscription first.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Visual Studio and JetBrains')
    y -= 4
    y = p.subheading(MX, y, 'Visual Studio (2022 17.10+)')
    y -= 4
    y = p.body(MX, y, 'Copilot ships with Visual Studio — there is usually nothing to '
                      'install. Sign in with the GitHub account carrying your subscription '
                      'via the account picker at the top right.')
    y -= 6
    y = p.code_block(MX, y, [
        '# If it seems missing:',
        'Tools > Options > GitHub > Copilot',
        '# Or add it via the Visual Studio Installer:',
        'Individual components > GitHub Copilot',
    ])
    y -= 14
    y = p.subheading(MX, y, 'JetBrains (IntelliJ, PyCharm, WebStorm, Rider, GoLand...)')
    y -= 4
    y = p.step_card(MX, y, 1, 'Install the plugin', [
        'Settings -> Plugins -> Marketplace -> "GitHub Copilot" -> Install.',
        'Restart the IDE when prompted.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Sign in', [
        'Tools -> GitHub Copilot -> Login to GitHub.',
        'Copy the device code, paste it in the browser window that opens.',
    ])
    y -= 8
    y = p.tip_box(MX, y, 'Same plugin, every JetBrains IDE', [
        'Install once per IDE, but the subscription and settings follow your account.',
    ])
    y -= 14
    p.table(MX, y, ['If sign-in fails', 'Try'], [
        ('Browser never opens', 'Copy the device code and open github.com/login/device'),
        ('Signed in, no suggestions', 'Restart the IDE — the plugin loads at startup'),
        ('Works in one IDE, not another', 'Each IDE needs the plugin installed separately'),
        ('Corporate network', 'Proxy settings — Copilot needs outbound HTTPS'),
    ], [230, CW - 230])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Neovim and the Terminal')
    y -= 4
    y = p.subheading(MX, y, 'Neovim')
    y -= 4
    y = p.body(MX, y, 'Completions only — there is no chat panel in Neovim. Install via '
                      'your plugin manager, then authenticate once.')
    y -= 6
    y = p.code_block(MX, y, [
        '# lazy.nvim',
        '{ "github/copilot.vim" }',
        '',
        '# then, inside Neovim:',
        ':Copilot setup',
        ':Copilot status',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Copilot CLI')
    y -= 4
    y = p.body(MX, y, 'Brings Copilot to the terminal — explaining commands, suggesting '
                      'the incantation you have forgotten, and running agentic tasks. '
                      'Note that CLI usage DOES consume credits.')
    y -= 6
    y = p.code_block(MX, y, [
        'gh extension install github/gh-copilot',
        'gh copilot explain "tar -xzvf archive.tar.gz"',
        'gh copilot suggest "find files over 100MB"',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'The CLI is metered', [
        'Unlike editor completions, everything the CLI does draws on credits. Handy,',
        'but it is not the free part of Copilot.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'Where the CLI earns its keep')
    y -= 4
    p.table(MX, y, ['Use it for', 'Rather than'], [
        ('Recalling a flag you use twice a year', 'Ten minutes in a man page'),
        ('Explaining a command before you run it', 'Running it and hoping'),
        ('Long pipelines of standard tools', 'Trial and error in the shell'),
        ('Anything destructive', 'Never — read it yourself first'),
    ], [250, CW - 250])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Verifying the Install')
    y = p.body(MX, y - 6, 'Two minutes now saves an hour of "is it even on?" later.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Create a scratch file', [
        'Something disposable — test.py, scratch.js. Real project, real language.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Write a signature and stop', [
        'Type a function name that states its intent, then wait a beat.',
        'Grey text should appear within a second or two.',
    ])
    y -= 6
    y = p.code_block(MX, y, [
        '# Type this and pause — do not type the body:',
        'def celsius_to_fahrenheit(celsius):',
    ])
    y -= 10
    y = p.step_card(MX, y, 3, 'Accept it', [
        'Tab accepts. Escape dismisses. If you got a correct body, you are done.',
    ])
    y -= 8
    p.info_panel(MX, y, 'STILL NOTHING?', [
        'Check the status bar icon, confirm the plan is active on github.com, and',
        'make sure the file has a recognised extension — Copilot is much quieter in',
        'a file with no language associated with it.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 4 — COMPLETIONS

def ch4(v):
    lbl = 'Chapter 4  ·  Completions & Next Edit Suggestions'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Part You Use All Day')
    y = p.body(MX, y - 6,
               'Completions are the grey text that appears as you type. They are the '
               'oldest part of Copilot, the most reliable, and — on any paid plan — the '
               'part that costs you nothing beyond the subscription.')
    y -= 10
    y = p.table(MX, y, ['Key', 'Does'], [
        ('Tab', 'Accept the whole suggestion'),
        ('Esc', 'Dismiss it'),
        ('Alt/Option + ]', 'Next alternative suggestion'),
        ('Alt/Option + [', 'Previous alternative'),
        ('Ctrl/Cmd + -> ', 'Accept one word only'),
        ('Alt/Option + \\', 'Ask for a suggestion right now'),
    ], [160, CW - 160])
    y -= 16
    y = p.subheading(MX, y, 'Accepting one word at a time')
    y -= 4
    y = p.body(MX, y, 'The most underused key in the list. When a suggestion starts right '
                      'and drifts wrong, take the good part word by word instead of '
                      'accepting everything and deleting half.')
    y -= 6
    y = p.tip_box(MX, y, 'Alternatives are free', [
        'Cycling through suggestions costs nothing. If the first one is wrong, look',
        'at the second before you start typing it yourself.',
    ])
    y -= 14
    y = p.info_panel(MX, y, 'WHAT THE GREY TEXT ACTUALLY IS', [
        'A prediction of the most likely continuation, given the window of context',
        'described in chapter 1. It is not a lookup, and it is not retrieved from a',
        'database of correct answers — which is exactly why it can be fluent and',
        'wrong at the same time. Fluency is what it optimises for.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Driving It Deliberately')
    y = p.body(MX, y - 6,
               'Waiting passively for grey text is the beginner mode. The skill is '
               'setting up the context so the suggestion you want is the obvious one.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Name things precisely', [
        'parse_iso_timestamp() produces a far better body than handle().',
        'The name is the prompt.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Write the comment first', [
        'A one-line comment stating the intent, then stop and wait.',
        'This is the single highest-leverage habit in the chapter.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Show it one example', [
        'Write the first case by hand. The next three arrive nearly free,',
        'because it now knows your shape, naming and error style.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Open the file you are mirroring', [
        'Open tabs are context. The sibling module is the best hint available.',
    ])
    y -= 8
    y = p.code_block(MX, y, [
        '# Comment first, then pause. This gets a good body far more often',
        '# than typing the signature alone.',
        '',
        '# Retry the request up to `attempts` times, doubling the wait',
        '# each failure, and re-raise the last error if all attempts fail.',
        'def retry_with_backoff(fn, attempts=3):',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Next Edit Suggestions')
    y = p.body(MX, y - 6,
               'Completions predict what you are about to type. Next Edit Suggestions '
               'predict where you are about to go — after a change, Copilot proposes the '
               'follow-up edits that change implies, elsewhere in the file.')
    y -= 10
    y = p.info_panel(MX, y, 'WHERE IT EARNS ITS KEEP', [
        'Rename a parameter, and it offers every call site that now needs updating.',
        'Add a field to a type, and it offers the constructor and the serialiser.',
        'Change a signature, and it walks you through the fallout edit by edit.',
    ])
    y -= 12
    y = p.body(MX, y, 'You accept or reject each one in turn, so it behaves like a guided '
                      'refactor rather than a bulk rewrite you have to audit afterwards.')
    y -= 6
    y = p.subheading(MX, y, 'Two things worth knowing')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'It is UNMETERED, exactly like completions — use it freely',
        'It is editor-dependent; VS Code has the most developed implementation',
    ], step=22)
    y -= 6
    y = p.tip_box(MX, y, 'Best habit for a mechanical refactor', [
        'Make the first change by hand, carefully. Then let Next Edit Suggestions',
        'carry the same change through the file while you review each step.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'What it looks like in practice')
    y -= 4
    p.code_block(MX, y, [
        '# 1. You rename the parameter by hand:',
        'def send(recipient, body):        # was: def send(to, body)',
        '',
        '# 2. NES then offers each follow-up in turn, and you accept or skip:',
        '#      line  47   send(to=user.email, ...)      -> recipient=',
        '#      line 112   send(to=admin, ...)           -> recipient=',
        '#      line 203   """Args: to -- the address"""  -> recipient',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When to Stop Accepting')
    y = p.body(MX, y - 6,
               'The failure mode is not bad suggestions. It is good-looking suggestions '
               'accepted without reading, in a file you did not fully understand.')
    y -= 10
    y = p.warn_box(MX, y, 'Read before you Tab', [
        'Copilot writes plausible code. Plausible code passes review, ships, and',
        'fails in production. You own every line you accept.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'Treat these as hard stops')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Anything touching authentication, passwords or tokens',
        'Anything writing SQL from user input',
        'Anything handling money, or rounding it',
        'Anything you could not explain to a colleague afterwards',
        'Any dependency you have never heard of — check it exists',
    ], step=22)
    y -= 8
    y = p.info_panel(MX, y, 'A USEFUL RULE', [
        'If you would not have been able to write it yourself given enough time,',
        'do not accept it until you understand it. Speed you cannot audit is debt.',
    ])
    y -= 14
    y = p.subheading(MX, y, 'A ten-second review that catches most of it')
    y -= 4
    p.table(MX, y, ['Check', 'Looking for'], [
        ('Does it handle the empty case?', 'Empty list, null, zero, missing key'),
        ('Are the errors real?', 'Silently swallowed exceptions'),
        ('Does that function exist?', 'Invented methods that look plausible'),
        ('Is that import real?', 'Hallucinated or typo-squatted packages'),
        ('Off-by-one?', 'Ranges, slices, boundary conditions'),
    ], [230, CW - 230])
    v.close()


# ══════════════════════════════════════════════════════ CH 5 — FIRST HOUR

def ch5(v):
    lbl = 'Chapter 5  ·  Your First Hour'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Guided Run')
    y = p.body(MX, y - 6,
               'Follow this in a real project you know well — familiarity is what lets '
               'you judge whether a suggestion is any good. Budget an hour.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Minutes 0-10  ·  Install and verify', [
        'Chapter 3 for your editor. Do not continue until grey text appears.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Minutes 10-20  ·  Completions only', [
        'No chat yet. Write comments first and let completions answer them.',
        'Practise Alt+] to cycle, and accepting a single word at a time.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Minutes 20-35  ·  Write tests for one function', [
        'Open a function you know is correct. Ask completions for its tests.',
        'Run them. Some will be wrong — that is the lesson, not a failure.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Minutes 35-50  ·  First chat question', [
        'Select code you find confusing and ask it to explain.',
        'Notice this one spends credits, and how little it spends.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Minutes 50-60  ·  Check your usage', [
        'Open the usage page. See what an hour actually cost you.',
        'Now you can forecast a month from evidence rather than a guess.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Habits That Separate Users')
    y = p.body(MX, y - 6,
               'After a few weeks the difference between people who find Copilot '
               'transformative and people who find it annoying comes down to a handful '
               'of habits rather than any setting.')
    y -= 10
    y = p.table(MX, y, ['Habit', 'Why it matters'], [
        ('Comment, then pause', 'Turns a guess into a brief'),
        ('Cycle alternatives', 'The second suggestion is often the right one'),
        ('Accept word by word', 'Keeps the good half of a mixed suggestion'),
        ('Curate open tabs', 'Open files are context; junk tabs are noise'),
        ('Read before Tab', 'The only defence against plausible-but-wrong'),
        ('Scope agent tasks', 'Vague goals are where bills come from'),
    ], [190, CW - 190])
    y -= 16
    y = p.subheading(MX, y, 'And one anti-habit')
    y -= 4
    y = p.body(MX, y, 'Do not fight a suggestion. If two attempts have not produced what '
                      'you want, write it yourself — you will finish sooner than you will '
                      'coax it, and you will understand the result.')
    y -= 6
    y = p.tip_box(MX, y, 'Give it two weeks', [
        'The first days feel like autocomplete with delusions of grandeur. The habits',
        'above are what turn it into something you would pay for.',
    ])
    y -= 14
    p.info_panel(MX, y, 'HOW TO TELL IT IS WORKING FOR YOU', [
        'You reach for it without thinking on routine code, and you stop reaching',
        'for it on the hard parts. If you find yourself arguing with it on hard',
        'problems, or hand-writing the boilerplate it would have handled, the habit',
        'has settled the wrong way round.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Do this', 'How'], [
        ('Accept a suggestion', 'Tab'),
        ('Reject it', 'Esc'),
        ('Next / previous option', 'Alt+]  /  Alt+['),
        ('Accept one word', 'Ctrl/Cmd + Right arrow'),
        ('Force a suggestion', 'Alt+\\'),
        ('Open chat', 'Ctrl/Cmd+Shift+I  (VS Code)'),
        ('Sign in', 'Palette -> GitHub Copilot: Sign In'),
        ('Turn it off in one file', 'Status bar icon -> disable for this language'),
    ], [200, CW - 200])
    y -= 16
    y = p.table(MX, y, ['Cost fact', 'Value'], [
        ('1 AI Credit', '$0.01'),
        ('Free plan', '2,000 completions + 50 chat requests / month'),
        ('Pro', '$10/mo, 1,500 credits'),
        ('Pro+', '$39/mo, 7,000 credits'),
        ('Max', '$100/mo, 20,000 credits'),
        ('Never metered', 'Completions, Next Edit Suggestions'),
        ('Always metered', 'Chat, agent mode, CLI, code review'),
    ], [180, CW - 180])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('No suggestions at all', 'Check status bar icon, then plan is active'),
        ('Signed in, still nothing', 'A GitHub account alone is not a subscription'),
        ('Suggestions stopped today', 'Free plan? You may have hit 2,000 completions'),
        ('Chat refuses to answer', 'Out of credits — completions still work'),
        ('Suggestions are irrelevant', 'Close unrelated tabs; name things better'),
        ('Wrong language suggestions', 'File extension missing or unrecognised'),
        ('Slow suggestions', 'Large file; try splitting it'),
        ('Cannot sign in on JetBrains', 'Tools -> GitHub Copilot -> Login, device code'),
    ], [200, CW - 200])
    y -= 18
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'Volume 2 — Chat & Agent Mode: the metered half of Copilot, and how to get',
        'real work out of it without burning a month of credits in an afternoon.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Before you go — the three things worth remembering', [
        'Completions are free and constant. Chat and agents are metered and',
        'occasional. Read every line before you accept it.',
    ])
    y -= 14
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
               title='Getting Started with Copilot',
               subtitle='Install it, understand what it costs, and use it well',
               badge='VOLUME ONE',
               tagline='WHAT IT IS  ·  COST  ·  INSTALL  ·  COMPLETIONS  ·  FIRST HOUR')

    total = 2 + 4 + 5 + 5 + 4 + 4
    v.cover(
        stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('5', 'EDITORS'),
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
