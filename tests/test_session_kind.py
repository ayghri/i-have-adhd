import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "hooks" / "session-kind.mjs"
NOTICE = (
    "i-have-adhd: couldn't tell if a human is reading; rules not loaded. "
    "Run /i-have-adhd to turn them on."
)

CALL_MODULE = """
const mod = await import(process.argv[1]);
const request = JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify(mod[request.fn](request.args)));
"""


@unittest.skipUnless(shutil.which("node"), "node is required for the shared module")
class SessionKindTest(unittest.TestCase):
    def call(self, fn, args):
        result = subprocess.run(
            ["node", "--input-type=module", "-e", CALL_MODULE, MODULE.as_uri(), json.dumps({"fn": fn, "args": args})],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return json.loads(result.stdout)

    def classify(self, **kwargs):
        kwargs.setdefault("env", {})
        return self.call("classifySession", kwargs)

    def test_opt_out_wins_before_agent_specific_signals(self):
        human_signals = {
            "claude": {"env": {"I_HAVE_ADHD": "0", "CLAUDE_CODE_SESSION_ATTENDED": "1"}},
            "codex": {"env": {"I_HAVE_ADHD": "0"}, "parent": ["codex", "app-server", "--managed-daemon"]},
            "pi": {"env": {"I_HAVE_ADHD": "0"}, "ctx": {"mode": "tui"}},
            "omp": {"env": {"I_HAVE_ADHD": "0"}, "ctx": {"mode": "tui", "agent": {"kind": "main"}}},
            "opencode": {"env": {"I_HAVE_ADHD": "0"}, "ctx": {}},
        }
        for agent, signals in human_signals.items():
            with self.subTest(agent=agent):
                result = self.classify(agent=agent, **signals)
                self.assertEqual("opt-out", result["decision"])
                self.assertEqual({}, result["signals"])

    def test_claude_attendance_mapping(self):
        cases = {
            "1": "human",
            "0": "non-human",
            None: "unclear",
            "": "unclear",
            "true": "unclear",
            "2": "unclear",
        }
        for value, decision in cases.items():
            with self.subTest(attended=value):
                env = {} if value is None else {"CLAUDE_CODE_SESSION_ATTENDED": value}
                result = self.classify(agent="claude", env=env)
                self.assertEqual(decision, result["decision"])
                self.assertTrue(result["reason"])
                self.assertIn("attended", result["signals"])

    def test_codex_parent_argv_mapping(self):
        cases = {
            ("codex", "app-server", "--managed-daemon"): "human",
            ("/usr/local/bin/codex", "app-server", "--managed-daemon", "--config", "x"): "human",
            ("codex", "exec", "do the thing"): "non-human",
            ("/opt/codex", "exec", "--json", "prompt"): "non-human",
            ("codex", "--version"): "unclear",
            ("codex",): "human",
            ("node", "server.js"): "unclear",
            (): "unclear",
        }
        for argv, decision in cases.items():
            with self.subTest(argv=argv):
                result = self.classify(agent="codex", parent=list(argv))
                self.assertEqual(decision, result["decision"])
                self.assertTrue(result["reason"])
                self.assertIn("parent", result["signals"])
                self.assertNotIn("prompt", json.dumps(result["signals"]))
        self.assertEqual(
            "unclear", self.classify(agent="codex", parent=None)["decision"]
        )

    def test_codex_global_flags_before_subcommand(self):
        cases = [
            (["codex", "--yolo", "exec", "do", "the", "thing"], "non-human"),
            (["codex", "-c", "k=v", "exec", "do", "the", "thing"], "non-human"),
            (["codex", "--config=k=v", "exec"], "non-human"),
            (["codex", "--enable", "x", "app-server", "--managed-daemon"], "human"),
            (["codex", "--yolo", "app-server"], "unclear"),
            (["codex", "--yolo"], "human"),
            (["codex", "-c"], "unclear"),
        ]
        for parent, expected in cases:
            with self.subTest(parent=parent):
                result = self.classify(agent="codex", parent=parent)
                self.assertEqual(expected, result["decision"])

    def test_codex_alias_e_is_non_human(self):
        result = self.classify(agent="codex", parent=["codex", "e", "do the thing"])
        self.assertEqual("non-human", result["decision"])
        self.assertEqual("codex-exec", result["reason"])
        self.assertEqual({"parent": "exec"}, result["signals"])

    def test_codex_interactive_tui_without_managed_daemon_is_human(self):
        for parent in (["codex"], ["/usr/local/bin/codex"], ["codex", "--yolo"]):
            with self.subTest(parent=parent):
                result = self.classify(agent="codex", parent=parent)
                self.assertEqual("human", result["decision"])
                self.assertEqual("codex-tui", result["reason"])
                self.assertEqual({"parent": "tui"}, result["signals"])

    def test_codex_info_flags_stay_unclear(self):
        for parent in (
            ["codex", "--help"],
            ["codex", "-h"],
            ["codex", "--version"],
            ["codex", "-c"],
        ):
            with self.subTest(parent=parent):
                result = self.classify(agent="codex", parent=parent)
                self.assertEqual("unclear", result["decision"])

    def test_codex_local_provider_and_multivalue_images(self):
        cases = [
            (["codex", "--oss", "--local-provider", "ollama", "exec"], "non-human"),
            (["codex", "-i", "a.png", "b.png", "exec"], "non-human"),
            (["codex", "--image", "a.png", "b.png", "app-server", "--managed-daemon"], "human"),
            (["codex", "-i", "a.png", "b.png"], "human"),
        ]
        for parent, expected in cases:
            with self.subTest(parent=parent):
                result = self.classify(agent="codex", parent=parent)
                self.assertEqual(expected, result["decision"])

    def test_win32_process_fallback_drops_executable_token(self):
        output = "1234\tC:\\Program Files\\codex\\codex.exe\tcodex app-server --managed-daemon"
        parsed = self.call("parseWin32Process", output)
        self.assertEqual(
            ["C:\\Program Files\\codex\\codex.exe", "app-server", "--managed-daemon"],
            parsed["argv"],
        )
        result = self.classify(agent="codex", parent=parsed["argv"])
        self.assertEqual("human", result["decision"])

    def test_pi_mode_mapping(self):
        for mode, decision in {"tui": "human", "print": "non-human", "json": "non-human", "rpc": "unclear"}.items():
            with self.subTest(mode=mode):
                result = self.classify(agent="pi", ctx={"mode": mode})
                self.assertEqual(decision, result["decision"])
                self.assertEqual(mode, result["signals"]["mode"])

    def test_omp_kind_and_mode_mapping(self):
        cases = {
            ("main", "tui"): "human",
            ("sub", "tui"): "non-human",
            ("main", "print"): "non-human",
            ("main", "json"): "non-human",
            ("sub", "rpc"): "non-human",
            ("main", "rpc"): "unclear",
            (None, "tui"): "unclear",
        }
        for (kind, mode), decision in cases.items():
            with self.subTest(kind=kind, mode=mode):
                agent = {} if kind is None else {"kind": kind}
                result = self.classify(agent="omp", ctx={"mode": mode, "agent": agent})
                self.assertEqual(decision, result["decision"])
                self.assertEqual(mode, result["signals"]["mode"])

    def test_opencode_parent_id_mapping(self):
        self.assertEqual(
            "human", self.classify(agent="opencode", ctx={})["decision"]
        )
        self.assertEqual(
            "non-human",
            self.classify(agent="opencode", ctx={"parentID": "ses_parent"})["decision"],
        )
        self.assertEqual(
            "unclear",
            self.classify(agent="opencode", ctx={"parentID": 42})["decision"],
        )

    def test_missing_or_malformed_signals_are_unclear(self):
        for label, kwargs in {
            "claude": {"agent": "claude"},
            "codex": {"agent": "codex"},
            "pi": {"agent": "pi"},
            "pi-null-ctx": {"agent": "pi", "ctx": None},
            "omp": {"agent": "omp"},
            "unknown": {"agent": "mystery"},
        }.items():
            with self.subTest(agent=label):
                self.assertEqual("unclear", self.classify(**kwargs)["decision"])

        self.assertEqual(
            "unclear", self.classify(agent="pi", ctx={"mode": 3})["decision"]
        )
        self.assertEqual(
            "unclear", self.classify(agent="omp", ctx={"mode": "tui", "agent": {"kind": 1}})["decision"]
        )


@unittest.skipUnless(shutil.which("node"), "node is required for the shared module")
class DecisionLogTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        base = Path(self.temp_dir.name)
        self.home = base / "home"
        self.home.mkdir()
        self.config_dir = base / "claude"
        self.config_dir.mkdir()
        self.flag = self.config_dir / ".i-have-adhd-always"
        self.log = self.home / ".local" / "state" / "i-have-adhd" / "decisions.log"

    def env(self, **overrides):
        env = os.environ.copy()
        for key in ("I_HAVE_ADHD", "I_HAVE_ADHD_LOG", "CLAUDE_CODE_SESSION_ATTENDED"):
            env.pop(key, None)
        env.update(
            {
                "HOME": str(self.home),
                "USERPROFILE": str(self.home),
                "XDG_CONFIG_HOME": str(self.home / ".config"),
                "XDG_STATE_HOME": str(self.home / "state"),
                "CLAUDE_CONFIG_DIR": str(self.config_dir),
            }
        )
        env.update(overrides)
        return env

    def run_hook(self, **env_overrides):
        return subprocess.run(
            ["node", str(ROOT / "hooks" / "always-on.mjs"), "--agent", "claude"],
            check=False,
            capture_output=True,
            text=True,
            env=self.env(**env_overrides),
            cwd=ROOT,
        )

    def log_lines(self):
        self.assertTrue(self.log.exists(), "no decision log was written")
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_empty_home_without_flag_stays_silent_and_creates_no_log(self):
        result = self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)
        self.assertFalse(self.log.exists())
        self.assertFalse((self.home / ".local").exists())

    def test_flag_log_line_and_env_enable_decision_logging(self):
        self.flag.write_text("log\n")
        result = self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(self.log.exists(), "the flag's log line did not enable logging")

        self.flag.unlink()
        self.log.unlink()
        self.flag.write_text("")
        result = self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1", I_HAVE_ADHD_LOG="1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(self.log.exists(), "I_HAVE_ADHD_LOG=1 did not enable logging")

        self.log.unlink()
        result = self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(self.log.exists(), "logging must stay off by default")

    def test_log_lines_contain_timestamp_agent_signals_and_result(self):
        self.flag.write_text("log\n")
        self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1", SECRET_SENTINEL="do-not-log")
        self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="0", SECRET_SENTINEL="do-not-log")
        self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="not-a-signal")
        self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1", I_HAVE_ADHD="0")

        lines = self.log_lines()
        self.assertEqual(
            ["injected", "skipped-non-human", "skipped-unclear", "skipped-optout"],
            [line["result"] for line in lines],
        )
        for line in lines:
            self.assertEqual({"timestamp", "agent", "signals", "result"}, set(line))
            datetime.fromisoformat(line["timestamp"].replace("Z", "+00:00"))
            self.assertEqual("claude", line["agent"])
            if line["result"] == "skipped-optout":
                self.assertEqual({}, line["signals"])
            else:
                self.assertEqual({"attended"}, set(line["signals"]))
            self.assertNotIn("do-not-log", json.dumps(line))
            self.assertNotIn("SECRET_SENTINEL", json.dumps(line))

    def test_log_write_failure_does_not_change_decision(self):
        self.flag.write_text("log\n")
        self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1")
        self.assertTrue(self.log.exists(), "the enabled logger never wrote a line")
        self.log.unlink()
        shutil.rmtree(self.home / ".local" / "state")
        (self.home / ".local" / "state").write_text("not a directory\n")
        (self.home / ".local" / "state").write_text("not a directory\n")

        result = self.run_hook(CLAUDE_CODE_SESSION_ATTENDED="1")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)
        self.assertFalse(self.log.exists())


if __name__ == "__main__":
    unittest.main()
