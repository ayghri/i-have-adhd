# ADR 0004: Shared-core sync by tooling

**Status:** accepted 2026-08-24

## Context

ADR 0001 accepts duplicated shared sections across skills as the price of self-containment. Unchecked duplication drifts: a fix to "When to break the rules" in one skill silently misses its siblings.

## Decision

Three sections are **shared core** and must be textually identical across all family skills (upstream ADHD is the reference):

- `## Persistence`
- `## When to break the rules`
- `## Pre-send check`

Each skill's own mode word (`adhd`, `dyslexia`, `autism`, `anxiety`, `brain-fog`) may appear in the core; the checker normalizes the skill's own mode token to `<mode>` before comparing, so `"stop dyslexia mode"` and `"stop adhd mode"` compare equal.

`scripts/check_shared_core.py` extracts the sections from every `skills/*/SKILL.md`, normalizes, and diffs against the reference. `tests/test_shared_core.py` runs it, so the existing Python test suite fails on drift.

## Consequences

- Editing a core section requires editing it everywhere; the test names every file that drifted.
- A core fix is a mechanical copy, reviewable as such.
- Per-skill behavior beyond the core lives in the rules sections, which are free to differ.
