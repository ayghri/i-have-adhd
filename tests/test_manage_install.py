"""Offline installer tests; all destinations are disposable directories."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("manage_install", ROOT / "scripts/manage_install.py")
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="adhd space ")
        self.root = Path(self.temp.name).resolve()
        self.state = m.empty_state()
        self.config_patch = mock.patch.dict(os.environ, {key: "" for key in ("CLAUDE_CONFIG_DIR", "CODEX_HOME", "GEMINI_CLI_HOME", "HERMES_HOME", "XDG_CONFIG_HOME", "OPENCODE_CONFIG", "OPENCODE_CONFIG_DIR")})
        self.config_patch.start()

    def tearDown(self):
        self.config_patch.stop()
        self.temp.cleanup()

    def apply(self, agent="codex", mode="on-demand", action="install", scope="project", source=ROOT, selected=None):
        state, changes = m.plan(self.root, scope, self.state, agent, action, mode, source, selected)
        m.commit(self.root, state, changes)
        self.state = state
        return changes

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = m.main(list(args))
        return result, out.getvalue(), err.getvalue()

    def test_export_is_exact_body(self):
        code, out, err = self.cli("export")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, m.body())
        self.assertNotIn("disable-model-invocation:", out)
        self.assertTrue(out.startswith("# i-have-adhd"))

    def test_capability_registry_covers_documented_agents(self):
        docs = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
        for key, entry in m.AGENTS.items():
            if key != "generic":
                self.assertIn(entry[0], docs)
            for scope in ("user", "project"):
                for mode in m.MODES:
                    self.assertIn(m.capability(key, scope, mode), ("automatic", "guided", "unsupported"))

    def test_all_automatic_routes_roundtrip(self):
        for agent in m.AGENTS:
            for scope in ("project", "user"):
                for mode in m.MODES:
                    if not m.route(agent, scope, mode):
                        continue
                    with self.subTest(agent=agent, scope=scope, mode=mode):
                        with tempfile.TemporaryDirectory() as temp:
                            root = Path(temp).resolve()
                            state, changes = m.plan(root, scope, m.empty_state(), agent, "install", mode)
                            m.commit(root, state, changes)
                            m.load_state(root, scope)
                            self.assertIn("hashes match", m.status(root, scope, state, agent))
                            state, changes = m.plan(root, scope, state, agent, "uninstall", mode)
                            m.commit(root, state, changes)
                            self.assertEqual(state, m.empty_state())

    def test_repeated_install_and_reinstall_after_uninstall(self):
        self.apply()
        self.assertEqual(self.apply(), {})
        self.apply(action="uninstall")
        self.apply()
        self.assertTrue((self.root / ".agents/skills/i-have-adhd/SKILL.md").exists())

    def test_block_preserves_crlf_and_external_edits(self):
        path = self.root / "AGENTS.md"
        original = b"# My instructions\r\nPreserve this.\r\n"
        path.write_bytes(original)
        self.apply(mode="always-on")
        self.assertTrue(path.read_bytes().startswith(original))
        path.write_bytes(path.read_bytes() + b"\r\nLater instruction\r\n")
        self.apply(mode="always-on", action="update")
        self.apply(mode="always-on", action="uninstall")
        self.assertEqual(path.read_bytes(), original + b"\r\nLater instruction\r\n")

    def test_empty_existing_file_remains_after_uninstall(self):
        (self.root / "AGENTS.md").write_bytes(b"")
        self.apply(mode="always-on")
        self.apply(mode="always-on", action="uninstall")
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), b"")

    def test_mode_transition_removes_previous_resources(self):
        self.apply()
        self.apply(mode="always-on")
        self.assertFalse((self.root / ".agents/skills/i-have-adhd/SKILL.md").exists())
        self.assertTrue((self.root / "AGENTS.md").exists())
        self.apply()
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_edit_blocks_update_remove_and_transition(self):
        self.apply()
        target = self.root / ".agents/skills/i-have-adhd/SKILL.md"
        target.write_bytes(target.read_bytes() + b"my edits")
        for action, mode in (("update", "on-demand"), ("uninstall", "on-demand"), ("install", "always-on")):
            with self.subTest(action=action):
                with self.assertRaisesRegex(m.Conflict, "edited"):
                    self.apply(action=action, mode=mode)
        self.assertTrue(target.read_bytes().endswith(b"my edits"))

    def test_block_edit_and_missing_markers_rejected(self):
        self.apply(mode="always-on")
        target = self.root / "AGENTS.md"
        original = target.read_bytes()
        for content in (original.replace(b"# i-have-adhd", b"# changed"), original.replace(m.END, b""), original + m.END):
            target.write_bytes(content)
            with self.assertRaises(m.Conflict):
                self.apply(mode="always-on", action="uninstall")
        target.write_bytes(original)

    def test_unmanaged_files_and_skill_directories_are_not_adopted(self):
        target = self.root / ".agents/skills/i-have-adhd"
        target.mkdir(parents=True)
        (target / "notes.txt").write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(m.Conflict, "Unmanaged"):
            self.apply()
        self.assertEqual((target / "notes.txt").read_text(), "keep")

    def test_unmanaged_rules_are_not_duplicated(self):
        (self.root / "AGENTS.md").write_text("# i-have-adhd\nmanual rules", encoding="utf-8")
        with self.assertRaisesRegex(m.Conflict, "unmanaged"):
            self.apply(mode="always-on")

    def test_shared_files_reference_counted(self):
        self.apply()
        self.apply(agent="opencode")
        rel = ".agents/skills/i-have-adhd/SKILL.md"
        self.assertEqual(self.state["resources"][rel]["owners"], ["codex", "opencode"])
        self.apply(action="uninstall")
        self.assertTrue((self.root / rel).exists())
        self.apply(agent="opencode", action="uninstall")
        self.assertFalse((self.root / rel).exists())

    def test_shared_block_survives_removing_one_owner(self):
        self.apply(mode="always-on")
        self.apply(agent="hermes", mode="always-on")
        self.apply(mode="always-on", action="uninstall")
        self.assertTrue((self.root / "AGENTS.md").exists())
        self.apply(agent="hermes", mode="always-on", action="uninstall")
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_update_from_checkout_and_shared_owners(self):
        self.apply()
        self.apply(agent="opencode")
        candidate = self.root / "candidate"
        shutil.copytree(ROOT / "skills", candidate / "skills")
        skill = candidate / "skills/i-have-adhd/SKILL.md"
        skill.write_bytes(skill.read_bytes() + b"\nUpdated source\n")
        with self.assertRaisesRegex(m.Conflict, "all owners"):
            self.apply(action="update", source=candidate)
        self.apply(action="update", source=candidate, selected=["codex", "opencode"])
        self.apply(agent="opencode", action="update", source=candidate, selected=["codex", "opencode"])
        self.assertIn(b"Updated source", (self.root / ".agents/skills/i-have-adhd/SKILL.md").read_bytes())

    def test_update_removes_only_old_owned_source_files(self):
        self.apply()
        candidate = self.root / "candidate"
        shutil.copytree(ROOT / "skills", candidate / "skills")
        (candidate / "skills/i-have-adhd/agents/gemini.toml").unlink()
        directory = self.root / ".agents/skills/i-have-adhd"
        (directory / "personal.txt").write_text("keep", encoding="utf-8")
        self.apply(action="update", source=candidate)
        self.assertFalse((directory / "agents/gemini.toml").exists())
        self.assertEqual((directory / "personal.txt").read_text(), "keep")

    def test_preview_never_writes_and_deduplicates_shared_paths(self):
        args = ("install", "--project", str(self.root), "--agent", "codex", "--agent", "opencode")
        code, out, err = self.cli(*args)
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertEqual(out.count("create: " + str(self.root / ".agents/skills/i-have-adhd/SKILL.md")), 1)
        self.assertIn("opencode: install on-demand; 0 file change(s)", out)

    def test_partial_agent_failure_keeps_successful_agent(self):
        bad = self.root / ".cursor/skills/i-have-adhd"
        bad.mkdir(parents=True)
        (bad / "SKILL.md").write_text("mine")
        code, out, err = self.cli("install", "--project", str(self.root), "--agent", "codex", "--agent", "cursor", "--apply")
        self.assertEqual(code, 1)
        state = m.load_state(self.root, "project")
        self.assertEqual(state["agents"], {"codex": "on-demand"})
        self.assertIn("Unmanaged", err)

    def test_failure_rolls_back_all_agent_files(self):
        state, changes = m.plan(self.root, "project", self.state, "codex", "install", "on-demand")
        original = m.write_atomic
        calls = []
        def failing(path, content):
            calls.append(path)
            if len(calls) == 2:
                raise PermissionError("simulated permission failure")
            original(path, content)
        with mock.patch.object(m, "write_atomic", side_effect=failing):
            with self.assertRaises(PermissionError):
                m.commit(self.root, state, changes)
        self.assertFalse((self.root / m.STATE / "manifest.json").exists())
        self.assertFalse(any(path.is_file() for path in self.root.rglob("*")))

    def test_manifest_failure_rolls_back_content(self):
        state, changes = m.plan(self.root, "project", self.state, "codex", "install", "always-on")
        original = m.write_atomic
        def failing(path, content):
            if path.name == "manifest.json":
                raise PermissionError("manifest denied")
            original(path, content)
        with mock.patch.object(m, "write_atomic", side_effect=failing):
            with self.assertRaises(PermissionError):
                m.commit(self.root, state, changes)
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_concurrent_edit_after_plan_is_preserved(self):
        (self.root / "AGENTS.md").write_text("before")
        state, changes = m.plan(self.root, "project", self.state, "codex", "install", "always-on")
        (self.root / "AGENTS.md").write_text("after")
        with self.assertRaisesRegex(m.Conflict, "changed since"):
            m.commit(self.root, state, changes)
        self.assertEqual((self.root / "AGENTS.md").read_text(), "after")

    def test_safe_paths_reject_traversal(self):
        for path in ("../elsewhere", "/absolute", "C:/outside", ".agents/../outside", "back\\slash"):
            with self.subTest(path=path), self.assertRaises(m.Conflict):
                m.safe_path(self.root, path)

    def test_symlink_destination_is_rejected(self):
        destination = self.root / "real"
        destination.mkdir()
        try:
            (self.root / ".agents").symlink_to(destination, target_is_directory=True)
        except OSError:
            self.skipTest("OS does not allow creating symlinks")
        with self.assertRaisesRegex(m.Conflict, "Linked"):
            self.apply()

    def test_hardlink_destination_is_rejected(self):
        original = self.root / "original"
        original.write_text("hello")
        try:
            os.link(original, self.root / "AGENTS.md")
        except OSError:
            self.skipTest("Filesystem does not allow hardlinks")
        with self.assertRaisesRegex(m.Conflict, "Hard-linked"):
            self.apply(mode="always-on")

    def test_manifest_cannot_redirect_writes(self):
        self.apply(mode="always-on")
        state = json.loads(json.dumps(self.state))
        state["resources"]["private.txt"] = state["resources"].pop("AGENTS.md")
        (self.root / m.STATE / "manifest.json").write_text(json.dumps(state))
        with self.assertRaisesRegex(m.Conflict, "does not belong"):
            m.load_state(self.root, "project")

    def test_missing_managed_file_reported_as_drift(self):
        self.apply()
        (self.root / ".agents/skills/i-have-adhd/SKILL.md").unlink()
        self.assertIn("drift", m.status(self.root, "project", self.state, "codex"))

    def test_status_does_not_claim_native_install_absent(self):
        code, out, err = self.cli("status", "--project", str(self.root), "--agent", "pi")
        self.assertEqual(code, 0)
        self.assertIn("native/UI installations not inspected", out)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_guided_and_unsupported_no_commands_or_writes(self):
        with mock.patch.object(m.shutil, "which", return_value=None), mock.patch("subprocess.run") as run:
            code, out, err = self.cli("install", "--project", str(self.root), "--agent", "qwen", "--mode", "always-on", "--apply")
            self.assertEqual(code, 2)
            self.assertIn("unsupported", out)
            self.assertNotIn("Native alternative", out)
            run.assert_not_called()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_custom_configuration_is_guided_without_writes(self):
        with mock.patch.object(m.Path, "home", return_value=self.root), mock.patch.dict(os.environ, {"CODEX_HOME": "custom"}):
            code, out, err = self.cli("install", "--user", "--agent", "codex", "--apply")
        self.assertEqual(code, 2)
        self.assertIn("custom configuration", out)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_guided_native_dependency_is_not_installed(self):
        with mock.patch.object(m.Path, "home", return_value=self.root), mock.patch.object(m.shutil, "which", return_value=None), mock.patch("subprocess.run") as run:
            code, out, err = self.cli("install", "--user", "--agent", "qwen", "--apply")
            run.assert_not_called()
        self.assertEqual(code, 2)
        self.assertIn("Dependency missing: qwen", out)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_documented_snippet_is_detected(self):
        (self.root / "AGENTS.md").write_text("## Output style\nThe reader has ADHD. Shape every response.")
        with self.assertRaisesRegex(m.Conflict, "unmanaged"):
            self.apply(mode="always-on")
        self.assertIn("unmanaged", m.status(self.root, "project", self.state, "codex"))

    def test_lock_blocks_competing_run_without_removing_it(self):
        (self.root / m.STATE).mkdir()
        lock = self.root / m.STATE / "lock"
        lock.write_text("other run")
        code, out, err = self.cli("install", "--project", str(self.root), "--agent", "codex", "--apply")
        self.assertEqual(code, 1)
        self.assertTrue(lock.exists())

    def test_scope_required(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            m.main(["install", "--agent", "codex"])

    def test_user_scope_isolated(self):
        with mock.patch.object(m.Path, "home", return_value=self.root):
            code, out, err = self.cli("install", "--user", "--agent", "codex", "--mode", "always-on", "--apply")
        self.assertEqual((code, err), (0, ""))
        self.assertTrue((self.root / ".codex/AGENTS.md").exists())
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_gemini_prompt_uses_canonical_body(self):
        import tomllib
        rendered = m.desired("gemini", "user", "on-demand")[".gemini/commands/i-have-adhd.toml"][1]
        self.assertEqual(tomllib.loads(rendered.decode())["prompt"], m.body() + "\n{{args}}\n")

    def test_unicode_directory_subprocess(self):
        root = self.root / "a\u00e7\u00e3o"
        root.mkdir()
        result = subprocess.run([sys.executable, str(ROOT / "scripts/manage_install.py"), "install",
                                 "--agent", "codex", "--project", str(root), "--apply"],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((root / "AGENTS.md").exists() or (root / ".agents/skills/i-have-adhd/SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
