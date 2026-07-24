#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汉川市, 孝感市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_汉川市
Level: 县级市
Targets: 市委书记 & 市长

Research status: PARTIAL — web access to Chinese government sites (hanchuan.gov.cn,
xiaogan.gov.cn) is heavily restricted. Site uses JS rendering which cannot be bypassed
with available tools. Baidu Baike returns 403. Exa search API rate-limited.
Previous worker attempts (3x) also failed to produce artifacts.

The following data is based on available news snippets from xiaogan.gov.cn homepage
(which loaded partially), cross-referenced with limited accessible sources.

Confirmed from Xiaogan government homepage news feeds (2026-07-24):
  - 汉川 is active in reporting (news items dated July 2026 about 汉川)
  - 胡玖明 is the 孝感市委书记 (confirmed from xiaogan.gov.cn news)
  - 市政府七届八十一次常务会议召开 (Xiaogan city government active)

Biographical details (birth year, education, birthplace, career timeline):
NOT FOUND — government site requires JavaScript that cannot be rendered.

Given the extended connectivity issues across all three previous worker attempts,
this investigation produces artifacts with explicit uncertainty markers.

NOTE: This script uses the gov_relation runner pattern (similar to 孝昌县_data.py).
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "汉川市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
# NOTE: Leader names NOT confirmed from official sources due to restricted
# web access. All core leader entries use "待确认" (to be confirmed) markers.
# See report/open_gaps.md for priority research items.

persons = [
    # ═══════ Core Leadership (UNVERIFIED — see gaps) ═══════
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委书记",
        "current_org": "中共汉川市委员会",
        "source": "http://www.hanchuan.gov.cn/ (requires JS, unreachable)"
    },
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委副书记、市人民政府市长",
        "current_org": "汉川市人民政府",
        "source": "http://www.hanchuan.gov.cn/ (requires JS, unreachable)"
    },

    # ═══════ Known Xiaogan City Leaders (CONFIRMED from xiaogan.gov.cn) ═══════
    {
        "id": 3,
        "name": "胡玖明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "孝感市委书记",
        "current_org": "中共孝感市委员会",
        "source": "http://www.xiaogan.gov.cn/ (homepage news references)"
    },

    # ═══════ Leadership Team Members (UNVERIFIED) ═══════
    {
        "id": 4,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委常委、常务副市长",
        "current_org": "汉川市人民政府",
        "source": "待确认 — 无访问来源"
    },
    {
        "id": 5,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委副书记",
        "current_org": "中共汉川市委员会",
        "source": "待确认 — 无访问来源"
    },
    {
        "id": 6,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委常委、市纪委书记、市监委主任",
        "current_org": "中共汉川市纪律检查委员会",
        "source": "待确认 — 无访问来源"
    },
    {
        "id": 7,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委常委、组织部部长",
        "current_org": "中共汉川市委员会",
        "source": "待确认 — 无访问来源"
    },
    {
        "id": 8,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委常委、宣传部部长",
        "current_org": "中共汉川市委员会",
        "source": "待确认 — 无访问来源"
    },
    {
        "id": 9,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委常委、政法委书记",
        "current_org": "中共汉川市委员会",
        "source": "待确认 — 无访问来源"
    },
    {
        "id": 10,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉川市委常委、统战部部长",
        "current_org": "中共汉川市委员会",
        "source": "待确认 — 无访问来源"
    },
    # ═══════ Predecessors (UNVERIFIED) ═══════
    {
        "id": 11,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "待确认 — 需调查前任书记信息"
    },
    {
        "id": 12,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "待确认 — 需调查前任市长信息"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共汉川市委员会", "type": "党委", "level": "县处级",
     "parent": "中共孝感市委员会", "location": "湖北省孝感市汉川市"},
    {"id": 2, "name": "汉川市人民政府", "type": "政府", "level": "县处级",
     "parent": "孝感市人民政府", "location": "湖北省孝感市汉川市"},
    {"id": 3, "name": "中共汉川市纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共孝感市纪律检查委员会", "location": "湖北省孝感市汉川市"},
    {"id": 4, "name": "汉川市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "孝感市人民代表大会常务委员会", "location": "湖北省孝感市汉川市"},
    {"id": 5, "name": "中国人民政治协商会议汉川市委员会", "type": "政协", "level": "县处级",
     "parent": "政协孝感市委员会", "location": "湖北省孝感市汉川市"},
    {"id": 6, "name": "汉川市人民武装部", "type": "军事", "level": "县处级",
     "parent": "孝感军分区", "location": "湖北省孝感市汉川市"},
    {"id": 7, "name": "中共孝感市委员会", "type": "党委", "level": "厅级",
     "parent": "中共湖北省委员会", "location": "湖北省孝感市"},
    {"id": 8, "name": "孝感市人民政府", "type": "政府", "level": "厅级",
     "parent": "湖北省人民政府", "location": "湖北省孝感市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 市委书记 (待确认)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "汉川市委书记",
     "start": "", "end": "", "rank": "县处级正职", "note": "现任，姓名待确认"},

    # 市长 (待确认)
    {"id": 2, "person_id": 2, "org_id": 2, "title": "汉川市委副书记、市人民政府市长",
     "start": "", "end": "", "rank": "县处级正职", "note": "现任，姓名待确认"},

    # 胡玖明 (孝感市委书记)
    {"id": 3, "person_id": 3, "org_id": 7, "title": "孝感市委书记",
     "start": "", "end": "", "rank": "厅级", "note": "现任，确认自xiaogan.gov.cn"},

    # 常务副市长 (待确认)
    {"id": 4, "person_id": 4, "org_id": 2, "title": "汉川市委常委、常务副市长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 市委副书记 (待确认)
    {"id": 5, "person_id": 5, "org_id": 1, "title": "汉川市委副书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 纪委书记 (待确认)
    {"id": 6, "person_id": 6, "org_id": 3, "title": "汉川市委常委、市纪委书记、市监委主任",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 组织部长 (待确认)
    {"id": 7, "person_id": 7, "org_id": 1, "title": "汉川市委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 宣传部长 (待确认)
    {"id": 8, "person_id": 8, "org_id": 1, "title": "汉川市委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 政法委书记 (待确认)
    {"id": 9, "person_id": 9, "org_id": 1, "title": "汉川市委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 统战部长 (待确认)
    {"id": 10, "person_id": 10, "org_id": 1, "title": "汉川市委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任，姓名待确认"},

    # 前任书记 (待确认)
    {"id": 11, "person_id": 11, "org_id": 1, "title": "汉川市委书记（前任）",
     "start": "", "end": "", "rank": "县处级正职", "note": "前任，信息待查"},

    # 前任市长 (待确认)
    {"id": 12, "person_id": 12, "org_id": 2, "title": "汉川市人民政府市长（前任）",
     "start": "", "end": "", "rank": "县处级正职", "note": "前任，信息待查"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Note: No confirmed relationships yet — all core names unknown
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "汉川市委书记与市长（党政正职搭档）",
     "overlap_org": "汉川市", "overlap_period": ""},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级",
     "context": "汉川市委书记受孝感市委书记领导",
     "overlap_org": "孝感市", "overlap_period": "2026"},
    {"id": 3, "person_a": 2, "person_b": 3, "type": "上下级",
     "context": "汉川市长受孝感市委领导",
     "overlap_org": "孝感市", "overlap_period": "2026"},
]

# ── BUILD ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Create DB
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
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
        );
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
        );
    """)

    for p in persons:
        conn.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth,
            birthplace, education, party_join, work_start, current_post,
            current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        conn.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    # Stats
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    posc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]
    conn.close()
    print(f"  Persons: {pc}")
    print(f"  Organizations: {oc}")
    print(f"  Positions: {posc}")
    print(f"  Relationships: {rc}")

    # ── GEXF ──
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>china-gov-network skill</creator>')
    lines.append(f'    <description>汉川市领导班子工作关系网络 - {today} (PARTIAL DATA — core names unconfirmed)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
    lines.append('      <attribute id="source" title="Source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="period" title="Period" type="string"/>')
    lines.append('    </attributes>')

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        # Color by role
        if pid == 1:  # 市委书记
            color = "255,50,50"
            size = 20.0
        elif pid == 2:  # 市长
            color = "50,100,255"
            size = 20.0
        elif pid == 3:  # 孝感市委书记 (上级)
            color = "255,100,100"
            size = 16.0
        elif pid == 6:  # 纪委书记
            color = "255,165,0"
            size = 14.0
        else:
            color = "100,100,100"
            size = 12.0

        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        r, g, b = color.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,220,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "军事": "220,220,220",
    }
    for o in organizations:
        oid = 100000 + o["id"]
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append('        </attvalues>')
        r, g, b = oc.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        oid = 100000 + pos["org_id"]
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_nodes = len(persons) + len(organizations)
    total_edges = len(positions) + len(relationships)
    print(f"\nGEXF written: {GEXF_PATH}")
    print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {total_nodes}")
    print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges}")
    print("\n⚠️  WARNING: This build contains PARTIAL data. Core leader names are unconfirmed.")
    print("   See report/open_gaps.md for priority research items to fill.")
    print("Done!")
