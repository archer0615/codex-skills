---
name: security-review
version: 1.0
status: active
last_reviewed: 2026-10-05
description: Use for a focused security review of code, configuration, dependencies, data flows, or an AI feature when security risk is in scope.
---

# Security Review

## Use when

Use this skill when the user requests a security audit or review, or when the requested change materially touches authentication, authorization, untrusted input, sensitive data, external integrations, file handling, dependency supply chain, or LLM/tool security.

Do not use for routine changes with no material security surface. For general delivery readiness, use `quality-gate`; for security-specific technical checks after implementation, use this Skill as the security owner and hand its evidence to `implementation-validator` or `quality-gate` only when those distinct outcomes are requested.

## Inputs

- Required: Target code/configuration or system scope, applicable repository instructions, and the requested review depth.
- Optional: Threat model, architecture/data-flow notes, known security requirements, dependency manifests/lockfiles, and prior findings.
- Preconditions: Readable source and relevant repository guidance; tests, scanners, browser access, and external services are optional capabilities, not assumed.
- Missing information: Review the bounded available scope and mark gaps as `UNKNOWN` or `UNVERIFIED`; ask only when the missing scope materially changes the review.
- Output artifact: Evidence-backed findings ranked by severity, affected paths, exploit scenario/impact, confidence, remediation direction, checks performed, and coverage gaps.

## Procedure

1. Read `AGENTS.md`, relevant security/configuration documentation, and the smallest source/config/test scope that can answer the request. Identify application boundaries and declared dependencies without installing tools or packages.
2. Map trust boundaries and assets proportionally to risk. Trace untrusted values from entry points to sensitive sinks; consider authentication, authorization and ownership, injection/output encoding, file/path operations, external URL fetching, secrets, personal data, availability, and AI/LLM inputs or tool calls when present. Use STRIDE or abuse cases as a thinking aid where useful, not as a mandatory ceremony.
3. Inspect concrete flows for defects and missing controls. Treat user input, external responses, model output, logs, configuration from untrusted sources, and paths/arguments supplied by other processes according to their provenance. Check authorization at the resource/action boundary, not merely authentication.
4. Review dependency and supply-chain evidence only when relevant and available: identify the package manager from project declarations and lockfiles; inspect dependency changes and existing audit evidence. Do not run networked audits, install dependencies, update lockfiles, or execute package scripts unless the user authorized that action and project policy allows it.
5. Run only relevant checks authorized by the user and project instructions. Prefer read-only inspection first. Record the exact commands/tools and results; skipped or unavailable checks remain `UNVERIFIED`. Do not attempt exploitation against live systems or access data beyond the authorized scope.
6. Report each finding with severity (`critical`, `high`, `medium`, `low`, or `informational`), confidence, file/line or evidence location, affected asset/boundary, plausible impact or abuse path, and a specific remediation direction. Separate confirmed vulnerabilities from hardening suggestions and unknowns.
7. If remediation is explicitly requested, make only the in-scope fix through the selected implementation owner, then perform authorized targeted verification. Security review alone does not authorize edits, dependency changes, credential rotation, external requests, commits, releases, or deployment.

## Decision rules

- Follow the user request and repository instructions; this Skill does not override authorization or project-specific security policy.
- Prioritize reachable, evidence-supported vulnerabilities. Do not present generic best practices as confirmed findings.
- Report a finding as confirmed only when source/config/runtime evidence supports it. If exploitability or reachability is unclear, label it as a hypothesis or unverified concern.
- Do not prescribe framework-specific controls as universal requirements; confirm the actual framework, deployment model, threat boundary, and existing protections.
- Do not claim regulatory compliance or a clean bill of health from a bounded review.
- `ai-governance` owns organizational AI risk/ownership controls; this Skill owns technical security analysis of code and systems. `quality-gate` owns final delivery readiness and consumes security evidence rather than repeating the audit.
- Stop and report `BLOCKED / USER AUTHORIZATION REQUIRED` if the requested check requires credentials, production access, external service interaction, installation, or a potentially harmful test not already authorized.

## Verification

- The reviewed scope and excluded/unavailable areas are explicit.
- Every confirmed finding points to reproducible source, configuration, test, or runtime evidence.
- Severity and confidence are distinguished; recommendations address the identified cause.
- Commands and tools are reported with actual outcomes; skipped checks are not described as passing.
- No out-of-scope remediation or external action was performed.

## Output

Return a concise security review with:

- Scope and review depth.
- Findings grouped by severity, each with location, evidence, confidence, impact/abuse path, and remediation direction.
- Positive controls observed only when evidenced.
- Checks performed and their exact results.
- `UNVERIFIED`, `UNKNOWN`, and blocked coverage gaps.
- A clear statement that the report is limited to the inspected scope.
