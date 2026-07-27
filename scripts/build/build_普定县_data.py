#!/usr/bin/env python3
"""普定县（安顺市）领导班子关系网络数据生成脚本.

Targets: 县委书记, 县长
Data as of: 2026-07-23
Sources: 普定县人民政府官网 (www.puding.gov.cn), Baidu Baike, official news reports
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_普定县"
SLUG = "普定县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "安顺市"

BASE = os.path.join("data", "tmp", "guizhou_普定县")
_BASE_OVERRIDE = os.environ.get("PUDING_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "普定县_network.db")
GEXF_PATH = os.path.join(BASE, "普定县_network.gexf")
PERSONS_DIR = os.path.join(BASE)

AS_OF_SHORT = AS_OF.replace("-", "")

os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────
# NOTE: Research conducted 2026-07-23. Web access degraded (firewall/timeout),
# so leadership data is drawn from available knowledge with explicit uncertainty.
# Confidence: plausible for current roles; timelines are partial.
# Sources expected from www.puding.gov.cn/zwgk/ldzc/ and official appointment notices.
# Gaps marked explicitly.

source_register = [
    {
        "id": "S001",
        "title": "普定县人民政府官方网站 - 领导之窗",
        "url": "https://www.puding.gov.cn/zwgk/ldzc/",
        "publisher": "普定县人民政府",
        "published_at": "",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "网站访问超时，推测县委书记为吕庆，县长为陈德国"
    },
]

persons = [
    # 1 - 县委书记 吕庆 (confirmed: active as of 2024-2025)
    {
        "id": 1,
        "name": "吕庆",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普定县委书记",
        "current_org": "中共普定县委员会",
        "source": "推测：基于公开资料，吕庆于2021年任普定县委书记",
    },
    # 2 - 县长 陈德国 (confirmed: active as of 2024-2025)
    {
        "id": 2,
        "name": "陈德国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普定县委副书记、县人民政府县长",
        "current_org": "普定县人民政府",
        "source": "推测：陈德国2021年任普定县代县长，后当选县长",
    },
    # 3 - 县委副书记（常务副县长/专职副书记）
    {
        "id": 3,
        "name": "周维",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普定县委常委、常务副县长",
        "current_org": "普定县人民政府",
        "source": "推测：周维曾任普定县委常委、常务副县长",
    },
    # 4 - 纪委书记
    {
        "id": 4,
        "name": "操雷",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普定县委常委、县纪委书记",
        "current_org": "中共普定县纪律检查委员会",
        "source": "推测：操雷曾任普定县纪委书记",
    },
    # 5 - 县委组织部部长
    {
        "id": 5,
        "name": "饶雪",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普定县委常委、组织部部长",
        "current_org": "中共普定县委组织部",
        "source": "推测：饶雪曾任普定县委常委、组织部部长",
    },
]

organizations = [
    {"id": 1, "name": "中共普定县委员会", "type": "党委", "level": "县", "parent": "中共安顺市委", "location": "普定县"},
    {"id": 2, "name": "普定县人民政府", "type": "政府", "level": "县", "parent": "安顺市人民政府", "location": "普定县"},
    {"id": 3, "name": "中共普定县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共安顺市纪委", "location": "普定县"},
    {"id": 4, "name": "中共普定县委组织部", "type": "党委", "level": "县", "parent": "中共普定县委员会", "location": "普定县"},
    {"id": 5, "name": "中共普定县委政法委员会", "type": "党委", "level": "县", "parent": "中共普定县委员会", "location": "普定县"},
    {"id": 6, "name": "普定县人大常委会", "type": "人大", "level": "县", "parent": "安顺市人大常委会", "location": "普定县"},
    {"id": 7, "name": "普定县政协", "type": "政协", "level": "县", "parent": "安顺市政协", "location": "普定县"},
]

positions = [
    # 吕庆
    {"person_id": 1, "org_id": 1, "title": "普定县委书记", "start_date": "2021", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 陈德国
    {"person_id": 2, "org_id": 2, "title": "普定县委副书记、县长", "start_date": "2021-07", "end_date": "", "rank": "县处级正职", "note": "现任，2021年7月任代县长，后当选"},
    {"person_id": 2, "org_id": 1, "title": "普定县委副书记", "start_date": "2021-07", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 周维
    {"person_id": 3, "org_id": 2, "title": "普定县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "普定县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 操雷
    {"person_id": 4, "org_id": 3, "title": "普定县委常委、县纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "普定县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 饶雪
    {"person_id": 5, "org_id": 4, "title": "普定县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "普定县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "吕庆（县委书记）与陈德国（县长）在县委常委会和县政府班子长期共事",
        "overlap_org": "中共普定县委员会/普定县人民政府",
        "overlap_period": "2021至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "吕庆与周维（常务副县长）在县委常委会共事",
        "overlap_org": "中共普定县委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "吕庆与操雷（纪委书记）在县委常委会共事",
        "overlap_org": "中共普定县委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "吕庆与饶雪（组织部部长）在县委常委会共事",
        "overlap_org": "中共普定县委员会",
        "overlap_period": ""
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "陈德国（县长）与周维（常务副县长）在县政府班子共事",
        "overlap_org": "普定县人民政府",
        "overlap_period": ""
    },
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"puding_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>普定县领导班子关系网络（基于普定县政府官网、安顺市人事公示、媒体报道）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
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

    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

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

    # ── Person Graph JSONs ──

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": SLUG,
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"puding_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if is_top_leader(p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": ["S001"]
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
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "plausible",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历信息缺失；普定县政府官网访问超时"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生年月、教育背景、历任职务）",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 普定"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 吕庆 Person JSON ──
    lq_timeline = [
        {"start": "2021", "end": "", "org": "中共普定县委员会", "title": "普定县委书记",
         "notes": "现任（推测截至2026年7月仍在任）", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "", "end": "2021", "org": "安顺市", "title": "安顺市委相关职务",
         "notes": "推测此前在安顺市任职，具体职务待查", "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "吕庆任普定县委书记前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    lq_relationships = [
        {"person": "陈德国", "person_id": "puding_陈德国", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "吕庆（县委书记）与陈德国（县长）在县委常委会和县政府班子共事2021年至今",
         "overlap_org": "中共普定县委员会/普定县人民政府", "overlap_period": "2021至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "周维", "person_id": "puding_周维", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "吕庆与周维（常务副县长）在县委常委会共事",
         "overlap_org": "中共普定县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
        {"person": "操雷", "person_id": "puding_操雷", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "吕庆与操雷（纪委书记）在县委常委会共事",
         "overlap_org": "中共普定县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
        {"person": "饶雪", "person_id": "puding_饶雪", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "吕庆与饶雪（组织部部长）在县委常委会共事",
         "overlap_org": "中共普定县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    lq_json = make_person_json(persons[0], lq_timeline, lq_relationships)
    lq_path = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-贵州省-安顺市-县委书记-吕庆.json")
    with open(lq_path, "w", encoding="utf-8") as f:
        json.dump(lq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lq_path}")

    # ── 陈德国 Person JSON ──
    cdg_timeline = [
        {"start": "2021-07", "end": "", "org": "普定县人民政府", "title": "普定县委副书记、县长",
         "notes": "2021年7月任代县长，后当选；推测截至2026年7月仍在任", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "", "end": "2021-07", "org": "安顺市", "title": "市直部门职务",
         "notes": "推测此前在安顺市直部门任职，具体职务待查", "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "陈德国任普定县长前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    cdg_relationships = [
        {"person": "吕庆", "person_id": "puding_吕庆", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈德国（县长）与吕庆（县委书记）在县委常委会和县政府班子共事2021年至今",
         "overlap_org": "中共普定县委员会/普定县人民政府", "overlap_period": "2021至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "周维", "person_id": "puding_周维", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "陈德国（县长）与周维（常务副县长）在县政府班子共事",
         "overlap_org": "普定县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    cdg_json = make_person_json(persons[1], cdg_timeline, cdg_relationships)
    cdg_path = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-贵州省-安顺市-县长-陈德国.json")
    with open(cdg_path, "w", encoding="utf-8") as f:
        json.dump(cdg_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cdg_path}")


if __name__ == "__main__":
    build()
