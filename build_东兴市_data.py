#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Dongxing City leadership network.

东兴市 — 广西壮族自治区防城港市代管县级市

Targets: 市委书记, 市长
Research date: 2026-07-23
Web access: severely degraded (Exa rate-limited, Baidu 403, Baike/Google/Bing all blocked,
            dongxing.gov.cn DNS NXDOMAIN, web.archive.org connection refused)
Status: partial evidence mode — all facts have confidence labels. Some core figures
        have incomplete biographies. Build artifacts are structurally valid.
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(BASE)
DB_PATH = os.path.join(TMP, "东兴市_network.db")
GEXF_PATH = os.path.join(TMP, "东兴市_network.gexf")
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
        "person_id": f"dongxing_{person['name']}",
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
            "region": "东兴市",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_东兴市",
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
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Web access entirely degraded during research (2026-07-23). All leadership data is from pre-training knowledge, not verified against current official sources."
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Who is the current 市委书记 of 东兴市 as of {AS_OF}? Is it still 彭绍关 or someone else?",
                "why_it_matters": "This is the primary target role for the investigation.",
                "suggested_queries": [
                    f"彭绍关 东兴市委书记 2025 2026",
                    f"东兴市 市委书记 2025 2026"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"Who is the current 市长 of 东兴市 as of {AS_OF}? Is it still 李健 or someone else?",
                "why_it_matters": "This is the secondary target role for the investigation.",
                "suggested_queries": [
                    f"李健 东兴市市长 2025 2026",
                    f"东兴市 市长 2025 2026"
                ],
                "last_attempted": AS_OF
            }
        ]
    }


# =========================================================================
# Data (sourced from pre-training knowledge — NOT verified against current
# official sources. All claims are labeled 'unverified' due to total web
# access failure during this research session.)
# =========================================================================

# Note: The following data is based on pre-training knowledge which may be
# outdated. All confidences are set to 'unverified'. When web access is
# restored, verify against:
# - www.dongxing.gov.cn (DNS currently NXDOMAIN)
# - baike.baidu.com (currently 403)
# - 防城港市委组织部 任前公示

persons = [
    {
        "id": 1,
        "name": "彭绍关",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兴市委书记",
        "current_org": "中共东兴市委员会",
        "current_confirmed": False,
        "source": "未确认 — 网络完全不可用"
    },
    {
        "id": 2,
        "name": "李健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兴市委副书记、市长",
        "current_org": "东兴市人民政府",
        "current_confirmed": False,
        "source": "未确认 — 网络完全不可用"
    },
    {
        "id": 3,
        "name": "罗湘洲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "current_post": "东兴市人大常委会主任",
        "current_org": "东兴市人大常委会",
        "current_confirmed": False,
        "source": "未确认 — 网络完全不可用"
    },
    {
        "id": 4,
        "name": "吴文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "current_post": "东兴市政协主席",
        "current_org": "政协东兴市委员会",
        "current_confirmed": False,
        "source": "未确认 — 网络完全不可用"
    },
    {
        "id": 5,
        "name": "陈建林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "current_post": "东兴市委副书记（前任市长）",
        "current_org": "中共东兴市委员会",
        "current_confirmed": False,
        "source": "未确认 — 网络完全不可用"
    },
]

# Organizations
organizations = [
    {"id": 1, "name": "中共东兴市委员会", "type": "党委", "level": "县级", "parent": "中共防城港市委员会", "location": "广西东兴"},
    {"id": 2, "name": "东兴市人民政府", "type": "政府", "level": "县级", "parent": "防城港市人民政府", "location": "广西东兴"},
    {"id": 3, "name": "东兴市人大常委会", "type": "人大", "level": "县级", "parent": "防城港市人大常委会", "location": "广西东兴"},
    {"id": 4, "name": "政协东兴市委员会", "type": "政协", "level": "县级", "parent": "政协防城港市委员会", "location": "广西东兴"},
    {"id": 5, "name": "中共东兴市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共防城港市纪律检查委员会", "location": "广西东兴"},
    {"id": 6, "name": "中共东兴市委组织部", "type": "党委", "level": "县级", "parent": "中共东兴市委员会", "location": "广西东兴"},
    {"id": 7, "name": "中共东兴市委政法委", "type": "党委", "level": "县级", "parent": "中共东兴市委员会", "location": "广西东兴"},
    {"id": 8, "name": "中共东兴市委宣传部", "type": "党委", "level": "县级", "parent": "中共东兴市委员会", "location": "广西东兴"},
    {"id": 9, "name": "东兴国家重点开发开放试验区管委会", "type": "开发区", "level": "县级", "parent": "防城港市人民政府", "location": "广西东兴"},
    {"id": 10, "name": "东兴市江平镇", "type": "乡镇/街道", "level": "乡镇", "parent": "东兴市人民政府", "location": "广西东兴"},
    {"id": 11, "name": "东兴市东兴镇", "type": "乡镇/街道", "level": "乡镇", "parent": "东兴市人民政府", "location": "广西东兴"},
    {"id": 12, "name": "东兴市马路镇", "type": "乡镇/街道", "level": "乡镇", "parent": "东兴市人民政府", "location": "广西东兴"},
]

# Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 彭绍关 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "东兴市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 李健 — 市长
    {"person_id": 2, "org_id": 2, "title": "东兴市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "东兴市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 罗湘洲 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "东兴市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 吴文 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "东兴市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 陈建林 — 前任市长/副书记
    {"person_id": 5, "org_id": 1, "title": "东兴市委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "前任市长"},
    {"person_id": 5, "org_id": 2, "title": "东兴市市长（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# Relationships
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "彭绍关（市委书记）与李健（市长）为东兴市党政主要搭档",
        "overlap_org": "东兴市党政班子",
        "overlap_period": ""
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "彭绍关（市委书记）与罗湘洲（人大主任）同为东兴市四家班子主要领导",
        "overlap_org": "东兴市四家班子",
        "overlap_period": ""
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "彭绍关（市委书记）与吴文（政协主席）同为东兴市四家班子主要领导",
        "overlap_org": "东兴市四家班子",
        "overlap_period": ""
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "predecessor_successor",
        "context": "李健接替陈建林任东兴市长",
        "overlap_org": "东兴市人民政府",
        "overlap_period": ""
    },
]


# =========================================================================
# Build Main
# =========================================================================
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
    lines.append('    <description>东兴市领导班子关系网络（基于未验证的预训练知识 — 因网络完全不可用未能核实）</description>')
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
        is_mayor = "市长" in post and "副" not in post and "市委" not in post.split("、")[0] if "、" in post else ("市长" in post and "副" not in post)
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

    source_register = []

    # 彭绍关 person JSON
    psg_timeline = []
    psg_relationships = [
        {"person": "李健", "person_id": "dongxing_李健", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "彭绍关（市委书记）与李健（市长）为东兴市党政主要搭档",
         "overlap_org": "东兴市党政班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
    ]
    psg_json = make_person_json(persons[0], psg_timeline, psg_relationships, source_register)
    psg_json["identity"] = {
        "person_id": "dongxing_彭绍关",
        "name": "彭绍关",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "彭绍关_",
            "name_birthplace": "彭绍关_",
            "official_profile_url": ""
        }
    }
    psg_json["confidence_summary"]["identity"] = "unverified"
    psg_json["confidence_summary"]["current_role"] = "unverified"
    psg_json["confidence_summary"]["career_completeness"] = "thin"
    psg_json["confidence_summary"]["biggest_gap"] = "所有信息均未核实。网络完全不可用（Exa限流、百度403、东兴.gov.cn DNS NXDOMAIN）"
    psg_json["open_questions"] = [
        {"priority": "critical", "question": "彭绍关的出生年月、籍贯、学历、入党时间、参加工作时间", "why_it_matters": "无法建立身份标识", "suggested_queries": ["彭绍关 简历 东兴"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "彭绍关的完整履历", "why_it_matters": "无法追溯其任职路径", "suggested_queries": ["彭绍关 东兴 任职经历"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "彭绍关是否仍在任东兴市委书记", "why_it_matters": "可能已调整", "suggested_queries": ["彭绍关 东兴市委书记 2025 2026"], "last_attempted": AS_OF},
    ]
    psg_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-防城港市-市委书记-彭绍关.json")
    with open(psg_path, "w", encoding="utf-8") as f:
        json.dump(psg_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {psg_path}")

    # 李健 person JSON
    lj_timeline = []
    lj_relationships = [
        {"person": "彭绍关", "person_id": "dongxing_彭绍关", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "李健（市长）与彭绍关（市委书记）为东兴市党政主要搭档",
         "overlap_org": "东兴市党政班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
        {"person": "陈建林", "person_id": "dongxing_陈建林", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "李健接替陈建林任东兴市长",
         "overlap_org": "东兴人民政府",
         "overlap_period": "",
         "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
    ]
    lj_json = make_person_json(persons[1], lj_timeline, lj_relationships, source_register)
    lj_json["identity"] = {
        "person_id": "dongxing_李健",
        "name": "李健",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "李健_",
            "name_birthplace": "李健_",
            "official_profile_url": ""
        }
    }
    lj_json["confidence_summary"]["identity"] = "unverified"
    lj_json["confidence_summary"]["current_role"] = "unverified"
    lj_json["confidence_summary"]["career_completeness"] = "thin"
    lj_json["open_questions"] = [
        {"priority": "critical", "question": "李健的出生年月、籍贯、学历、入党时间、参加工作时间", "why_it_matters": "无法建立身份标识", "suggested_queries": ["李健 东兴 市长 简历"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "李健的完整履历", "why_it_matters": "无法追溯其任职路径", "suggested_queries": ["李健 东兴 任职经历"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "李健是否仍在任东兴市长", "why_it_matters": "可能已调整", "suggested_queries": ["李健 东兴市长 2025 2026"], "last_attempted": AS_OF},
    ]
    lj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-防城港市-市长-李健.json")
    with open(lj_path, "w", encoding="utf-8") as f:
        json.dump(lj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lj_path}")

    # 陈建林 person JSON (predecessor)
    cjl_timeline = []
    cjl_relationships = [
        {"person": "李健", "person_id": "dongxing_李健", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "陈建林卸任东兴市长后由李健接任",
         "overlap_org": "东兴市人民政府",
         "overlap_period": "",
         "direction": "person_to_other", "confidence": "unverified", "source_ids": []},
    ]
    cjl_json = make_person_json(persons[4], cjl_timeline, cjl_relationships, source_register)
    cjl_json["identity"] = {
        "person_id": "dongxing_陈建林",
        "name": "陈建林",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "陈建林_",
            "name_birthplace": "陈建林_",
            "official_profile_url": ""
        }
    }
    cjl_json["confidence_summary"]["identity"] = "unverified"
    cjl_json["confidence_summary"]["current_role"] = "unverified"
    cjl_json["confidence_summary"]["career_completeness"] = "thin"
    cjl_json["open_questions"] = [
        {"priority": "critical", "question": "陈建林的出生年月、籍贯、学历", "why_it_matters": "无法建立身份标识", "suggested_queries": ["陈建林 东兴 简历"], "last_attempted": AS_OF},
        {"priority": "high", "question": "陈建林卸任东兴市长后去向", "why_it_matters": "了解班子调整动态", "suggested_queries": ["陈建林 东兴 市长 卸任"], "last_attempted": AS_OF},
    ]
    cjl_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-防城港市-市长-陈建林.json")
    with open(cjl_path, "w", encoding="utf-8") as f:
        json.dump(cjl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cjl_path}")

    print("\nBuild complete (partial evidence mode). All data unverified due to total web access failure.")
    print("See report/open_gaps.md for details.")


if __name__ == "__main__":
    build()
