#!/usr/bin/env python3
"""Smoke-test the Pi or OMP package without making a model request."""

from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
RPC_TIMEOUT_SECONDS = 30
SHARED_MANIFEST_FIELDS = ("name", "version", "description", "license", "homepage")


def validate_package_manifest() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf8"))
    kimi = json.loads((ROOT / "kimi.plugin.json").read_text(encoding="utf8"))

    for field in SHARED_MANIFEST_FIELDS:
        assert package.get(field) == kimi.get(field), (
            f"package.json and kimi.plugin.json disagree on {field}"
        )

    assert package.get("pi") == {
        "extensions": ["./extensions/i-have-adhd.ts"],
        "skills": ["./skills"],
    }
    assert package.get("omp") == {
        "extensions": ["./extensions/i-have-adhd.ts"],
    }


class RpcClient:
    def __init__(
        self,
        executable: str,
        env: dict[str, str],
        *args: str,
    ) -> None:
        self.stderr_file = tempfile.TemporaryFile(mode="w+t")
        self.process = subprocess.Popen(
            [executable, "--mode", "rpc", *args],
            cwd=ROOT,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self.stderr_file,
            text=True,
        )
        if self.process.stdout is None:
            raise RuntimeError("Agent RPC stdout is unavailable")

        self.stdout_lines: queue.Queue[str | None] = queue.Queue()
        self.stdout_thread = threading.Thread(
            target=self._read_stdout,
            daemon=True,
        )
        self.stdout_thread.start()

    def _read_stdout(self) -> None:
        if self.process.stdout is None:
            self.stdout_lines.put(None)
            return

        for line in self.process.stdout:
            self.stdout_lines.put(line)
        self.stdout_lines.put(None)

    def _read_stderr(self) -> str:
        self.stderr_file.flush()
        self.stderr_file.seek(0)
        return self.stderr_file.read()

    def request(
        self,
        request_id: str,
        command: dict[str, Any],
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if self.process.stdin is None:
            raise RuntimeError("Agent RPC stdin is unavailable")

        payload = {"id": request_id, **command}
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()

        events: list[dict[str, Any]] = []
        while True:
            try:
                line = self.stdout_lines.get(timeout=RPC_TIMEOUT_SECONDS)
            except queue.Empty as error:
                raise TimeoutError(
                    f"Agent RPC did not respond within {RPC_TIMEOUT_SECONDS} seconds",
                ) from error

            if line is None:
                raise RuntimeError(
                    f"Agent RPC exited before responding: {self._read_stderr()}",
                )

            event = json.loads(line)
            events.append(event)
            if event.get("type") == "response" and event.get("id") == request_id:
                return event, events

    def events_until(
        self,
        predicate: Callable[[dict[str, Any]], bool],
    ) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        while True:
            try:
                line = self.stdout_lines.get(timeout=RPC_TIMEOUT_SECONDS)
            except queue.Empty as error:
                raise TimeoutError(
                    f"Agent RPC did not emit the expected event within "
                    f"{RPC_TIMEOUT_SECONDS} seconds",
                ) from error

            if line is None:
                raise RuntimeError(
                    f"Agent RPC exited before emitting the expected event: "
                    f"{self._read_stderr()}",
                )

            event = json.loads(line)
            events.append(event)
            if predicate(event):
                return events

    def close(self) -> None:
        if self.process.stdin is not None:
            self.process.stdin.close()

        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)

        return_code = self.process.returncode
        stderr = self._read_stderr()
        self.stderr_file.close()

        if return_code not in (0, -15):
            raise RuntimeError(f"Agent RPC exited with {return_code}: {stderr}")


def build_isolated_env(agent_dir: str) -> dict[str, str]:
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.endswith("_API_KEY")
        and key not in {"ANTHROPIC_AUTH_TOKEN", "OPENAI_ACCESS_TOKEN"}
    }
    env.update(
        {
            "PI_CODING_AGENT_DIR": agent_dir,
            "PI_SKIP_VERSION_CHECK": "1",
            "PI_TELEMETRY": "0",
        }
    )
    return env


def status_texts(events: list[dict[str, Any]]) -> list[str | None]:
    return [
        event.get("statusText")
        for event in events
        if event.get("type") == "extension_ui_request"
        and event.get("method") == "setStatus"
        and event.get("statusKey") == "i-have-adhd"
    ]


def message_count(entries_response: dict[str, Any], custom_type: str) -> int:
    return sum(
        1
        for entry in entries_response["data"]["entries"]
        if entry.get("type") == "custom_message"
        and entry.get("customType") == custom_type
    )


def latest_enabled(entries_response: dict[str, Any]) -> bool:
    states = [
        entry.get("data", {}).get("enabled")
        for entry in entries_response["data"]["entries"]
        if entry.get("type") == "custom"
        and entry.get("customType") == "i-have-adhd-state"
    ]
    if not states or not isinstance(states[-1], bool):
        raise AssertionError("No persisted i-have-adhd state found")
    return states[-1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke-test the i-have-adhd extension without a model request."
    )
    parser.add_argument(
        "--runtime",
        choices=("pi", "omp"),
        default="pi",
        help="Agent runtime to exercise (default: pi)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_package_manifest()
    executable = shutil.which(args.runtime)
    if executable is None:
        raise RuntimeError(f"{args.runtime} executable is not available")

    with tempfile.TemporaryDirectory(
        prefix=f"i-have-adhd-{args.runtime}-"
    ) as agent_dir:
        env = build_isolated_env(agent_dir)
        if args.runtime == "omp":
            env.pop("PI_CODING_AGENT_DIR", None)
        if args.runtime == "pi":
            subprocess.run(
                [executable, "install", str(ROOT)],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
        extension_args = (
            []
            if args.runtime == "pi"
            else ["--no-extensions", "-e", str(ROOT)]
        )

        reload_probe = Path(agent_dir, "reload-probe.ts")
        passthrough_probe_flag = Path(agent_dir, "passthrough-probe-enabled")
        reload_probe_source = """import { existsSync } from \"node:fs\";
import type { ExtensionAPI } from \"@earendil-works/pi-coding-agent\";
const passthroughProbeFlag = __PASSTHROUGH_PROBE_FLAG__;
export default function (pi: ExtensionAPI) {
  pi.registerCommand(\"reload-probe\", {
    description: \"Reload Pi for smoke testing\",
    handler: async (_args, ctx) => { await ctx.reload(); },
  });
  pi.on(\"input\", async (event) => {
    if (!existsSync(passthroughProbeFlag) || event.text.trim().toLowerCase() !== \"normal mode\") {
      return { action: \"continue\" };
    }
    pi.appendEntry(\"passthrough-probe\", { seen: true });
    return { action: \"handled\" };
  });
}
"""
        reload_probe.write_text(
            reload_probe_source.replace(
                "__PASSTHROUGH_PROBE_FLAG__",
                json.dumps(str(passthrough_probe_flag)),
            ),
            encoding="utf8",
        )

        client = RpcClient(
            executable,
            env,
            "--no-session",
            *extension_args,
            "-e",
            str(reload_probe),
            "--adhd",
        )
        if args.runtime == "omp":
            try:
                startup_events = client.events_until(
                    lambda event: event.get("type")
                    == "available_commands_update",
                )
                command_event = startup_events[-1]
                command_names = {
                    command["name"]
                    for command in command_event["commands"]
                }
                assert "i-have-adhd" in command_names
                assert "skill:i-have-adhd" in command_names
                assert any(
                    "ADHD ON" in (text or "")
                    for text in status_texts(startup_events)
                )
            finally:
                client.close()

            print("omp extension smoke test passed")
            return

        try:
            commands, startup_events = client.request("commands", {"type": "get_commands"})
            command_names = {command["name"] for command in commands["data"]["commands"]}
            assert "i-have-adhd" in command_names
            assert "skill:i-have-adhd" in command_names
            assert any("ADHD ON" in (text or "") for text in status_texts(startup_events))

            entries, _ = client.request("entries-startup", {"type": "get_entries"})
            assert message_count(entries, "i-have-adhd-rules") == 1
            assert message_count(entries, "i-have-adhd-disabled") == 0

            reloaded, reload_events = client.request(
                "reload-enabled",
                {"type": "prompt", "message": "/reload-probe"},
            )
            assert reloaded["success"] is True
            assert any("ADHD ON" in (text or "") for text in status_texts(reload_events))

            entries, _ = client.request("entries-reloaded", {"type": "get_entries"})
            assert message_count(entries, "i-have-adhd-rules") == 1, (
                "Rules were injected twice for one active session"
            )

            toggled_off, toggle_off_events = client.request(
                "toggle-off",
                {"type": "prompt", "message": "/i-have-adhd"},
            )
            assert toggled_off["success"] is True
            assert None in status_texts(toggle_off_events)

            entries, _ = client.request("entries-toggled-off", {"type": "get_entries"})
            assert latest_enabled(entries) is False
            assert message_count(entries, "i-have-adhd-disabled") == 1

            reloaded, reload_events = client.request(
                "reload-disabled",
                {"type": "prompt", "message": "/reload-probe"},
            )
            assert reloaded["success"] is True
            assert not any("ADHD ON" in (text or "") for text in status_texts(reload_events))

            entries, _ = client.request("entries-reload-disabled", {"type": "get_entries"})
            assert message_count(entries, "i-have-adhd-rules") == 1
            assert message_count(entries, "i-have-adhd-disabled") == 1

            toggled_on, toggle_on_events = client.request(
                "toggle-on",
                {"type": "prompt", "message": "/i-have-adhd"},
            )
            assert toggled_on["success"] is True
            assert any("ADHD ON" in (text or "") for text in status_texts(toggle_on_events))

            entries, _ = client.request("entries-toggled-on", {"type": "get_entries"})
            assert latest_enabled(entries) is True
            assert message_count(entries, "i-have-adhd-rules") == 2

            explicit_off, _ = client.request(
                "explicit-off",
                {"type": "prompt", "message": "/i-have-adhd off"},
            )
            assert explicit_off["success"] is True

            skill, skill_events = client.request(
                "skill-alias",
                {"type": "prompt", "message": "/skill:i-have-adhd"},
            )
            assert skill["success"] is True
            assert not any(event.get("type") == "agent_start" for event in skill_events)

            entries, _ = client.request("entries-enabled", {"type": "get_entries"})
            assert latest_enabled(entries) is True
            assert message_count(entries, "i-have-adhd-rules") == 3

            stopped, stop_events = client.request(
                "stop-phrase",
                {"type": "prompt", "message": "normal mode"},
            )
            assert stopped["success"] is True
            assert None in status_texts(stop_events)

            entries, _ = client.request("entries-stopped", {"type": "get_entries"})
            assert latest_enabled(entries) is False

            passthrough_probe_flag.touch()
            passthrough, _ = client.request(
                "disabled-passthrough",
                {"type": "prompt", "message": "normal mode"},
            )
            assert passthrough["success"] is True

            entries, _ = client.request("entries-passthrough", {"type": "get_entries"})
            assert any(
                entry.get("type") == "custom"
                and entry.get("customType") == "passthrough-probe"
                and entry.get("data", {}).get("seen") is True
                for entry in entries["data"]["entries"]
            ), "Disabled mode swallowed ordinary input"
        finally:
            client.close()

        if args.runtime == "pi":
            Path(agent_dir, ".i-have-adhd-always").touch()
            always_on = RpcClient(
                executable,
                env,
                "--no-session",
                *extension_args,
            )
            try:
                _, always_on_events = always_on.request(
                    "always-on",
                    {"type": "get_state"},
                )
                assert any(
                    "ADHD ON" in (text or "")
                    for text in status_texts(always_on_events)
                )
            finally:
                always_on.close()

    print(f"{args.runtime} extension smoke test passed")


if __name__ == "__main__":
    main()
