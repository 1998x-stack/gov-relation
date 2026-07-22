"""Tests for gov_relation/slugs.py."""

from __future__ import annotations

from gov_relation.slugs import artifact_paths, region_slug


class TestRegionSlug:
    def test_known_region_returns_mapped_slug(self) -> None:
        assert region_slug("安义县") == "anyi"

    def test_unknown_region_returns_identity(self) -> None:
        assert region_slug("七里河区") == "七里河区"

    def test_empty_string(self) -> None:
        assert region_slug("") == ""


class TestArtifactPaths:
    def test_returns_all_keys(self) -> None:
        paths = artifact_paths("安义县")
        assert set(paths.keys()) == {"slug", "build_script", "db_output", "gexf_output"}

    def test_build_script_for_known_region(self) -> None:
        paths = artifact_paths("安义县")
        assert paths["build_script"] == "build_anyi_data.py"

    def test_db_output_path(self) -> None:
        paths = artifact_paths("安义县")
        assert paths["db_output"] == "data/database/anyi_network.db"

    def test_gexf_output_path(self) -> None:
        paths = artifact_paths("安义县")
        assert paths["gexf_output"] == "data/graph/anyi_network.gexf"

    def test_unknown_region_uses_raw_name_in_paths(self) -> None:
        paths = artifact_paths("七里河区")
        assert paths["build_script"] == "build_七里河区_data.py"
        assert paths["db_output"] == "data/database/七里河区_network.db"

    def test_consistency_db_and_gexf_share_slug(self) -> None:
        paths = artifact_paths("红谷滩区")
        slug = paths["slug"]
        assert slug == "honggutan"
        assert slug in paths["db_output"]
        assert slug in paths["gexf_output"]
