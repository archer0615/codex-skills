#!/usr/bin/env python3
"""Preview or apply user-level local Codex bootstrap files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


TOOLS = [
    "git", "node", "npm", "npx", "pnpm", "yarn", "java", "mvn", "gradle",
    "terraform", "terraform-docs", "gcloud", "kubectl", "docker", "python", "py", "codex",
]

GLOBAL_AGENTS = """# Global Codex Environment Instructions

## General

- 使用繁體中文回覆。
- 這是本機環境；執行建置、測試、安裝或啟動服務前先檢查環境。
- 不得因單一命令失敗就判定工具未安裝。
- 不要自行 commit、push、merge、deploy 或 release。
- 安裝工具、修改系統 PATH、啟動外部服務或執行雲端操作前，先說明影響並取得確認。

## Tool discovery

依序檢查命令解析結果、where/PATH、版本、專案 wrapper 與專案文件。將狀態區分為 FOUND、PATH_ISSUE、MISSING、OPTIONAL、BLOCKED_BY_AUTH。

## Project-aware behavior

- 先判斷目前目錄、Git root、專案文件與 lockfile。
- Node 專案先讀 package.json 與 lockfile。
- Java 專案先讀 pom.xml、build.gradle、gradle.properties 與 wrapper。
- Terraform plan/apply 前必須取得確認。
- 專案自己的 AGENTS.md、README、測試與 wrapper 優先於本規則。
- 不把專案絕對路徑、憑證、Token、Secret 或固定版本寫入全域設定。

## Verification

環境修正後重新確認 executable 路徑、版本、依賴、最小建置或測試，以及新 Codex session 是否仍可解析工具。不得宣稱未實際執行的命令成功。
"""

CONFIG = """[shell_environment_policy]
ignore_default_excludes = false

[shell_environment_policy.filters]
\"PATH\" = \"include\"
\"PATHEXT\" = \"include\"
\"ComSpec\" = \"include\"
\"SystemRoot\" = \"include\"
\"USERPROFILE\" = \"include\"
\"APPDATA\" = \"include\"
\"LOCALAPPDATA\" = \"include\"
"""


def codex_home(value: Optional[str]) -> Path:
    configured = value or os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def version(command: str) -> Optional[str]:
    try:
        result = subprocess.run(
            [command, "--version"], capture_output=True, text=True, timeout=5, check=False
        )
        line = (result.stdout or result.stderr).splitlines()
        return line[0].strip() if line else None
    except (OSError, subprocess.SubprocessError):
        return None


def inventory() -> List[Dict[str, Optional[str]]]:
    rows = []
    for name in TOOLS:
        path = shutil.which(name)
        rows.append({
            "name": name,
            "status": "FOUND" if path else "NOT_FOUND_BY_SHELL",
            "path": path,
            "version": version(path) if path else None,
        })
    return rows


def backup(path: Path) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    target = path.with_name(f"{path.name}.backup-{stamp}")
    shutil.copy2(path, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.preview == args.apply:
        parser.error("請指定且只指定 --preview 或 --apply")

    home = codex_home(args.codex_home)
    targets = [home / "AGENTS.md", home / "config.toml", home / "environment-inventory.json"]
    existing = [str(path) for path in targets if path.exists()]

    print(f"Codex home: {home}")
    print("Targets:")
    for path in targets:
        print(f"- {path} {'(exists)' if path.exists() else '(new)'}")

    rows = inventory()
    print("Tools:")
    for row in rows:
        print(f"- {row['name']}: {row['status']} | {row['path'] or '-'} | {row['version'] or '-'}")

    if args.preview:
        print("Preview only; no files changed.")
        return 0

    if existing and not args.force:
        print("Existing target files found. Re-run with --force only after confirming overwrite.")
        return 2

    home.mkdir(parents=True, exist_ok=True)
    for path in targets:
        if path.exists():
            print(f"Backup: {backup(path)}")
    (home / "AGENTS.md").write_text(GLOBAL_AGENTS, encoding="utf-8")
    (home / "config.toml").write_text(CONFIG, encoding="utf-8")
    payload = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "computer": os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME"),
        "path": os.environ.get("PATH"),
        "tools": rows,
    }
    (home / "environment-inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Bootstrap applied. Restart Codex and run doctor.py in a new conversation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
