"""Release metadata checks for the standalone fork."""

import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNTIME_MANIFESTS = (
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "package.json",
    "kimi.plugin.json",
    "gemini-extension.json",
    "qwen-extension.json",
    "plugin.json",
)


class ReleaseMetadataTest(unittest.TestCase):
    def test_all_runtime_manifests_use_version_0_5_0(self):
        for relative_path in RUNTIME_MANIFESTS:
            with self.subTest(manifest=relative_path):
                manifest = json.loads((ROOT / relative_path).read_text(encoding="utf8"))
                self.assertEqual("0.5.0", manifest["version"])

    def test_fork_metadata_preserves_skill_and_plugin_names(self):
        manifests = {
            path: json.loads((ROOT / path).read_text(encoding="utf8"))
            for path in RUNTIME_MANIFESTS
        }
        for path, manifest in manifests.items():
            with self.subTest(manifest=path):
                self.assertEqual("i-have-adhd", manifest["name"])

        claude_marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf8")
        )
        codex_marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf8")
        )
        for marketplace in (claude_marketplace, codex_marketplace):
            self.assertEqual("flyingnobita-i-have-adhd", marketplace["name"])
            for plugin in marketplace["plugins"]:
                self.assertEqual("i-have-adhd", plugin["name"])

        self.assertEqual("flyingnobita", claude_marketplace["owner"]["name"])
        self.assertEqual(
            "flyingnobita", manifests[".claude-plugin/plugin.json"]["author"]["name"]
        )
        self.assertEqual(
            "https://github.com/flyingnobita",
            manifests[".claude-plugin/plugin.json"]["author"]["url"],
        )
        self.assertEqual(
            "https://github.com/flyingnobita/i-have-adhd.git",
            codex_marketplace["plugins"][0]["source"]["url"],
        )
        for path in ("package.json", "kimi.plugin.json", ".codex-plugin/plugin.json"):
            self.assertEqual(
                "https://github.com/flyingnobita/i-have-adhd",
                manifests[path]["homepage"],
            )
        for field in ("name", "version", "description", "license", "homepage"):
            self.assertEqual(manifests["package.json"][field], manifests["kimi.plugin.json"][field])

        readme = (ROOT / "README.md").read_text(encoding="utf8")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf8")
        self.assertIn("Ayoub G.", readme)
        self.assertIn("original author", readme)
        self.assertIn("Copyright (c) 2026 Ayoub Ghriss", license_text)
        self.assertRegex(license_text, r"fork.*flyingnobita|flyingnobita.*fork")

        changelog_path = ROOT / "CHANGELOG.md"
        self.assertTrue(changelog_path.is_file(), "CHANGELOG.md is missing")
        changelog = changelog_path.read_text(encoding="utf8")
        self.assertRegex(
            changelog,
            r"(?m)^- Nov-10, 2026 - \d{2}:\d{2} [AP]M \+08 - .*0\.5\.0",
        )
        self.assertIn("five new eval cases", changelog)
        self.assertIn("no-regression gate", changelog)

        for path in ("AGENTS.md", "CONTRIBUTING.md"):
            text = (ROOT / path).read_text(encoding="utf8")
            self.assertIn("flyingnobita/i-have-adhd", text)
        self.assertNotIn("## AI Agora discussions", (ROOT / "AGENTS.md").read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()
