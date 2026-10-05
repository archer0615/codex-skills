#!/usr/bin/env python3
"""Smoke-test bootstrap in an isolated temporary directory."""
import argparse, json, shutil, tempfile
from pathlib import Path
from repo_tools import bootstrap, validate_skill

root = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix="repo-understanding-bootstrap-") as tmp:
    tmp = Path(tmp); target = tmp / "target"; home = tmp / "codex"
    shutil.copytree(root / "skills", target / "skills"); shutil.copy2(root / "plugin.json", target / "plugin.json"); shutil.copy2(root / "toolchain.json", target / "toolchain.json")
    plugin_path = target / "plugin.json"
    plugin = json.loads(plugin_path.read_text(encoding="utf-8")); plugin["version"] = "1.2.3"
    plugin_path.write_text(json.dumps(plugin), encoding="utf-8")
    assert validate_skill(target / "skills" / "repo-understanding") == 0
    base = dict(repository_path=str(target), codex_home=str(home), apply=False, force=False, repair_npm_prefix=False, install_project_dependencies=False)
    assert bootstrap(argparse.Namespace(**base)) == 0 and not home.exists()
    base["apply"] = True; assert bootstrap(argparse.Namespace(**base)) == 0
    installed = home / "skills" / "repo-understanding"; assert (installed / "SKILL.md").is_file()
    assert bootstrap(argparse.Namespace(**base)) == 0
    (installed / "user-marker.txt").write_text("preserve", encoding="utf-8")
    assert bootstrap(argparse.Namespace(**base)) != 0 and (installed / "user-marker.txt").exists()
    base["force"] = True; assert bootstrap(argparse.Namespace(**base)) == 0
    assert list((home / "skills").glob("repo-understanding.backup-*"))
    assert not list((home / "skills").glob(".repo-understanding.staging-*"))
print("Bootstrap smoke tests passed.")
