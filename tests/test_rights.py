"""Tests for signed, fail-closed source-rights decisions."""

from __future__ import annotations

import copy
import sqlite3
import subprocess
from pathlib import Path

import pytest

from gov_relation.platform.rights import (
    RightsManifestError,
    apply_manifest,
    register_review_key,
    sign_manifest,
    validate_manifest,
    verify_manifest_signature,
)
from gov_relation.platform.schema import SCHEMA_VERSION, connect, create_schema


def _keys(tmp_path: Path) -> tuple[Path, Path]:
    private_key = tmp_path / "private.pem"
    public_key = tmp_path / "public.pem"
    subprocess.run(
        [
            "openssl", "genpkey", "-algorithm", "EC", "-pkeyopt",
            "ec_paramgen_curve:P-256", "-out", str(private_key),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["openssl", "pkey", "-in", str(private_key), "-pubout", "-out", str(public_key)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return private_key, public_key


def _manifest(*, manifest_id: str = "rights-2026-001") -> dict:
    return {
        "schema_version": "1.0",
        "manifest_id": manifest_id,
        "created_at": "2026-08-10T00:00:00Z",
        "reviewed_by": "reviewer@example.test",
        "review_authority": "Test Rights Committee",
        "legal_memo_ref": "LEGAL-2026-001",
        "effective_from": "2026-01-01T00:00:00Z",
        "effective_to": None,
        "decisions": [
            {
                "decision_id": "decision-001",
                "source_selector": {"canonical_domain": "example.gov"},
                "decision": "cleared",
                "permitted_uses": ["customer_display", "commercial_distribution"],
                "permitted_fields": ["identity", "career"],
                "restrictions": {"attribution_required": True},
                "rationale": "Synthetic source cleared for test use.",
            }
        ],
    }


def _database(path: Path) -> sqlite3.Connection:
    conn = connect(path)
    create_schema(conn)
    conn.execute(
        """INSERT INTO sources
           (source_id, canonical_url, title, source_type, reliability)
           VALUES ('src:1', 'https://example.gov/person/1', 'Test source', 'official', 'high')"""
    )
    conn.commit()
    return conn


def _trust_key(conn: sqlite3.Connection, public_key: Path) -> None:
    register_review_key(
        conn,
        public_key,
        reviewer_identity="reviewer@example.test",
        review_authority="Test Rights Committee",
        valid_from="2026-01-01T00:00:00Z",
    )
    conn.commit()


def test_commercial_clearance_requires_memo_use_and_fields() -> None:
    manifest = _manifest()
    manifest["legal_memo_ref"] = ""
    with pytest.raises(RightsManifestError, match="legal_memo_ref"):
        validate_manifest(manifest, require_signature=False)

    manifest = _manifest()
    manifest["decisions"][0]["permitted_uses"] = ["customer_display"]
    with pytest.raises(RightsManifestError, match="commercial_distribution"):
        validate_manifest(manifest, require_signature=False)

    manifest = _manifest()
    manifest["decisions"][0]["decision"] = "restricted"
    with pytest.raises(RightsManifestError, match="cannot permit"):
        validate_manifest(manifest, require_signature=False)


def test_sign_verify_and_tamper_detection(tmp_path: Path) -> None:
    private_key, public_key = _keys(tmp_path)
    signed = sign_manifest(_manifest(), private_key)
    verify_manifest_signature(signed, public_key)

    tampered = copy.deepcopy(signed)
    tampered["decisions"][0]["rationale"] = "Changed after signature"
    with pytest.raises(RightsManifestError, match="OpenSSL failed"):
        verify_manifest_signature(tampered, public_key)


def test_apply_is_atomic_audited_and_idempotent(tmp_path: Path) -> None:
    private_key, public_key = _keys(tmp_path)
    conn = _database(tmp_path / "canonical.db")
    signed = sign_manifest(_manifest(), private_key)

    with pytest.raises(RightsManifestError, match="not an active trusted key"):
        apply_manifest(conn, signed, public_key)
    _trust_key(conn, public_key)

    result = apply_manifest(conn, signed, public_key)
    assert result["status"] == "applied"
    assert result["sources_updated"] == 1
    source = conn.execute(
        "SELECT rights_status, commercial_use_allowed FROM sources WHERE source_id='src:1'"
    ).fetchone()
    assert tuple(source) == ("cleared", 1)
    assert conn.execute("SELECT COUNT(*) FROM rights_manifests").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM source_rights_decisions").fetchone()[0] == 1

    repeated = apply_manifest(conn, signed, public_key)
    assert repeated["status"] == "skipped"
    assert conn.execute("SELECT COUNT(*) FROM source_rights_decisions").fetchone()[0] == 1
    conn.close()


def test_unmatched_or_overlapping_decisions_write_nothing(tmp_path: Path) -> None:
    private_key, public_key = _keys(tmp_path)
    conn = _database(tmp_path / "canonical.db")
    _trust_key(conn, public_key)

    unmatched = _manifest(manifest_id="unmatched")
    unmatched["decisions"][0]["source_selector"] = {"source_id": "missing"}
    with pytest.raises(RightsManifestError, match="zero sources"):
        apply_manifest(conn, sign_manifest(unmatched, private_key), public_key)
    assert conn.execute("SELECT COUNT(*) FROM rights_manifests").fetchone()[0] == 0

    overlapping = _manifest(manifest_id="overlapping")
    second = copy.deepcopy(overlapping["decisions"][0])
    second["decision_id"] = "decision-002"
    second["source_selector"] = {"source_id": "src:1"}
    overlapping["decisions"].append(second)
    with pytest.raises(RightsManifestError, match="Multiple decisions"):
        apply_manifest(conn, sign_manifest(overlapping, private_key), public_key)
    assert conn.execute("SELECT COUNT(*) FROM rights_manifests").fetchone()[0] == 0
    assert tuple(conn.execute(
        "SELECT rights_status, commercial_use_allowed FROM sources"
    ).fetchone()) == ("unknown", 0)
    conn.close()


def test_expired_clearance_never_enters_commercial_view(tmp_path: Path) -> None:
    private_key, public_key = _keys(tmp_path)
    conn = _database(tmp_path / "canonical.db")
    _trust_key(conn, public_key)
    expired = _manifest(manifest_id="expired")
    expired["effective_from"] = "2020-01-01T00:00:00Z"
    expired["effective_to"] = "2021-01-01T00:00:00Z"

    result = apply_manifest(conn, sign_manifest(expired, private_key), public_key)
    assert result["status"] == "applied"
    assert conn.execute("SELECT COUNT(*) FROM gold_commercial_sources").fetchone()[0] == 0
    assert tuple(conn.execute(
        "SELECT rights_status, commercial_use_allowed FROM sources"
    ).fetchone()) == ("unknown", 0)
    conn.close()


def test_schema_upgrades_additively_from_2_0(tmp_path: Path) -> None:
    path = tmp_path / "old.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    conn.execute("INSERT INTO schema_meta VALUES ('schema_version', '2.0.0')")
    conn.commit()
    conn.close()

    upgraded = connect(path)
    create_schema(upgraded)
    assert upgraded.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()[0] == SCHEMA_VERSION
    assert upgraded.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='rights_manifests'"
    ).fetchone()
    upgraded.close()
