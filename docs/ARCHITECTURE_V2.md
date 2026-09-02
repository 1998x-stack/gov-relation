# Government Relationship Data Platform v2

## Product boundary

The repository becomes an evidence-backed data platform, while preserving existing regional builders as legacy producers. The canonical database is a reproducible derivative, not a hand-edited source file. Public availability does not imply commercial reuse permission: every source and dataset has explicit rights fields, defaulting to blocked.

## Runtime modes

1. **Research** — collect official rosters, timelines, relationships, and source registers under `data/tmp/<task_id>/`.
2. **Validate and promote** — run `scripts/process_tmp.py`; only validated artifacts enter canonical legacy directories.
3. **Ingest** — `scripts/govdb.py build` imports SQLite and person JSON losslessly into a temporary database, then atomically publishes it.
4. **Resolve and quality** — conservative deterministic matching creates canonical entities; ambiguous identities remain separate and enter `resolution_candidates`/`quality_issues`.
5. **Publish and export** — local APIs use read-only connections. Commercial exports must use rights-cleared sources and pass integrity, evidence, freshness, and privacy gates.

## Data layers

| Layer | Tables | Contract |
| --- | --- | --- |
| Bronze | `datasets`, `raw_records`, `profile_documents` | Immutable source payload and checksum; no field loss |
| Silver | `persons`, `organizations`, `positions`, `relationships`, `person_statuses` | Normalized IDs, temporal fields, conservative entity resolution |
| Evidence | `sources`, `claims`, `evidence_links`, `entity_provenance` | Every material fact can trace to source and transformation |
| Quality | `quality_issues`, `resolution_candidates`, `ingest_runs` | Quarantine, review state, reproducibility and operational audit |
| Gold | `gold_current_positions`, `gold_relationship_edges`, `gold_commercial_sources` | Stable read models for API, graph analytics, and licensed export |

## Identity and temporal rules

- Merge people globally only when normalized name and birth value both match. Name-only records remain dataset-scoped; false separation is safer than false identity.
- Scope organization matching to jurisdiction or source dataset until a verified organization registry exists.
- Preserve source date text and precision. Never invent missing month/day boundaries.
- Treat relationships as evidence-backed records, not inferred social ties. Strong edges require an overlap organization/period or explicit source.
- Keep current status as an observation with an `as_of` date; do not overwrite historical positions.

## Deployment path

SQLite is the single system of record across research and production. The unified platform database `data/platform/gov_relation.db` stores every layer, and versioned read APIs, graph, and search projections are built from the same SQLite source. Raw/evidence records remain append-only; corrections create reviewed claims or superseding versions. Tenant billing and access control belong in the application database, not the research corpus.

## Commands

```bash
python3 scripts/govdb.py build --database data/platform/gov_relation.db
python3 scripts/govdb.py audit --database data/platform/gov_relation.db
python3 scripts/govdb.py release-check --database data/platform/gov_relation.db
```

Use `--replace` only to atomically rebuild that exact derived database. Commercial read models include only facts linked to a rights-cleared source. The release check also fails while error-level quality issues remain open or no facts qualify for commercial export.
