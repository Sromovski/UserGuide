#!/usr/bin/env python3
"""Codex Field Guide — Volume 4: Delegation, Review & Cost.

    python build_codex_v4.py

FACTS VERIFIED 2026-08-02. Documented and load-bearing:
  * cloud task delegation starts at PLUS — Go is light, local use only
  * usage limits run on a 5-HOUR ROLLING WINDOW
  * per-message pricing was retired 2 April 2026; billing is token-based credits
    (input, cached input, output)
  * GitHub integration provides automatic pull-request code review; there is a Slack
    integration; Codex handles long-horizon task execution
  * /review analyses the current changes for issues

DELIBERATE OMISSION: OpenAI's cloud-task pages were not publicly fetchable when this was
written, so this volume does NOT state specifics about the remote execution environment,
PR-opening behaviour or hard runtime limits. Do not add them on reprint without a
verified source — an invented limit is worse than an acknowledged gap.
"""
import os

from fieldguide import CODEX, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Codex_Field_Guide_Volume_4_Delegation_Review_Cost.pdf')

CHAPTERS = [
    (1, 'Delegating Work', 'Handing over a task and walking away', 3),
    (2, 'Code Review', 'Automated review, and what it is actually good at', 8),
    (3, 'Reviewing Its Work', 'Reading a diff you did not watch being written', 13),
    (4, 'Cost & the Window', 'Where consumption goes, and how to pace it', 18),
    (5, 'Practice', 'A working rhythm, and the whole series in one page', 23),
]


def ch1(v):
    lbl = 'Chapter 1  ·  Delegating Work'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Feature That Changes How You Work')
    y = p.body(MX, y - 6,
               'Everything in Volumes 2 and 3 has you sitting there. Delegation is Codex '
               'running somewhere else, on a task you described, while you do something '
               'entirely different.')
    y -= 10
    y = p.info_panel(MX, y, 'IT STARTS AT PLUS', [
        'Cloud task delegation — the background-agent behaviour — is not included in',
        'the Go tier, which is light, local use only. If working-while-you-are-away',
        'is why you are here, Plus is the entry point.',
    ])
    y -= 12
    y = p.table(MX, y, ['Local (Volumes 2-3)', 'Delegated'], [
        ('Runs on your machine', 'Runs remotely'),
        ('Stops if you close the laptop', 'Keeps going'),
        ('You approve as it goes', 'You review at the end'),
        ('Can reach your local setup', 'Cannot'),
        ('Good for work you steer', 'Good for work you can describe'),
    ], [230, CW - 230])
    y -= 14
    p.tip_box(MX, y, 'The mental model', [
        'A capable contractor you brief in writing and review on the way out — not',
        'a pair programmer. You do not get to correct it mid-thought, so the brief',
        'has to carry everything.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What To Delegate')
    y -= 6
    y = p.table(MX, y, ['Good candidate', 'Why'], [
        ('A well-described bug', 'The failing test is the specification'),
        ('Tests for one module', 'Clear finish line'),
        ('Dependency bumps', 'Mechanical, and CI verifies it'),
        ('Applying a rule repo-wide', 'Repetitive and tedious'),
        ('Documentation from code', 'Bounded, low risk if imperfect'),
        ('A first draft you dreaded', 'Better than a blank file'),
    ], [210, CW - 210])
    y -= 14
    y = p.table(MX, y, ['Keep local', 'Why'], [
        ('Anything needing your local setup', 'A VPN, a local DB, your credentials'),
        ('Work you want to steer closely', 'Delegation removes the steering'),
        ('Design and architecture', 'It decides rather than consulting'),
        ('Anything you cannot describe fully', 'Ambiguity has nobody to resolve it'),
    ], [230, CW - 230])
    y -= 14
    p.info_panel(MX, y, 'THE TEST', [
        'Could a competent contractor who has never seen your product, and cannot',
        'ask you anything, produce something useful from your description? If yes,',
        'delegate. If they would need to ask two questions first, keep it local.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Writing the Brief')
    y = p.body(MX, y - 6,
               'The same four parts as every task in this series, and they matter more '
               'here than anywhere else — nobody is watching the first two minutes to '
               'catch a misunderstanding.')
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
        'pytest tests/test_pricing.py passes, including a new case for',
        'quantity=500 asserting the cap.',
        '',
        '## Out of scope',
        'Do not change tax calculation or touch any other module.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'FIVE HEADINGS, EVERY TIME', [
        'Problem · Expected · Where · How to verify · Out of scope.',
        'A brief missing "how to verify" produces work that declares itself finished',
        'without either of you being sure.',
    ])
    y -= 12
    p.tip_box(MX, y, 'These make your tickets better for people too', [
        'Every heading is something a human picking up the work also wanted and',
        'usually had to ask for.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Long-Horizon Work')
    y = p.body(MX, y - 6,
               'Codex handles long-horizon tasks — work with many steps that would not '
               'fit a single interactive exchange. That capability is genuinely useful '
               'and it is also where the largest failures come from.')
    y -= 10
    y = p.table(MX, y, ['Long task', 'Risk'], [
        ('Many steps, clear finish line', 'Low — it converges'),
        ('Many steps, vague goal', 'High — it sprawls'),
        ('Exploratory with no verification', 'Highest — plausible output, unchecked'),
    ], [250, CW - 250])
    y -= 16
    y = p.warn_box(MX, y, 'Length is not the risk. Vagueness is', [
        'A long task with a test to run converges, however many steps it takes. A',
        'short task with nothing to check against stops at the first plausible',
        'answer. Give it something to verify and the duration stops mattering.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Split anything you cannot describe in one brief', [
        'If the five headings do not fit on a page, it is more than one task. Three',
        'well-scoped briefs review far more easily than one enormous diff.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE REVIEW COST SCALES WORSE THAN THE WORK', [
        'A task twice as large does not take twice as long to review — it takes',
        'longer than that, because the parts interact. Two briefs that each produce',
        'a readable diff beat one that produces something you skim.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Where To Start It')
    y -= 6
    y = p.table(MX, y, ['Surface', 'Good for'], [
        ('Web', 'Describing a task and leaving — the main route'),
        ('iOS', 'Starting or checking one away from your desk'),
        ('VS Code', 'Handing off from where you are already working'),
        ('GitHub integration', 'Review, and work attached to a repository'),
        ('Slack integration', 'Teams that live there'),
    ], [180, CW - 180])
    y -= 16
    y = p.info_panel(MX, y, 'CHECK THE CURRENT DOCS FOR THE DETAIL', [
        'The delegation surfaces and their exact behaviour are the fastest-moving',
        'part of Codex. This volume covers the shape and the judgement — for the',
        'specifics of what a cloud run can reach and how results come back, read',
        'the current documentation rather than any printed guide, including this one.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Try one small delegated task first', [
        'A typo fix or a missing test. You learn the whole loop — brief, wait,',
        'review — for almost nothing, and you find out how results reach you.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Do not delegate something you would struggle to review', [
        'The value of delegation is the time it saves you. A change in an area you',
        'do not know well costs more to review than it saved to generate, and the',
        'temptation to merge it unread is exactly the wrong habit to build early.',
    ])
    v.close()


def ch2(v):
    lbl = 'Chapter 2  ·  Code Review'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Automated Review')
    y = p.body(MX, y - 6,
               'The GitHub integration provides automatic pull-request code review — '
               'including on pull requests people wrote. It is a first pass, not a gate.')
    y -= 10
    y = p.table(MX, y, ['Good at catching', 'Weak at'], [
        ('Obvious bugs and typos', 'Whether the feature is right at all'),
        ('Missing null and edge cases', 'Domain rules it was never told'),
        ('Inconsistent conventions', 'Architectural judgement'),
        ('Missing tests', 'Whether the tests are meaningful'),
        ('Small security smells', 'Threat modelling'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'USE IT TO CLEAR THE MECHANICAL OBJECTIONS', [
        'So that human review starts on the interesting questions instead of',
        'spelling and null checks. It makes people faster; it does not replace them,',
        'and a team that treats a clean automated review as approval will ship',
        'things nobody read.',
    ])
    y -= 12
    p.tip_box(MX, y, '/review does the same thing locally', [
        'Before you push, /review analyses your current changes. Cheapest possible',
        'first pass, and it costs a fraction of what producing the change did.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Reviewing Agent Work With An Agent')
    y = p.body(MX, y - 6,
               'It is tempting to close the loop entirely: an agent writes it, an agent '
               'reviews it, and you merge. That pipeline has no review in it.')
    y -= 10
    y = p.warn_box(MX, y, 'The loop has to have a person in it', [
        'An automated reviewer shares the blind spots of the automated author. It',
        'will not catch the misunderstanding that produced the change, because it',
        'has the same limited view of what you actually wanted.',
    ])
    y -= 12
    y = p.table(MX, y, ['Automated review catches', 'You catch'], [
        ('Mechanical defects', 'Wrong approach'),
        ('Missing cases', 'Solving the wrong problem'),
        ('Convention drift', 'Consequences it cannot see'),
        ('Obvious risk', 'Whether this should exist at all'),
    ], [250, CW - 250])
    y -= 14
    p.info_panel(MX, y, 'THE USEFUL SPLIT', [
        'Let the machine find what is wrong with the code. Keep for yourself the',
        'question of whether the code is the right code. Those are different jobs,',
        'and only one of them is automatable today.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Making Review Cheaper')
    y = p.body(MX, y - 6,
               'Most of what makes agent output hard to review is decided before it runs.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Scope the brief tightly', [
        'A diff confined to two files is a diff you will actually read.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Say what is out of scope', [
        'Most unreviewable diffs are unreviewable because of the parts you did',
        'not ask for.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Require the tests to pass', [
        'Then the diff arrives already knowing it works, and you can spend your',
        'attention on whether it is right.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Ask for small commits', [
        'A history you can read step by step beats one enormous change.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Run /review before you read', [
        'It removes the mechanical objections first.',
    ])
    y -= 8
    p.tip_box(MX, y, 'Review time is the real constraint', [
        'Generation is cheap and getting cheaper. Your attention is not. Every',
        'habit above is about spending less of the scarce resource.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Team Norms Worth Agreeing')
    y -= 6
    y = p.table(MX, y, ['Norm', 'Why'], [
        ('Agent work is labelled', 'Reviewers calibrate differently, and should'),
        ('A person merges. Always', 'The control everything else rests on'),
        ('Same review bar as human code', 'Or the bar quietly becomes lower'),
        ('The author reviews first', 'Do not outsource your own diff to a colleague'),
        ('Unreviewable diffs get rejected', 'Not merged with an apology'),
    ], [230, CW - 230])
    y -= 16
    y = p.warn_box(MX, y, 'The failure mode is social, not technical', [
        'Nobody decides to merge unread code. It happens gradually, because the',
        'last nine agent diffs were fine and this one is long and it is Friday.',
        'Norms exist to make that moment a decision rather than a drift.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'YOU ARE THE AUTHOR ONCE YOU MERGE', [
        'Your name is in the blame and it is your problem at 3am. "The agent wrote',
        'it" has never survived an incident review, and it never will.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Agree these before adoption, not after an incident', [
        'Norms written calmly are norms people follow. Norms written in the',
        'aftermath of a bad merge are a blame document, and they get quietly',
        'ignored within a month.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Slack and Where Work Shows Up')
    y = p.body(MX, y - 6,
               'There is a Slack integration, which mainly changes where a team notices '
               'that work has happened rather than what the work is.')
    y -= 10
    y = p.table(MX, y, ['Helps with', 'Watch for'], [
        ('Visibility of what ran', 'Notification fatigue'),
        ('Kicking off routine tasks', 'Casual briefs, because it is a chat box'),
        ('Sharing results', 'Approval by emoji rather than review'),
    ], [230, CW - 230])
    y -= 16
    y = p.warn_box(MX, y, 'A chat box invites a worse brief', [
        'The five headings are harder to type into Slack than into an issue, so',
        'people do not. The task quality drops and nobody notices until the diff',
        'arrives. If it matters, write it where writing it properly is natural.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Notify, do not approve, in chat', [
        'Chat is a good place to learn that something finished. It is a poor place',
        'to decide whether it was right.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHERE THE BRIEF LIVES SHAPES ITS QUALITY', [
        'An issue template with five headings produces five headings. A chat prompt',
        'produces a sentence. Neither tool is better — but if you want good briefs,',
        'put the work where writing a good one is the path of least resistance.',
    ])
    v.close()


def ch3(v):
    lbl = 'Chapter 3  ·  Reviewing Its Work'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Diff You Did Not Watch')
    y = p.body(MX, y - 6,
               'Reviewing delegated work is different from reviewing your own. You have '
               'no memory of the decisions, and the change arrives complete rather than '
               'growing under your eye.')
    y -= 10
    y = p.code_block(MX, y, [
        '# The shape first — this is the highest-information thirty seconds',
        'git diff --stat',
        '',
        '# Then the detail',
        'git diff',
        '',
        '# Then run the tests YOURSELF',
        'pytest',
        '',
        '# If it is wrong',
        'git restore .',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'START WITH --stat', [
        'The list of files tells you whether it understood the task before you read',
        'a single line. A file you did not expect is the clearest signal available,',
        'and it costs you seconds to see.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Read the smallest surprising diff first', [
        'Not the biggest file. The one-line change somewhere you did not expect is',
        'where the misunderstanding usually shows.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What To Look For')
    y -= 6
    y = p.table(MX, y, ['Check', 'Because'], [
        ('Files outside the stated scope', 'The clearest sign it misunderstood'),
        ('Deletions', 'Easy to miss, expensive to lose'),
        ('What the tests assert', 'Green is not the same as correct'),
        ('New dependencies', 'Does the package exist? Do you want it?'),
        ('Error handling', 'Exceptions swallowed to make tests pass'),
        ('Changed behaviour', 'A "refactor" that quietly does something else'),
        ('Commit history', 'Thrashing means it was guessing'),
    ], [220, CW - 220])
    y -= 16
    y = p.warn_box(MX, y, 'Tests passing is weak evidence', [
        'Anything that can edit both the code and the tests can make any suite',
        'green. Read what they assert. This is the single most common way a',
        'confident run goes wrong, and it looks exactly like success.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE THRASHING TELL', [
        'Commits that add something, remove it, then add it back differently mean it',
        'never had a clear model of the problem. The end state may work by accident.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Accept, Iterate or Reject')
    y -= 6
    y = p.table(MX, y, ['Situation', 'Do'], [
        ('Right approach, details wrong', 'Iterate — this is what it is good at'),
        ('Missed a case you spotted', 'Iterate'),
        ('Wrong approach, code works', 'Reject. Rewrite the brief'),
        ('You do not understand it', 'Reject. Do not merge to save the work'),
        ('Two files right, one wrong', 'Take the two, re-scope the third'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'THE SUNK COST TRAP', [
        'It ran for twenty minutes and produced four hundred lines. That is spent',
        'whether you merge it or bin it. The only live question is whether you want',
        'this code in your repository — and watching it appear is not the same as',
        'having reviewed it.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Rejecting is data, not waste', [
        'Note why it was wrong, put that in the brief as an explicit constraint, and',
        'the second attempt is usually much better and much cheaper.',
    ])
    y -= 12
    p.warn_box(MX, y, 'The one that catches people is "wrong approach, code works"', [
        'It runs, the tests pass, and it is built on a decision you would not have',
        'made. That is the hardest one to reject and the most expensive one to keep,',
        'because it becomes the thing everything after it is built on.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Partial Acceptance Is Normal')
    y = p.body(MX, y - 6,
               'Most delegated work is not uniformly good. Taking the parts that are right '
               'and re-scoping the rest is the common outcome, not a failed run.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Keep some files, discard others',
        'git add tests/test_pricing.py services/pricing.py',
        'git checkout -- .                 # discard everything else',
        'git commit -m "cap discount at 40%"',
        '',
        '# Then a smaller brief for what is left',
    ])
    y -= 12
    y = p.subheading(MX, y, 'Commit in coherent pieces')
    y -= 4
    y = p.body(MX, y, 'Accepting one logical change at a time costs nothing and turns '
                      '"something in here broke it" into a two-minute bisect. It also '
                      'makes the history readable by whoever inherits it, which will '
                      'eventually be you.')
    y -= 8
    y = p.tip_box(MX, y, 'Never commit an agent change without reading it', [
        'Not as a rule about agents. As a rule about your repository — the same one',
        'you would apply to a pull request from anyone you had not met.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'PARTIAL ACCEPTANCE IS A GOOD OUTCOME', [
        'It means the brief was mostly right and you caught the part that was not.',
        'Treating it as a failed run is how people end up accepting everything to',
        'avoid the feeling of waste.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Then make the next brief narrower', [
        'The rejected part tells you exactly which sentence was ambiguous.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'When It Fails')
    y -= 6
    y = p.table(MX, y, ['Symptom', 'Usually'], [
        ('Solved a different problem', 'The brief was ambiguous — fix upstream'),
        ('Touched unrelated files', 'No "out of scope" section'),
        ('Says done, nothing works', 'No verification step in the brief'),
        ('Enormous unreviewable diff', 'Task too big — split it'),
        ('Ran out of the usage window', 'Rolling 5 hours — wait, then resume'),
        ('Thrashing history', 'It never understood; re-scope and restart'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'THE PATTERN IN ALL OF THAT', [
        'Almost every failure traces to the brief rather than the agent. It is fast,',
        'literal and tireless, and it cannot ask a clarifying question halfway',
        'through. Ambiguity a colleague would resolve across a desk becomes twenty',
        'minutes of confident work in the wrong direction.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Keep the briefs that worked', [
        'One that produced a clean result is a template. The five headings plus your',
        'conventions is a reusable asset — and AGENTS.md carries the conventions',
        'so the brief only has to carry this job.',
    ])
    v.close()


def ch4(v):
    lbl = 'Chapter 4  ·  Cost & the Window'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'How Consumption Works Now')
    y = p.body(MX, y - 6,
               'On 2 April 2026 per-message pricing was retired for Plus, Pro and Business '
               'and replaced with token-based credits. Cost now tracks the size of the '
               'job rather than the number of times you pressed enter.')
    y -= 10
    y = p.table(MX, y, ['Counted', 'Meaning'], [
        ('Input tokens', 'Everything sent — the brief, files it read, history'),
        ('Cached input tokens', 'Context it has already seen — cheaper'),
        ('Output tokens', 'Everything it wrote back'),
    ], [190, CW - 190])
    y -= 16
    y = p.info_panel(MX, y, 'AND LIMITS ARE A 5-HOUR ROLLING WINDOW', [
        'Not daily, not monthly. A heavy afternoon throttles you for hours, not for',
        'the rest of the month — and a quiet week banks nothing. That is the single',
        'biggest difference from tools with a monthly allowance.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'So pace, do not ration', [
        'There is nothing to save up and nothing to eke out. Spread heavy work',
        'across a day and you will rarely meet the ceiling at all.',
    ])
    y -= 12
    p.info_panel(MX, y, 'CACHED INPUT IS THE ONE LEVER MOST PEOPLE MISS', [
        'Context it has already seen costs less than context it is reading fresh.',
        'That is a quiet argument for one coherent session per task rather than a',
        'new one for every question — right up to the point where the session gets',
        'confused, at which point starting fresh is cheaper than both.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Where It Actually Goes')
    y -= 6
    y = p.table(MX, y, ['Driver', 'Effect'], [
        ('A vague brief', 'The largest, by a distance — it reads everything'),
        ('Reasoning effort', 'Multiplies everything else'),
        ('Long sessions', 'Whole conversation resent each turn'),
        ('Broad exploration', 'Reading is billed, not just writing'),
        ('Repeated failed attempts', 'Each retry costs as much as the first'),
        ('Automation on a timer', 'Charged whether or not there was work'),
    ], [200, CW - 200])
    y -= 16
    y = p.info_panel(MX, y, 'THE 80/20', [
        'Almost all avoidable consumption is agent work on under-specified tasks.',
        'Interactive questions, even hundreds of them, are noise beside one badly',
        'scoped long-horizon run on a large repository.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Which is a quality problem in disguise', [
        'Well-scoped briefs are cheaper AND produce better output. You are not',
        'trading one against the other — the same discipline buys both.',
    ])
    y -= 12
    p.code_block(MX, y, [
        '# Expensive — it reads everything looking for work',
        'Improve the error handling in this project.',
        '',
        '# Cheap — it reads one file and stops when the tests pass',
        'In api/orders.py, replace bare except blocks with specific exceptions.',
        'Do not change behaviour. tests/test_orders.py must still pass.',
        'Do not modify any other file.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Practical Levers')
    y -= 6
    y = p.step_card(MX, y, 1, 'Name the files', [
        'The cheapest task is the one that never searched the repository.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Drop the reasoning effort', [
        '/model. High effort on a rename produces the same rename, slower.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Use low-effort subagents for reading', [
        'Volume 3. Most delegated work is investigation, and investigation',
        'does not need deep reasoning.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Keep one session per task', [
        'Long enough for the cache to help, short enough to stay coherent.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Put conventions in AGENTS.md', [
        'So every brief is shorter, and you stop paying to restate them.',
    ])
    y -= 8
    p.info_panel(MX, y, 'IN ROUGH ORDER OF IMPACT', [
        'Brief quality first, by a long way. Then reasoning effort. Then session',
        'hygiene. Everything else is rounding.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing a Tier')
    y -= 6
    y = p.table(MX, y, ['If you', 'Then'], [
        ('Want to try it locally', 'Go — but no delegation'),
        ('Want delegation at all', 'Plus, minimum'),
        ('Use it most working days', 'Pro 5x'),
        ('Consistently hit Pro 5x limits', 'Pro 20x — 2x price, ~4x headroom'),
        ('Are buying for a team', 'Business / Enterprise'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'THE PRO 20x ARITHMETIC IS UNUSUAL', [
        'Twice the price of Pro 5x for roughly four times the headroom. If you are',
        'genuinely hitting the Pro 5x ceiling regularly, the step up is better value',
        'per unit than the step you already took — which is not how tiers usually',
        'work, and worth knowing before you assume the top tier is a rip-off.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'But hit the ceiling first', [
        'Do not buy headroom in anticipation. The window is rolling — meeting it',
        'occasionally is normal and costs you a few hours, not a month.',
    ])
    y -= 12
    p.warn_box(MX, y, 'And check the prices before you commit', [
        'This table was verified in August 2026, and the tiers moved twice that',
        'year — Pro 5x did not exist before April. Anything printed about pricing',
        'is a snapshot, including this page.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Is It Worth It?')
    y = p.body(MX, y - 6,
               'Against your own hourly cost rather than against zero.')
    y -= 10
    y = p.info_panel(MX, y, 'THE BAR IS LOWER THAN PEOPLE ASSUME', [
        'Plus is $20 a month — a small fraction of one working hour. It does not',
        'have to be transformative. It has to save an hour a month, and most people',
        'clear that in the first week on tests alone.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'What genuinely justifies it')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Work that was being deferred indefinitely now happens',
        'Test coverage that exists because writing tests got cheap',
        'Migrations and upgrades that used to eat an afternoon',
        'Reading unfamiliar code without reading all of it',
    ], step=22)
    y -= 6
    y = p.warn_box(MX, y, 'And what does not', [
        'Volume of code produced. If the team is shipping more and understanding',
        'less, the subscription is not the cost worth worrying about.',
    ])
    y -= 12
    p.info_panel(MX, y, 'A MEASURE THAT IS NOT NONSENSE', [
        'After a month, ask whether you would give it up. A tool you would fight to',
        'keep is paying for itself. One you would shrug at is not, whatever the',
        'number of tasks completed says.',
    ])
    v.close()


def ch5(v):
    lbl = 'Chapter 5  ·  Practice'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Working Rhythm')
    y -= 6
    y = p.step_card(MX, y, 1, 'Write AGENTS.md once', [
        'Commands, conventions, boundaries. Twenty lines. Volume 3.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Branch and commit before every run', [
        'Two seconds, and every bad outcome becomes recoverable.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Write the brief with five headings', [
        'Problem, expected, where, how to verify, out of scope.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Local for steering, delegated for describing', [
        'If you want to watch it, keep it local. If you can describe it, hand it off.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Review as if a stranger wrote it', [
        '--stat, then the diff, then run the tests yourself.',
    ])
    y -= 6
    y = p.step_card(MX, y, 6, 'Reject freely', [
        'Cheapest decision available, and it improves the next brief.',
    ])
    y -= 8
    p.info_panel(MX, y, 'THAT IS THE WHOLE PRACTICE', [
        'Six habits. Everything else in these four volumes is detail underneath',
        'one of them.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Series in One Page')
    y -= 6
    y = p.table(MX, y, ['Volume', 'What it gave you'], [
        ('1 — Getting Started', 'What Codex is, where it runs, plans and limits'),
        ('2 — The CLI', 'Permissions, sandbox, commands, codex exec'),
        ('3 — AGENTS.md & MCP', 'Conventions, subagents, your own tools'),
        ('4 — This one', 'Delegation, review and cost'),
    ], [190, CW - 190])
    y -= 16
    y = p.subheading(MX, y, 'If you remember four things')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'The brief determines the result — everything else is downstream',
        'Give it something to verify against, or it stops at plausible',
        'Constrain the environment; do not rely on being attentive',
        'Never merge code you do not understand',
    ], step=24)
    y -= 6
    y = p.tip_box(MX, y, 'None of those are about Codex', [
        'They are about working with something fast, literal and confident that',
        'cannot ask you a question. That skill transfers to every agent you will',
        'use, including the ones that do not exist yet.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHICH IS WHY THE SPECIFICS MATTER LEAST', [
        'Commands change. Prices change. Tiers get renamed — Pro 5x did not exist',
        'six months before this was written. The judgement about how to describe a',
        'task, what to verify and when to reject is the part that keeps working.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Fact', 'Value'], [
        ('Usage limits', '5-hour ROLLING window'),
        ('Billing', 'Token-based credits since 2 Apr 2026'),
        ('Counted', 'Input, cached input, output tokens'),
        ('Delegation', 'Starts at Plus — not in Go'),
        ('Pro 5x', 'Added 9 Apr 2026, $100'),
        ('Pro 20x', 'Was "Pro", $200, ~4x Pro 5x headroom'),
    ], [190, CW - 190])
    y -= 14
    y = p.table(MX, y, ['Do this', 'With'], [
        ('Review local changes', '/review'),
        ('See the shape of a diff', 'git diff --stat'),
        ('Undo everything uncommitted', 'git restore .'),
        ('Continue yesterday', 'codex resume'),
        ('Set model and effort', '/model'),
    ], [190, CW - 190])
    y -= 14
    p.info_panel(MX, y, 'THE FIVE BRIEF HEADINGS', [
        'Problem · Expected · Where · How to verify · Out of scope',
        '',
        'If you take one line from four volumes, take that one.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('Cannot delegate', 'Go is local-only — delegation starts at Plus'),
        ('Hit the usage window', 'Rolling 5 hours. Wait rather than upgrade'),
        ('Costs more than expected', 'Vague briefs, or high reasoning effort'),
        ('Solved the wrong problem', 'The brief was ambiguous — rewrite it'),
        ('Diff too big to review', 'Task was too big — split the brief'),
        ('Tests green, behaviour wrong', 'Read what the tests assert'),
        ('Review feels endless', 'Scope tighter; that is a briefing problem'),
        ('It ignored your conventions', 'Write AGENTS.md — Volume 3'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'THAT IS THE SERIES', [
        'Four volumes: what Codex is, the CLI, configuration, and delegation.',
        'The judgement in them outlasts the specifics — check current documentation',
        'for exact limits and pricing, which move faster than any printed guide.',
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
               title='Delegation, Review & Cost',
               subtitle='Handing work over, checking it, and pacing the usage window',
               badge='VOLUME FOUR',
               tagline='DELEGATION  ·  REVIEW  ·  DIFFS  ·  COST  ·  PRACTICE')
    total = 2 + 5 + 5 + 5 + 5 + 4
    v.cover(stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('5', 'BRIEF HEADINGS'),
                   ('2026', 'EDITION')],
            inside=[(n, t, b) for n, t, b, _ in CHAPTERS])
    v.contents([(n, t, b, s) for n, t, b, s in CHAPTERS])
    ch1(v); ch2(v); ch3(v); ch4(v); ch5(v)
    v.save()
    print('Saved: %s  (%d pages)' % (OUT, v.page_no))


if __name__ == '__main__':
    main()
