# Step 01 — PostgreSQL Production Foundation

Status: completed and locally verified on PostgreSQL 17

## Delivered

- `migrations/postgres/0001_registry_and_assertions.sql`: forward-only production schema.
- `migrations/postgres/verify/0001_registry_and_assertions.sql`: structural and transactional invariant tests.
- `infra/postgres/compose.yml`: isolated local PostgreSQL 17 service on `127.0.0.1:55439`.
- `scripts/postgres_dev.sh`: lifecycle, checksum-protected migration and verification entrypoint.
- `.github/workflows/postgres-schema.yml`: migration verification on changes and pull requests.

The migration creates seven bounded schemas (`meta`, `ingest`, `registry`, `evidence`, `assertion`, `review`, `publishing`), 26 core tables and six domain triggers.

## Verified invariants

- Migration is transactional and records its SHA-256 checksum.
- Reapplying the migration is idempotent and skips an identical checksum.
- Current position assertions require an observation timestamp.
- Position, relationship and attribute detail rows must match the base assertion type.
- Assertion type/observation updates cannot invalidate existing detail rows.
- Strong relationships require explicit evidence semantics or verified overlap.
- Release items require reviewed assertions, supporting evidence, an effective rights decision permitting `commercial_distribution`, and evidence from the rights decision's source.
- The verification fixture is rolled back and leaves no test data.

## Reproduction

```bash
bash scripts/postgres_dev.sh up
bash scripts/postgres_dev.sh migrate
bash scripts/postgres_dev.sh verify
bash scripts/postgres_dev.sh down
```

`down` preserves the named development volume. No reset/delete-volume command is provided.

## Acceptance evidence

- Initial migration: committed successfully on PostgreSQL 17.
- Verification result: `postgres schema 0001 verification passed`.
- Second migration execution: `skip 0001 (already applied)`.

## Next step

Define the signed source-rights decision manifest and importer. This is required before any current source can enter a commercial release.
