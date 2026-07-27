#!/usr/bin/env python3
"""Build script for 鹿寨县 cadre exchange network investigation."""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-23"

# Paths
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(TMP, "鹿寨县_network.db")
GEXF_PATH = os.path.join(TMP, "鹿寨县_network.gexf")
PERSONS_DIR = os.path.join(TMP)

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

AS_OF_SHORT = AS_OF.replace("-", "")

# ── Persons ──
persons = [
    {"id": 1, "name": "雷道理", "gender": "男", "ethnicity": "汉族", "birth": "1981", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "鹿寨县委书记", "current_org": "中共鹿寨县委员会",
     "source": "https://www.163.com/dy/article/L11IJ0I405563DJA.html"},
    {"id": 2, "name": "覃宝花", "gender": "女", "ethnicity": "壮族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "鹿寨县委副书记、县长", "current_org": "鹿寨县人民政府",
     "source": "https://baike.baidu.com/item/%E9%B9%BF%E5%AF%A8%E5%8E%BF/4696525"},
    {"id": 3, "name": "陈需勤", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "鹿寨县人大常委会主任", "current_org": "鹿寨县人大常委会",
     "source": "https://baike.baidu.com/item/%E9%B9%BF%E5%AF%A8%E5%8E%BF/4696525"},
    {"id": 4, "name": "朱燕文", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "鹿寨县政协主席", "current_org": "鹿寨县政协",
     "source": "https://baike.baidu.com/item/%E9%B9%BF%E5%AF%A8%E5%8E%BF/4696525"},
    {"id": 5, "name": "王轶", "gender": "男", "ethnicity": "汉族", "birth": "1978-07", "birthplace": "湖北黄陂",
     "education": "在职大学（湖南大学网络学院法学专业）", "party_join": "2004-08", "work_start": "1998-10",
     "current_post": "来宾市兴宾区委书记（原鹿寨县委书记）", "current_org": "中共来宾市兴宾区委员会",
     "source": "https://www.163.com/dy/article/K87FM1LV0514R9P4.html"},
    {"id": 6, "name": "杨毅", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任鹿寨县委书记（2025.10-2026.06，约8个月）", "current_org": "中共鹿寨县委员会（前）",
     "source": "https://www.163.com/dy/article/L11IJ0I405563DJA.html"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共鹿寨县委员会", "type": "党委", "level": "县级", "parent": "中共柳州市委员会", "location": "鹿寨县鹿寨镇"},
    {"id": 2, "name": "鹿寨县人民政府", "type": "政府", "level": "县级", "parent": "柳州市人民政府", "location": "鹿寨县鹿寨镇"},
    {"id": 3, "name": "鹿寨县人大常委会", "type": "人大", "level": "县级", "parent": "柳州市人大常委会", "location": "鹿寨县鹿寨镇"},
    {"id": 4, "name": "鹿寨县政协", "type": "政协", "level": "县级", "parent": "柳州市政协", "location": "鹿寨县鹿寨镇"},
    {"id": 5, "name": "柳州市自然资源和规划局", "type": "政府", "level": "地市级", "parent": "柳州市人民政府", "location": "柳州市"},
    {"id": 6, "name": "三江侗族自治县人民政府", "type": "政府", "level": "县级", "parent": "柳州市人民政府", "location": "三江侗族自治县古宜镇"},
    {"id": 7, "name": "中共三江侗族自治县委员会", "type": "党委", "level": "县级", "parent": "中共柳州市委员会", "location": "三江侗族自治县古宜镇"},
    {"id": 8, "name": "中共来宾市兴宾区委员会", "type": "党委", "level": "县级", "parent": "中共来宾市委员会", "location": "来宾市兴宾区"},
    {"id": 9, "name": "柳州市鱼峰区人民政府", "type": "政府", "level": "县级", "parent": "柳州市人民政府", "location": "柳州市鱼峰区"},
    {"id": 10, "name": "中共柳州市鱼峰区委员会", "type": "党委", "level": "县级", "parent": "中共柳州市委员会", "location": "柳州市鱼峰区"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "鹿寨县委书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级",
     "note": "2026年7月上任，as of 2026-07-23"},
    {"person_id": 1, "org_id": 5, "title": "柳州市自然资源和规划局党组书记、局长", "start_date": "2024-04", "end_date": "2026-07", "rank": "正处级",
     "note": "调任鹿寨县委书记前职务"},
    {"person_id": 1, "org_id": 7, "title": "三江县委常委、副县长", "start_date": "", "end_date": "2024-04", "rank": "副处级",
     "note": "任柳州市自然资源和规划局长前职务"},
    {"person_id": 1, "org_id": 6, "title": "三江县副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "挂职，具体起止时间未知"},
    {"person_id": 2, "org_id": 2, "title": "鹿寨县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任鹿寨县县长，as of 2026-07"},
    {"person_id": 3, "org_id": 3, "title": "鹿寨县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任鹿寨县人大常委会主任"},
    {"person_id": 4, "org_id": 4, "title": "鹿寨县政协主席", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任鹿寨县政协主席"},
    {"person_id": 5, "org_id": 8, "title": "来宾市兴宾区委书记", "start_date": "2025-08", "end_date": "present", "rank": "正处级",
     "note": "2025年8月跨市调任兴宾区委书记"},
    {"person_id": 5, "org_id": 1, "title": "鹿寨县委书记", "start_date": "2020-08", "end_date": "2025-08", "rank": "正处级",
     "note": "在鹿寨县工作多年，先任县长后任书记；任书记约5年"},
    {"person_id": 5, "org_id": 2, "title": "鹿寨县委副书记、县长", "start_date": "", "end_date": "2020-08", "rank": "正处级",
     "note": "升任书记前担任县长"},
    {"person_id": 5, "org_id": 10, "title": "鱼峰区委副书记、区长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 5, "org_id": 10, "title": "鱼峰区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    {"person_id": 6, "org_id": 1, "title": "鹿寨县委书记", "start_date": "2025-10", "end_date": "2026-06", "rank": "正处级",
     "note": "任期极短，约8个月，去向不明"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "雷道理（县委书记）与覃宝花（县长）为鹿寨县党政主要领导搭档",
     "overlap_org": "鹿寨县党政班子", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "党政人大", "context": "雷道理（县委书记）与陈需勤（人大主任）为县四家班子领导",
     "overlap_org": "鹿寨县四家班子", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "党政政协", "context": "雷道理（县委书记）与朱燕文（政协主席）为县四家班子领导",
     "overlap_org": "鹿寨县四家班子", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 3, "type": "政府人大", "context": "覃宝花（县长）与陈需勤（人大主任）为县四家班子领导",
     "overlap_org": "鹿寨县四家班子", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府政协", "context": "覃宝花（县长）与朱燕文（政协主席）为县四家班子领导",
     "overlap_org": "鹿寨县四家班子", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "人大政协", "context": "陈需勤（人大主任）与朱燕文（政协主席）为县四家班子领导",
     "overlap_org": "鹿寨县四家班子", "overlap_period": ""},
    {"person_a": 5, "person_b": 2, "type": "党政搭档", "context": "王轶（时任县委书记）与覃宝花（县长）在鹿寨县共事",
     "overlap_org": "鹿寨县党政班子", "overlap_period": "2020-2025"},
    {"person_a": 5, "person_b": 6, "type": "前后任", "context": "王轶（2020.8-2025.8鹿寨县委书记）→ 杨毅（2025.10-2026.6接任书记）",
     "overlap_org": "中共鹿寨县委员会", "overlap_period": "2025-2026"},
    {"person_a": 6, "person_b": 1, "type": "前后任", "context": "杨毅（2025.10-2026.6鹿寨县委书记）→ 雷道理（2026.7接任书记）",
     "overlap_org": "中共鹿寨县委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 3, "type": "党政人大", "context": "王轶（时任书记）与陈需勤（人大主任）曾共事",
     "overlap_org": "鹿寨县四家班子", "overlap_period": "2020-2025"},
    {"person_a": 5, "person_b": 4, "type": "党政政协", "context": "王轶（时任书记）与朱燕文（政协主席）曾共事",
     "overlap_org": "鹿寨县四家班子", "overlap_period": "2020-2025"},
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
            "region": "鹿寨县",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_鹿寨县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"luzhai_{person['name']}",
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
            "biggest_gap": "Complete career timeline and identity details for 覃宝花, 杨毅, 陈需勤, 朱燕文; early career of 雷道理"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline and identity details for {person['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full identity and timeline",
                "suggested_queries": [f"{person['name']} 简历 鹿寨", f"{person['name']} 任职经历", f"{person['name']} 百度百科"],
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
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>鹿寨县领导班子关系网络</description>')
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
        {"id": "S001", "title": "雷道理任鹿寨县委书记（网易号/汲古知新）", "url": "https://www.163.com/dy/article/L11IJ0I405563DJA.html",
         "publisher": "网易号", "published_at": "2026-07-05", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "引用官方公众号'我爱鹿寨'消息，确认雷道理2026年7月任鹿寨县委书记；确认杨毅前任身份"},
        {"id": "S002", "title": "广西柳州市鹿寨县委书记王轶跨市调任来宾市兴宾区委书记（澎湃新闻）",
         "url": "https://www.163.com/dy/article/K87FM1LV0514R9P4.html",
         "publisher": "澎湃新闻", "published_at": "2025-08-30", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "确认王轶完整履历：出生年月、籍贯、入党时间、参加工作、学历、历任职务及跨市调任详情"},
        {"id": "S003", "title": "鹿寨县 百度百科", "url": "https://baike.baidu.com/item/%E9%B9%BF%E5%AF%A8%E5%8E%BF/4696525",
         "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium", "notes": "数据截至2025年11月，列有四家班子领导名单：覃宝花(县长)、陈需勤(人大主任)、朱燕文(政协主席)"},
    ]

    # 雷道理 person JSON
    ldl_timeline = [
        {"start": "2026-07", "end": "present", "org": "中共鹿寨县委员会", "title": "鹿寨县委书记",
         "level": "正处级", "location": "广西鹿寨县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "2026年7月任鹿寨县委书记",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-04", "end": "2026-07", "org": "柳州市自然资源和规划局", "title": "党组书记、局长",
         "level": "正处级", "location": "广西柳州市", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "2024年4月任局长",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "2024-04", "org": "中共三江侗族自治县委员会", "title": "县委常委、副县长",
         "level": "副处级", "location": "广西三江县", "system": "government", "rank": "副处级",
         "is_key_promotion": False, "notes": "任柳州市自然资源局前在三江县工作",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "三江侗族自治县人民政府", "title": "副县长（挂职）",
         "level": "副处级", "location": "广西三江县", "system": "government", "rank": "副处级",
         "is_key_promotion": False, "notes": "挂职经历",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到雷道理1981年出生至赴三江县工作前的早期履历",
         "confidence": "unverified", "source_ids": []},
    ]
    ldl_relationships = [
        {"person": "覃宝花", "person_id": "luzhai_覃宝花", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "雷道理（县委书记）与覃宝花（县长）为鹿寨县党政主要搭档",
         "overlap_org": "鹿寨县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "杨毅", "person_id": "luzhai_杨毅", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "雷道理接替杨毅任鹿寨县委书记",
         "overlap_org": "中共鹿寨县委员会",
         "overlap_period": "2026",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    ldl_json = make_person_json(persons[0], ldl_timeline, ldl_relationships, source_register)
    ldl_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-县委书记-雷道理.json")
    with open(ldl_path, "w", encoding="utf-8") as f:
        json.dump(ldl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {ldl_path}")

    # 覃宝花 person JSON
    qbh_timeline = [
        {"start": "", "end": "present", "org": "鹿寨县人民政府", "title": "鹿寨县委副书记、县长",
         "level": "正处级", "location": "广西鹿寨县", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "现任鹿寨县县长，as of 2026-07",
         "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到覃宝花任鹿寨县长前的任何履历信息。身份细节（出生年、籍贯、教育、入党时间等）均为未知",
         "confidence": "unverified", "source_ids": []},
    ]
    qbh_relationships = [
        {"person": "雷道理", "person_id": "luzhai_雷道理", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "覃宝花（县长）与雷道理（县委书记）为鹿寨县党政主要搭档",
         "overlap_org": "鹿寨县党政班子",
         "overlap_period": "2026-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "王轶", "person_id": "luzhai_王轶", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "覃宝花（县长）在王轶任县委书记期间亦担任县长，二人曾在鹿寨县党政班子共事",
         "overlap_org": "鹿寨县党政班子",
         "overlap_period": "2020-2025",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S002", "S003"]},
    ]
    qbh_json = make_person_json(persons[1], qbh_timeline, qbh_relationships, source_register)
    qbh_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-县长-覃宝花.json")
    with open(qbh_path, "w", encoding="utf-8") as f:
        json.dump(qbh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {qbh_path}")

    # 王轶 person JSON (predecessor with full bio)
    wy_timeline = [
        {"start": "2025-08", "end": "present", "org": "中共来宾市兴宾区委员会", "title": "兴宾区委书记",
         "level": "正处级", "location": "广西来宾市", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "2025年8月从鹿寨县跨市调任兴宾区委书记",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2020-08", "end": "2025-08", "org": "中共鹿寨县委员会", "title": "鹿寨县委书记",
         "level": "正处级", "location": "广西鹿寨县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "先任鹿寨县长后升书记，任期约5年",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "", "end": "2020-08", "org": "鹿寨县人民政府", "title": "鹿寨县委副书记、县长",
         "level": "正处级", "location": "广西鹿寨县", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "升任县委书记前担任县长",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "", "end": "", "org": "中共柳州市鱼峰区委员会/鱼峰区人民政府", "title": "鱼峰区委常委、副区长→副书记、区长",
         "level": "正处级", "location": "广西柳州市", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "在鱼峰区从区委常委、副区长升至区长",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    wy_relationships = [
        {"person": "覃宝花", "person_id": "luzhai_覃宝花", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王轶（时任县委书记）与覃宝花（县长）在鹿寨县党政班子共事多年",
         "overlap_org": "鹿寨县党政班子",
         "overlap_period": "2020-2025",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "杨毅", "person_id": "luzhai_杨毅", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "王轶调任兴宾后，杨毅接任鹿寨县委书记",
         "overlap_org": "中共鹿寨县委员会",
         "overlap_period": "2025",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    wy_json = make_person_json(persons[4], wy_timeline, wy_relationships, source_register)
    wy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-县委书记-王轶.json")
    with open(wy_path, "w", encoding="utf-8") as f:
        json.dump(wy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wy_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
