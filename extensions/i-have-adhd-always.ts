/**
 * Always-on i-have-adhd for pi — pi's equivalent of Claude Code's SessionStart hook.
 *
 * Pi has no hooks.json; the extension system is the equivalent mechanism. When the
 * flag file $PI_CODING_AGENT_DIR/.i-have-adhd-always (default ~/.pi/agent/.i-have-adhd-always)
 * exists, this extension appends the full i-have-adhd ruleset to the system prompt
 * of every turn, so the rules apply from message one in every session.
 *
 * The hook only fires when the flag file exists, so installing the extension changes
 * nothing by itself. "stop adhd mode" still turns it off for the current session.
 *
 * Install: copy to ~/.pi/agent/extensions/ (global, all projects) or .pi/extensions/
 * (project-local), then /reload or restart pi.
 * Turn on:  touch ~/.pi/agent/.i-have-adhd-always
 * Turn off: rm ~/.pi/agent/.i-have-adhd-always
 *
 * Mirrors hooks/always-on.sh: pure no-op unless the flag exists, never blocks
 * session start.
 */
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

// Strip a leading YAML frontmatter block (--- ... --- at the very top of file).
function stripFrontmatter(md: string): string {
	const lines = md.split("\n");
	if (lines[0]?.trim() !== "---") return md;
	const end = lines.slice(1).findIndex((line) => line.trim() === "---");
	return end === -1 ? md : lines.slice(end + 2).join("\n");
}

export default function iHaveAdhdAlways(pi: ExtensionAPI) {
	let ruleset = "";

	pi.on("session_start", async (_event, ctx) => {
		const configDir = process.env.PI_CODING_AGENT_DIR ?? path.join(os.homedir(), ".pi", "agent");
		const flagPath = path.join(configDir, ".i-have-adhd-always");

		ruleset = "";
		if (!fs.existsSync(flagPath)) return;

		// The extension ships as a single file, so it can't assume its own directory
		// contains the repo. Check the repo layout first (clone / in-place install),
		// then the pi-global skill install (~/.pi/agent/skills/).
		const candidates = [
			path.join(__dirname, "..", "skills", "i-have-adhd", "SKILL.md"),
			path.join(configDir, "skills", "i-have-adhd", "SKILL.md"),
		];
		const skillPath = candidates.find((p) => fs.existsSync(p));
		if (!skillPath) {
			ctx.ui.notify(
				"i-have-adhd always-on: SKILL.md not found (install the skill first)",
				"warning",
			);
			return;
		}

		const body = stripFrontmatter(fs.readFileSync(skillPath, "utf8"));
		ruleset =
			"ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. " +
			`"stop adhd mode" turns it off for this session; delete ${flagPath} to turn always-on off for good.\n\n` +
			body;
	});

	// Re-appended every turn so it survives /reload, resume, and fork; pi resets the
	// system prompt to the base each turn unless an extension returns a replacement.
	pi.on("before_agent_start", async (event) => {
		if (!ruleset) return;
		return { systemPrompt: `${event.systemPrompt}\n\n${ruleset}` };
	});
}
