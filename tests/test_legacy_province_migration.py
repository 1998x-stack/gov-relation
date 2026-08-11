"""Tests for fail-closed legacy province resolution."""

import importlib.util
from pathlib import Path


def _module():
    path = Path("scripts/migrate/migrate_legacy_to_provinces.py").resolve()
    spec = importlib.util.spec_from_file_location("legacy_provinces", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_unique_region_resolves():
    module = _module()
    assert module.resolve_province("data/database/a.db", "唯一县", {"唯一县": {"sichuan"}}, {}) == ("sichuan", "todo")


def test_cross_province_name_is_ambiguous():
    module = _module()
    slug, reason = module.resolve_province(
        "data/database/朝阳区_network.db",
        "朝阳区",
        {"朝阳区": {"beijing", "jilin"}},
        {},
    )
    assert slug is None and reason.startswith("ambiguous:")


def test_exact_path_override_resolves_ambiguity():
    module = _module()
    path = "data/database/朝阳区_network.db"
    assert module.resolve_province(
        path, "朝阳区", {"朝阳区": {"beijing", "jilin"}}, {path: "beijing"}
    ) == ("beijing", "override")
