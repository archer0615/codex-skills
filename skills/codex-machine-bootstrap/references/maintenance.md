# Maintenance Guide

## First computer setup

```powershell
python scripts/bootstrap.py --preview
python scripts/bootstrap.py --apply
```

Restart Codex after applying the files. If existing user-level files are different, stop and review them; use `--force` only after confirming that a timestamp backup is acceptable.

## Routine diagnosis

```powershell
python scripts/doctor.py --project-root .
python scripts/doctor.py --project-root C:\path\to\project --json
```

The doctor is read-only. It reports command resolution and project markers but does not install tools, modify PATH, authenticate cloud accounts, start tunnels, or alter project files.

## Adding project knowledge

Keep common behavior in the global `AGENTS.md`. Add project-specific rules to the project repository's own `AGENTS.md`. When a project changes its runtime requirements, update its manifest or wrapper first; do not copy a temporary machine path into the global file.

## Completion criteria

- The global files exist at the selected `CODEX_HOME`.
- Existing files were preserved or explicitly replaced with backups.
- The doctor reports actual command paths and versions.
- A new Codex conversation can summarize the loaded global guidance.
- Any missing tool, PATH issue, authentication block, or unavailable external service is reported rather than guessed or silently repaired.
