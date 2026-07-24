#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 召陵区 leadership network.

调查日期: 2026-07-24
信息来源: 召陵区人民政府网站 (lhsl.gov.cn), 漯河市人民政府网站 (luohe.gov.cn)
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "召陵区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "召陵区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省漯河市召陵区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════

    # 王中伟 — 区委书记（2026年六届区委产生）
    {
        "id": 1,
        "name": "王中伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共漯河市召陵区委书记",
        "current_org": "中共漯河市召陵区委员会",
        "source": "https://www.lhsl.gov.cn/xwzx2/zlyw1/content_1058995 (2026-07-24)",
    },
    # 李景超 — 区委副书记、区长
    {
        "id": 2,
        "name": "李景超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区委副书记、区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.lhsl.gov.cn/zwgk/fdzdgknr/ldzc/ (2026-07-24)",
    },
    # 白羽 — 区委副书记、政法委书记
    {
        "id": 3,
        "name": "白羽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区委副书记、政法委书记",
        "current_org": "中共漯河市召陵区委员会",
        "source": "https://www.lhsl.gov.cn/xwzx2/zlyw1/content_1058282 (2026-07-17)",
    },

    # ═══════════════════════════════
    # 区政府领导
    # ═══════════════════════════════
    # 王智扬 — 区政府副区长
    {
        "id": 4,
        "name": "王智扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.luohe.gov.cn/jrlh/xqdt/content_1058732 (2026-07-22)",
    },
    # 鲁俊涛 — 区政府副区长
    {
        "id": 5,
        "name": "鲁俊涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.luohe.gov.cn/jrlh/xqdt/content_1058732 (2026-07-22)",
    },
    # 王玉峰 — 区政府副区长
    {
        "id": 6,
        "name": "王玉峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.luohe.gov.cn/jrlh/xqdt/content_1058732 (2026-07-22)",
    },
    # 陈勇 — 区政府党组成员、副区长，市公安局召陵分局局长
    {
        "id": 7,
        "name": "陈勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长、公安分局局长",
        "current_org": "召陵区人民政府",
        "source": "https://www.lhsl.gov.cn/zwgk/fdzdgknr/ldzc/ (2026-07-24)",
    },
    # 黄海霞 — 区政府党组成员、副区长
    {
        "id": 8,
        "name": "黄海霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.lhsl.gov.cn/zwgk/fdzdgknr/ldzc/ (2026-07-24)",
    },
    # 李云超 — 区政府党组成员、副区长
    {
        "id": 9,
        "name": "李云超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.lhsl.gov.cn/zwgk/fdzdgknr/ldzc/ (2026-07-24)",
    },
    # 廉鹏 — 区政府副区长
    {
        "id": 10,
        "name": "廉鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区副区长",
        "current_org": "召陵区人民政府",
        "source": "https://www.luohe.gov.cn/jrlh/xqdt/content_1058732 (2026-07-22)",
    },
    # 陈新阳 — 区领导（具体职务待确认）
    {
        "id": 11,
        "name": "陈新阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "召陵区区领导",
        "current_org": "召陵区人民政府",
        "source": "https://www.lhsl.gov.cn/xwzx2/zlyw1/content_1058995 (2026-07-24)",
    },

    # ═══════════════════════════════
    # 前任领导
    # ═══════════════════════════════
    # 王奇山 — 前任召陵区委书记（升任漯河市副市长）
    {
        "id": 12,
        "name": "王奇山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "漯河市副市长（原召陵区委书记）",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/fdzdgknr1/ldzc1 (2026-07-24)",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共漯河市召陵区委员会", "type": "党委", "level": "县处级",
     "parent": "中共漯河市委员会", "location": "河南省漯河市召陵区"},
    {"id": 2, "name": "召陵区人民政府", "type": "政府", "level": "县处级",
     "parent": "漯河市人民政府", "location": "河南省漯河市召陵区"},
    {"id": 3, "name": "漯河市人民政府", "type": "政府", "level": "地厅级",
     "parent": "河南省人民政府", "location": "河南省漯河市"},
    {"id": 4, "name": "中共漯河市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共河南省委员会", "location": "河南省漯河市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────
positions = [
    # 王中伟
    {"person_id": 1, "org_id": 1, "title": "中共漯河市召陵区委书记",
     "start": "2026", "end": "present", "rank": "县处级正职",
     "note": "2026年召陵区第六届区委产生"},
    # 李景超
    {"person_id": 2, "org_id": 1, "title": "召陵区委副书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "一级调研员"},
    {"person_id": 2, "org_id": 2, "title": "召陵区区长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "区政府党组书记"},
    # 白羽
    {"person_id": 3, "org_id": 1, "title": "召陵区委副书记、政法委书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # 王智扬
    {"person_id": 4, "org_id": 2, "title": "召陵区副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # 鲁俊涛
    {"person_id": 5, "org_id": 2, "title": "召陵区副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # 王玉峰
    {"person_id": 6, "org_id": 2, "title": "召陵区副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # 陈勇
    {"person_id": 7, "org_id": 2, "title": "召陵区副区长、公安分局局长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "二级高级警长"},
    # 黄海霞
    {"person_id": 8, "org_id": 2, "title": "召陵区副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责农业农村等领域"},
    # 李云超
    {"person_id": 9, "org_id": 2, "title": "召陵区副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责民政、教育、文旅等领域"},
    # 廉鹏
    {"person_id": 10, "org_id": 2, "title": "召陵区副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # 陈新阳
    {"person_id": 11, "org_id": 2, "title": "召陵区区领导",
     "start": "", "end": "present", "rank": "",
     "note": "具体职务待确认"},
    # 王奇山（前任）
    {"person_id": 12, "org_id": 1, "title": "中共漯河市召陵区委书记（前任）",
     "start": "", "end": "2025/2026", "rank": "县处级正职",
     "note": "后升任漯河市副市长"},
    {"person_id": 12, "org_id": 3, "title": "漯河市副市长",
     "start": "", "end": "present", "rank": "地厅级副职",
     "note": ""},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "王中伟（区委书记）与李景超（区长）为召陵区党政主要领导搭档",
     "overlap_org": "中共漯河市召陵区委员会、召陵区人民政府",
     "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委常委会共同成员",
     "overlap_org": "中共漯河市召陵区委员会",
     "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "王中伟为区委书记，白羽为区委副书记",
     "overlap_org": "中共漯河市召陵区委员会",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "同为区委副书记，区长与政法委书记",
     "overlap_org": "中共漯河市召陵区委员会",
     "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor",
     "context": "王中伟接替王奇山担任召陵区委书记；王奇山升任漯河市副市长",
     "overlap_org": "中共漯河市召陵区委员会",
     "overlap_period": "2025/2026"},
]

# ── HELPER FUNCTIONS ──────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for a person node based on role."""
    post = p.get("current_post", "")
    if "区委书记" in post or "县委书记" in post:
        return "255,50,50"
    if "区长" in post or "县长" in post or "市长" in post:
        return "50,100,255"
    if "副书记" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "区委书记" in post or "区长" in post

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


# ── BUILD DATABASE ─────────────────────────────────────────────────
def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT
        )
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"],
                     p["birth"], p["birthplace"], p["education"],
                     p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>召陵区领导关系网络 - {SLUG}</description>')
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
    edge_id = 0

    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p.get("current_post", "")
        org = p.get("current_org", "")
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"]
        name = o["name"]
        t = o.get("type", "")
        c = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(t)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: positions (person -> org)
    lines.append('    <edges>')
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos.get("title", "")
        lines.append(f'      <edge id="e{edge_id}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="曾任/现任该职务"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    # Edges: relationships (person <-> person)
    for r in relationships:
        a = r["person_a"]
        b = r["person_b"]
        rtype = r.get("type", "")
        ctx = r.get("context", "")
        lines.append(f'      <edge id="e{edge_id}" source="p{a}" target="p{b}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# ── PERSON JSON ────────────────────────────────────────────────────
def write_person_json(person, slug_override=None):
    """Write a per-person graph JSON file."""
    name = person["name"]
    post_key = person["current_post"].replace("中共", "").strip()
    # Build a short job title
    if "区委书记" in person["current_post"]:
        job = "区委书记"
    elif "区长" in person["current_post"]:
        job = "区长"
    elif "副书记" in person["current_post"]:
        job = "区委副书记"
    else:
        job = post_key

    filename = f"{TODAY}-河南省-漯河市-{job}-{name}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    # Build relationship entries for this person
    person_relationships = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other_id = r["person_b"]
            other = next((p for p in persons if p["id"] == other_id), None)
            if other:
                person_relationships.append({
                    "person": other["name"],
                    "person_id": f"henan_luohe_shaoling_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("superior_subordinate", "predecessor_successor") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                })
        elif r["person_b"] == person["id"]:
            other_id = r["person_a"]
            other = next((p for p in persons if p["id"] == other_id), None)
            if other:
                person_relationships.append({
                    "person": other["name"],
                    "person_id": f"henan_luohe_shaoling_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("superior_subordinate", "predecessor_successor") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                })

    data = {
        "schema_version": "1.0",
        "generated_at": "2026-07-24",
        "investigation_scope": {
            "province": "河南省",
            "city": "漯河市",
            "region": "召陵区",
            "job": job,
            "task_id": "henan_召陵区",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"henan_luohe_shaoling_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": person.get("education", ""),
                "major": "",
                "degree": "大学" if person.get("education") == "大学" else "",
                "study_type": "unknown",
                "source_ids": ["S001"]
            }] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": "https://www.lhsl.gov.cn/zwgk/fdzdgknr/ldzc/"
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职" if is_top_leader(person) else "县处级副职",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": person_relationships,
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
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "召陵区人民政府 - 政府领导", "url": "https://www.lhsl.gov.cn/zwgk/fdzdgknr/ldzc/", "publisher": "召陵区人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "官方领导之窗页面"},
            {"id": "S002", "title": "漯河市人民政府 - 县区动态", "url": "https://www.luohe.gov.cn/jrlh/xqdt/", "publisher": "漯河市人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "市级政府新闻报道"}
        ],
        "confidence_summary": {
            "identity": "partial" if not person.get("birth") else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "早期履历完全缺失"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{name}的出生年份和籍贯", "why_it_matters": "核实身份和同乡关系的基础信息", "suggested_queries": [f"{name} 出生 {name} 籍贯"], "last_attempted": "2026-07-24"},
            {"priority": "high", "question": f"{name}的完整工作履历", "why_it_matters": "了解干部成长路径和系统经验", "suggested_queries": [f"{name} 简历 召陵区 {name} 工作经历"], "last_attempted": "2026-07-24"},
            {"priority": "high", "question": f"{name}的教育背景", "why_it_matters": "推断专业能力和分管理由", "suggested_queries": [f"{name} 毕业院校"], "last_attempted": "2026-07-24"},
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {filepath}")


# ── MAIN ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_db()
    build_gexf()
    # Write person JSON for the two core leaders
    for p in persons:
        if p["id"] in (1, 2):  # 王中伟 and 李景超
            write_person_json(p)
    print("Done.")
