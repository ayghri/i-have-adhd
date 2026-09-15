# ADR 0005: Conditions on a domain backbone

**Status:** accepted 2026-08-24

## Context

Two framings compete for organizing the family. **Condition labels** (dyslexia, autism…) match how people search and self-describe, but real readers are **spiky** — a profile is a shape across cognitive domains (working memory, processing speed, attention…), not a pure diagnosis, and two conditions can share a trough (ADHD and brain fog both tax working memory). A condition-only family would restate the same domain rules repeatedly with no shared vocabulary.

## Decision

- **Surface by condition, internals by domain.** Skills are named and invoked by condition (discoverability), but inside each skill the rules are grouped under domain headings (`### Working memory`, `### Language`, …) and `docs/DOMAINS.md` is the single taxonomy: per domain — what a peak looks like, what a trough looks like, the functional impact on reading agent output, and the normal (statistical) vs expected (age/role) distinction.
- Domains compose; conditions are curated bundles of domain rules. Rule overlap between conditions is a feature (same trough, same fix), stated in shared vocabulary.
- `docs/GLOSSARY.md` fixes the leading words: *spiky profile*, *domain*, *condition bundle*, *normal vs expected*.

## Consequences

- Later pure-domain skills reuse the taxonomy verbatim; no restructuring.
- SOURCES.md and each rule's `Source:` line can reference domains, so one citation grounds the same rule in several skills.
- DOMAINS.md is load-bearing: adding a domain is an ADR-level change, not a casual edit.
