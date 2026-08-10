# API v1 Contract

Status: Draft for OpenAPI implementation

## 1. Contract rules

- Base path: `/v1`; JSON UTF-8; timestamps use RFC 3339 UTC.
- Authentication: OAuth2 client credentials for customers; separate human SSO for curator tools.
- Every request is evaluated against tenant, release and field entitlements.
- Every collection uses opaque cursor pagination with stable ordering.
- `release_id` is required or resolved once from `latest`; the resolved ID is returned.
- Confidence defaults to `confirmed`; clients must opt in to `plausible`.
- Errors use a stable code, request ID, message and optional field violations.

## 2. Read endpoints

| Method and path | Purpose |
| --- | --- |
| `GET /v1/persons` | Search by name, jurisdiction, role, organization and active date |
| `GET /v1/persons/{person_id}` | Canonical identity, aliases and coverage metadata |
| `GET /v1/persons/{person_id}/career` | Evidence-backed temporal career assertions |
| `GET /v1/persons/{person_id}/network` | Bounded relationship traversal (`depth <= 2`) |
| `GET /v1/organizations` | Search canonical organizations |
| `GET /v1/organizations/{organization_id}/officeholders` | Officeholders at an `as_of` date |
| `GET /v1/jurisdictions/{jurisdiction_id}/leadership` | Leadership snapshot at a date |
| `GET /v1/relationships` | Filtered relationship-edge query |
| `GET /v1/sources/{source_id}` | Redistributable source metadata, not restricted content |
| `GET /v1/changes` | Cursor-based changes between releases |
| `GET /v1/releases/{release_id}` | Release manifest and quality metrics |

## 3. Asynchronous endpoints

| Method and path | Purpose |
| --- | --- |
| `POST /v1/exports` | Request an entitled release extract |
| `GET /v1/exports/{export_id}` | Poll status and obtain an expiring download link |

Curator mutations are intentionally excluded from the customer API. They use an internal service with append-only review decisions and stronger authentication.

## 4. Common response envelope

```json
{
  "data": {},
  "meta": {
    "request_id": "req_...",
    "release_id": "rel_2026_08_10_001",
    "generated_at": "2026-08-10T00:00:00Z",
    "as_of": "2026-08-10",
    "next_cursor": null,
    "warnings": []
  }
}
```

An assertion includes `assertion_id`, `valid_time`, `confidence`, `review_status`, `evidence_count` and permitted source metadata. Raw source payloads, internal rights notes and resolver features are never returned from customer endpoints.

## 5. Network query limits

- Maximum depth is 2; default depth is 1.
- Maximum returned nodes/edges is tenant-plan specific.
- `relationship_type`, confidence and valid-time filters are applied before traversal.
- Weak edges and unresolved endpoints are excluded unless the entitlement explicitly permits research-preview data.
- Long-running analysis uses an asynchronous export/analytics job, not the request thread.

## 6. Versioning and errors

Breaking field or semantic changes require a new major path. Additive fields are allowed within v1. Important error codes include:

- `release_not_found`
- `field_not_entitled`
- `rights_restricted`
- `cursor_invalid`
- `query_too_broad`
- `rate_limit_exceeded`
- `export_gate_failed`

The executable specification should target OpenAPI 3.1 and include examples derived from synthetic data only.

