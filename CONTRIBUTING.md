# Contributing

Thanks for improving **i-have-adhd**. Contributions from humans and coding agents are welcome. Keep changes understandable, reviewable, safe to run, and compatible with existing users.

## Authorship and provenance

Every pull request must select exactly one category:

- **Human-authored** — a human made the substantive implementation and text. Autocomplete, formatting, search, and minor suggestions do not make a contribution hybrid.
- **Autonomous agent-authored** — an agent made most substantive decisions and changes, with a human primarily providing the task and reviewing the result.
- **Hybrid** — a human and one or more agents both made substantive decisions or changes.

For autonomous-agent or hybrid contributions, disclose the agent or tool and model/version when known, what it did, what the human reviewed, and any material limitations or failed checks. Do not call generated work human-authored or independently verified when it was only reviewed by the same agent that produced it.

The submitting human remains accountable for the full diff. Before submission, read the changed files, remove unrelated generated changes, and verify the claims in the PR description.

## Labels

Use one label from each applicable group:

- **Target:** `Target:Integrations` for a CLI integration, `Target:Evals` for evaluation scripts, `Target:Rules` for skill rules, or `Target:Docs` for documentation and translations.
- **Author:** `Author:Human`, `Author:Hybrid`, or `Author:AI`, matching the authorship category above.
- **Workflow:** `bug` for defects, `enhancement` for new features, `issue` for general issue tracking, `question` when more information is needed, or `duplicate` when the issue or PR already exists.

Choose the labels that describe the change; do not use labels as a substitute for the PR description or provenance disclosure. Use `issue` only when no more specific workflow label applies.

## Scope and reviewability

Keep each PR focused. Avoid drive-by formatting, unrelated dependency changes, generated filler, and broad rewrites that make behavior changes difficult to inspect.

The PR description must explain:

1. what changed and why;
2. observable behavior before and after;
3. safety, compatibility, and side-effect considerations;
4. the exact verification performed.

Discuss large behavior changes, new integrations, new hooks, and potentially breaking changes in an issue first.

## Safety and side effects

Contributions must not weaken platform safeguards, override higher-priority instructions, conceal risky behavior, or encourage inaccurate claims.

Skill changes must stay focused on response structure and usability. Do not add instructions, examples, fixtures, or tests that tell an agent to:

- read or transmit credentials, tokens, environment variables, private files, or repository data;
- modify shell profiles, global Git configuration, editor settings, or unrelated agent configuration;
- bypass confirmation for destructive, privileged, production, or externally visible actions;
- silently install software, fetch and execute remote code, or create persistence;
- misrepresent medical information or imply that this skill diagnoses ADHD.

Installation, activation, validation, tests, and evaluations must be narrowly scoped and predictable. By default, repository code must not modify files outside the repository or a documented temporary directory, alter user configuration or credentials, publish or send data, require elevated privileges, perform irreversible actions, or leave background processes behind. Intentional writes outside the repository require explicit opt-in, documentation, a specific path, and an easy undo path.

## Hooks, scripts, and evaluations

Hooks run in user environments: keep them fast, bounded, fail-safe, opt-in, and free of unnecessary network access. Optional failures must not block agent startup.

Scripts and workflows must validate inputs and paths, avoid shell commands built from untrusted text, use temporary fixtures, avoid secrets and undeclared uploads, and use least privilege. New third-party actions, packages, CLIs, or network calls need a clear justification and data/permission description.

Evaluation code must not execute model output, access production systems or unrelated user files, perform externally visible actions, or create unbounded cost. Provider-backed evaluations need explicit budgets, recorded runner/model/CLI/cases/trials/rubric, and comparable conditions. Unit tests for eval code should use stubs and temporary files without network or paid model calls.

## Compatibility and breaking changes

Preserve existing installation methods, invocation names, file locations, opt-in behavior, and supported integrations unless a breaking change is explicitly accepted. Potentially breaking changes include moving the canonical skill, changing invocation or hook semantics, changing manifests or installation commands, and removing a supported platform.

A breaking change requires an issue, migration path, updated documentation, and a compatibility or deprecation plan. Prefer additive, staged changes.

`skills/i-have-adhd/SKILL.md` is canonical. When it changes, synchronize the Cursor copy:

```sh
cp skills/i-have-adhd/SKILL.md .cursor/skills/i-have-adhd/SKILL.md
cmp skills/i-have-adhd/SKILL.md .cursor/skills/i-have-adhd/SKILL.md
```

Review platform-specific manifests and documentation whenever shared names, descriptions, paths, or behavior change.

## Verification

Run relevant checks and include the commands and results in the PR. For Python and evaluation-harness changes:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
```

For behavior changes, add or update representative eval cases when needed, run paired baseline/candidate evaluations under the same conditions, and apply the release gate. For hook or plugin changes, verify loading in an isolated configuration directory. If a check was not run, say so and explain why; never invent results or treat inspection as execution.

## Documentation and checklist

Keep examples safe to copy: use harmless fixtures, explicit placeholders, and read-only previews. Never include real secrets, personal paths, production identifiers, or commands that could damage a reader's environment. Distinguish required behavior from suggestions and avoid unsupported medical, accessibility, platform, or performance claims.

A PR is ready when:

- one authorship category is selected and agent involvement is disclosed accurately;
- the full diff has been reviewed by a human contributor;
- the change is focused and free of unrelated generated edits;
- side effects, compatibility, costs, and verification are documented.

Maintainers may close PRs that conceal provenance, introduce unsafe behavior, lack verification, or make unplanned breaking changes.
