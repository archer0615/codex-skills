#!/usr/bin/env python3
"""Read-only local Codex and project environment diagnostic."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


TOOLS = [
    "git", "node", "npm", "npx", "pnpm", "yarn", "java", "mvn", "gradle",
    "terraform", "terraform-docs", "gcloud", "kubectl", "docker", "python", "py", "codex",
]
MARKERS = {
    "AGENTS.md", "README.md", "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "pom.xml", "build.gradle", "settings.gradle", "gradlew", "gradlew.bat", "terraform.tf",
    "main.tf", "Dockerfile", "docker-compose.yml",
}
SKIP = {".git", "node_modules", "target", "build", "dist", ".gradle", ".venv"}


def get_version(path: str) -> Optional[str]:
    try:
        result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5, check=False)
        lines = (result.stdout or result.stderr).splitlines()
        return lines[0].strip() if lines else None
    except (OSError, subprocess.SubprocessError):
        return None


def find_markers(root: Path) -> list[str]:
    found: list[str] = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP]
        for name in files:
            if name in MARKERS:
                found.append(str(Path(current) / name))
    return sorted(found)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=os.getcwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    rows = []
    for name in TOOLS:
        path = shutil.which(name)
        rows.append({
            "name": name,
            "status": "FOUND" if path else "NOT_FOUND_BY_SHELL",
            "path": path,
            "version": get_version(path) if path else None,
        })
    payload = {
        "projectRoot": str(root),
        "codexHome": os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"),
        "agents": [str(root / name) for name in ("AGENTS.override.md", "AGENTS.md") if (root / name).exists()],
        "tools": rows,
        "pathEntries": [item for item in os.environ.get("PATH", "").split(os.pathsep) if item],
        "projectMarkers": find_markers(root),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Project root: {payload['projectRoot']}")
        print(f"Codex home: {payload['codexHome']}")
        print("Instruction files:")
        for item in payload["agents"]:
            print(f"- {item}")
        print("Tools:")
        for row in rows:
            print(f"- {row['name']}: {row['status']} | {row['path'] or '-'} | {row['version'] or '-'}")
        print("Project markers:")
        for item in payload["projectMarkers"][:80]:
            print(f"- {item}")
        print("No files were changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
