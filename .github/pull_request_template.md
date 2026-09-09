## Summary

<!-- What changed, why it is needed, and the observable behavior before and after. -->

## Authorship and provenance — select exactly one

- [ ] **Human-authored** — substantive implementation and text were produced by a human.
- [ ] **Autonomous agent-authored** — an agent planned and produced most of the substantive change.
- [ ] **Hybrid** — a human and one or more agents both made substantive contributions.

**Agent/tool and model/version:** <!-- Write “None” for human-authored PRs. -->

**Agent contribution:** <!-- Planning, code, tests, docs, review, or other work. -->

**Human verification:** <!-- What the submitting human personally reviewed and ran. -->

**Known limitations or uncertain results:** <!-- Write “None known” only after review. -->

## Labels

**Target label:** <!-- Select exactly one: Target:Integrations, Target:Evals, Target:Rules, or Target:Docs. -->

**Author label:** <!-- Select exactly one: Author:Human, Author:Hybrid, or Author:AI. -->

**Workflow labels:** <!-- Add applicable labels: bug, enhancement, issue, question, or duplicate. -->

## Safety and side effects

- [ ] The change does not access or expose secrets, private files, or unrelated user/repository data.
- [ ] Scripts, hooks, workflows, and evals are bounded and do not create surprising or irreversible side effects.
- [ ] No destructive, privileged, production, externally visible, or persistent action occurs without explicit user intent and appropriate safeguards.
- [ ] Network access, third-party code, permissions, and provider costs are minimized and documented.
- [ ] Prompt text, examples, and fixtures contain no hidden instructions that weaken safety or expand agent authority.

**Side effects, permissions, network access, and cost:**

<!-- State “None” when applicable; otherwise describe exact scope and rollback. -->

## Compatibility

- [ ] This is not a breaking change.
- [ ] This is a breaking change; it was discussed, and migration/deprecation documentation is included below.
- [ ] Canonical and mirrored skill files are synchronized when applicable.
- [ ] Relevant platform manifests and installation documentation were reviewed.

**Migration or rollback notes:**

## Verification

<!-- List only commands actually run and their results. Remove unrun examples. -->

<!-- Common checks, when relevant:
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
-->

- `<command>` — `<result>`

**Behavior evals:** <!-- Required for material skill-behavior changes; include runner/model/cases/trials/rubric and release-gate result. -->

## Final accountability

- [ ] I reviewed the complete diff, removed unrelated generated changes, and take responsibility for the submitted content.
- [ ] All failed, skipped, or unrun checks are disclosed above.
