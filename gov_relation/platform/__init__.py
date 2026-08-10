"""Canonical data platform for government personnel relationship data."""

from .schema import SCHEMA_VERSION, connect, create_schema

__all__ = ["SCHEMA_VERSION", "connect", "create_schema"]
