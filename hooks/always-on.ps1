# SessionStart hook fallback for Windows PowerShell. Injects the full
# i-have-adhd ruleset when the user has opted in by creating
# $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude).
# Never blocks session start: any failure exits 0.

try {
  # Look in every config dir the user could have created it in, not just one.
  # Claude Code supports a per-project CLAUDE_CONFIG_DIR, and a common setup
  # points it at a directory that symlinks settings.json/hooks/commands back to
  # ~/.claude without mirroring everything else. The flag then stays a real file
  # in ~/.claude, is never found, and this hook exits 0 — indistinguishable from
  # a deliberate opt-out. Measured on one such setup: 2,061 invocations of this
  # plugin, every one emitting zero bytes.
  $candidateDirs = New-Object System.Collections.Generic.List[string]
  if ($env:CLAUDE_CONFIG_DIR) { $candidateDirs.Add($env:CLAUDE_CONFIG_DIR) }
  $candidateDirs.Add((Join-Path ([Environment]::GetFolderPath("UserProfile")) ".claude"))
  if ($env:XDG_CONFIG_HOME) { $candidateDirs.Add((Join-Path $env:XDG_CONFIG_HOME "claude")) }

  $flagPath = $null
  foreach ($candidateDir in $candidateDirs) {
    $candidate = Join-Path $candidateDir ".i-have-adhd-always"
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
      $flagPath = $candidate
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
