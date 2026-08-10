"""Signed, fail-closed source-rights decisions for the canonical database."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import sqlite3
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


SCHEMA_VERSION = "1.0"
SIGNATURE_ALGORITHM = "ecdsa-p256-sha256"
RIGHTS = {"unknown", "cleared", "restricted"}
USES = {
    "internal_research", "customer_display", "api_delivery", "bulk_export",
    "commercial_distribution",
}
FIELDS = {"identity", "career", "relationship", "governance", "source_metadata"}


class RightsManifestError(ValueError):
    """Raised when a rights manifest cannot be trusted or applied."""


def load_manifest(path: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RightsManifestError(f"Cannot read rights manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise RightsManifestError("Manifest root must be a JSON object")
    return value


def _timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise RightsManifestError(f"{field} must be a non-empty RFC3339 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RightsManifestError(f"{field} must be an RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise RightsManifestError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _utc_text(value: str) -> str:
    return _timestamp(value, "timestamp").isoformat(timespec="seconds")


def _exact_keys(value: dict[str, Any], required: set[str], optional: set[str], field: str) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {sorted(missing)}")
        if extra:
            details.append(f"unknown {sorted(extra)}")
        raise RightsManifestError(f"{field}: " + "; ".join(details))


def validate_manifest(manifest: dict[str, Any], *, require_signature: bool = True) -> None:
    """Validate the closed manifest contract and commercial-release invariants."""
    required = {
        "schema_version", "manifest_id", "created_at", "reviewed_by",
        "review_authority", "legal_memo_ref", "effective_from", "effective_to",
        "decisions",
    }
    optional = {"signature"}
    _exact_keys(manifest, required, optional, "manifest")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise RightsManifestError(f"Unsupported manifest schema: {manifest['schema_version']!r}")
    for field in ("manifest_id", "reviewed_by", "review_authority"):
        if not isinstance(manifest[field], str) or not manifest[field].strip():
            raise RightsManifestError(f"{field} must be a non-empty string")
    if not isinstance(manifest["legal_memo_ref"], str):
        raise RightsManifestError("legal_memo_ref must be a string")
    _timestamp(manifest["created_at"], "created_at")
    effective_from = _timestamp(manifest["effective_from"], "effective_from")
    effective_to = None
    if manifest["effective_to"] is not None:
        effective_to = _timestamp(manifest["effective_to"], "effective_to")
        if effective_to < effective_from:
            raise RightsManifestError("effective_to must not precede effective_from")

    decisions = manifest["decisions"]
    if not isinstance(decisions, list) or not decisions:
        raise RightsManifestError("decisions must be a non-empty array")
    seen_ids: set[str] = set()
    for index, decision in enumerate(decisions):
        field = f"decisions[{index}]"
        if not isinstance(decision, dict):
            raise RightsManifestError(f"{field} must be an object")
        _exact_keys(
            decision,
            {"decision_id", "source_selector", "decision", "permitted_uses",
             "permitted_fields", "restrictions", "rationale"},
            set(), field,
        )
        decision_id = decision["decision_id"]
        if not isinstance(decision_id, str) or not decision_id.strip():
            raise RightsManifestError(f"{field}.decision_id must be a non-empty string")
        if decision_id in seen_ids:
            raise RightsManifestError(f"Duplicate decision_id: {decision_id}")
        seen_ids.add(decision_id)

        selector = decision["source_selector"]
        if not isinstance(selector, dict) or len(selector) != 1:
            raise RightsManifestError(f"{field}.source_selector must contain exactly one selector")
        selector_name, selector_value = next(iter(selector.items()))
        if selector_name not in {"source_id", "canonical_domain"}:
            raise RightsManifestError(f"{field}.source_selector has an unsupported selector")
        if not isinstance(selector_value, str) or not selector_value.strip():
            raise RightsManifestError(f"{field}.source_selector value must be non-empty")
        if selector_name == "canonical_domain" and (
            selector_value != selector_value.lower()
            or "://" in selector_value
            or "/" in selector_value
            or "*" in selector_value
        ):
            raise RightsManifestError("canonical_domain must be a lowercase hostname without wildcards")

        status = decision["decision"]
        if status not in RIGHTS:
            raise RightsManifestError(f"{field}.decision is invalid")
        uses = decision["permitted_uses"]
        permitted_fields = decision["permitted_fields"]
        if (
            not isinstance(uses, list) or len(uses) != len(set(uses))
            or any(use not in USES for use in uses)
        ):
            raise RightsManifestError(f"{field}.permitted_uses is invalid")
        if (
            not isinstance(permitted_fields, list)
            or len(permitted_fields) != len(set(permitted_fields))
            or any(item not in FIELDS for item in permitted_fields)
        ):
            raise RightsManifestError(f"{field}.permitted_fields is invalid")
        if not isinstance(decision["restrictions"], dict):
            raise RightsManifestError(f"{field}.restrictions must be an object")
        if not isinstance(decision["rationale"], str) or not decision["rationale"].strip():
            raise RightsManifestError(f"{field}.rationale must be non-empty")

        commercial = "commercial_distribution" in uses
        if status == "cleared":
            if not manifest["legal_memo_ref"].strip():
                raise RightsManifestError("cleared decisions require legal_memo_ref")
            if not commercial or not permitted_fields:
                raise RightsManifestError(
                    "cleared decisions require commercial_distribution and permitted_fields"
                )
        elif commercial:
            raise RightsManifestError(f"{status} decisions cannot permit commercial_distribution")

    signature = manifest.get("signature")
    if require_signature and signature is None:
        raise RightsManifestError("A signature is required")
    if signature is not None:
        if not isinstance(signature, dict):
            raise RightsManifestError("signature must be an object")
        _exact_keys(signature, {"algorithm", "key_id", "value_base64"}, set(), "signature")
        if signature["algorithm"] != SIGNATURE_ALGORITHM:
            raise RightsManifestError("Unsupported signature algorithm")
        for field in ("key_id", "value_base64"):
            if not isinstance(signature[field], str) or not signature[field]:
                raise RightsManifestError(f"signature.{field} must be non-empty")
        try:
            base64.b64decode(signature["value_base64"], validate=True)
        except (ValueError, TypeError) as exc:
            raise RightsManifestError("signature.value_base64 is invalid") from exc


def canonical_payload_bytes(manifest: dict[str, Any]) -> bytes:
    payload = {key: value for key, value in manifest.items() if key != "signature"}
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _run_openssl(arguments: list[str], *, payload: bytes | None = None) -> bytes:
    try:
        completed = subprocess.run(
            ["openssl", *arguments], input=payload, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
    except OSError as exc:
        raise RightsManifestError(f"Cannot execute OpenSSL: {exc}") from exc
    if completed.returncode:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RightsManifestError(f"OpenSSL failed: {message}")
    return completed.stdout


def _ensure_p256(key_path: str | Path, *, public: bool) -> None:
    arguments = ["pkey"]
    if public:
        arguments.append("-pubin")
    arguments.extend(["-in", str(key_path), "-text", "-noout"])
    description = _run_openssl(arguments).decode("utf-8", errors="replace")
    if "ASN1 OID: prime256v1" not in description and "NIST CURVE: P-256" not in description:
        raise RightsManifestError("Signing key must be an ECDSA P-256 key")


def public_key_fingerprint(public_key_path: str | Path) -> str:
    _ensure_p256(public_key_path, public=True)
    der = _run_openssl(["pkey", "-pubin", "-in", str(public_key_path), "-outform", "DER"])
    return hashlib.sha256(der).hexdigest()


def sign_manifest(manifest: dict[str, Any], private_key_path: str | Path) -> dict[str, Any]:
    unsigned = copy.deepcopy(manifest)
    unsigned.pop("signature", None)
    validate_manifest(unsigned, require_signature=False)
    _ensure_p256(private_key_path, public=False)
    public_der = _run_openssl(
        ["pkey", "-in", str(private_key_path), "-pubout", "-outform", "DER"]
    )
    signature = _run_openssl(
        ["dgst", "-sha256", "-sign", str(private_key_path)],
        payload=canonical_payload_bytes(unsigned),
    )
    unsigned["signature"] = {
        "algorithm": SIGNATURE_ALGORITHM,
        "key_id": hashlib.sha256(public_der).hexdigest(),
        "value_base64": base64.b64encode(signature).decode("ascii"),
    }
    return unsigned


def verify_manifest_signature(manifest: dict[str, Any], public_key_path: str | Path) -> None:
    validate_manifest(manifest, require_signature=True)
    signature = manifest["signature"]
    expected_key_id = public_key_fingerprint(public_key_path)
    if signature["key_id"] != expected_key_id:
        raise RightsManifestError("Signature key_id does not match the supplied public key")
    signature_bytes = base64.b64decode(signature["value_base64"], validate=True)
    with tempfile.NamedTemporaryFile() as signature_file:
        signature_file.write(signature_bytes)
        signature_file.flush()
        _run_openssl(
            ["dgst", "-sha256", "-verify", str(public_key_path),
             "-signature", signature_file.name],
            payload=canonical_payload_bytes(manifest),
        )


def _domain(url: str) -> str:
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def _decision_row_id(manifest_id: str, decision_id: str, source_id: str) -> str:
    digest = hashlib.sha256(f"{manifest_id}|{decision_id}|{source_id}".encode()).hexdigest()
    return f"rgt:{digest}"


def register_review_key(
    conn: sqlite3.Connection,
    public_key_path: str | Path,
    *,
    reviewer_identity: str,
    review_authority: str,
    valid_from: str,
    valid_to: str | None = None,
) -> dict[str, str]:
    """Register a public key as an explicitly trusted rights reviewer identity."""
    if not reviewer_identity.strip() or not review_authority.strip():
        raise RightsManifestError("Reviewer identity and authority must be non-empty")
    normalized_from = _utc_text(valid_from)
    normalized_to = _utc_text(valid_to) if valid_to is not None else None
    if normalized_to is not None and normalized_to < normalized_from:
        raise RightsManifestError("Key valid_to must not precede valid_from")
    path = Path(public_key_path)
    try:
        public_key_pem = path.read_text(encoding="ascii")
    except (OSError, UnicodeError) as exc:
        raise RightsManifestError(f"Cannot read public key: {exc}") from exc
    key_id = public_key_fingerprint(path)
    existing = conn.execute(
        """SELECT public_key_pem, reviewer_identity, review_authority, valid_from, valid_to
           FROM rights_review_keys WHERE key_id=?""",
        (key_id,),
    ).fetchone()
    expected = (
        public_key_pem, reviewer_identity, review_authority, normalized_from, normalized_to,
    )
    if existing:
        if tuple(existing) != expected:
            raise RightsManifestError("Review key is already registered with different metadata")
        return {"key_id": key_id, "status": "skipped"}
    conn.execute(
        """INSERT INTO rights_review_keys
           (key_id, algorithm, public_key_pem, reviewer_identity, review_authority,
            valid_from, valid_to)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            key_id, SIGNATURE_ALGORITHM, public_key_pem, reviewer_identity,
            review_authority, normalized_from, normalized_to,
        ),
    )
    return {"key_id": key_id, "status": "registered"}


def apply_manifest(
    conn: sqlite3.Connection,
    manifest: dict[str, Any],
    public_key_path: str | Path,
) -> dict[str, Any]:
    """Verify and transactionally apply one manifest to matching sources."""
    verify_manifest_signature(manifest, public_key_path)
    payload_hash = hashlib.sha256(canonical_payload_bytes(manifest)).hexdigest()
    manifest_id = manifest["manifest_id"]
    key_id = manifest["signature"]["key_id"]
    created_at = _utc_text(manifest["created_at"])
    trusted = conn.execute(
        """SELECT 1 FROM rights_review_keys
           WHERE key_id=? AND status='active' AND reviewer_identity=? AND review_authority=?
             AND datetime(valid_from)<=datetime(?)
             AND (valid_to IS NULL OR datetime(valid_to)>=datetime(?))""",
        (
            key_id, manifest["reviewed_by"], manifest["review_authority"],
            created_at, created_at,
        ),
    ).fetchone()
    if not trusted:
        raise RightsManifestError(
            "Signing key is not an active trusted key for this reviewer and authority"
        )
    existing = conn.execute(
        "SELECT payload_sha256 FROM rights_manifests WHERE manifest_id=?", (manifest_id,)
    ).fetchone()
    if existing:
        if existing[0] != payload_hash:
            raise RightsManifestError("manifest_id already exists with different signed content")
        return {"manifest_id": manifest_id, "status": "skipped", "sources_updated": 0}

    sources = [dict(row) for row in conn.execute("SELECT source_id, canonical_url FROM sources")]
    assignments: dict[str, dict[str, Any]] = {}
    for decision in manifest["decisions"]:
        selector_name, selector_value = next(iter(decision["source_selector"].items()))
        if selector_name == "source_id":
            matches = [row for row in sources if row["source_id"] == selector_value]
        else:
            matches = [row for row in sources if _domain(row["canonical_url"]) == selector_value]
        if not matches:
            raise RightsManifestError(
                f"Decision {decision['decision_id']} selector matched zero sources"
            )
        for source in matches:
            source_id = source["source_id"]
            if source_id in assignments:
                raise RightsManifestError(f"Multiple decisions target source {source_id}")
            assignments[source_id] = decision

    signature = manifest["signature"]
    effective_from = _utc_text(manifest["effective_from"])
    effective_to = (
        _utc_text(manifest["effective_to"]) if manifest["effective_to"] is not None else None
    )
    savepoint = "apply_rights_manifest"
    conn.execute(f"SAVEPOINT {savepoint}")
    try:
        conn.execute(
            """INSERT INTO rights_manifests
               (manifest_id, schema_version, payload_sha256, signature_algorithm,
                signature_key_id, signature_base64, created_at, reviewed_by,
                review_authority, legal_memo_ref, effective_from, effective_to)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                manifest_id, manifest["schema_version"], payload_hash,
                signature["algorithm"], signature["key_id"], signature["value_base64"],
                created_at, manifest["reviewed_by"],
                manifest["review_authority"], manifest["legal_memo_ref"],
                effective_from, effective_to,
            ),
        )
        for source_id, decision in assignments.items():
            conn.execute(
                """INSERT INTO source_rights_decisions
                   (decision_row_id, decision_id, manifest_id, source_id, decision,
                    permitted_uses_json, permitted_fields_json, restrictions_json,
                    rationale, effective_from, effective_to)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    _decision_row_id(manifest_id, decision["decision_id"], source_id),
                    decision["decision_id"], manifest_id, source_id, decision["decision"],
                    json.dumps(decision["permitted_uses"], ensure_ascii=False, sort_keys=True),
                    json.dumps(decision["permitted_fields"], ensure_ascii=False, sort_keys=True),
                    json.dumps(decision["restrictions"], ensure_ascii=False, sort_keys=True),
                    decision["rationale"], effective_from, effective_to,
                ),
            )

        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for source_id in assignments:
            current = conn.execute(
                """SELECT decision, permitted_uses_json
                   FROM source_rights_decisions
                   WHERE source_id=? AND effective_from<=?
                     AND (effective_to IS NULL OR effective_to>=?)
                   ORDER BY effective_from DESC, rowid DESC LIMIT 1""",
                (source_id, now, now),
            ).fetchone()
            status = current[0] if current else "unknown"
            allowed = int(
                status == "cleared"
                and "commercial_distribution" in json.loads(current[1])
            ) if current else 0
            conn.execute(
                "UPDATE sources SET rights_status=?, commercial_use_allowed=? WHERE source_id=?",
                (status, allowed, source_id),
            )
        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
    except BaseException:
        conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        raise
    return {
        "manifest_id": manifest_id,
        "status": "applied",
        "sources_updated": len(assignments),
        "payload_sha256": payload_hash,
    }
