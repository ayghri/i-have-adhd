# Unified installation manager

Run from a reviewed checkout with **Python 3.11+**. No pip packages, network
requests, agent CLI execution, background processes or npm publication are needed.
Existing native/plugin installation methods in [INSTALL.md](INSTALL.md) remain valid.

## Commands

```sh
python scripts/manage_install.py list
python scripts/manage_install.py install --agent claude --agent codex --user --mode always-on
python scripts/manage_install.py install --agent claude --agent codex --user --mode always-on --apply
python scripts/manage_install.py status --agent claude --agent codex --user
python scripts/manage_install.py update --agent claude --agent codex --user --apply
python scripts/manage_install.py uninstall --agent claude --agent codex --user --apply
python scripts/manage_install.py export
```

For a project, replace `--user` with `--project ./your-project`; the directory must
already exist. Omit `--apply` to preview any mutation, including update and removal.
Repeated `--agent` selects multiple agents; duplicated selections are ignored.
Install defaults to `--mode on-demand`. Re-run install with the other mode to
transition. Update keeps the recorded mode and reads the current checkout;
it never pulls or upgrades other packages. Export prints the complete canonical
Markdown body without YAML frontmatter. Use the original
[SKILL.md](skills/i-have-adhd/SKILL.md) for interfaces requiring skill metadata.

Exit codes: **0** completed/previewed, **1** conflict or error, **2** manual work
or an unsupported combination remains. A batch keeps successful agents and
reports individual failures. Status checks managed hashes, not model behavior,
and cannot establish the absence of native/UI installations.

## Coverage

A = automatic file management for install/update/uninstall/status.
G = guided, no installation mutation. U = unsupported mode/scope; portable export
is available without promising equivalent activation.
Columns describe this manager, not every capability of the agent itself.

| Agent | Project: on-demand / always-on | User: on-demand / always-on |
| --- | --- | --- |
| Antigravity | U / U | G / A |
| AstronClaw | G / U | G / U |
| Claude Code | A / A | A / A |
| Codex | A / A | A / A |
| Gemini CLI | G / G | A / A |
| GitHub Copilot | A / A | A / G |
| Hermes | G / A | A / G |
| Kimi Code CLI | G / U | G / U |
| OpenCode | A / G | A / A |
| Pi | U / U | G / G |
| Oh My Pi (OMP) | U / U | G / U |
| Qwen Code | U / U | G / U |
| Zed | G / G | A / A |
| Cursor | A / A | A / G |
| Amp | G / U | G / U |
| Generic | G / G | G / G |

Guided native/UI routes deliberately stay under their original installer:
this script cannot hash or safely undo changes inside an opaque package store.
It prints the source file, relevant procedure and missing CLI dependency.
It does not install that dependency, execute displayed commands, import through
a UI, or record manual work as completed. The proposed v1 therefore automates
filesystem routes, not native package-manager mutations.

## Automatic destinations

All paths below are relative to the selected project or user home. The preview
prints absolute destinations before applying. Automatic skill routes copy the
whole canonical skill directory, including its agent metadata.

| Agent | Project on-demand | User on-demand | Project always-on | User always-on |
| --- | --- | --- | --- | --- |
| Antigravity | — | — | — | .gemini/GEMINI.md |
| Claude Code | .claude/skills/i-have-adhd/ | .claude/skills/i-have-adhd/ | CLAUDE.md | .claude/CLAUDE.md |
| Codex | .agents/skills/i-have-adhd/ | .agents/skills/i-have-adhd/ | AGENTS.md | .codex/AGENTS.md |
| Gemini CLI | — | .gemini/commands/i-have-adhd.toml | — | .gemini/GEMINI.md |
| Copilot | .github/skills/i-have-adhd/ | .copilot/skills/i-have-adhd/ | .github/copilot-instructions.md | — |
| Hermes | — | .hermes/skills/i-have-adhd/ | AGENTS.md | — |
| OpenCode | .agents/skills/i-have-adhd/ | .agents/skills/i-have-adhd/ | — | .config/opencode/AGENTS.md |
| Zed | — | .agents/skills/i-have-adhd/ | — | .config/zed/AGENTS.md |
| Cursor | .cursor/skills/i-have-adhd/ | .cursor/skills/i-have-adhd/ | .cursor/rules/i-have-adhd.mdc | — |

These are standalone skill/instruction routes, not native plugin installations.
Claude always-on uses its documented CLAUDE.md mechanism, so no hook is required.
Gemini's TOML prompt is generated from the full canonical body. Cursor's project
rule uses `alwaysApply: true`. Other persistent Markdown files receive a
delimited managed block. Always-on installs persistent instructions rather than
a second on-demand copy; transitioning removes only the previous owned content.

Shared paths are shared in the agent too: an AGENTS.md block or .agents skill may
be discovered by other agents using the same directory. Selecting one agent
cannot make a shared instruction file private to it. Native plugins, other
scopes, or manual rules may also affect activation. Start a new session after
changing mode and verify behavior yourself. Hermes invocation has an open
[documentation issue #118](https://github.com/ayghri/i-have-adhd/issues/118);
filesystem presence does not resolve that issue.

Path references: the existing INSTALL.md file, [Claude skills](https://code.claude.com/docs/en/skills),
[Claude memory](https://code.claude.com/docs/en/memory), and
[Codex skills](https://developers.openai.com/codex/skills).
When known configuration overrides (such as CODEX_HOME, CLAUDE_CONFIG_DIR or
XDG_CONFIG_HOME) are set, user-scope operations fall back to guidance without
reading or changing the default destination. Custom configuration locations are not migrated; use the guided instructions
when the default destinations are not the ones your agent loads.

## Ownership, conflicts and recovery

The scope-local `.i-have-adhd-install/manifest.json` records modes, relative
destinations, SHA-256 hashes, block separators and owners. It stores no credentials.
Do not edit the manifest to adopt an existing installation. Back up or reconcile
an existing manual/native installation using its documented method first.

A pre-existing skill/file is not overwritten, even if its contents match.
Unmanaged i-have-adhd blocks are not duplicated. Shared Markdown preserves bytes
outside the managed markers, including CRLF and subsequent external edits.
Edited or missing managed content blocks update, mode transition and removal.
Extra files added to a skill directory are preserved. Empty directories and the
empty ownership manifest may remain after removal.

Shared resources are written once and kept until their final owner is removed.
When updating changed shared rules, select all their recorded owners in the same
command. A later agent failure does not roll back earlier successful agents.

Each agent is preflighted before writing. Files and the manifest use atomic
replacement; ordinary write failures restore previously changed files for that
agent. Concurrent installer runs are rejected using a scope-local lock. Stop
editors/other writers while applying; this is not a filesystem-wide transaction.
Abrupt termination may leave a lock and partial files: review those destinations
and restore from your backup before removing the stale lock and retrying.
Do not delete a live run's lock. Symlink/junction descendants, hard-linked files,
out-of-scope manifest destinations and files over 4 MiB are rejected.

## Verification

```sh
python -m unittest tests.test_manage_install -v
python -m unittest discover -s tests -v
python scripts/run_evals.py validate
git diff --check
```

Installer tests use temporary roots; native tools are not required. The added
workflow runs the installer suite on Windows, Linux and macOS. CI results must
be observed before claiming those platforms passed. No paid model calls are made,
and file roundtrips do not prove a particular agent loaded the rules.
