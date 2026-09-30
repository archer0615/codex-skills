# Evidence-backed Workflow

## Modes and persistent contract

Use `FULL` for first analysis, missing/untrusted baseline or unsafe impact boundary; `INCREMENTAL` only with trusted revision/index/diff; `RESUME` only after validating the saved working-tree identity; `FINAL-VERIFY` only for artifact, link, diagram and evidence consistency checks. Record the selected mode and reason in `run-state.md`.

Every run updates `run-state.md`, `execution-log.md`, `scope-inventory.md`, `evidence-inventory.md`, `artifact-inventory.md`, `pending-gaps.md`, and `blocked-items.md`. Preserve prior evidence and append revisions; do not silently overwrite a claim.

## Freeze before production

1. **Scope Freeze:** inventory every repository and its frontend entry, routes/controllers/services, persistence/cache, jobs/workflows, Terraform/IaC, external APIs, dynamic settings, runtime/deployment evidence, planned documents/diagrams, and exclusions. Unconfirmed multi-repository candidates require confirmation.
2. **Evidence Freeze:** use `Claim | Source | Evidence type | Confidence | Artifact`. Confidence is one of `CONFIRMED`, `INFERRED`, `UNKNOWN`, `INCOMPLETE`, `BLOCKED`. Primary source order is source/config/test/runtime > GitNexus > names/docs. GitNexus never proves deployment.
3. **Artifact Plan:** list every document, matrix, gap report, run-state and diagram before generating HTML. Independent features, data boundaries or lifecycles get separate artifacts.
4. **Feature Boundary Review:** answer entry/trigger/route/controller/service/data source/async-retry-response-error/dynamic-setting/unknown for each feature. Split when purpose, data source or lifecycle differs.
5. **Diagram Design Lock:** define participants, message/return order, conditions, loops, errors, async/polling, boundaries, evidence and output path before Archify.

## Required analysis coverage

For each API, trace frontend call site, method, payload, auth context, controller, service, repository/cache/external call, response mapping, error/retry/polling and side effects. Track frontend WebPart/Command Set, backend layers, Redis/JPA, Batch/Job, Cloud Run/Workflow/Scheduler, Terraform, CAAS, SharePoint, token/Secret Manager/AuthType. Explicitly report dynamic routes, settings, schema/migrations, runtime response and deployment as `UNKNOWN` or `INCOMPLETE` when not evidenced. Source-confirmed path is not the same as every deployed path.

For each independent flow produce separate docs/diagrams; DEX sign-off must be split into list, load-document and submit-signature where applicable. Newcomer notes explain purpose, trigger, backend work, downstream calls, configured data, returned state, unknowns and common misconceptions.

## GitNexus and Archify routing

Build a capability profile per repository and reconcile native inventory against indexed/excluded/unsupported/generated/ignored/unexplained files. Record query target, result, primary evidence, limitation and fallback. Do not loop on failed native extensions or FTS/VECTOR; retain the first useful error and continue with source/config/test evidence.

Put formal diagram HTML outside the knowledge-base directory; put specs in `diagrams/specs/` and sidecars/PNG/contact sheets in `diagrams/verification/`. Maintain `diagram-index.html` with categories: architecture, API, DEX, iForm, Batch/Cloud Run, CAAS, Terraform and detailed flows. Archify receives only confirmed evidence plus explicitly labelled inferences/limitations.

## Verification and completion

For each artifact run schema validation, Archify validate/deliver, showcase 9/9, zero errors/warnings, visual checks across viewports and Light/Dark themes, HTML link check and inventory consistency. Apply `Identify → Fix → Re-verify`; classify failures as regression, pre-existing, tool limitation, insufficient evidence or missing external environment. Quality gate requires every scope to be documented or explicitly N/A/BLOCKED, route-to-controller-to-service traceability, current diagrams, valid links, no stale counts/names, and explicit unknown/incomplete/blocked lists.

Final report sections: (A) evidence-complete, (B) source-only, (C) reasonable inference, (D) missing evidence, (E) environment-blocked, (F) minimum user inputs needed.
