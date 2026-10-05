---
name: web-interface-review
version: 1.1
status: active
last_reviewed: 2026-10-05
description: Use when reviewing a web interface for accessibility, interaction behavior, responsive layout, forms, content states, or user-facing usability issues.
---

# Web Interface Review

## Use when

Use when the user asks to review a web UI, accessibility, interaction behavior, forms, responsive states, or practical usability. It can review any web stack when the relevant files or rendered interface are available.

Do not use for general implementation readiness or code performance alone. Use `react-performance-review` for React/Next.js performance analysis, `implementation-validator` for authorized technical checks, `security-review` for security analysis, and `quality-gate` for a final delivery decision.

## Inputs

- Required: Target pages, components, files, or rendered flow, plus applicable project instructions and design/product requirements.
- Optional: Supported viewport/browser matrix, accessibility target, design system, user scenarios, browser/assistive technology access, and existing issue reports.
- Preconditions: Review scope is readable. Browser automation and accessibility scanners are optional; use them only if available and authorized.
- Missing information: Review the bounded target using available evidence; mark unavailable viewport, runtime, or assistive-technology coverage as `UNVERIFIED`.
- Output artifact: Prioritized UI findings with location, user impact, evidence, confidence, and a practical correction direction.

## Procedure

1. Read project instructions, design system and relevant routes/components. Identify the user task and supported devices/locales from project evidence; do not invent product requirements.
2. Inspect semantics and assistive access: prefer native elements for their intended behavior; check accessible names, labels, heading structure, image alternatives, status announcements, keyboard operability, visible focus, focus movement, and zoom support where relevant.
3. Inspect interaction and form behavior: verify controls communicate their action, links perform navigation, keyboard and pointer paths are both available, loading/success/error states are understandable, validation feedback is associated with the relevant fields, and destructive or data-losing actions have an appropriate recovery or confirmation mechanism.
4. Inspect responsive and content resilience: check relevant narrow and wide viewports, overflow, long or localized content, empty/error/loading states, safe-area constraints where applicable, and whether essential information remains available without relying on color or hover alone.
5. When the request is a before/after or visual regression review and a baseline is available, compare the same route, viewport, interaction state, browser conditions, and relevant content. Record differences and likely causes; do not call a difference a regression until checked against intended changes and project requirements. A screenshot by itself does not prove usability or correctness.
6. Inspect motion and visual feedback: check reduced-motion preferences, focus/hover/active states, layout shifts, and whether animation obscures interaction or information. Follow the project's established visual language unless it conflicts with usability or accessibility evidence.
7. Separate confirmed defects from recommendations. Record location and the observed or reproducible user impact; do not report a rule violation solely because a particular implementation pattern is absent.
8. If changes are requested, make the smallest scoped correction, preserve the design system and behavior, and use only authorized checks. Report browser/device or assistive technology coverage that was not performed as `UNVERIFIED`.

## Decision rules

- Project requirements, supported user journeys, and applicable accessibility standards take precedence over generic style preferences.
- Treat interface guidance as review prompts, not a universal checklist. A pattern is a finding only when evidence shows a usability, accessibility, correctness, or compatibility problem in this context.
- Do not impose vendor branding, copywriting preferences, arbitrary numeric thresholds, or framework-specific patterns on unrelated projects.
- Keep performance findings owned by `react-performance-review` when React/Next.js performance is the main question; mention only directly observed UI consequences here.
- Static source inspection cannot prove rendered behavior or assistive technology usability. State the evidence type and limits.
- For visual regression claims, compare equivalent baseline/candidate conditions and distinguish intended changes, environment/rendering noise, and confirmed regressions. If no baseline or repeatable capture is available, report a current-state review only.
- Review does not authorize redesign, file edits, browser access to authenticated profiles, external scans, deployment, or other out-of-scope actions.
- This locally maintained review is informed by [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines). It is a selective adaptation, not an official Vercel product or a claim of complete upstream-rule coverage. See `THIRD-PARTY-NOTICES.md` for attribution and license.

## Verification

- Each finding is tied to a scoped file/element, rendered state, interaction, or reproducible scenario.
- Findings distinguish confirmed defects, likely issues, suggestions, and unverified coverage.
- Keyboard, responsive, loading/error, and assistive-technology checks are claimed only when actually inspected.
- Any implemented correction receives an authorized, relevant verification; unavailable checks remain explicit.

## Output

Return:

- Scope and evidence mode: source, rendered inspection, or both.
- Findings ordered by user impact, with severity, location, evidence, confidence, and recommended correction.
- For a regression review, baseline/candidate conditions and confirmed visual differences.
- Checks actually performed and results.
- Unverified viewports, browsers, interactions, or assistive-technology coverage.
- A concise scope limitation statement.
