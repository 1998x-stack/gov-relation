# Canonical Database Migration Report

Date: 2026-08-10  
Schema: `2.0.0`  
Database: `data/platform/gov_relation.db`

## Outcome

The canonical database was rebuilt atomically from every readable legacy input: 2,292 regional SQLite files and 6,630 person JSON files. One malformed JSON file was repaired before the final build. The published database passes SQLite foreign-key validation with zero violations.

| Metric | Count |
| --- | ---: |
| Datasets / raw records | 8,922 / 129,382 |
| Jurisdictions / organizations | 4,484 / 33,907 |
| Persons / status observations | 47,727 / 37,764 |
| Positions / relationships | 58,488 / 37,989 |
| Sources / evidence links | 23,228 / 60,625 |
| Claims / profile documents | 26,337 / 6,585 |
| Resolution candidates | 23,257 |

## Quality gate

The database is operational but **not approved for commercial release**. This distinction is deliberate: all 23,228 source rights are currently `unknown`, and no source is marked commercially cleared. Identity resolution is conservative; 38,592 people (80.86%) remain unresolved rather than being merged on name or approximate birth text.

Open quarantine issues total 1,836:

| Issue | Count |
| --- | ---: |
| Invalid relationship endpoints | 614 |
| Position references missing person | 585 |
| Invalid profile relationship targets | 378 |
| Position references missing organization | 160 |
| Profile/person missing name | 45 / 41 |
| Database missing persons table | 13 |

## Release path

1. Review source terms and set rights only with documented authorization.
2. Resolve error-level foreign-key/source-data defects at their legacy producers, then rebuild.
3. Review `resolution_candidates`; never bulk-merge name-only matches.
4. Add freshness SLAs and current-role evidence dates.
5. Export only reviewed claims whose evidence sources are rights-cleared.

Reproduce and audit with:

```bash
python3 scripts/govdb.py build --database data/platform/gov_relation.db --replace
python3 scripts/govdb.py audit --database data/platform/gov_relation.db
python3 scripts/govdb.py release-check --database data/platform/gov_relation.db
```
