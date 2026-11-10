"""Checks installation paths in INSTALL.md and translations."""

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ClaudeCodeUpdateTest(unittest.TestCase):
    def test_marketplace_refresh_is_paired_with_plugin_update(self):
        # `claude plugin marketplace update` refreshes only the marketplace
        # listing; the installed copy stays at its old version until
        # `claude plugin update` runs, so the docs must never offer the first alone.
        refresh = re.compile(r"claude plugin marketplace update (?P<name>[a-z0-9-]+)")
        translations = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        self.assertTrue(translations, "No translated installation guides found")
        for path in [ROOT / "INSTALL.md", *translations]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                self.assertRegex(text, r"claude plugin update i-have-adhd@[a-z0-9-]+")
                for block in re.split(r"\n[^\S\n]*\n", text):
                    for match in refresh.finditer(block):
                        update = f"claude plugin update i-have-adhd@{match.group('name')}"
                        self.assertIn(update, block)


class ZedInstallPathTest(unittest.TestCase):
    def test_zed_install_paths(self):
        translations = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        self.assertTrue(translations, "No translated installation guides found")
        for path in [ROOT / "INSTALL.md", *translations]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                marker = "<summary><strong>Zed</strong></summary>"
                self.assertIn(marker, text)
                section = text.split(marker, 1)[1]
                self.assertIn("</details>", section)
                section = section.split("</details>", 1)[0]

                self.assertNotIn("~/.config/zed/skills", section)
                self.assertIn(
                    "mkdir -p ~/.agents/skills\n"
                    "cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/",
                    section,
                )
                self.assertIn("~/.agents/skills/i-have-adhd", section)


class GrokInstallPathTest(unittest.TestCase):
    def test_grok_install_commands(self):
        text = (ROOT / "INSTALL.md").read_text(encoding="utf8")
        marker = "<summary><strong>Grok (<code>grok</code>)</strong></summary>"
        self.assertIn(marker, text)
        section = text.split(marker, 1)[1]
        self.assertIn("</details>", section)
        section = section.split("</details>", 1)[0]

        self.assertRegex(
            section,
            r"grok plugin install (?:ayghri|flyingnobita)/i-have-adhd --trust",
        )
        self.assertIn("grok plugin enable i-have-adhd", section)
        self.assertIn("grok plugin update i-have-adhd", section)
        self.assertIn("grok plugin uninstall i-have-adhd --confirm", section)
        self.assertIn("/i-have-adhd", section)
        self.assertIn("~/.grok/AGENTS.md", section)
        self.assertIn("~/.grok/rules/i-have-adhd.md", section)
        self.assertNotIn("~/.claude/.i-have-adhd-always", section)


class ForkInstallDocsTest(unittest.TestCase):
    def test_install_docs_cover_opt_out_codex_trust_and_opencode_exception(self):
        readme = (ROOT / "README.md").read_text(encoding="utf8")
        install = (ROOT / "INSTALL.md").read_text(encoding="utf8")
        notice = (
            "i-have-adhd: couldn't tell if a human is reading; rules not loaded. "
            "Run /i-have-adhd to turn them on."
        )

        self.assertIn("## Why this fork exists", readme)
        self.assertIn("Original README (upstream ayghri/i-have-adhd)", readme)
        self.assertIn("| Agent | Human | Non-human | Unclear |", readme)
        for row in (
            "| Claude | `CLAUDE_CODE_SESSION_ATTENDED=1` | `CLAUDE_CODE_SESSION_ATTENDED=0` | unset or malformed |",
            "| Codex | parent `codex app-server ... --managed-daemon`, or the interactive TUI's parent `codex` with no subcommand | parent `codex exec` (or `e`) | any other parent |",
            "| Pi | `mode=tui` | `mode=print` or `mode=json` | `mode=rpc` or missing/malformed signals |",
            "| omp | `kind=main` and `mode=tui` | `kind=sub`, `mode=print`, or `mode=json` | main `mode=rpc` or missing/malformed signals |",
            "| OpenCode | top-level session (assumed human) | any `parentID` subagent | the session lookup fails or returns no session, the session ID is missing, or the `parentID` is malformed |",
        ):
            self.assertIn(row, readme)
        for required in (
            notice,
            "~/.local/state/i-have-adhd/decisions.log",
            "I_HAVE_ADHD_LOG=1",
            "I_HAVE_ADHD=0",
            'herdr pane run <pane> "export I_HAVE_ADHD=0"',
            "Orca",
            "scope clause",
            "assumed human",
        ):
            self.assertIn(required, readme)

        for command in (
            "claude plugin uninstall i-have-adhd",
            "claude plugin marketplace remove i-have-adhd",
            "codex plugin remove i-have-adhd",
            "codex plugin marketplace remove i-have-adhd",
            "omp plugin uninstall --scope user i-have-adhd@i-have-adhd",
            "omp plugin marketplace remove i-have-adhd",
            "claude plugin marketplace add flyingnobita/i-have-adhd",
            "claude plugin install i-have-adhd@flyingnobita-i-have-adhd",
            "codex plugin marketplace add flyingnobita/i-have-adhd --ref main",
            "codex plugin add i-have-adhd@flyingnobita-i-have-adhd",
            "omp plugin marketplace add flyingnobita/i-have-adhd",
            "omp plugin install --scope user i-have-adhd@flyingnobita-i-have-adhd",
        ):
            self.assertIn(command, install)
        for required in (
            "uninstall upstream first",
            "same skill name",
            "Node.js",
            "trust",
            "top-level",
            "parentID",
            "V1",
            "assumed human",
            "~/.pi/agent/.i-have-adhd-always",
            "I_HAVE_ADHD=0",
            "I_HAVE_ADHD_LOG=1",
            "~/.local/state/i-have-adhd/decisions.log",
        ):
            self.assertIn(required, install)

        for route in (
            "Antigravity",
            "AstronClaw",
            "Claude Code",
            "Codex",
            "Grok",
            "Gemini CLI",
            "GitHub Copilot",
            "Hermes",
            "Kimi Code CLI",
            "OpenCode",
            "Pi",
            "Oh My Pi (OMP)",
            "Qwen Code",
            "Zed",
            "Cursor, Amp, and any other agent-skills harness",
        ):
            self.assertIn(route, install)

    def test_translations_point_to_fork_and_link_english_gating_docs(self):
        readmes = sorted((ROOT / ".github/readme").glob("README.*.md"))
        installs = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        self.assertEqual(11, len(readmes))
        self.assertEqual(8, len(installs))

        for path in readmes:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                self.assertIn("../../README.md#why-this-fork-exists", text)
                self.assertIn("flyingnobita/i-have-adhd", text)
                historical = re.sub(
                    r"https://github\.com/ayghri/i-have-adhd/(?:issues|pull)/\d+",
                    "",
                    text,
                )
                self.assertNotIn("ayghri/i-have-adhd", historical)

        for path in installs:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                self.assertIn("../../INSTALL.md#fork-installation-notes", text)
                self.assertIn("flyingnobita/i-have-adhd", text)
                self.assertIn("i-have-adhd@flyingnobita-i-have-adhd", text)
                self.assertNotIn("i-have-adhd@i-have-adhd", text)
                historical = re.sub(
                    r"https://github\.com/ayghri/i-have-adhd/(?:issues|pull)/\d+",
                    "",
                    text,
                )
                self.assertNotIn("ayghri/i-have-adhd", historical)


if __name__ == "__main__":
    unittest.main()
