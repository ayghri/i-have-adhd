#!/usr/bin/env python3
"""Preview-first, offline management of the canonical skill. Python 3.11+."""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAME = "i-have-adhd"
STATE = ".i-have-adhd-install"
BEGIN = b"<!-- i-have-adhd:managed:start -->"
END = b"<!-- i-have-adhd:managed:end -->"
MODES = ("on-demand", "always-on")
URL = "https://github.com/ayghri/i-have-adhd"

# Paths are relative to the explicitly selected project or home directory.
# None means a guided route, never an invented automatic installation path.
# The native plugin alternatives are documented in INSTALL.md.
AGENTS = {
    "antigravity": ("Antigravity", None, None, None, ".gemini/GEMINI.md"),
    "astronclaw": ("AstronClaw", None, None, None, None),
    "claude": ("Claude Code", ".claude/skills", ".claude/skills", "CLAUDE.md", ".claude/CLAUDE.md"),
    "codex": ("Codex", ".agents/skills", ".agents/skills", "AGENTS.md", ".codex/AGENTS.md"),
    "gemini": ("Gemini CLI", None, "command", None, ".gemini/GEMINI.md"),
    "copilot": ("GitHub Copilot", ".github/skills", ".copilot/skills", ".github/copilot-instructions.md", None),
    "hermes": ("Hermes", None, ".hermes/skills", "AGENTS.md", None),
    "kimi": ("Kimi Code CLI", None, None, None, None),
    "opencode": ("OpenCode", ".agents/skills", ".agents/skills", None, ".config/opencode/AGENTS.md"),
    "pi": ("Pi", None, None, None, None),
    "omp": ("Oh My Pi (OMP)", None, None, None, None),
    "qwen": ("Qwen Code", None, None, None, None),
    "zed": ("Zed", None, ".agents/skills", None, ".config/zed/AGENTS.md"),
    "cursor": ("Cursor", ".cursor/skills", ".cursor/skills", ".cursor/rules/i-have-adhd.mdc", None),
    "amp": ("Amp", None, None, None, None),
    "generic": ("Portable Markdown", None, None, None, None),
}

# Native operations remain guided: their private package stores are not owned
# by our manifest. Commands are displayed as argv, NEVER evaluated in a shell.
NATIVE = {
    "antigravity": (["agy", "plugin", "install", URL], ["agy", "plugin", "uninstall", NAME]),
    "claude": (["claude", "plugin", "install", NAME + "@" + NAME], ["claude", "plugin", "uninstall", NAME]),
    "codex": (["codex", "plugin", "add", NAME + "@" + NAME], ["codex", "plugin", "remove", NAME]),
    "pi": (["pi", "install", URL], ["pi", "remove", URL]),
    "omp": (["omp", "plugin", "install", "--scope", "user", NAME + "@" + NAME],
            ["omp", "plugin", "uninstall", "--scope", "user", NAME + "@" + NAME]),
    "qwen": (["qwen", "extensions", "install", "ayghri/" + NAME], ["qwen", "extensions", "uninstall", NAME]),
}


class Conflict(ValueError):
    """A conflict requires user review; do not overwrite or adopt it."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def body(source=ROOT):
    text = (source / "skills" / NAME / "SKILL.md").read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise Conflict("Canonical skill is missing frontmatter")
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "".join(lines[i + 1:]).lstrip("\n")
    raise Conflict("Canonical skill has unterminated frontmatter")


def route(agent, scope, mode):
    entry = AGENTS[agent]
    return entry[(1 if scope == "project" else 2) if mode == MODES[0]
                 else (3 if scope == "project" else 4)]


def capability(agent, scope, mode):
    if route(agent, scope, mode):
        return "automatic"
    if agent == "generic":
        return "guided"
    # Unknown scope/mode combinations must not be described as supported.
    if mode == "always-on" and agent in {"astronclaw", "kimi", "omp", "qwen", "amp"}:
        return "unsupported"
    if scope == "project" and agent in {"antigravity", "pi", "omp", "qwen"}:
        return "unsupported"
    return "guided"


def custom_location(agent, scope):
    if scope != "user":
        return None
    variables = {
        "claude": ("CLAUDE_CONFIG_DIR",), "codex": ("CODEX_HOME",),
        "gemini": ("GEMINI_CLI_HOME",), "hermes": ("HERMES_HOME",),
        "opencode": ("XDG_CONFIG_HOME", "OPENCODE_CONFIG", "OPENCODE_CONFIG_DIR"),
        "zed": ("XDG_CONFIG_HOME",), "antigravity": ("GEMINI_CLI_HOME",),
    }
    active = [name for name in variables.get(agent, ()) if os.environ.get(name)]
    return ", ".join(active) if active else None


def linked(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def guidance(agent, scope, mode, action):
    result = [f"{capability(agent, scope, mode)}: {mode}, {scope}; no installation changes made."]
    if agent in NATIVE and capability(agent, scope, mode) != "unsupported":
        args = NATIVE[agent][1 if action == "uninstall" else 0]
        if action == "update":
            result.append("Use the package-specific Update procedure in INSTALL.md; do not reinstall over edits.")
        else:
            result.append("Native alternative (check prerequisites in INSTALL.md): " + json.dumps(args))
        if shutil.which(args[0]) is None:
            result.append(f"Dependency missing: {args[0]}; install it separately if using the native route.")
    if agent == "astronclaw":
        result.append("My skills: import SKILL.md, review, then Enable. Update: download/review your copy first; remove with Delete.")
    elif agent == "kimi":
        result.append("Kimi /plugins: Custom -> repository URL -> Trust and install. Update: R; uninstall: D.")
    elif agent == "amp":
        result.append("Use the existing npx skills procedure with -a amp (and -g for user scope).")
    elif agent == "zed":
        result.append("Zed Skills manager: Create skill from URL, choose Project. Update/reimport or remove there.")
    elif agent == "cursor" and mode == "always-on":
        result.append("Cursor Settings -> Rules -> User Rules: paste exported Markdown; later replace/remove only your pasted text.")
    elif agent == "hermes":
        result.append("Follow the Hermes section; activation is disputed in #118. User always-on requires choosing your persona SOUL.md manually.")
    if mode == "always-on" and agent == "pi":
        result.append("After native install, use the documented .i-have-adhd-always flag in Pi's agent directory; remove it to undo.")
    result += ["Full skill for imports: " + str(ROOT / "skills" / NAME / "SKILL.md"),
               "Portable body: python scripts/manage_install.py export",
               "Review the matching INSTALL.md section for mode, scope, activation and undo. Runtime behavior is not verified."]
    return "\n  ".join(result)


def desired(agent, scope, mode, source=ROOT):
    """Return relative path -> (file/block, bytes); no I/O in the destination."""
    target = route(agent, scope, mode)
    if target is None:
        return {}
    if mode == "always-on":
        if target.endswith(".mdc"):
            return {target: ("file", ("---\nalwaysApply: true\n---\n\n" + body(source)).encode())}
        return {target: ("block", body(source).encode())}
    if target == "command":
        # JSON string escaping is also valid for this TOML basic string. Use
        # the full canonical body instead of the older abbreviated TOML copy.
        prompt = json.dumps(body(source) + "\n{{args}}\n", ensure_ascii=False)
        return {".gemini/commands/i-have-adhd.toml":
                ("file", ('description = "ADHD-friendly output"\nprompt = ' + prompt + "\n").encode())}
    result = {}
    tree = source / "skills" / NAME
    for file in sorted(tree.rglob("*")):
        if file.is_symlink():
            raise Conflict("Symlink in canonical skill: " + str(file))
        if file.is_file():
            result[f"{target}/{NAME}/{file.relative_to(tree).as_posix()}"] = ("file", file.read_bytes())
    return result


def safe_path(root, relative):
    rel = PurePosixPath(relative)
    if not relative or rel.is_absolute() or ".." in rel.parts or "\\" in relative or ":" in relative:
        raise Conflict("Invalid destination: " + relative)
    path = root
    for part in rel.parts:
        path = path / part
        if linked(path):
            raise Conflict("Linked destination requires manual review: " + str(path))
    if path.exists() and path.is_file() and path.stat().st_nlink > 1:
        raise Conflict("Hard-linked destination requires manual review: " + str(path))
    if not path.resolve().is_relative_to(root.resolve()):
        raise Conflict("Destination escapes selected scope: " + relative)
    return path


def read(path):
    if not path.exists():
        return None
    if path.stat().st_size > 4 * 1024 * 1024:
        raise Conflict("File exceeds 4 MiB limit: " + str(path))
    return path.read_bytes()


def block_bounds(data):
    if data.count(BEGIN) != 1 or data.count(END) != 1:
        raise Conflict("Managed markers missing, duplicated or malformed")
    start = data.index(BEGIN)
    end = data.index(END) + len(END)
    if end <= start:
        raise Conflict("Managed markers out of order")
    return start, end


def verify(data, record):
    if data is None:
        raise Conflict("Managed content is missing; restore it before changing the installation")
    owned = data
    if record["kind"] == "block":
        start, end = block_bounds(data)
        owned = data[start:end]
    if digest(owned) != record["sha256"]:
        raise Conflict("Managed content was edited; preserve/reconcile your edits before retrying")


def replace_content(data, record, kind, content):
    """Preserve bytes outside our block, including the original line endings."""
    if kind == "file":
        return content, digest(content), ""
    eol = b"\r\n" if data and b"\r\n" in data else b"\n"
    rendered = BEGIN + eol + content.replace(b"\r\n", b"\n").replace(b"\n", eol) + END
    if record:
        start, end = block_bounds(data)
        return data[:start] + rendered + data[end:], digest(rendered), record["separator"]
    existing = data or b""
    if BEGIN in existing or END in existing or NAME.encode() in existing or b"The reader has ADHD" in existing:
        raise Conflict("Existing unmanaged skill/rules detected; use the existing INSTALL.md procedure")
    separator = eol * 2 if existing else b""
    return existing + separator + rendered, digest(rendered), separator.decode()


def remove_content(data, record):
    if record["kind"] == "file":
        return None
    start, end = block_bounds(data)
    separator = record["separator"].encode()
    if separator and data[:start].endswith(separator):
        start -= len(separator)
    remaining = data[:start] + data[end:]
    return None if record["created"] and not remaining else remaining


def empty_state():
    return {"version": 1, "agents": {}, "resources": {}}


def load_state(root, scope):
    path = safe_path(root, STATE + "/manifest.json")
    raw = read(path)
    if raw is None:
        return empty_state()
    state = json.loads(raw)
    if not isinstance(state, dict) or state.get("version") != 1:
        raise Conflict("Unsupported installation manifest")
    if not isinstance(state.get("agents"), dict) or not isinstance(state.get("resources"), dict):
        raise Conflict("Invalid installation manifest")
    for agent, mode in state["agents"].items():
        if agent not in AGENTS or mode not in MODES or route(agent, scope, mode) is None:
            raise Conflict("Invalid agent/mode in manifest")
    for rel, rec in state["resources"].items():
        safe_path(root, rel)
        if not isinstance(rec, dict) or rec.get("kind") not in {"file", "block"}:
            raise Conflict("Invalid resource in manifest")
        if not isinstance(rec.get("owners"), list) or not rec["owners"]:
            raise Conflict("Invalid resource owners")
        if not isinstance(rec.get("sha256"), str) or len(rec["sha256"]) != 64:
            raise Conflict("Invalid resource hash")
        if type(rec.get("created")) is not bool or rec.get("separator") not in {"", "\n\n", "\r\n\r\n"}:
            raise Conflict("Invalid resource metadata")
        for agent in rec["owners"]:
            if agent not in state["agents"]:
                raise Conflict("Unknown resource owner")
            target = route(agent, scope, state["agents"][agent])
            if state["agents"][agent] == "always-on":
                allowed = rel == target
            elif target == "command":
                allowed = rel == ".gemini/commands/i-have-adhd.toml"
            else:
                allowed = rel.startswith(target + "/" + NAME + "/")
            if not allowed:
                raise Conflict("Manifest destination does not belong to its adapter: " + rel)
    return state


def plan(root, scope, state, agent, action, mode, source=ROOT, selected=None, overlay=None):
    """Preflight one complete agent before returning any mutations."""
    next_state = copy.deepcopy(state)
    selected = set(selected or [agent])
    overlay = overlay or {}
    old_mode = state["agents"].get(agent)
    if action in {"update", "uninstall"} and not old_mode:
        raise Conflict("Not managed here; use INSTALL.md for an existing native/manual installation")
    wanted = {} if action == "uninstall" else desired(agent, scope, mode, source)
    previous = {p for p, r in state["resources"].items() if agent in r["owners"]}
    changes = {}
    # Detect a pre-existing skill directory even if only an extra file remains.
    target = route(agent, scope, mode)
    if action != "uninstall" and mode == "on-demand" and target != "command":
        directory = safe_path(root, target + "/" + NAME)
        managed_tree = any(p.startswith(target + "/" + NAME + "/") for p in state["resources"])
        if directory.exists() and any(linked(p) or p.is_file() for p in directory.rglob("*")) and not managed_tree:
            raise Conflict("Unmanaged skill directory exists: " + str(directory))
    for rel in sorted(previous | set(wanted)):
        path = safe_path(root, rel)
        data = overlay[rel] if rel in overlay else read(path)
        record = state["resources"].get(rel)
        if record:
            verify(data, record)
        elif data is not None and wanted[rel][0] == "file":
            raise Conflict("Unmanaged file exists: " + str(path))
        if rel in wanted:
            kind, content = wanted[rel]
            if record and record["kind"] != kind:
                raise Conflict("Conflicting adapter resource kinds")
            updated, sha, separator = replace_content(data, record, kind, content)
            owners = sorted(set((record or {}).get("owners", [])) | {agent})
            # Shared bytes cannot change behind another agent's recorded state.
            if record and set(record["owners"]) - selected and sha != record["sha256"]:
                raise Conflict("Shared content changed; select all owners to update: " + rel)
            next_state["resources"][rel] = {"kind": kind, "sha256": sha, "owners": owners,
                "created": record["created"] if record else data is None, "separator": separator}
        else:
            remaining = [owner for owner in record["owners"] if owner != agent]
            if remaining:
                next_state["resources"][rel]["owners"] = remaining
                updated = data
            else:
                updated = remove_content(data, record)
                del next_state["resources"][rel]
        if updated != data:
            changes[rel] = (data, updated)
    if action == "uninstall":
        next_state["agents"].pop(agent, None)
    else:
        next_state["agents"][agent] = mode
    return next_state, changes


def write_atomic(path, content):
    if content is None:
        path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".i-have-adhd-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def commit(root, state, changes):
    """Rollback ordinary write failures; keep other completed agents intact."""
    mutations = dict(changes)
    manifest = STATE + "/manifest.json"
    mutations[manifest] = (read(safe_path(root, manifest)),
                          (json.dumps(state, indent=2, sort_keys=True) + "\n").encode())
    completed = []
    try:
        for rel, (before, after) in mutations.items():
            path = safe_path(root, rel)
            if read(path) != before:
                raise Conflict("File changed since preview: " + rel)
            if before == after:
                continue
            write_atomic(path, after)
            completed.append(rel)
    except BaseException as error:
        failures = []
        for rel in reversed(completed):
            try:
                path = safe_path(root, rel)
                if read(path) != mutations[rel][1]:
                    raise Conflict("Concurrent edit prevents rollback")
                write_atomic(path, mutations[rel][0])
            except (OSError, ValueError) as rollback_error:
                failures.append(f"{rel}: {rollback_error}")
        if failures:
            raise Conflict("Rollback incomplete; manual recovery required: " + "; ".join(failures)) from error
        raise


def status(root, scope, state, agent, source=ROOT):
    mode = state["agents"].get(agent)
    if mode:
        try:
            paths = [p for p, r in state["resources"].items() if agent in r["owners"]]
            if not paths:
                raise Conflict("Manifest has no managed resources")
            for rel in paths:
                verify(read(safe_path(root, rel)), state["resources"][rel])
        except (ValueError, OSError) as error:
            return f"managed {mode}, drift: {error}"
        return f"managed {mode}, hashes match; runtime behavior not verified"
    for candidate in MODES:
        for rel, (kind, _) in desired(agent, scope, candidate, source).items():
            data = read(safe_path(root, rel))
            if data is not None and (kind == "file" or NAME.encode() in data or b"The reader has ADHD" in data):
                return "unmanaged/shared installation detected; review INSTALL.md before changing it"
    return "not managed; native/UI installations not inspected; consult INSTALL.md or export"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("list", help="Show capability matrix")
    sub.add_parser("export", help="Print canonical Markdown body to stdout")
    for action in ("install", "update", "uninstall", "status"):
        cmd = sub.add_parser(action)
        cmd.add_argument("--agent", action="append", choices=sorted(AGENTS), required=True)
        scope = cmd.add_mutually_exclusive_group(required=True)
        scope.add_argument("--project", type=Path)
        scope.add_argument("--user", action="store_true")
        if action != "status":
            cmd.add_argument("--apply", action="store_true", help="Opt in to writes in the selected scope")
        if action == "install":
            cmd.add_argument("--mode", choices=MODES, default="on-demand")
    args = parser.parse_args(argv)
    if args.action == "export":
        sys.stdout.write(body())
        return 0
    if args.action == "list":
        print("agent | project on-demand / always-on | user on-demand / always-on")
        for agent in AGENTS:
            columns = [" / ".join(capability(agent, scope, m) for m in MODES) for scope in ("project", "user")]
            print(agent + " | " + " | ".join(columns))
        print("Automatic: install/update/uninstall/status. Guided: manual steps only. Unsupported: export fallback.")
        return 0
    scope = "user" if args.user else "project"
    root = (Path.home() if args.user else args.project).absolute()
    if not root.is_dir():
        parser.error("Selected scope must be an existing directory")
    # Resolving the explicitly chosen root permits macOS /var -> /private/var;
    # every descendant is still checked for symlinks/junctions.
    root = root.resolve()
    apply = getattr(args, "apply", False)
    lock = None
    result = 0
    try:
        lock_path = safe_path(root, STATE + "/lock")
        if lock_path.exists():
            raise Conflict("Installer lock exists; stop other runs and review partial changes before removing " + str(lock_path))
        if apply:
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            lock = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        state = load_state(root, scope)
        overlay = {}
        print(f"{'Apply' if apply else 'Read-only'}; scope: {root}")
        for agent in dict.fromkeys(args.agent):
            try:
                override = custom_location(agent, scope)
                if override:
                    print(f"{agent}: custom configuration ({override}); default paths not inspected or changed. Use INSTALL.md and export.")
                    result = 2 if result == 0 else result
                    continue
                if args.action == "status":
                    print(f"{agent}: {status(root, scope, state, agent)}")
                    continue
                mode = getattr(args, "mode", state["agents"].get(agent, "on-demand"))
                if not route(agent, scope, mode):
                    print(f"{agent}: " + guidance(agent, scope, mode, args.action))
                    result = 2 if result == 0 else result
                    continue
                new_state, changes = plan(root, scope, state, agent, args.action, mode, selected=args.agent, overlay=overlay)
                print(f"{agent}: {args.action} {mode}; {len(changes)} file change(s)")
                for rel, (before, after) in changes.items():
                    verb = "remove" if after is None else "create" if before is None else "update"
                    print(f"  {verb}: {safe_path(root, rel)}")
                print("  manifest: " + str(root / STATE / "manifest.json"))
                if apply:
                    commit(root, new_state, changes)
                    print("  Applied. Start a new agent session; runtime behavior not verified.")
                state = new_state
                if not apply:
                    overlay.update({p: after for p, (_, after) in changes.items()})
            except (OSError, ValueError) as error:
                print(f"{agent}: {error}", file=sys.stderr)
                result = 1
        return result
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    finally:
        if lock is not None:
            os.close(lock)
            lock_path.unlink()
            try:
                lock_path.parent.rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
