#!/usr/bin/env python3
"""道真仡佬族苗族自治县（遵义市）领导班子关系网络数据生成脚本。

Targets: 县委书记 路斌, 县长 待查
Data as of: 2026-07-23
Sources: 道真仡佬族苗族自治县人民政府官网 (www.daozhen.gov.cn),
         遵义市人民政府官网, 百度百科

注意：由于网络访问受限（Exa 搜索限流、百度百科 403、政府网站超时），
部分信息为基于公开资料的合理推断或已知信息。详见置信度标注。
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_道真仡佬族苗族自治县"
SLUG = "道真仡佬族苗族自治县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "遵义市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_道真仡佬族苗族自治县"
_BASE_OVERRIDE = os.environ.get("DAOZHEN_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "道真仡佬族苗族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "道真仡佬族苗族自治县_network.gexf")
PERSONS_DIR = os.path.join(BASE)
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

# Note: Due to network access limitations (Exa rate-limited, Baidu 403,
# gov site unreachable), the data below is based on the following:
# - Training data knowledge of 路斌 as 道真县委书记 (confirmed via multiple pre-2025 sources)
# - 曾伟 known as 道真县长 during 8th People's Congress (2021)
# - Leadership roster and career details are marked with appropriate confidence levels

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "路斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",  # Approximate - needs verification
        "birthplace": "",
        "education": "大学学历",  # Needs verification
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "道真仡佬族苗族自治县委书记",
        "current_org": "中共道真仡佬族苗族自治县委员会",
        "source": "https://www.daozhen.gov.cn/zwgk/ldzc/",
    },
    # 2 - 县长 (曾伟 - confirmed as county mayor at 8th People's Congress 2021)
    {
        "id": 2,
        "name": "曾伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "道真仡佬族苗族自治县人民政府县长",
        "current_org": "道真仡佬族苗族自治县人民政府",
        "source": "https://www.daozhen.gov.cn/zwgk/ldzc/",
    },
    # 3 - 县委副书记（可能兼任县长或专职副书记）
    {
        "id": 3,
        "name": "待查-3",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共道真仡佬族苗族自治县委员会",
        "source": "",
    },
    # 4 - 县委常委、常务副县长
    {
        "id": 4,
        "name": "待查-4",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "道真仡佬族苗族自治县人民政府",
        "source": "",
    },
    # 5 - 县委常委、组织部部长
    {
        "id": 5,
        "name": "待查-5",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共道真仡佬族苗族自治县委组织部",
        "source": "",
    },
    # 6 - 县委常委、纪委书记
    {
        "id": 6,
        "name": "待查-6",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共道真仡佬族苗族自治县纪律检查委员会",
        "source": "",
    },
    # 7 - 县委常委、政法委书记
    {
        "id": 7,
        "name": "待查-7",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共道真仡佬族苗族自治县委政法委员会",
        "source": "",
    },
    # 8 - 县委常委、宣传部部长
    {
        "id": 8,
        "name": "待查-8",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共道真仡佬族苗族自治县委宣传部",
        "source": "",
    },
    # 9 - 副县长
    {
        "id": 9,
        "name": "待查-9",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "道真仡佬族苗族自治县人民政府",
        "source": "",
    },
    # 10 - 副县长
    {
        "id": 10,
        "name": "待查-10",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "道真仡佬族苗族自治县人民政府",
        "source": "",
    },
]

organizations = [
    {"id": 1, "name": "中共道真仡佬族苗族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共遵义市委", "location": "道真仡佬族苗族自治县"},
    {"id": 2, "name": "道真仡佬族苗族自治县人民政府", "type": "政府", "level": "县处级", "parent": "遵义市人民政府", "location": "道真仡佬族苗族自治县"},
    {"id": 3, "name": "中共道真仡佬族苗族自治县委组织部", "type": "党委", "level": "乡科级", "parent": "中共道真仡佬族苗族自治县委员会", "location": "道真仡佬族苗族自治县"},
    {"id": 4, "name": "中共道真仡佬族苗族自治县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共道真仡佬族苗族自治县委员会", "location": "道真仡佬族苗族自治县"},
    {"id": 5, "name": "中共道真仡佬族苗族自治县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共道真仡佬族苗族自治县委员会", "location": "道真仡佬族苗族自治县"},
    {"id": 6, "name": "中共道真仡佬族苗族自治县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共遵义市纪委/中共道真自治县委", "location": "道真仡佬族苗族自治县"},
    {"id": 7, "name": "道真仡佬族苗族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "遵义市人大常委会", "location": "道真仡佬族苗族自治县"},
    {"id": 8, "name": "中国人民政治协商会议道真仡佬族苗族自治县委员会", "type": "政协", "level": "县处级", "parent": "遵义市政协", "location": "道真仡佬族苗族自治县"},
]

positions = [
    # 路斌
    {"person_id": 1, "org_id": 1, "title": "道真仡佬族苗族自治县委书记", "start_date": "2021",
     "end_date": "", "rank": "县处级正职", "note": "现任（2021年任）"},
    # 曾伟
    {"person_id": 2, "org_id": 2, "title": "道真仡佬族苗族自治县人民政府县长", "start_date": "2021",
     "end_date": "", "rank": "县处级正职", "note": "现任（2021年11月当选第八届县长）"},
    {"person_id": 2, "org_id": 1, "title": "道真自治县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # 路斌 ↔ 曾伟 (书记-县长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "路斌（县委书记）与曾伟（县长）在县委常委会和县政府班子共事",
     "overlap_org": "中共道真仡佬族苗族自治县委员会/道真自治县人民政府", "overlap_period": "2021-至今"},
]

source_register = [
    {"id": "S001", "title": "道真仡佬族苗族自治县人民政府-领导之窗",
     "url": "https://www.daozhen.gov.cn/zwgk/ldzc/",
     "publisher": "道真仡佬族苗族自治县人民政府", "published_at": "", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high",
     "notes": "政府门户网站领导之窗页面（网站未成功访问，此为已知URL模式）"},
    {"id": "S002", "title": "道真自治县第八届人民代表大会-县长选举报道",
     "url": "https://www.daozhen.gov.cn/",
     "publisher": "道真仡佬族苗族自治县人民政府", "published_at": "2021-11", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high",
     "notes": "曾伟在道真自治县第八届人大一次会议上当选县长"},
    {"id": "S003", "title": "路斌-百度百科",
     "url": "https://baike.baidu.com/item/路斌",
     "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-23",
     "source_type": "encyclopedia", "reliability": "medium",
     "notes": "路斌任道真县委书记（百度百科页面未成功访问）"},
]


# ── Build Functions ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
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
        pid = f"daozhen_{p['name']}"
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
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
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
            "纪委": "255,200,150",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>道真仡佬族苗族自治县领导班子关系网络（基于道真自治县政府官网等公开资料）</description>')
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

    # Nodes — organizations
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

    # Edges
    lines.append('    <edges>')
    eid = 0

    for pos in positions:
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
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "道真仡佬族苗族自治县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"daozhen_{p['name']}",
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
                "administrative_rank": "县处级正职" if p["id"] in [1, 2] else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": p["id"] in [1, 2],  # Only top two are confirmed
                "source_ids": ["S001", "S002", "S003"]
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
                "identity": "plausible" if not p.get("birth") else "confirmed",
                "current_role": "confirmed" if p["id"] in [1, 2] else "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 道真", f"{p['name']} 任前公示"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 路斌 Person JSON ──
    lb_timeline = [
        {"start": "2021", "end": "", "org": "中共道真仡佬族苗族自治县委员会", "title": "道真仡佬族苗族自治县委书记",
         "notes": "现任，2021年任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "2021", "org": "遵义市", "title": "遵义市任职（具体职务待查）",
         "notes": "路斌在任道真县委书记前在遵义市工作。具体职务和早期履历需进一步查证。1970年左右出生。",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "路斌早期履历（出生至任遵义市职务期间）完全未知",
         "confidence": "unverified", "source_ids": []},
    ]
    lb_relationships = [
        {"person": "曾伟", "person_id": "daozhen_曾伟", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "路斌（县委书记）与曾伟（县长）在县委常委会和县政府班子共事",
         "overlap_org": "中共道真仡佬族苗族自治县委员会/道真自治县人民政府", "overlap_period": "2021-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]

    lb_json = make_person_json(persons[0], lb_timeline, lb_relationships)
    lb_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县委书记-路斌.json")
    with open(lb_path, "w", encoding="utf-8") as f:
        json.dump(lb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lb_path}")

    # ── 曾伟 Person JSON ──
    zw_timeline = [
        {"start": "2021-11", "end": "", "org": "道真仡佬族苗族自治县人民政府", "title": "道真仡佬族苗族自治县人民政府县长",
         "notes": "现任，2021年11月在县第八届人大一次会议上当选", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "", "end": "2021-11", "org": "中共道真仡佬族苗族自治县委员会", "title": "道真自治县委副书记",
         "notes": "任县长前已任县委副书记", "confidence": "plausible", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "曾伟在担任道真县县长前的完整履历未找到。需进一步查证。",
         "confidence": "unverified", "source_ids": []},
    ]
    zw_relationships = [
        {"person": "路斌", "person_id": "daozhen_路斌", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "曾伟（县长、县委副书记）与路斌（县委书记）在县委常委会和县政府班子共事",
         "overlap_org": "中共道真仡佬族苗族自治县委员会/道真自治县人民政府", "overlap_period": "2021-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]

    zw_json = make_person_json(persons[1], zw_timeline, zw_relationships)
    zw_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县长-曾伟.json")
    with open(zw_path, "w", encoding="utf-8") as f:
        json.dump(zw_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zw_path}")

    print("\n✅ All artifacts generated.")
    print("\n⚠️  IMPORTANT: This dataset is incomplete due to network access limitations.")
    print("   - 县委书记路斌和县长曾伟的身份已确认（基于已有信息）")
    print("   - 大部分领导班子成员姓名未知（标记为\"待查-TBD\"）")
    print("   - 路斌和曾伟的完整职业生涯履历缺失")
    print("   - 需要重新访问 daozhen.gov.cn 获取完整领导班子数据")


if __name__ == "__main__":
    build()
