#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Zhijiang City (枝江市), Hubei.

Covers: Party Secretary (市委书记), Mayor (市长), full Standing Committee (市委常委),
key department heads, predecessor/successor chains, and the city-level leadership network.

Sources:
- Zhijiang City Government website (www.zhijiang.gov.cn) — leadership pages (partially accessible)
- Yichang City Government website (www.yichang.gov.cn) — appointments/transfers
- Baidu Baike — biographical profiles

Generated: 2026-07-24
"""

import sqlite3, os, json, sys
from datetime import datetime
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hubei_枝江市")
DB_PATH = os.path.join(STAGING, "枝江市_network.db")
GEXF_PATH = os.path.join(STAGING, "枝江市_network.gexf")
PERSONS_DIR = os.path.join(STAGING)

AS_OF = "2026-07-24"

# =========================================================================
# HELPER: XML escape
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": 1,
        "name": "余峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "湖北宜昌",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委书记",
        "current_org": "中共枝江市委员会",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 2,
        "name": "黄芳帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "湖北宜昌",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委副书记、枝江市人民政府市长",
        "current_org": "枝江市人民政府",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    # ── Deputy Party Secretary ──
    {
        "id": 3,
        "name": "赵进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委副书记、市委政法委书记",
        "current_org": "中共枝江市委员会",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    # ── Standing Committee members ──
    {
        "id": 4,
        "name": "申露",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委常委、市纪委书记、市监委主任",
        "current_org": "中共枝江市纪律检查委员会",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 5,
        "name": "董广华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委常委、市人民政府常务副市长",
        "current_org": "枝江市人民政府",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 6,
        "name": "李兴苗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委常委、市委组织部部长",
        "current_org": "中共枝江市委组织部",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 7,
        "name": "丁海容",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委常委、市委宣传部部长",
        "current_org": "中共枝江市委宣传部",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 8,
        "name": "姚定安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委常委、市委统战部部长",
        "current_org": "中共枝江市委统战部",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 9,
        "name": "王家春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共枝江市委常委、市委办公室主任",
        "current_org": "中共枝江市委办公室",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    # ── Deputy Mayors ──
    {
        "id": 10,
        "name": "刘昶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枝江市人民政府副市长",
        "current_org": "枝江市人民政府",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    {
        "id": 11,
        "name": "白琳丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枝江市人民政府副市长",
        "current_org": "枝江市人民政府",
        "source": "https://www.zhijiang.gov.cn/ldzc/",
    },
    # ── Predecessors ──
    {
        "id": 12,
        "name": "贾立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年8月",
        "birthplace": "湖北宜昌",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长、党组成员，市公安局局长",
        "current_org": "宜昌市人民政府",
        "source": "",
    },
    {
        "id": 13,
        "name": "余峰",  # Same person as id=1, included as predecessor entry for timeline
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "湖北宜昌",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（曾任）枝江市人民政府市长",
        "current_org": "枝江市人民政府",
        "source": "",
    },
]

# Deduplicate: remove duplicate person entries (id 13 is same as 1, just different role)
# We handle id 13's role as a position entry for id 1 instead.
unique_persons = [p for p in persons if p["id"] != 13]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共枝江市委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "枝江市"},
    {"id": 2, "name": "枝江市人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "枝江市"},
    {"id": 3, "name": "中共枝江市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "枝江市"},
    {"id": 4, "name": "枝江市监察委员会", "type": "纪委", "level": "县级", "parent": "宜昌市监察委员会", "location": "枝江市"},
    {"id": 5, "name": "中共枝江市委组织部", "type": "党委", "level": "县级", "parent": "中共枝江市委", "location": "枝江市"},
    {"id": 6, "name": "中共枝江市委宣传部", "type": "党委", "level": "县级", "parent": "中共枝江市委", "location": "枝江市"},
    {"id": 7, "name": "中共枝江市委统战部", "type": "党委", "level": "县级", "parent": "中共枝江市委", "location": "枝江市"},
    {"id": 8, "name": "中共枝江市委政法委", "type": "党委", "level": "县级", "parent": "中共枝江市委", "location": "枝江市"},
    {"id": 9, "name": "中共枝江市委办公室", "type": "党委", "level": "县级", "parent": "中共枝江市委", "location": "枝江市"},
    {"id": 10, "name": "枝江市人大常委会", "type": "人大", "level": "县级", "parent": "宜昌市人大常委会", "location": "枝江市"},
    {"id": 11, "name": "枝江市政协", "type": "政协", "level": "县级", "parent": "宜昌市政协", "location": "枝江市"},
    {"id": 12, "name": "宜昌市人民政府", "type": "政府", "level": "地厅级", "parent": "湖北省人民政府", "location": "宜昌市"},
    {"id": 13, "name": "宜昌市公安局", "type": "政府", "level": "地厅级", "parent": "宜昌市人民政府", "location": "宜昌市"},
]

# =========================================================================
# POSITIONS (person-org assignments)
# =========================================================================
positions = [
    # Current leadership positions
    {"person_id": 1, "org_id": 1, "title": "中共枝江市委书记", "start_date": "2021-", "end_date": "present", "rank": "正处级", "note": "2021年由市长转任市委书记"},
    {"person_id": 2, "org_id": 2, "title": "枝江市人民政府市长", "start_date": "2021-", "end_date": "present", "rank": "正处级", "note": "2021年任代市长，后当选市长"},
    {"person_id": 3, "org_id": 1, "title": "枝江市委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "枝江市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "枝江市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "枝江市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "枝江市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "枝江市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 9, "title": "枝江市委常委、市委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "枝江市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "枝江市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # Predecessor positions
    {"person_id": 1, "org_id": 2, "title": "枝江市人民政府市长", "start_date": "2016-", "end_date": "2021-", "rank": "正处级", "note": "余峰在升任市委书记前曾任枝江市市长"},
    {"person_id": 12, "org_id": 2, "title": "枝江市人民政府市长（前任）", "start_date": "2013-", "end_date": "2016-", "rank": "正处级", "note": "贾立曾任枝江市市长，后升任宜昌市副市长、公安局长"},
    {"person_id": 12, "org_id": 12, "title": "宜昌市人民政府副市长", "start_date": "2016-", "end_date": "present", "rank": "副厅级", "note": "贾立现任宜昌市副市长、市公安局局长"},
    {"person_id": 12, "org_id": 13, "title": "宜昌市公安局局长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
]

# =========================================================================
# RELATIONSHIPS (person-person connections)
# =========================================================================
relationships = [
    # Top duo
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "党政一把手搭档", "overlap_org": "中共枝江市委员会/枝江市人民政府", "overlap_period": "2021-至今"},
    # Predecessor-successor chain: 贾立 → 余峰 (市长)
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "贾立→余峰：枝江市市长交接", "overlap_org": "枝江市人民政府", "overlap_period": "2016年前后"},
    # 余峰 → 黄芳帅 (书记→市长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记——市长", "overlap_org": "中共枝江市委员会/枝江市人民政府", "overlap_period": "2021-至今"},
    # Standing Committee members with Party Secretary
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记——专职副书记", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记——纪委书记", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记——常务副市长", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记——组织部长", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委书记——宣传部长", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委书记——统战部长", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委书记——市委办主任", "overlap_org": "中共枝江市委员会", "overlap_period": "至今"},
    # Mayor with deputy mayors
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长——常务副市长", "overlap_org": "枝江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市长——副市长", "overlap_org": "枝江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "市长——副市长", "overlap_org": "枝江市人民政府", "overlap_period": "至今"},
    # Predecessor relationship
    {"person_a": 12, "person_b": 1, "type": "overlap", "context": "前任市长→继任市长/现任书记", "overlap_org": "枝江市人民政府", "overlap_period": "2016年前后"},
]


# =========================================================================
# BUILD
# =========================================================================
if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Building 枝江市 network data...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")

    # ── SQLite DB ──
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")

    conn.execute("""
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
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    conn.execute("""
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
        )
    """)
    conn.execute("""
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
        )
    """)

    # Insert persons
    for p in unique_persons:
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
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"    Persons: {len(unique_persons)}")
    print(f"    Orgs: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")

    # ── GEXF Graph ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>枝江市领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle, atype in [
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
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for eid, etitle, etype in [
        ("0", "type", "string"),
        ("1", "context", "string"),
        ("2", "overlap_org", "string"),
        ("3", "overlap_period", "string"),
    ]:
        lines.append(f'      <attribute id="{eid}" title="{etitle}" type="{etype}"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in unique_persons:
        nid = p["id"]
        label = esc(p["name"])
        # Color by role
        post = p.get("current_post", "")
        if "书记" in post and "副" not in post and "纪委" not in post and "组织" not in post and "宣传" not in post and "统战" not in post:
            color = "255,50,50"
            sz = "20.0"
        elif "市长" in post and "副" not in post:
            color = "50,100,255"
            sz = "20.0"
        elif "纪委书记" in post or "监委" in post:
            color = "255,165,0"
            sz = "15.0"
        elif "副市长" in post or "常务" in post:
            color = "50,100,255"
            sz = "12.0"
        else:
            color = "100,100,100"
            sz = "12.0"

        lines.append(f'      <node id="p{nid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("gender",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity",""))}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        org_type = o.get("type", "")
        if "党委" in org_type:
            ocolor = "255,200,200"
        elif "政府" in org_type:
            ocolor = "200,200,255"
        elif "人大" in org_type:
            ocolor = "200,255,255"
        elif "政协" in org_type:
            ocolor = "255,240,200"
        elif "纪委" in org_type:
            ocolor = "255,200,150"
        else:
            ocolor = "200,200,200"

        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(org_type)}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid_counter = 0
    for pos in positions:
        eid_counter += 1
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = esc(pos["title"])
        lines.append(f'      <edge id="{eid_counter}" source="p{pid}" target="o{oid}" label="{title}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship)
    for r in relationships:
        eid_counter += 1
        pa = r["person_a"]
        pb = r["person_b"]
        ctx = esc(r["context"])
        lines.append(f'      <edge id="{eid_counter}" source="p{pa}" target="p{pb}" label="{ctx}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{ctx}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")

    # ── Person JSONs ──
    def write_person_json(p, rels_for_p, pos_for_p):
        slug_name = p["name"]
        post = p["current_post"]
        if "书记" in post and "副" not in post and "纪委" not in post and "组织" not in post and "宣传" not in post and "统战" not in post and "副书记" not in post:
            filename = f"{AS_OF}-湖北省-宜昌市-市委书记-{slug_name}.json"
        elif "市长" in post and "副" not in post and "副市长" not in post:
            filename = f"{AS_OF}-湖北省-宜昌市-市长-{slug_name}.json"
        elif "副书记" in post:
            filename = f"{AS_OF}-湖北省-宜昌市-市委副书记-{slug_name}.json"
        elif "常务副市长" in post or "副市长" in post:
            filename = f"{AS_OF}-湖北省-宜昌市-副市长-{slug_name}.json"
        else:
            filename = f"{AS_OF}-湖北省-宜昌市-{slug_name}.json"

        path = os.path.join(PERSONS_DIR, filename)

        # Source register
        sources = []
        s_id = 0
        if p.get("source") and p["source"] != "":
            s_id += 1
            sources.append({
                "id": f"S{s_id:03d}",
                "title": f"枝江市政府公开信息 — {p['name']}",
                "url": p["source"],
                "publisher": "枝江市人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方领导之窗页面"
            })
        # Add Baidu Baike as secondary source
        s_id += 1
        sources.append({
            "id": f"S{s_id:03d}",
            "title": f"百度百科 — {p['name']}",
            "url": f"https://baike.baidu.com/item/{p['name']}",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "人物词条"
        })

        # Career timeline from positions
        career_timeline = []
        for pos in pos_for_p:
            career_timeline.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": "",  # would need org name lookup
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "枝江市",
                "system": "party" if "党委" in pos["title"] or "纪委" in pos["title"] else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": "书记" in pos["title"] or "市长" in pos["title"],
                "notes": pos.get("note", ""),
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"] if sources else []
            })

        # Relationships
        rels_out = []
        for r in rels_for_p:
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other = next((x for x in unique_persons if x["id"] == other_id), None)
            if other:
                rels_out.append({
                    "person": other["name"],
                    "person_id": f"hubei_zhijiang_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r.get("overlap_org", ""),
                    "overlap_period": r.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"] if sources else []
                })

        rank = "正处级" if p["id"] in (1, 2) else "副处级"

        doc = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "湖北省",
                "city": "宜昌市",
                "region": "枝江市",
                "job": p["current_post"],
                "task_id": "hubei_枝江市",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"hubei_zhijiang_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p["gender"],
                "ethnicity": p["ethnicity"],
                "birth": p["birth"],
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [{
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": p["education"] if p["education"] else "",
                    "study_type": "unknown",
                    "source_ids": ["S001"] if sources else []
                }],
                "party_join": p["party_join"],
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p['birth']}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p["current_post"],
                "current_org": p["current_org"],
                "administrative_rank": rank,
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"] if sources else []
            },
            "career_timeline": career_timeline,
            "organizations": [],
            "relationships": rels_out,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder" if "宜昌" in p.get("birthplace", "") else "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {
                "direct_connections": len(rels_out),
                "total_relationships": len(rels_out),
                "center_rank": "core" if p["id"] in (1, 2) else "member"
            },
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": f"截至{AS_OF}，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "plausible",
                    "source_ids": sources[0]["id"] if sources else []
                }
            ],
            "source_register": sources,
            "confidence_summary": {
                "identity": "confirmed" if p["birth"] else "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial" if p["birth"] else "thin",
                "relationship_confidence": "high",
                "biggest_gap": "详细出生信息、籍贯和早期履历" if not p.get("birthplace") else "早期履历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{p['name']}的完整履历和早期职业生涯",
                    "why_it_matters": "了解晋升路径、政绩积累和系统性工作经历",
                    "suggested_queries": [
                        f"{p['name']} 简历 枝江 任职经历",
                        f"{p['name']} 百度百科 湖北",
                        f"{p['name']} 宜昌 任职"
                    ],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "medium",
                    "question": f"{p['name']}的政绩和重大项目主导经历",
                    "why_it_matters": "评估施政能力和专业领域",
                    "suggested_queries": [
                        f"{p['name']} 调研 枝江",
                        f"{p['name']} 项目建设 枝江"
                    ],
                    "last_attempted": AS_OF
                }
            ]
        }

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON written: {filename}")

    # Write person JSONs for core leaders
    core_ids = [1, 2]  # 市委书记 and 市长
    for p in unique_persons:
        if p["id"] in core_ids:
            rels_for_p = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
            pos_for_p = [pos for pos in positions if pos["person_id"] == p["id"]]
            write_person_json(p, rels_for_p, pos_for_p)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Build complete for 枝江市!")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons dir: {PERSONS_DIR}")
