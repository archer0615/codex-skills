#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
from repo_tools import audit, bootstrap, ROOT
p=argparse.ArgumentParser(); p.add_argument('--repository-path', default=str(ROOT)); p.add_argument('--codex-home'); p.add_argument('--apply', action='store_true'); p.add_argument('--force', action='store_true'); p.add_argument('--repair-npm-prefix', action='store_true'); p.add_argument('--install-project-dependencies', action='store_true'); p.add_argument('--audit-only', action='store_true'); a=p.parse_args()
code=audit(Path(a.repository_path).resolve(), a.codex_home)
if a.audit_only or code == 1: sys.exit(code)
sys.exit(bootstrap(argparse.Namespace(repository_path=a.repository_path, codex_home=a.codex_home, apply=a.apply, force=a.force, repair_npm_prefix=a.repair_npm_prefix, install_project_dependencies=a.install_project_dependencies)))
