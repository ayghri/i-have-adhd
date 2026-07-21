#!/usr/bin/env node
// SessionStart hook — injects the full i-have-adhd ruleset when always-on
// mode is enabled. Opt-in via flag file, so installing the plugin changes
// nothing until you ask for it:
//
//   touch ~/.claude/.i-have-adhd-always    # enable
//   rm ~/.claude/.i-have-adhd-always       # disable
//
// Honors $CLAUDE_CONFIG_DIR. Never blocks session start: any failure exits 0.

const fs = require('fs');
const os = require('os');
const path = require('path');

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = path.join(claudeDir, '.i-have-adhd-always');

try {
  if (!fs.existsSync(flagPath)) process.exit(0);

  const skillPath = path.join(__dirname, '..', 'skills', 'i-have-adhd', 'SKILL.md');
  const body = fs
    .readFileSync(skillPath, 'utf8')
    .replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ''); // strip YAML frontmatter

  console.log(
    'ADHD MODE ACTIVE (always-on) — the ruleset below applies to every response. ' +
      '"stop adhd mode" turns it off for this session; ' +
      `delete ${flagPath} to turn always-on off for good.\n\n${body}`
  );
} catch {
  process.exit(0);
}
