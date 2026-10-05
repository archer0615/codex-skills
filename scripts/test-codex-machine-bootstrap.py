#!/usr/bin/env python3
"""Smoke-test the bundled local Codex bootstrap and doctor helpers safely."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_SCRIPTS = ROOT / "skills" / "codex-machine-bootstrap" / "scripts"
BOOTSTRAP = SKILL_SCRIPTS / "bootstrap.py"
DOCTOR = SKILL_SCRIPTS / "doctor.py"


def run(script: Path, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


with tempfile.TemporaryDirectory(prefix="codex-machine-bootstrap-") as raw:
    root = Path(raw)
    codex_home = root / "codex-home"
    project = root / "project"
    project.mkdir()
    env = os.environ.copy()
    env["PATH"] = ""
    env.pop("CODEX_HOME", None)

    preview = run(BOOTSTRAP, "--codex-home", str(codex_home), "--preview", env=env)
    assert preview.returncode == 0, preview.stdout + preview.stderr
    assert not codex_home.exists(), "Preview must not create the Codex home."

    applied = run(BOOTSTRAP, "--codex-home", str(codex_home), "--apply", env=env)
    assert applied.returncode == 0, applied.stdout + applied.stderr
    expected = ["AGENTS.md", "config.toml", "environment-inventory.json"]
    for name in expected:
        assert (codex_home / name).is_file(), f"Bootstrap did not create {name}."

    inventory = json.loads((codex_home / "environment-inventory.json").read_text(encoding="utf-8"))
    assert inventory["tools"], "Inventory must contain the declared tool checks."

    doctor = run(DOCTOR, "--project-root", str(project), "--json", env=env)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    diagnosis = json.loads(doctor.stdout)
    assert diagnosis["projectRoot"] == str(project.resolve())
    assert not list(project.iterdir()), "Doctor must not modify the target project."

    before = {name: (codex_home / name).read_bytes() for name in expected}
    blocked = run(BOOTSTRAP, "--codex-home", str(codex_home), "--apply", env=env)
    assert blocked.returncode == 2, "Existing files must block apply without --force."
    assert before == {name: (codex_home / name).read_bytes() for name in expected}

    forced = run(BOOTSTRAP, "--codex-home", str(codex_home), "--apply", "--force", env=env)
    assert forced.returncode == 0, forced.stdout + forced.stderr
    assert list(codex_home.glob("*.backup-*")), "Force must preserve timestamped backups."

print("Codex machine bootstrap smoke tests passed.")
