# SessionStart hook fallback for Windows PowerShell. Injects the full
# i-have-adhd ruleset at the start of every session once always-on is turned
# on. Off by default. Any one of these turns it on: the flag file
# $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude), the plugin option
# "always_on" (exported to hooks as CLAUDE_PLUGIN_OPTION_ALWAYS_ON), or the
# environment variable I_HAVE_ADHD_ALWAYS_ON. $CLAUDE_CONFIG_DIR/.i-have-adhd-off
# wins over all. Never blocks session start: any failure exits 0.

try {
  $claudeDir = if ($env:CLAUDE_CONFIG_DIR) {
    $env:CLAUDE_CONFIG_DIR
  } else {
    Join-Path ([Environment]::GetFolderPath("UserProfile")) ".claude"
  }
  $offPath = Join-Path $claudeDir ".i-have-adhd-off"
  $alwaysPath = Join-Path $claudeDir ".i-have-adhd-always"

  # Explicit opt-out wins over every way of opting in.
  if (Test-Path -LiteralPath $offPath -PathType Leaf) {
    exit 0
  }

  function Test-Truthy([string]$value) {
    if ($null -eq $value) { return $false }
    return @("1", "true", "yes", "on") -contains $value.Trim().ToLowerInvariant()
  }
  $enabled = (Test-Path -LiteralPath $alwaysPath -PathType Leaf) -or
    (Test-Truthy $env:CLAUDE_PLUGIN_OPTION_ALWAYS_ON) -or
    (Test-Truthy $env:I_HAVE_ADHD_ALWAYS_ON)
  if (-not $enabled) {
    exit 0
  }

  # Also silent when settings.json selects the plugin's output style: the
  # rules are already in the system prompt (with or without a plugin prefix).
  $settingsPath = Join-Path $claudeDir "settings.json"
  if (Test-Path -LiteralPath $settingsPath -PathType Leaf) {
    $settings = [System.IO.File]::ReadAllText($settingsPath)
    if ($settings -match '"outputStyle"\s*:\s*"([^"]*:)?i-have-adhd"') {
      exit 0
    }
  }

  $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  $skillPath = Join-Path $scriptDir "../skills/i-have-adhd/SKILL.md"
  if (-not (Test-Path -LiteralPath $skillPath -PathType Leaf)) {
    exit 0
  }

  $lines = [System.IO.File]::ReadAllLines($skillPath)
  $bodyStart = 0

  if ($lines.Length -gt 0 -and $lines[0] -match '^---\s*$') {
    # Only treat the block as frontmatter when the closing delimiter exists;
    # an unterminated fence is not frontmatter, so keep the whole file.
    for ($i = 1; $i -lt $lines.Length; $i++) {
      if ($lines[$i] -match '^---\s*$') {
        $bodyStart = $i + 1
        break
      }
    }
  }

  $body = if ($bodyStart -lt $lines.Length) {
    [string]::Join([Environment]::NewLine, $lines[$bodyStart..($lines.Length - 1)])
  } else {
    ""
  }

  $banner = 'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. ' +
    '"stop adhd mode" turns it off for this session; create '
  [Console]::Out.Write($banner + $offPath + " to turn always-on off for good.`n`n" + $body + "`n")
} catch {
  # Never block session start.
  exit 0
}
