# Changelog

- Nov-10, 2026 - 07:55 PM +08 - Release 0.5.1 loads always-on rules in the Codex TUI: a plain `codex` parent with no subcommand is now a human session, while `codex exec` (or `e`) stays non-human.
- Nov-10, 2026 - 07:55 PM +08 - Treat a Codex parent with no subcommand as the interactive TUI, keeping `--help`, `--version`, and malformed flag tails unclear.

- Nov-10, 2026 - 05:50 PM +08 - Evict OpenCode session cache on the real V2 session.deleted envelope.
- Nov-10, 2026 - 05:35 PM +08 - Drop redundant command token in Win32 fallback process parsing to correctly identify Codex parents.
- Nov-10, 2026 - 05:30 PM +08 - Consume OpenCode V2 event stream to evict deleted sessions from cache.
- Nov-10, 2026 - 05:25 PM +08 - Fail closed as unclear when OpenCode V1 session lookup returns an error object without data.
- Nov-10, 2026 - 05:20 PM +08 - Add support for Codex --local-provider and multi-value -i/--image flags in parent process classification.
- Nov-10, 2026 - 05:15 PM +08 - Isolate process executable path from command line arguments when identifying Codex parents.
- Nov-10, 2026 - 05:10 PM +08 - Evict OpenCode session cache entry when session.deleted event is received.
- Nov-10, 2026 - 05:05 PM +08 - Treat missing OpenCode session IDs as unclear and gate diagnostic logging with a once-flag.
- Nov-10, 2026 - 05:00 PM +08 - Look up OpenCode parent session via runtime API to skip subagents and fail closed on lookup error.
- Nov-10, 2026 - 04:27 PM +08 - Correct Herdr worker opt-out documentation to export I_HAVE_ADHD=0 in the pane before starting the agent.
- Nov-10, 2026 - 04:26 PM +08 - Cache OpenCode session decisions to log and toast at most once per session ID across repeated transforms.
- Nov-10, 2026 - 04:24 PM +08 - Treat Codex subcommand alias "e" as non-human execution.
- Nov-10, 2026 - 04:23 PM +08 - Fix Codex subcommand discovery to skip leading global options and value flags before classifying the session.
- Nov-10, 2026 - 03:22 PM +08 - Release 0.5.0 adds human-session gating across Claude, Codex, Pi, omp, and OpenCode, opt-in decision logging, fork installation guidance, and five new eval cases using a no-regression gate.
