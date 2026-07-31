#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT;
if (!pluginRoot) process.exit(0);

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = path.join(claudeDir, '.i-have-adhd-always');

if (!fs.existsSync(flagPath)) process.exit(0);

const skillPath = path.join(pluginRoot, 'skills', 'i-have-adhd', 'SKILL.md');
if (!fs.existsSync(skillPath)) process.exit(0);

const content = fs.readFileSync(skillPath, 'utf-8');

const body = content.replace(/^---[\s\S]*?---\n?/, '');

console.log(
  `ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "stop adhd mode" turns it off for this session; delete ${flagPath} to turn always-on off for good.\n`
);
console.log(body);
