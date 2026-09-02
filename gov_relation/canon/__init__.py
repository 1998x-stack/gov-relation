"""Canonical JSONL + SQLite backup data engine.

Design contract
    - ``data/records/<table>.jsonl`` is the single system of record. Every line
      is one JSON object (one row). Content-addressable via manifest sha256.
    - ``data/database/platform.db`` is a *derived* SQLite backup, rebuilt from
      the JSONL streams by ``gov2 backup``. It is disposable and never the
      source of truth.
    - ``gov2 verify`` guarantees the two representations are byte-for-byte
      consistent (same row order, same values, same counts).
    - A ``records/schema.sql`` holds the DDL and ``records/manifest.json`` the
      canonical catalogue (schema version, per-stream counts and hashes,
      lineage) so the backup can always be rebuilt from a bare checkout.

Pillars
-------
- Pillar A (data generation): write JSONL streams, then rebuild SQLite backup.
- Pillar B (data visualization): read JSONL/SQLite -> GEXF/graph/dashboard.
- Pillar C (data classification/induction): derive taxonomy from JSONL.
"""

from __future__ import annotations

from .engine import (
    export_db_to_records,
    rebuild_db_from_records,
    verify_consistency,
    write_manifest,
)
from .streams import iter_jsonl, write_jsonl, jsonl_sha256, table_columns

SCHEMA_VERSION = "2.0.0"

__all__ = [
    "SCHEMA_VERSION",
    "export_db_to_records",
    "rebuild_db_from_records",
    "verify_consistency",
    "write_manifest",
    "iter_jsonl",
    "write_jsonl",
    "jsonl_sha256",
    "table_columns",
]