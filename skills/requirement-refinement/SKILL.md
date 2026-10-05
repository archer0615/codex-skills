---
name: requirement-refinement
version: 1.2
status: active
last_reviewed: 2026-10-05
description: Use when a request needs explicit scope, constraints, and acceptance criteria.
---

# Requirement Refinement

## Use when

Use this skill when a request is ambiguous about scope, constraints, expected behavior, priority, acceptance criteria, or domain terms/rules, and proceeding without clarification could materially change the result. For domain modeling, use it only when business concepts, relationships, or rules affect the requested behavior or data contract; do not invoke it just to maintain a glossary.

## Inputs

- Required: Original request and available project or domain context.
- Optional: Existing behavior, examples, constraints, users, deadline, and known risks.
- Optional: Existing glossary, domain model, decision records, schemas, and domain-owner input.
- Preconditions: Ambiguity could change implementation, cost, safety, or acceptance.
- Missing information: Ask focused questions only for material unknowns; record non-material assumptions.
- Output artifact: Clarified requirements with scope, constraints, acceptance criteria, assumptions, open questions, and, when relevant, resolved domain terms/rules and their evidence or owner.

## Procedure

1. Restate the requested outcome in one sentence without adding new scope.
2. Inspect repository instructions, existing glossary/domain documents, relevant code/schema/tests, behavior, and other available evidence before asking questions.
3. Identify only ambiguities that can change implementation, risk, compatibility, data meaning, or acceptance. For relevant domain concepts, check for overloaded terms, unclear ownership, lifecycle/state boundaries, relationships, invariants, and edge cases. Ignore harmless wording preferences.
4. Separate user/domain claims, repository-documented rules, and observed implementation behavior. If they conflict, show the discrepancy and ask only when the difference materially affects the requested outcome; do not silently treat current code as the intended business rule.
5. Convert the request into explicit scope, out-of-scope items, constraints, assumptions, priority, and observable acceptance criteria. Include a concise term/rule definition only where needed to make the requirement unambiguous.
6. Ask the smallest set of focused questions when a material decision cannot be inferred safely. If the task is already actionable, preserve the request and proceed; do not add a design-approval checkpoint, options exercise, or written specification solely because implementation is creative or changes behavior.
7. Update or create a glossary/domain artifact only when the user requested it or the repository's documented convention makes it part of the requested work. Create/update an ADR only for a consequential, non-obvious choice among real alternatives, and only within the requested scope. Do not invent a documentation location or create artifacts merely because a term was discussed.
8. Resolve answers and repository evidence into a concise implementation-ready brief; hand ongoing repository-wide architecture mapping to `repo-understanding`, and existing document taxonomy/migration to `knowledge-base-organizing` when those distinct outcomes are requested.

## Decision rules

- Preserve the user’s intent; do not optimize a clear request into a different task.
- Prefer existing project conventions over invented requirements.
- Mark inferred details as assumptions and make them easy to revise.
- Treat domain terms and business rules as evidence-backed constraints; distinguish them from implementation names and current code behavior.
- Prefer the existing glossary/domain source of truth. Do not create a competing model or duplicate repository knowledge base.
- Domain modeling is conditional analysis within requirement refinement, not a mandatory interview or documentation workflow.
- Treat security, data loss, public API compatibility, and production impact as material constraints.
- Do not ask the user to manually perform a check that can be inspected or verified through the repository.

## Verification

- The outcome is specific enough to identify what changes and what must remain unchanged.
- Each acceptance criterion is observable and testable.
- Scope boundaries, assumptions, and unresolved decisions are explicit.
- The refined brief does not introduce unsupported technologies, dependencies, or behavior.

## Output

Return the implementation-ready brief with objective, in-scope items, out-of-scope items, constraints, assumptions, acceptance criteria, unresolved questions, and the recommended next skill or action.
