#!/usr/bin/env python3
import tempfile, subprocess, sys
from pathlib import Path

root=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix="repo-understanding-claude-") as tmp:
    tmp=Path(tmp); codex=tmp/"codex"; skill=codex/"skills"/"repo-understanding"; skill.mkdir(parents=True); (skill/"SKILL.md").write_text("---\nname: repo-understanding\ndescription: test\n---\n", encoding="utf-8")
    home=tmp/"claude"; script=root/"scripts"/"install-claude-bridge.py"
    assert subprocess.run([sys.executable, str(script), "--home", str(home), "--codex-home", str(codex), "--apply"]).returncode == 0
    assert subprocess.run([sys.executable, str(script), "--home", str(home), "--codex-home", str(codex), "--apply"]).returncode == 0
    path=home/"CLAUDE.md"; assert "repo-understanding:begin" in path.read_text(encoding="utf-8")
print("Claude Code bridge smoke tests passed.")
