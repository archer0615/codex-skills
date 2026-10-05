---
name: existing-project-takeover
version: 1.3
status: active
last_reviewed: 2026-10-05
description: Use for a bounded first-pass map of an unfamiliar repository before a separate implementation workflow.
---

# Existing Project Takeover

## Use when

Use this skill for a bounded, read-only first-pass brief when a repository, codebase, or service is unfamiliar and the user needs orientation before choosing an implementation path. For a full evidence-backed repository knowledge base, use `repo-understanding`; do not duplicate that skill's persistent inventory, GitNexus, or diagram workflow. If the user already gave a specific change and the relevant path is clear, inspect only what is needed and proceed under the applicable implementation workflow instead of producing a separate takeover report.

## Inputs

- Required: Repository path or workspace and requested investigation or change.
- Optional: Known symptoms, target subsystem, preferred commands, or issue references.
- Preconditions: Repository files can be inspected without changing them.
- Missing information: Build a bounded project overview first; do not guess an implementation target.
- Output artifact: Architecture and workflow summary, risks, evidence, and safe next route.

## Procedure

1. Establish the takeover objective, requested scope, constraints, and definition of done.
2. Inspect repository status and structure, `AGENTS.md` files, README and project documentation, dependency and build configuration, entry points, tests, and relevant history. Keep the working-tree state separate from committed history; if history is unavailable or shallow, record that limit instead of treating it as evidence of stability.
3. Identify the architecture, primary execution path, data or state boundaries, external integrations, and conventions that the requested change must preserve.
4. When an implementation is explicitly in scope, run only a relevant, authorized baseline check; record existing failures separately. Do not run tests or modify files merely to complete a takeover brief.
5. Map a requested change to the smallest likely set of files and checks. Note assumptions, risks, unknowns, and files explicitly kept out of scope.
6. Return the bounded project map, evidence, baseline status, and recommended next route. Implementation belongs to the selected implementation workflow; a multi-phase correction loop belongs to `closed-loop-task-solver`.

## Decision rules

- Treat repository instructions and existing tests as authoritative evidence for local conventions.
- Use history as optional supporting context when it can answer the takeover question or clarify risk: identify recurring change hotspots and maintenance/fix activity with bounded Git history queries, then cross-check those paths against current source, tests, ownership guidance, and the requested scope. Do not run a full contributor analytics exercise for a short orientation brief unless asked.
- Treat commit counts, author names, fix-related messages, and change frequency as noisy signals, not proof of defect rate, individual ownership, bus factor, or code quality. Squashes, bots, rebases, shallow clones, and repository age can distort them; describe the sample window and limitations, and omit unsupported conclusions.
- Prefer Git commands that work in the current shell; do not assume POSIX-only utilities. History analysis is read-only and must not require installing tools or contacting external services.
- Do not rewrite architecture, upgrade dependencies, or clean unrelated code unless explicitly required.
- Do not infer production behavior from a filename alone; trace the relevant call or data path.
- Inspect secrets and environment references for usage, but never expose or copy secret values.
- If the baseline cannot run, document the exact blocker and use static inspection or narrower checks where safe.
- Keep this skill's output read-only and bounded unless the user separately requested implementation; do not duplicate `closed-loop-task-solver`'s execute-verify-correct loop.

## Verification

- The project structure, instructions, relevant execution path, and affected files are identified.
- Baseline and post-change verification results are distinguished.
- The brief identifies relevant execution paths, conventions, evidence, assumptions, and a safe next route.
- Any checks are authorized and relevant; skipped checks and blockers remain explicit.

## Output

Return a takeover brief containing project map, relevant conventions, baseline status when applicable, likely affected files, assumptions, risks, recommended next route, and remaining blockers. If implementation was separately requested, report its result and verification under the selected implementation workflow.
