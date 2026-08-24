# ADR 0003: Strict source tracing

**Status:** accepted 2026-08-24

## Context

Output-shaping rules for cognitive profiles can drift into invented pop-psychology. Upstream credits Ramsay & Rostain for its ADHD basis. The fork needs the same defensibility for every new profile.

## Decision

1. Every rule in every new skill carries a `Source:` line naming the published guidance it derives from (section-level where the source has sections, e.g. W3C COGA §4.4.9).
2. A rule with no published basis is labeled `Source: synthesis` — an honest authorial claim, never a fake citation.
3. Master list of sources with URLs and access dates lives in `docs/SOURCES.md`; per-rule lines cite by short name.
4. SEO-blog-tier sources are excluded. Strong tier only: standards bodies (W3C), clinical/professional bodies (BDA, NAS, RCSLT), academic literature (PMC), and major clinical institutions.
5. Upstream `skills/i-have-adhd/SKILL.md` stays **byte-identical** to upstream: merge-friendly, and its existing Ramsay & Rostain credit stands. New skills copy its skeleton but are not edits to it.

## Consequences

- Rules are auditable: `SOURCES.md` → rule → citation.
- `synthesis` rules are visible as the fork's own judgment and can be grilled independently.
- Upstream merges keep applying cleanly to the ADHD skill.
