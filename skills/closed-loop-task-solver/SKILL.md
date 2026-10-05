---
name: closed-loop-task-solver
version: 1.3
status: active
last_reviewed: 2026-10-05
description: Use for substantial multi-phase tasks that need a bounded correction loop until acceptance criteria pass.
---

# Closed Loop Task Solver

## Use when

Use this skill when a substantial task spans multiple phases and needs an explicit correction loop until acceptance criteria are met. It owns orchestration across phases, not a duplicate implementation or validation procedure: select one domain/implementation owner, then use its output to drive the correction loop. Do not use it for routine single-step answers or small changes that a narrower skill can complete directly.

## Inputs

- Required: Objective, acceptance criteria, constraints, current state, and available evidence.
- Optional: Selected execution Skill, files, commands, baseline, risks, and correction history.
- Preconditions: The task can be decomposed into inspect, execute, verify, and correction stages.
- Missing information: Stop at the affected stage and record the blocker when acceptance cannot be evaluated.
- Output artifact: Completion report with actions, evidence, corrections, final state, and unresolved blockers.

## Procedure

1. Define the objective, scope, constraints, acceptance criteria, and safe stopping condition from the request and repository context.
2. Inspect relevant files, tests, configuration, history, and existing conventions. Record assumptions, risks, and the smallest viable change.
3. Execute only the approved in-scope change through the selected implementation owner, preserving unrelated work and existing compatibility. Do not dispatch parallel agents or create worktrees unless the user, applicable instructions, and available tools authorize that approach and it materially helps.
4. Select verification based on project instructions, user authorization, change risk, and available evidence. Use tests where permitted and useful; otherwise use the narrowest authorized static, syntax, manual, or other evidence-based check and mark uncovered behavior unverified.
5. Compare the observed result with every acceptance criterion. Separate passed checks, failed checks, warnings, and unverified items.
6. If verification fails, identify the direct cause, make the minimum corrective change, and repeat verification. Do not conceal or bypass a failed check.
7. Stop when all criteria pass, or when a genuine external blocker remains. Report the blocker and the evidence needed to continue.

## Decision rules

- Prefer repository evidence over assumptions and external information.
- Diagnose failures by reproducing the symptom, tracing the affected execution/data path, and identifying a cause supported by evidence before changing code; distinguish correlation from root cause.
- Do not impose a design-approval gate, written plan, test-first sequence, commit, or fixed subagent workflow unless the request, project rules, or a material risk requires it.
- Keep each correction focused on the verified failure that caused it.
- Do not broaden scope merely because an adjacent improvement is visible.
- Escalate to `implementation-validator` when the main work is complete and only targeted validation remains.
- Escalate to `quality-gate` when readiness, compatibility, security, or delivery completeness requires a final review.
- Own the inspect-execute-verify-correct loop after routing; do not replace `personal-ai-task-router` when capability selection is the primary problem.
- Never claim completion from an unrun command or from an incomplete acceptance check.

## Verification

- Every acceptance criterion has a matching evidence item or an explicit blocker.
- The final verification was run after the last modification.
- Failed checks are either corrected and re-run or reported as unresolved.
- The final state and changed files are consistent with the requested scope.

## Output

Return the outcome, changed files, verification commands or evidence, remaining limitations, and the next action if blocked.
