---
name: skill-curator
version: 1.1
status: active
last_reviewed: 2026-08-24
description: Use to review, deduplicate, and maintain a skill library.
---

# Skill Curator

## Use when

Use this skill to review, deduplicate, classify, improve, retire, or maintain a skill library.

## Inputs

- Required: Skill library, authoring rules, validation tools, and review objective.
- Optional: Known overlaps, route scenarios, change history, categories, and compatibility constraints.
- Preconditions: All in-scope Skills and related documentation can be inventoried.
- Missing information: Report uncertain overlap or stale references instead of deleting or merging silently.
- Output artifact: Inventory, findings, boundary decisions, approved changes, validation evidence, and remaining gaps.

## Procedure

1. Inventory skill names, descriptions, categories, triggers, procedures, outputs, dependencies, and validation status.
2. Check each skill for narrow scope, actionable instructions, clear routing, consistent structure, and overlap with other skills.
3. Identify duplicates, gaps, stale references, overly broad skills, weak triggers, and inconsistent terminology.
4. Recommend the smallest change: clarify, split, merge, relocate, deprecate, or create only when the gap is real.
5. When maintenance is requested, apply the smallest change while preserving compatibility and repository conventions. Borrow useful methods from external libraries by adapting them to this library's routing, authority, and verification rules; do not import a competing global router or duplicate an existing owner.
6. Run structural and targeted content validation, then report unresolved overlap or future candidates.

## Decision rules

- Use the narrowest Skill whose trigger and output match the request.
- Treat directory names and YAML `name` values as compatibility identifiers.
- Classify overlap as duplicate, specialization, orchestration, or intentional handoff.
- Prefer clarification and explicit handoffs over copied procedures or silent deletion.
- Do not expand a skill library by adding another skill when an existing owner can absorb a small, clearly bounded improvement without broadening its trigger or responsibility.

## Verification

- Every skill has valid metadata and a specific trigger.
- Each skill has a distinct purpose or documented relationship to related skills.
- Procedures, verification, and outputs are actionable and internally consistent.
- Validation covers the final library state and no unsupported capability is claimed.

## Output

Return the library inventory, findings, change recommendations or updates, overlap decisions, validation evidence, and remaining gaps.
