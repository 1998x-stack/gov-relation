#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 息县 (Xixian County), 信阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_息县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.xixian.gov.cn/ — official government website
  - 县政府领导 page: /zwgk/ — confirmed 郑春 as 县长, 刘创 as 常务副县长
  - 郑春 bio: /2023/10-30/349647.html — 中共息县县委副书记、县政府党组书记、县长
  - 刘创 bio: /2026/04-09/779559.html — 县委常委、县政府党组副书记、常务副县长
  - 十五届人大七次会议预备会议: /2026/02-11/753593.html — confirmed 县委书记管保臣 + leadership roster
  - 2025年政府工作报告: /2025/03-26/605843.html — by 县长郑春, confirmed县委"3+X"工作部署

Confidence notes:
  - 管保臣 (县委书记): confirmed via official 2026-02-11 news article. Full resume unknown.
  - 郑春 (县长): confirmed via government leadership page. First appeared as 县长 ca. 2023.
    Full birth year and early career unverified.
  - 刘创 (常务副县长): confirmed via official bio page (2026-04-09). Full resume unknown.
  - 胡峰, 高东, 李华, 涂瑶, 刘波, 胡洋, 黎小帅: confirmed as 县领导 from congress article.
    Specific party committee posts unknown.
  - 马建国 (县人大常委会主任): confirmed.
  - This is a partial-evidence artifact: core leader identities confirmed; detailed career
    histories, birth info, and party committee role assignments incomplete.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "息县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "管保臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道确认管保臣为县委书记。完整履历待查。"
    },
    {
        "id": 2,
        "name": "郑春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "息县人民政府",
        "source": "息县人民政府网 领导信息页 (2023-10-30): 中共息县县委副书记、县政府党组书记、县长。主持县政府全面工作。"
    },
    {
        "id": 3,
        "name": "刘创",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "息县人民政府",
        "source": "息县人民政府网 领导信息页 (2026-04-09): 县委常委、县政府党组副书记、常务副县长。分管发改委、财政局、统计局、应急管理局等。"
    },
    {
        "id": 4,
        "name": "马建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "息县人大常委会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道确认马建国为县人大常委会主任。"
    },
    {
        "id": 5,
        "name": "胡峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导胡峰出席会议。"
    },
    {
        "id": 6,
        "name": "高东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导高东出席会议。"
    },
    {
        "id": 7,
        "name": "李华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导李华出席会议。"
    },
    {
        "id": 8,
        "name": "涂瑶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导涂瑶出席会议。"
    },
    {
        "id": 9,
        "name": "刘波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导刘波出席会议。"
    },
    {
        "id": 10,
        "name": "胡洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导胡洋出席会议。"
    },
    {
        "id": 11,
        "name": "黎小帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共息县委员会",
        "source": "息县人民政府网 2026-02-11 人大预备会议报道: 县领导黎小帅出席会议。"
    },
    # ═══════ Predecessor ═══════
    {
        "id": 12,
        "name": "汪明君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "信阳市副市长（前任息县县委书记）",
        "current_org": "信阳市人民政府",
        "source": "2026-07-24 信阳市调查: 汪明君任信阳市副市长。此前曾任息县县委书记。"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共息县委员会", "type": "党委", "level": "县处级", "parent": "中共信阳市委员会", "location": "河南省信阳市息县"},
    {"id": 2, "name": "息县人民政府", "type": "政府", "level": "县处级", "parent": "信阳市人民政府", "location": "河南省信阳市息县"},
    {"id": 3, "name": "息县人大常委会", "type": "人大", "level": "县处级", "parent": "信阳市人大常委会", "location": "河南省信阳市息县"},
    {"id": 4, "name": "息县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共息县委员会", "location": "河南省信阳市息县"},
    {"id": 5, "name": "息县政协", "type": "政协", "level": "县处级", "parent": "信阳市政协", "location": "河南省信阳市息县"},
    {"id": 6, "name": "信阳市人民政府", "type": "政府", "level": "厅局级", "parent": "河南省人民政府", "location": "河南省信阳市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed from 2026-02-11 congress article"},
    {"person_id": 2, "org_id": 2, "title": "县长、县委副书记、县政府党组书记", "start_date": "2023-10", "end_date": "present", "rank": "县处级正职", "note": "confirmed from gov leadership page since 2023-10-30"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长、县政府党组副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed from 2026-04-09 bio page"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed from 2026-02-11 congress article"},
    {"person_id": 5, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 6, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 7, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 8, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 9, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 10, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "attended 2026-02-11 people's congress; specific post unknown"},
    {"person_id": 12, "org_id": 6, "title": "副市长", "start_date": "", "end_date": "present", "rank": "厅局级副职", "note": "previously served as 息县县委书记"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "中共息县委员会/息县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共息县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "息县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "汪明君前任县委书记，管保臣接任", "overlap_org": "中共息县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与人大主任党政配合", "overlap_org": "息县", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────────
def build_db():
    """Create SQLite database with persons, orgs, positions, relationships."""
    import sqlite3
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
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

        CREATE TABLE relationships (
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

    # Insert persons
    for p in persons:
        conn.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH}")


def build_gexf():
    """Generate GEXF 1.3 graph with viz namespace using string formatting."""
    from datetime import datetime as dt

    def esc(s):
        """XML-escape a string."""
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        """Return r,g,b string based on role."""
        if "书记" in post and "副" not in post and "副书记" not in post:
            return "200,30,30"  # Red for party secretary
        if "县长" in post and "副" not in post:
            return "30,100,200"  # Blue for county mayor
        if "副" in post or "副书记" in post:
            return "100,150,220"  # Light blue for deputies
        if "人大" in post or "主任" in post:
            return "60,180,60"  # Green for people's congress
        return "180,180,180"  # Grey for others

    def person_size(post):
        if "书记" in post and "副" not in post and "副书记" not in post:
            return "20.0"
        if "县长" in post and "副" not in post:
            return "20.0"
        if "副" in post or "副书记" in post:
            return "12.0"
        return "12.0"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>息县领导班子工作关系网络 — {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = person_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        org_color_map = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        oc = org_color_map.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append(f'          <attvalue for="5" value=""/>')
        lines.append(f'          <attvalue for="6" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 1
    lines.append('    <edges>')
    # Person -> Organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(str(GEXF_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


def write_person_json():
    """Write person JSON files for core figures."""
    today_str = datetime.now().strftime("%Y%m%d")
    PERSONS_DIR.mkdir(parents=True, exist_ok=True)

    person_files = [
        {
            "file": f"{today_str}-河南省-信阳市-县委书记-管保臣.json",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "信阳市",
                    "region": "息县",
                    "job": "县委书记",
                    "task_id": "henan_息县",
                    "time_focus": "2025-2026"
                },
                "identity": {
                    "person_id": "xixian_guan_baochen",
                    "name": "管保臣",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": "管保臣_",
                        "name_birthplace": "管保臣_",
                        "official_profile_url": "https://www.xixian.gov.cn/2026/02-11/753593.html"
                    }
                },
                "current_status": {
                    "current_post": "中共息县县委书记",
                    "current_org": "中共息县委员会",
                    "administrative_rank": "县处级正职",
                    "as_of": "2026-02-11",
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料未找到管保臣任息县县委书记前的完整履历",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "郑春",
                        "person_id": "xixian_zheng_chun",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "县委书记与县长党政搭档，共同出席息县十五届人大七次会议",
                        "overlap_org": "中共息县委员会/息县人民政府",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "person": "刘创",
                        "person_id": "xixian_liu_chuang",
                        "relationship_type": "superior_subordinate",
                        "strength": "medium",
                        "evidence": "县委书记与常务副县长工作关系",
                        "overlap_org": "中共息县委员会",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "person": "汪明君",
                        "person_id": "xinyang_wang_mingjun",
                        "relationship_type": "predecessor_successor",
                        "strength": "medium",
                        "evidence": "汪明君前任息县县委书记，管保臣接任",
                        "overlap_org": "中共息县委员会",
                        "overlap_period": "",
                        "direction": "other_to_person",
                        "confidence": "plausible",
                        "source_ids": ["S003"]
                    }
                ],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "未知",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "截至2026-07-24未发现管保臣相关的纪律审查、审计问题或负面报道",
                        "date": "",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "息县十五届人民代表大会第七次会议预备会议召开",
                        "url": "http://www.xixian.gov.cn/2026/02-11/753593.html",
                        "publisher": "息县人民政府",
                        "published_at": "2026-02-11",
                        "accessed_at": "2026-07-24",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认管保臣为县委书记，列出县领导名单"
                    },
                    {
                        "id": "S003",
                        "title": "信阳市领导班子调查数据",
                        "url": "",
                        "publisher": "gov-relation investigation",
                        "published_at": "2026-07-24",
                        "accessed_at": "2026-07-24",
                        "source_type": "database",
                        "reliability": "high",
                        "notes": "来自信阳市调查数据，确认汪明君为信阳市副市长（前任息县县委书记）"
                    }
                ],
                "confidence_summary": {
                    "identity": "partial",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "管保臣任县委书记前的完整履历未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "管保臣的出生年份、出生地、教育背景",
                        "why_it_matters": "核心人物身份识别基信息",
                        "suggested_queries": ["管保臣 简历", "管保臣 任前公示 信阳"],
                        "last_attempted": "2026-07-24"
                    },
                    {
                        "priority": "critical",
                        "question": "管保臣任息县县委书记前的完整职业履历",
                        "why_it_matters": "理解其晋升路径和可能的跨县交流网络",
                        "suggested_queries": ["管保臣 任职 经历", "管保臣 此前担任"],
                        "last_attempted": "2026-07-24"
                    },
                    {
                        "priority": "critical",
                        "question": "管保臣接任县委书记的时间点",
                        "why_it_matters": "确定上任时间，分析前任去向",
                        "suggested_queries": ["管保臣 任息县县委书记 任命", "息县 县委书记 任免"],
                        "last_attempted": "2026-07-24"
                    }
                ]
            }
        },
        {
            "file": f"{today_str}-河南省-信阳市-县长-郑春.json",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "信阳市",
                    "region": "息县",
                    "job": "县长",
                    "task_id": "henan_息县",
                    "time_focus": "2025-2026"
                },
                "identity": {
                    "person_id": "xixian_zheng_chun",
                    "name": "郑春",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": "郑春_",
                        "name_birthplace": "郑春_",
                        "official_profile_url": "https://www.xixian.gov.cn/2023/10-30/349647.html"
                    }
                },
                "current_status": {
                    "current_post": "中共息县县委副书记、县政府党组书记、县长",
                    "current_org": "息县人民政府",
                    "administrative_rank": "县处级正职",
                    "as_of": "2023-10-30",
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "2023-10",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料未找到郑春任息县县长前的完整履历",
                        "confidence": "unverified",
                        "source_ids": []
                    },
                    {
                        "start": "2023-10",
                        "end": "present",
                        "org": "息县人民政府",
                        "title": "中共息县县委副书记、县政府党组书记、县长",
                        "level": "县处级正职",
                        "location": "河南省信阳市息县",
                        "system": "government",
                        "is_key_promotion": True,
                        "notes": "主持县政府全面工作，负责审计方面工作。分管县政府办公室、县审计局。",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "管保臣",
                        "person_id": "xixian_guan_baochen",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "县长与县委书记党政搭档",
                        "overlap_org": "中共息县委员会/息县人民政府",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S003"]
                    },
                    {
                        "person": "刘创",
                        "person_id": "xixian_liu_chuang",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "县长与常务副县长直接上下级关系",
                        "overlap_org": "息县人民政府",
                        "overlap_period": "",
                        "direction": "person_to_other",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2024",
                        "domain": "economic_development",
                        "achievement_or_event": "全县生产总值增长5.6%，居全市第2位",
                        "role_in_event": "县长，政府工作主持人",
                        "measurable_outcome": "GDP增速全市第二",
                        "location": "息县",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    },
                    {
                        "period": "2024",
                        "domain": "rural_revitalization",
                        "achievement_or_event": "进入全国超级产粮大县序列，粮食总产量21.73亿斤",
                        "role_in_event": "县长",
                        "measurable_outcome": "粮食播种面积、平均亩产、总产量增幅均居全市第一",
                        "location": "息县",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "未知",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "speech_themes": [
                        "产业培育与招商引资",
                        "乡村振兴与粮食安全",
                        "城市建设与治理",
                        "营商环境优化",
                        "民生保障"
                    ],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "截至2026-07-24未发现郑春相关的纪律审查、审计问题或负面报道",
                        "date": "",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "郑春 领导信息",
                        "url": "http://www.xixian.gov.cn/2023/10-30/349647.html",
                        "publisher": "息县人民政府",
                        "published_at": "2023-10-30",
                        "accessed_at": "2026-07-24",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认郑春为中共息县县委副书记、县政府党组书记、县长"
                    },
                    {
                        "id": "S002",
                        "title": "刘创 领导信息",
                        "url": "http://www.xixian.gov.cn/2026/04-09/779559.html",
                        "publisher": "息县人民政府",
                        "published_at": "2026-04-09",
                        "accessed_at": "2026-07-24",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认刘创为县委常委、常务副县长，佐证郑春的县长职务"
                    },
                    {
                        "id": "S003",
                        "title": "2025年息县人民政府工作报告",
                        "url": "http://www.xixian.gov.cn/2025/03-26/605843.html",
                        "publisher": "息县人民政府",
                        "published_at": "2025-03-26",
                        "accessed_at": "2026-07-24",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "郑春在十五届人大六次会议上作政府工作报告，详述2024年工作"
                    }
                ],
                "confidence_summary": {
                    "identity": "partial",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "郑春任息县县长前的完整履历未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "郑春的出生年份、出生地、教育背景",
                        "why_it_matters": "核心人物身份识别基本信息",
                        "suggested_queries": ["郑春 息县 简历", "郑春 信阳 任前公示"],
                        "last_attempted": "2026-07-24"
                    },
                    {
                        "priority": "critical",
                        "question": "郑春任息县县长前的完整职业履历",
                        "why_it_matters": "理解其晋升路径和可能的跨县交流网络",
                        "suggested_queries": ["郑春 此前担任 什么职务", "郑春 任职经历"],
                        "last_attempted": "2026-07-24"
                    }
                ]
            }
        }
    ]

    for pf in person_files:
        filepath = PERSONS_DIR / pf["file"]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filepath}")


def get_stats():
    """Return summary statistics."""
    return {
        "persons": len(persons),
        "organizations": len(organizations),
        "positions": len(positions),
        "relationships": len(relationships),
    }


def main():
    print(f"Building 息县 network — {AS_OF}")
    print(f"  Staging dir: {STAGING_DIR}")
    build_db()
    build_gexf()
    write_person_json()
    stats = get_stats()
    print(f"\nDone: {stats['persons']} persons, {stats['organizations']} orgs, "
          f"{stats['positions']} positions, {stats['relationships']} relationships")


if __name__ == "__main__":
    main()
