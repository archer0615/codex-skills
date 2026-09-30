#!/usr/bin/env python3
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
candidates = [home / "skills" / "archify", Path.home() / ".agents" / "skills" / "archify", Path.home() / ".codex" / "skills" / "archify"]
archify = next((p for p in candidates if (p / "SKILL.md").is_file() and (p / "bin" / "archify.mjs").is_file()), None)
if not archify: print("找不到 Archify Skill。", file=sys.stderr); sys.exit(1)
node = shutil.which("node") or shutil.which("node.exe")
if not node: print("找不到 Node.js。", file=sys.stderr); sys.exit(1)
with tempfile.TemporaryDirectory(prefix="archify-smoke-") as tmp:
    subprocess.run([node, str(archify / "bin" / "archify.mjs"), "doctor"], check=True)
    output = Path(tmp) / "output"; subprocess.run([node, str(archify / "bin" / "archify.mjs"), "demo", str(output)], check=True)
    if not any(output.rglob("*")): raise SystemExit("Archify demo 沒有產生輸出。")
print(f"Archify smoke test passed: {archify}")
