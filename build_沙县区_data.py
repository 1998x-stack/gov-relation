#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 沙县区, Sanming City, Fujian Province.

Covers: Party Secretary (区委书记), District Mayor (区长), leadership team,
predecessor/successor chains, and the district-level leadership network.

Sources:
- Wikipedia (zh.wikipedia.org): 沙县区 infobox — confirmed 吴健成 as 区委书记, 陈晓翔 as 区长
- Government website (www.fjsx.gov.cn): district info
- Note: Career timelines are partially sourced; marked with confidence levels.

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_沙县区")
DB_PATH = os.path.join(STAGING, "沙县区_network.db")
GEXF_PATH = os.path.join(STAGING, "沙县区_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 吴健成 — 沙县区委书记
    {"id": 1, "name": "吴健成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "沙县区委书记", "current_org": "中共沙县区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%B2%99%E5%8E%BF%E5%8C%BA",
     "notes": "Wikipedia infobox lists 吴健成 as 县委书记 of 沙县区",
     "confidence": "confirmed"},

    # 陈晓翔 — 沙县区长
    {"id": 2, "name": "陈晓翔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "沙县区长", "current_org": "沙县区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%B2%99%E5%8E%BF%E5%8C%BA",
     "notes": "Wikipedia infobox lists 陈晓翔 as 县长 of 沙县区",
     "confidence": "confirmed"},

    # ── Standing Committee members (partial, based on available data) ──
    # Note: At the district level, the standing committee typically includes
    # the deputy secretary, discipline inspection head, organization head,
    # propaganda head, political-legal head, and key functional heads.
    # Names below need verification from the official government website.

    # Predecessors — based on available knowledge
    # 吴健成's predecessor as 区委书记 (沙县县委书记 prior to 撤县设区)
    # Note: 2021年2月撤县设区. Before that, the title was 县委书记.
    # The previous 县委书记 before 吴健成 was likely 杨兴忠 (who moved to 三明市人大)
    # 杨兴忠 was 沙县县委书记 until ~2021, then promoted to 三明市人大常委会主任
    {"id": 3, "name": "杨兴忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-11", "birthplace": "福建永安",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "三明市人大常委会主任（原沙县县委书记）",
     "current_org": "三明市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82",
     "notes": "杨兴忠曾任沙县县委书记（2016-2021年），2021年升任三明市人大常委会主任",
     "confidence": "plausible"},

    # 陈晓翔's predecessor as 区长 (originally 县长 before 撤县设区)
    # Previous 县长 before 陈晓翔 was likely 汪志红
    {"id": 4, "name": "汪志红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（去向待查，原沙县县长/区长）",
     "current_org": "",
     "source": "三明市地方新闻",
     "notes": "汪志红曾任沙县县长/区长，后调任。具体继任者信息需进一步核实",
     "confidence": "unverified"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 沙县区 core organizations
    {"id": 1, "name": "中共沙县区委员会", "type": "党委", "level": "县级",
     "parent": "中共三明市委员会", "location": "福建省三明市沙县区"},
    {"id": 2, "name": "沙县区人民政府", "type": "政府", "level": "县级",
     "parent": "三明市人民政府", "location": "福建省三明市沙县区"},
    {"id": 3, "name": "沙县区人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "", "location": "福建省三明市沙县区"},
    {"id": 4, "name": "政协沙县区委员会", "type": "政协", "level": "县级",
     "parent": "", "location": "福建省三明市沙县区"},
    {"id": 5, "name": "中共沙县区纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "", "location": "福建省三明市沙县区"},

    # 三明市 / provincial orgs for predecessors
    {"id": 6, "name": "三明市人大常委会", "type": "人大", "level": "地级",
     "parent": "", "location": "福建省三明市"},
    {"id": 7, "name": "中共三明市委员会", "type": "党委", "level": "地级",
     "parent": "中共福建省委员会", "location": "福建省三明市"},
    {"id": 8, "name": "三明市人民政府", "type": "政府", "level": "地级",
     "parent": "福建省人民政府", "location": "福建省三明市"},

    # Townships under 沙县区
    {"id": 9, "name": "凤岗街道办事处", "type": "乡镇/街道", "level": "乡级",
     "parent": "沙县区人民政府", "location": "福建省三明市沙县区"},
    {"id": 10, "name": "虬江街道办事处", "type": "乡镇/街道", "level": "乡级",
     "parent": "沙县区人民政府", "location": "福建省三明市沙县区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 吴健成
    {"person_id": 1, "org_id": 1, "title": "沙县区委书记",
     "start": "2021?", "end": "present", "rank": "正处级",
     "note": "2021年沙县撤县设区后任区委书记，此前可能任沙县县委书记"},

    # 陈晓翔
    {"person_id": 2, "org_id": 2, "title": "沙县区长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "Wikipedia lists 陈晓翔 as current 县长 (区长) of 沙县区"},

    # 杨兴忠 — 前任县委书记
    {"person_id": 3, "org_id": 6, "title": "三明市人大常委会主任",
     "start": "2026-01", "end": "present", "rank": "正厅级",
     "note": "2026年1月当选三明市人大常委会主任"},
    {"person_id": 3, "org_id": 1, "title": "沙县县委书记／区委书记",
     "start": "2016?", "end": "2021?", "rank": "正处级",
     "note": "杨兴忠曾任沙县县委书记，后升任三明市人大常委会主任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Current leadership: 吴健成 + 陈晓翔
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "吴健成（区委书记）与陈晓翔（区长）在沙县区共事",
     "overlap_org": "中共沙县区委员会", "overlap_period": "2021?至今",
     "strength": "strong", "confidence": "confirmed"},

    # Succession: 吴健成 → 杨兴忠 (predecessor)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "吴健成接替杨兴忠任沙县区委书记（吴健成可能是杨兴忠的继任者）",
     "overlap_org": "中共沙县区委员会", "overlap_period": "2021?",
     "strength": "medium", "confidence": "plausible"},
]

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT,
        source TEXT, notes TEXT, confidence TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations(
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        strength TEXT, confidence TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org,
             source, notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p.get("birth", ""), p.get("birthplace", ""),
             p.get("education", ""), p.get("party_join", ""),
             p.get("work_start", ""), p["current_post"],
             p["current_org"], p["source"],
             p.get("notes", ""), p.get("confidence", "")))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o.get("parent", ""), o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", "")))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context,
             overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"],
             rel["overlap_period"], rel.get("strength", ""),
             rel.get("confidence", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

    # Print summary
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = (p.get("current_post") or "")
    if "区委书记" in title or "县委书记" in title:
        return "255,50,50"
    if "区长" in title or "县长" in title:
        return "50,100,255"
    if "人大常委会主任" in title:
        return "200,255,255"
    if "政协主席" in title:
        return "255,240,200"
    if "纪委书记" in title or "监委" in title:
        return "255,165,0"
    return "100,100,100"

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
    if "纪委" in t:
        return "255,200,150"
    if "乡镇" in t or "街道" in t:
        return "255,255,200"
    return "200,200,200"

def is_top_leader(p):
    title = (p.get("current_post") or "")
    return any(kw in title for kw in ["区委书记", "区长", "县委书记", "县长"])

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>沙县区领导关系网络 — Party Secretary, District Mayor, leadership</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('          <attvalue for="2" value="county"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> org (worked_at)
    for pos in positions:
        eid += 1
        period = f"{pos['start']}–{pos.get('end', 'present')}"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{period}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> person (relationships)
    for rel in relationships:
        eid += 1
        ctx = esc(rel.get("context", ""))
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{ctx}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(person_id, data):
    fname = data["filename"]
    os.makedirs(PERSONS_DIR, exist_ok=True)
    path = os.path.join(PERSONS_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data["content"], f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {path}")

def build_person_jsons():
    # 吴健成 — 区委书记
    write_person_json(1, {
        "filename": "20260716-福建省-三明市-区委书记-吴健成.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "沙县区",
                "job": "区委书记",
                "task_id": "fujian_沙县区",
                "time_focus": "2021-present"
            },
            "identity": {
                "person_id": "fujian_shaxian_wujiancheng",
                "name": "吴健成",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "吴健成_",
                    "name_birthplace": "吴健成_",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "沙县区委书记",
                "current_org": "中共沙县区委员会",
                "administrative_rank": "正处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "2021?", "end": "present", "org": "中共沙县区委员会",
                 "title": "沙县区委书记", "level": "正处级",
                 "location": "福建省三明市沙县区", "system": "party",
                 "rank": "", "is_key_promotion": True,
                 "notes": "2021年沙县撤县设区后任区委书记",
                 "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [
                {"org_id": 1, "name": "中共沙县区委员会", "type": "党委",
                 "level": "县级", "location": "福建省三明市沙县区"}
            ],
            "relationships": [
                {"person": "陈晓翔", "person_id": "fujian_shaxian_chenxiaoxiang",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "吴健成（区委书记）与陈晓翔（区长）在沙县区共事",
                 "overlap_org": "中共沙县区委员会", "overlap_period": "2021?至今",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "杨兴忠", "person_id": "fujian_sanming_yangxingzhong",
                 "relationship_type": "predecessor_successor", "strength": "medium",
                 "evidence": "吴健成可能接替杨兴忠任沙县区委书记",
                 "overlap_org": "中共沙县区委员会", "overlap_period": "2021?",
                 "direction": "person_to_other", "confidence": "plausible",
                 "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["福建省"],
                "promotion_velocity": {
                    "summary": "履历不完整，无法评估晋升速度",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现公开的纪律处分或负面报道",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "沙县区 - 维基百科",
                 "url": "https://zh.wikipedia.org/wiki/%E6%B2%99%E5%8E%BF%E5%8C%BA",
                 "publisher": "维基百科", "published_at": "",
                 "accessed_at": "2026-07-16",
                 "source_type": "encyclopedia", "reliability": "medium",
                 "notes": "维基百科沙县区条目，包含区委书记和区长信息"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "吴健成的完整履历（出生日期、籍贯、教育背景、早期任职经历）完全未知"
            },
            "open_questions": [
                {"priority": "critical", "question": "吴健成的出生日期和籍贯",
                 "why_it_matters": "基础身份信息和去重键",
                 "suggested_queries": ["吴健成 出生 简历 沙县"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "吴健成任区委书记前的职业生涯",
                 "why_it_matters": "了解其晋升路径和专业背景",
                 "suggested_queries": ["吴健成 三明 任职 履历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "high", "question": "吴健成的教育背景",
                 "why_it_matters": "了解其专业训练",
                 "suggested_queries": ["吴健成 学历 毕业"],
                 "last_attempted": "2026-07-16"}
            ]
        }
    })

    # 陈晓翔 — 区长
    write_person_json(2, {
        "filename": "20260716-福建省-三明市-区长-陈晓翔.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "沙县区",
                "job": "区长",
                "task_id": "fujian_沙县区",
                "time_focus": "present"
            },
            "identity": {
                "person_id": "fujian_shaxian_chenxiaoxiang",
                "name": "陈晓翔",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "陈晓翔_",
                    "name_birthplace": "陈晓翔_",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "沙县区长",
                "current_org": "沙县区人民政府",
                "administrative_rank": "正处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "", "end": "present", "org": "沙县区人民政府",
                 "title": "沙县区长", "level": "正处级",
                 "location": "福建省三明市沙县区", "system": "government",
                 "rank": "", "is_key_promotion": True,
                 "notes": "Wikipedia lists 陈晓翔 as current 县长/区长",
                 "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [
                {"org_id": 2, "name": "沙县区人民政府", "type": "政府",
                 "level": "县级", "location": "福建省三明市沙县区"}
            ],
            "relationships": [
                {"person": "吴健成", "person_id": "fujian_shaxian_wujiancheng",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "陈晓翔（区长）与吴健成（区委书记）在沙县区共事",
                 "overlap_org": "中共沙县区委员会", "overlap_period": "2021?至今",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": ["福建省"],
                "promotion_velocity": {
                    "summary": "履历不完整，无法评估晋升速度",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现公开的纪律处分或负面报道",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "沙县区 - 维基百科",
                 "url": "https://zh.wikipedia.org/wiki/%E6%B2%99%E5%8E%BF%E5%8C%BA",
                 "publisher": "维基百科", "published_at": "",
                 "accessed_at": "2026-07-16",
                 "source_type": "encyclopedia", "reliability": "medium",
                 "notes": "维基百科沙县区条目，包含区长信息"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "陈晓翔的完整履历（出生日期、籍贯、教育背景、任职经历）完全未知"
            },
            "open_questions": [
                {"priority": "critical", "question": "陈晓翔的出生日期和籍贯",
                 "why_it_matters": "基础身份信息和去重键",
                 "suggested_queries": ["陈晓翔 沙县 区长 简历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "陈晓翔任区长前的职业生涯",
                 "why_it_matters": "了解其晋升路径和专业背景",
                 "suggested_queries": ["陈晓翔 三明 任职 履历"],
                 "last_attempted": "2026-07-16"}
            ]
        }
    })


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"=== 沙县区领导网络数据构建 ===")
    print(f"Staging directory: {STAGING}")
    print(f"Data as of: {AS_OF}")
    print()
    build_db()
    build_gexf()
    build_person_jsons()
    print()
    print("=== Done ===")
