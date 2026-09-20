"""Content for the Cheat Sheet Pack — single source, so a fact is fixed in one place.

Every sheet is one printed page. Keep rows short: this renders at 9pt in two columns on
a light background, and `verify_no_overflow()` in the build script hard-fails on anything
that would run past the column.

Facts here were verified against code.claude.com/docs and the vendor pricing pages during
the 2026-07-30 correctness pass. The known-error list in CLAUDE.md is fixed in this data —
do not re-import the old values from the guide scripts.
"""

# Each sheet: title, subtitle, and blocks. A block is (heading, [(left, right), ...]).
SHEETS = [
    dict(
        title='Claude Code — Slash Commands',
        sub='Type these at the Claude Code prompt',
        blocks=[
            ('Session', [
                ('/help', 'List commands and usage'),
                ('/clear', 'Wipe the conversation and start fresh'),
                ('/compact', 'Summarise context — 60-80% token reduction'),
                ('/status', 'Session info, model, token usage'),
                ('/cost', 'Spend so far this session'),
                ('/doctor', 'Diagnose installation problems'),
            ]),
            ('Setup', [
                ('/terminal-setup', 'Configure terminal key bindings'),
                ('/plugins', 'Browse and manage plugins'),
                ('/skills', 'List available skills'),
                ('/config', 'Open settings'),
            ]),
            ('Control', [
                ('Escape', 'Cancel the current run mid-flight'),
                ('Ctrl+C', 'Interrupt'),
                ('--max-turns N', 'Hard cap on agentic iterations'),
                ('!<command>', 'Run a shell command in the session'),
            ]),
        ],
    ),
    dict(
        title='Claude Code — Hooks',
        sub='Automation that runs deterministically, not by persuasion',
        blocks=[
            ('Exit codes — this is what most people get wrong', [
                ('exit 0', 'Success. stdout parsed as JSON if present'),
                ('exit 2', 'BLOCKING. stderr is fed back to Claude'),
                ('exit 1 or other', 'Non-blocking error — execution CONTINUES'),
            ]),
            ('Core events', [
                ('SessionStart / SessionEnd', 'Session opens / terminates'),
                ('UserPromptSubmit', 'You submit a prompt, before Claude sees it'),
                ('PreToolUse', 'Before a tool call executes'),
                ('PostToolUse', 'After a tool call succeeds'),
                ('PostToolUseFailure', 'After a tool call fails'),
                ('Stop', 'Claude finishes responding'),
                ('StopFailure', 'Turn ends due to an API error'),
                ('Notification', 'Claude Code sends a notification'),
            ]),
            ('Input and config', [
                ('Input arrives on', 'stdin as JSON — NOT arguments or env vars'),
                ('Read a file path', "jq -r '.tool_input.file_path'"),
                ('Env var that exists', 'CLAUDE_PROJECT_DIR'),
                ('Shared config', '.claude/settings.json'),
                ('Personal config', '.claude/settings.local.json'),
                ('Default timeout', '60 seconds per hook command'),
            ]),
        ],
    ),
    dict(
        title='CLAUDE.md — Build Plans That Work',
        sub='Auto-loaded into context every session',
        blocks=[
            ('Locations, most general first', [
                ('~/.claude/CLAUDE.md', 'Global — applies to every project'),
                ('./CLAUDE.md', 'Project root — checked into the repo'),
                ('./sub/CLAUDE.md', 'Subdirectory override — most specific wins'),
            ]),
            ('Six sections worth having', [
                ('Tech Stack', 'Languages, frameworks, versions'),
                ('Commands', 'Build, test, lint, run — exact invocations'),
                ('Architecture', 'How the pieces fit, where things live'),
                ('Conventions', 'Naming, style, patterns to match'),
                ('Boundaries', 'What not to touch, what needs asking'),
                ('Build Rules', 'Numbered, checkable, unambiguous'),
            ]),
            ('Rules of thumb', [
                ('Length', 'Under ~200 lines — it costs tokens every turn'),
                ('Detail', 'Link out to detail files, do not inline them'),
                ('Reliability', 'Advisory (~70-90%). Hooks are deterministic'),
                ('Test', 'If it is critical, enforce it with a hook instead'),
            ]),
        ],
    ),
    dict(
        title='MCP Servers — Install & Config',
        sub='Model Context Protocol: tools, resources and prompts',
        blocks=[
            ('Config file locations', [
                ('Mac (Desktop)', '~/Library/Application Support/Claude/'),
                ('', 'claude_desktop_config.json'),
                ('Windows (Desktop)', '%APPDATA%\\Claude\\claude_desktop_config.json'),
                ('Claude Code (project)', '.claude/settings.json -> "mcpServers"'),
                ('Claude Code (global)', '~/.claude.json -> "mcpServers"'),
                ('After editing', 'Restart the app — configs load at startup'),
            ]),
            ('Current reference servers', [
                ('filesystem', '@modelcontextprotocol/server-filesystem'),
                ('memory', '@modelcontextprotocol/server-memory'),
                ('sequential-thinking', 'Structured multi-step reasoning'),
                ('fetch / git / time', 'Other maintained reference servers'),
            ]),
            ('Vendor servers moved — old packages are archived', [
                ('GitHub', 'ghcr.io/github/github-mcp-server (Docker)'),
                ('', 'or hosted at api.githubcopilot.com/mcp/'),
                ('Brave Search', '@brave/brave-search-mcp-server'),
                ('Do NOT use', '@modelcontextprotocol/server-github'),
                ('Do NOT use', '@modelcontextprotocol/server-brave-search'),
            ]),
            ('Three primitives', [
                ('Tools', 'Actions the model can take'),
                ('Resources', 'Read-only data it can pull in'),
                ('Prompts', 'Reusable templates'),
            ]),
        ],
    ),
    dict(
        title='Model IDs & Pricing',
        sub='Per million tokens. Verify before relying on it — this moves.',
        blocks=[
            ('Anthropic API', [
                ('Haiku 4.5', 'claude-haiku-4-5-20251001'),
                ('Sonnet 4.6', 'claude-sonnet-4-6'),
                ('Opus 4.8', 'claude-opus-4-8'),
            ]),
            ('Indicative rates (input / output)', [
                ('Haiku 4.5', '$1 / $5'),
                ('Sonnet 4.6', '$3 / $15'),
                ('Opus 4.8', '$5 / $25'),
            ]),
            ('Discounts that actually matter', [
                ('Prompt cache hit', '~90% off the input price'),
                ('Cache write', 'Costs more than a normal input token'),
                ('Message Batches', '50% off, async, up to 24h turnaround'),
                ('Model routing', 'Cheapest model that clears the bar'),
            ]),
            ('Where the money goes', [
                ('Output tokens', 'Priced 3-5x input — brevity is the lever'),
                ('Context regrowth', 'Every turn resends the conversation'),
                ('Long agentic runs', 'Context compounds — /compact resets it'),
                ('Retries', 'A failed run still bills for what it produced'),
            ]),
        ],
    ),
    dict(
        title='Prompting — Structure & Technique',
        sub='What reliably changes output quality',
        blocks=[
            ('Five parts of a prompt', [
                ('Role', 'What kind of expert is answering'),
                ('Task', 'The specific job, stated plainly'),
                ('Context', 'The raw material — data, code, text'),
                ('Constraints', 'Scope, length, tone, what not to do'),
                ('Output Format', 'Exactly how the answer should look'),
            ]),
            ('XML tags — the most reliable structuring method', [
                ('<instructions>', 'Keeps directions separate from data'),
                ('<context>', 'Background or source material'),
                ('<example>', 'Few-shot examples — repeat the tag'),
                ('<thinking>', 'Reasoning, kept out of the answer'),
                ('<answer>', 'The final result, clearly marked'),
                ('<format>', 'The output structure you want'),
            ]),
            ('Techniques', [
                ('Few-shot', '3-5 examples calibrate tone and shape'),
                ('Chain-of-thought', '+19 points on hard reasoning tasks'),
                ('CoT exception', 'Skip it for extended-thinking models'),
                ('Negatives', 'Say what to avoid, not only what to do'),
                ('Length', '~150-300 words is the useful range'),
                ('Iterate', 'Fix the prompt, not the output'),
            ]),
        ],
    ),
    dict(
        title='Agentic Loops & Cost Control',
        sub='How the loop runs and every way it stops',
        blocks=[
            ('The loop', [
                ('1. Receive', 'Task or tool result arrives'),
                ('2. Evaluate', 'Decide the next action'),
                ('3. Tool call', 'Read, Write, Edit, Bash, Grep, Agent...'),
                ('4. Decide', 'Continue or stop'),
            ]),
            ('Stopping conditions', [
                ('Task complete', 'The model decides it is done'),
                ('--max-turns N', 'Hard iteration cap'),
                ('max_budget_usd', 'Spend ceiling'),
                ('Hook exit 2', 'A PreToolUse hook blocks the call'),
                ('Escape', 'You interrupt'),
            ]),
            ('Keeping the bill down', [
                ('/compact', 'Summarise context, 60-80% reduction'),
                ('/cost and /status', 'Check before you are surprised'),
                ('Explicit done criteria', 'Vague tasks run long'),
                ('Smaller model', 'Route mechanical work to Haiku'),
                ('Scope the task', 'Narrow beats broad for both cost and quality'),
            ]),
        ],
    ),
    dict(
        title='Claude Skills',
        sub='Folders of instructions Claude loads on demand',
        blocks=[
            ('Anatomy', [
                ('Location', '~/.claude/skills/<skill-name>/'),
                ('Required file', 'SKILL.md'),
                ('Format', 'YAML frontmatter + markdown body'),
            ]),
            ('Frontmatter fields', [
                ('name', 'Short kebab-case identifier'),
                ('description', 'THE TRIGGER — be specific, not vague'),
                ('allowed-tools', 'Restrict what the skill may call'),
                ('disable-model-invocation', 'Manual-only invocation'),
            ]),
            ('Practice', [
                ('Trigger quality', 'Name concrete nouns and verbs users type'),
                ('Body length', 'Keep it tight — it costs tokens per turn'),
                ('Invoke', '/skills to list, /<name> to run'),
                ('Create one', 'Ask Claude to "create a new skill"'),
            ]),
        ],
    ),
    dict(
        title='Git — The Commands You Actually Use',
        sub='For people who did not come from a terminal',
        blocks=[
            ('Daily', [
                ('git status', 'What has changed'),
                ('git add .', 'Stage everything'),
                ('git commit -m "..."', 'Save a checkpoint with a message'),
                ('git push', 'Send commits to the remote'),
                ('git pull', 'Fetch and merge remote changes'),
                ('git log --oneline', 'Compact history'),
            ]),
            ('Branching', [
                ('git switch -c name', 'Create and move to a new branch'),
                ('git switch main', 'Move back'),
                ('git merge name', 'Bring a branch into this one'),
            ]),
            ('Getting out of trouble', [
                ('git restore <file>', 'Discard uncommitted changes to a file'),
                ('git reset --soft HEAD~1', 'Undo last commit, keep the work'),
                ('git stash / git stash pop', 'Park changes, get them back'),
                ('git diff', 'See exactly what changed'),
            ]),
            ('Glossary', [
                ('repo', 'A project folder Git is tracking'),
                ('commit', 'A saved snapshot with a message'),
                ('branch', 'A parallel line of work'),
                ('PR', 'A request to merge one branch into another'),
            ]),
        ],
    ),
    dict(
        title='Node.js, npm & Docker',
        sub='The setup commands, three platforms',
        blocks=[
            ('Verify an install', [
                ('node -v', 'Should print v24.x.x on current LTS'),
                ('npm -v', 'Should print 10.x.x or higher'),
                ('docker --version', 'Confirms Docker is on PATH'),
            ]),
            ('nvm — version switching', [
                ('nvm install lts', 'Install the current LTS'),
                ('nvm use lts', 'Switch to it'),
                ('nvm ls', 'List what is installed'),
                ('Windows', 'Use nvm-windows — a separate project'),
            ]),
            ('Docker essentials', [
                ('docker pull <image>', 'Download an image'),
                ('docker run <image>', 'Start a container'),
                ('docker ps', 'List running containers'),
                ('docker stop <id>', 'Stop one'),
                ('docker logs <id>', 'See its output'),
                ('docker compose up', 'Start everything in the compose file'),
            ]),
            ('npm', [
                ('npm install', 'Install this project dependencies'),
                ('npm install -g <pkg>', 'Install a tool globally'),
                ('npx <pkg>', 'Run a package without installing it'),
            ]),
        ],
    ),
    dict(
        title='Claude Plans & Apps',
        sub='Where Claude runs and what each tier gives you',
        blocks=[
            ('Where it runs', [
                ('Web', 'claude.ai — nothing to install'),
                ('Desktop', 'claude.ai/download — Mac and Windows'),
                ('Mobile', 'iOS App Store and Google Play'),
                ('Chrome', 'Extension — browsing agent, page summaries'),
                ('Terminal', 'Claude Code CLI — needs a paid plan or API key'),
            ]),
            ('Tiers, broadly', [
                ('Free', 'Chat, limited usage, no Claude Code'),
                ('Pro', 'Higher limits, Claude Code, code execution'),
                ('Max', 'Much higher limits, priority access'),
                ('Team / Enterprise', 'Seats, admin, shared projects'),
            ]),
            ('Shortcuts worth knowing', [
                ('Ctrl/Cmd + K', 'New chat'),
                ('Ctrl/Cmd + ,', 'Settings'),
                ('Drag a file in', 'Attach for analysis'),
                ('Projects', 'Persistent context across conversations'),
            ]),
        ],
    ),
    dict(
        title='Troubleshooting — Fast Fixes',
        sub='The failures that actually come up',
        blocks=[
            ('Claude Code', [
                ('Command not found', 'npm install -g @anthropic-ai/claude-code'),
                ('Auth loop', 'Check the plan — Claude Code needs a paid tier'),
                ('Anything odd', '/doctor first, it checks the obvious things'),
                ('Context feels lost', '/compact, or /clear for a clean start'),
                ('Runaway run', 'Escape. Then add --max-turns'),
            ]),
            ('Hooks', [
                ('Hook never fires', 'settings.json must be valid JSON — check it'),
                ('Command not found', 'Use absolute paths, not bare names'),
                ('Block does nothing', 'You need exit 2. exit 1 does not block'),
                ('Cannot read the file path', 'Parse stdin JSON with jq'),
            ]),
            ('MCP', [
                ('Server missing', 'Restart the app — config loads at startup'),
                ('Server fails to start', 'Run the npx command by hand, read the error'),
                ('Package 404s', 'Vendor servers moved — check the MCP sheet'),
                ('Node missing', 'Most servers need Node 18+ on PATH'),
            ]),
            ('API', [
                ('401', 'Key wrong, missing, or not in the environment'),
                ('429', 'Rate limited — back off exponentially'),
                ('529', 'Overloaded — retry'),
                ('400', 'Malformed request — check the model id first'),
            ]),
        ],
    ),
]
