import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTICE = (
    "i-have-adhd: couldn't tell if a human is reading; rules not loaded. "
    "Run /i-have-adhd to turn them on."
)
FRONTMATTER = re.compile(r"^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)")


def skill_body(path):
    """Mirror the hook's frontmatter stripping without translating newlines."""
    text = path.read_bytes().decode("utf8")
    return re.sub(r"(?:\r?\n)+$", "", FRONTMATTER.sub("", text, count=1))


@unittest.skipUnless(shutil.which("node"), "node is required for the Codex hook")
@unittest.skipUnless(os.name == "posix", "the parent probe fixture is POSIX-only")
class CodexHookTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        base = Path(self.temp_dir.name)
        self.home = base / "home"
        self.home.mkdir()
        self.bin_dir = base / "bin"
        self.bin_dir.mkdir()
        self.plugin_root = base / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        self.config_dir = base / "claude config"
        self.config_dir.mkdir()
        self.flag = self.config_dir / ".i-have-adhd-always"
        self.log = self.home / ".local" / "state" / "i-have-adhd" / "decisions.log"

    def fake_ps(self, line, comm=None):
        path = self.bin_dir / "ps"
        if comm is None:
            parts = line.strip().split()
            comm = parts[1] if len(parts) > 1 else ""
        script = f"""#!/bin/sh
for arg in "$@"; do
  case "$arg" in
    *comm=*)
      printf '%s\\n' {json.dumps(comm)}
      exit 0
      ;;
  esac
done
printf '%s\\n' {json.dumps(line)}
"""
        path.write_text(script)
        path.chmod(0o755)

    def env(self, **overrides):
        env = os.environ.copy()
        for key in ("I_HAVE_ADHD", "I_HAVE_ADHD_LOG", "CLAUDE_CODE_SESSION_ATTENDED"):
            env.pop(key, None)
        env.update(
            {
                "HOME": str(self.home),
                "USERPROFILE": str(self.home),
                "PATH": str(self.bin_dir) + os.pathsep + env.get("PATH", ""),
                "CLAUDE_CONFIG_DIR": str(self.config_dir),
                "CLAUDE_PLUGIN_ROOT": str(self.plugin_root),
                "PLUGIN_ROOT": str(self.plugin_root),
            }
        )
        env.update(overrides)
        return env

    def hook(self):
        path = ROOT / "hooks" / "hooks.codex.json"
        self.assertTrue(path.is_file(), "hooks/hooks.codex.json is missing")
        return json.loads(path.read_text())["hooks"]["SessionStart"][0]["hooks"][0]

    def run_hook(self, **overrides):
        return subprocess.run(
            self.hook()["command"],
            check=False,
            capture_output=True,
            env=self.env(**overrides),
            input=json.dumps(
                {
                    "session_id": "test-session",
                    "cwd": str(self.plugin_root),
                    "hook_event_name": "SessionStart",
                    "source": "startup",
                }
            ).encode("utf8"),
            shell=True,
        )

    def payload(self, result):
        return json.loads(result.stdout.decode("utf8"))

    def opt_in(self, contents=""):
        self.flag.write_text(contents)

    def managed_daemon(self):
        self.fake_ps("1 codex app-server --managed-daemon")

    def test_codex_receives_the_complete_context_in_a_json_envelope(self):
        self.opt_in()
        self.managed_daemon()

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        payload = self.payload(result)
        output = payload["hookSpecificOutput"]
        self.assertEqual("SessionStart", output["hookEventName"])
        header = (
            "ADHD MODE ACTIVE (always-on). The ruleset below applies to every "
            'response. "stop adhd mode" turns it off for this session; delete '
            f"{self.flag} to turn always-on off for good."
        )
        expected = header + "\n\n" + skill_body(
            self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        )
        self.assertEqual(expected, output["additionalContext"])
        self.assertNotIn("systemMessage", payload)

    def test_codex_preserves_crlf_skill_bytes_in_additional_context(self):
        self.opt_in()
        self.managed_daemon()
        skill = self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        skill.write_bytes(
            b"---\r\nname: fixture\r\n---\r\nFixture line one.\r\nFixture line two.\r\n\r\n"
        )

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        additional = self.payload(result)["hookSpecificOutput"]["additionalContext"]
        self.assertTrue(additional.endswith("\r\nFixture line two."), repr(additional[-60:]))
        self.assertNotIn("Fixture line one.\nFixture", additional)

    def test_codex_exec_is_silent(self):
        self.opt_in()
        self.fake_ps("1 codex exec do the thing")

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_codex_global_flags_exec_is_silent(self):
        self.opt_in()
        self.fake_ps("1 codex --yolo exec do the thing")

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_codex_unclear_returns_only_system_message(self):
        self.opt_in()
        self.fake_ps("1 /bin/zsh -l")

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"systemMessage": NOTICE}, self.payload(result))

    def test_codex_parent_executable_with_spaces_classifies(self):
        self.opt_in()
        self.fake_ps(
            "1 /Applications/Custom Codex/bin/codex app-server --managed-daemon",
            comm="/Applications/Custom Codex/bin/codex",
        )

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        payload = self.payload(result)
        self.assertIn("additionalContext", payload["hookSpecificOutput"])
        self.assertIn("ADHD MODE ACTIVE", payload["hookSpecificOutput"]["additionalContext"])

    def test_non_codex_parent_executable_with_spaces_stays_unclear(self):
        self.opt_in()
        self.fake_ps(
            "1 /Applications/Custom Tool/bin/tool some-arg",
            comm="/Applications/Custom Tool/bin/tool",
        )

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"systemMessage": NOTICE}, self.payload(result))

    def test_codex_opt_out_wins_over_managed_daemon(self):
        self.opt_in()
        self.managed_daemon()

        result = self.run_hook(I_HAVE_ADHD="0")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_codex_is_silent_without_opt_in(self):
        self.managed_daemon()

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)
        self.assertFalse(self.log.exists())
        self.assertFalse((self.home / ".local").exists())

    def test_codex_is_silent_when_skill_is_missing(self):
        self.opt_in()
        self.managed_daemon()
        shutil.rmtree(self.plugin_root / "skills")

        result = self.run_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_codex_is_silent_when_plugin_is_missing(self):
        self.opt_in()
        self.managed_daemon()

        result = self.run_hook(CLAUDE_PLUGIN_ROOT="/nonexistent", PLUGIN_ROOT="/nonexistent")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stdout)


if __name__ == "__main__":
    unittest.main()
