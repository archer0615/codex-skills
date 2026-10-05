#!/usr/bin/env python3
"""Cross-platform helpers for the Repo Understanding plugin.

Only Python's standard library is used.  Each public command is exposed by a
small ``*.py`` entry point in this directory.
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Optional

SKILL_NAME = "repo-understanding"
ROOT = Path(__file__).resolve().parent.parent


def fail(message: str, code: int = 1) -> int:
    print(message, file=sys.stderr)
    return code


def codex_home(value: Optional[str] = None) -> Path:
    raw = value or os.environ.get("CODEX_HOME")
    if raw:
        return Path(os.path.expandvars(os.path.expanduser(raw))).resolve()
    return Path.home() / ".codex"


def source_skill(root: Path = ROOT) -> Path:
    return root / "skills" / SKILL_NAME


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def equivalent(left: Path, right: Path) -> bool:
    if not left.is_dir() or not right.is_dir():
        return False
    lfiles = {p.relative_to(left).as_posix(): p for p in left.rglob("*") if p.is_file()}
    rfiles = {p.relative_to(right).as_posix(): p for p in right.rglob("*") if p.is_file()}
    return lfiles.keys() == rfiles.keys() and all(sha256(lfiles[k]) == sha256(rfiles[k]) for k in lfiles)


def validate_skill(path: Path) -> int:
    path = path.resolve()
    errors: list[str] = []
    skill_file = path / "SKILL.md"
    metadata = path / "agents" / "openai.yaml"
    if not skill_file.is_file(): errors.append(f"缺少 SKILL.md：{path}")
    if not metadata.is_file(): errors.append(f"缺少 agents/openai.yaml：{path}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", path.name): errors.append(f"Skill 目錄名稱不符合規則：{path.name}")
    content = skill_file.read_text(encoding="utf-8") if skill_file.is_file() else ""
    match = re.search(r"(?ms)^---\s*\n(.*?)\n---", content)
    if not match: errors.append("SKILL.md 缺少 YAML frontmatter。")
    else:
        frontmatter = match.group(1)
        name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter)
        if not name: errors.append("frontmatter 缺少合法 name。")
        elif name.group(1) != path.name: errors.append(f"frontmatter name '{name.group(1)}' 與目錄 '{path.name}' 不一致。")
        if not re.search(r"(?m)^description:\s*.+$", frontmatter): errors.append("frontmatter 缺少 description。")
        version = re.search(r"(?m)^version:\s*['\"]?([0-9]+\.[0-9]+(?:\.[0-9]+)?)['\"]?\s*$", frontmatter)
        if not version: errors.append("frontmatter 缺少 version（major.minor[.patch]）。")
        status = re.search(r"(?m)^status:\s*['\"]?(active|experimental|deprecated|retired)['\"]?\s*$", frontmatter)
        if not status: errors.append("frontmatter 缺少合法 status。")
        reviewed = re.search(r"(?m)^last_reviewed:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?\s*$", frontmatter)
        if not reviewed:
            errors.append("frontmatter 缺少 last_reviewed（YYYY-MM-DD）。")
        else:
            try: date.fromisoformat(reviewed.group(1))
            except ValueError: errors.append("frontmatter last_reviewed 不是有效日期。")
    section_bodies: dict[str, str] = {}
    for heading in ("Use when", "Inputs", "Procedure", "Decision rules", "Verification", "Output"):
        section = re.search(r"(?ms)^##\s+" + re.escape(heading) + r"\s*\n(.*?)(?=^##\s+|\Z)", content)
        if not section:
            errors.append(f"SKILL.md 缺少必要章節：{heading}")
        else:
            section_bodies[heading] = section.group(1).strip()
            if not section_bodies[heading]: errors.append(f"SKILL.md 必要章節不可為空：{heading}")
    procedure = section_bodies.get("Procedure", "")
    if procedure and not re.search(r"(?m)^(?:\d+\.\s+|###\s+\d+\.\s+)", procedure):
        errors.append("Procedure 至少要包含一個可執行的編號步驟。")
    example = re.search(r"(?ms)^## Example\s*\n(.*?)(?=^##\s+|\Z)", content)
    if example and not example.group(1).strip(): errors.append("Example 章節不可為空；請補範例或移除章節。")
    inputs_match = re.search(r"(?ms)^## Inputs\s*\n(.*?)(?=^## |\Z)", content)
    if inputs_match:
        for field in ("Required:", "Optional:", "Preconditions:", "Missing information:", "Output artifact:"):
            if field not in inputs_match.group(1): errors.append(f"Inputs 缺少欄位：{field}")
    if status and status.group(1) in {"deprecated", "retired"} and not re.search(r"(?i)migrat|replacement|替代|遷移", content):
        errors.append("deprecated／retired Skill 必須說明替代或遷移方式。")
    if re.search(r"(?i)\b(?:TODO|FIXME|PLACEHOLDER)\b", content): errors.append("SKILL.md 含未完成 TODO/FIXME/PLACEHOLDER。")
    if metadata.is_file():
        metadata_text = metadata.read_text(encoding="utf-8")
        for field in ("display_name:", "short_description:", "default_prompt:"):
            if field not in metadata_text: errors.append(f"openai.yaml 缺少 {field}")
    for rel in sorted(set(re.findall(r"(?:references|assets)/[A-Za-z0-9_.\-/]+", content))):
        resource = path / rel.rstrip("/")
        if not resource.exists(): errors.append(f"SKILL.md 引用不存在的資源：{rel}")
    plugin_root = path.parent.parent
    manifests = [p for p in (plugin_root / "skills").glob("*/SKILL.md") if p.is_file()]
    if skill_file.resolve() not in {p.resolve() for p in manifests}: errors.append("目前 Skill 不在 Plugin 的 skills/ manifest 清單中。")
    plugin_file = plugin_root / "plugin.json"
    if not plugin_file.is_file(): errors.append(f"缺少根 Plugin manifest：{plugin_file}")
    else:
        try: plugin = json.loads(plugin_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: errors.append(f"plugin.json 無效：{exc}"); plugin = {}
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(plugin.get("name", ""))): errors.append("plugin.json name 必須是 lowercase kebab-case。")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))): errors.append("plugin.json version 必須符合 major.minor.patch 格式。")
        if not plugin.get("description"): errors.append("plugin.json 缺少 description。")
    toolchain_file = plugin_root / "toolchain.json"
    if toolchain_file.is_file():
        try:
            bundled = set(load_toolchain(plugin_root).get("bundledSkills", []))
            manifest_names = {p.parent.name for p in manifests}
            if path.name not in bundled: errors.append(f"toolchain.json 未宣告 Skill：{path.name}")
            if bundled != manifest_names: errors.append("toolchain.json bundledSkills 與 skills/*/SKILL.md 不一致。")
        except (json.JSONDecodeError, TypeError):
            errors.append("toolchain.json 無法讀取 bundledSkills。")
    if errors:
        for error in errors: print(f"[validate] ERROR {error}", file=sys.stderr)
        return 1
    print(f"Skill validation passed: {path}")
    return 0


def load_toolchain(root: Path) -> dict:
    return json.loads((root / "toolchain.json").read_text(encoding="utf-8"))


def command_path(name: str) -> Optional[str]:
    return shutil.which(name) or shutil.which(name + ".cmd")


def bootstrap(args: argparse.Namespace) -> int:
    root = Path(args.repository_path).resolve()
    try: toolchain = load_toolchain(root)
    except Exception as exc: return fail(f"[bootstrap] 找不到或無法讀取 toolchain.json：{exc}")
    home = codex_home(args.codex_home)
    if args.repair_npm_prefix or args.install_project_dependencies:
        npm = command_path("npm")
        if not npm: return fail("[bootstrap] 找不到 npm；請安裝 Node.js，或不要使用需要 npm 的選項。")
    if args.repair_npm_prefix:
        current = subprocess.check_output([npm, "config", "get", "prefix"], text=True).strip()
        safe = toolchain.get("npm", {}).get("globalPrefixOnUnicodePath", {})
        safe = safe.get("windows" if os.name == "nt" else "posix", "") if isinstance(safe, dict) else safe
        safe = os.path.expandvars(os.path.expanduser(safe or (str(Path(os.environ.get("LOCALAPPDATA", Path.home())) / "npm-global") if os.name == "nt" else str(Path.home() / ".npm-global"))))
        if any(ord(c) > 127 for c in current):
            if not args.apply: print(f"[bootstrap] npm prefix '{current}' 含非 ASCII；加上 --apply 才會改為 {safe}")
            else:
                Path(safe).mkdir(parents=True, exist_ok=True); subprocess.run([npm, "config", "set", "prefix", safe], check=True); print(f"[bootstrap] npm 全域 prefix 已改為 {safe}")
        else: print(f"[bootstrap] npm 全域 prefix 可安全使用：{current}")
    for name in toolchain.get("bundledSkills", []):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(name)): return fail(f"[bootstrap] toolchain.json 含無效 Skill 名稱：{name}")
        skill = root / "skills" / name
        if not (skill / "SKILL.md").is_file(): return fail(f"[bootstrap] Skill 不存在或缺少 SKILL.md：{skill}")
        if validate_skill(skill) != 0: return 1
        dest = home / "skills" / name
        if dest.is_dir() and equivalent(skill, dest): print(f"[bootstrap] Codex Skill 已是最新：{name}"); continue
        if dest.exists() and not args.force: return fail(f"[bootstrap] Codex Skill 已存在且內容不同：{dest}。若要更新，請加上 --force。")
        print(f"[bootstrap] {'將安裝' if not args.apply else '安裝'} Codex Skill：{name} → {dest}")
        if args.apply:
            dest.parent.mkdir(parents=True, exist_ok=True); staging = dest.parent / f".{name}.staging-{uuid.uuid4().hex}"; backup = None
            try:
                shutil.copytree(skill, staging)
                if not (staging / "SKILL.md").is_file() or not (staging / "agents" / "openai.yaml").is_file():
                    raise ValueError(f"暫存 Skill 缺少必要檔案：{staging}")
                if dest.exists(): backup = dest.with_name(dest.name + ".backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")); dest.rename(backup)
                staging.rename(dest)
                if backup: print(f"[bootstrap] 已保留舊版本備份：{backup}")
            except Exception:
                if staging.exists(): shutil.rmtree(staging, ignore_errors=True)
                if backup and backup.exists() and not dest.exists(): backup.rename(dest)
                raise
    if args.install_project_dependencies:
        package = root / "package.json"; lock = root / "package-lock.json"
        if not package.exists(): print("[bootstrap] 沒有 package.json；略過 npm 專案依賴。")
        elif not lock.exists(): return fail("[bootstrap] package.json 沒有 package-lock.json；未執行 npm ci。")
        elif args.apply: subprocess.run([npm, "ci"], cwd=root, check=True)
        else: print("[bootstrap] 預覽：將在目標根目錄執行 npm ci（需 --apply）。")
    return 0


def prepare(args: argparse.Namespace) -> int:
    repo = Path(args.repository_path).resolve(); output = Path(args.output_path or repo / "docs" / "repo-understanding").resolve()
    names = ["index.md", "run-state.md", "gitnexus-coverage.md", "architecture-coverage.md", "diagram-coverage.md", "toolchain-utilization.md", "evidence-inventory.md", "scope-inventory.md", "artifact-inventory.md", "execution-log.md", "pending-gaps.md", "blocked-items.md"]
    template = ROOT / "skills" / SKILL_NAME / "assets" / "output-templates"
    print(f"[prepare] repository: {repo}\n[prepare] output: {output}")
    for name in names:
        source, dest = template / name, output / name
        if not source.is_file(): return fail(f"缺少 template：{source}")
        if dest.exists(): print(f"[prepare] EXISTS {dest}")
        elif args.apply: output.mkdir(parents=True, exist_ok=True); shutil.copy2(source, dest); print(f"[prepare] CREATED {dest}")
        else: print(f"[prepare] PREVIEW {dest}")
    if not args.apply: print("[prepare] 預覽模式：未修改目標 repository。")
    return 0


def organize(path: Path) -> int:
    path = path.resolve(); index = path / "index.md"
    if not index.is_file(): return fail(f"缺少 dashboard index.md：{index}")
    known = ["profile.md", "architecture-coverage.md", "gitnexus-coverage.md", "diagram-coverage.md", "run-state.md", "toolchain-utilization.md", "gaps.md", "evidence-model.md"]
    docs = [f"- [{Path(n).stem}]({n})" for n in known if (path / n).is_file()] or ["- 尚未產生文件。"]
    diagrams = [f"- [{p.name}]({p.relative_to(path).as_posix()})" for p in sorted((path / "diagrams").rglob("*") if (path / "diagrams").is_dir() else []) if p.is_file()] or ["- 尚未產生圖表。"]
    content = index.read_text(encoding="utf-8")
    content = re.sub(r"(?s)<!-- ORGANIZED-DOCUMENTS:START -->.*?<!-- ORGANIZED-DOCUMENTS:END -->", "<!-- ORGANIZED-DOCUMENTS:START -->\n" + "\n".join(docs) + "\n<!-- ORGANIZED-DOCUMENTS:END -->", content)
    content = re.sub(r"(?s)<!-- ORGANIZED-DIAGRAMS:START -->.*?<!-- ORGANIZED-DIAGRAMS:END -->", "<!-- ORGANIZED-DIAGRAMS:START -->\n" + "\n".join(diagrams) + "\n<!-- ORGANIZED-DIAGRAMS:END -->", content)
    index.write_text(content, encoding="utf-8")
    print(f"Knowledge base organized: {path}"); return 0


def validate_kb(path: Path) -> int:
    required = ["index.md", "run-state.md", "gitnexus-coverage.md", "architecture-coverage.md", "diagram-coverage.md", "toolchain-utilization.md", "evidence-inventory.md", "scope-inventory.md", "artifact-inventory.md", "execution-log.md", "pending-gaps.md", "blocked-items.md"]
    if not path.is_dir(): return fail(f"Knowledge base 目錄不存在：{path}")
    missing = [n for n in required if not (path / n).is_file()]
    files = list(path.rglob("*.md"))
    if missing: return fail("Knowledge base 缺少必要文件：" + ", ".join(missing))
    if any(re.search(r"(?i)\b(TODO|FIXME|PLACEHOLDER)\b", p.read_text(encoding="utf-8", errors="replace")) for p in files): return fail("Knowledge base 含未完成 TODO/FIXME/PLACEHOLDER。")
    print(f"Knowledge base validation passed: {path} ({len(files)} markdown files)"); return 0


def bridge(args: argparse.Namespace, kind: str) -> int:
    user = Path(args.home or os.environ.get("CLAUDE_HOME" if kind == "claude" else "CURSOR_HOME", Path.home() / (".claude" if kind == "claude" else ".cursor"))).expanduser()
    codex = codex_home(args.codex_home); skill = codex / "skills" / SKILL_NAME / "SKILL.md"
    if not skill.is_file(): return fail(f"找不到已安裝的 Codex Skill：{skill}。請先安裝 Skill。")
    if kind == "claude":
        target, begin, end = user / "CLAUDE.md", "<!-- repo-understanding:begin -->", "<!-- repo-understanding:end -->"
        block = f"{begin}\n# Repository Understanding Claude Code bridge\n\nUse the installed Codex Skill at `$CODEX_HOME/skills/{SKILL_NAME}/` as the single source of truth. Do not recreate a repository-local portable workflow. If it is missing, report BLOCKED / USER AUTHORIZATION REQUIRED.\n{end}\n"
        pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S); existing = target.read_text(encoding="utf-8") if target.exists() else ""
        updated = pattern.sub(block.strip(), existing, count=1) if pattern.search(existing) else (existing.rstrip() + "\n\n" + block if existing else block)
    else:
        target = user / "rules" / f"{SKILL_NAME}.mdc"; existing = target.read_text(encoding="utf-8") if target.exists() else ""
        updated = f"---\ndescription: Use the installed Repository Understanding Skill\nalwaysApply: true\n---\n\nUse `$CODEX_HOME/skills/{SKILL_NAME}/` as the single source of truth. Do not recreate a portable workflow.\n"
    if existing == updated: print(f"[{kind}-bridge] 已是最新：{target}"); return 0
    if existing and not args.force: return fail(f"[{kind}-bridge] 已有不同設定：{target}。請使用 --force 才能備份並更新。")
    print(f"[{kind}-bridge] 預覽：將更新 {target}（需 --apply）。")
    if args.apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists(): shutil.copy2(target, target.with_name(target.name + ".backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")))
        staging = target.with_name("." + target.name + ".staging-" + uuid.uuid4().hex); staging.write_text(updated, encoding="utf-8"); staging.replace(target)
    return 0


def audit(root: Path, home: Optional[str]) -> int:
    missing = 0; ch = codex_home(home); skill = source_skill(root); dest = ch / "skills" / SKILL_NAME
    print(f"[audit] platform: {sys.platform}\n[audit] Codex home: {ch}")
    for label, p in [("plugin.json", root / "plugin.json"), ("toolchain.json", root / "toolchain.json"), ("SKILL.md", skill / "SKILL.md"), ("agents/openai.yaml", skill / "agents" / "openai.yaml")]:
        print(f"[audit] {'PASS' if p.exists() else 'MISSING'} {label} : {p}"); missing += not p.exists()
    purposes = {
        "git": "revision / diff / working-tree identity",
        "node": "Node-based runners such as Archify",
        "npm": "authorized project dependency installation",
        "gitnexus": "graph evidence and GitNexus impact gates",
    }
    for name in ("git", "node", "npm", "gitnexus"):
        found = command_path(name)
        state = "AVAILABLE" if found else "OPTIONAL MISSING (gate-dependent)"
        print(f"[audit] {state} {name} | scope: {purposes[name]} | {found or 'not found'}")
    archify_candidates = [ch / "skills" / "archify", Path.home() / ".agents" / "skills" / "archify", Path.home() / ".codex" / "skills" / "archify"]
    archify = next((p for p in archify_candidates if (p / "SKILL.md").is_file() and (p / "bin" / "archify.mjs").is_file()), None)
    node = command_path("node")
    archify_state = "AVAILABLE" if archify and node else "OPTIONAL MISSING (diagram gate only)"
    archify_detail = str(archify) if archify and node else (f"Skill found at {archify}, but Node runner is unavailable" if archify else "not found")
    print(f"[audit] {archify_state} archify | {archify_detail}")
    print(f"[audit] {'INFO installed Skill exists' if dest.exists() else 'INFO installed Skill not found'} : {dest}")
    if missing: return 1
    return 0


def run_analysis(args: argparse.Namespace) -> int:
    repo = Path(args.repository_path).resolve(); output = Path(args.output_path or repo / "docs" / "repo-understanding").resolve()
    print(f"[run] repository: {repo}\n[run] mode: {args.mode}")
    if prepare(argparse.Namespace(repository_path=repo, output_path=output, apply=args.apply)) != 0: return 1
    if not args.apply: print("[run] 預覽模式：未建立或修改知識庫。"); return 0
    if args.mode == "FINAL-VERIFY":
        return 0 if organize(output) == 0 and validate_kb(output) == 0 else 1
    if args.run_gitnexus:
        runner = command_path("gitnexus")
        if not runner: return fail("找不到 GitNexus；無法執行 analyze。")
        subprocess.run([runner, "analyze", "--skip-agents-md", "--skip-skills"], cwd=repo, check=True)
    if organize(output) != 0 or validate_kb(output) != 0: return 1
    print(f"[run] deterministic phases passed: {output}\n[run] AI phases remain: evidence collection, semantic validation, and final coverage review."); return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate-skill"); v.add_argument("path", nargs="?", default=str(ROOT / "skills" / SKILL_NAME))
    b = sub.add_parser("bootstrap"); b.add_argument("--repository-path", default=str(ROOT)); b.add_argument("--codex-home"); b.add_argument("--apply", action="store_true"); b.add_argument("--force", action="store_true"); b.add_argument("--repair-npm-prefix", action="store_true"); b.add_argument("--install-project-dependencies", action="store_true")
    pr = sub.add_parser("prepare"); pr.add_argument("--repository-path", default=os.getcwd()); pr.add_argument("--output-path"); pr.add_argument("--apply", action="store_true")
    o = sub.add_parser("organize"); o.add_argument("path")
    k = sub.add_parser("validate-kb"); k.add_argument("path")
    a = sub.add_parser("audit"); a.add_argument("--repository-path", default=str(ROOT)); a.add_argument("--codex-home")
    r = sub.add_parser("run"); r.add_argument("--repository-path", required=True); r.add_argument("--output-path"); r.add_argument("--mode", choices=["FULL", "INCREMENTAL", "RESUME", "FINAL-VERIFY"], default="FULL"); r.add_argument("--apply", action="store_true"); r.add_argument("--run-gitnexus", action="store_true")
    for kind in ("claude", "cursor"):
        x = sub.add_parser(f"install-{kind}-bridge"); x.add_argument("--home"); x.add_argument("--codex-home"); x.add_argument("--apply", action="store_true"); x.add_argument("--force", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "validate-skill": return validate_skill(Path(args.path))
        if args.command == "bootstrap": return bootstrap(args)
        if args.command == "prepare": return prepare(args)
        if args.command == "organize": return organize(Path(args.path))
        if args.command == "validate-kb": return validate_kb(Path(args.path))
        if args.command == "audit": return audit(Path(args.repository_path).resolve(), args.codex_home)
        if args.command == "run": return run_analysis(args)
        if args.command.startswith("install-"): return bridge(args, args.command.removeprefix("install-").removesuffix("-bridge"))
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as exc:
        return fail(f"[repo-tools] 失敗：{exc}")
    return 2


if __name__ == "__main__": sys.exit(main())
