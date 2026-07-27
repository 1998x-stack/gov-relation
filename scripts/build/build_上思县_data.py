#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Shangsi County leadership network.

上思县 — 广西壮族自治区防城港市辖县

Targets: 县委书记, 县长
Research date: 2026-07-23
Web access: partially degraded (Exa rate-limited, Baidu 403, shangsi.gov.cn accessible but leadership page not found)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(BASE)
DB_PATH = os.path.join(TMP, "上思县_network.db")
GEXF_PATH = os.path.join(TMP, "上思县_network.gexf")
PERSONS_DIR = os.path.join(TMP)

AS_OF = "2026-07-23"

# ── Helper ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def make_person_json(person, timeline, relationships, source_register):
    """Build a person graph JSON following person_graph_json.md schema."""
    identity = {
        "person_id": f"shangsi_{person['name']}",
        "name": person["name"],
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("native_place", ""),
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{person['name']}_{person.get('birth','')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
            "official_profile_url": ""
        }
    }

    current_status = {
        "current_post": person.get("current_post", ""),
        "current_org": person.get("current_org", ""),
        "administrative_rank": "正处级",
        "as_of": AS_OF,
        "is_current_confirmed": person.get("current_confirmed", False),
        "source_ids": ["S001"]
    }

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "防城港市",
            "region": "上思县",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_上思县",
            "time_focus": "2020-2026"
        },
        "identity": identity,
        "current_status": current_status,
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {},
        "open_questions": []
    }


# ═══════════════════════════════════════════════════════════════════════
# DATA: Persons
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── ID 1: 戴兰华 — Current Party Secretary (县委书记) [plausible] ──
    {
        "id": 1, "name": "戴兰华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "上思县委书记", "current_org": "中共上思县委员会",
        "source": "http://www.shangsi.gov.cn/ (2026-07 news: 戴兰华调研督导文旅提质增效工作)",
        "current_confirmed": False,
    },
    # ── ID 2: [Unknown] — Current County Magistrate (县长) ──
    {
        "id": 2, "name": "（待查）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "上思县长", "current_org": "上思县人民政府",
        "source": "",
        "current_confirmed": False,
    },
    # ── ID 3: 黎家迎 — Former Party Secretary → 防城港市委常委/统战部长 ──
    {
        "id": 3, "name": "黎家迎", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "防城港市委常委、统战部部长", "current_org": "中共防城港市委员会",
        "source": "report/20260723-防城港市-跨市干部交流网络调查报告.md",
        "current_confirmed": True,
    },
    # ── ID 4: [Name Unknown] — Predecessor of 黎家迎 ──
    {
        "id": 4, "name": "（前任待查）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "", "current_org": "",
        "source": "",
        "current_confirmed": False,
    },
]

# ═══════════════════════════════════════════════════════════════════════
# DATA: Organizations
# ═══════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共上思县委员会", "type": "党委", "level": "县处级", "parent": "中共防城港市委员会", "location": "广西防城港市上思县"},
    {"id": 2, "name": "上思县人民政府", "type": "政府", "level": "县处级", "parent": "防城港市人民政府", "location": "广西防城港市上思县"},
    {"id": 3, "name": "上思县人大常委会", "type": "人大", "level": "县处级", "parent": "防城港市人大常委会", "location": "广西防城港市上思县"},
    {"id": 4, "name": "上思县政协", "type": "政协", "level": "县处级", "parent": "防城港市政协", "location": "广西防城港市上思县"},
    {"id": 5, "name": "上思县纪委监委", "type": "纪委", "level": "县处级", "parent": "防城港市纪委监委", "location": "广西防城港市上思县"},
    {"id": 6, "name": "中共防城港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西防城港市"},
    {"id": 7, "name": "思阳镇", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县思阳镇"},
    {"id": 8, "name": "叫安镇", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县叫安镇"},
    {"id": 9, "name": "在妙镇", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县在妙镇"},
    {"id": 10, "name": "华兰镇", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县华兰镇"},
    {"id": 11, "name": "南屏瑶族乡", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县南屏瑶族乡"},
    {"id": 12, "name": "那琴乡", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县那琴乡"},
    {"id": 13, "name": "公正乡", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县公正乡"},
    {"id": 14, "name": "平福乡", "type": "乡镇/街道", "level": "乡科级", "parent": "上思县", "location": "上思县平福乡"},
]

# ═══════════════════════════════════════════════════════════════════════
# DATA: Positions
# ═══════════════════════════════════════════════════════════════════════

positions = [
    # 戴兰华 — 县委书记 (plausible)
    {"person_id": 1, "org_id": 1, "title": "上思县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "2026年7月以县委书记身份公开活动（调研文旅提质增效工作）"},
    # 未知名县长
    {"person_id": 2, "org_id": 2, "title": "上思县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "姓名待查；公开资料未找到县长任职信息"},
    # 黎家迎 — 前县委书记
    {"person_id": 3, "org_id": 1, "title": "上思县委书记",
     "start_date": "", "end_date": "约2019", "rank": "正处级",
     "note": "任上思县委书记后晋升防城港市委常委/统战部长"},
    {"person_id": 3, "org_id": 6, "title": "防城港市委常委、统战部部长",
     "start_date": "约2019", "end_date": "present", "rank": "副厅级",
     "note": "从上思县委书记提拔，截至2026年7月在任"},
]

# ═══════════════════════════════════════════════════════════════════════
# DATA: Relationships
# ═══════════════════════════════════════════════════════════════════════

relationships = [
    # 戴兰华 ↔ 未知名县长 (当前党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "戴兰华（县委书记）与（待查县长）为上思县党政主要搭档",
     "overlap_org": "上思县党政班子",
     "overlap_period": "2026-",
     "confidence": "unverified"},
    # 戴兰华 ← 黎家迎 (前后任书记)
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "黎家迎任上思县委书记后晋升市委常委/统战部长，戴兰华接任县委书记",
     "overlap_org": "中共上思县委员会",
     "overlap_period": "约2019-",
     "confidence": "plausible"},
    # 黎家迎 ↔ 前任书记
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor",
     "context": "黎家迎的前任县委书记（姓名待查）",
     "overlap_org": "中共上思县委员会",
     "overlap_period": "",
     "confidence": "unverified"},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

def build():
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>上思县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else "书记" in post and not post.startswith("副")
        is_mayor = "县长" in post and "副" not in post
        is_discipline = "纪委" in post

        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"

        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        if otype == "党委":
            ocolor = "255,200,200"
        elif otype == "政府":
            ocolor = "200,200,255"
        elif otype == "人大":
            ocolor = "200,255,255"
        elif otype == "政协":
            ocolor = "255,240,200"
        elif otype == "纪委":
            ocolor = "255,200,150"
        elif otype == "开发区":
            ocolor = "200,255,200"
        elif otype == "乡镇/街道":
            ocolor = "255,255,200"
        else:
            ocolor = "200,200,200"

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    source_register = [
        {"id": "S001", "title": "上思县人民政府门户网站", "url": "http://www.shangsi.gov.cn/",
         "publisher": "上思县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2026年7月可见'戴兰华调研督导文旅提质增效工作'新闻，但领导之窗页面URL未找到"},
        {"id": "S002", "title": "防城港市跨市干部交流网络调查报告", "url": "report/20260723-防城港市-跨市干部交流网络调查报告.md",
         "publisher": "内部报告", "published_at": "2026-07-23", "accessed_at": AS_OF,
         "source_type": "database", "reliability": "medium",
         "notes": "确认黎家迎由上思县委书记晋升防城港市委常委/统战部长"},
        {"id": "S003", "title": "防城区领导班子调查报告", "url": "data/tmp/guangxi_防城区/report/20260723-防城区-领导班子-调查报告.md",
         "publisher": "内部报告", "published_at": "2026-07-23", "accessed_at": AS_OF,
         "source_type": "database", "reliability": "medium",
         "notes": "提及上思县跨区干部交流信息缺口"},
    ]

    # 戴兰华 person JSON
    dlh_timeline = [
        {"start": "", "end": "present", "org": "中共上思县委员会", "title": "上思县委书记",
         "level": "正处级", "location": "广西上思县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "2026年7月以县委书记身份公开活动",
         "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到戴兰华任上思县委书记前的任何早期履历信息。身份细节（出生年、籍贯、教育、入党时间等）均为未知",
         "confidence": "unverified", "source_ids": []},
    ]
    dlh_relationships = [
        {"person": "（待查县长）", "person_id": "shangsi_unknown_mayor", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "戴兰华（县委书记）与当前县长（姓名待查）为上思县党政主要搭档",
         "overlap_org": "上思县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "unverified", "source_ids": ["S001"]},
        {"person": "黎家迎", "person_id": "shangsi_黎家迎", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "戴兰华接替黎家迎任上思县委书记（黎家迎晋升防城港市委常委/统战部长）",
         "overlap_org": "中共上思县委员会",
         "overlap_period": "约2019-2026",
         "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S001", "S002"]},
    ]
    dlh_json = make_person_json(persons[0], dlh_timeline, dlh_relationships, source_register)
    dlh_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-防城港市-县委书记-戴兰华.json")
    with open(dlh_path, "w", encoding="utf-8") as f:
        json.dump(dlh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {dlh_path}")

    # 黎家迎 person JSON
    ljy_timeline = [
        {"start": "约2019", "end": "present", "org": "中共防城港市委员会", "title": "防城港市委常委、统战部部长",
         "level": "副厅级", "location": "广西防城港市", "system": "party", "rank": "副厅级",
         "is_key_promotion": True, "notes": "由上思县委书记晋升市委常委/统战部长",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "", "end": "约2019", "org": "中共上思县委员会", "title": "上思县委书记",
         "level": "正处级", "location": "广西上思县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "任上思县委书记后被提拔",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到黎家迎任上思县委书记前的早期履历",
         "confidence": "unverified", "source_ids": []},
    ]
    ljy_relationships = [
        {"person": "戴兰华", "person_id": "shangsi_戴兰华", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "黎家迎晋升后，戴兰华接任上思县委书记",
         "overlap_org": "中共上思县委员会",
         "overlap_period": "约2019-2026",
         "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001", "S002"]},
        {"person": "（前任县委书记）", "person_id": "shangsi_previous_secretary", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "黎家迎接替前任县委书记任上思县委书记",
         "overlap_org": "中共上思县委员会",
         "overlap_period": "",
         "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
    ]
    ljy_json = make_person_json(persons[2], ljy_timeline, ljy_relationships, source_register)
    ljy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-防城港市-县委书记-黎家迎.json")
    with open(ljy_path, "w", encoding="utf-8") as f:
        json.dump(ljy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {ljy_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
