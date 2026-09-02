# Implementation Roadmap

## Gate 0 — Design approval

- Confirm launch customer, jurisdictions, permitted confidence levels and field classes.
- Obtain written privacy/source-rights policy from counsel.
- Approve `SYSTEM_DESIGN.md`, `DOMAIN_MODEL.md` and `API_CONTRACT.md`.

Exit: no unresolved product or legal decision changes the core data model.

## Gate 1 — Production data foundation

- Keep SQLite as the versioned schema and single system of record (`data/platform/gov_relation.db`).
- Implement immutable source assets, assertions, evidence, review decisions and releases.
- Migrate the SQLite v2 corpus with lineage reconciliation.
- Add backup/restore and migration rollback drills.

Exit: row-count reconciliation, zero foreign-key failures, deterministic replay and successful restore test.

## Gate 2 — Quality and rights remediation

- Repair 1,298 current error-level producer defects.
- Review source families and load signed rights decisions.
- Build curator queues for 23,257 identity candidates and assertion conflicts.
- Measure freshness and evidence coverage per jurisdiction.

Exit: pilot scope has no error-level issues, approved rights, reviewed core identities and documented freshness.

## Gate 3 — Release and API

- Build immutable release manifests and Gold projections.
- Implement the OpenAPI contract, OAuth2, entitlements, rate limits and audit logs.
- Add contract, load, authorization-isolation and projection-rebuild tests.

Exit: staging SLOs pass; every response is reproducible from a release; cross-tenant tests fail closed.

## Gate 4 — Commercial pilot

- Launch a deliberately narrow jurisdiction/customer slice.
- Exercise correction, suppression, takedown and source-expiry workflows.
- Reconcile metering, exports and customer-visible evidence.

Exit: legal/product sign-off, operational runbook, support ownership and successful release rollback.

## Immediate backlog

1. **Completed:** SQLite platform schema `2.1.0` with signed source-rights manifests.
2. **Next:** define the source-rights decision manifest and reviewer workflow.
3. Hardened the SQLite migration and backup/restore workflow.
4. Convert `API_CONTRACT.md` into executable OpenAPI YAML.
5. Create an automated producer-defect report grouped by build script.
6. Select a pilot province/city and freeze its acceptance dataset.
