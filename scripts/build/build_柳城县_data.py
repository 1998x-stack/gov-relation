#!/usr/bin/env python3
"""Build script for 柳城县 cadre exchange network investigation."""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-23"

# Paths
TMP = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(TMP, "柳城县_network.db")
GEXF_PATH = os.path.join(TMP, "柳城县_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

AS_OF_SHORT = AS_OF.replace("-", "")

# ── Persons ──
persons = [
    {"id": 1, "name": "黄立平", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳城县委书记", "current_org": "中共柳城县委员会",
     "source": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF"},
    {"id": 2, "name": "谭建", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳城县代理县长", "current_org": "柳城县人民政府",
     "source": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF"},
    {"id": 3, "name": "罗长青", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳城县人大常委会主任", "current_org": "柳城县人大常委会",
     "source": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF"},
    {"id": 4, "name": "蒋威", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳城县政协主席", "current_org": "柳城县政协",
     "source": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共柳城县委员会", "type": "党委", "level": "县级", "parent": "中共柳州市委员会", "location": "柳城县大埔镇"},
    {"id": 2, "name": "柳城县人民政府", "type": "政府", "level": "县级", "parent": "柳州市人民政府", "location": "柳城县大埔镇"},
    {"id": 3, "name": "柳城县人大常委会", "type": "人大", "level": "县级", "parent": "柳州市人大常委会", "location": "柳城县大埔镇"},
    {"id": 4, "name": "柳城县政协", "type": "政协", "level": "县级", "parent": "柳州市政协", "location": "柳城县大埔镇"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "柳城县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任柳城县委书记，as of 2026-07"},
    {"person_id": 2, "org_id": 2, "title": "柳城县代理县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任柳城县代理县长，as of 2026-07"},
    {"person_id": 3, "org_id": 3, "title": "柳城县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任柳城县人大常委会主任"},
    {"person_id": 4, "org_id": 4, "title": "柳城县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任柳城县政协主席"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "黄立平（县委书记）与谭建（代理县长）为柳城县党政主要领导搭档",
     "overlap_org": "柳城县党政班子", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "党政人大", "context": "黄立平（县委书记）与罗长青（人大主任）为县四家班子领导",
     "overlap_org": "柳城县四家班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "党政政协", "context": "黄立平（县委书记）与蒋威（政协主席）为县四家班子领导",
     "overlap_org": "柳城县四家班子", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "政府人大", "context": "谭建（代理县长）与罗长青（人大主任）为县四家班子领导",
     "overlap_org": "柳城县四家班子", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府政协", "context": "谭建（代理县长）与蒋威（政协主席）为县四家班子领导",
     "overlap_org": "柳城县四家班子", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "人大政协", "context": "罗长青（人大主任）与蒋威（政协主席）为县四家班子领导",
     "overlap_org": "柳城县四家班子", "overlap_period": ""},
]


# =========================================================================
# Helper: Person JSON Builder
# =========================================================================
def make_person_json(person, timeline_items, relationships_items, source_items):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "region": "柳城县",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_柳城县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"liucheng_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": []
            }],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationships_items,
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": source_items,
        "confidence_summary": {
            "identity": "thin",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "Complete career timeline and identity details (birth, birthplace, education) for all core leaders"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete identity and career timeline for {person['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full identity and timeline",
                "suggested_queries": [f"{person['name']} 简历 柳城", f"{person['name']} 任职经历", f"{person['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>柳城县领导班子关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')

    # Edge attributes
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')

    # Nodes — persons
    gexf_lines.append('    <nodes>')
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

        gexf_lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="person"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        gexf_lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        gexf_lines.append(f'        <viz:size value="{size}"/>')
        gexf_lines.append(f'        <viz:shape value="{shape}"/>')
        gexf_lines.append('      </node>')

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

        gexf_lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        gexf_lines.append(f'        <viz:size value="8.0"/>')
        gexf_lines.append(f'        <viz:shape value="hexagon"/>')
        gexf_lines.append('      </node>')

    gexf_lines.append('    </nodes>')

    # Edges
    gexf_lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="relationship"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    source_register = [
        {"id": "S001", "title": "柳城县 百度百科", "url": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF",
         "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium", "notes": "Contains current leadership roster table"},
        {"id": "S002", "title": "县委书记黄立平到企业开展督导工作（柳城人柳城事）",
         "url": "https://www.163.com/dy/article/",
         "publisher": "柳城人柳城事/网易", "published_at": "2026-07-22", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "Confirms 黄立平 as current 县委书记, article published 2026-07-22"},
        {"id": "S003", "title": "柳城县四家班子（扩大）会议召开（柳城人柳城事）",
         "url": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF",
         "publisher": "柳城人柳城事", "published_at": "2026-05-03", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "Baidu Baike reference [29]"},
        {"id": "S004", "title": "柳城县第十八届人大常委会第三十九次会议召开",
         "url": "https://baike.baidu.com/item/%E6%9F%B3%E5%9F%8E%E5%8E%BF",
         "publisher": "柳城人柳城事", "published_at": "2026-07-14", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "Baidu Baike reference [31], may contain appointment details for 谭建"},
    ]

    # 黄立平 person JSON
    hlp_timeline = [
        {"start": "", "end": "present", "org": "中共柳城县委员会", "title": "柳城县委书记",
         "level": "正处级", "location": "广西柳城县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "现任柳城县委书记，as of 2026-07-22",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到黄立平任柳城县委书记前的完整履历。身份细节（出生年、籍贯、教育等）均为未知",
         "confidence": "unverified", "source_ids": []},
    ]
    hlp_relationships = [
        {"person": "谭建", "person_id": "liucheng_谭建", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄立平（县委书记）与谭建（代理县长）为柳城县党政主要搭档",
         "overlap_org": "柳城县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    hlp_json = make_person_json(persons[0], hlp_timeline, hlp_relationships, source_register)
    hlp_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-县委书记-黄立平.json")
    with open(hlp_path, "w", encoding="utf-8") as f:
        json.dump(hlp_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hlp_path}")

    # 谭建 person JSON
    tj_timeline = [
        {"start": "", "end": "present", "org": "柳城县人民政府", "title": "柳城县代理县长",
         "level": "正处级", "location": "广西柳城县", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "现任柳城县代理县长，as of 2026-07",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到谭建任柳城县代理县长前的完整履历。身份细节（出生年、籍贯、教育等）均为未知",
         "confidence": "unverified", "source_ids": []},
    ]
    tj_relationships = [
        {"person": "黄立平", "person_id": "liucheng_黄立平", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "谭建（代理县长）与黄立平（县委书记）为柳城县党政主要搭档",
         "overlap_org": "柳城县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    tj_json = make_person_json(persons[1], tj_timeline, tj_relationships, source_register)
    tj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-代理县长-谭建.json")
    with open(tj_path, "w", encoding="utf-8") as f:
        json.dump(tj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {tj_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
