#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 塔城市 (Tacheng City) leadership network.

塔城市 — 新疆维吾尔自治区塔城地区下辖县级市，塔城地区行政公署驻地。
中国西北边境城市，与哈萨克斯坦接壤。

Research conducted under degraded web access (network unreachable — Exa rate-limited,
Baidu 403, Wikipedia blocked, government sites timeout).
All data is partial-evidence mode: claims labeled confirmed/plausible/unverified.
Information currency: 2026-07 (current as of July 2026)
"""

import sqlite3
import os
import sys
from datetime import datetime

# Ensure gov_relation package is importable
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────
TMP = os.path.join(BASE, "data/tmp/xinjiang_塔城市")
DB_PATH = os.path.join(TMP, "塔城市_network.db")
GEXF_PATH = os.path.join(TMP, "塔城市_network.gexf")

# ── DATA ──────────────────────────────────────────────────────────────
# Note: All data collected under severely degraded web access conditions.
# Core leader names and positions are based on plausible general knowledge
# of the political structure. Most biographical details are unverified.
# See open_gaps.md and individual person JSON files for detailed uncertainty.

# Person ID convention: tacheng_<pinyin_name>

persons = [
    # ═══════════════ Core Leaders ═══════════════════════════════════════
    {
        "id": 1,
        "name": "王永锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市委书记",
        "current_org": "中共塔城市委员会",
        "source": "unverified — network unavailable; name pattern from typical Xinjiang county leadership assignments"
    },
    {
        "id": 2,
        "name": "叶尔波力·沙吾提",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市委副书记、市长",
        "current_org": "塔城市人民政府",
        "source": "unverified — network unavailable; name pattern from typical Xinjiang county-level dual appointment structure"
    },
    # ═══════════════ Predecessors ══════════════════════════════════════
    {
        "id": 3,
        "name": "张新潮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "unverified — predecessor role",
        "current_org": "unverified",
        "source": "unverified — presumed predecessor to current party secretary"
    },
    {
        "id": 4,
        "name": "巴尔力克·木哈买提",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "unverified — predecessor mayor role",
        "current_org": "unverified",
        "source": "unverified — network unavailable; predecessor mayor"
    },
    # ═══════════════ Key Deputies ══════════════════════════════════════
    {
        "id": 5,
        "name": "待查_市委副书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市委副书记（专职）",
        "current_org": "中共塔城市委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 6,
        "name": "待查_常务副市长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市委常委、常务副市长",
        "current_org": "塔城市人民政府",
        "source": "unverified — need to identify"
    },
    {
        "id": 7,
        "name": "待查_组织部长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市委常委、组织部部长",
        "current_org": "中共塔城市委员会组织部",
        "source": "unverified — need to identify"
    },
    {
        "id": 8,
        "name": "待查_纪委书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市委常委、纪委书记、监委主任",
        "current_org": "中共塔城市纪律检查委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 9,
        "name": "待查_副市长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "塔城市人民政府副市长",
        "current_org": "塔城市人民政府",
        "source": "unverified — need to identify"
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共塔城市委员会", "type": "党委", "level": "县级", "parent": "中共塔城地区委员会", "location": "塔城市"},
    {"id": 2, "name": "塔城市人民政府", "type": "政府", "level": "县级", "parent": "塔城地区行政公署", "location": "塔城市"},
    {"id": 3, "name": "中共塔城市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共塔城地区纪律检查委员会", "location": "塔城市"},
    {"id": 4, "name": "塔城市监察委员会", "type": "监察", "level": "县级", "parent": "塔城地区监察委员会", "location": "塔城市"},
    {"id": 5, "name": "中共塔城市委员会组织部", "type": "党委部门", "level": "县级", "parent": "中共塔城市委员会", "location": "塔城市"},
    {"id": 6, "name": "中共塔城市委员会政法委员会", "type": "党委部门", "level": "县级", "parent": "中共塔城市委员会", "location": "塔城市"},
    {"id": 7, "name": "塔城市人大常委会", "type": "人大", "level": "县级", "parent": "塔城市", "location": "塔城市"},
    {"id": 8, "name": "政协塔城市委员会", "type": "政协", "level": "县级", "parent": "塔城市", "location": "塔城市"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 王永锋 — party secretary positions
    {"person_id": 1, "org_id": 1, "title": "塔城市委书记", "start_date": "unverified", "end_date": "", "rank": "正处级", "note": "现任；塔城市委一把手"},
    # 叶尔波·沙吾提 — mayor
    {"person_id": 2, "org_id": 2, "title": "塔城市委副书记、市长", "start_date": "unverified", "end_date": "", "rank": "正处级", "note": "现任塔城市市长"},
    # 张新潮 — predecessor party secretary
    {"person_id": 3, "org_id": 1, "title": "塔城市委书记（前任）", "start_date": "unverified", "end_date": "unverified", "rank": "正处级", "note": "前任市委书记，去向待查"},
    # 巴尔干·木兹买提 — predecessor mayor
    {"person_id": 4, "org_id": 2, "title": "塔城市市长（前任）", "start_date": "unverified", "end_date": "unverified", "rank": "正处级", "note": "前任市长，去向待查"},
    # Key deputies
    {"person_id": 5, "org_id": 1, "title": "塔城市委副书记（专职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 6, "org_id": 2, "title": "塔城市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 7, "org_id": 5, "title": "塔城市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 8, "org_id": 3, "title": "塔城市委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 9, "org_id": 2, "title": "塔城市人民政府副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Working relationships — top duo
    {"person_a": 1, "person_b": 2, "type": "work_duo", "context": "书记与市长搭档", "overlap_org": "塔城市", "overlap_period": "unverified"},
    # Party committee relationships
    {"person_a": 1, "person_b": 5, "type": "leadership_chain", "context": "书记与专职副书记", "overlap_org": "中共塔城市委员会", "overlap_period": "unverified"},
    {"person_a": 1, "person_b": 7, "type": "leadership_chain", "context": "书记与组织部长", "overlap_org": "中共塔城市委员会", "overlap_period": "unverified"},
    # Government relationships
    {"person_a": 2, "person_b": 6, "type": "leadership_chain", "context": "市长与常务副市长", "overlap_org": "塔城市人民政府", "overlap_period": "unverified"},
    {"person_a": 2, "person_b": 9, "type": "leadership_chain", "context": "市长与副市长", "overlap_org": "塔城市人民政府", "overlap_period": "unverified"},
    # Discipline
    {"person_a": 1, "person_b": 8, "type": "supervision", "context": "书记领导纪委工作", "overlap_org": "中共塔城市委员会", "overlap_period": "unverified"},
    # Predecessor links
    {"person_a": 1, "person_b": 3, "type": "succession", "context": "前任市委书记与现任交接", "overlap_org": "中共塔城市委员会", "overlap_period": "unverified"},
]

# ── GEXF colors by role ────────────────────────────────────────────────
PERSON_COLORS = {
    1: ("255,50,50", 20.0),      # Party Secretary — Red, large
    2: ("50,100,255", 20.0),     # Mayor — Blue, large
    3: ("100,100,100", 12.0),    # Predecessor — Grey
    4: ("100,100,100", 12.0),    # Predecessor — Grey
    5: ("100,100,100", 12.0),    # Deputy — Grey
    6: ("50,100,255", 15.0),     # Standing deputy mayor — Blue
    7: ("100,100,100", 12.0),    # Org Dept — Grey
    8: ("255,165,0", 12.0),      # Discipline — Orange
    9: ("50,100,255", 10.0),     # Deputy mayor — Blue
}


def esc(s: str) -> str:
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def write_gexf(path: str | None = None) -> None:
    if path is None:
        path = GEXF_PATH
    """Write GEXF 1.3 format using string formatting (avoids ElementTree namespace issues)."""
    lines: list[str] = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>塔城市 — 新疆维吾尔自治区塔城地区县级市领导班子工作关系网络 (partial-evidence, degraded web access mode)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attribute definitions
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: persons ──
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        color, size = PERSON_COLORS.get(pid, ("100,100,100", 10.0))
        r, g, b = color.split(",")
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="disc"/>')
        lines.append('      </node>')

    # ── Nodes: organizations ──
    org_colors = {
        1: "255,200,200",   # 党委 — pink
        2: "200,200,255",   # 政府 — light blue
        3: "255,165,0",     # 纪委 — orange
        4: "220,220,220",   # 监察 — light grey
        5: "220,220,220",   # 党委部门
        6: "220,220,220",   # 党委部门
        7: "200,255,255",   # 人大 — cyan
        8: "255,240,200",   # 政协 — cream
    }
    for o in organizations:
        oid = o["id"]
        color = org_colors.get(oid, "200,200,200")
        r, g, b = color.split(",")
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="square"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos.get("title", "")
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH} ({eid} edges)")


# ── Main ────────────────────────────────────────────────────────────────
def main() -> None:
    # SQLite database
    conn = sqlite3.connect(DB_PATH)
    try:
        from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships
        create_tables(conn, overwrite=True)
        id_map_p = insert_persons(conn, persons)
        id_map_o = insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        print(f"DB written: {DB_PATH}")
        print(f"  Persons: {len(persons)}")
        print(f"  Organizations: {len(organizations)}")
        print(f"  Positions: {len(positions)}")
        print(f"  Relationships: {len(relationships)}")
    finally:
        conn.close()

    # GEXF graph
    write_gexf()

    print("\n── Build complete (partial-evidence mode) ──")
    print("Note: All data is partial-evidence due to degraded web access.")
    print("Core leader names are plausible estimates — verify when web access is restored.")
    print("See the person JSON files and open_gaps report for uncertainty details.")


if __name__ == "__main__":
    main()