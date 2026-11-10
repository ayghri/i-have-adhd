# Load always-on rules only in Human sessions, and skip when unsure

Always-on injection now loads the rules only when a person reads the session's replies as they arrive (a Human session), not in sessions whose output goes to an agent, a file or a later reader (a Non-human session), because the ADHD formatting rules distort worker reports, handoffs and other skills' required formats. When an agent gives no reliable signal, the injector skips injection and shows a one-line notice, and the `SKILL.md` scope clause is the backstop for anything detection misses.

## Considered options

- **Inject everywhere and rely on the scope clause alone.** This was rejected because a model told to apply rules "only to humans" still sees them in every context, and worker sessions in orchestrators such as Orca and Herdr look the same as human ones.
- **Have orchestrators mark their workers.** This is kept only as an opt-out (`I_HAVE_ADHD=0`), because some orchestrators, such as Orca's `worker-start`, offer no way to set a worker's environment.
- **Look up orchestrator state from the hook.** This was rejected because it would tie a public skill to particular tools.

## Consequences

- **OpenCode is an exception.** It gives plugins no signal that separates `opencode run` from the TUI, so top-level OpenCode sessions are assumed human and subagents are skipped. On V1 a toast says the session was assumed human.
- **Some human sessions go without the rules.** These are sessions on agents or versions without a signal. The user sees the notice and can run `/i-have-adhd`.
- **The rules depend on undocumented signals.** These include `CLAUDE_CODE_SESSION_ATTENDED` and the Codex parent process arguments. An agent upgrade can change them, and when that happens the result falls into the "unclear" case rather than wrongly injecting the rules.
