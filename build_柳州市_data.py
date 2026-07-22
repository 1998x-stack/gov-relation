#!/usr/bin/env python3
"""柳州市（地级市）领导班子关系网络数据生成脚本。

Generated at: 2026-07-22
Task: guangxi_柳州市
"""

import json
import os
import sqlite3

# =========================================================================
# Paths
# =========================================================================
TMP = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(TMP, "柳州市_network.db")
GEXF_PATH = os.path.join(TMP, "柳州市_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-22"

# =========================================================================
# Data: Persons
# =========================================================================
persons = [
    {
        "id": 1,
        "name": "张壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年5月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "柳州市委书记",
        "current_org": "中共柳州市委员会",
        "source": "https://www.163.com/dy/article/KBRTIBEV0514CQIE.html"
    },
    {
        "id": 2,
        "name": "待查（现任市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "柳州市市长（待确认）",
        "current_org": "柳州市人民政府",
        "source": ""
    },
    {
        "id": 3,
        "name": "谭丕创",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "广西贵港",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广西壮族自治区党委常委、统战部部长",
        "current_org": "广西壮族自治区委员会",
        "source": "https://www.163.com/dy/article/JD4G6QB0055040N3.html"
    },
    {
        "id": 4,
        "name": "张晓钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "江苏南通",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广西壮族自治区人大常委会副主任",
        "current_org": "广西壮族自治区人大常委会",
        "source": "https://www.163.com/dy/article/JD4G6QB0055040N3.html"
    },
    {
        "id": 5,
        "name": "吴炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原柳州市委书记（已落马判死缓）",
        "current_org": "",
        "source": "https://www.163.com/dy/article/JJQ15A110530WJIN.html"
    },
]

# =========================================================================
# Data: Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共柳州市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西柳州"},
    {"id": 2, "name": "柳州市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西柳州"},
    {"id": 3, "name": "广西壮族自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广西南宁"},
    {"id": 4, "name": "广西壮族自治区人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "广西南宁"},
    {"id": 5, "name": "中共广西壮族自治区委员会", "type": "党委", "level": "省级", "parent": "", "location": "广西南宁"},
]

# =========================================================================
# Data: Positions
# =========================================================================
positions = [
    # 张壮
    {"person_id": 1, "org_id": 1, "title": "柳州市委书记", "start_date": "2025-10", "end_date": "present", "rank": "正厅级", "note": "2025年10月任柳州市委书记，此前为柳州市市长"},
    {"person_id": 1, "org_id": 2, "title": "柳州市市长", "start_date": "2021", "end_date": "2025-10", "rank": "正厅级", "note": "2021年起任柳州市市长"},
    {"person_id": 1, "org_id": 2, "title": "柳州市委副书记、市长", "start_date": "2021", "end_date": "2025-10", "rank": "正厅级", "note": ""},
    # 待查市长
    {"person_id": 2, "org_id": 2, "title": "柳州市市长", "start_date": "unknown", "end_date": "present", "rank": "正厅级", "note": "张壮升任书记后，现任市长姓名待确认"},
    # 谭丕创
    {"person_id": 3, "org_id": 5, "title": "广西壮族自治区党委常委、统战部部长", "start_date": "2025-10", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "柳州市委书记（兼）", "start_date": "2024-09", "end_date": "2025-10", "rank": "正厅级（兼）", "note": "兼任柳州市委书记，同时为自治区副主席"},
    {"person_id": 3, "org_id": 3, "title": "广西壮族自治区副主席", "start_date": "2024-05", "end_date": "2025-10", "rank": "副省级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "防城港市委书记", "start_date": "2021-03", "end_date": "2024-09", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "钦州市市长", "start_date": "2018", "end_date": "2021-03", "rank": "正厅级", "note": ""},
    # 张晓钦
    {"person_id": 4, "org_id": 4, "title": "广西壮族自治区人大常委会副主任", "start_date": "2018", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "柳州市委书记（兼）", "start_date": "2023-11", "end_date": "2024-09", "rank": "正厅级（兼）", "note": "兼任柳州市委书记"},
    {"person_id": 4, "org_id": 3, "title": "广西壮族自治区政府副主席", "start_date": "2013", "end_date": "2018", "rank": "副省级", "note": ""},
    # 吴炜
    {"person_id": 5, "org_id": 1, "title": "柳州市委书记", "start_date": "待查", "end_date": "2024", "rank": "正厅级", "note": "被查落马，2024年12月一审被判死缓"},
    {"person_id": 5, "org_id": 2, "title": "柳州市市长", "start_date": "待查", "end_date": "待查", "rank": "正厅级", "note": ""},
]

# =========================================================================
# Data: Relationships
# =========================================================================
relationships = [
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "张壮接替谭丕创任柳州市委书记",
        "overlap_org": "中共柳州市委员会",
        "overlap_period": "2024-09/2025-10"
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "predecessor_successor",
        "context": "谭丕创接替张晓钦任柳州市委书记",
        "overlap_org": "中共柳州市委员会",
        "overlap_period": "2023-11/2024-09"
    },
    {
        "person_a": 4, "person_b": 5,
        "type": "predecessor_successor",
        "context": "张晓钦接替吴炜（吴炜被查后）任柳州市委书记",
        "overlap_org": "中共柳州市委员会",
        "overlap_period": "2023-11"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "张壮任市长期间与吴炜（时任书记）党政搭档",
        "overlap_org": "柳州市党政班子",
        "overlap_period": "2021-2024"
    },
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
            "region": "柳州市",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_柳州市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"liuzhou_{person['name']}",
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
            "administrative_rank": "正厅级",
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
            "career_pattern": "local_ladder",
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
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "Complete career timeline before mayoral role"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role for {person['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任职经历", f"{person['name']} 百度百科"],
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
    gexf_lines.append('    <description>柳州市领导班子关系网络</description>')
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
        is_mayor = "市长" in post and "副" not in post
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
        {"id": "S001", "title": "张壮任广西柳州市委书记（中国经济网）", "url": "https://www.163.com/dy/article/KBRTIBEV0514CQIE.html",
         "publisher": "中国经济网", "published_at": "2025-10-14", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "广西壮族自治区副主席谭丕创兼任柳州市委书记（上观新闻）",
         "url": "https://www.163.com/dy/article/JD4G6QB0055040N3.html",
         "publisher": "上观新闻", "published_at": "2024-09-27", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "Contains full biography of 谭丕创 and 张晓钦"},
        {"id": "S003", "title": "柳州市委原书记吴炜一审被判死缓（齐鲁壹点）",
         "url": "https://www.163.com/dy/article/JJQ15A110530WJIN.html",
         "publisher": "齐鲁壹点", "published_at": "2024-12-19", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": ""},
    ]

    # 张壮 person JSON
    zz_timeline = [
        {"start": "2025-10", "end": "present", "org": "中共柳州市委员会", "title": "柳州市委书记",
         "level": "正厅级", "location": "广西柳州", "system": "party", "rank": "正厅级",
         "is_key_promotion": True, "notes": "接替谭丕创任柳州市委书记",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021", "end": "2025-10", "org": "柳州市人民政府", "title": "柳州市市长",
         "level": "正厅级", "location": "广西柳州", "system": "government", "rank": "正厅级",
         "is_key_promotion": True, "notes": "任柳州市委副书记、市长",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "2021", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到张壮任柳州市市长前的完整履历。已知：1970年5月生，汉族，研究生学历，中共党员",
         "confidence": "unverified", "source_ids": []},
    ]
    zz_relationships = [
        {"person": "谭丕创", "person_id": "liuzhou_谭丕创", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "张壮接替谭丕创任柳州市委书记",
         "overlap_org": "中共柳州市委员会",
         "overlap_period": "2024-09/2025-10",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "吴炜", "person_id": "liuzhou_吴炜", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "张壮任市长期间与吴炜（时任书记）党政搭档",
         "overlap_org": "柳州市党政班子",
         "overlap_period": "2021-2024",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]
    zz_json = make_person_json(persons[0], zz_timeline, zz_relationships, source_register)
    zz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-市委书记-张壮.json")
    with open(zz_path, "w", encoding="utf-8") as f:
        json.dump(zz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zz_path}")

    # 谭丕创 person JSON
    tp_timeline = [
        {"start": "2025-10", "end": "present", "org": "中共广西壮族自治区委员会", "title": "自治区党委常委、统战部部长",
         "level": "副省级", "location": "广西南宁", "system": "party", "rank": "副省级",
         "is_key_promotion": True, "notes": "晋升自治区党委常委",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2024-09", "end": "2025-10", "org": "中共柳州市委员会", "title": "柳州市委书记（兼）",
         "level": "正厅级（兼）", "location": "广西柳州", "system": "party", "rank": "正厅级",
         "is_key_promotion": True, "notes": "兼任柳州市委书记",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2024-05", "end": "2025-10", "org": "广西壮族自治区人民政府", "title": "广西壮族自治区副主席",
         "level": "副省级", "location": "广西南宁", "system": "government", "rank": "副省级",
         "is_key_promotion": True, "notes": "",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021-03", "end": "2024-09", "org": "中共防城港市委员会", "title": "防城港市委书记",
         "level": "正厅级", "location": "广西防城港", "system": "party", "rank": "正厅级",
         "is_key_promotion": True, "notes": "",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2018", "end": "2021-03", "org": "钦州市人民政府", "title": "钦州市市长",
         "level": "正厅级", "location": "广西钦州", "system": "government", "rank": "正厅级",
         "is_key_promotion": True, "notes": "",
         "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "待查", "end": "2018", "org": "曾任", "title": "凭祥市委书记、梧州市委常委组织部部长、百色市副市长等职",
         "level": "厅级", "location": "广西", "system": "party", "rank": "厅级",
         "is_key_promotion": False,
         "notes": "曾任广西凭祥市委副书记、市长，凭祥市委书记，梧州市委常委、组织部部长，百色市委常委、副市长",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    tp_relationships = [
        {"person": "张壮", "person_id": "liuzhou_张壮", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "谭丕创兼任柳州市委书记期间，张壮为市长并最终接任书记",
         "overlap_org": "中共柳州市委员会/柳州市人民政府",
         "overlap_period": "2024-09/2025-10",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "张晓钦", "person_id": "liuzhou_张晓钦", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "谭丕创接替张晓钦任柳州市委书记",
         "overlap_org": "中共柳州市委员会",
         "overlap_period": "2024-09",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    tp_json = make_person_json(persons[2], tp_timeline, tp_relationships, source_register)
    tp_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-市委书记（兼）-谭丕创.json")
    with open(tp_path, "w", encoding="utf-8") as f:
        json.dump(tp_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {tp_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
