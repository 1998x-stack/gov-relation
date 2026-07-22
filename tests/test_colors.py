"""Tests for gov_relation/colors.py."""

from __future__ import annotations

from gov_relation.colors import _match_role, node_color, node_shape, node_size


class TestMatchRole:
    def test_matches_书记_prefix(self) -> None:
        assert _match_role("区委书记") == "书记"

    def test_matches_副_before_县长_when_both_present(self) -> None:
        # "副县长" should match "副" (longer prefix match) rather than "县长"
        assert _match_role("副县长") == "副"

    def test_常委_match(self) -> None:
        assert _match_role("县委常委") == "常委"

    def test_empty_title_returns_none(self) -> None:
        assert _match_role("") is None

    def test_unknown_title_returns_none(self) -> None:
        assert _match_role("调研员") is None


class TestNodeColor:
    def test_书记_is_red(self) -> None:
        color = node_color("县委书记")
        assert color["r"] == 200
        assert color["g"] == 30
        assert color["b"] == 30

    def test_区长_is_blue(self) -> None:
        color = node_color("区长")
        assert color["r"] == 30
        assert color["g"] == 100
        assert color["b"] == 200

    def test_unknown_role_is_grey(self) -> None:
        color = node_color("调研员")
        assert color["r"] == 180
        assert color["g"] == 180
        assert color["b"] == 180

    def test_returns_all_four_keys(self) -> None:
        color = node_color("市长")
        assert set(color.keys()) == {"r", "g", "b", "a"}


class TestNodeSize:
    def test_书记_gets_large_size(self) -> None:
        assert node_size("县委书记") == 60.0

    def test_unknown_role_default_size(self) -> None:
        assert node_size("调研员") == 20.0

    def test_副职_smaller_than_正职(self) -> None:
        assert node_size("副区长") < node_size("区长")


class TestNodeShape:
    def test_书记_is_square(self) -> None:
        assert node_shape("县委书记") == "square"

    def test_人大_is_diamond(self) -> None:
        assert node_shape("区人大常委会主任") == "diamond"

    def test_政协_is_diamond(self) -> None:
        assert node_shape("县政协主席") == "diamond"

    def test_副职_is_triangle(self) -> None:
        assert node_shape("副县长") == "triangle"

    def test_other_is_circle(self) -> None:
        assert node_shape("局长") == "circle"
