# Step 02 — Signed Source-rights Manifests

## Outcome

SQLite schema `2.1.0` adds immutable manifest metadata and source-level decision rows. The current `sources.rights_status` and `commercial_use_allowed` columns are operational summaries and are no longer intended for manual edits. Commercial views query the effective ledger decision directly, so an expired clearance cannot remain publishable because of a stale summary.

## Trust boundary

- The manifest payload is canonical JSON signed with ECDSA P-256/SHA-256.
- `key_id` is the SHA-256 fingerprint of the public key's DER encoding.
- A registered active key must bind that fingerprint to the manifest's reviewer and authority.
- Verification occurs before any database write.
- Source reliability, factual confidence, and redistribution rights remain separate.
- Unknown, expired, future, restricted, unmatched, conflicting, or unsigned decisions never enable commercial use.

The executable validator is intentionally stricter than the published JSON Schema: it checks unique decision IDs, timezone-aware intervals, key fingerprints, selector matches, and cross-field commercial rules without requiring a third-party JSON Schema package.

## Operations

Use `rights-sign`, `rights-verify`, `rights-key-register`, and `rights-apply` in `scripts/govdb.py`. Private signing keys must live outside the repository. Key registration is an administrative operation, not part of ordinary ingestion. Applying a previously accepted manifest with identical content is a no-op; reusing its ID with different content is rejected.

No existing source was cleared as part of this step. Commercial publication still requires an accountable reviewer, a documented legal basis, applicable permitted fields and uses, and the existing evidence and quality gates.
