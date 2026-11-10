// Shared human-session classifier and opt-in decision log for every injector.
//
// Always-on rules may only load when a person is reading replies as they
// arrive. Anything unknown is `unclear`, never a guess in the human direction.
//
// Decision log: off unless the flag file has a line exactly `log` or
// I_HAVE_ADHD_LOG=1. One JSON object per line in
// ~/.local/state/i-have-adhd/decisions.log. Logging never changes a decision.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";

export const NOTICE =
  "i-have-adhd: couldn't tell if a human is reading; rules not loaded. " +
  "Run /i-have-adhd to turn them on.";

const LOG_SIGNAL_KEYS = ["attended", "mode", "agentKind", "parent", "parentId"];

function result(decision, reason, signals) {
  return { decision, reason, signals };
}

function unclear(reason, signals) {
  return result("unclear", reason, signals);
}

function classifyClaude(env) {
  const raw = env ? env.CLAUDE_CODE_SESSION_ATTENDED : undefined;
  if (raw === "1") return result("human", "claude-attended", { attended: "1" });
  if (raw === "0") return result("non-human", "claude-unattended", { attended: "0" });
  return unclear("claude-attendance-unset", {
    attended: raw === undefined ? "unset" : "malformed",
  });
}

const CODEX_VALUE_FLAGS = new Set([
  "-c",
  "--config",
  "--enable",
  "--disable",
  "--remote",
  "-m",
  "--model",
  "-p",
  "--profile",
  "-s",
  "--sandbox",
  "-a",
  "--ask-for-approval",
  "-C",
  "--cd",
  "--local-provider",
  "--add-dir",
  "--remote-auth-token-env",
]);

// Informational one-shots never open a session, so a `codex` process carrying
// one of these is not the interactive TUI.
const CODEX_INFO_FLAGS = new Set(["-h", "--help", "-V", "-v", "--version"]);

const CODEX_SUBCOMMANDS = new Set([
  "agents",
  "exec",
  "e",
  "review",
  "login",
  "logout",
  "mcp",
  "plugin",
  "app-server",
  "remote-control",
  "app",
  "completion",
  "update",
  "doctor",
  "sandbox",
  "debug",
  "apply",
  "a",
  "resume",
  "queue",
  "archive",
  "delete",
  "migrate-rollouts",
  "migrate-nfs-db",
  "unarchive",
  "fork",
  "cloud",
  "exec-server",
  "features",
  "help",
]);

function codexParent(parent) {
  if (!Array.isArray(parent) || parent.length === 0) return null;
  const executable = typeof parent[0] === "string" ? parent[0] : "";
  const name = path.basename(executable.replace(/\\/g, "/")).replace(/\.(?:exe|cmd)$/i, "").toLowerCase();
  if (name !== "codex") return null;

  let i = 1;
  while (i < parent.length) {
    const token = parent[i];
    if (typeof token !== "string") return "";
    if (token === "--") {
      i += 1;
      break;
    }
    if (token === "-i" || token === "--image") {
      i += 1;
      while (i < parent.length) {
        const next = parent[i];
        if (typeof next !== "string") return "";
        if (next.startsWith("-") || CODEX_SUBCOMMANDS.has(next)) {
          break;
        }
        i += 1;
      }
      continue;
    }
    if (token.startsWith("-")) {
      if (CODEX_VALUE_FLAGS.has(token)) {
        if (i + 1 >= parent.length) return null;
        i += 2;
      } else {
        i += 1;
      }
      continue;
    }
    return token;
  }
  return typeof parent[i] === "string" ? parent[i] : "";
}

function classifyCodex(parent) {
  const subcommand = codexParent(parent);
  if (subcommand === null) return unclear("codex-parent-unknown", { parent: "unknown" });
  if (subcommand === "") {
    if (parent.some((token) => CODEX_INFO_FLAGS.has(token))) {
      return unclear("codex-parent-unknown", { parent: "unknown" });
    }
    // `codex` with no subcommand opens the interactive TUI. With
    // `daemon_auto_start = false` no managed daemon exists, so this argv is the
    // only human signal an interactive session has.
    return result("human", "codex-tui", { parent: "tui" });
  }
  if (subcommand === "app-server") {
    if (parent.includes("--managed-daemon")) {
      return result("human", "codex-managed-daemon", { parent: "app-server" });
    }
    return unclear("codex-parent-unknown", { parent: "app-server" });
  }
  if (subcommand === "exec" || subcommand === "e") return result("non-human", "codex-exec", { parent: "exec" });
  return unclear("codex-parent-unknown", { parent: "unknown" });
}

function modeOf(ctx) {
  return ctx && typeof ctx.mode === "string" ? ctx.mode : null;
}

function classifyMode(agent, ctx) {
  const mode = modeOf(ctx);
  if (mode === null) return unclear(`${agent}-mode-unknown`, { mode: "malformed" });
  if (mode === "tui") return result("human", `${agent}-tui`, { mode });
  if (mode === "print" || mode === "json") {
    return result("non-human", `${agent}-${mode}`, { mode });
  }
  return unclear(`${agent}-mode-unclear`, { mode });
}

function agentKindOf(ctx) {
  if (!ctx) return null;
  if (typeof ctx.agentKind === "string") return ctx.agentKind;
  if (ctx.agent && typeof ctx.agent.kind === "string") return ctx.agent.kind;
  return null;
}

function classifyOmp(ctx) {
  // shortcut: the omp context shape (ctx.agent.kind or ctx.agentKind) is taken
  // from upstream source, not the installed binary; real-agent QA confirms it.
  const agentKind = agentKindOf(ctx);
  const mode = modeOf(ctx);
  const signals = {
    mode: mode === null ? "malformed" : mode,
    agentKind: agentKind === null ? "malformed" : agentKind,
  };
  if (agentKind === "sub") return result("non-human", "omp-subagent", signals);
  if (mode === "print" || mode === "json") {
    return result("non-human", `omp-${mode}`, signals);
  }
  if (agentKind === "main" && mode === "tui") {
    return result("human", "omp-main-tui", signals);
  }
  return unclear("omp-mode-unclear", signals);
}

function classifyOpenCode(ctx) {
  const parentID = ctx ? ctx.parentID : undefined;
  if (parentID === undefined || parentID === null || parentID === "") {
    return result("human", "opencode-top-level", { parentId: "absent" });
  }
  if (typeof parentID === "string") {
    return result("non-human", "opencode-subagent", { parentId: "present" });
  }
  return unclear("opencode-parent-unknown", { parentId: "malformed" });
}

export function classifySession({ agent, env = process.env, parent = null, ctx = null } = {}) {
  if (env && String(env.I_HAVE_ADHD ?? "").trim() === "0") {
    return result("opt-out", "opt-out-env", {});
  }
  if (ctx !== null && typeof ctx !== "object") {
    return unclear("context-malformed", {});
  }
  switch (agent) {
    case "claude":
      return classifyClaude(env);
    case "codex":
      return classifyCodex(parent);
    case "pi":
      return classifyMode("pi", ctx);
    case "omp":
      return classifyOmp(ctx);
    case "opencode":
      return classifyOpenCode(ctx);
    default:
      return unclear("agent-unknown", {});
  }
}

export function flagPathFor(agent, env = process.env) {
  if (agent === "opencode") {
    return path.join(
      env.XDG_CONFIG_HOME || path.join(os.homedir(), ".config"),
      "opencode",
      ".i-have-adhd-always",
    );
  }
  if (agent === "pi" || agent === "omp") return null; // callers know their agent dir
  return path.join(
    env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude"),
    ".i-have-adhd-always",
  );
}

export function loggingEnabled({ agent, env = process.env, flagPath } = {}) {
  if (env && env.I_HAVE_ADHD_LOG === "1") return true;
  const flag = flagPath === undefined ? flagPathFor(agent, env) : flagPath;
  if (!flag) return false;
  try {
    return fs.readFileSync(flag, "utf8").split(/\r?\n/).includes("log");
  } catch {
    return false;
  }
}

export function logDecision({
  agent,
  decision,
  reason,
  signals = {},
  env = process.env,
  flagPath,
} = {}) {
  try {
    if (!loggingEnabled({ agent, env, flagPath })) return false;
    const safeSignals = {};
    for (const key of LOG_SIGNAL_KEYS) {
      if (signals[key] !== undefined) safeSignals[key] = String(signals[key]);
    }
    const directory = path.join(os.homedir(), ".local", "state", "i-have-adhd");
    fs.mkdirSync(directory, { recursive: true });
    fs.appendFileSync(
      path.join(directory, "decisions.log"),
      JSON.stringify({
        timestamp: new Date().toISOString(),
        agent,
        signals: safeSignals,
        result: decisionResult(decision),
      }) + "\n",
    );
    return true;
  } catch {
    return false;
  }
}

export function decisionResult(decision) {
  if (decision === "opt-out") return "skipped-optout";
  return decision === "human" ? "injected" : `skipped-${decision}`;
}

function parseProcessOutputs(comm, argsOutput) {
  const match = /^\s*(\d+)\s+(.+?)\s*$/.exec(argsOutput);
  if (!match) return null;
  const ppid = Number(match[1]);
  const fullArgs = match[2];

  if (!comm) {
    return { ppid, argv: fullArgs.split(/\s+/) };
  }

  if (fullArgs.startsWith(comm)) {
    const rest = fullArgs.slice(comm.length).trim();
    return { ppid, argv: [comm, ...(rest ? rest.split(/\s+/) : [])] };
  }

  const quotedComm = `"${comm}"`;
  if (fullArgs.startsWith(quotedComm)) {
    const rest = fullArgs.slice(quotedComm.length).trim();
    return { ppid, argv: [comm, ...(rest ? rest.split(/\s+/) : [])] };
  }

  const commBase = path.basename(comm).toLowerCase();
  const idx = fullArgs.toLowerCase().indexOf(commBase);
  if (idx !== -1) {
    const endIdx = idx + commBase.length;
    const nextChar = fullArgs.charAt(endIdx);
    if (nextChar === "" || nextChar === " " || nextChar === '"') {
      const execCandidate = fullArgs.slice(0, endIdx).replace(/^"/, "");
      if (path.basename(execCandidate).toLowerCase() === commBase) {
        const rest = fullArgs.slice(endIdx + (nextChar === '"' ? 1 : 0)).trim();
        return { ppid, argv: [execCandidate, ...(rest ? rest.split(/\s+/) : [])] };
      }
    }
  }

  return { ppid, argv: fullArgs.split(/\s+/) };
}

export function parseWin32Process(output) {
  if (!output) return null;
  const parts = output.trim().split("\t");
  if (parts.length < 3) return null;
  const ppid = Number(parts[0]);
  const execPath = parts[1].trim();
  const cmdLine = parts[2].trim();

  if (!Number.isInteger(ppid) || ppid <= 0) return null;
  if (!execPath) {
    if (!cmdLine) return null;
    return { ppid, argv: cmdLine.split(/\s+/) };
  }

  if (cmdLine.startsWith(`"${execPath}"`)) {
    const rest = cmdLine.slice(execPath.length + 2).trim();
    return { ppid, argv: [execPath, ...(rest ? rest.split(/\s+/) : [])] };
  }
  if (cmdLine.startsWith(execPath)) {
    const rest = cmdLine.slice(execPath.length).trim();
    return { ppid, argv: [execPath, ...(rest ? rest.split(/\s+/) : [])] };
  }

  const tokens = cmdLine ? cmdLine.split(/\s+/) : [];
  return { ppid, argv: [execPath, ...(tokens.length > 0 ? tokens.slice(1) : [])] };
}

function readProcess(pid) {
  try {
    if (process.platform === "win32") {
      const output = execFileSync(
        "powershell",
        [
          "-NoProfile",
          "-NonInteractive",
          "-Command",
          `$p = Get-CimInstance Win32_Process -Filter 'ProcessId=${pid}'; if ($p) { "$($p.ParentProcessId)\`t$($p.ExecutablePath)\`t$($p.CommandLine)" }`,
        ],
        { encoding: "utf8", timeout: 1000, stdio: ["ignore", "pipe", "ignore"] },
      );
      return parseWin32Process(output);
    }
    const commOutput = execFileSync("ps", ["-o", "comm=", "-p", String(pid)], {
      encoding: "utf8",
      timeout: 1000,
      maxBuffer: 64 * 1024,
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
    const argsOutput = execFileSync("ps", ["-o", "ppid=,args=", "-p", String(pid)], {
      encoding: "utf8",
      timeout: 1000,
      maxBuffer: 64 * 1024,
      stdio: ["ignore", "pipe", "ignore"],
    });
    return parseProcessOutputs(commOutput, argsOutput);
  } catch {
    return null;
  }
}

/**
 * Walk up to eight ancestors looking for the `codex` process that launched this
 * hook. Bounded, argv-only, no shell strings. Any failure means `null`, which
 * the classifier turns into `unclear`.
 */
export function parentArgv(startPid = process.ppid) {
  const seen = new Set();
  let pid = startPid;
  for (let depth = 0; depth < 8; depth++) {
    if (!Number.isInteger(pid) || pid <= 0 || seen.has(pid)) return null;
    seen.add(pid);
    const info = readProcess(pid);
    if (!info) return null;
    if (path.basename((info.argv[0] || "").replace(/\\/g, "/")).replace(/\.(?:exe|cmd)$/i, "").toLowerCase() === "codex") {
      return info.argv;
    }
    pid = info.ppid;
  }
  return null;
}
