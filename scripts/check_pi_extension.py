#!/usr/bin/env python3
"""Smoke-test the Pi package without making a model request."""

from __future__ import annotations

import json
import os
import queue
import subprocess
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RPC_TIMEOUT_SECONDS = 30


class RpcClient:
    def __init__(self, env: dict[str, str], *args: str) -> None:
        self.stderr_file = tempfile.TemporaryFile(mode="w+t")
        self.process = subprocess.Popen(
            ["pi", "--mode", "rpc", *args],
            cwd=ROOT,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self.stderr_file,
            text=True,
        )
        if self.process.stdout is None:
            raise RuntimeError("Pi RPC stdout is unavailable")

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
            raise RuntimeError("Pi RPC stdin is unavailable")

        payload = {"id": request_id, **command}
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()

        events: list[dict[str, Any]] = []
        while True:
            try:
                line = self.stdout_lines.get(timeout=RPC_TIMEOUT_SECONDS)
            except queue.Empty as error:
                raise TimeoutError(
                    f"Pi RPC did not respond within {RPC_TIMEOUT_SECONDS} seconds",
                ) from error

            if line is None:
                raise RuntimeError(
                    f"Pi RPC exited before responding: {self._read_stderr()}",
                )

            event = json.loads(line)
            events.append(event)
            if event.get("type") == "response" and event.get("id") == request_id:
                return event, events

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
            raise RuntimeError(f"Pi RPC exited with {return_code}: {stderr}")


def _status_texts(events: list[dict[str, Any]]) -> list[str | None]:
    return [
        event.get("statusText")
        for event in events
        if event.get("type") == "extension_ui_request"
        and event.get("method") == "setStatus"
        and event.get("statusKey") == "i-have-adhd"
    ]


def _message_count(entries: list[dict[str, Any]], custom_type: str) -> int:
    return sum(
        1
        for entry in entries
        if entry.get("type") == "custom_message" and entry.get("customType") == custom_type
    )


def _latest_enabled(entries: list[dict[str, Any]]) -> bool | None:
    states = [
        entry.get("data", {}).get("enabled")
        for entry in entries
        if entry.get("type") == "custom" and entry.get("customType") == "i-have-adhd-state"
    ]
    if not states:
        return None
    if not isinstance(states[-1], bool):
        raise AssertionError("Persisted i-have-adhd state is not a boolean")
    return states[-1]


def _passthrough_seen(entries: list[dict[str, Any]]) -> bool:
    return any(
        entry.get("type") == "custom"
        and entry.get("customType") == "passthrough-probe"
        and entry.get("data", {}).get("seen") is True
        for entry in entries
    )


def write_reload_probe(agent_dir: str) -> tuple[Path, Path]:
    """Write the extension used to drive /reload and passthrough-input probes."""
    probe_path = Path(agent_dir, "reload-probe.ts")
    passthrough_flag = Path(agent_dir, "passthrough-probe-enabled")
    source = """import { existsSync } from "node:fs";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
const passthroughProbeFlag = __PASSTHROUGH_PROBE_FLAG__;
export default function (pi: ExtensionAPI) {
  pi.registerCommand("reload-probe", {
    description: "Reload Pi for smoke testing",
    handler: async (_args, ctx) => { await ctx.reload(); },
  });
  pi.on("input", async (event) => {
    if (!existsSync(passthroughProbeFlag) || event.text.trim().toLowerCase() !== "normal mode") {
      return { action: "continue" };
    }
    pi.appendEntry("passthrough-probe", { seen: true });
    return { action: "handled" };
  });
}
"""
    probe_path.write_text(
        source.replace("__PASSTHROUGH_PROBE_FLAG__", json.dumps(str(passthrough_flag))),
        encoding="utf8",
    )
    return probe_path, passthrough_flag


@dataclass
class SessionState:
    rules_count: int
    disabled_count: int
    enabled: bool | None
    passthrough_seen: bool


class Session:
    """A Pi RPC session, speaking in ADHD-mode terms: toggle, injection, stop phrase.

    Wraps the raw request/response/event protocol of `RpcClient` so callers
    describe behaviour instead of restating the wire format.
    """

    def __init__(self, client: RpcClient) -> None:
        self._client = client
        self._request_count = 0
        self._last_events: list[dict[str, Any]] = []

    def _request(self, command: dict[str, Any]) -> dict[str, Any]:
        self._request_count += 1
        request_id = f"{command['type']}-{self._request_count}"
        response, self._last_events = self._client.request(request_id, command)
        return response

    @property
    def status(self) -> str | None:
        """The status the last command reported: text, or None if it cleared it.

        Every command asserted on below is expected to report status, so a
        command that emitted no setStatus at all is a failure rather than a
        cleared status - otherwise `status is None` would pass vacuously.
        """
        texts = _status_texts(self._last_events)
        if not texts:
            raise AssertionError(
                "expected a setStatus event for i-have-adhd, got none"
            )
        return texts[-1]

    @property
    def triggered_agent(self) -> bool:
        return any(event.get("type") == "agent_start" for event in self._last_events)

    def commands(self) -> set[str]:
        response = self._request({"type": "get_commands"})
        return {command["name"] for command in response["data"]["commands"]}

    def prompt(self, message: str) -> bool:
        response = self._request({"type": "prompt", "message": message})
        return response["success"]

    def toggle(self) -> bool:
        return self.prompt("/i-have-adhd")

    def explicit_off(self) -> bool:
        return self.prompt("/i-have-adhd off")

    def skill_alias(self) -> bool:
        return self.prompt("/skill:i-have-adhd")

    def reload(self) -> bool:
        return self.prompt("/reload-probe")

    def stop_phrase(self) -> bool:
        return self.prompt("normal mode")

    def get_state(self) -> None:
        self._request({"type": "get_state"})

    def state(self) -> SessionState:
        response = self._request({"type": "get_entries"})
        entries = response["data"]["entries"]
        return SessionState(
            rules_count=_message_count(entries, "i-have-adhd-rules"),
            disabled_count=_message_count(entries, "i-have-adhd-disabled"),
            enabled=_latest_enabled(entries),
            passthrough_seen=_passthrough_seen(entries),
        )

    def close(self) -> None:
        self._client.close()


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


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="i-have-adhd-pi-") as agent_dir:
        env = build_isolated_env(agent_dir)
        subprocess.run(
            ["pi", "install", str(ROOT)],
            cwd=ROOT,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )

        reload_probe, passthrough_probe_flag = write_reload_probe(agent_dir)
        session = Session(
            RpcClient(env, "--no-session", "-e", str(reload_probe), "--adhd")
        )
        try:
            commands = session.commands()
            assert "i-have-adhd" in commands
            assert "skill:i-have-adhd" in commands
            assert session.status and "ADHD ON" in session.status

            state = session.state()
            assert state.rules_count == 1
            assert state.disabled_count == 0

            assert session.reload() is True
            assert session.status and "ADHD ON" in session.status

            state = session.state()
            assert state.rules_count == 1, "Rules were injected twice for one active session"

            assert session.toggle() is True
            assert session.status is None

            state = session.state()
            assert state.enabled is False
            assert state.disabled_count == 1

            assert session.reload() is True
            assert session.status is None

            state = session.state()
            assert state.rules_count == 1
            assert state.disabled_count == 1

            assert session.toggle() is True
            assert session.status and "ADHD ON" in session.status

            state = session.state()
            assert state.enabled is True
            assert state.rules_count == 2

            assert session.explicit_off() is True

            assert session.skill_alias() is True
            assert not session.triggered_agent

            state = session.state()
            assert state.enabled is True
            assert state.rules_count == 3

            assert session.stop_phrase() is True
            assert session.status is None

            state = session.state()
            assert state.enabled is False

            passthrough_probe_flag.touch()
            assert session.prompt("normal mode") is True

            state = session.state()
            assert state.passthrough_seen, "Disabled mode swallowed ordinary input"
        finally:
            session.close()

        Path(agent_dir, ".i-have-adhd-always").touch()
        always_on = Session(RpcClient(env, "--no-session"))
        try:
            always_on.get_state()
            assert always_on.status and "ADHD ON" in always_on.status
        finally:
            always_on.close()

    print("Pi extension smoke test passed")


if __name__ == "__main__":
    main()
