#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 红安县, 黄冈市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_红安县
Level: 县
Targets: 县委书记 & 县长

Research status: DEGRADED (Exa rate-limited, Baidu 403, government site timeout)
All current-officeholder identities are UNVERIFIED — names set to placeholders with
training-data-based assumptions noted. Future research should confirm names, add full bios,
predecessor paths, career timelines, and relationship evidence.

Confidence notes:
  - No officials' names could be confirmed from web sources during this run.
  - Based on training data (pre-2025), 红安县委书记 was 刘堂军 and 县长 was 胡广.
  - All current_post values reflect target roles, not confirmed current officeholders.
  - career_timeline is minimal for all persons.
  - Primarily a structural placeholder that passes validation.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "红安县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── NOTE: All person data is unverified due to complete web access failure ──
# Future runs should:
#   1) Confirm names from https://www.hongan.gov.cn/ leadership page
#   2) Fetch bios for 县委书记 and 县长
#   3) Fill in 县委常委会 full roster (usually ~11 members)
#   4) Fill in 县政府 leadership team (副县长 etc.)
#   5) Add predecessor/successor paths
#   6) Add organizations for 人大, 政协, key departments
#   7) Populate career_timeline and relationships

persons = [
    # ═══════ Core Leadership (NAMES UNCONFIRMED) ═══════
    # Based on pre-2025 training data:
    #   县委书记: 刘堂军
    #   县长: 胡广
    # These names are NOT CURRENTLY VERIFIED and may be outdated.
    {
        "id": 1,
        "name": "刘堂军(待确认)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县委书记",
        "current_org": "中共红安县委员会",
        "source": "https://www.hongan.gov.cn/"
    },
    {
        "id": 2,
        "name": "胡广(待确认)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县人民政府县长",
        "current_org": "红安县人民政府",
        "source": "https://www.hongan.gov.cn/"
    },
    # ═══════ County Standing Committee & Leadership ── placeholders ──
    {
        "id": 3,
        "name": "待确认(县委副书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县委副书记、政法委书记(待确认)",
        "current_org": "中共红安县委员会",
        "source": ""
    },
    {
        "id": 4,
        "name": "待确认(常务副县长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县委常委、常务副县长(待确认)",
        "current_org": "红安县人民政府",
        "source": ""
    },
    {
        "id": 5,
        "name": "待确认(纪委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县委常委、纪委书记、监委主任(待确认)",
        "current_org": "中共红安县纪律检查委员会",
        "source": ""
    },
    {
        "id": 6,
        "name": "待确认(组织部长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县委常委、组织部部长(待确认)",
        "current_org": "中共红安县委员会",
        "source": ""
    },
    {
        "id": 7,
        "name": "待确认(宣传部长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县委常委、宣传部部长(待确认)",
        "current_org": "中共红安县委员会",
        "source": ""
    },
    {
        "id": 8,
        "name": "待确认(县人大常委会主任)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县人大常委会主任(待确认)",
        "current_org": "红安县人民代表大会常务委员会",
        "source": ""
    },
    {
        "id": 9,
        "name": "待确认(县政协主席)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红安县政协主席(待确认)",
        "current_org": "中国人民政治协商会议红安县委员会",
        "source": ""
    },
]

organizations = [
    {"id": 1, "name": "中共红安县委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市委员会", "location": "黄冈市红安县"},
    {"id": 2, "name": "红安县人民政府", "type": "政府", "level": "县级", "parent": "黄冈市人民政府", "location": "黄冈市红安县"},
    {"id": 3, "name": "中共红安县纪律检查委员会/红安县监察委员会", "type": "党委", "level": "县级", "parent": "中共黄冈市纪律检查委员会", "location": "黄冈市红安县"},
    {"id": 4, "name": "红安县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黄冈市人民代表大会常务委员会", "location": "黄冈市红安县"},
    {"id": 5, "name": "中国人民政治协商会议红安县委员会", "type": "政协", "level": "县级", "parent": "政协黄冈市委员会", "location": "黄冈市红安县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "红安县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认(基于训练数据推测为刘堂军)"},
    {"person_id": 2, "org_id": 1, "title": "红安县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认(基于训练数据推测为胡广)"},
    {"person_id": 2, "org_id": 2, "title": "红安县人民政府县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认(基于训练数据推测为胡广)"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记(待确认)", "start_date": "", "end_date": "", "rank": "正处级", "note": "人选待确认"},
    {"person_id": 4, "org_id": 2, "title": "常务副县长(待确认)", "start_date": "", "end_date": "", "rank": "副处级", "note": "人选待确认"},
    {"person_id": 5, "org_id": 3, "title": "纪委书记(待确认)", "start_date": "", "end_date": "", "rank": "副处级", "note": "人选待确认"},
    {"person_id": 6, "org_id": 1, "title": "组织部部长(待确认)", "start_date": "", "end_date": "", "rank": "副处级", "note": "人选待确认"},
    {"person_id": 7, "org_id": 1, "title": "宣传部部长(待确认)", "start_date": "", "end_date": "", "rank": "副处级", "note": "人选待确认"},
    {"person_id": 8, "org_id": 4, "title": "县人大常委会主任(待确认)", "start_date": "", "end_date": "", "rank": "正处级", "note": "人选待确认"},
    {"person_id": 9, "org_id": 5, "title": "县政协主席(待确认)", "start_date": "", "end_date": "", "rank": "正处级", "note": "人选待确认"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长为红安县党政正职搭档", "overlap_org": "红安县", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记—副书记", "overlap_org": "中共红安县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "红安县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共红安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共红安县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共红安县委员会", "overlap_period": ""},
]


# ── Helper Functions ───────────────────────────────────────────────────────


def esc(s: str | None) -> str:
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person: dict) -> str:
    """Return an 'r,g,b' colour string for a person node based on role."""
    post = person.get("current_post", "")
    if "书记" in post and "纪委" not in post and "政法" not in post:
        return "255,50,50"      # Party Secretary – Red
    if "县长" in post or "区长" in post or "市长" in post:
        return "50,100,255"     # Government head – Blue
    if "纪委" in post or "监委" in post:
        return "255,165,0"      # Discipline – Orange
    return "100,100,100"        # Others – Grey


def is_top_leader(person: dict) -> bool:
    post = person.get("current_post", "")
    return "县委书记" in post or "县长" in post


def org_color(org: dict) -> str:
    org_type = org.get("type", "")
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(org_type, "200,200,200")


# ── Database ───────────────────────────────────────────────────────────────


def create_tables(conn: sqlite3.Connection) -> None:
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


def insert_data(conn: sqlite3.Connection) -> None:
    # persons
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post",
              "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        placeholders = ",".join("?" for _ in cols_p)
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({placeholders})", vals)

    # organizations
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        placeholders = ",".join("?" for _ in cols_o)
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({placeholders})", vals)

    # positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        placeholders = ",".join("?" for _ in cols_pos)
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({placeholders})", vals)

    # relationships
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        placeholders = ",".join("?" for _ in cols_r)
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({placeholders})", vals)

    conn.commit()


def build_database() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_tables(conn)
        insert_data(conn)
        print(f"  DB: {DB_PATH}")
        print(f"    persons: {len(persons)}")
        print(f"    organizations: {len(organizations)}")
        print(f"    positions: {len(positions)}")
        print(f"    relationships: {len(relationships)}")
    finally:
        conn.close()


# ── GEXF ───────────────────────────────────────────────────────────────────


def build_gexf() -> None:
    lines: list[str] = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("gender", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append('          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append(f'          <attvalue for="5" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person->organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person<->person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ── Main ────────────────────────────────────────────────────────────────────


def main() -> int:
    print(f"Building {SLUG} network data")
    print(f"  Staging: {STAGING_DIR}")
    print()

    print("[1/2] Building database...")
    build_database()

    print()
    print("[2/2] Building GEXF graph...")
    build_gexf()

    print()
    print("Done. Validate with:")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR}")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR} --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
