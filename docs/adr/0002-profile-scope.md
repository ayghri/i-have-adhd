# ADR 0002: Profile scope — wave 1

**Status:** accepted 2026-08-24

## Context

The fork's goal is output shaping for readers across the spectrum of learning, comprehension, and contextual difficulties. That population is larger than any one wave can cover well, and the strict source policy (ADR 0003) caps how fast profiles can be added honestly.

## Decision

Wave 1 ships four new profiles alongside untouched upstream ADHD:

| Skill | Profile |
|---|---|
| `i-have-adhd` | ADHD — upstream, byte-identical |
| `i-have-dyslexia` | Dyslexia — reading fluency / decoding |
| `i-have-autism` | Autism — literal language, predictability |
| `i-have-anxiety` | Anxiety — uncertainty tolerance |
| `i-have-brain-fog` | Brain fog — working memory, fatigue, fluctuation |

Chosen because each maps to a distinct trough cluster (see `docs/DOMAINS.md`), each has at least one strong published source, and together they exercise most domains in the taxonomy.

Later waves may add pure **domain** skills (e.g. `i-have-low-working-memory`) for readers who are spiky without a condition label; ADR 0005's backbone makes that an extension, not a restructure. Translated READMEs are out of scope for wave 1.

## Consequences

- Scope stays honest: every wave-1 rule traces or is labeled *synthesis*.
- Profiles not covered (dyscalculia, dyspraxia, depression, sensory-only, cognitive aging) have a documented home in DOMAINS.md for later waves.
