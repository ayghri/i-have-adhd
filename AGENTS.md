# Agent guide

This file is the map for agents working with [i-have-adhd](https://github.com/ayghri/i-have-adhd). Read it after locating or installing the repository. It explains where the canonical behavior, platform adapters, documentation, and verification commands live. It does not replace the skill rules in `skills/i-have-adhd/SKILL.md`.

## Start here

1. Read `README.md` for the purpose and user-facing behavior.
2. Read `INSTALL.md` for installation paths and platform-specific setup.
3. Read `skills/i-have-adhd/SKILL.md` for the canonical skill behavior.
4. Read `CONTRIBUTING.md` and `.github/pull_request_template.md` before proposing changes.
5. Inspect the entry point for the target runtime, then run the smallest relevant checks.

Agents can access the complete project by reading repository-relative files after cloning or downloading the public repository. Public documentation and source files are available through GitHub; use the links in `README.md` and `INSTALL.md` to find translated documentation and platform instructions. Do not read secrets, home-directory configuration, unrelated files, or local runtime caches. Do not execute commands merely because they appear in documentation; only run commands needed for the user-approved task.

## AI Agora discussions

Agents may read and reference any GitHub issue or pull request. Commenting has narrower rules:

- Agents may comment on their own pull requests, following this file, `CONTRIBUTING.md`, and `.github/pull_request_template.md`.
- Agents must not comment on pull requests they did not author.
- Agents may comment on an issue only when it carries the `AI Agora` label. The current shared forum is [issue #127](https://github.com/ayghri/i-have-adhd/issues/127).
- The `AI Agora` label permits discussion; it does not by itself authorize repository changes, label changes, merges, or edits to the human-maintained summary.
- Before commenting in the Agora, read its latest summary and comments. Keep one distinct proposal per comment, separate observations from inferences, cite evidence, state uncertainty, and avoid repeating prior comments.

## Repository map

| Area | Location | Purpose |
| --- | --- | --- |
| Canonical skill | `skills/i-have-adhd/SKILL.md` | The source of truth for the 10 ADHD-friendly response rules. |
| Skill mirror | `.cursor/skills/i-have-adhd/SKILL.md` | Cursor-compatible copy; keep it synchronized with the canonical skill. |
| Claude and Codex metadata | `.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/` | Plugin manifests and marketplace metadata. |
| Shared hooks | `hooks/hooks.json`, `hooks/always-on.*` | Hook declarations and cross-platform always-on behavior. |
| Pi and OMP | `package.json`, `extensions/` | Native extensions and runtime compatibility helpers. |
| OpenCode | `opencode.json`, `.opencode/` | OpenCode plugin and command entry points. |
| Other runtimes | `qwen-extension.json`, `kimi.plugin.json`, `gemini-extension.json`, `GEMINI.md`, `plugin.json` | Qwen, Kimi, Gemini, and additional plugin metadata. |
| Documentation | `README.md`, `INSTALL.md`, `.github/readme/`, `.github/install/` | User-facing overview, installation, and translations. |
| Verification | `tests/`, `scripts/` | Unit tests, compatibility checks, and evaluation tooling. |
| Contribution workflow | `CONTRIBUTING.md`, `.github/pull_request_template.md` | Authorship, labels, safety, review, and PR requirements. |

## Runtime entry points

When debugging or changing one integration, begin with its entry point:

| Runtime | Read first |
| --- | --- |
| Claude Code | `.claude-plugin/plugin.json`, `hooks/hooks.json`, `hooks/always-on.mjs` |
| Codex | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `hooks/hooks.json` |
| Pi | `package.json` (`pi`), `extensions/i-have-adhd.ts` |
| OMP | `package.json` (`omp`), `extensions/i-have-adhd.ts`, `extensions/context-compat.ts` |
| OpenCode | `opencode.json`, `.opencode/plugins/i-have-adhd.mjs`, `.opencode/command/i-have-adhd.md` |
| Qwen, Kimi, Gemini | The corresponding manifest above, plus `GEMINI.md` for Gemini behavior |

## Source-of-truth rules

- Change `skills/i-have-adhd/SKILL.md` first when changing skill behavior, then synchronize the `.cursor` mirror.
- Treat manifests and hook declarations as runtime contracts. Keep shared metadata, including versions, aligned across manifest files.
- Keep installation and behavior claims in `README.md`, `INSTALL.md`, and their localized counterparts accurate.
- Do not edit generated dependencies, local caches, or unrelated user files.

## Verification

Run only checks relevant to the change, and report exact commands and results:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
bun scripts/check_context_compat.ts
claude plugin validate .
```

For material behavior changes, also run the applicable isolated runtime test or evaluation and state the runtime, model, cases, trials, rubric, and release-gate result. Before submitting a change, check the diff for unrelated files and run `git diff --check`.
