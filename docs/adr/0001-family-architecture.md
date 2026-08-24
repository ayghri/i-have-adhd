# ADR 0001: Family of self-contained skills

**Status:** accepted 2026-08-24

## Context

Upstream ships one skill, `i-have-adhd`. The fork expands to several cognitive profiles. A repo can package many skills in `skills/`, but two shapes were possible: one router skill with profiles as internal reference files, or many self-contained skills, one directory each.

## Decision

The fork ships a **family of self-contained skills**: `skills/<condition>/SKILL.md`, one per profile, each loadable without its siblings.

## Consequences

- Any profile can be installed alone by copying its directory — personal-skill installs (e.g. `~/.zcode/skills/<name>/`) work with no packaging machinery.
- Each skill is invoked and discovered by its condition name (`/i-have-dyslexia`), which also carries the upstream naming identity.
- Rules shared across profiles are **duplicated** between skills. This is the accepted cost; ADR 0004 makes the duplication enforced rather than accidental.
- Every platform integration in this repo that discovers `skills/*` gets the whole family with no manifest changes.
