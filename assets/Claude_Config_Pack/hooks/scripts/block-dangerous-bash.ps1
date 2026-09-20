# PreToolUse hook for the Bash tool (Windows / PowerShell).
# Reads the hook payload from stdin and exits 2 to BLOCK the command.
# Install to .claude\hooks\block-dangerous-bash.ps1

$ErrorActionPreference = 'Stop'
$payload = $input | Out-String
if (-not $payload.Trim()) { exit 0 }
$cmd = ($payload | ConvertFrom-Json).tool_input.command
if (-not $cmd) { exit 0 }

$patterns = @(
  @{ re = 'rm\s+-[rf]{2}\s+[/~]';        why = 'recursive delete of a root path' },
  @{ re = 'git\s+push\b.*(--force|\s-f)'; why = 'force push' },
  @{ re = 'git\s+reset\s+--hard';         why = 'hard reset discards uncommitted work' },
  @{ re = 'git\s+clean\s+-\w*[fd]';       why = 'git clean would delete untracked files' },
  @{ re = '(DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE\s+)'; why = 'destructive SQL' },
  @{ re = 'chmod\s+-R\s+777';             why = 'world-writable permissions' },
  @{ re = '>>?\s*\.env';                  why = 'writing to .env' },
  @{ re = 'curl[^|]*\|\s*(sh|bash)';      why = 'piping a download straight into a shell' }
)

foreach ($p in $patterns) {
  if ($cmd -match $p.re) {
    [Console]::Error.WriteLine("BLOCKED by block-dangerous-bash hook: $($p.why)")
    [Console]::Error.WriteLine("If this is genuinely what you want, run it yourself in a terminal.")
    exit 2                      # exit 2 = block, stderr goes back to Claude
  }
}
exit 0
