# SessionStart hook fallback for Windows PowerShell. Injects the full
# i-have-adhd ruleset when the user has opted in by creating a
# .i-have-adhd-always flag in the active host's config directory
# (Claude: CLAUDE_CONFIG_DIR or ~/.claude; Codex: CODEX_HOME or ~/.codex).
# Never blocks session start: any failure exits 0.

try {
  $profileDir = [Environment]::GetFolderPath("UserProfile")
  $configDirs = if ($env:CLAUDE_CONFIG_DIR) {
    @($env:CLAUDE_CONFIG_DIR)
  } elseif ($env:CODEX_HOME) {
    @($env:CODEX_HOME)
  } else {
    @(
      (Join-Path $profileDir ".claude")
      (Join-Path $profileDir ".codex")
    )
  }
  $flagPath = $null
  foreach ($configDir in $configDirs) {
    $candidateFlagPath = Join-Path $configDir ".i-have-adhd-always"
    if (Test-Path -LiteralPath $candidateFlagPath -PathType Leaf) {
      $flagPath = $candidateFlagPath
      break
    }
  }

  if (-not $flagPath) {
    exit 0
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
    '"stop adhd mode" turns it off for this session; delete '
  [Console]::Out.Write($banner + $flagPath + " to turn always-on off for good.`n`n" + $body + "`n")
} catch {
  # Never block session start.
  exit 0
}
