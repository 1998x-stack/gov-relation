# gov-relation 系统性重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 对 gov-relation 仓库的代码框架、数据框架、日志框架进行系统性重构，抽公共库、移动目录、收敛命名、统一日志。

**Architecture:** 三圈同步但分步实施：(1) 在 `gov_relation/` 新增 5 个公共模块（schema/gexf/colors/runner/log），新脚本使用公共库从 400 行降到 ~50 行；(2) 迁移根目录入口到 `scripts/tools/`、清理 tmp、收敛命名；(3) 旧 build 脚本分批迁入 `scripts/build/`；(4) 日志统一上线。

**Tech Stack:** Python 3.10+, sqlite3, ElementTree (标准库), logging (标准库), Pathlib

## Global Constraints

- 旧 build 脚本（484 个 `build_*_data.py`）**不改一行**，零风险兼容。
- 新脚本用 `gov_relation.runner.run_build()` 替代模板代码。
- 所有文件路径使用 `gov_relation.paths` 中的常量，不硬编码绝对路径。
- 分批迁移，每批 ~20 个文件，每批一个独立 commit。
- `.agents/skills/china-gov-network/` 中的调研 prompt 模板在最后阶段更新。

---

### Task 1: 创建 `gov_relation/schema.py`

**Files:**
- Create: `gov_relation/schema.py`

**Interfaces:**
- Consumes: `gov_relation.paths` (implied, not directly used here)
- Produces: `create_tables(conn, overwrite=False)`, `insert_persons(conn, persons)`, `insert_organizations(conn, orgs)`, `insert_positions(conn, positions)`, `insert_relationships(conn, relationships)`

- [ ] **Step 1: Create `gov_relation/schema.py`**

```python
"""SQLite schema and bulk-insert helpers for the gov-relation pipeline."""

from __future__ import annotations

import sqlite3
from typing import Any

CREATE_PERSONS = """
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT DEFAULT '',
    ethnicity TEXT DEFAULT '',
    birth TEXT DEFAULT '',
    birthplace TEXT DEFAULT '',
    education TEXT DEFAULT '',
    party_join TEXT DEFAULT '',
    work_start TEXT DEFAULT '',
    current_post TEXT DEFAULT '',
    current_org TEXT DEFAULT '',
    source TEXT DEFAULT ''
)
"""

CREATE_ORGANIZATIONS = """
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
)
"""

CREATE_POSITIONS = """
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    note TEXT DEFAULT '',
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
)
"""

CREATE_RELATIONSHIPS = """
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)
"""


def create_tables(conn: sqlite3.Connection, overwrite: bool = False) -> None:
    """Create the four standard tables.

    Parameters
    ----------
    conn:
        Open SQLite connection.
    overwrite:
        If True, DROP existing tables before creating them.
    """
    if overwrite:
        for name in ("relationships", "positions", "organizations", "persons"):
            conn.execute(f"DROP TABLE IF EXISTS {name}")
    for ddl in (CREATE_PERSONS, CREATE_ORGANIZATIONS, CREATE_POSITIONS, CREATE_RELATIONSHIPS):
        conn.execute(ddl)
    conn.commit()


_COLUMN_MAP: dict[str, list[str]] = {
    "persons": ["id", "name", "gender", "ethnicity", "birth", "birthplace",
                 "education", "party_join", "work_start", "current_post",
                 "current_org", "source"],
    "organizations": ["id", "name", "type", "level", "parent", "location"],
    "positions": ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"],
    "relationships": ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"],
}


def _columns(table: str) -> list[str]:
    return _COLUMN_MAP.get(table, [])


def _placeholders(count: int) -> str:
    return ",".join("?" for _ in range(count))


def insert_persons(conn: sqlite3.Connection, persons: list[dict[str, Any]]) -> dict[int, int]:
    """Insert persons and return a mapping from old id → new rowid.

    The returned mapping lets callers update organization/position foreign keys
    after insertion.
    """
    cols = _columns("persons")
    placeholders = _placeholders(len(cols))
    id_map: dict[int, int] = {}
    for entry in persons:
        values = [entry.get(c, "") for c in cols]
        cur = conn.execute(f"INSERT INTO persons ({','.join(cols)}) VALUES ({placeholders})", values)
        id_map[entry["id"]] = cur.lastrowid
    conn.commit()
    return id_map


def insert_organizations(conn: sqlite3.Connection, organizations: list[dict[str, Any]]) -> dict[int, int]:
    """Insert organizations and return a mapping from old id → new rowid."""
    cols = _columns("organizations")
    placeholders = _placeholders(len(cols))
    id_map: dict[int, int] = {}
    for entry in organizations:
        values = [entry.get(c, "") for c in cols]
        cur = conn.execute(f"INSERT INTO organizations ({','.join(cols)}) VALUES ({placeholders})", values)
        id_map[entry["id"]] = cur.lastrowid
    conn.commit()
    return id_map


def insert_positions(conn: sqlite3.Connection, positions: list[dict[str, Any]]) -> None:
    """Insert position records."""
    cols = _columns("positions")
    placeholders = _placeholders(len(cols))
    for entry in positions:
        values = [entry.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO positions ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()


def insert_relationships(conn: sqlite3.Connection, relationships: list[dict[str, Any]]) -> None:
    """Insert relationship records."""
    cols = _columns("relationships")
    placeholders = _placeholders(len(cols))
    for entry in relationships:
        values = [entry.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO relationships ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()
```

- [ ] **Step 2: Quick smoke test**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
import sqlite3, tempfile, os
from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships
with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
    conn = sqlite3.connect(f.name)
    create_tables(conn)
    id_map = insert_persons(conn, [{'id': 1, 'name': '测试', 'current_post': '书记'}])
    assert id_map[1] == 1
    rows = conn.execute('SELECT name FROM persons').fetchall()
    assert rows == [('测试',)]
    os.unlink(f.name)
    print('schema.py smoke test PASSED')
"
```

Expected: `schema.py smoke test PASSED`

- [ ] **Step 3: Commit**

```bash
git add gov_relation/schema.py
git commit -m "feat(gov_relation): add schema.py with standard table DDL and bulk-insert helpers"
```

---

### Task 2: 创建 `gov_relation/colors.py`

**Files:**
- Create: `gov_relation/colors.py`

**Interfaces:**
- Produces: `node_color(role, level="")`, `node_size(role, level="")`, `node_shape(title)`

- [ ] **Step 1: Create `gov_relation/colors.py`**

```python
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
    "书记", "副书记", "区长", "县长", "市长", "省长",
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
    """Find the first role key that appears in *title*."""
    for role in _ROLE_ORDER:
        if role in title:
            return role
    return None


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
```

- [ ] **Step 2: Quick smoke test**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
from gov_relation.colors import node_color, node_size, node_shape
# 书记 should be red
c = node_color('区委书记')
assert c['r'] > 150 and c['g'] < 80, f'unexpected color: {c}'
# 区长 should be blue
c = node_color('区长')
assert c['g'] > 80 and c['b'] > 150, f'unexpected color: {c}'
# size
assert node_size('区委书记') == 60.0
assert node_size('副区长') == 35.0
assert node_shape('区委书记') == 'square'
assert node_shape('区长') == 'circle'
print('colors.py smoke test PASSED')
"
```

Expected: `colors.py smoke test PASSED`

- [ ] **Step 3: Commit**

```bash
git add gov_relation/colors.py
git commit -m "feat(gov_relation): add colors.py with role-based node style rules"
```

---

### Task 3: 创建 `gov_relation/gexf.py`

**Files:**
- Create: `gov_relation/gexf.py`

**Interfaces:**
- Consumes: `gov_relation.colors`
- Produces: `GEXFBuilder`

- [ ] **Step 1: Create `gov_relation/gexf.py`**

```python
"""GEXF graph builder for gov-relation networks.

Usage::

    builder = GEXFBuilder("七里河区领导班子关系图")
    builder.add_person(1, "胡真", current_post="区委书记")
    builder.add_organization(1, "中共七里河区委员会")
    builder.add_relationship(1, 2, "共事", "区委书记—区长")
    builder.write("output.gexf")
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from .colors import node_color, node_size, node_shape


class GEXFBuilder:
    """Build a GEXF graph incrementally and write to file."""

    def __init__(self, title: str = "") -> None:
        self._title = title
        self._nodes: dict[int, dict[str, Any]] = {}
        self._edges: list[dict[str, Any]] = []
        self._edge_counter = 0

    def add_person(
        self,
        id: int,
        name: str,
        current_post: str = "",
        current_org: str = "",
        gender: str = "",
        ethnicity: str = "",
        birth: str = "",
        source: str = "",
    ) -> None:
        """Add a person node.

        Color and size are inferred from *current_post* via
        ``gov_relation.colors``.
        """
        color = node_color(current_post)
        size = node_size(current_post)
        shape = node_shape(current_post)
        self._nodes[id] = {
            "label": name,
            "type": "person",
            "current_post": current_post,
            "current_org": current_org,
            "gender": gender,
            "ethnicity": ethnicity,
            "birth": birth,
            "source": source,
            "r": color["r"],
            "g": color["g"],
            "b": color["b"],
            "a": color["a"],
            "size": size,
            "shape": shape,
        }

    def add_organization(
        self,
        id: int,
        name: str,
        org_type: str = "",
        level: str = "",
        location: str = "",
    ) -> None:
        """Add an organization node."""
        self._nodes[id] = {
            "label": name,
            "type": "organization",
            "org_type": org_type,
            "level": level,
            "location": location,
            "r": 220,
            "g": 220,
            "b": 220,
            "a": 0.8,
            "size": 15.0,
            "shape": "hexagon",
        }

    def add_relationship(
        self,
        source: int,
        target: int,
        rel_type: str,
        context: str = "",
        overlap_org: str = "",
        overlap_period: str = "",
    ) -> None:
        """Add a directed edge between two nodes."""
        self._edge_counter += 1
        self._edges.append({
            "id": self._edge_counter,
            "source": source,
            "target": target,
            "type": rel_type,
            "context": context,
            "overlap_org": overlap_org,
            "overlap_period": overlap_period,
        })

    def write(self, path: Path | str) -> None:
        """Serialize the graph to a GEXF file."""
        root = ET.Element(
            "gexf",
            attrib={
                "xmlns": "http://www.gexf.net/1.3",
                "xmlns:viz": "http://www.gexf.net/1.3/viz",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd",
                "version": "1.3",
            },
        )
        graph = ET.SubElement(root, "graph", attrib={
            "mode": "static",
            "defaultedgetype": "directed",
        })

        if self._title:
            meta = ET.SubElement(root, "meta")
            title_el = ET.SubElement(meta, "title")
            title_el.text = self._title

        # ── Attributes ──
        attributes = ET.SubElement(graph, "attributes", attrib={"class": "node"})
        for attr_id, attr_name, attr_type in [
            ("0", "type", "string"),
            ("1", "current_post", "string"),
            ("2", "current_org", "string"),
            ("3", "gender", "string"),
            ("4", "ethnicity", "string"),
            ("5", "birth", "string"),
            ("6", "source", "string"),
            ("7", "org_type", "string"),
            ("8", "level", "string"),
            ("9", "location", "string"),
        ]:
            a = ET.SubElement(attributes, "attribute", attrib={"id": attr_id, "title": attr_name, "type": attr_type})

        edge_attrs = ET.SubElement(graph, "attributes", attrib={"class": "edge"})
        for eid, ename, etype in [
            ("0", "type", "string"),
            ("1", "context", "string"),
            ("2", "overlap_org", "string"),
            ("3", "overlap_period", "string"),
        ]:
            a = ET.SubElement(edge_attrs, "attribute", attrib={"id": eid, "title": ename, "type": etype})

        # ── Nodes ──
        nodes_el = ET.SubElement(graph, "nodes")
        for nid, data in sorted(self._nodes.items()):
            node_el = ET.SubElement(nodes_el, "node", attrib={"id": str(nid), "label": data["label"]})
            ET.SubElement(node_el, "viz:size", attrib={"value": f"{data['size']:.1f}"})
            ET.SubElement(node_el, "viz:shape", attrib={"value": data["shape"]})
            ET.SubElement(node_el, "viz:color", attrib={
                "r": str(data["r"]),
                "g": str(data["g"]),
                "b": str(data["b"]),
                "a": str(data["a"]),
            })
            for attr_id, key in [
                ("0", "type"),
                ("1", "current_post"),
                ("2", "current_org"),
                ("3", "gender"),
                ("4", "ethnicity"),
                ("5", "birth"),
                ("6", "source"),
                ("7", "org_type"),
                ("8", "level"),
                ("9", "location"),
            ]:
                val = data.get(key, "")
                if val:
                    attvalues = node_el.find("attvalues")
                    if attvalues is None:
                        attvalues = ET.SubElement(node_el, "attvalues")
                    ET.SubElement(attvalues, "attvalue", attrib={"for": attr_id, "value": val})

        # ── Edges ──
        edges_el = ET.SubElement(graph, "edges")
        for edge in self._edges:
            edge_el = ET.SubElement(edges_el, "edge", attrib={
                "id": str(edge["id"]),
                "source": str(edge["source"]),
                "target": str(edge["target"]),
            })
            for attr_id, key in [("0", "type"), ("1", "context"), ("2", "overlap_org"), ("3", "overlap_period")]:
                val = edge.get(key, "")
                if val:
                    attvalues = edge_el.find("attvalues")
                    if attvalues is None:
                        attvalues = ET.SubElement(edge_el, "attvalues")
                    ET.SubElement(attvalues, "attvalue", attrib={"for": attr_id, "value": val})

        # ── Write ──
        tree = ET.ElementTree(root)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(str(path), encoding="utf-8", xml_declaration=True)

    def to_string(self) -> str:
        """Return the GEXF XML as a string (for testing)."""
        import io
        buf = io.BytesIO()
        root = ET.Element("gexf", attrib={"xmlns": "http://www.gexf.net/1.3", "version": "1.3"})
        # minimal serialization for testing
        graph = ET.SubElement(root, "graph")
        nodes_el = ET.SubElement(graph, "nodes")
        for nid, data in sorted(self._nodes.items()):
            ET.SubElement(nodes_el, "node", attrib={"id": str(nid), "label": data["label"]})
        edges_el = ET.SubElement(graph, "edges")
        for edge in self._edges:
            ET.SubElement(edges_el, "edge", attrib={
                "id": str(edge["id"]), "source": str(edge["source"]), "target": str(edge["target"]),
            })
        tree = ET.ElementTree(root)
        tree.write(buf, encoding="utf-8", xml_declaration=True)
        return buf.getvalue().decode("utf-8")
```

- [ ] **Step 2: Smoke test**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
from gov_relation.gexf import GEXFBuilder
b = GEXFBuilder('Test')
b.add_person(1, '胡真', current_post='区委书记')
b.add_person(2, '孙洋', current_post='区长')
b.add_relationship(1, 2, '共事')
xml = b.to_string()
assert '胡真' in xml
assert '孙洋' in xml
assert 'source=\"1\"' in xml
assert 'target=\"2\"' in xml
import tempfile, os
with tempfile.NamedTemporaryFile(suffix='.gexf', delete=False) as f:
    b.write(f.name)
    os.unlink(f.name)
print('gexf.py smoke test PASSED')
"
```

Expected: `gexf.py smoke test PASSED`

- [ ] **Step 3: Commit**

```bash
git add gov_relation/gexf.py
git commit -m "feat(gov_relation): add gexf.py with GEXFBuilder class"
```

---

### Task 4: 创建 `gov_relation/log.py`

**Files:**
- Create: `gov_relation/log.py`

**Interfaces:**
- Produces: `get_logger(name)`, `init_logging(log_dir, level)`

- [ ] **Step 1: Create `gov_relation/log.py`**

```python
"""Unified logging configuration for the gov-relation pipeline.

Usage::

    from gov_relation.log import get_logger

    logger = get_logger(__name__)
    logger.info("Wrote GEXF: %s", path)
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_LOG_CONFIGURED = False
_DEFAULT_LOG_DIR = None  # set on first init_logging call


def _default_log_dir() -> Path:
    """Lazily resolve the logs directory relative to this file's repo."""
    return Path(__file__).resolve().parents[1] / "logs"


def get_logger(name: str) -> logging.Logger:
    """Return a logger with unified formatting.

    The first call to this function performs one-time initialization
    of the root handler configuration.
    """
    global _LOG_CONFIGURED
    if not _LOG_CONFIGURED:
        _init_root()
        _LOG_CONFIGURED = True
    return logging.getLogger(name)


def _init_root() -> None:
    """Configure the root logger with a console handler (WARNING+).

    File handlers are added by ``init_logging()`` which should be called
    from the application entry point.  This minimal setup ensures log
    calls from library code always have somewhere to go.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(_formatter())
        root.addHandler(handler)


def _formatter() -> logging.Formatter:
    return logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def init_logging(log_dir: Path | None = None, level: int = logging.INFO) -> None:
    """Initialize file logging with rotation.

    Call this once from the application entry point (e.g. ``worker_loop.py``
    or ``scripts/todo_queue.py``).  Adds a rotating file handler to the
    root logger.

    Parameters
    ----------
    log_dir:
        Directory for ``gov_relation.log``.  Defaults to ``<repo>/logs/``.
    level:
        Log level for the file handler.  Default ``INFO``.
    """
    from logging.handlers import RotatingFileHandler

    global _DEFAULT_LOG_DIR
    _DEFAULT_LOG_DIR = Path(log_dir) if log_dir else _default_log_dir()
    _DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    log_path = _DEFAULT_LOG_DIR / "gov_relation.log"
    handler = RotatingFileHandler(
        str(log_path),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(_formatter())
    root.addHandler(handler)
```

- [ ] **Step 2: Smoke test**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
from gov_relation.log import get_logger, init_logging
import tempfile, os
with tempfile.TemporaryDirectory() as d:
    init_logging(log_dir=Path(d))
    logger = get_logger('test')
    logger.info('hello world')
    log_file = Path(d) / 'gov_relation.log'
    assert log_file.exists()
    content = log_file.read_text()
    assert 'hello world' in content
    assert 'INFO' in content
print('log.py smoke test PASSED')
"
```

Replace `Path(d)` with the import: the test is inline Python. Use:

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
from pathlib import Path
import tempfile
from gov_relation.log import get_logger, init_logging
with tempfile.TemporaryDirectory() as d:
    init_logging(log_dir=Path(d))
    logger = get_logger('test')
    logger.info('hello gov_relation')
    content = (Path(d) / 'gov_relation.log').read_text()
    assert 'hello gov_relation' in content
    assert 'INFO' in content
print('log.py smoke test PASSED')
"
```

Expected: `log.py smoke test PASSED`

- [ ] **Step 3: Commit**

```bash
git add gov_relation/log.py
git commit -m "feat(gov_relation): add log.py with unified logging and rotation"
```

---

### Task 5: 创建 `gov_relation/runner.py` + 更新 `__init__.py`

**Files:**
- Create: `gov_relation/runner.py`
- Modify: `gov_relation/__init__.py`

**Interfaces:**
- Consumes: `gov_relation.schema`, `gov_relation.gexf`, `gov_relation.log`
- Produces: `run_build(slug, persons, organizations, positions, relationships, db_path, gexf_path, overwrite=False)`

- [ ] **Step 1: Create `gov_relation/runner.py`**

```python
"""Top-level orchestration for a single region network build.

Usage::

    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    run_build(
        slug="七里河区",
        persons=[...],
        organizations=[...],
        positions=[...],
        relationships=[...],
        db_path=DATABASE_DIR / "七里河区_network.db",
        gexf_path=GRAPH_DIR / "七里河区_network.gexf",
    )
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .gexf import GEXFBuilder
from .log import get_logger
from .schema import (
    create_tables,
    insert_organizations,
    insert_persons,
    insert_positions,
    insert_relationships,
)

logger = get_logger(__name__)


def run_build(
    *,
    slug: str,
    persons: list[dict[str, Any]],
    organizations: list[dict[str, Any]],
    positions: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    db_path: str | Path,
    gexf_path: str | Path,
    overwrite: bool = False,
) -> None:
    """Orchestrate a full region network build.

    Parameters
    ----------
    slug:
        Region slug (e.g. ``"七里河区"``), used for the GEXF title.
    persons:
        Person records (list of dicts with at minimum ``id`` and ``name``).
    organizations:
        Organization records.
    positions:
        Position records.
    relationships:
        Relationship records.
    db_path:
        Output path for the SQLite database.
    gexf_path:
        Output path for the GEXF graph file.
    overwrite:
        If True, drop existing tables before inserting.
    """
    db_path = Path(db_path)
    gexf_path = Path(gexf_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    gexf_path.parent.mkdir(parents=True, exist_ok=True)

    # ── SQLite ──
    logger.info("Building database: %s", db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        create_tables(conn, overwrite=overwrite)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        logger.info(
            "DB ready: %d persons, %d orgs, %d positions, %d relationships",
            len(persons),
            len(organizations),
            len(positions),
            len(relationships),
        )
    finally:
        conn.close()

    # ── GEXF ──
    logger.info("Building GEXF: %s", gexf_path)
    builder = GEXFBuilder(title=slug)
    for p in persons:
        builder.add_person(
            id=p["id"],
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )
    for o in organizations:
        builder.add_organization(
            id=o["id"],
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )
    for r in relationships:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )
    builder.write(gexf_path)
    logger.info("GEXF ready: %s", gexf_path)
```

- [ ] **Step 2: Update `gov_relation/__init__.py`**

```python
"""Shared utilities for the gov-relation research pipeline."""

from .paths import REPO_ROOT, data_path, repo_path
from .log import get_logger

__all__ = [
    "REPO_ROOT",
    "data_path",
    "repo_path",
    "get_logger",
]
```

- [ ] **Step 3: Integration smoke test (build a real DB + GEXF from test data)**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
import tempfile, os, sqlite3
from pathlib import Path
from gov_relation.runner import run_build

persons = [
    {'id': 1, 'name': '张三', 'current_post': '区委书记'},
    {'id': 2, 'name': '李四', 'current_post': '区长'},
]
organizations = [
    {'id': 1, 'name': '中共XX区委员会', 'type': '党委', 'level': '县处级'},
]
positions = [
    {'person_id': 1, 'org_id': 1, 'title': '区委书记'},
    {'person_id': 2, 'org_id': 1, 'title': '区长'},
]
relationships = [
    {'person_a': 1, 'person_b': 2, 'type': '共事', 'context': '区委书记—区长'},
]

with tempfile.TemporaryDirectory() as d:
    db = Path(d) / 'test_network.db'
    gexf = Path(d) / 'test_network.gexf'
    run_build(slug='test', persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=db, gexf_path=gexf, overwrite=True)
    assert db.exists(), 'db not created'
    assert gexf.exists(), 'gexf not created'
    conn = sqlite3.connect(str(db))
    rows = conn.execute('SELECT COUNT(*) FROM persons').fetchone()
    assert rows[0] == 2, f'unexpected person count: {rows[0]}'
    conn.close()
    xml = gexf.read_text(encoding='utf-8')
    assert '张三' in xml
    assert '李四' in xml
print('runner.py integration test PASSED')
"
```

Expected: `runner.py integration test PASSED`

- [ ] **Step 4: Commit**

```bash
git add gov_relation/runner.py gov_relation/__init__.py
git commit -m "feat(gov_relation): add runner.py with run_build orchestration"
```

---

### Task 6: 数据框架 — 迁移 `run_todo_loop.py` 和 `generate_build_template.py` 到 `scripts/tools/`

**Files:**
- Move: `run_todo_loop.py` → `scripts/tools/run_todo_loop.py`
- Move: `generate_build_template.py` → `scripts/tools/generate_build_template.py`
- Modify: `scripts/todo_queue.py` (verify sys.path still works)
- Modify: `scripts/worker_loop.py` (verify sys.path still works)

- [ ] **Step 1: Stop any running workers**

```bash
bash scripts/stop_workers.sh 2>/dev/null || true
```

- [ ] **Step 2: Create `scripts/tools/` directory and move files**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
mkdir -p scripts/tools
git mv run_todo_loop.py scripts/tools/run_todo_loop.py
git mv generate_build_template.py scripts/tools/generate_build_template.py
```

- [ ] **Step 3: Verify sys.path works from the new location**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
# scripts/tools/ files are 2 levels deep from repo root
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts/tools/run_todo_loop.py').resolve().parents[2]))
# Should be able to import gov_relation
from gov_relation.todo import load_todo
print('sys.path works from scripts/tools/')
"
```

- [ ] **Step 4: Verify `scripts/todo_queue.py` and `scripts/worker_loop.py` still work**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
# todo_queue.py uses sys.path.insert(0, parents[1]) which is repo root
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('scripts/todo_queue.py').resolve().parents[1]))
from gov_relation.queue import queue_status
s = queue_status()
print(f'Queue OK: {s[\"done\"]}/{s[\"total\"]} done')
"
```

Expected: `Queue OK: 618/3116 done` (or similar)

- [ ] **Step 5: Commit**

```bash
git add scripts/tools/ scripts/todo_queue.py scripts/worker_loop.py
git commit -m "refactor(data): move root-level scripts to scripts/tools/"
```

---

### Task 7: 数据框架 — 清理已完成的 `data/tmp/` 目录

**Files:**
- Modify: `scripts/tools/process_tmp.py` (if needed)
- Delete: completed `data/tmp/<task_id>/` directories

- [ ] **Step 1: Write and run the tmp cleanup script**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
import json
from pathlib import Path
from gov_relation.todo import load_todo, iter_items

todo = load_todo()
# Collect all done task IDs
done_ids = set()
for item in iter_items(todo):
    if item.item.get('done'):
        done_ids.add(item.item['id'])

tmp_dir = Path('data/tmp')
if not tmp_dir.exists():
    print('No data/tmp/ directory')
    exit(0)

to_remove = []
for d in tmp_dir.iterdir():
    if d.is_dir() and d.name in done_ids:
        to_remove.append(d.name)

print(f'Found {len(to_remove)} completed task tmp dirs out of {len(list(tmp_dir.iterdir()))} total')
for name in sorted(to_remove)[:20]:
    print(f'  would remove: {name}')
if len(to_remove) > 20:
    print(f'  ... and {len(to_remove) - 20} more')
"
```

- [ ] **Step 2: After review, actually remove them**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
import shutil
from pathlib import Path
from gov_relation.todo import load_todo, iter_items

todo = load_todo()
done_ids = {item.item['id'] for item in iter_items(todo) if item.item.get('done')}
tmp_dir = Path('data/tmp')
removed = 0
failed = 0
for d in sorted(tmp_dir.iterdir()):
    if d.is_dir() and d.name in done_ids:
        try:
            shutil.rmtree(d)
            removed += 1
        except Exception as e:
            print(f'FAILED {d.name}: {e}')
            failed += 1
print(f'Removed {removed} tmp dirs. Failed: {failed}')
"
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "cleanup(data): remove completed task tmp directories"
```

---

### Task 8: 数据框架 — 修复命名例外

**Files:**
- Rename: `data/database/chenzhou.db` → `data/database/chenzhou_network.db`
- Rename: `data/database/jingdezhen_mayor.db` → `data/database/jingdezhen_mayor_network.db`
- Modify: `gov_relation/inventory.py` (update scan patterns if needed)

- [ ] **Step 1: Rename the files**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
git mv data/database/chenzhou.db data/database/chenzhou_network.db 2>/dev/null || echo "chenzhou.db not found (may already be renamed)"
git mv data/database/jingdezhen_mayor.db data/database/jingdezhen_mayor_network.db 2>/dev/null || echo "jingdezhen_mayor.db not found (may already be renamed)"
```

- [ ] **Step 2: Commit**

```bash
git commit -m "fix(data): normalize database filenames to *_network.db convention"
```

---

### Task 9: 数据框架 — 更新 `scripts/inventory.py` 扫描范围

**Files:**
- Modify: `gov_relation/inventory.py`
- Modify: `scripts/inventory.py`

- [ ] **Step 1: Update `gov_relation/inventory.py`**

The current `collect_inventory` only scans root directory for `build_*_data.py`. Update it to also scan `scripts/build/`.

```python
# Inside collect_inventory(), change the scripts line:
def collect_inventory(root: Path = REPO_ROOT) -> Inventory:
    scripts = sorted(root.glob("build_*_data.py"))
    scripts.extend(sorted((root / "scripts" / "build").glob("*.py"))) if (root / "scripts" / "build").exists() else None
    # ... rest unchanged
```

Actually, to keep the frozen dataclass simple, just update the patterns:

Replace line 44:
```python
    scripts = sorted(root.glob("build_*_data.py"))
```
with:
```python
    scripts = sorted(root.glob("build_*_data.py"))
    build_dir = root / "scripts" / "build"
    if build_dir.exists():
        scripts.extend(sorted(build_dir.glob("*_data.py")))
```

- [ ] **Step 2: Verify the inventory still works**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 scripts/inventory.py
```

Expected: prints repository inventory counts.

- [ ] **Step 3: Commit**

```bash
git add gov_relation/inventory.py
git commit -m "fix(inventory): scan both root and scripts/build/ for build scripts"
```

---

### Task 10: 日志框架 — 启用统一日志（gov_relation/ 模块 + worker_loop.py）

**Files:**
- Modify: `gov_relation/queue.py`
- Modify: `gov_relation/dispatch.py`
- Modify: `gov_relation/slugs.py`
- Modify: `gov_relation/todo.py`
- Modify: `gov_relation/inventory.py`
- Modify: `gov_relation/web.py`
- Modify: `scripts/worker_loop.py`

- [ ] **Step 1: Add `get_logger(__name__)` to each gov_relation module**

For `gov_relation/queue.py`, add after the imports:
```python
from .log import get_logger

logger = get_logger(__name__)
```

For `gov_relation/dispatch.py`, add:
```python
from .log import get_logger

logger = get_logger(__name__)
```

For `gov_relation/todo.py`, add:
```python
from .log import get_logger

logger = get_logger(__name__)
```

For `gov_relation/inventory.py`, add:
```python
from .log import get_logger

logger = get_logger(__name__)
```

For `gov_relation/web.py`, add:
```python
from .log import get_logger

logger = get_logger(__name__)
```

- [ ] **Step 2: Replace worker_loop.py's self-made `log()` with unified logger**

In `scripts/worker_loop.py`, replace:
```python
from gov_relation.queue import canonical_artifacts_ready, claim_next, set_claim_status
from gov_relation.slugs import artifact_paths
```
with:
```python
from gov_relation.log import get_logger, init_logging
from gov_relation.queue import canonical_artifacts_ready, claim_next, set_claim_status
from gov_relation.slugs import artifact_paths

logger = get_logger(__name__)
```

Then replace the `log()` function and all calls to it:
```python
# Remove this whole function:
def log(message: str) -> None:
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    print(f"[{ts}] {message}", flush=True)
```

Replace all `log(f"...")` calls with `logger.info("...")`.

At the start of `main()`, add:
```python
def main() -> int:
    init_logging()
```

- [ ] **Step 3: Commit**

```bash
git add gov_relation/queue.py gov_relation/dispatch.py gov_relation/todo.py
git add gov_relation/inventory.py gov_relation/web.py
git add scripts/worker_loop.py
git commit -m "feat(log): enable unified logging across all gov_relation modules and worker_loop"
```

---

### Task 11: 日志框架 — 重排日志目录

**Files:**
- Move: `logs/batch_*.log` → `logs/batch/`
- Move: `logs/jiangxi_*.log` etc. → `logs/tasks/`

- [ ] **Step 1: Create subdirectories and move files**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
mkdir -p logs/batch logs/tasks

# Move batch logs
for f in logs/batch_*.log; do
    [ -f "$f" ] && git mv "$f" logs/batch/ 2>/dev/null || true
done

# Move task logs (jiangxi_*, gansu_*, etc.)
for f in logs/*.log; do
    base=$(basename "$f")
    # skip files already in subdirectories
    case "$base" in
        batch_*|worker_*|watchdog_*|todo_*) ;;
        *.pid) ;;
        *)
            if [ -f "$f" ] && [ "$(dirname "$f")" = "logs" ]; then
                git mv "$f" logs/tasks/ 2>/dev/null || true
            fi
            ;;
    esac
done
```

- [ ] **Step 2: Verify no loose logs remain**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
remaining=$(find logs/ -maxdepth 1 -name '*.log' -type f)
if [ -n "$remaining" ]; then
    echo "Remaining loose logs: $remaining"
else
    echo "All logs organized."
fi
```

- [ ] **Step 3: Commit**

```bash
git add logs/
git commit -m "refactor(logs): organize log files into batch/ and tasks/ subdirectories"
```

---

### Task 12: 调研 agent prompt 模板更新

**Files:**
- Modify: `.agents/skills/china-gov-network/references/investigation_stages.md` (or equivalent prompt template)

- [ ] **Step 1: Locate the prompt template that generates build script instructions**

```bash
grep -rn "build_" .agents/skills/china-gov-network/ | grep -i "prompt\|template\|instruction" | head -20
```

- [ ] **Step 2: Update the template to reference `gov_relation.runner.run_build()`**

In the relevant prompt template, replace the "Write a build script" section with instructions to import and use `runner.run_build()` instead of writing raw SQLite + GEXF code.

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/china-gov-network/
git commit -m "docs(skill): update prompt template to use gov_relation.runner"
```

---

### Task 13: 旧 build 脚本迁移（首批 ~20 个）

**Files:**
- Move: 20 oldest/least-referenced `build_*_data.py` → `scripts/build/`

- [ ] **Step 1: Select and move 20 scripts**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
mkdir -p scripts/build
# Pick 20 files that are alphabetically first (arbitrary batch)
for f in $(ls build_*.py | head -20); do
    git mv "$f" scripts/build/
done
```

- [ ] **Step 2: Commit**

```bash
git add scripts/build/
git commit -m "refactor(scripts): migrate 20 build scripts to scripts/build/"
```

---

### Task 14: 更新 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README paths to reflect new structure**

Read the current README, update references:
- `scripts/todo_queue.py claim` (already correct)
- `run_todo_loop.py` → `scripts/tools/run_todo_loop.py`
- `generate_build_template.py` → `scripts/tools/generate_build_template.py`
- Add section about `gov_relation.runner` for new scripts
- Add section about unified logging

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README for new directory structure and runner"
```

---

### Task 15: 最终验证

- [ ] **Step 1: Run inventory**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 scripts/inventory.py
```

Expected: clean output showing all build scripts in root + scripts/build/.

- [ ] **Step 2: Run queue status**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 scripts/tools/run_todo_loop.py --status  # new path
# or:
python3 scripts/todo_queue.py status
```

Both should work.

- [ ] **Step 3: Verify a new-style build script works**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
python3 -c "
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
# Minimal example
run_build(
    slug='demo',
    persons=[{'id': 1, 'name': '测试', 'current_post': '副书记'}],
    organizations=[{'id': 1, 'name': '测试组织'}],
    positions=[{'person_id': 1, 'org_id': 1, 'title': '副书记'}],
    relationships=[],
    db_path='/tmp/demo_network.db',
    gexf_path='/tmp/demo_network.gexf',
    overwrite=True,
)
import os; os.unlink('/tmp/demo_network.db'); os.unlink('/tmp/demo_network.gexf')
print('End-to-end demo build PASSED')
"
```

Expected: `End-to-end demo build PASSED`

- [ ] **Step 4: Verify log file was written**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
ls -la logs/gov_relation.log 2>/dev/null || echo "log file not created (expected if init_logging was not called yet)"

# Trigger init_logging:
python3 -c "from gov_relation.log import init_logging; init_logging()"
ls -la logs/gov_relation.log
```

- [ ] **Step 5: Confirm git status is clean**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
git status --short
```
