# ADR 0006: Composable stack — domain skills stack on one condition skill

**Status:** accepted 2026-08-24

## Context

Wave 1 skills are one-at-a-time modes. ADR 0005 promised that domains compose ("conditions are curated bundles"), but until a pure-domain skill exists, nothing tests that promise. Wave 2 introduces `i-have-low-working-memory`, and a reader may need it *together with* a condition — say ADHD plus a working-memory trough on a bad day. Two modes on at once needs defined merge semantics, or the two Persistence sections contradict each other.

## Decision

1. **Two skill classes**, declared in frontmatter: `metadata.type: condition` (default — absent means condition, so upstream `i-have-adhd` stays untouched) and `metadata.type: domain`.
2. **Stack rule:** at most **one condition skill** plus **any number of domain skills** active at once. Invoking a second condition skill replaces the first (wave-1 behavior preserved).
3. **Merge semantics:** active rules are the **union**. When two rules conflict, the **stricter one wins** — stricter meaning the tighter constraint on output ("one instruction per message" overrides "number the steps").
4. **Stop phrases:** each skill ends only on its own `"stop <mode> mode"`. `"normal mode"` ends the entire stack, condition and domain alike (already present in every wave-1 Persistence section).
5. **Domain Persistence variant:** domain skills share a stacking-aware Persistence section (below). Condition skills keep the wave-1 core verbatim; `When to break the rules` and `Pre-send check` stay shared verbatim across **all** classes.

Domain Persistence variant (verbatim in every domain skill, mode token normalized):

> These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.
>
> This is a domain skill: it stacks with the one condition skill that may also be running. Apply both rulesets; where two rules conflict, the stricter one wins. Turning the condition skill off does not turn this one off.
>
> Turn this one off only when the reader says "stop \<mode\> mode" or "normal mode". Confirm in one line. "Normal mode" ends every active mode, condition and domain alike.

## Consequences

- `check_shared_core.py` becomes class-aware (ADR 0004 updated in spirit): conditions compare against upstream as before; domain skills compare against the first domain skill as reference.
- Wave-1 files require zero edits; upstream stays byte-identical.
- Readers can finally assemble a stack (`/i-have-adhd` + `/i-have-low-working-memory`) — the composition ADR 0005 promised.
