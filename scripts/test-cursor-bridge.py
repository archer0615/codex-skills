#!/usr/bin/env python3
import tempfile, subprocess, sys
from pathlib import Path

root=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix="repo-understanding-cursor-") as tmp:
    tmp=Path(tmp); codex=tmp/"codex"; skill=codex/"skills"/"repo-understanding"; skill.mkdir(parents=True); (skill/"SKILL.md").write_text("---\nname: repo-understanding\ndescription: test\n---\n", encoding="utf-8")
    home=tmp/"cursor"; script=root/"scripts/install-cursor-bridge.py"
    assert subprocess.run([sys.executable, str(script), "--home", str(home), "--codex-home", str(codex), "--apply"]).returncode == 0
    assert (home/"rules"/"repo-understanding.mdc").is_file()
print("Cursor bridge smoke tests passed.")
