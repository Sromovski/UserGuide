#!/usr/bin/env python3
"""Source data for The Claude Prompt Vault — 200 copy-paste prompts.

Single source of truth. build_prompt_vault.py renders this to PDF, Markdown
and plain text so buyers get a browsable book AND files they can paste from.

Placeholders use [SQUARE BRACKETS] so they are obvious and easy to find/replace.
"""

VAULT_TITLE = 'The Claude Prompt Vault'
VAULT_SUB = '200 copy-paste prompts that get better answers on the first try'

CATEGORIES = [
    ('Writing & Editing', 'Drafting, rewriting, tightening and proofing any kind of prose.', [
        ('Rewrite for clarity',
         'Rewrite the text below so a busy reader understands it in one pass. Keep every fact. '
         'Cut hedging, jargon and filler. Target [WORD COUNT] words.\n\n[PASTE TEXT]'),
        ('Match my voice',
         'Here are three samples of my writing. Study the sentence length, vocabulary and rhythm, '
         'then write [WHAT YOU WANT] in that same voice. Do not imitate the content, only the style.\n\n[PASTE 3 SAMPLES]'),
        ('Ruthless editor',
         'Act as a ruthless editor. Cut this by 30% without losing meaning. Show the edited version '
         'first, then a short list of what you removed and why.\n\n[PASTE TEXT]'),
        ('Explain to a beginner',
         'Explain [TOPIC] to someone who has never encountered it. Use one everyday analogy, avoid '
         'all jargon, and keep it under 200 words. End with the single most common misconception.'),
        ('Three headline options',
         'Write 10 headlines for an article about [TOPIC] aimed at [AUDIENCE]. Give me 3 curiosity-driven, '
         '3 benefit-driven, 3 contrarian and 1 plain-descriptive. No clickbait that the article cannot deliver.'),
        ('Structure before prose',
         'Do not write prose yet. Give me a detailed outline for [PIECE] covering [GOAL], with section '
         'headings and one line describing what each section must accomplish. I will approve it before you draft.'),
        ('Tone shift',
         'Rewrite the text below in a [FORMAL / WARM / DIRECT / PLAYFUL] tone for [AUDIENCE]. '
         'Keep the same structure and length.\n\n[PASTE TEXT]'),
        ('Kill the passive voice',
         'Rewrite this to use active voice throughout, replace nominalisations with verbs, and remove '
         'every adverb that is not doing real work. Show a before/after table for the five biggest changes.\n\n[PASTE TEXT]'),
        ('Fact-check my draft',
         'Read the draft below and flag every claim that is (a) factually checkable and (b) not obviously '
         'true. For each, say what evidence would be needed. Do not rewrite anything.\n\n[PASTE DRAFT]'),
        ('Opening paragraph rescue',
         'My opening is weak. Write 5 alternative first paragraphs for this piece, each using a different '
         'hook: a specific scene, a surprising number, a direct question, a contrarian claim, a short story.\n\n[PASTE DRAFT]'),
        ('Turn notes into prose',
         'Turn these rough notes into a clean [BLOG POST / MEMO / REPORT SECTION]. Preserve every point. '
         'Add connective tissue but invent no new facts. Flag anything that reads as a gap.\n\n[PASTE NOTES]'),
        ('Simplify reading level',
         'Rewrite this at a [GRADE 8] reading level without dumbing down the substance. Shorter sentences, '
         'common words, concrete examples. Tell me the original and new reading level.\n\n[PASTE TEXT]'),
        ('Consistent terminology',
         'Scan this document for inconsistent terminology (the same concept called different things). '
         'Produce a table of variants, recommend one canonical term for each, then apply it.\n\n[PASTE DOC]'),
        ('Write the counter-argument',
         'Write the strongest possible argument against the position in this piece. Steelman it. '
         'Then tell me which two points I must address to keep my argument credible.\n\n[PASTE PIECE]'),
        ('Executive summary',
         'Write a one-paragraph executive summary of the document below for a reader who will read '
         'nothing else. Lead with the conclusion. Include the two numbers that matter most.\n\n[PASTE DOC]'),
        ('Transitions pass',
         'The sections below do not flow. Rewrite only the first and last sentence of each section so '
         'they hand off to each other cleanly. Leave the middles untouched.\n\n[PASTE SECTIONS]'),
        ('Title and subtitle',
         'Give me 8 title + subtitle pairs for [PIECE]. The title should be under 8 words and the subtitle '
         'should say exactly what the reader gets. Rank them by how well they set expectations.'),
        ('Proofread only',
         'Proofread for spelling, grammar and punctuation only. Do not change word choice, style or structure. '
         'Output a numbered list of corrections with the original and the fix.\n\n[PASTE TEXT]'),
        ('Localise for an audience',
         'Adapt this for a [COUNTRY / INDUSTRY] audience: swap examples, idioms, units and references '
         'that will not land. List every change you made and why.\n\n[PASTE TEXT]'),
        ('Repurpose one piece five ways',
         'Take this article and produce: a 250-word LinkedIn post, a 6-tweet thread, a 100-word newsletter '
         'blurb, 5 pull quotes, and a 60-second script. Keep the core argument identical.\n\n[PASTE ARTICLE]'),
    ]),

    ('Email & Messages', 'Inbox work — drafting, replying, chasing, declining, and de-escalating.', [
        ('Reply from bullets',
         'Draft a reply to the email below. My points to make: [BULLET 1], [BULLET 2], [BULLET 3]. '
         'Tone: [WARM BUT BRIEF]. Under 120 words. No filler openers.\n\n[PASTE EMAIL]'),
        ('Say no gracefully',
         'Write a decline to the request below. Be clear that the answer is no, give one honest reason, '
         'offer one alternative if there is a real one, and do not over-apologise.\n\n[PASTE REQUEST]'),
        ('Chase without nagging',
         'Write a third follow-up on [TOPIC]. I have sent two already. Be friendly, acknowledge they are busy, '
         'make the ask a single yes/no question, and give them an easy out.'),
        ('De-escalate an angry email',
         'This customer is angry. Draft a reply that acknowledges the specific problem, takes responsibility '
         'for what is ours, states exactly what happens next and by when. No defensiveness.\n\n[PASTE EMAIL]'),
        ('Cold outreach that is not spam',
         'Write a cold email to [ROLE] at [COMPANY]. I offer [WHAT]. Reference something specific and real about '
         'them: [DETAIL]. Under 100 words. One clear ask. No superlatives.'),
        ('Meeting request',
         'Draft a short email requesting 25 minutes with [PERSON] about [TOPIC]. State the outcome I want, '
         'why it matters to them, and propose three specific slots.'),
        ('Summarise a long thread',
         'Summarise this thread: the decision made, who owns what, open questions, and dates. '
         'Then draft a short message I can send to confirm.\n\n[PASTE THREAD]'),
        ('Bad news, clearly',
         'Tell [AUDIENCE] that [BAD NEWS]. Lead with the news, not the preamble. Explain the cause in one '
         'sentence, the impact in one, the plan in three. No corporate euphemisms.'),
        ('Negotiate a price',
         'Draft a reply pushing back on this quote. My target is [NUMBER] and my walk-away is [NUMBER]. '
         'Anchor politely, justify with [REASON], and keep the relationship intact.\n\n[PASTE QUOTE]'),
        ('Intro email',
         'Write a double opt-in intro connecting [PERSON A, ROLE] and [PERSON B, ROLE]. Say why each should '
         'care about the other in one line, then get out of the way.'),
        ('Ask for a testimonial',
         'Write a short note asking [CLIENT] for a review of [PRODUCT]. Make it easy: offer 3 specific '
         'questions they can answer instead of writing from scratch.'),
        ('Apologise properly',
         'Draft an apology for [WHAT HAPPENED]. Name the mistake plainly, say what it cost them, say what '
         'changes so it does not recur. No "if you were affected" language.'),
        ('Status update nobody skips',
         'Write a weekly update on [PROJECT]. Format: Shipped / In flight / Blocked / Needs a decision from you. '
         'Under 150 words. Bold the one thing they must act on.'),
        ('Reply triage',
         'Here are 10 unread emails. For each, tell me: reply now, reply later, delegate, or archive — '
         'and one line of reasoning. Then draft the "reply now" ones.\n\n[PASTE EMAILS]'),
        ('Set a boundary',
         'Draft a message telling [PERSON] that [BEHAVIOUR] does not work for me, proposing what would work '
         'instead. Firm, not hostile. Under 100 words.'),
        ('Sales follow-up after a demo',
         'Write a follow-up after a demo with [COMPANY]. Recap the two problems they named, tie each to a '
         'specific capability, and propose one concrete next step with a date.'),
        ('Ask a busy expert for help',
         'Write to [EXPERT] asking one specific question about [TOPIC]. Show I did the homework, make the '
         'question answerable in two minutes, and give them permission to ignore it.'),
        ('Resignation letter',
         'Draft a resignation letter to [MANAGER]. Last day [DATE]. Gracious, brief, no grievances, '
         'offer a concrete handover plan.'),
        ('Rewrite my draft, keep my voice',
         'Tighten the email below. Keep my voice and every point. Cut the throat-clearing at the top and '
         'make the ask unmissable.\n\n[PASTE DRAFT]'),
        ('Out of office with substance',
         'Write an out-of-office for [DATES] that tells people who to contact for [TOPIC A] and [TOPIC B], '
         'and sets a realistic expectation for when I will reply.'),
    ]),

    ('Business & Strategy', 'Decisions, planning, positioning and the documents that carry them.', [
        ('Pre-mortem',
         'It is 12 months from now and [PROJECT] has failed badly. Write the post-mortem explaining why. '
         'Give the 8 most likely causes ranked by probability, and the earliest warning signal for each.'),
        ('Decide between two options',
         'I must choose between [OPTION A] and [OPTION B]. Goal: [GOAL]. Constraints: [CONSTRAINTS]. '
         'Build a decision table with the criteria that actually matter, score both, then recommend one and say what would change your mind.'),
        ('One-page strategy',
         'Write a one-page strategy for [BUSINESS]. Sections: where we play, how we win, what we will not do, '
         'the three bets, and the metric that tells us it is working.'),
        ('Positioning statement',
         'Write a positioning statement for [PRODUCT]: for [WHO], who [PROBLEM], [PRODUCT] is a [CATEGORY] '
         'that [BENEFIT]. Unlike [ALTERNATIVE], we [DIFFERENTIATOR]. Then give 3 alternates with different category choices.'),
        ('Pricing sanity check',
         'I sell [PRODUCT] at [PRICE] to [CUSTOMER]. Walk through value-based, cost-plus and competitor-anchored '
         'pricing for it. Tell me which frame fits and what price it implies.'),
        ('Competitor teardown',
         'Analyse [COMPETITOR] against [MY PRODUCT]. Compare positioning, pricing, target buyer, and the one '
         'thing each does better. End with the gap I can credibly own.'),
        ('Business model options',
         'Give me 5 different ways to monetise [PRODUCT / AUDIENCE]. For each: revenue mechanics, what has to '
         'be true for it to work, and how long before it produces real money.'),
        ('Customer interview script',
         'Write 12 interview questions to test whether [AUDIENCE] actually has [PROBLEM]. Non-leading, past-behaviour '
         'focused. Flag which three matter most.'),
        ('Write the FAQ objections',
         'List the 10 objections a [BUYER] will raise about [PRODUCT], ranked by how often they come up. '
         'For each, write the honest one-paragraph answer — not a dodge.'),
        ('SWOT that is not useless',
         'Do a SWOT on [BUSINESS], but every entry must be specific and falsifiable. No "strong team" or '
         '"market is growing". Then tell me the single most important quadrant right now.'),
        ('Board update',
         'Write a monthly investor update for [COMPANY]. Sections: headline metric, what worked, what did not, '
         'what I need help with, cash position. Honest tone. Under 500 words.'),
        ('Unit economics',
         'Walk me through the unit economics of [BUSINESS] given [INPUTS]. Show CAC, LTV, payback period and '
         'contribution margin with the arithmetic visible. Flag which input the answer is most sensitive to.'),
        ('Prioritise a backlog',
         'Score these initiatives on reach, impact, confidence and effort. Show the table, then give me the '
         'ranked list and tell me which two I should kill outright.\n\n[PASTE LIST]'),
        ('Job description',
         'Write a job description for [ROLE] at [COMPANY]. Lead with the problems they will own, not a list of '
         'requirements. Include what success looks like at 90 days and 12 months.'),
        ('Process documentation',
         'Turn this messy process into clean SOP documentation: numbered steps, owner per step, inputs, outputs, '
         'and what to do when it goes wrong.\n\n[PASTE PROCESS]'),
        ('Meeting agenda that ends early',
         'Build an agenda for a [30/60] minute meeting on [TOPIC] with [ATTENDEES]. Each item needs an owner, '
         'a time box, and a decision to be made. Pre-reads listed separately.'),
        ('Risk register',
         'Build a risk register for [PROJECT]: risk, likelihood, impact, owner, mitigation, and the trigger '
         'that means we act. Order by expected cost.'),
        ('Explain this contract',
         'Explain the agreement below in plain English. List every obligation on me, every obligation on them, '
         'the termination terms, and the three clauses I should push back on. You are not giving legal advice.\n\n[PASTE CONTRACT]'),
        ('Investor pitch narrative',
         'Draft the narrative arc for a [SEED] pitch for [COMPANY]: the change in the world, the problem it '
         'creates, why now, our insight, the product, the wedge, and the size of the prize. One slide per beat.'),
        ('Kill criteria',
         'For [PROJECT], define explicit kill criteria: the metrics and dates at which we should stop. '
         'Make them specific enough that I cannot argue my way out of them later.'),
    ]),

    ('Marketing & Social', 'Copy, campaigns, listings and the content that feeds them.', [
        ('Landing page copy',
         'Write landing page copy for [PRODUCT] targeting [AUDIENCE]. Sections: hero headline + subhead, 3 benefit '
         'blocks, objection handling, social proof placeholder, and one CTA repeated twice. Benefits, not features.'),
        ('Product description',
         'Write a product description for [PRODUCT] for [MARKETPLACE]. Lead with the outcome the buyer gets. '
         'Include specifics (format, length, what is included). Under 200 words. Scannable.'),
        ('Etsy listing title',
         'Write 10 Etsy listing titles for [PRODUCT]. Front-load the keyword a buyer would actually type, '
         'stay under 140 characters, and vary the long-tail phrasing so they do not cannibalise each other.'),
        ('13 marketplace tags',
         'Give me 13 tags for an Etsy listing selling [PRODUCT]. Each under 20 characters. Mix broad and '
         'long-tail. No duplicates of words already in the title. Explain the logic in one line.'),
        ('Ad copy variants',
         'Write 6 ad variants for [PRODUCT] on [PLATFORM]. Two lead with pain, two with outcome, two with '
         'a specific number. Match the platform character limits.'),
        ('Content calendar',
         'Build a 4-week content calendar for [BRAND] on [PLATFORM]. Three posts a week. Mix education, proof, '
         'story and offer. Give the hook line for each, not just the topic.'),
        ('Hook lines',
         'Write 20 opening lines for short-form content about [TOPIC] aimed at [AUDIENCE]. Each must make '
         'someone stop scrolling in under a second. No "let me tell you".'),
        ('Email sequence',
         'Write a 5-email welcome sequence for people who downloaded [LEAD MAGNET]. Each email: one idea, one '
         'story, one CTA. Escalate toward [OFFER] without being pushy. Subject lines included.'),
        ('Turn a feature into a benefit',
         'Here are the features of [PRODUCT]. For each, write the benefit in the customer\'s words, then the '
         'proof that makes it believable.\n\n[PASTE FEATURES]'),
        ('Customer language mining',
         'Read these reviews and extract the exact phrases customers use to describe the problem and the '
         'result. Give me a swipe list I can put straight into copy.\n\n[PASTE REVIEWS]'),
        ('SEO article brief',
         'Write a content brief for an article targeting [KEYWORD]. Include search intent, the questions the '
         'page must answer, an H2 structure, internal link opportunities, and word count.'),
        ('Social proof rewrite',
         'Turn these raw testimonials into short, punchy quotes for a sales page. Keep every word truthful and '
         'attributable. Flag any that are too vague to use.\n\n[PASTE TESTIMONIALS]'),
        ('Launch plan',
         'Build a two-week launch plan for [PRODUCT]. Day by day: channel, asset, message, owner. '
         'Include the pre-launch tease and the post-launch follow-up.'),
        ('Newsletter issue',
         'Write a newsletter issue about [TOPIC] for [AUDIENCE]. Open with a specific story, deliver one '
         'genuinely useful idea, close with a soft mention of [OFFER]. Under 600 words.'),
        ('Video script',
         'Write a 60-second script about [TOPIC]. Hook in the first 3 seconds, one idea, one demonstration, '
         'one CTA. Mark the on-screen text separately from the voiceover.'),
        ('Rewrite for a different platform',
         'Adapt this post for [PLATFORM]. Match the native format, length and tone. Do not just truncate — '
         'restructure it for how people read there.\n\n[PASTE POST]'),
        ('Brand voice guide',
         'From the samples below, write a brand voice guide: 3 adjectives, what we sound like, what we never '
         'sound like, 5 do/don\'t pairs, and 3 example sentences.\n\n[PASTE SAMPLES]'),
        ('Case study',
         'Write a customer case study from these notes. Structure: situation, problem, what they tried, what '
         'we did, measurable result. Keep the customer as the hero.\n\n[PASTE NOTES]'),
        ('Offer stack',
         'Design an offer for [PRODUCT] at [PRICE]. What is the core deliverable, what bonuses genuinely '
         'increase value, what is the risk reversal, and what makes acting now rational rather than pressured?'),
        ('Audit my copy',
         'Audit the page below as a skeptical first-time visitor. Where do I lose interest, where do I not '
         'believe you, and what question is left unanswered? Then give the three highest-leverage fixes.\n\n[PASTE COPY]'),
    ]),

    ('Coding & Debugging', 'Everyday development work, from a stack trace to a design review.', [
        ('Explain this code',
         'Explain what the code below does, in order, in plain English. Then list any behaviour that would '
         'surprise a new reader.\n\n[PASTE CODE]'),
        ('Debug from a stack trace',
         'Here is the error and the relevant code. Give me the three most likely root causes ranked by '
         'probability, how to confirm each in under a minute, and the fix for the most likely one.\n\n[PASTE ERROR + CODE]'),
        ('Write the test first',
         'Write failing tests for [BEHAVIOUR] before any implementation. Cover the happy path, the boundary '
         'cases and the error cases. Use [FRAMEWORK]. Do not write the implementation yet.'),
        ('Review my code',
         'Review the diff below for correctness bugs only — not style. For each issue give the concrete input '
         'that triggers it and the wrong output it produces. Say "no issues" if there are none.\n\n[PASTE DIFF]'),
        ('Refactor safely',
         'Refactor this for readability without changing behaviour. Show the refactored code, then a short '
         'list of every behavioural risk your change introduces.\n\n[PASTE CODE]'),
        ('Regex I can read',
         'Write a regex that matches [PATTERN] and not [COUNTER-EXAMPLES]. Then explain it piece by piece '
         'and give me 5 test strings that should match and 5 that should not.'),
        ('SQL query',
         'Given this schema, write a query that returns [RESULT]. Explain the join logic, then tell me what '
         'index would make it fast and how it degrades at [ROW COUNT].\n\n[PASTE SCHEMA]'),
        ('Translate between languages',
         'Port this from [LANGUAGE A] to [LANGUAGE B]. Use idiomatic patterns for the target language rather '
         'than a literal translation. Note anything that cannot be expressed the same way.\n\n[PASTE CODE]'),
        ('Error handling pass',
         'Add proper error handling to this code. Distinguish recoverable from fatal, never swallow an '
         'exception silently, and make every message actionable for whoever reads the log.\n\n[PASTE CODE]'),
        ('Explain the trade-off',
         'I am choosing between [APPROACH A] and [APPROACH B] for [PROBLEM] at [SCALE]. Compare on '
         'correctness, performance, operational cost and how hard each is to reverse. Recommend one.'),
        ('Write the docstrings',
         'Add docstrings to every public function below in [STYLE] format. Document what, not how. '
         'Include the failure modes. Do not change any logic.\n\n[PASTE CODE]'),
        ('Reproduce a bug',
         'Given this bug report, write the smallest possible reproduction script and list the assumptions '
         'you had to make. Then tell me what information is missing from the report.\n\n[PASTE REPORT]'),
        ('Performance profile',
         'This is slow. Identify the likely bottleneck by reasoning about complexity, tell me how to measure '
         'it rather than guess, and give the fix ranked by effort-to-payoff.\n\n[PASTE CODE]'),
        ('Design an API',
         'Design a REST API for [DOMAIN]. Give resources, endpoints, status codes, error shape, pagination '
         'and versioning. Then list the three decisions you would regret at 100x scale.'),
        ('Security pass',
         'Review this for security issues: injection, authz gaps, secrets in code, unsafe deserialisation, '
         'and anything user-controlled reaching a dangerous sink. Concrete findings only.\n\n[PASTE CODE]'),
        ('Migration plan',
         'Plan a migration from [OLD] to [NEW] with zero downtime. Give the phased steps, what runs in parallel, '
         'the rollback at each phase, and how I verify correctness before cutting over.'),
        ('Understand a codebase',
         'I am new to this repo. Based on the structure below, tell me the entry point, the core data flow, '
         'where business logic lives, and the five files I should read first.\n\n[PASTE TREE]'),
        ('Commit message',
         'Write a commit message for this diff. One-line summary under 72 characters in the imperative, blank '
         'line, then why the change was needed — not what the diff already shows.\n\n[PASTE DIFF]'),
        ('Dependency decision',
         'Should I add [LIBRARY] or write this myself? Weigh maintenance burden, bundle size, security surface, '
         'and how much code it actually saves. Give a recommendation.'),
        ('Rubber duck',
         'I am stuck on [PROBLEM]. Ask me one question at a time to narrow down the cause. Do not propose '
         'solutions until you have asked at least four questions.'),
    ]),

    ('Claude Code & Agents', 'Prompts specifically for agentic sessions in Claude Code.', [
        ('Plan before you touch anything',
         'Do not edit any files yet. Read the relevant code, then give me a numbered implementation plan for '
         '[TASK] with the files you will change and why. I will approve before you write.'),
        ('Scope the blast radius',
         'Before changing [THING], find every place in this repo that depends on it. List them with file:line '
         'and tell me which will break.'),
        ('Constrain the edit',
         'Change only [FILE]. Do not touch tests, config or any other file. If the change requires touching '
         'something else, stop and tell me instead of doing it.'),
        ('Write the CLAUDE.md',
         'Read this repo and draft a CLAUDE.md covering tech stack, build and test commands, architecture, '
         'conventions and boundaries. Keep it under 150 lines. Only include things you verified in the code.'),
        ('Reproduce, then fix',
         'First write a failing test that reproduces [BUG]. Show me it fails. Only then fix the code, and '
         'show me the same test passing.'),
        ('Explain before you change',
         'Explain how [FEATURE] currently works, end to end, with file:line references. Do not suggest '
         'improvements yet.'),
        ('Small commits',
         'Implement [TASK] as a sequence of small, independently revertable commits. Tell me the commit '
         'sequence first, then do them one at a time and stop after each.'),
        ('Find the real cause',
         'The symptom is [SYMPTOM]. Do not patch the symptom. Trace it to the root cause, show me the '
         'evidence chain, and only then propose the fix.'),
        ('Verify your own work',
         'After you finish, run the tests and the linter, and paste the actual output. If anything fails, '
         'say so plainly rather than describing the change as complete.'),
        ('Parallel investigation',
         'Search this codebase three different ways for [THING]: by filename, by symbol reference, and by '
         'string content. Report what each method found that the others missed.'),
        ('Set up a hook',
         'Add a PostToolUse hook in .claude/settings.json that runs [COMMAND] after every Edit or Write to '
         '[FILE PATTERN]. Show me the JSON and explain the matcher.'),
        ('Build a subagent',
         'Create a custom subagent at .claude/agents/[NAME].md for [PURPOSE]. Write the frontmatter '
         '(description, tools) so it is triggered only for [SITUATION], and keep the system prompt tight.'),
        ('Audit before refactor',
         'Before refactoring, produce an inventory: every function in [MODULE], what calls it, whether it is '
         'tested, and whether it is dead code. Table format.'),
        ('Stop guessing',
         'Do not guess at the API surface. Read the actual source or docs for [LIBRARY] in this project '
         'and quote the signature you are relying on before you use it.'),
        ('Budget the session',
         'This task should take under [N] tool calls. Plan accordingly, and if you find it will take '
         'substantially more, stop and tell me why before continuing.'),
        ('Review your own diff',
         'Re-read the diff you just produced as a hostile reviewer. What would you reject? Fix those things '
         'before telling me you are done.'),
        ('Write the skill',
         'Create a skill at ~/.claude/skills/[NAME]/SKILL.md for [TASK]. The description field must be '
         'specific enough that it triggers on the right requests and nothing else.'),
        ('Migrate with a checklist',
         'Generate a checklist of every file that needs updating for [MIGRATION], then work through it one '
         'file at a time, marking each done. Do not batch them silently.'),
        ('Ask before assuming',
         'If anything about [TASK] is ambiguous, ask me before you build. Do the unambiguous parts first '
         'and list your questions at the end.'),
        ('Clean handoff',
         'Summarise this session: what changed, what is verified, what is still open, and what the next '
         'person needs to know. Write it as a note I can paste into an issue.'),
    ]),

    ('Data & Analysis', 'Making sense of numbers, spreadsheets and research output.', [
        ('Analyse this dataset',
         'Here is the data. Describe what it contains, flag data quality problems, then answer: [QUESTION]. '
         'Show your reasoning and state your assumptions explicitly.\n\n[PASTE DATA]'),
        ('Excel formula',
         'Write an Excel formula that does [GOAL] given columns [DESCRIBE]. Explain each part, and give '
         'a version that handles blanks and errors gracefully.'),
        ('Find the story',
         'Look at these numbers and tell me the three most interesting things a decision-maker should know. '
         'Rank by how much they should change behaviour, not by how surprising they are.\n\n[PASTE DATA]'),
        ('Sanity check my analysis',
         'Here is my analysis and conclusion. Try to break it. What confounders, selection effects or '
         'arithmetic errors would change the answer?\n\n[PASTE ANALYSIS]'),
        ('Clean this data',
         'Describe every cleaning step this dataset needs before analysis: types, missing values, duplicates, '
         'outliers, inconsistent categories. Give me the code to do it in [TOOL].\n\n[PASTE SAMPLE]'),
        ('Choose the right chart',
         'I want to show [RELATIONSHIP] to [AUDIENCE]. Recommend the chart type, tell me what to put on each '
         'axis, and name two chart types that would mislead here.'),
        ('Explain a statistic',
         'Explain [STATISTIC / METHOD] to someone with no stats background. One analogy, one worked example '
         'with small numbers, and the single most common way people misuse it.'),
        ('Forecast with assumptions visible',
         'Project [METRIC] for the next [PERIOD] from this history. State every assumption as a separate line, '
         'give an optimistic/base/pessimistic case, and tell me which assumption matters most.\n\n[PASTE DATA]'),
        ('Cohort analysis',
         'Structure a cohort analysis for [BUSINESS] to answer [QUESTION]. Define the cohorts, the metric, '
         'the time window, and what a healthy result looks like.'),
        ('Summarise a report',
         'Summarise this report in three layers: one sentence, one paragraph, one page. Preserve the numbers '
         'and the caveats — those are what people drop first.\n\n[PASTE REPORT]'),
        ('Build the metric definition',
         'Define [METRIC] precisely enough that two teams computing it independently get the same number. '
         'Include the numerator, denominator, time window, filters and known edge cases.'),
        ('A/B test read',
         'Here are my test results. Tell me whether the difference is meaningful, what sample size I would '
         'need for confidence, and what could explain it other than the treatment.\n\n[PASTE RESULTS]'),
        ('Pivot table plan',
         'Given these columns, tell me exactly how to build a pivot table that answers [QUESTION]: rows, '
         'columns, values, filters, and what to sort by.\n\n[PASTE COLUMNS]'),
        ('Reconcile two sources',
         'These two reports disagree about [METRIC]. List the plausible reasons for the gap, ranked, and '
         'tell me the fastest check for each.\n\n[PASTE BOTH]'),
        ('Dashboard spec',
         'Spec a dashboard for [ROLE] who needs to decide [DECISION] weekly. Maximum 6 tiles. For each: '
         'the metric, the comparison, and the action it should trigger.'),
        ('Categorise free text',
         'Group these free-text responses into no more than 8 categories that a human would find natural. '
         'Give the category, the count, and two verbatim examples each.\n\n[PASTE RESPONSES]'),
        ('Question the metric',
         'We optimise for [METRIC]. Tell me how someone could improve that number while making the business '
         'worse, and what guardrail metric would catch it.'),
        ('Survey design',
         'Write a [N]-question survey to find out [GOAL] from [AUDIENCE]. Avoid leading and double-barrelled '
         'questions. Tell me which question I will regret including.'),
        ('Python for this analysis',
         'Write pandas code to answer [QUESTION] from a CSV with columns [LIST]. Comment each step. '
         'Include the sanity checks you would run before trusting the output.'),
        ('Present to executives',
         'Turn this analysis into 5 slides for an executive audience. Each slide: one message as the title, '
         'one chart, one implication. Put the detail in an appendix.\n\n[PASTE ANALYSIS]'),
    ]),

    ('Learning & Research', 'Getting up to speed on something new, fast and without illusions.', [
        ('Teach me from zero',
         'Teach me [TOPIC] from zero. Start with the one idea everything else depends on. After each concept, '
         'ask me a question to check I followed before moving on.'),
        ('The 20% that matters',
         'What are the 20% of concepts in [FIELD] that explain 80% of it? List them, explain each in three '
         'sentences, and tell me the order to learn them in.'),
        ('Feynman check',
         'I am going to explain [TOPIC] to you as if teaching it. Point out where my explanation is wrong, '
         'vague or missing something important.\n\n[MY EXPLANATION]'),
        ('Compare two schools of thought',
         'Explain the strongest version of both [POSITION A] and [POSITION B] on [QUESTION]. What evidence '
         'would each side accept as decisive? Where do they actually agree?'),
        ('Reading list',
         'Build me a reading list on [TOPIC] in order: one thing to read first, three to build on it, one '
         'that will change how I think. Say what each one gives me that the others do not.'),
        ('Glossary',
         'Give me a glossary of the 25 terms I will encounter in [FIELD]. Plain-English definition, plus the '
         'most common misunderstanding of each.'),
        ('Interrogate a paper',
         'Read this paper. Tell me the claim, the evidence, the method, the sample, the limitations the '
         'authors admit, and the limitations they do not.\n\n[PASTE PAPER]'),
        ('Spaced repetition deck',
         'Turn this material into 20 flashcards. Question on one side, a short answer on the other. Test '
         'understanding, not recall of phrasing.\n\n[PASTE MATERIAL]'),
        ('Steelman then critique',
         'Make the best possible case for [CLAIM]. Then critique it as rigorously as you can. Then tell me '
         'where you actually land and how confident you are.'),
        ('Learning plan',
         'Build a [4-WEEK] plan to go from beginner to competent at [SKILL] with [HOURS] per week. Weekly '
         'goals, concrete exercises, and a way to tell whether I am actually improving.'),
        ('Explain the disagreement',
         'Experts disagree about [TOPIC]. Map the positions, explain what drives the disagreement (data, '
         'values, definitions?), and tell me what is genuinely unsettled versus settled.'),
        ('Historical context',
         'Give me the history of [TOPIC] as a sequence of problems and responses. What did each development '
         'solve, and what new problem did it create?'),
        ('Practice problems',
         'Give me 10 practice problems on [TOPIC], increasing in difficulty. Do not show the answers until '
         'I ask. Then critique my working, not just my answer.'),
        ('What am I missing',
         'Here is my understanding of [TOPIC]. What important thing am I not accounting for, and what would '
         'a specialist immediately notice was missing?\n\n[MY UNDERSTANDING]'),
        ('Translate the jargon',
         'Rewrite this technical passage for a smart non-specialist. Keep every claim intact. Define terms '
         'inline rather than in a glossary.\n\n[PASTE PASSAGE]'),
        ('Mental model',
         'Give me a mental model for reasoning about [DOMAIN]. What is the model, what does it predict well, '
         'and where does it break down?'),
        ('Interview an expert',
         'You are a [SPECIALIST]. I will ask you questions about [TOPIC]. Answer at the level of a working '
         'practitioner, flag where the field is uncertain, and correct my assumptions when they are wrong.'),
        ('Summarise a book',
         'Summarise [BOOK]: the central argument, the three or four supporting ideas, the best evidence, '
         'the strongest criticism of it, and who should actually read the whole thing.'),
        ('First principles',
         'Break [PROBLEM] down to first principles. What do we actually know, what are we assuming, and '
         'what conclusions survive if we drop the assumptions?'),
        ('Quiz me',
         'Quiz me on [TOPIC] with 10 questions of increasing difficulty. Ask one at a time, wait for my '
         'answer, and tell me what my wrong answers reveal about my mental model.'),
    ]),

    ('Productivity & Planning', 'Getting the right things done and keeping track of them.', [
        ('Triage my day',
         'Here is everything on my plate today plus [HOURS] of real working time. Tell me what to do, what '
         'to defer, what to delegate and what to drop. Justify the drops.\n\n[PASTE LIST]'),
        ('Break down a big task',
         'Break [PROJECT] into tasks no larger than 90 minutes each. Show dependencies, flag which can run '
         'in parallel, and mark the one that is most likely to blow up.'),
        ('Weekly review',
         'Run me through a weekly review. Ask me one question at a time about what shipped, what slipped, '
         'what I learned, and what next week must contain. Then summarise it.'),
        ('Realistic timeline',
         'Estimate how long [PROJECT] will actually take given [CONSTRAINTS]. Give an optimistic, likely and '
         'pessimistic estimate, and name the three things most likely to cause the slip.'),
        ('Meeting notes to actions',
         'Turn these notes into: decisions made, action items with owner and date, open questions, and '
         'anything that was discussed but never resolved.\n\n[PASTE NOTES]'),
        ('Say what to cut',
         'I am committed to all of the following and cannot do it all. Tell me what to cut and in what '
         'order, based on [GOAL].\n\n[PASTE COMMITMENTS]'),
        ('Design a checklist',
         'Build a checklist for [RECURRING TASK]. Every item must be verifiable, ordered correctly, and '
         'include the step people most often forget.'),
        ('Automate this',
         'Here is a task I do manually every week. Tell me which parts are automatable, what tool would do '
         'it, and roughly how long it takes to set up versus how much it saves.\n\n[DESCRIBE TASK]'),
        ('Unblock me',
         'I have been stuck on [TASK] for [TIME]. Ask me diagnostic questions to work out whether the '
         'blocker is unclear scope, missing information, missing skill, or avoidance.'),
        ('Time audit',
         'Here is how I spent last week. Tell me where the time actually went versus where I think it went, '
         'and the single change with the biggest payoff.\n\n[PASTE LOG]'),
        ('Delegate properly',
         'Write a delegation brief for [TASK] to [PERSON]: the outcome, the constraints, the decisions they '
         'own, the decisions they must check with me, and the deadline.'),
        ('Standard operating procedure',
         'Watch me describe how I do [TASK] and turn it into an SOP someone else could follow without asking '
         'me questions. Flag every step where I was vague.\n\n[DESCRIBE]'),
        ('Prep for a hard conversation',
         'I need to talk to [PERSON] about [ISSUE]. Help me prepare: what outcome I want, what they likely '
         'want, my opening two sentences, and how to respond to the three likeliest reactions.'),
        ('Design my week',
         'Given these recurring commitments and [PRIORITY], design a weekly template that protects deep work. '
         'Tell me what has to move and what I have to say no to.\n\n[PASTE COMMITMENTS]'),
        ('Decision journal entry',
         'I am about to decide [DECISION]. Interview me so we capture: what I expect to happen, why, what '
         'would prove me wrong, and when to review it. Then write the entry.'),
        ('Reduce a process',
         'Here is a process with [N] steps. Which steps exist only because of history? Redesign it with the '
         'fewest steps that still produce the same result safely.\n\n[PASTE PROCESS]'),
        ('Onboarding plan',
         'Write a 30-day onboarding plan for [ROLE]. Week by week: what they read, who they meet, what they '
         'ship, and how we know it is going well.'),
        ('Travel or event plan',
         'Plan [TRIP / EVENT] given [DATES], [BUDGET], [CONSTRAINTS]. Give the plan, the booking order, '
         'and the three things most likely to go wrong with a fallback for each.'),
        ('Kill my busywork',
         'Here is my task list. Which of these are genuinely moving [GOAL] forward and which are activity '
         'that feels productive? Be blunt.\n\n[PASTE LIST]'),
        ('End-of-project retro',
         'Run a retro on [PROJECT]. Ask me about what went well, what did not, and what surprised us. '
         'Then write up the three changes worth actually making next time.'),
    ]),

    ('Creative & Ideas', 'Divergent thinking, naming, world-building and getting unstuck.', [
        ('Twenty ideas, no filter',
         'Give me 20 ideas for [GOAL]. The first 10 can be obvious. The last 10 must be ones I would not '
         'have thought of. Do not evaluate them yet.'),
        ('Name it',
         'Generate 20 names for [THING]. Five descriptive, five metaphorical, five invented words, five '
         'short and blunt. Check none are obviously taken in [INDUSTRY]. Say which three you would shortlist.'),
        ('Combine two things',
         'What happens if I combine [A] and [B]? Give me 10 genuinely different concepts that come out of '
         'that intersection, and mark the one with the most potential.'),
        ('Constraint as fuel',
         'Design [THING] under this hard constraint: [CONSTRAINT]. Do not argue with the constraint. '
         'Show me three approaches that treat it as an advantage.'),
        ('Story from a premise',
         'Here is a premise: [PREMISE]. Give me three different directions the story could go, each with '
         'a different central conflict. One paragraph each.'),
        ('Character interview',
         'You are [CHARACTER] from my story. I will interview you. Answer in character, stay consistent '
         'with [DETAILS], and let me discover contradictions.'),
        ('World-building questions',
         'Ask me 15 questions about [WORLD / SETTING] that I have not thought about yet — the ones that '
         'will make it feel real rather than decorated.'),
        ('Analogy generator',
         'Give me 10 analogies for [CONCEPT] drawn from completely different domains. For each, say what it '
         'captures well and where it breaks down.'),
        ('Rewrite in another genre',
         'Rewrite this passage as [GENRE]. Keep the events identical; change only how they are told.\n\n[PASTE PASSAGE]'),
        ('What would break this',
         'Here is my creative concept. Play the audience who does not care. What is boring, confusing or '
         'derivative about it, and what would fix it?\n\n[PASTE CONCEPT]'),
        ('Random constraint',
         'Give me a creative brief for [PROJECT] with three arbitrary constraints that will force an '
         'interesting solution. Then solve it yourself as a demonstration.'),
        ('Dialogue that sounds real',
         'Write a scene where [A] wants [X] and [B] wants [Y], but neither says it directly. Subtext only. '
         'No one explains their feelings.'),
        ('Visual concept',
         'Describe three visual directions for [PROJECT]. For each: palette, typography feel, imagery, '
         'and the emotion it should produce. No mood-board clichés.'),
        ('Title and tagline',
         'Give me 15 title and tagline pairs for [PROJECT]. Vary the register from plain to poetic. '
         'Mark the three that would survive being said out loud.'),
        ('Take the opposite',
         'Everyone in [FIELD] assumes [ASSUMPTION]. What becomes possible if that is false? Give me three '
         'concepts built on the inversion.'),
        ('Structure a talk',
         'Help me structure a [LENGTH] talk on [TOPIC] for [AUDIENCE]. Give the through-line, three movements, '
         'the story that opens it, and the single idea they should remember.'),
        ('Give me a first line',
         'Write 15 possible first lines for [PIECE]. Vary them: one image, one voice, one question, one fact, '
         'one contradiction. No throat-clearing.'),
        ('Develop a half-idea',
         'Here is a half-formed idea. Ask me five questions to sharpen it, then reflect back the strongest '
         'version of what I am actually trying to make.\n\n[PASTE IDEA]'),
        ('Reference hunt',
         'What existing work is [MY IDEA] closest to? Name specific examples, say what each did well, '
         'and tell me what I would have to do differently to not be a copy.'),
        ('Finish it',
         'I have stalled at [POINT]. Do not restart or restructure. Give me three ways forward from exactly '
         'here, and tell me which is the least precious.'),
    ]),
]


def total_prompts():
    return sum(len(items) for _, _, items in CATEGORIES)


if __name__ == '__main__':
    print('%d categories, %d prompts' % (len(CATEGORIES), total_prompts()))
