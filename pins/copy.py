"""The words on a pin, and where it points.

Titles lead with the SEARCH PHRASE, not the product name -- Pinterest is a
search engine and nobody searches a brand they have not heard of. Descriptions
are keyword-led prose, not hashtag strings, which Pinterest has downranked for
years.

TITLES and DESCRIPTIONS are carried verbatim from outputs/pins/PINS_wave1.csv
-- those nine strings were already written, length-checked against
Pinterest's 100-character title limit, and the owner has already started
posting with them. Do not rewrite them here.

HOOKS, TIPS and COMPARISONS are the only hand-authored strings in this
package. Each must be traceable to something the book actually says.
"""
import build_etsy_kit as _kit
from etsypub import db as _edb
import gumroadpub.publish as _gp

SKUS = [
    '12-start-here',          # free: leads, because free pins get saved
    '40-chatgpt-v1',
    '01-prompt-vault',
    '10-cheat-sheet-pack',
    '02-starter-volume',
    '11-cost-calculator',
    '03-complete-library',
    '20-copilot-v1',
    '30-codex-v1',
]

BOARDS = ['AI for Beginners', 'ChatGPT Tips', 'AI Prompts & Templates',
          'Printable Cheat Sheets', 'AI Tools & Productivity']

BOARD_FOR = {
    '12-start-here': 'AI for Beginners',
    '40-chatgpt-v1': 'ChatGPT Tips',
    '01-prompt-vault': 'AI Prompts & Templates',
    '10-cheat-sheet-pack': 'Printable Cheat Sheets',
    '02-starter-volume': 'AI for Beginners',
    '11-cost-calculator': 'AI Tools & Productivity',
    '03-complete-library': 'AI for Beginners',
    '20-copilot-v1': 'AI Tools & Productivity',
    '30-codex-v1': 'AI Tools & Productivity',
}

# Verbatim from outputs/pins/PINS_wave1.csv `title` column. Already
# length-checked against Pinterest's 100-character limit and already live on
# Pinterest -- do not edit here without editing the CSV and the live pins.
TITLES = {
    '40-chatgpt-v1': 'ChatGPT for Beginners 2026 | Plain English Guide to '
                      'Prompts, Memory and Plugins',
    '01-prompt-vault': '200 AI Prompts to Copy and Paste | Writing, Email, '
                        'Business and Marketing',
    '10-cheat-sheet-pack': 'Printable AI Cheat Sheets | 12 One-Page '
                            'References for ChatGPT and Claude',
    '02-starter-volume': 'Claude AI for Beginners | Complete Starter Guide, '
                          'No Coding Required',
    '11-cost-calculator': 'AI Cost Calculator Spreadsheet | Compare '
                           'ChatGPT, Claude and Gemini Pricing',
    '12-start-here': 'Free AI Learning Roadmap | Where to Start With '
                      'ChatGPT, Claude and Copilot',
    '03-complete-library': 'Complete AI Guide Library | 23 Guides, 140 '
                            'Pages, Beginner to Advanced',
    '20-copilot-v1': 'GitHub Copilot for Beginners | What It Costs and How '
                      'to Set It Up',
    '30-codex-v1': 'OpenAI Codex for Beginners | Install, Setup and Usage '
                    'Limits Explained',
}

# Verbatim from outputs/pins/PINS_wave1.csv `description` column. Same rule
# as TITLES: a pin already live on Pinterest and this file must say the
# same thing.
DESCRIPTIONS = {
    '40-chatgpt-v1': 'New to ChatGPT? This 27-page guide covers plans, '
                      'prompting, Projects and memory in plain English -- '
                      'plus what is replacing Custom GPTs now they are '
                      'being retired. No tech background needed.',
    '01-prompt-vault': '200 ready-to-use AI prompts across 10 everyday '
                        'categories. Fill-in-the-blank format, so you just '
                        'swap the words in brackets. Works with ChatGPT, '
                        'Claude and any assistant you already use.',
    '10-cheat-sheet-pack': '12 printable one-page cheat sheets for AI '
                            'tools. Light, ink-friendly design made for '
                            'actually printing and pinning above your '
                            'desk. Commands, prompts and settings at a '
                            'glance.',
    '02-starter-volume': 'Everything you need to start using Claude AI on '
                          'web, phone, desktop and in Chrome. 32 pages, '
                          'five guides, every step numbered. Plan '
                          'comparison included so you know what you are '
                          'paying for.',
    '11-cost-calculator': 'Enter your monthly usage and see what every '
                           'major AI model actually costs. Live formulas '
                           'over an editable rates tab, so it stays '
                           'accurate when vendors change pricing. Excel '
                           'and Google Sheets.',
    '12-start-here': 'Not sure which AI tool to learn first? This free '
                      '2-page roadmap maps four clear paths depending on '
                      'what you want to do. No cost, no signup maze. '
                      'Instant download.',
    '03-complete-library': 'All 23 field guides in one 140-page library. '
                            'Starts at what is an AI assistant and ends at '
                            'building your own automations. Six volumes, '
                            'linked contents, one download.',
    '20-copilot-v1': 'Copilot explained without the jargon: the three '
                      'products hiding behind one name, what each actually '
                      'costs, and how to install it in any editor. 24 '
                      'pages, every step numbered.',
    '30-codex-v1': 'Codex explained from scratch: installing it, the '
                    'commands that matter, and how its 5-hour rolling '
                    'usage window really works. 26 pages, plain English, '
                    'for people new to AI coding tools.',
}

# One sentence, high contrast, designed to stop a scroll. Traceable to the book.
HOOKS = {
    # EXPIRES 2026-12-11, when Custom GPTs stop running. Rewrite after that.
    '40-chatgpt-v1': 'Custom GPTs stop working\non 11 Dec 2026.',
    '12-start-here': 'Four AI tools.\nWhich one first?',
    '01-prompt-vault': 'Stop rewriting\nthe same prompt.',
    '10-cheat-sheet-pack': 'Print it once.\nStop googling it.',
    '02-starter-volume': 'You do not need\nto code to use AI.',
    '11-cost-calculator': 'What does AI\nactually cost you?',
    '03-complete-library': '23 guides.\nOne download.',
    '20-copilot-v1': 'Copilot is three\nproducts, not one.',
    '30-codex-v1': 'Codex resets every\n5 hours, not daily.',
}

# One concrete, immediately useful thing from the book.
TIPS = {
    '40-chatgpt-v1': 'Custom instructions are for who you are. Memory is for what '
                     'you are working on. Mixing them up is why ChatGPT forgets.',
    '12-start-here': 'Pick the tool that matches the job you actually have, not the '
                     'one with the loudest launch.',
    '01-prompt-vault': 'Everything you need to change is in [BRACKETS]. Swap those, '
                       'leave the rest alone.',
    '10-cheat-sheet-pack': 'Printed on a light background on purpose -- a dark PDF '
                           'costs a fortune in ink.',
    '02-starter-volume': 'Free, Pro and Max differ by usage limits more than by '
                         'features. Check limits before you upgrade.',
    '11-cost-calculator': 'Cached input costs about a tenth of fresh input. Reusing '
                          'a prompt is cheaper than rewriting it.',
    '03-complete-library': 'Start at volume one even if you are technical -- the '
                           'plan and pricing chapters apply to everyone.',
    '20-copilot-v1': 'Code completions are unmetered on every paid plan. Chat and '
                     'agent mode are not.',
    '30-codex-v1': 'The usage window is 5 hours rolling, so a heavy morning frees '
                   'up by mid-afternoon.',
}

# Two-column rows. A SKU absent here is SKIPPED by the comparison template --
# never padded with `included`, which is a file manifest, not a comparison.
COMPARISONS = {
    '40-chatgpt-v1': [('Free', '$0'), ('Go', '$8'), ('Plus', '$20'),
                      ('Pro', '$100 / $200')],
    '02-starter-volume': [('Free', 'Limited usage'), ('Pro', 'More usage'),
                          ('Max', 'Highest usage')],
    '20-copilot-v1': [('Completions', 'Unmetered'), ('Chat', 'Uses credits'),
                      ('Agent mode', 'Uses credits')],
}


def sku_record(sku):
    return next(s for s in _kit.SKUS if s['sku'] == sku)


def _etsy_url(sku):
    """The listing's URL, but only once the local db records it as live.

    Etsy listings expire after four months and `--status` writes the
    resulting state back to the db, so an existing row's `url` column can
    outlive the listing it points at. Only `state == 'active'` means the
    listing is actually there.
    """
    r = _edb.get(sku) or {}
    if r.get('state') != 'active':
        return ''
    return r.get('url') or ''


def _gumroad_url(sku):
    """The product's URL, but only once the local db records it as published."""
    r = _gp.get(sku) or {}
    if not r.get('published'):
        return ''
    return r.get('url') or ''


def url_for(sku):
    """Etsy first, Gumroad second. A pin pointing nowhere is worse than no pin."""
    u = _etsy_url(sku) or _gumroad_url(sku)
    if not u:
        raise KeyError('%s resolves to no live listing on either channel' % sku)
    return u


def palette_key_for(sku):
    """The series palette for this SKU, via the covers catalogue."""
    from covers import catalogue
    return catalogue.palette_for(sku_record(sku))
