#!/usr/bin/env python3
"""Small fixture smoke test for mode routing and the persistent KB contract."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts" / "run-repo-understanding.py"
VALIDATOR = ROOT / "scripts" / "validate-knowledge-base.py"
MODES = ("FULL", "INCREMENTAL", "RESUME", "FINAL-VERIFY")

with tempfile.TemporaryDirectory(prefix="repo-understanding-fixture-") as raw:
    fixture = Path(raw)
    (fixture / "src").mkdir()
    (fixture / "src" / "app.py").write_text("def health(): return 'ok'\n", encoding="utf-8")
    for mode in MODES:
        apply = mode == "FULL"
        cmd = [sys.executable, str(RUNNER), "--repository-path", str(fixture), "--mode", mode]
        if apply:
            cmd.append("--apply")
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            raise SystemExit(f"mode {mode} failed: {result.stdout}\n{result.stderr}")
    result = subprocess.run([sys.executable, str(VALIDATOR), str(fixture / "docs" / "repo-understanding")], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
print("repo-understanding fixture smoke test passed")
