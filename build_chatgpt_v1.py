#!/usr/bin/env python3
"""ChatGPT Field Guide — Volume 1: Getting Started.

    python build_chatgpt_v1.py

Written at volume scale (chapters inside one document) on the fieldguide/ engine, for
NON-TECHNICAL beginners. Output filename must start `ChatGPT_` — covers/catalogue.py's
PREFIX_PALETTE resolves that prefix to the `gpt` cover palette and fails closed on an
unrecognised one.

FACTS VERIFIED 2026-09-20 — see .superpowers/notes/chatgpt-v1-research.md for sources.
ChatGPT's plan lineup moves faster than anything else in this catalogue, so **every
price lives in ONE table on page 6** (chapter 1, "Choosing a Plan") — a reprint is a
single edit there, and nowhere else in the file.

Two things this volume deliberately gets right that an older or generic guide would not:
  * Chapter 4 states the Custom GPT retirement with real dates (migration opens
    17 Sep 2026, new creation ends 25 Sep 2026, GPTs stop running 11 Dec 2026 — confirmed
    for Enterprise, other plans expected to follow) and says plainly that the 2026
    "Plugins" are NOT the 2023 plugins beta OpenAI shut down in 2024.
  * Chapter 1 states the Pro $200 tier is PAUSED for new sign-ups (since 10 Sep 2026) so
    the book never points a buyer at a door that is shut.
  * Chapter 5's voice/image/file limits are UNVERIFIED per the research file — OpenAI
    does not publish exact numbers. The chapter teaches the stable workflows and says so
    explicitly rather than printing a figure that cannot be sourced. The garbled "voice
    tiers" claim and the lower-confidence GPT-6 Astra model note are both omitted, per
    the research file's own instruction.
"""
import os

from fieldguide import GPT, CW, H, MX, Painter, wrap
from fieldguide.volume import Volume

OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'ChatGPT_Field_Guide_Volume_1_Getting_Started.pdf')

CHAPTERS = [
    (1, 'Getting Started', 'What ChatGPT is, signing up, the interface and the plans', 3),
    (2, 'Prompting That Actually Works', 'Copy-paste templates for people who have never written one', 8),
    (3, 'Projects, Memory & Custom Instructions', 'Three ways ChatGPT remembers you, and when to use which', 13),
    (4, 'Plugins & Connected Apps', 'What replaced Custom GPTs, with the dates that matter', 18),
    (5, 'Voice, Images, Files & Data', 'The multimodal side — and what is not yet confirmed', 23),
]


# ══════════════════════════════════════════════════════ CH 1 — GETTING STARTED

def ch1(v):
    lbl = 'Chapter 1  ·  Getting Started'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What ChatGPT Actually Is')
    y = p.body(MX, y - 6,
               'ChatGPT is a website and an app, made by a company called OpenAI, that '
               'you talk to by typing (or speaking) like you would text a very '
               'well-read assistant. Nothing here assumes you have used AI before, or '
               'that you know how to code. If you can send a text message, you already '
               'have the only skill this chapter requires.')
    y -= 10
    y = p.step_card(MX, y, 1, 'A conversation, not a search engine', [
        'Google finds pages that might have your answer. ChatGPT writes the answer',
        'directly, in its own words. That is faster, and it is also why you should',
        'double-check anything that actually matters — it can sound sure and be wrong.',
    ])
    y -= 8
    y = p.step_card(MX, y, 2, 'It remembers the conversation you are in', [
        'Ask a follow-up and it knows what you were just talking about. Start a new',
        'chat, and by default that context is gone — Memory (chapter 3) changes that.',
    ])
    y -= 8
    y = p.step_card(MX, y, 3, 'It does far more than chat', [
        'Write and edit text, generate and edit images, read files you upload, browse',
        'the web, and — through Plugins — reach into apps like Gmail or Calendar.',
        'Every one of those gets its own chapter later in this book.',
    ])
    y -= 10
    p.tip_box(MX, y, 'Treat it like a fast, confident intern', [
        'Great for a first draft, a summary, or an explanation. Not a substitute for',
        'checking anything with real consequences — money, health, legal, dates.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Creating Your Account')
    y = p.body(MX, y - 6,
               'Signing up takes about two minutes and does not require a credit card '
               'unless you choose to subscribe to a paid plan.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Go to chatgpt.com', [
        'Type the address directly rather than searching — search results and app',
        'stores both carry lookalikes that are not the real product.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Choose how to sign up', [
        'Continue with Google, Microsoft or Apple, or use an email address and',
        'password. Any of these are fine — pick whichever you already have handy.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Verify your age and your email', [
        'OpenAI asks for a birth date and, for an email signup, a confirmation link.',
        'This is a one-time step.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Install the mobile app too', [
        'iOS and Android both have official apps. Sign in with the same account and',
        'your chats sync automatically between phone, tablet and browser.',
    ])
    y -= 8
    p.warn_box(MX, y, 'One account is all you need', [
        'Creating several accounts to try to get more free usage is against OpenAI\'s',
        'terms, and it will not meaningfully help — the free tier is what it is.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'The Interface, Briefly')
    y = p.body(MX, y - 6,
               'The screen looks close to empty on purpose. Here is what each part does.')
    y -= 8
    y = p.table(MX, y, ['On screen', 'What it does'], [
        ('New chat', 'Starts a fresh conversation with no earlier context'),
        ('Sidebar', 'Your past chats, and your Projects — see chapter 3'),
        ('Message box', 'Where you type; Shift+Enter for a new line, Enter to send'),
        ('Model picker', 'Top of the screen — which underlying model answers you'),
        ('Attach (+ / paperclip)', 'Upload a file, image or photo to the chat'),
        ('Microphone icon', 'Starts voice mode — see chapter 5'),
        ('Settings gear', 'Account, subscription, personalization, data controls'),
    ], [150, CW - 150])
    y -= 16
    y = p.subheading(MX, y, 'The model picker, without the jargon')
    y -= 4
    y = p.body(MX, y,
               'You will see a short list of model names. They trade off speed, depth '
               'and cost of the underlying compute, and which ones you can pick from '
               'depends on your plan. As a beginner you do not need to chase the '
               '"best" one for every message.')
    y -= 6
    y = p.tip_box(MX, y, 'When in doubt, use the default', [
        'The model selected for you out of the box is a reasonable choice for almost',
        'everything in this book. Come back to the picker once you know why you need to.',
    ])
    y -= 14
    p.info_panel(MX, y, 'A FEW HABITS WORTH BUILDING EARLY', [
        'Rename a chat once it has a clear topic — the sidebar gets long fast.',
        'Start a New Chat when the subject changes entirely, rather than dragging',
        'an old conversation somewhere it was never meant to go.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Choosing a Plan')
    y = p.body(MX, y - 6,
               'Every price in this book lives on this one page, on purpose — ChatGPT\'s '
               'lineup changes more often than anything else in this series. Verified '
               'against OpenAI\'s own help pages as of 20 September 2026. Check '
               'chatgpt.com/pricing before you buy; a printed guide cannot move as fast '
               'as a pricing page can.')
    y -= 10
    y = p.table(MX, y, ['Plan', 'Price', 'Notes'], [
        ('Free', '$0', 'No payment info required to start'),
        ('Go', '$8/mo', '98 countries incl. the EU, since Jan 2026'),
        ('Plus', '$20/mo', 'The standard paid consumer plan'),
        ('Pro (5x)', '$100/mo', '5x Plus usage'),
        ('Pro (20x)', '$200/mo', 'New sign-ups PAUSED — see below'),
        ('Business Standard', '$20-25/seat', 'Per user, team workspace'),
        ('Business Premium', '$100-125/seat', 'Per user, team workspace'),
        ('Enterprise', 'Custom quote', 'Contact sales'),
    ], [120, 90, CW - 210])
    y -= 18
    y = p.warn_box(MX, y, 'The $200 Pro tier is currently closed to new buyers', [
        'OpenAI paused new sign-ups and upgrades to Pro (20x) on 10 September 2026.',
        'Existing $200 subscribers and everyone on the $100 Pro plan are unaffected.',
        'Do not be sold, or sell yourself, a tier you cannot currently purchase.',
    ])
    y -= 14
    p.tip_box(MX, y, 'How billing actually works', [
        'Paid plans bill monthly by default and can be cancelled any time from',
        'Settings > Subscription — you keep access until the period you already',
        'paid for runs out, rather than losing it the moment you cancel.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Which Plan Should You Start With')
    y = p.body(MX, y - 6,
               'Most beginners are well served by Free or Plus. Use this as a starting '
               'point, not a verdict — you can change plans at any time.')
    y -= 10
    y = p.table(MX, y, ['If you...', 'Start with'], [
        ('Just want to try it out', 'Free'),
        ('Use it daily, for work or school', 'Plus'),
        ('Do heavy daily work and want headroom', 'Pro $100 (5x)'),
        ('Already have Pro $200', 'Keep it — new sign-ups only are paused'),
        ('Are buying for a team', 'Business Standard or Premium seats'),
        ('Are buying for a large organisation', 'Enterprise — talk to sales'),
    ], [230, CW - 230])
    y -= 18
    y = p.info_panel(MX, y, 'BEFORE YOU UPGRADE', [
        'Try Free for a real week before paying for anything — most people learn',
        'enough in that week to know whether Plus is worth it for them.',
        'This table can go stale faster than this book can be reprinted; the current',
        'numbers always live at chatgpt.com/pricing.',
    ])
    y -= 14
    p.tip_box(MX, y, 'Downgrading has no penalty', [
        'You keep your account, your chats and your Memory if you drop to Free.',
        'You only lose the paid-only features while you are on the free tier.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 2 — PROMPTING

def ch2(v):
    lbl = 'Chapter 2  ·  Prompting That Actually Works'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What Makes a Prompt Good')
    y = p.body(MX, y - 6,
               'Most disappointing answers are not the AI\'s fault — they come from a '
               'one-line prompt that leaves out everything the AI would need to do '
               'well. Four things turn a vague request into a genuinely useful one.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Say what you want it to be', [
        'A role focuses the answer: "You are a patient math tutor" reads differently',
        'from no role at all, and shapes tone, depth and vocabulary automatically.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Say exactly what you want it to do', [
        'Not "help with my resume" — "rewrite the summary at the top of my resume',
        'to emphasise project management, in three sentences."',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Give it the details it cannot guess', [
        'Audience, tone, length, background it would not otherwise know. It cannot',
        'read your mind, only your message.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Say what the answer should look like', [
        'A bullet list, a table, a word count, plain text with no headers — say so,',
        'or accept whatever format it happens to default to.',
    ])
    y -= 8
    p.tip_box(MX, y, 'One sentence beats one word', [
        '"Trip to Lisbon" gets you something generic. "Plan a 4-day Lisbon trip for',
        'two, mid-range budget, light on museums" gets you something usable.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Before and After')
    y = p.body(MX, y - 6, 'The same request, weak and strong, side by side.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Weak — leaves everything to guesswork:',
        '"Write an email to my landlord."',
        '',
        '# Strong — role, task, context and format are all present:',
        '"Write a polite but firm email to my landlord asking for the broken',
        ' heater to be repaired within a week. Mention I first reported it on',
        ' the 3rd. Keep it under 100 words and end with a clear deadline."',
    ])
    y -= 16
    y = p.code_block(MX, y, [
        '# Weak:',
        '"Help me plan a trip."',
        '',
        '# Strong:',
        '"Help me plan a 5-day trip to Kyoto for one person, mid-October,',
        ' moderate budget. Ask me any questions you need answered first,',
        ' then give me a day-by-day plan."',
    ])
    y -= 16
    y = p.code_block(MX, y, [
        '# Weak:',
        '"Fix my resume."',
        '',
        '# Strong:',
        '"Rewrite the summary at the top of my resume to emphasise project',
        ' management experience, in exactly three sentences, no buzzwords."',
    ])
    y -= 16
    p.tip_box(MX, y, 'Iterate instead of starting over', [
        'Do not delete a mediocre answer and retype from scratch. Reply with "make',
        'it shorter", "more casual", or "cut the second paragraph" — it will revise.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Templates: Work & Writing')
    y = p.body(MX, y - 6,
               'Copy the bracketed template, replace everything in [brackets] with '
               'your own details, and send it as your first message.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Write something',
        '"Write a [tone] [type of message] to [who] about [topic].',
        ' Keep it under [length]. End with a clear [ask/next step]."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Summarize something long',
        '"Summarize this in [3 bullet points / one short paragraph].',
        ' Focus on [what matters to me]. Skip anything I did not ask about."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Explain something confusing',
        '"Explain [topic] as if I have never heard of it. Use one simple',
        ' everyday example. No jargon, or define any word you have to use."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Proofread and tighten',
        '"Proofread this and tighten the wording without changing the meaning.',
        ' Show me what you changed and why, in a short list under the result."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Brainstorm ideas',
        '"Give me [number] different ideas for [goal]. One sentence each,',
        ' then tell me which one you would try first and why."',
    ])
    y -= 12
    p.tip_box(MX, y, 'Five templates, one habit', [
        'Notice all five share the same shape: role or task, the details it needs,',
        'and the format you want back. That shape is the actual skill here.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Templates: Planning & Decisions')
    y = p.body(MX, y - 6, 'Four more, for the moments a blank message box is hardest.')
    y -= 10
    y = p.code_block(MX, y, [
        '# Plan something',
        '"Help me plan [a trip / an event / a project]. Ask me whatever',
        ' questions you need answered first, then build the plan."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Decide between two options',
        '"I am deciding between [option A] and [option B] for [goal].',
        ' List the real tradeoffs, then tell me what you would pick and why."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Learn something new',
        '"Teach me [topic] in [number] short lessons. Quiz me briefly after',
        ' each one before you move on to the next."',
    ])
    y -= 12
    y = p.code_block(MX, y, [
        '# Get unstuck on a problem',
        '"Here is what I have tried on [problem]: [what you tried]. What am',
        ' I missing, and what would you try next?"',
    ])
    y -= 14
    y = p.info_panel(MX, y, 'MAKE ANY TEMPLATE YOURS', [
        'None of these are fixed scripts. Once one gets you most of the way there,',
        'change a phrase, drop a sentence, or bolt two templates together.',
    ])
    y -= 14
    p.tip_box(MX, y, 'Save your favourites somewhere real', [
        'Pin the templates that work for you in a notes app or a document —',
        'not in the chat history, and not in memory.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Common Mistakes')
    y = p.body(MX, y - 6,
               'The same handful of habits account for most disappointing sessions.')
    y -= 10
    y = p.table(MX, y, ['Mistake', 'Fix'], [
        ('Too vague', 'Add a role, a specific task and real context'),
        ('Treating the first answer as final', 'Ask it to revise — do not restart'),
        ('Trusting numbers and dates blindly', 'Verify anything that matters'),
        ('Assuming it remembers last week', 'It does not, unless Memory is on'),
        ('One giant request', 'Break it into steps and check each one'),
    ], [230, CW - 230])
    y -= 18
    y = p.warn_box(MX, y, 'Do not paste sensitive personal information', [
        'Passwords, ID numbers, medical or financial details do not belong in a',
        'chat message. Check Settings > Data Controls for how your chats are used,',
        'and treat the message box like an email you cannot fully take back.',
    ])
    y -= 14
    y = p.tip_box(MX, y, 'The fastest way to get better at this', [
        'Save the templates on this and the previous page somewhere you will',
        'actually reopen them. Muscle memory beats remembering the theory.',
    ])
    y -= 14
    p.info_panel(MX, y, 'IF A PROMPT KEEPS MISFIRING', [
        'Ask it directly: "what information would help you answer this better?"',
        'It will usually tell you exactly what it is missing.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 3 — PROJECTS, MEMORY

def ch3(v):
    lbl = 'Chapter 3  ·  Projects, Memory & Custom Instructions'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Three Ways ChatGPT Remembers You')
    y = p.body(MX, y - 6,
               'These are three separate settings, easy to mix up, and each solves a '
               'different problem. Knowing which one to reach for saves real time.')
    y -= 10
    y = p.table(MX, y, ['Feature', 'What it remembers'], [
        ('Custom instructions', 'A stable identity you set once — tone, language'),
        ('Memory', 'Facts and preferences it picks up over time'),
        ('Projects', 'Files and chats grouped into one topic workspace'),
    ], [170, CW - 170])
    y -= 18
    y = p.info_panel(MX, y, 'THE RULE OF THUMB', [
        'Custom instructions are for something STABLE — the way you always want to',
        'be answered. Memory is for something that EVOLVES — a fact about your life',
        'that was not true a year ago and might not be true next year.',
    ])
    y -= 14
    y = p.tip_box(MX, y, 'You do not have to choose only one', [
        'They are not competing settings. A typical setup uses all three at once:',
        'a fixed tone, a growing set of facts, and a project for the thing you are',
        'currently working on.',
    ])
    y -= 14
    p.info_panel(MX, y, 'A QUICK EXAMPLE OF ALL THREE AT ONCE', [
        'Custom instructions: always answer in a casual tone. Memory: remembers',
        'you have two kids and a dog. A Project: a folder just for planning your',
        'kitchen remodel, with the contractor quotes already attached.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Custom Instructions')
    y = p.body(MX, y - 6,
               'A short, one-time setup that shapes every future conversation, not just '
               'the one you are in.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Open the setting', [
        'Settings > Personalization > Custom instructions.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Answer the two prompts', [
        'What should ChatGPT know about you, and how should it respond. Both are',
        'free text — write in plain sentences, not keywords.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Save it and test it', [
        'Ask something ordinary in a new chat and watch the tone actually stick —',
        'that is the proof it is working.',
    ])
    y -= 8
    y = p.tip_box(MX, y, 'Write it like a note to a new assistant', [
        'Example: "I am a nurse, keep medical explanations precise. I prefer short',
        'answers with bullet points over long paragraphs."',
    ])
    y -= 14
    p.warn_box(MX, y, 'It applies everywhere, all the time', [
        'Unlike Memory, custom instructions are not selective by topic — they',
        'colour every conversation. Keep them general rather than task-specific.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Memory — Two Parts')
    y = p.body(MX, y - 6,
               'Memory has a Saved Memories list you can read and edit directly, plus a '
               'quieter Reference Chat History that recalls things implicitly. Both '
               'store extracted facts and preferences — NOT full transcripts of past '
               'conversations.')
    y -= 10
    y = p.step_card(MX, y, 1, 'See what it remembers', [
        'Settings > Personalization > Manage Memory shows the saved list plainly.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Edit or delete anything wrong', [
        'Click a saved memory to correct or remove it — the same way you would',
        'correct a person who misremembered something.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Turn it off if you would rather it forget', [
        'Saved memories and reference chat history can each be switched off',
        'independently, in the same settings panel.',
    ])
    y -= 8
    y = p.info_panel(MX, y, 'A REALISTIC EXPECTATION', [
        'Memory is a list of extracted facts, not a searchable archive of every',
        'conversation you have had. It can also be wrong or out of date — check',
        'the list occasionally, the same way you would correct a colleague.',
    ])
    y -= 14
    p.tip_box(MX, y, 'Memory works best when you correct it', [
        'If it remembers something wrong, say so directly — "that is not right,',
        'I actually..." — the same way you would correct a person.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Projects')
    y = p.body(MX, y - 6,
               'A Project is a persistent workspace: chats grouped by topic, with '
               'shared files and its own instructions, separate from your main chat.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Create a project', [
        'Sidebar > Projects > New project. Give it a real name — "Kitchen Remodel"',
        'or "College Applications", not "Project 1".',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Add files and start chats inside it', [
        'Upload the documents relevant to that topic; every chat inside the',
        'project can see them without re-uploading.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Set project-specific instructions', [
        'A mini version of custom instructions, scoped to only this project —',
        'useful when one project needs a different tone than everything else.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Choose default or project-only memory', [
        'Keep a sensitive project\'s context out of your general Memory if you',
        'would rather it not carry over into unrelated chats.',
    ])
    y -= 8
    p.info_panel(MX, y, 'WHERE PROJECTS ARE AVAILABLE', [
        'Free, Go, Plus, Pro, Business, Enterprise and Edu — on both web and',
        'mobile, with sharing included.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Which One, For Which Job')
    y -= 6
    y = p.table(MX, y, ['Situation', 'Use'], [
        ('You always want a certain tone or language', 'Custom instructions'),
        ('You want facts about you to carry across chats', 'Memory'),
        ('You are running a multi-week effort with files', 'A Project'),
        ('One topic should not leak into another', 'Separate Projects'),
        ('You want a clean slate, just this once', 'Temporary chat'),
    ], [280, CW - 280])
    y -= 18
    y = p.tip_box(MX, y, 'Start with just one', [
        'You do not need all three set up on day one. Custom instructions alone',
        'is the highest-value five minutes most beginners can spend here.',
    ])
    y -= 14
    y = p.warn_box(MX, y, 'Shared devices, shared accounts', [
        'If you share an account with family or a team, remember Memory and',
        'Projects are visible to everyone on that account — do not store anything',
        'you would not want a co-worker or family member to see.',
    ])
    y -= 14
    p.info_panel(MX, y, 'ONE MORE THING WORTH KNOWING', [
        'Temporary chats do not appear in your history and are not used to update',
        'Memory — reach for one when you want a single throwaway conversation.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 4 — PLUGINS

def ch4(v):
    lbl = 'Chapter 4  ·  Plugins & Connected Apps'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'This Is Not What "Plugins" Used to Mean')
    y = p.body(MX, y - 6,
               'If you read an older guide, or remember trying ChatGPT plugins '
               'yourself years ago, the word is being reused for something genuinely '
               'different. Worth stating plainly, because that older information is '
               'now wrong rather than just outdated.')
    y -= 10
    y = p.info_panel(MX, y, 'A SHORT HISTORY, SO YOU ARE NOT CONFUSED', [
        '2023 — OpenAI launched a "plugins" beta letting ChatGPT call third-party',
        '       tools. It was clunky and never left beta.',
        '2024 — That beta was shut down entirely.',
        '2026 — The name "Plugins" was reused for a new, unrelated system built on',
        '       skills and connected apps. It is not a revival of the 2023 version.',
    ])
    y -= 14
    y = p.tip_box(MX, y, 'If you already know the old plugins, forget them', [
        'Nothing about how they worked, what they could do, or how you installed',
        'them carries over. Read this chapter as if it is your first time.',
    ])
    y -= 16
    p.table(MX, y, ['2023 plugins beta', '2026 plugins'], [
        ('Shut down entirely in 2024', 'Live now, and actively expanding'),
        ('Called outside tools only', 'Bundles skills with connected apps'),
        ('No lasting connection to an app', 'Persistent, authorised connections'),
        ('Discovery was clunky and hidden', 'Installed once, called with @'),
    ], [230, CW - 230])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Custom GPTs Are Being Retired')
    y = p.body(MX, y - 6,
               'The most important fact in this book. Confirmed by OpenAI for '
               'Enterprise workspaces so far, with other plans expected to follow — '
               'check your own workspace rather than assume you are unaffected.')
    y -= 10
    y = p.table(MX, y, ['Date', 'What happens'], [
        ('17 Sep 2026', 'Migration to plugins becomes available'),
        ('25 Sep 2026', 'New GPT creation ends'),
        ('11 Dec 2026', 'Existing Custom GPTs stop running'),
    ], [130, CW - 130])
    y -= 18
    y = p.warn_box(MX, y, 'If you already built a Custom GPT, act on this', [
        'Talk to your workspace admin about migrating it to a plugin once migration',
        'opens on 17 Sep. Do not build a new one after 25 Sep — it will not survive',
        'past 11 Dec. Back up its instructions and any attached files now.',
    ])
    y -= 14
    y = p.body(MX, y,
           'If you have never built or used a Custom GPT, none of this affects you — '
           'skip straight to what a plugin actually is, below.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Not sure whether you have one?', [
        'Check "My GPTs" or "Explore GPTs" in the sidebar — anything you built',
        'yourself is listed there, under your own account.',
    ])
    y -= 8
    p.tip_box(MX, y, 'This is about the feature, not any one GPT', [
        'The retirement is Custom GPTs disappearing over time as a category — not',
        'a ban on a specific one. Treat any GPT you currently rely on as time-limited.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'What a Plugin Actually Is')
    y = p.body(MX, y - 6,
               'A plugin bundles skills — reusable instructions — with a connected '
               'app. Once installed it can search that app\'s data, call its tools, '
               'run multi-step workflows, show its own interactive screens, and take '
               'approved actions inside it on your behalf.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Open Plugins in the sidebar', [
        'Look for "Plugins" in the left-hand sidebar of the app or web version.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Pick one and click Install plugin', [
        'Browse the list, or search for the app you already use.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Connect the account it asks for', [
        'You are sent to that provider\'s own login screen — Gmail asks you to sign',
        'in to Google, not to ChatGPT.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Review the requested permissions before approving', [
        'The screen lists exactly what it can read or do. Read it before clicking',
        'through.',
    ])
    y -= 8
    p.warn_box(MX, y, 'Read the permission screen', [
        'Once approved, a plugin can act on your behalf inside that connected app.',
        'Only connect accounts, and grant permissions, you are actually comfortable',
        'with it touching.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Using Plugins, and What Is Actually Available')
    y = p.body(MX, y - 6,
               'Call an installed plugin with an @ mention — for example, typing '
               '"@Gmail" in the message box — or reach it from the + button under '
               '"More".')
    y -= 10
    y = p.table(MX, y, ['Connected app', 'Common use'], [
        ('Gmail', 'Draft and find emails'),
        ('Google Calendar', 'Check and create events'),
        ('Outlook Email', 'Same, for Microsoft accounts'),
        ('Google Drive', 'Find and summarize your files'),
        ('Slack', 'Search and post messages'),
        ('Notion', 'Read and update pages'),
        ('GitHub', 'Look up issues and code'),
        ('Canva', 'Generate design drafts'),
        ('Figma', 'Pull design context'),
        ('HubSpot', 'CRM lookups'),
    ], [150, CW - 150])
    y -= 20
    p.info_panel(MX, y, 'A PLAN CAVEAT WORTH STATING', [
        'OpenAI\'s pricing page lists Plugins on Free, Go, Plus and Pro. Which',
        'specific plugins you can actually install depends on your plan, workspace,',
        'role and region — do not assume one you saw in a screenshot is available',
        'to you. The Plugins panel itself is the source of truth for your account.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Plugin Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('No "Plugins" in the sidebar', 'Check your plan and workspace settings'),
        ('Install button greyed out', 'A workspace admin may need to enable it'),
        ('@ mention does not trigger it', 'Confirm it is installed, not just browsed'),
        ('Keeps asking to reauthorize', 'Normal — tokens expire, just reconnect'),
        ('My old Custom GPT is missing', 'See the retirement dates on the page before'),
        ('Unsure what a plugin can see', 'Reopen the permission screen from settings'),
    ], [220, CW - 220])
    y -= 18
    y = p.tip_box(MX, y, 'When in doubt, disconnect', [
        'You can remove a connected account at any time from the same Plugins',
        'panel. Nothing is permanent, and reconnecting takes under a minute.',
    ])
    y -= 14
    y = p.info_panel(MX, y, 'IF YOU MANAGE A WORKSPACE', [
        'Admins control which plugins are available and whether members can',
        'install their own — check your workspace\'s Plugin settings before',
        'assuming a teammate\'s issue is on their end rather than a policy.',
    ])
    y -= 14
    p.warn_box(MX, y, 'Do not confuse "disconnected" with "deleted"', [
        'Removing a plugin connection stops it acting on that app — it does not',
        'delete anything already sent or created through it. Undo that separately,',
        'inside the connected app itself, if you need to.',
    ])
    v.close()


# ══════════════════════════════════════════════════════ CH 5 — VOICE, IMAGES, FILES

def ch5(v):
    lbl = 'Chapter 5  ·  Voice, Images, Files & Data'

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Voice Mode')
    y = p.body(MX, y - 6,
               'Voice mode lets you talk instead of type — a full spoken conversation, '
               'hands-free.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Tap the microphone icon', [
        'It sits in the message box on the web and in both mobile apps.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Talk normally, then pause', [
        'It responds by voice once you stop speaking — no wake word needed.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Interrupt any time', [
        'Just start talking again — you do not have to wait for it to finish.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Switch back to text whenever', [
        'Tap the keyboard icon to end voice mode and keep typing in the same chat.',
    ])
    y -= 8
    p.warn_box(MX, y, 'Usage limits exist, but are not printed here as a number', [
        'OpenAI has not published an exact, sourced voice-minutes limit as of this',
        'writing. Figures you will find on other sites vary by plan and are not',
        'traced to an OpenAI page, so this book is not repeating an unverified',
        'number. If you hit a limit, the app will tell you at the time.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Images — Generating and Editing')
    y = p.body(MX, y - 6,
               'Two different things live under "images": generating a brand new one '
               'from a description, and editing one you already have.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Describe what you want, in plain language', [
        '"Generate an image of..." — subject, style and mood are all it needs.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Iterate instead of restarting', [
        '"Make the background darker", "add a hat" — it edits toward what you',
        'described rather than starting over from nothing.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Upload a photo to edit it directly', [
        'Attach button, then describe the change you want made to that photo.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Or ask it to read a photo instead', [
        'Upload and ask "what is this" or "read the text in this image" — that is',
        'analysis, not generation, and works the same way.',
    ])
    y -= 8
    p.info_panel(MX, y, 'ON DAILY LIMITS — STATED HONESTLY', [
        'OpenAI does not publish an exact number of images per day per plan.',
        'Specific figures you may read elsewhere ("2-3 a day on Free") are',
        'estimates from outside sources, not confirmed by OpenAI — treat any exact',
        'number you see, including anywhere else, the same way: unverified.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Files and Data Analysis')
    y = p.body(MX, y - 6,
               'Upload a spreadsheet, PDF or document and ask questions about it. It '
               'can build charts, tables and calculations directly from the data you '
               'give it.')
    y -= 10
    y = p.step_card(MX, y, 1, 'Attach the file', [
        'The paperclip or + icon in the message box, then choose the file.',
    ])
    y -= 6
    y = p.step_card(MX, y, 2, 'Ask a specific question', [
        '"Which month had the highest expenses" gets a real answer. "Look at',
        'this" does not.',
    ])
    y -= 6
    y = p.step_card(MX, y, 3, 'Ask for a chart or table directly', [
        'It can generate a visualisation right inside the answer, not just describe',
        'one in words.',
    ])
    y -= 6
    y = p.step_card(MX, y, 4, 'Push it further with follow-ups', [
        '"Now exclude refunds and redo that" works on the same file across',
        'several messages in the same chat.',
    ])
    y -= 8
    p.warn_box(MX, y, 'File and usage limits exist; exact numbers are unverified', [
        'Sources outside OpenAI describe caps on file count, size and messages per',
        'period, but none trace to an OpenAI page as of this writing. Do not plan',
        'anything time-critical around a specific number you have not confirmed',
        'yourself at chatgpt.com/pricing or help.openai.com.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Quick Reference')
    y -= 6
    y = p.table(MX, y, ['Do this', 'How'], [
        ('Start voice mode', 'Tap the microphone icon'),
        ('Generate an image', 'Describe what you want, in plain language'),
        ('Edit an image', 'Upload it, then say what to change'),
        ('Analyze a spreadsheet', 'Attach it, then ask a specific question'),
        ('Set your tone permanently', 'Settings > Personalization > Custom instructions'),
        ('Check or edit what it remembers', 'Settings > Personalization > Manage Memory'),
        ('Start a persistent workspace', 'Sidebar > Projects > New project'),
        ('Connect an outside app', 'Sidebar > Plugins > Install plugin'),
    ], [220, CW - 220])
    y -= 20
    y = p.table(MX, y, ['Cost fact', 'Value'], [
        ('Free', '$0'),
        ('Go', '$8/mo'),
        ('Plus', '$20/mo'),
        ('Pro (5x)', '$100/mo'),
        ('Pro (20x)', '$200/mo -- paused for new sign-ups'),
    ], [150, CW - 150])
    y -= 16
    p.info_panel(MX, y, 'A NOTE ON THE NUMBERS ABOVE', [
        'Voice, image and file limits are deliberately not listed here — OpenAI',
        'does not publish them. Every figure on this page is confirmed and sourced.',
    ])
    v.close()

    p, y = v.open(lbl)
    y = p.heading(MX, y - 20, 'Troubleshooting')
    y -= 6
    y = p.table(MX, y, ['Problem', 'Fix'], [
        ('Forgot which plan I am on', 'Settings > Subscription'),
        ('Cannot sign up for Pro $200', 'Paused since 10 Sep 2026 -- try $100 or wait'),
        ('My Custom GPT stopped working', 'See the retirement dates in chapter 4'),
        ('It gave me a fact that looks wrong', 'Ask it to double-check, or verify yourself'),
        ('Voice, image or file feature refuses', 'Limits are real but unpublished -- retry later'),
        ('Memory has something wrong in it', 'Settings > Manage Memory > edit or delete'),
    ], [230, CW - 230])
    y -= 18
    y = p.info_panel(MX, y, 'NEXT IN THE SERIES', [
        'This is Volume 1 of the ChatGPT Field Guide series. Future volumes go',
        'deeper on advanced prompting technique and OpenAI\'s other tools.',
    ])
    y -= 14
    y = p.tip_box(MX, y, 'Before you go -- three things worth remembering', [
        'The Custom GPT retirement dates in chapter 4, the Pro $200 pause in',
        'chapter 1, and: always check chatgpt.com/pricing before buying anything —',
        'this book is accurate as printed, but this category moves fast.',
    ])
    y -= 14
    p.info_panel(MX, y, 'MORE GUIDES', [
        'etsy.com/shop/FranksMarketDesigns',
        '',
        'Unofficial and independent. Not affiliated with, endorsed by, or',
        'sponsored by OpenAI.',
    ])
    v.close()


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v = Volume(OUT, GPT,
               title='Getting Started with ChatGPT',
               subtitle='Sign up, prompt well, and use the features that matter',
               badge='VOLUME ONE',
               tagline='GETTING STARTED  ·  PROMPTING  ·  MEMORY  ·  PLUGINS  ·  MULTIMODAL')

    total = 2 + 5 + 5 + 5 + 5 + 5
    v.cover(
        stats=[('5', 'CHAPTERS'), (str(total), 'PAGES'), ('8', 'PLANS COVERED'),
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
