import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const CUSTOM_TYPE = "i-have-adhd";
const baseDir = dirname(fileURLToPath(import.meta.url));
const skillPath = join(baseDir, "skills", "i-have-adhd", "SKILL.md");

let cachedRuleset: string | null | undefined;
function loadRuleset(): string | null {
  if (cachedRuleset !== undefined) return cachedRuleset;
  try {
    const raw = readFileSync(skillPath, "utf8");
    cachedRuleset = raw.replace(/^---[\s\S]*?\n---\s*/, "").trim(); // strip YAML frontmatter
  } catch {
    cachedRuleset = null; // skill missing -> stay silent, never crash
  }
  return cachedRuleset;
}

export default function (pi: ExtensionAPI) {
  // Session start hook: visible activation + ruleset cache.
  pi.on("session_start", async (_event, ctx) => {
    if (loadRuleset() && ctx.hasUI) {
      ctx.ui.notify("ADHD MODE ACTIVE: outputs shaped for an ADHD reader (i-have-adhd)", "info");
    }
  });

  // Inject the ruleset whenever it is missing from active context
  // (session start, resume-after-compact, post-compact: all covered).
  pi.on("before_agent_start", async (_event, ctx) => {
    const ruleset = loadRuleset();
    if (!ruleset) return;
    const alreadyPresent = ctx.sessionManager
      .buildContextEntries()
      .some((e) => e.type === "custom_message" && e.customType === CUSTOM_TYPE);
    if (alreadyPresent) return;
    return {
      message: {
        customType: CUSTOM_TYPE,
        content: `ADHD MODE ACTIVE. The reader has ADHD — shape every response for an ADHD reader. The ruleset below applies to every response; "stop adhd mode" turns it off for this session.\n\n${ruleset}`,
        display: true,
      },
    };
  });

  // Keep the original skill usable in pi: /skill:i-have-adhd works from this repo.
  pi.on("resources_discover", () => ({
    skillPaths: [join(baseDir, "skills")],
  }));
}
