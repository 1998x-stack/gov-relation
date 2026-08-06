#!/usr/bin/env python3
"""Build script for 锦州市古塔区 cadre exchange network investigation.

targets: 古塔区委书记（一把手）焦健 / 古塔区区长（二把手）张相龙
Sources: official 古塔区政府网 (jzgtq.gov.cn) 分工通知 + 任前公示 + 政府新闻.
"""

import json
import os
import sqlite3

AS_OF = "2026-08-06"
AS_OF_SHORT = AS_OF.replace("-", "")

# Paths — this script lives in data/tmp/liaoning_古塔区/, so stage there directly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "古塔区_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "古塔区_network.gexf")
PERSONS_DIR = os.path.join(BASE_DIR, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

persons = [
    {"id": 1, "name": "焦健", "gender": "男", "ethnicity": "汉族", "birth": "1970-04",
     "birthplace": "", "education": "在职大学学历", "party_join": "1994-06", "work_start": "1992-08",
     "current_post": "古塔区委书记", "current_org": "中共锦州市古塔区委员会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 2, "name": "张相龙", "gender": "男", "ethnicity": "汉族", "birth": "1980-01",
     "birthplace": "", "education": "大学学历,学士学位", "party_join": "2000-10", "work_start": "2002-07",
     "current_post": "古塔区委副书记、区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1054/12444.htm"},
    {"id": 3, "name": "王肖肖", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委常委、常务副区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1140/11251.htm"},
    {"id": 4, "name": "刘佳伟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委常委、副区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1054/12444.htm"},
    {"id": 5, "name": "李占一", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区副区长兼公安古塔分局局长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1140/11251.htm"},
    {"id": 6, "name": "韩志强", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区副区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1140/11251.htm"},
    {"id": 7, "name": "杨海", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区副区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1140/11251.htm"},
    {"id": 8, "name": "张晶晶", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区副区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 9, "name": "郭鹏宇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委常委、副区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 10, "name": "朱洪", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委常委、政法委书记", "current_org": "中共锦州市古塔区委员会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 11, "name": "李连秋", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委常委、宣传部部长", "current_org": "中共锦州市古塔区委员会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 12, "name": "伊昕阳", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委副书记", "current_org": "中共锦州市古塔区委员会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 13, "name": "高亮", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区委办主任", "current_org": "中共锦州市古塔区委员会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 14, "name": "江秀海", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区人大常委会主任", "current_org": "古塔区人大常委会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 15, "name": "方震", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区政协主席", "current_org": "政协古塔区委员会",
     "source": "http://www.jzgtq.gov.cn/"},
    {"id": 16, "name": "尤源", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区前任区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1026/8436.htm"},
    {"id": 17, "name": "刘占禄", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "古塔区前任区长", "current_org": "古塔区人民政府",
     "source": "http://www.jzgtq.gov.cn/info/1024/1212.htm"},
]

organizations = [
    {"id": 1, "name": "中共锦州市古塔区委员会", "type": "党委", "level": "县处级", "parent": "中共锦州市委员会", "location": "锦州市古塔区"},
    {"id": 2, "name": "古塔区人民政府", "type": "政府", "level": "县处级", "parent": "锦州市人民政府", "location": "锦州市古塔区"},
    {"id": 3, "name": "古塔区人大常委会", "type": "人大", "level": "县处级", "parent": "锦州市人大常委会", "location": "锦州市古塔区"},
    {"id": 4, "name": "政协古塔区委员会", "type": "政协", "level": "县处级", "parent": "政协锦州市委员会", "location": "锦州市古塔区"},
    {"id": 5, "name": "锦州市人民政府办公室", "type": "政府", "level": "县处级", "parent": "锦州市人民政府", "location": "锦州市"},
    {"id": 6, "name": "锦州市公安局古塔分局", "type": "政府", "level": "乡科级", "parent": "锦州市公安局", "location": "锦州市古塔区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "古塔区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任古塔区委书记"},
    {"person_id": 2, "org_id": 1, "title": "古塔区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "古塔区区长", "start_date": "2025", "end_date": "present", "rank": "县处级正职",
     "note": "原任锦州市人民政府办公室综合九科科长，后任古塔区区长（2026-07官方分工通知确认在任）"},
    {"person_id": 2, "org_id": 5, "title": "锦州市人民政府办公室综合九科科长", "start_date": "", "end_date": "", "rank": "乡科级正职",
     "note": "任前公示原任职务"},
    {"person_id": 3, "org_id": 1, "title": "古塔区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "古塔区常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责区政府常务工作及发改、财税、金融、人社、应急等"},
    {"person_id": 4, "org_id": 1, "title": "古塔区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "古塔区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责农业、工业、科技、营商环境、数字经济等"},
    {"person_id": 5, "org_id": 2, "title": "古塔区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法"},
    {"person_id": 5, "org_id": 6, "title": "锦州市公安局古塔分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": "兼任区公安分局党委书记"},
    {"person_id": 6, "org_id": 2, "title": "古塔区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责住建、城管、文旅、招商、外贸"},
    {"person_id": 7, "org_id": 2, "title": "古塔区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责民政、市场监管、退役军人、民族宗教"},
    {"person_id": 8, "org_id": 2, "title": "古塔区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责教育、卫生健康"},
    {"person_id": 9, "org_id": 1, "title": "古塔区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "古塔区副区长（曾任常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "此前曾负责区政府常务工作"},
    {"person_id": 10, "org_id": 1, "title": "古塔区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "古塔区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "古塔区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "古塔区委办主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "古塔区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "古塔区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "古塔区区长（前任）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "曾任区长，后由张相龙接任"},
    {"person_id": 17, "org_id": 2, "title": "古塔区区长（更早前任）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "更早时期任区长"},
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "焦健（区委书记）与张相龙（区委副书记、区长）组成现任古塔区党政正职搭档",
     "overlap_org": "古塔区党政班子", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 16, "type": "前任搭档",
     "context": "焦健与前任区长尤源在此前时期组成党政正职搭档",
     "overlap_org": "古塔区党政班子", "overlap_period": "2024-2025"},
    {"person_a": 2, "person_b": 16, "type": "继承关系",
     "context": "张相龙接任尤源的区长职务，为区长职务的继任者",
     "overlap_org": "古塔区人民政府", "overlap_period": "2025"},
    {"person_a": 2, "person_b": 17, "type": "继承关系",
     "context": "张相龙为刘占禄、尤源之后的最新一任区长",
     "overlap_org": "古塔区人民政府", "overlap_period": "2025"},
    {"person_a": 3, "person_b": 9, "type": "职务交替",
     "context": "郭鹏宇曾任常务副区长，其后由王肖肖任常务副区长",
     "overlap_org": "古塔区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 3, "type": "同僚",
     "context": "刘佳伟与王肖肖同为区政府班子成员（副区长/常务副区长）",
     "overlap_org": "古塔区人民政府", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "焦健与政法委书记朱洪同在区委班子，曾在公安交流活动同台",
     "overlap_org": "古塔区区委班子", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级",
     "context": "焦健与区委常委、副区长郭鹏宇在区委班子共事",
     "overlap_org": "古塔区区委班子", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "同僚",
     "context": "张相龙与伊昕阳同为古属区委副书记",
     "overlap_org": "古塔区区委班子", "overlap_period": "至今"},
    {"person_a": 14, "person_b": 15, "type": "同届班子",
     "context": "江秀海（区人大主任）与方震（区政协主席）会同区委领导出席区妇代会",
     "overlap_org": "古塔区区级班子", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "同僚",
     "context": "李占一与韩志强同任古塔区副区长（区人民政府班子成员）",
     "overlap_org": "古塔区人民政府", "overlap_period": "至今"},
]


# ── Core figure persona data (confirmable bios) ──
CORE_BIOS = {
    "焦健": {
        "current_confirmed": True, "career_pattern": "local_ladder",
        "identity_note": "男，汉族，1970年4月出生，1992年8月参加工作，1994年6月加入中国共产党，在职大学学历。",
        "basis": ["S003"],
    },
    "张相龙": {
        "current_confirmed": True, "career_pattern": "cross_county_rotation",
        "identity_note": "男，汉族，1980年1月生，2002年7月参加工作，2000年10月加入中国共产党，大学学历，学士学位。原任锦州市人民政府办公室综合九科科长。",
        "basis": ["S004"],
    },
}


def make_person_json(person, timeline, relationship_items, source_items):
    bio = CORE_BIOS.get(person["name"], {})
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "锦州市", "region": "古塔区",
            "job": person.get("current_post", ""), "task_id": "liaoning_古塔区", "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"guta_{person['name']}", "name": person["name"], "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "", "education": [{"degree": person.get("education", "")}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""), "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级", "as_of": AS_OF,
            "is_current_confirmed": bio.get("current_confirmed", False),
            "source_ids": bio.get("basis", ["S001"])
        },
        "career_timeline": timeline,
        "organizations": [], "relationships": relationship_items,
        "governance_record": [], "professional_profile": {
            "primary_specializations": [], "career_pattern": bio.get("career_pattern", "unknown"),
            "systems_experience": [], "geographic_pattern": []
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "本调查未检索到针对焦健、张相龙等核心领导的公开负面处置/纪律审查信息",
             "date": AS_OF, "confidence": "plausible", "source_ids": []}
        ],
        "source_register": source_items,
        "open_questions": [
            {"priority": "critical", "question": f"Complete career timeline before current role for {person['name']}",
             "why_it_matters": "为评估晋升路径与关系网络需要早期履历",
             "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任职经历"], "last_attempted": AS_OF}
        ]
    }


def build():
    os.makedirs(BASE_DIR, exist_ok=True)
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
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
            level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
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
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))
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
    gexf_lines.append('    <description>锦州市古塔区领导班子关系网络（市辖区干部配置）</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        if "区委书记" in post and "副" not in post:
            color = "200,30,30"
        elif "区长" in post and "副" not in post:
            color = "30,100,200"
        elif "纪委" in post:
            color = "255,165,0"
        else:
            color = "100,100,100"
        size = "20.0" if ("区委书记" in post or "区长" in post) else "12.0"
        shape = "square" if "区委书记" in post else ("circle" if "区长" in post else "triangle")
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
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        color_map = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
                     "政协": "255,240,200", "纪委": "255,200,150", "国企": "200,255,200"}
        ocolor = color_map.get(otype, "200,200,200")
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
    gexf_lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
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
    source_register = [
        {"id": "S001", "title": "古塔区政府领导同志工作分工通知",
         "url": "http://www.jzgtq.gov.cn/info/1140/11251.htm", "publisher": "古塔区人民政府",
         "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S002", "title": "张相龙带队深入敬业街道开展调研座谈",
         "url": "http://www.jzgtq.gov.cn/info/1054/12444.htm", "publisher": "古塔区人民政府",
         "published_at": "2026-07-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S003", "title": "焦健简历（任前公示/百科）",
         "url": "https://baike.baidu.com/", "publisher": "百度百科", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium", "notes": "男1970-04/1992-08参加工作/1994-06入党/在职大学"},
        {"id": "S004", "title": "张相龙任前公示（原市政府办综九科科长→古塔区长）",
         "url": "http://www.jzgtq.gov.cn/", "publisher": "锦州市委组织部（公示）", "accessed_at": AS_OF,
         "source_type": "appointment_notice", "reliability": "high", "notes": "1980-01生/2002-07参加工作/2000-10入党"},
        {"id": "S005", "title": "古塔区妇代会报道（人大主任江秀海、政协主席方震、区委副书记伊昕阳、副区长张晶晶）",
         "url": "http://www.jzgtq.gov.cn/", "publisher": "古塔区人民政府", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "medium"},
        {"id": "S006", "title": "区委书记焦健/区长尤源/郭鹏宇/朱洪 出席公安交流（早期报道）",
         "url": "http://gaj.jz.gov.cn/", "publisher": "锦州市公安局", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "medium"},
        {"id": "S007", "title": "北京丹东企业商会接待张相龙（区委副书记、区长）",
         "url": "http://mp.weixin.qq.com/", "publisher": "北京丹东企业商会", "published_at": "2025-08-03",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "medium"},
    ]
    core_names = ["焦健", "张相龙", "尤源", "王肖肖", "郭鹏宇"]
    for p in persons:
        if p["name"] not in core_names:
            continue
        rels = []
        for r in relationships:
            if r["person_a"] == p["id"]:
                other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
                rels.append({"person": other, "person_id": f"guta_{other}", "relationship_type": r["type"],
                             "strength": "strong", "evidence": r["context"],
                             "overlap_org": r.get("overlap_org", ""), "overlap_period": r.get("overlap_period", ""),
                             "direction": "undirected", "confidence": "confirmed"})
            elif r["person_b"] == p["id"]:
                other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
                rels.append({"person": other, "person_id": f"guta_{other}", "relationship_type": r["type"],
                             "strength": "strong", "evidence": r["context"],
                             "overlap_org": r.get("overlap_org", ""), "overlap_period": r.get("overlap_period", ""),
                             "direction": "undirected", "confidence": "confirmed"})
        post = p["current_post"].replace("、", "_").replace("（", "_").replace("）", "_")
        fname = f"{AS_OF_SHORT}-辽宁省-锦州市-{post}-{p['name']}.json"
        if p["name"] == "焦健":
            # Build a proper career timeline for the core secretary
            timeline = [
                {"start": "unknown", "end": "unknown", "org": "古塔区委员会（区委）", "title": "区委书记", "rank": "县处级正职",
                 "location": "辽宁省锦州市古塔区", "system": "party", "notes": "现任区委书记（proven by official reporting）", "confidence": "confirmed", "source_ids": ["S003", "S001"]},
                {"start": "1992-08", "end": "unknown", "org": "辽宁省", "title": "干部", "rank": "",
                 "location": "辽宁省", "system": "party", "notes": "1992年8月参加工作，早期履历公开有限", "confidence": "plausible", "source_ids": ["S003"]},
            ]
        elif p["name"] == "张相龙":
            timeline = [
                {"start": "", "end": "present", "org": "古塔区人民政府", "title": "区长", "rank": "县处级正职",
                 "location": "辽宁省锦州市古塔区", "system": "government", "notes": "现任区长", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "", "end": "", "org": "锦州市人民政府办公室", "title": "综合科科长", "rank": "乡科级正职",
                 "location": "辽宁省锦州市", "system": "government", "notes": "任前公示原任职务", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "2002-07", "end": "unknown", "org": "辽宁省", "title": "干部", "rank": "",
                 "location": "辽宁省", "system": "government", "notes": "2002年7月参加工作", "confidence": "plausible", "source_ids": ["S004"]},
            ]
        else:
            timeline = [{"start": "unknown", "end": "unknown", "org": "古塔区", "title": "领导干部", "rank": "",
                         "notes": "早期履历待补充", "confidence": "unverified", "source_ids": []}]
        pjson = make_person_json(p, timeline, rels, source_register)
        p_path = os.path.join(PERSONS_DIR, fname)
        with open(p_path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {p_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()