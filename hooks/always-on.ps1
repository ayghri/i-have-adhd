# SessionStart hook fallback for Windows PowerShell. Injects the full
# i-have-adhd ruleset when the user has opted in by creating
# $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude).
# Never blocks session start: any failure exits 0.
#
# Reads skills/i-have-adhd/rules.md verbatim: frontmatter parsing happens
# once, at build time, in scripts/generate_rules.mjs.
#
# The banner text is shared with the other two runtimes via banner.txt,
# which carries a {{FLAG_PATH}} placeholder that each runtime splices its
# own flag path into, instead of being hand-authored three times, once per
# runtime's string-escaping dialect.

try {
  $claudeDir = if ($env:CLAUDE_CONFIG_DIR) {
    $env:CLAUDE_CONFIG_DIR
  } else {
    Join-Path ([Environment]::GetFolderPath("UserProfile")) ".claude"
  }
  $flagPath = Join-Path $claudeDir ".i-have-adhd-always"

  if (-not (Test-Path -LiteralPath $flagPath -PathType Leaf)) {
    exit 0
  }

  $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  $rulesPath = Join-Path $scriptDir "../skills/i-have-adhd/rules.md"
  if (-not (Test-Path -LiteralPath $rulesPath -PathType Leaf)) {
    exit 0
  }

  $body = [System.IO.File]::ReadAllText($rulesPath).TrimEnd("`r", "`n")

  $bannerTemplate = [System.IO.File]::ReadAllText((Join-Path $scriptDir "banner.txt")).TrimEnd("`r", "`n")
  $token = "{{FLAG_PATH}}"
  $tokenIndex = $bannerTemplate.IndexOf($token)
  $banner = $bannerTemplate.Substring(0, $tokenIndex) + $flagPath + $bannerTemplate.Substring($tokenIndex + $token.Length)
  [Console]::Out.Write($banner + "`n`n" + $body + "`n")
} catch {
  # Never block session start.
  exit 0
}
