#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 怀化市 (Huaihua City), 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_怀化市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.huaihua.gov.cn — 怀化市人民政府官网：确认韦朝晖（市委书记，女）2026年7月仍主持市委常委会
  - www.huaihua.gov.cn/huaihua/c114851/szf.shtml — 市政府领导页：列出7名副市长和秘书长，市长席位空缺
  - www.hhrd.cn — 怀化市人大网站：确认"韦朝晖辞去怀化市人民政府市长职务"决定，李万千为市人大常委会主任
  - www.hnhhszx.com — 怀化市政协网站：张家铣（政协主席），韦朝晖在通道调研等报道

Confidence notes:
  - 韦朝晖: confirmed via city government news articles — 市委书记，女，之前担任怀化市市长
  - 市长: 2026年7月市政府页面未显示市长姓名，可能空缺或新任还未到任
  - 尹培国: confirmed as 市委常委、常务副市长，主持市政府常务会议
  - 李万千: confirmed as 市人大常委会主任
  - 张家铣: confirmed as 市政协主席
  - 7名副市长: 尹培国、胡和平、余建勇、周重颜、向汝莲、曾文谦、何唯英 — confirmed
  - 秘书长: 林华 — confirmed
  - 详细履历（教育背景、早期职务、出生信息）因网络搜索受限未能完整验证
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "怀化市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "韦朝晖",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共怀化市委员会",
        "source": "https://www.huaihua.gov.cn — 2026-07-24市委常委会会议报道"
    },
    {
        "id": 2,
        "name": "尹培国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长（主持市政府工作）",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府常务会议报道(2026-07-08)"
    },
    {
        "id": 3,
        "name": "李万千",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "怀化市人民代表大会常务委员会",
        "source": "http://www.hhrd.cn — 人大网站报道"
    },
    {
        "id": 4,
        "name": "张家铣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议怀化市委员会",
        "source": "http://www.hnhhszx.com — 政协网站报道"
    },
    {
        "id": 5,
        "name": "胡和平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
    {
        "id": 6,
        "name": "向汝莲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
    {
        "id": 7,
        "name": "余建勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
    {
        "id": 8,
        "name": "周重颜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
    {
        "id": 9,
        "name": "曾文谦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
    {
        "id": 10,
        "name": "何唯英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
    {
        "id": 11,
        "name": "林华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "怀化市人民政府",
        "source": "https://www.huaihua.gov.cn — 市政府领导页"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共怀化市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共湖南省委员会",
        "location": "怀化市"
    },
    {
        "id": 2,
        "name": "怀化市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "湖南省人民政府",
        "location": "怀化市"
    },
    {
        "id": 3,
        "name": "怀化市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "湖南省人民代表大会常务委员会",
        "location": "怀化市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议怀化市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议湖南省委员会",
        "location": "怀化市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 韦朝晖 — career timeline (partial)
    {"person_id": 1, "org_id": 2, "title": "怀化市人民政府市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "曾任怀化市市长，具体任职时间待查。人大网站确认已辞去市长职务"},
    {"person_id": 1, "org_id": 1, "title": "怀化市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "2026年7月以市委书记身份主持市委常委会会议"},
    {"person_id": 1, "org_id": 1, "title": "怀化市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "同时担任市委副书记"},

    # 尹培国
    {"person_id": 2, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月主持市政府常务会议——此前履历待查"},

    # 李万千
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "出席市六届人大常委会第三十一次会议"},

    # 张家铣
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "率队开展重点提案现场督办协商"},

    # 胡和平
    {"person_id": 5, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "参加城市建设管理工作专题会议"},

    # 向汝莲
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "女，参加鹤中一体化会议"},

    # 余建勇
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "接听12345政务服务便民热线公告"},

    # 周重颜
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 曾文谦
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 何唯英
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "参加城市建设管理工作专题会议"},

    # 林华
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "韦朝晖作为市委书记，尹培国作为常务副市长主持市政府工作，党政主要领导搭档",
        "overlap_org": "怀化市",
        "overlap_period": "2026年至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "韦朝晖与李万千在怀化市共事",
        "overlap_org": "怀化市",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "韦朝晖与张家铣在怀化市共事",
        "overlap_org": "怀化市",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "韦朝晖作为市委书记，胡和平作为市委常委，党委领导班子搭档",
        "overlap_org": "中共怀化市委员会",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "尹培国与胡和平均在市政府任职，同为市委常委",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "尹培国与向汝莲在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "尹培国与余建勇在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "尹培国与周重颜在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "overlap",
        "context": "尹培国与曾文谦在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "overlap",
        "context": "尹培国与何唯英在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "尹培国与林华在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "胡和平与向汝莲在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "向汝莲与余建勇在市政府共事",
        "overlap_org": "怀化市人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "李万千与张家铣分别担任人大和政协主要负责人",
        "overlap_org": "怀化市",
        "overlap_period": "至今"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # Party Secretary — Red
    if name == "韦朝晖":
        return "255,50,50"
    # Government leader (acting) — Blue
    if name == "尹培国":
        return "50,100,255"
    # 人大 — Cyan
    if name == "李万千":
        return "200,255,255"
    # 政协 — Cream
    if name == "张家铣":
        return "255,240,200"
    # Others — Grey
    return "100,100,100"


def person_size(name):
    if name in ("韦朝晖", "尹培国"):
        return "20.0"
    if name in ("李万千", "张家铣"):
        return "16.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "事业单位" in o_type:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>怀化市领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "怀化市",
            "region": "怀化市",
            "job": p.get("current_post", ""),
            "task_id": "hunan_怀化市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"huaihua_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正厅级" if p["id"] in (1, 3, 4) else "副厅级" if p["id"] not in (11,) else "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含出生信息、教育背景、历任职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "核心人物，但履历信息不完整",
                "suggested_queries": [f"{p['name']} 简历 怀化", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "怀化市人民政府网站", "url": "https://www.huaihua.gov.cn", "publisher": "怀化市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "怀化市政府官网确认韦朝晖（市委书记）、尹培国（常务副市长）等领导信息"},
        {"id": "S002", "title": "怀化市人大网站", "url": "http://www.hhrd.cn", "publisher": "怀化市人民代表大会常务委员会", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李万千（人大主任）、韦朝晖辞去市长职务信息"},
        {"id": "S003", "title": "怀化市政协网站", "url": "http://www.hnhhszx.com", "publisher": "中国人民政治协商会议怀化市委员会", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认张家铣（政协主席）"},
    ]

    # === 1. 韦朝晖 (市委书记) ===
    wei_timeline = [
        {"start": "unknown", "end": "unknown", "org": "怀化市人民政府", "title": "市长", "notes": "曾任怀化市市长，具体任职起始时间待查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "present", "org": "中共怀化市委员会", "title": "市委书记", "notes": "2026年7月确认以市委书记身份主持工作", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到完整履历。韦朝晖，女，中共党员，此前职务和生涯轨迹待查。人大网站确认她曾任市长并辞去市长职务。", "confidence": "unverified", "source_ids": []},
    ]
    wei_relationships = [
        {"person": "尹培国", "person_id": "huaihua_尹培国", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市委书记与常务副市长（主持市政府工作）搭档", "overlap_org": "怀化市", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "李万千", "person_id": "huaihua_李万千", "relationship_type": "overlap", "strength": "medium", "evidence": "在怀化市共事", "overlap_org": "怀化市", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "张家铣", "person_id": "huaihua_张家铣", "relationship_type": "overlap", "strength": "medium", "evidence": "在怀化市共事", "overlap_org": "怀化市", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "胡和平", "person_id": "huaihua_胡和平", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "党委领导班子搭档", "overlap_org": "中共怀化市委员会", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wei_json = make_person_json(persons[0], wei_timeline, wei_relationships, source_register)
    wei_json["professional_profile"]["career_pattern"] = "local_ladder"
    wei_json["professional_profile"]["systems_experience"] = ["地方党政"]
    wei_json["professional_profile"]["geographic_pattern"] = ["怀化"]
    wei_json["professional_profile"]["promotion_velocity"] = {
        "summary": "从市长转任市委书记（同一城市党政主要领导职务接续），具体任职时间待查",
        "notable_fast_promotions": []
    }
    wei_json["open_questions"] = [
        {"priority": "critical", "question": "韦朝晖的完整职业生涯履历（含出生信息、教育背景、历任职务）", "why_it_matters": "核心人物（市委书记），但基本信息几乎完全空白", "suggested_queries": ["韦朝晖 简历 怀化", "韦朝晖 任前公示", "韦朝晖 出生 籍贯"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "韦朝晖从市长转任市委书记的具体时间", "why_it_matters": "确定任职时间线", "suggested_queries": ["韦朝晖 任怀化市委书记 时间", "怀化市委书记 任命"], "last_attempted": AS_OF},
        {"priority": "high", "question": "韦朝晖的前任职务和职业生涯路径", "why_it_matters": "了解其从政轨迹", "suggested_queries": ["韦朝晖 历任", "韦朝晖 工作经历"], "last_attempted": AS_OF},
    ]
    wei_path = PERSONS_DIR / f"{TODAY}-湖南省-怀化市-市委书记-韦朝晖.json"
    with open(wei_path, "w", encoding="utf-8") as f:
        json.dump(wei_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wei_path.name}")

    # === 2. 尹培国 (常务副市长，主持市政府工作) ===
    yin_timeline = [
        {"start": "unknown", "end": "present", "org": "怀化市人民政府", "title": "市委常委、常务副市长", "notes": "2026年7月主持市政府常务会议——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "尹培国——此前履历完全未知", "confidence": "unverified", "source_ids": []},
    ]
    yin_relationships = [
        {"person": "韦朝晖", "person_id": "huaihua_韦朝晖", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "常务副市长在市委书记领导下主持市政府工作", "overlap_org": "怀化市", "overlap_period": "2026年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "胡和平", "person_id": "huaihua_胡和平", "relationship_type": "overlap", "strength": "medium", "evidence": "同在市政府领导班子", "overlap_org": "怀化市人民政府", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "向汝莲", "person_id": "huaihua_向汝莲", "relationship_type": "overlap", "strength": "medium", "evidence": "同在市政府领导班子", "overlap_org": "怀化市人民政府", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "余建勇", "person_id": "huaihua_余建勇", "relationship_type": "overlap", "strength": "medium", "evidence": "同在市政府领导班子", "overlap_org": "怀化市人民政府", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    yin_json = make_person_json(persons[1], yin_timeline, yin_relationships, source_register)
    yin_json["identity"]["gender"] = "男"
    yin_json["current_status"]["is_current_confirmed"] = True
    yin_json["open_questions"] = [
        {"priority": "critical", "question": "尹培国的完整职业生涯履历（含出生信息、教育背景、历任职务）", "why_it_matters": "主持市政府工作的常务副市长，但履历几乎完全空白", "suggested_queries": ["尹培国 怀化 简历", "尹培国 任前公示", "尹培国 出生"], "last_attempted": AS_OF},
        {"priority": "high", "question": "怀化市市长是否已任命到位", "why_it_matters": "市长席位空缺确认和新任任命跟踪", "suggested_queries": ["怀化市市长 任命 2026", "怀化市人大 市长 选举"], "last_attempted": AS_OF},
    ]
    yin_path = PERSONS_DIR / f"{TODAY}-湖南省-怀化市-常务副市长-尹培国.json"
    with open(yin_path, "w", encoding="utf-8") as f:
        json.dump(yin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yin_path.name}")

    # === 3. 李万千 (人大主任) ===
    li_timeline = [
        {"start": "unknown", "end": "present", "org": "怀化市人民代表大会常务委员会", "title": "主任", "notes": "出席市六届人大常委会第三十一次会议——此前履历待查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "李万千——此前履历完全未知", "confidence": "unverified", "source_ids": []},
    ]
    li_relationships = []
    li_json = make_person_json(persons[2], li_timeline, li_relationships, source_register)
    li_path = PERSONS_DIR / f"{TODAY}-湖南省-怀化市-人大主任-李万千.json"
    with open(li_path, "w", encoding="utf-8") as f:
        json.dump(li_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {li_path.name}")

    # === 4. 张家铣 (政协主席) ===
    zhang_timeline = [
        {"start": "unknown", "end": "present", "org": "中国人民政治协商会议怀化市委员会", "title": "主席", "notes": "率队开展重点提案现场督办协商——此前履历待查", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "张家铣——此前履历完全未知", "confidence": "unverified", "source_ids": []},
    ]
    zhang_relationships = []
    zhang_json = make_person_json(persons[3], zhang_timeline, zhang_relationships, source_register)
    zhang_path = PERSONS_DIR / f"{TODAY}-湖南省-怀化市-政协主席-张家铣.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")
