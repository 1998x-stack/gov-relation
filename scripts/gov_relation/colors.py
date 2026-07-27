"""Node style rules for GEXF graph visualization.

Roles hierarchy for size/color:
  一级党委 > 政府一把手 > 副职 > 党委常委/政协 > 部门负责人 > 其他
"""

from __future__ import annotations

from typing import Any

# ── Standard role → color mapping ──────────────────────────────────
# RGB tuples 0-255, plus alpha.  Role-matching is prefix-based:
# e.g. "区委书记" matches "书记", "市长" matches "市长".

_ROLE_COLORS: dict[str, tuple[int, int, int, float]] = {
    "书记": (200, 30, 30, 1.0),         # 深红 — 一把手
    "区长": (30, 100, 200, 1.0),         # 深蓝 — 政府首长
    "县长": (30, 100, 200, 1.0),         # 深蓝
    "市长": (30, 100, 200, 1.0),         # 深蓝
    "省长": (30, 100, 200, 1.0),         # 深蓝
    "副书记": (220, 80, 80, 0.9),        # 浅红 — 副书记
    "副": (100, 150, 220, 0.85),         # 浅蓝 — 副职
    "常委": (180, 100, 180, 0.85),       # 紫色 — 常委
    "主任": (60, 180, 60, 0.85),         # 绿色 — 人大/政协负责人
    "主席": (60, 180, 60, 0.85),         # 绿色
    "局长": (200, 160, 50, 0.8),         # 金色 — 部门负责人
    "部长": (200, 160, 50, 0.8),
}

_DEFAULT_COLOR = (180, 180, 180, 0.7)

_ROLE_ORDER: list[str] = [
    "副书记", "书记", "区长", "县长", "市长", "省长",
    "副", "常委", "主任", "主席", "局长", "部长",
]

_NODE_SIZES: dict[str, float] = {
    "书记": 60.0,
    "副书记": 45.0,
    "区长": 50.0,
    "县长": 50.0,
    "市长": 55.0,
    "省长": 60.0,
    "副": 35.0,
    "常委": 30.0,
    "主任": 30.0,
    "主席": 30.0,
    "局长": 25.0,
    "部长": 25.0,
}

_DEFAULT_SIZE = 20.0


def _match_role(title: str) -> str | None:
    """Find the role key that appears in *title*.

    Prefers start-of-title prefix matches over substring matches,
    then prefers longer matches over shorter ones.
    This ensures "副区长" matches "副" instead of "区长".
    """
    candidates: list[tuple[int, int, str]] = []
    for role in _ROLE_ORDER:
        if role in title:
            start_p = -1 if title.startswith(role) else 0
            candidates.append((start_p, -len(role), role))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][2]


def node_color(role: str, level: str = "") -> dict[str, Any]:
    """Return a GEXF ``<color>``-compatible dict for the given role.

    Returns
    -------
    dict with keys ``r``, ``g``, ``b``, ``a``.
    """
    matched = _match_role(role)
    r, g, b, a = _ROLE_COLORS.get(matched, _DEFAULT_COLOR)
    return {"r": r, "g": g, "b": b, "a": a}


def node_size(role: str, level: str = "") -> float:
    """Return the node size for the given role."""
    matched = _match_role(role)
    if matched and matched in _NODE_SIZES:
        return _NODE_SIZES[matched]
    return _DEFAULT_SIZE


def node_shape(title: str) -> str:
    """Return the GEXF node shape.

    Intended for a person's full title string.
    """
    if "书记" in title:
        return "square"
    if "人大" in title or "政协" in title:
        return "diamond"
    if "副" in title:
        return "triangle"
    return "circle"
