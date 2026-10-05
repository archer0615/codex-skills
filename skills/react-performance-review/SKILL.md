---
name: react-performance-review
version: 1.0
status: active
last_reviewed: 2026-10-05
description: Use when implementing, reviewing, or optimizing React or Next.js code where rendering, data fetching, bundle size, or runtime performance is in scope.
---

# React Performance Review

## Use when

Use for a focused performance review or implementation task involving React or Next.js components, route rendering, data fetching, hydration, client bundles, or measured UI slowness.

Do not invoke for unrelated stacks or routine changes with no performance concern. This Skill reviews performance only; `implementation-validator` owns authorized technical checks, `quality-gate` owns delivery readiness, and `security-review` owns security analysis.

## Inputs

- Required: Target component, route, diff, or user-described performance issue; repository instructions and detected React/framework version.
- Optional: Profiling traces, Web Vitals, bundle reports, request waterfall, production-like workload, acceptance target, and supported browsers/devices.
- Preconditions: Target files and project conventions are readable. Profilers, browsers, builds, and tests are optional and must be available and authorized before use.
- Missing information: Inspect the bounded target and report missing measurements or environment as `UNVERIFIED`; ask only if the target or performance objective cannot be inferred.
- Output artifact: Ranked performance findings or a focused implementation with evidence, expected trade-offs, checks performed, and unverified areas.

## Procedure

1. Read project instructions, package manifests/lockfiles, relevant framework configuration, and the target code. Confirm React, Next.js, router/rendering mode, compiler, and data-fetching conventions before applying version-specific advice.
2. Identify the user-visible symptom or requested outcome. Prefer existing traces, metrics, profiling, bundle reports, and request waterfalls. Separate measured bottlenecks from source-level hypotheses; do not claim a speedup without evidence.
3. Trace the relevant render and data path. Check for:
   - Avoidable serial waits when independent requests or computations can safely overlap; preserve real dependency ordering and error semantics.
   - Excessive client JavaScript, broad imports, duplicated packages, eager loading of rarely used heavy features, or unnecessary third-party code.
   - Repeated server work, unsafe shared mutable request state, avoidable serialization, or duplicated data fetching in the actual rendering model.
   - Unnecessary subscriptions, derived state stored redundantly, expensive work repeated during render, or effects used where a direct event or render calculation fits better.
   - Large-list rendering, layout/paint work, hydration mismatch workarounds, or resource loading that delays useful content.
4. Rank only issues supported by evidence or clearly label hypotheses. Estimate impact and confidence; explain the relevant user path and trade-offs. Treat micro-optimizations as low priority unless measurement shows they matter.
5. If implementation is requested, make the smallest change that addresses the demonstrated or high-confidence bottleneck. Preserve behavior, accessibility, error handling, cache correctness, and project architecture. Do not add memoization, caching, parallelism, or dynamic loading mechanically; verify invalidation, dependencies, and user-visible loading behavior.
6. Select the smallest relevant verification based on project instructions, user authorization, risk, and available evidence. Re-measure with the same workload when possible; otherwise state that improvement is unverified. Do not install packages, run networked audits, access production, or broaden the test suite without authorization.
7. Hand technical test evidence to `implementation-validator` when a distinct validation report is requested; hand readiness decisions to `quality-gate` only when delivery judgment is requested.

## Decision rules

- Project documentation and the installed framework/version determine whether a pattern is supported; generic guidance never overrides them.
- Prefer measured user-facing improvements over stylistic optimization or raw micro-benchmark gains.
- Parallelize only independent work. Preserve ordering, cancellation, rate limits, consistency, and error semantics.
- Caching must state its scope, freshness, invalidation, and tenant/request isolation. Never introduce cross-user data leakage to improve speed.
- Memoization has memory and complexity costs; use it only when it avoids demonstrated or substantial repeated work and its dependencies are correct.
- Keep SSR/server components and client components within the framework's supported boundaries; do not move work client-side or server-side without tracing data, bundle, and security effects.
- Read-only review does not authorize edits. Performance work does not authorize deployment, production profiling, package installation, dependency upgrades, or commits.
- This skill is a local, focused adaptation informed by [Vercel's React/Next.js performance guidance](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices), whose upstream skill declares MIT metadata. It is not an official Vercel product and does not mirror or guarantee coverage of the upstream rule set.

## Verification

- The target framework and relevant execution path are identified from project evidence.
- Each finding is marked as measured, source-confirmed, hypothesis, or unverified.
- Any claimed improvement is compared against a relevant baseline under the same or explicitly comparable conditions.
- Behavior, correctness, cache isolation, and accessibility risks are considered where affected.
- Commands, tools, results, skipped checks, and environment limitations are accurately reported.

## Output

Return:

- Target and framework/version evidence.
- Ranked findings with location, evidence type, likely impact, confidence, and recommended next step.
- Changes made, if requested, and their trade-offs.
- Actual checks/measurements and results.
- Unverified areas and limits of the review.
