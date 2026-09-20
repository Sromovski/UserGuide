#!/usr/bin/env python3
"""Copilot Field Guide — Volume 5: Credits, Cost & Teams.

    python build_copilot_v5.py

The series capstone: what Copilot actually costs once more than one person is using it,
and how to keep that predictable.

FACTS VERIFIED 2026-08-02 against docs.github.com/copilot billing documentation.
Documented and load-bearing: 1 AI credit = $0.01 · org credits are POOLED at the billing
entity level · Business 1,900/user/month and Enterprise 3,900/user/month, with a
promotional 3,000 / 7,000 through 1 Sept 2026 · unused credits DO NOT carry over ·
additional usage is ENABLED BY DEFAULT for organizations · budgets exist at four levels.

NOTE: GitHub does not publish Business/Enterprise per-seat prices on its public plans
page. Do not print a seat price here — the credit allocations are the documented facts.
"""
import os

from fieldguide import COPILOT, CW, MX
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Copilot_Field_Guide_Volume_5_Credits_Cost_and_Teams.pdf')

CHAPTERS = [
    (1, 'How Credits Actually Work', 'Pooling, what is billed, and what expires', 3),
    (2, 'Budgets & Controls', 'Four levels of ceiling, and the default that surprises', 8),
    (3, 'Reading Your Usage', 'Measuring, attributing and forecasting real spend', 13),
    (4, 'Business & Enterprise', 'Seats, policy, indemnity and what admins control', 18),
    (5, 'Cost Discipline at Scale', 'Team habits that hold up past ten people', 23),
]


# ══════════════════════════════════════════════════════ CH 1 — CREDITS

def ch1(v):
    lbl = 'Chapter 1  ·  How Credits Actually Work'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'One Number, Then Arithmetic')
    y = p.body(MX, y - 6,
               'Volume 1 introduced credits. This volume is what happens when the bill '
               'has more than one name on it. Everything still starts from one fact.')
    y -= 10
    y = p.info_panel(MX, y, '1 AI CREDIT = $0.01 USD', [
        'So 1,000 credits is $10 of metered usage, 7,000 is $70, and a plan',
        'including 1,900 credits per user includes $19 of usage per user.',
        'Every figure in this volume is that multiplication.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'What consumes them')
    y -= 4
    y = p.table(MX, y, ['Billed in credits', 'Never billed'], [
        ('Copilot Chat', 'Code completions'),
        ('Copilot CLI', 'Next Edit Suggestions'),
        ('Cloud coding agent', ''),
        ('Copilot Spaces, Spark', ''),
        ('Third-party coding agents', ''),
        ('Code review', ''),
    ], [250, CW - 250])
    y -= 16
    y = p.warn_box(MX, y, 'Credits track model usage, not actions', [
        'A credit is not "one request". It is tokens through a model, so the same',
        'button costs different amounts depending on how much context went with it',
        'and which model answered. Volume is a weak predictor; scope is a strong one.',
    ])
    y -= 12
    p.tip_box(MX, y, 'The free half stays free at any scale', [
        'Completions and Next Edit Suggestions are unmetered on every paid plan, for',
        'every seat. A hundred developers autocompleting all day adds nothing.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Pooling — The Thing That Changes At Team Size')
    y = p.body(MX, y - 6,
               'For organisations, credits are pooled at the billing entity level rather '
               'than locked to each seat. This one detail changes how you should think '
               'about the whole bill.')
    y -= 10
    y = p.info_panel(MX, y, 'WHAT POOLING MEANS IN PRACTICE', [
        'Your heavy users draw more than their allocation. Your light users never',
        'touch theirs. What matters is the TOTAL against the pool — not whether any',
        'individual went over. Most teams have a handful of people generating most',
        'of the usage, and pooling is what makes that fine rather than a problem.',
    ])
    y -= 12
    y = p.table(MX, y, ['Do not', 'Instead'], [
        ('Police individual usage', 'Watch the pool'),
        ('Ration the heavy users', 'Ask what they are doing that others are not'),
        ('Buy for the heaviest user', 'Buy for the average, and rely on pooling'),
    ], [200, CW - 200])
    y -= 14
    y = p.tip_box(MX, y, 'A heavy user is usually a signal, not a problem', [
        'The person burning credits is often the one who found the workflow that',
        'works. Find out what it is before you cap them.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'INDIVIDUAL PLANS DO NOT POOL', [
        'Pro, Pro+ and Max are single-seat allocations. Pooling is a property of the',
        'organisation plans, and it is one of the more practical reasons to move a',
        'team off individual subscriptions once there are more than a few of them.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Do not average and assume', [
        'A pool sized on the mean will be exhausted by a team whose distribution is',
        'two heavy users and eight light ones — the mean is the same either way.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Allocations')
    y = p.body(MX, y - 6, 'Documented monthly credit allocations, verified August 2026.')
    y -= 8
    y = p.table(MX, y, ['Individual', 'Base', 'Flex', 'Total'], [
        ('Pro', '1,000', '500', '1,500  ($15)'),
        ('Pro+', '3,900', '3,100', '7,000  ($70)'),
        ('Max', '10,000', '10,000', '20,000  ($200)'),
    ], [130, 100, 100, CW - 330])
    y -= 14
    y = p.table(MX, y, ['Per user, per month', 'Standard', 'Promotional'], [
        ('Copilot Business', '1,900', '3,000'),
        ('Copilot Enterprise', '3,900', '7,000'),
    ], [200, 120, CW - 320])
    y -= 14
    y = p.warn_box(MX, y, 'The promotional rates end 1 September 2026', [
        'Business drops from 3,000 to 1,900 per user, Enterprise from 7,000 to 3,900.',
        'If you sized your team on the promotional numbers, your effective allowance',
        'falls by roughly 40% on that date. Budget for the standard figure now.',
    ])
    y -= 12
    p.info_panel(MX, y, 'SEAT PRICES ARE NOT PUBLISHED', [
        'GitHub does not list Business or Enterprise per-seat pricing on its public',
        'plans page — you get it from sales. The credit allocations above ARE',
        'documented, and they are the number that determines your usage headroom.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Credits Do Not Carry Over')
    y = p.body(MX, y - 6,
               'Unused monthly credits expire. They do not bank, and they do not roll '
               'into next month.')
    y -= 10
    y = p.table(MX, y, ['Consequence', 'What to do'], [
        ('A quiet month is money gone', 'There is no saving it — use it or lose it'),
        ('A quiet quarter means over-buying', 'Size down; you can upgrade instantly'),
        ('Seasonal work spikes', 'Budget for the peak, expect waste in the trough'),
        ('New joiners mid-month', 'Their first month is a partial allocation'),
    ], [230, CW - 230])
    y -= 16
    y = p.subheading(MX, y, 'The planning implication')
    y -= 4
    y = p.body(MX, y, 'Consistently finishing the month with most of the pool unused is '
                      'not prudence — it is a plan one size too large, every month, '
                      'permanently. Look at three months of actuals rather than the '
                      'largest number anybody has hit.')
    y -= 8
    y = p.tip_box(MX, y, 'Upgrading is instant and prorated', [
        'You pay only the difference and the larger pool applies straight away, so',
        'there is no reason to buy headroom "just in case". Start low.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THE ASYMMETRY WORTH EXPLOITING', [
        'Being under-provisioned costs you a few blocked hours and one upgrade',
        'click. Being over-provisioned costs you the difference every month,',
        'silently, forever — and nobody ever files a ticket about it. Err low.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Diarise a review', [
        'Three months after rollout, look at actuals and resize. Almost nobody does',
        'this, which is why so many teams are quietly paying for a tier above the',
        'one they use.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Drives the Number')
    y -= 6
    y = p.table(MX, y, ['Driver', 'Effect'], [
        ('Agent mode on vague goals', 'The single largest, by a distance'),
        ('Model choice', 'Multiplies everything else'),
        ('Cloud agent runs', 'Up to an hour of usage per task'),
        ('Codebase search', 'Reading is billed, not just writing'),
        ('Long chat sessions', 'The whole conversation resent each turn'),
        ('Automated triggers', 'Charged whether or not there was work'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'THE 80/20 OF COPILOT SPEND', [
        'Almost all of it is agent work on under-specified tasks. Chat questions,',
        'even hundreds of them, are noise against one badly scoped agent run on a',
        'large repository. If you only fix one thing, fix task descriptions.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Which is a quality problem wearing a cost costume', [
        'Well-scoped tasks are cheaper AND produce better output. You do not have to',
        'trade one for the other — the same discipline buys both.',
    ])
    y -= 12
    p.info_panel(MX, y, 'WHERE THE OTHER VOLUMES FIT', [
        'Volume 2 chapter 3 — writing an agent task it can finish.',
        'Volume 3 chapter 2 — the five issue headings for the cloud agent.',
        'Volume 4 chapter 1 — putting the rules where everyone gets them.',
        '',
        'This chapter is the invoice those three chapters produce.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 2 — BUDGETS

def ch2(v):
    lbl = 'Chapter 2  ·  Budgets & Controls'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Default That Surprises People')
    y = p.body(MX, y - 6,
               'For organisations, additional usage beyond the included credits is '
               '**enabled by default**. Nobody has to opt in for the bill to exceed the '
               'subscription.')
    y -= 10
    y = p.warn_box(MX, y, 'Know this before your first invoice, not after', [
        'On individual plans, overage is opt-in. On organisation plans it is on',
        'unless an administrator turns it off. That is a reasonable default for',
        'not blocking work, and an unpleasant surprise if nobody told you.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'Two ways to control it')
    y -= 4
    y = p.step_card(MX, y, 1, 'Set budgets', [
        'Caps that stop spend at a number you chose. Work stops at the ceiling.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Disable the paid-usage policy', [
        'Turn off "AI credits paid usage" and usage simply stops when the included',
        'credits run out. No overage is possible at all.',
    ])
    y -= 10
    p.info_panel(MX, y, 'WHICH TO CHOOSE', [
        'Disable paid usage if a predictable bill matters more than uninterrupted',
        'work — most smaller teams. Use budgets if you would rather absorb some',
        'overage than have people blocked mid-task, but want a known worst case.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Four Levels of Budget')
    y -= 6
    y = p.table(MX, y, ['Level', 'Caps'], [
        ('User', 'One person\'s consumption per cycle'),
        ('Cost centre', 'Metered charges for a defined group of users'),
        ('Organization', 'Charges for organization-billed seats'),
        ('Enterprise spending limit', 'Total charges across the enterprise'),
    ], [190, CW - 190])
    y -= 16
    y = p.subheading(MX, y, 'Use the outer ones first')
    y -= 4
    y = p.body(MX, y, 'An enterprise or organisation limit gives you a guaranteed worst '
                      'case with no administration. Per-user budgets are the fiddliest '
                      'and least useful — they fight the pooling that makes the model '
                      'work in the first place.')
    y -= 8
    y = p.table(MX, y, ['Situation', 'Budget at'], [
        ('You just want a known maximum', 'Enterprise or organization'),
        ('Charging teams separately', 'Cost centre'),
        ('One team is a genuine outlier', 'Cost centre for that team'),
        ('One individual is a problem', 'A conversation, not a budget'),
    ], [250, CW - 250])
    y -= 14
    y = p.tip_box(MX, y, 'Set the outer limit on day one', [
        'Before rollout, not after the first invoice. A limit you never reach costs',
        'nothing and removes the entire category of nasty surprise.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Per-user budgets fight the design', [
        'Pooling exists so heavy users can draw on what light users do not touch.',
        'Cap every individual and you have recreated per-seat allocation with extra',
        'administration — and you will still be under the pool overall.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Happens At The Ceiling')
    y = p.body(MX, y - 6,
               'Hitting a limit is not a failure state. It is worth knowing exactly what '
               'people experience, so you can decide whether it is acceptable.')
    y -= 10
    y = p.table(MX, y, ['Still works', 'Stops'], [
        ('Code completions', 'Chat'),
        ('Next Edit Suggestions', 'Agent mode'),
        ('The editor generally', 'Copilot CLI'),
        ('', 'Cloud coding agent'),
        ('', 'Code review'),
    ], [250, CW - 250])
    y -= 16
    y = p.info_panel(MX, y, 'THE HALF THAT KEEPS WORKING IS THE HALF PEOPLE USE MOST', [
        'A developer who hits the limit still has inline autocomplete all day. They',
        'lose the deliberate, occasional features. That is a genuinely survivable',
        'outage — which is what makes disabling paid usage a reasonable default for',
        'a team that wants a fixed bill.',
    ])
    y -= 12
    y = p.warn_box(MX, y, 'Unless it happens on the 3rd of the month', [
        'A pool exhausted in the first week means the plan is wrong, not that people',
        'are careless. Resize rather than leaving the team without chat for 25 days.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Tell people what happens before it happens', [
        'Someone who knows chat stops at the ceiling plans around it. Someone who',
        'discovers it mid-task files a bug report and loses an afternoon deciding',
        'whether their installation is broken.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Sensible Configuration')
    y = p.body(MX, y - 6, 'What to set before anyone starts, for a team new to this.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Set an organisation-level budget', [
        'Pick a number you would be comfortable paying every month, and set it',
        'as the cap. It is a ceiling, not a commitment.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Decide on paid usage deliberately', [
        'On for continuity, off for predictability. Either is defensible;',
        'not having chosen is not.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Leave per-user budgets alone', [
        'They fight pooling and generate administration. Add them only if a',
        'specific problem appears.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Tell people what you chose', [
        'A developer who knows chat will stop at the limit behaves differently',
        'to one who discovers it mid-task.',
    ])
    y -= 10
    p.tip_box(MX, y, 'Revisit after two months, not two weeks', [
        'The first fortnight is exploration and is not representative. Two months',
        'of actuals tells you what the team really uses.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Cost Centres')
    y = p.body(MX, y - 6,
               'A cost centre caps and attributes metered charges for a defined group of '
               'users — the mechanism for charging spend back to the team that generated '
               'it, or for ring-fencing one group without touching everyone else.')
    y -= 10
    y = p.table(MX, y, ['Use a cost centre when', 'Because'], [
        ('Teams are billed separately', 'Attribution has to be per team'),
        ('One group is experimenting', 'Contain the experiment, not the company'),
        ('A contractor group needs a cap', 'Different risk, different ceiling'),
        ('You want per-team visibility', 'The pool alone hides who is doing what'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'DO NOT REACH FOR THIS EARLY', [
        'Cost centres are real administration. For a single team on one budget, the',
        'organisation-level limit does everything you need. Add structure when the',
        'org chart demands it, not in anticipation.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Attribution beats restriction', [
        'Teams that can see their own usage manage it themselves. Teams that are',
        'simply capped tend to escalate instead.',
    ])
    y -= 12
    p.info_panel(MX, y, 'THE ORDER TO ADD STRUCTURE IN', [
        'One organisation-level ceiling, always.  Cost centres when finance needs',
        'per-team attribution.  Per-user budgets essentially never — and if you find',
        'yourself wanting one, the real problem is a conversation you have not had.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 3 — USAGE

def ch3(v):
    lbl = 'Chapter 3  ·  Reading Your Usage'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Measure Before You Decide Anything')
    y = p.body(MX, y - 6,
               'Almost every argument about Copilot cost is conducted without data. The '
               'usage view resolves it in about five minutes.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Run a deliberate month', [
        'Normal work, no rationing. A team told to be careful produces a number',
        'that tells you nothing about what they would actually use.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Read the pool, not the people', [
        'Total consumption against total allocation. Individual variation is',
        'expected and is what pooling is for.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Find the shape', [
        'Is it a broad base, or two people and everyone else? Those are',
        'different situations needing different responses.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Project three months', [
        'One month is a sample. Three is a trend, and covers a quiet period.',
    ])
    y -= 10
    p.info_panel(MX, y, 'THE ONLY TWO QUESTIONS THAT MATTER', [
        'Are we within the pool? And is the work it produced worth what it cost?',
        'Everything else is detail.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Interpreting What You See')
    y -= 6
    y = p.table(MX, y, ['Pattern', 'Usually means'], [
        ('Well under the pool, every month', 'Over-provisioned — size down'),
        ('Steady, near the pool', 'Correctly sized. Do nothing'),
        ('Exhausted early, every month', 'Under-provisioned, or agent misuse'),
        ('One huge spike', 'One task, badly scoped — find out which'),
        ('Rising month on month', 'Adoption. Expected, and good'),
        ('Fell off a cliff', 'People stopped using it — ask why'),
    ], [230, CW - 230])
    y -= 16
    y = p.warn_box(MX, y, 'Falling usage is the one to investigate', [
        'A team that stops using a tool you are paying for has usually hit',
        'something — bad results, a slow model, a policy that blocks them. The',
        'invoice looks better and the problem is worse.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Ask before you conclude', [
        'The usage view tells you what happened, never why. Five minutes with the',
        'heaviest and lightest user explains more than any dashboard.',
    ])
    y -= 12
    p.info_panel(MX, y, 'TWO QUESTIONS THAT GET YOU THE ANSWER', [
        'To the heaviest user: "what are you using it for that others might not be?"',
        'To the lightest: "what stopped you reaching for it?"',
        '',
        'Between them those two answers explain most usage distributions, and both',
        'produce something you can act on.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Is It Worth It?')
    y = p.body(MX, y - 6,
               'The honest comparison is not Copilot against zero. It is Copilot against '
               'the hourly cost of the people using it.')
    y -= 10
    y = p.info_panel(MX, y, 'THE ARITHMETIC', [
        'A Business seat includes 1,900 credits — $19 of metered usage per user per',
        'month, plus the seat price. Against a loaded developer cost, that is a',
        'small fraction of one hour. The bar is not "transformative"; the bar is',
        '"saves an hour a month", and most teams clear it in the first week.',
    ])
    y -= 12
    y = p.subheading(MX, y, 'What actually justifies it')
    y -= 4
    y = p.bullets(MX + 4, y, [
        'Boilerplate written in seconds rather than minutes, constantly',
        'Tests that get written because writing them got cheap',
        'Unfamiliar syntax stopped being a context switch',
        'Mechanical migrations that would otherwise be deferred forever',
    ], step=22)
    y -= 6
    y = p.warn_box(MX, y, 'And what does not', [
        'Time "saved" producing code nobody reviewed is not a saving. If your team',
        'is shipping more and understanding less, the number on the invoice is not',
        'the cost you should be worried about.',
    ])
    y -= 12
    p.info_panel(MX, y, 'A MEASURE THAT IS NOT NONSENSE', [
        'Do not count lines generated or suggestions accepted — both go up when',
        'things get worse. Ask the team whether they would give it up. A tool people',
        'would fight to keep is paying for itself; one they would shrug at is not,',
        'whatever the acceptance rate says.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Forecasting a Rollout')
    y = p.body(MX, y - 6,
               'Going from five users to fifty is not linear, because usage is not evenly '
               'distributed and pooling absorbs the variance.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Pilot with a representative ten', [
        'Not the ten most enthusiastic. Enthusiasts are not your median.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Take the per-user average from the pilot', [
        'Average, not peak. Pooling covers the peaks.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Multiply, then add a margin', [
        'Twenty to thirty per cent covers adoption growth as people get better',
        'at using it — which they will.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Compare against the pooled allocation', [
        'Business is 1,900 per user per month standard. Fifty seats is 95,000',
        'credits pooled — $950 of metered usage before any overage.',
    ])
    y -= 10
    p.tip_box(MX, y, 'Remember the promotional cliff', [
        'If you forecast during the promotional period, model the standard rate',
        'as well. Business falls from 3,000 to 1,900 on 1 September 2026.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'A Worked Example')
    y = p.body(MX, y - 6, 'Fifty developers on Business, standard allocation.')
    y -= 10
    y = p.code_block(MX, y, [
        'Pooled allocation   50 seats x 1,900 credits   = 95,000 credits',
        '                                               = $950 of usage',
        '',
        'Pilot actuals       1,400 credits/user/month average',
        'Projected           50 x 1,400                 = 70,000 credits',
        'Plus 25% adoption margin                       = 87,500 credits',
        '',
        'Headroom            95,000 - 87,500            = 7,500 credits',
        'Verdict             Comfortable. No overage expected.',
        '',
        '# But at the promotional rate you would have seen 150,000 pooled,',
        '# and concluded you had twice the headroom you will actually have.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'THE POINT OF THE EXAMPLE', [
        'Every number is either documented or measured. None of it is a vendor',
        'estimate or a rule of thumb — which is why you can defend the answer.',
    ])
    y -= 12
    y = p.table(MX, y, ['If the projection came out', 'Then'], [
        ('Comfortably under the pool', 'Proceed. Review in three months'),
        ('Within 10% of the pool', 'Proceed, but decide the overage policy first'),
        ('Over the pool', 'Either size up, or fix task scoping first'),
    ], [250, CW - 250])
    y -= 14
    p.tip_box(MX, y, 'Fix scoping before you buy more', [
        'A team over its pool because of vague agent tasks will be over a bigger',
        'pool too. The cheaper intervention is usually Volume 2, not an upgrade.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 4 — BUSINESS

def ch4(v):
    lbl = 'Chapter 4  ·  Business & Enterprise'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What The Organisation Plans Add')
    y = p.body(MX, y - 6,
               'Business and Enterprise do not primarily add capability. They add the '
               'things an organisation needs in order to allow the capability at all.')
    y -= 10
    y = p.table(MX, y, ['Adds', 'Why it matters'], [
        ('License management', 'Assign and reclaim seats as people join and leave'),
        ('Policy management', 'Decide centrally which features are available'),
        ('IP indemnity', 'The legal cover most companies actually need'),
        ('Pooled credits', 'Heavy users absorbed by light ones'),
        ('Larger allocations', '1,900 or 3,900 per user per month'),
    ], [180, CW - 180])
    y -= 16
    y = p.subheading(MX, y, 'Enterprise on top of Business')
    y -= 4
    y = p.body(MX, y, 'Enterprise includes everything in Business and adds customisation '
                      'layers and deeper GitHub.com integration, plus the larger credit '
                      'allocation. For most teams the question is whether you need '
                      'Business at all, not which of the two.')
    y -= 8
    y = p.info_panel(MX, y, 'IP INDEMNITY IS OFTEN THE DECIDING FACTOR', [
        'It is the item that gets Copilot past legal review at a lot of companies,',
        'and it is not available on individual plans. If your organisation has a',
        'procurement process, expect this to matter more than any feature.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Individual plans on company code are a governance gap', [
        'Developers expensing Pro subscriptions get no indemnity, no policy control',
        'and no visibility for whoever is accountable. It is usually how adoption',
        'starts, and it should not be how it continues.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Policy Management')
    y = p.body(MX, y - 6,
               'An administrator decides which Copilot features the organisation can use. '
               'This is why a feature in this series may simply not appear for you.')
    y -= 10
    y = p.table(MX, y, ['Commonly controlled', 'Effect if disabled'], [
        ('The cloud coding agent', 'Volume 3 does not apply to you'),
        ('AI credits paid usage', 'Hard stop at the included credits'),
        ('Model availability', 'Some models absent from the picker'),
        ('Third-party agents', 'Extension-provided agents unavailable'),
        ('MCP and customisation', 'Volume 4 partly unavailable'),
    ], [200, CW - 200])
    y -= 16
    y = p.tip_box(MX, y, 'Check policy before you debug', [
        'If something in this series does not exist in your editor, the most likely',
        'explanation by far is that an administrator switched it off — not that',
        'your installation is broken. Ask first; it saves an afternoon.',
    ])
    y -= 12
    y = p.info_panel(MX, y, 'FOR ADMINISTRATORS', [
        'Every feature you disable is one your developers will read about and ask',
        'for. Deciding deliberately, and saying so, is much better received than a',
        'silent absence that people discover one at a time.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Write the decisions down somewhere developers look', [
        'A short note in the repository — what is enabled, what is not, and why —',
        'prevents the same question arriving five times and makes the policy feel',
        'like a decision rather than an obstacle.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Rolling Out To A Team')
    y -= 6
    y = p.step_card(MX, y, 1, 'Decide the policies first', [
        'Cloud agent on or off. Paid usage on or off. Which models.',
        'Changing these later is disruptive; deciding them now is free.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Set the budget ceiling', [
        'Organisation level. A number you would happily pay monthly.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Pilot with ten representative people', [
        'For a month. Measure. Do not skip to the whole company.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Write the instruction file', [
        'Volume 4. One repository-level file does more for output quality',
        'than any amount of training.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'Then widen, and re-measure', [
        'Adoption changes the numbers. Check again after two months.',
    ])
    y -= 8
    p.warn_box(MX, y, 'Do not roll out and walk away', [
        'The failure mode is not overspend. It is a tool everyone has, nobody was',
        'shown how to use, and half the team quietly stopped opening.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Governance Questions')
    y = p.body(MX, y - 6,
               'Worth answering before someone senior asks, rather than after.')
    y -= 10
    y = p.table(MX, y, ['Question', 'Where the answer is'], [
        ('What code leaves our network?', 'Copilot sends context to generate output'),
        ('Are we indemnified?', 'Business and Enterprise include IP indemnity'),
        ('Can we cap the spend?', 'Yes — four budget levels, chapter 2'),
        ('Can we disable features?', 'Yes — policy management, this chapter'),
        ('Who can start an agent?', 'Policy-controlled; PRs still need review'),
        ('Does CI run on agent PRs?', 'Not without human approval — Volume 3'),
    ], [220, CW - 220])
    y -= 16
    y = p.info_panel(MX, y, 'THE ONE THAT GETS ASKED FIRST', [
        '"Does our code train their models?" Get the current answer from GitHub\'s',
        'own terms rather than from a guide — it is exactly the kind of commitment',
        'that changes, and it is the question you must not get wrong in a room.',
    ])
    y -= 12
    y = p.tip_box(MX, y, 'Volume 3 chapter 5 is the other half of this', [
        'Branch protections, required review and CI approval are the controls that',
        'make agent-authored code safe. Governance is not only about spend.',
    ])
    y -= 12
    p.warn_box(MX, y, 'Do not answer these from a guide', [
        'Including this one. Data handling and training commitments are exactly the',
        'terms that change between versions, and a confident wrong answer in front',
        'of legal or security costs far more than the ten minutes of checking.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Common Administrative Problems')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Cause'], [
        ('A user has no Copilot at all', 'No seat assigned'),
        ('Feature missing for everyone', 'Policy disabled at org level'),
        ('Feature missing for one team', 'Policy set at a lower scope'),
        ('Unexpected overage', 'Paid usage on by default — chapter 2'),
        ('Pool gone by the 5th', 'Under-provisioned, or one agent misuse'),
        ('Agent cannot open PRs', 'Ruleset blocks it — Volume 3 chapter 5'),
        ('Costs jumped this month', 'Someone discovered agent mode'),
    ], [200, CW - 200])
    y -= 16
    y = p.subheading(MX, y, 'The last one is not a problem')
    y -= 4
    y = p.body(MX, y, 'A jump in spend when someone starts using agent mode is adoption, '
                      'not abuse. The question is whether the output was worth it — and '
                      'usually the answer is to teach the whole team to scope tasks '
                      'properly rather than to cap the one person who got there first.')
    y -= 8
    y = p.info_panel(MX, y, 'BUDGET FOR A LEARNING CURVE', [
        'Month one is always the most expensive per unit of useful output. People',
        'get dramatically better at scoping within a few weeks, and the number',
        'falls without anyone being told to spend less.',
    ])
    y -= 12
    p.tip_box(MX, y, 'Which is an argument for the pilot', [
        'Ten people learning expensively is a rounding error. Two hundred people',
        'learning expensively at the same time is a conversation with finance.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 5 — DISCIPLINE

def ch5(v):
    lbl = 'Chapter 5  ·  Cost Discipline at Scale'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Habits That Scale')
    y = p.body(MX, y - 6,
               'Individual discipline does not survive a growing team. These are the ones '
               'that work because they are built into the repository rather than asked '
               'for in a meeting.')
    y -= 10
    y = p.step_card(MX, y, 1, 'An instruction file, committed', [
        'Better output on every request, for everyone, forever. Volume 4.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Prompt files for the repeated tasks', [
        'A well-scoped prompt everyone uses beats everyone improvising.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'A read-only planner agent', [
        'Cheap thinking before expensive doing.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Hooks for anything mechanical', [
        'Formatting enforced by a hook is formatting you never pay tokens for.',
    ])
    y -= 6
    y = p.step_card(MX, y, 5, 'A shared definition of a good task', [
        'Scope, definition of done, verification, exclusions. Volumes 2 and 3.',
    ])
    y -= 10
    p.info_panel(MX, y, 'NOTICE WHAT IS NOT ON THAT LIST', [
        'Usage policing, per-user caps, and asking people to use it less. Those',
        'reduce spend by reducing value, which is not the same as efficiency.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Teaching the Expensive Lesson Cheaply')
    y = p.body(MX, y - 6,
               'The whole cost story reduces to one skill: describing a task well. It is '
               'worth teaching directly rather than hoping people work it out from an '
               'invoice.')
    y -= 10
    y = p.code_block(MX, y, [
        '# The version that costs a fortune and produces a mess',
        'Improve error handling across the service.',
        '',
        '# The version that costs little and produces a reviewable diff',
        'In api/orders.py, replace bare `except:` with specific exceptions.',
        'Do not change behaviour. Tests in tests/test_orders.py must pass.',
        'Do not modify any other file.',
        '',
        '# Same intent. Different order of magnitude, both in cost and in',
        '# how long the review takes.',
    ])
    y -= 12
    y = p.table(MX, y, ['Teach', 'Because'], [
        ('Name the files', 'Stops repo-wide searching'),
        ('Say what done looks like', 'Stops it running until the limit'),
        ('Give it something to verify', 'Stops plausible-but-wrong output'),
        ('Say what not to touch', 'Stops the diff sprawling'),
    ], [200, CW - 200])
    y -= 14
    p.tip_box(MX, y, 'Put those four lines in the instruction file', [
        'Then every task description in the repository starts from them, including',
        'the ones written by people who never read this volume.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Fact', 'Value'], [
        ('1 AI credit', '$0.01 USD'),
        ('Pro', '1,500 credits/month'),
        ('Pro+', '7,000 credits/month'),
        ('Max', '20,000 credits/month'),
        ('Business', '1,900/user/month (3,000 until 1 Sep 2026)'),
        ('Enterprise', '3,900/user/month (7,000 until 1 Sep 2026)'),
        ('Org credits', 'Pooled at the billing entity level'),
        ('Unused credits', 'Expire — no carry-over'),
        ('Org overage', 'ENABLED by default'),
        ('Never billed', 'Completions, Next Edit Suggestions'),
    ], [180, CW - 180])
    y -= 14
    y = p.table(MX, y, ['Control', 'Level'], [
        ('Budget', 'User · cost centre · organization · enterprise'),
        ('Hard stop', 'Disable the "AI credits paid usage" policy'),
        ('Feature availability', 'Policy management, per organisation'),
    ], [180, CW - 180])
    y -= 14
    p.info_panel(MX, y, 'THE FOUR-LINE VERSION OF THIS VOLUME', [
        'Set an organisation ceiling before rollout.  Decide overage deliberately.',
        'Measure a real month rather than guessing.  And fix task scoping before',
        'you buy a bigger plan — it is cheaper and it improves the output too.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('Bill higher than the subscription', 'Org overage is on by default'),
        ('Pool exhausted early', 'Under-provisioned, or one bad agent run'),
        ('One user dominates the pool', 'Ask what they are doing — often a good sign'),
        ('Usage collapsed', 'People stopped using it; find out why'),
        ('Allowance dropped in September', 'Promotional rates ended 1 Sep 2026'),
        ('Cannot find a feature', 'Policy disabled by an administrator'),
        ('Credits vanished unused', 'They expire monthly; there is no carry-over'),
        ('Forecast was badly wrong', 'Modelled on promotional rates, or on enthusiasts'),
    ], [230, CW - 230])
    y -= 16
    y = p.info_panel(MX, y, 'THAT IS THE SERIES', [
        'Volume 1 — what Copilot is and what it costs.  Volume 2 — chat and agents.',
        'Volume 3 — the CLI and the cloud coding agent.  Volume 4 — customisation.',
        'Volume 5 — credits, cost and running it across a team.',
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
               title='Credits, Cost & Teams',
               subtitle='What Copilot costs at scale, and how to keep it predictable',
               badge='VOLUME FIVE',
               tagline='CREDITS  ·  BUDGETS  ·  USAGE  ·  ADMINISTRATION  ·  DISCIPLINE')

    total = 2 + 5 + 5 + 5 + 5 + 4
    v.cover(
        stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('4', 'BUDGET LEVELS'),
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
