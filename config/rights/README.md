# Source-rights manifests

Rights manifests are review artifacts, not crawler output. They record what a named reviewer is authorized to permit for each source and are the only supported way to change a source from the fail-closed `unknown` state.

Create an unsigned JSON document conforming to `rights-manifest.schema.json`. Select a source by exact canonical `source_id`, or a source family by lowercase `canonical_domain`. Domain selectors do not include a scheme, path, port, or wildcard. A `cleared` decision must cite `legal_memo_ref`, explain its rationale, include at least one permitted field, and explicitly include `commercial_distribution`. Public availability by itself is not clearance.

```bash
# Keep the private key outside this repository.
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out /secure/rights-reviewer.pem
openssl pkey -in /secure/rights-reviewer.pem -pubout -out config/rights/reviewer-public.pem

python3 scripts/govdb.py rights-sign \
  --manifest review-unsigned.json --private-key /secure/rights-reviewer.pem \
  --output review-signed.json
python3 scripts/govdb.py rights-verify \
  --manifest review-signed.json --public-key config/rights/reviewer-public.pem
python3 scripts/govdb.py rights-key-register \
  --database data/platform/gov_relation.db \
  --public-key config/rights/reviewer-public.pem \
  --reviewer reviewer@example.org --authority "Source Rights Committee" \
  --valid-from 2026-08-10T00:00:00Z
python3 scripts/govdb.py rights-apply \
  --database data/platform/gov_relation.db \
  --manifest review-signed.json --public-key config/rights/reviewer-public.pem
```

Key registration is the administrative trust boundary: the key is bound to the exact reviewer identity and authority written into the manifest. Applying is atomic and idempotent. An untrusted or inactive key, invalid signature, reused manifest ID with changed content, selector matching no sources, or overlapping decisions aborts the entire import. The signed payload and each expanded source decision remain in the database audit ledger. Never commit private keys, and do not treat the example commands as legal advice.
