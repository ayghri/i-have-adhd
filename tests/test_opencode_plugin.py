import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Exercise both runtime APIs against the same fixtures.
INJECTION_MODES = ["context", "v1-context"]


@unittest.skipUnless(shutil.which("node"), "node is required for the OpenCode plugin")
class OpenCodePluginTest(unittest.TestCase):
    """Mirror tests/test_always_on_hooks.py for the OpenCode server plugin: the
    always-on flag gates injection, and frontmatter stripping matches the hooks.

    V2 registers through `ctx.skill.transform` and `ctx.command.transform`; V1
    mutates the config object in its `config` hook. Both paths are covered."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name).resolve() / "plugin"
        shutil.copytree(ROOT / ".opencode", self.plugin_root / ".opencode")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        # The plugin reads its flag from $XDG_CONFIG_HOME/opencode/.i-have-adhd-always.
        self.config_dir = Path(self.temp_dir.name) / "config"
        (self.config_dir / "opencode").mkdir(parents=True)
        self.home_dir = Path(self.temp_dir.name) / "home"
        self.home_dir.mkdir()
        self.log = self.home_dir / ".local" / "state" / "i-have-adhd" / "decisions.log"

    def run_plugin(self, mode=None, options=None, extra_env=None):
        env = os.environ.copy()
        for key in ("I_HAVE_ADHD", "I_HAVE_ADHD_LOG"):
            env.pop(key, None)
        env.update(
            {
                "HOME": str(self.home_dir),
                "USERPROFILE": str(self.home_dir),
                "XDG_CONFIG_HOME": str(self.config_dir),
                "XDG_STATE_HOME": str(self.home_dir / "state"),
            }
        )
        env.update(extra_env or {})
        args = [
            "node",
            str(ROOT / "tests" / "opencode_plugin_driver.mjs"),
            str(self.plugin_root / ".opencode" / "plugins" / "i-have-adhd.mjs"),
        ]
        if mode:
            args.append(mode)
        if options is not None:
            args.append(json.dumps(options))
        return subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def context(self, mode, extra_env=None, **options):
        if "sessionID" not in options:
            options["sessionID"] = "ses_default"
        elif options["sessionID"] is None:
            del options["sessionID"]
        result = self.run_plugin(mode, options or None, extra_env=extra_env)
        self.assertEqual(0, result.returncode, result.stderr)
        if result.stdout == "":
            return {"system": "", "toasts": [], "lookups": 0}
        payload = json.loads(result.stdout)
        return {
            "system": payload.get("system", ""),
            "toasts": payload.get("toasts", []),
            "lookups": payload.get("lookups", 0),
        }

    def contexts(self, mode, calls, extra_env=None):
        result = self.run_plugin(mode, calls, extra_env=extra_env)
        self.assertEqual(0, result.returncode, result.stderr)
        if result.stdout == "":
            return {"systems": [], "toasts": [], "lookups": 0}
        payload = json.loads(result.stdout)
        return {
            "systems": payload.get("systems", []),
            "toasts": payload.get("toasts", []),
            "lookups": payload.get("lookups", 0),
        }

    def opt_in(self):
        (self.config_dir / "opencode" / ".i-have-adhd-always").touch()

    def write_skill(self, text):
        (self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md").write_text(text)

    # --- always-on injection, asserted through both APIs ---

    def test_silent_without_opt_in_flag(self):
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.run_plugin(mode)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("", result.stdout)
        self.assertFalse(self.log.exists())
        self.assertFalse((self.home_dir / ".local").exists())

    def test_top_level_sessions_inject_and_v1_shows_assumed_human_toast(self):
        self.opt_in()

        v2 = self.context("context")
        self.assertIn("ADHD MODE ACTIVE (always-on)", v2["system"])
        self.assertIn("Working memory is small", v2["system"])
        self.assertEqual([], v2["toasts"], "V2 has no toast call")

        v1 = self.context("v1-context")
        self.assertEqual(v2["system"], v1["system"])
        self.assertEqual(1, len(v1["toasts"]))
        self.assertIn("assumed human", v1["toasts"][0])

    def test_repeated_transforms_in_same_session_toast_and_log_once(self):
        self.opt_in()
        res = self.contexts(
            "v1-context",
            [{"sessionID": "ses_repeat"}, {"sessionID": "ses_repeat"}],
            extra_env={"I_HAVE_ADHD_LOG": "1"},
        )
        self.assertEqual(2, len(res["systems"]))
        self.assertIn("ADHD MODE ACTIVE", res["systems"][0])
        self.assertIn("ADHD MODE ACTIVE", res["systems"][1])
        self.assertEqual(1, len(res["toasts"]))
        self.assertIn("assumed human", res["toasts"][0])
        self.assertTrue(self.log.exists())
        log_lines = self.log.read_text().strip().splitlines()
        self.assertEqual(1, len(log_lines))
        entry = json.loads(log_lines[0])
        self.assertEqual("opencode", entry["agent"])
        self.assertEqual("injected", entry["result"])

    def test_distinct_sessions_get_independent_decisions(self):
        self.opt_in()
        res = self.contexts(
            "v1-context",
            [{"sessionID": "ses_a"}, {"sessionID": "ses_b"}],
            extra_env={"I_HAVE_ADHD_LOG": "1"},
        )
        self.assertEqual(2, len(res["systems"]))
        self.assertIn("ADHD MODE ACTIVE", res["systems"][0])
        self.assertIn("ADHD MODE ACTIVE", res["systems"][1])
        self.assertEqual(2, len(res["toasts"]))
        self.assertTrue(self.log.exists())
        log_lines = self.log.read_text().strip().splitlines()
        self.assertEqual(2, len(log_lines))

    def test_interleaved_sessions_maintain_distinct_caches(self):
        self.opt_in()
        res = self.contexts(
            "v1-context",
            [
                {"sessionID": "ses_1"},
                {"sessionID": "ses_2"},
                {"sessionID": "ses_1"},
                {"sessionID": "ses_2"},
            ],
            extra_env={"I_HAVE_ADHD_LOG": "1"},
        )
        self.assertEqual(4, len(res["systems"]))
        for sys in res["systems"]:
            self.assertIn("ADHD MODE ACTIVE", sys)
        self.assertEqual(2, len(res["toasts"]))
        self.assertTrue(self.log.exists())
        log_lines = self.log.read_text().strip().splitlines()
        self.assertEqual(2, len(log_lines))

    def test_subagent_parent_id_skips_injection_and_toast(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.context(mode, parentID="ses_parent")
                self.assertEqual("", result["system"])
                self.assertEqual([], result["toasts"])

    def test_subagent_session_lookup_skips_injection_and_toast(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.context(
                    mode,
                    sessionID="ses_child",
                    sessions={"ses_child": {"id": "ses_child", "parentID": "ses_parent"}},
                )
                self.assertEqual("", result["system"])
                self.assertEqual([], result["toasts"])

    def test_lookup_error_fails_closed_as_unclear(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.context(
                    mode,
                    sessionID="ses_err",
                    failLookup=True,
                )
                self.assertEqual("", result["system"])
                self.assertEqual([], result["toasts"])

    def test_v1_session_get_resolving_error_fails_closed_as_unclear(self):
        self.opt_in()
        if self.log.exists():
            self.log.unlink()
        res = self.context(
            "v1-context",
            sessionID="ses_v1_err_obj",
            sessions={"ses_v1_err_obj": {"error": {"message": "Not found"}}},
            extra_env={"I_HAVE_ADHD_LOG": "1"},
        )
        self.assertEqual("", res["system"])
        self.assertEqual([], res["toasts"])
        self.assertTrue(self.log.exists())
        log_lines = self.log.read_text().strip().splitlines()
        self.assertEqual(1, len(log_lines))
        entry = json.loads(log_lines[0])
        self.assertEqual("skipped-unclear", entry["result"])
        self.assertEqual("unknown", entry["signals"]["parentId"])

    def test_v1_session_get_shapes_resolution(self):
        self.opt_in()
        sub_res = self.context(
            "v1-context",
            sessionID="ses_wrapped_child",
            sessions={"ses_wrapped_child": {"data": {"id": "ses_wrapped_child", "parentID": "ses_parent"}}},
        )
        self.assertEqual("", sub_res["system"])
        self.assertEqual([], sub_res["toasts"])

        top_res = self.context(
            "v1-context",
            sessionID="ses_wrapped_top",
            sessions={"ses_wrapped_top": {"data": {"id": "ses_wrapped_top"}}},
        )
        self.assertIn("ADHD MODE ACTIVE", top_res["system"])
        self.assertEqual(1, len(top_res["toasts"]))

        for invalid_session in ({}, None):
            with self.subTest(invalid=invalid_session):
                invalid_res = self.context(
                    "v1-context",
                    sessionID="ses_invalid",
                    sessions={"ses_invalid": invalid_session},
                )
                self.assertEqual("", invalid_res["system"])
                self.assertEqual([], invalid_res["toasts"])

    def test_lookup_runs_once_per_session_id_across_repeated_transforms(self):
        self.opt_in()
        res = self.contexts(
            "v1-context",
            [{"sessionID": "ses_repeat_lookup"}, {"sessionID": "ses_repeat_lookup"}],
            extra_env={"I_HAVE_ADHD_LOG": "1"},
        )
        self.assertEqual(2, len(res["systems"]))
        self.assertIn("ADHD MODE ACTIVE", res["systems"][0])
        self.assertIn("ADHD MODE ACTIVE", res["systems"][1])
        self.assertEqual(1, res.get("lookups"))

    def test_missing_session_id_is_unclear_and_logs_once(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                if self.log.exists():
                    self.log.unlink()
                res = self.contexts(
                    mode,
                    [{"sessionID": None}, {"sessionID": None}],
                    extra_env={"I_HAVE_ADHD_LOG": "1"},
                )
                self.assertEqual(2, len(res["systems"]))
                self.assertEqual("", res["systems"][0])
                self.assertEqual("", res["systems"][1])
                self.assertEqual([], res["toasts"])
                self.assertTrue(self.log.exists())
                log_lines = self.log.read_text().strip().splitlines()
                self.assertEqual(1, len(log_lines))
                entry = json.loads(log_lines[0])
                self.assertEqual("skipped-unclear", entry["result"])
                self.assertEqual("unknown", entry["signals"]["parentId"])

    def test_session_deleted_evicts_cache_entry(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                steps = [
                    {"type": "transform", "call": {"sessionID": "ses_evict"}},
                    {
                        "type": "event",
                        "event": {
                            "type": "session.deleted",
                            "data": {"sessionID": "ses_evict"},
                            "properties": {"info": {"id": "ses_evict"}},
                        },
                    },
                    {"type": "transform", "call": {"sessionID": "ses_evict"}},
                ]
                res = self.run_plugin(mode, {"steps": steps})
                self.assertEqual(0, res.returncode, res.stderr)
                payload = json.loads(res.stdout)
                self.assertEqual(2, len(payload["systems"]))
                self.assertIn("ADHD MODE ACTIVE", payload["systems"][0])
                self.assertIn("ADHD MODE ACTIVE", payload["systems"][1])
                self.assertEqual(2, payload.get("lookups"))

    def test_v2_async_stream_evicts_cache_entry(self):
        self.opt_in()
        steps = [
            {"type": "transform", "call": {"sessionID": "ses_v2_evict"}},
            {
                "type": "event",
                "event": {
                    "type": "session.deleted",
                    "data": {"sessionID": "ses_v2_evict"},
                },
            },
            {"type": "transform", "call": {"sessionID": "ses_v2_evict"}},
        ]
        res = self.run_plugin("context", {"steps": steps})
        self.assertEqual(0, res.returncode, res.stderr)
        payload = json.loads(res.stdout)
        self.assertEqual(2, len(payload["systems"]))
        self.assertIn("ADHD MODE ACTIVE", payload["systems"][0])
        self.assertIn("ADHD MODE ACTIVE", payload["systems"][1])
        self.assertEqual(2, payload.get("lookups"))

    def test_real_v2_session_deleted_envelope_evicts_cache(self):
        self.opt_in()
        steps = [
            {"type": "transform", "call": {"sessionID": "ses_v2_real"}},
            {
                "type": "event",
                "event": {
                    "id": "evt_1c4d305de001N54WlhS9KdELuF",
                    "created": 1794303526366,
                    "type": "session.deleted",
                    "durable": {"aggregateID": "ses_v2_real", "seq": 13, "version": 2},
                    "data": {"sessionID": "ses_v2_real"},
                },
            },
            {"type": "transform", "call": {"sessionID": "ses_v2_real"}},
        ]
        res = self.run_plugin("context", {"steps": steps})
        self.assertEqual(0, res.returncode, res.stderr)
        payload = json.loads(res.stdout)
        self.assertEqual(2, len(payload["systems"]))
        self.assertIn("ADHD MODE ACTIVE", payload["systems"][0])
        self.assertIn("ADHD MODE ACTIVE", payload["systems"][1])
        self.assertEqual(2, payload.get("lookups"))

    def test_event_with_only_event_id_evicts_nothing(self):
        self.opt_in()
        steps = [
            {"type": "transform", "call": {"sessionID": "evt_only_no_session"}},
            {
                "type": "event",
                "event": {
                    "id": "evt_only_no_session",
                    "type": "session.deleted",
                },
            },
            {"type": "transform", "call": {"sessionID": "evt_only_no_session"}},
        ]
        res = self.run_plugin("context", {"steps": steps})
        self.assertEqual(0, res.returncode, res.stderr)
        payload = json.loads(res.stdout)
        self.assertEqual(2, len(payload["systems"]))
        self.assertEqual(1, payload.get("lookups"))

    def test_v1_session_deleted_shape_evicts_cache(self):
        self.opt_in()
        steps = [
            {"type": "transform", "call": {"sessionID": "ses_v1_info"}},
            {
                "type": "event",
                "event": {
                    "type": "session.deleted",
                    "properties": {"info": {"id": "ses_v1_info"}},
                },
            },
            {"type": "transform", "call": {"sessionID": "ses_v1_info"}},
        ]
        res = self.run_plugin("v1-context", {"steps": steps})
        self.assertEqual(0, res.returncode, res.stderr)
        payload = json.loads(res.stdout)
        self.assertEqual(2, len(payload["systems"]))
        self.assertIn("ADHD MODE ACTIVE", payload["systems"][0])
        self.assertIn("ADHD MODE ACTIVE", payload["systems"][1])
        self.assertEqual(2, payload.get("lookups"))

    def test_aggregate_id_evicts_cache_only_when_starting_with_ses(self):
        self.opt_in()
        # Case 1: aggregateID starting with ses_ evicts
        steps_match = [
            {"type": "transform", "call": {"sessionID": "ses_agg_1"}},
            {
                "type": "event",
                "event": {
                    "type": "session.deleted",
                    "durable": {"aggregateID": "ses_agg_1"},
                },
            },
            {"type": "transform", "call": {"sessionID": "ses_agg_1"}},
        ]
        res = self.run_plugin("context", {"steps": steps_match})
        self.assertEqual(0, res.returncode, res.stderr)
        payload = json.loads(res.stdout)
        self.assertEqual(2, payload.get("lookups"))

        # Case 2: aggregateID not starting with ses_ does not evict
        steps_no_match = [
            {"type": "transform", "call": {"sessionID": "ses_keep"}},
            {
                "type": "event",
                "event": {
                    "type": "session.deleted",
                    "durable": {"aggregateID": "user_123"},
                },
            },
            {"type": "transform", "call": {"sessionID": "ses_keep"}},
        ]
        res = self.run_plugin("context", {"steps": steps_no_match})
        self.assertEqual(0, res.returncode, res.stderr)
        payload = json.loads(res.stdout)
        self.assertEqual(1, payload.get("lookups"))

    def test_opt_out_wins_over_top_level_assumption(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.run_plugin(mode, extra_env={"I_HAVE_ADHD": "0"})
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("", result.stdout)

    def test_injects_ruleset_when_opted_in(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.context(mode)
                self.assertIn("ADHD MODE ACTIVE (always-on)", result["system"])
                self.assertIn("Working memory is small", result["system"])

    def test_strips_frontmatter_with_trailing_whitespace(self):
        self.write_skill("---   \nname: fixture\n--- \t\nFixture body.\n")
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.context(mode)
                self.assertNotIn("name: fixture", result["system"])
                self.assertIn("\n\nFixture body.", result["system"])

    def test_keeps_content_when_frontmatter_is_unclosed(self):
        self.write_skill("---\nname: fixture\nFixture body, fence never closed.\n")
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.context(mode)
                self.assertIn("Fixture body, fence never closed.", result["system"])

    def test_both_apis_share_the_same_injected_text(self):
        self.opt_in()
        self.assertEqual(self.context("context")["system"], self.context("v1-context")["system"])

    # --- V2 registration ---

    def test_setup_registers_the_slash_command(self):
        # Regression test for #140: a global install (plugin loaded from a
        # path outside any checkout, no project-scope .opencode/command/
        # directory in play) must still get /i-have-adhd, because OpenCode's
        # skill-sourced commands are not surfaced in the TUI's `/` menu.
        result = self.run_plugin(mode="command")
        self.assertEqual(0, result.returncode, result.stderr)
        command = json.loads(result.stdout)[0]
        self.assertEqual("i-have-adhd", command["name"])
        self.assertIn("ADHD", command["description"])
        self.assertIn("stop adhd mode", command["template"])

    def test_setup_registers_the_skill(self):
        result = self.run_plugin(mode="skill")
        self.assertEqual(0, result.returncode, result.stderr)
        skill = json.loads(result.stdout)[0]
        self.assertEqual("i-have-adhd", skill["id"])
        self.assertEqual(
            str(self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"), skill["path"]
        )
        self.assertIn("ADHD", skill["description"])
        self.assertNotIn("---", skill["content"])

    def test_missing_command_keeps_skill_registration(self):
        (self.plugin_root / ".opencode/command/i-have-adhd.md").unlink()
        result = self.run_plugin(mode="command")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], json.loads(result.stdout))
        result = self.run_plugin(mode="skill")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("i-have-adhd", json.loads(result.stdout)[0]["id"])

    def test_malformed_command_keeps_skill_registration(self):
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        for text in ["---\n{broken}\n---\nBody", '---\n{"description":"unclosed"}\nBody']:
            with self.subTest(text=text):
                command.write_text(text)
                result = self.run_plugin(mode="command")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual([], json.loads(result.stdout))
                result = self.run_plugin(mode="skill")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("i-have-adhd", json.loads(result.stdout)[0]["id"])

    # --- V1 config registration ---

    def test_v1_config_hook_registers_the_slash_command(self):
        result = self.run_plugin(mode="v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        command = config["command"]["i-have-adhd"]
        self.assertIn("ADHD", command["description"])
        self.assertIn("stop adhd mode", command["template"])

    def test_v1_config_hook_registers_the_skills_path(self):
        result = self.run_plugin(mode="v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertIn(str(self.plugin_root / "skills"), config["skills"]["paths"])

    def test_v1_config_preserves_existing_command(self):
        custom = {"description": "User command", "template": "Keep this", "agent": "plan"}
        result = self.run_plugin("v1-config", {"command": {"i-have-adhd": custom}})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(custom, json.loads(result.stdout)["command"]["i-have-adhd"])

    def test_v1_repeated_config_does_not_duplicate_skill_paths(self):
        result = self.run_plugin("v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [str(self.plugin_root / "skills")], json.loads(result.stdout)["skills"]["paths"]
        )

    def test_v1_command_preserves_metadata_and_trims_template(self):
        metadata = {"description": 'ADHD: "focus"\nnext line', "agent": "plan",
                    "model": "fixture/model", "subagent": True}
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        command.write_bytes(("---  \r\n" + json.dumps(metadata) +
                             "\r\n--- \t\r\n\r\nUse the skill.\r\n\r\n").encode())
        result = self.run_plugin("v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({**metadata, "template": "Use the skill."},
                         json.loads(result.stdout)["command"]["i-have-adhd"])

    def test_v1_missing_command_keeps_skill_discovery(self):
        (self.plugin_root / ".opencode/command/i-have-adhd.md").unlink()
        result = self.run_plugin("v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertNotIn("i-have-adhd", config["command"])
        self.assertEqual([str(self.plugin_root / "skills")], config["skills"]["paths"])

    def test_v1_malformed_command_does_not_leak_frontmatter_into_prompt(self):
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        for text in ["---\n{broken}\n---\nBody", '---\n{"description":"unclosed"}\nBody']:
            with self.subTest(text=text):
                command.write_text(text)
                result = self.run_plugin("v1-config")
                self.assertEqual(0, result.returncode, result.stderr)
                config = json.loads(result.stdout)
                self.assertNotIn("i-have-adhd", config["command"])
                self.assertEqual([str(self.plugin_root / "skills")], config["skills"]["paths"])


    def test_js_mirror_reexports_the_implementation(self):
        # Discovery uses .js; re-exporting must preserve the module identity.
        mirror = ROOT / ".opencode" / "plugins" / "i-have-adhd.js"
        impl = ROOT / ".opencode" / "plugins" / "i-have-adhd.mjs"
        self.assertTrue(mirror.is_file(), "missing V2 auto-discovery mirror")
        self.assertTrue(impl.is_file())

        env = os.environ.copy()
        env["HOME"] = str(self.home_dir)
        env["USERPROFILE"] = str(self.home_dir)
        env["XDG_CONFIG_HOME"] = str(self.config_dir)
        script = (
            "const a = (await import(process.argv[1])).default;"
            "const b = (await import(process.argv[2])).default;"
            "process.stdout.write(JSON.stringify({"
            "same: a === b,"
            "id: a.id, keys: Object.keys(a).sort()}));"
        )
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script, mirror.as_uri(), impl.as_uri()],
            check=False, capture_output=True, text=True, env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        mirror_export = json.loads(result.stdout)
        self.assertTrue(mirror_export["same"], "mirror does not re-export the implementation")
        self.assertEqual("i-have-adhd", mirror_export["id"])
        self.assertEqual(["id", "server", "setup"], mirror_export["keys"])


if __name__ == "__main__":
    unittest.main()
