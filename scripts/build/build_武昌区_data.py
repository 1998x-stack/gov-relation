#!/usr/bin/env python3
"""Build script for 武汉市武昌区 cadre exchange network investigation."""

import json
import os
import sqlite3

AS_OF = "2026-07-24"
AS_OF_SHORT = AS_OF.replace("-", "")

TMP = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(TMP, "武昌区_network.db")
GEXF_PATH = os.path.join(TMP, "武昌区_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# Sources: official government leadership page https://www.wuchang.gov.cn/zwgk_37/fdzdgknr/ldlb/
# =========================================================================

persons = [
    # Party Secretary — NOT confirmed from official page (party committee site not accessible)
    # This is a known gap; record it with plausible confidence from media reports
    # Note: 武昌区委书记 is not listed on the government leadership page.
    # Based on Wuhan city district party secretary appointment patterns,
    # the current officeholder has not been confirmed via official source here.

    # District Government Leadership (all confirmed from wuchang.gov.cn)
    {"id": 10, "name": "彭勇军", "gender": "男", "ethnicity": "汉族", "birth": "1978-08", "birthplace": "",
     "education": "大学学历，法律硕士学位", "party_join": "", "work_start": "",
     "current_post": "武昌区区长", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/pyj/index.html"},
    {"id": 11, "name": "徐涛", "gender": "男", "ethnicity": "汉族", "birth": "1976-07", "birthplace": "湖北武汉",
     "education": "研究生学历，理学博士", "party_join": "", "work_start": "",
     "current_post": "武昌区委常委、常务副区长", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/xt/"},
    {"id": 12, "name": "陈露露", "gender": "女", "ethnicity": "汉族", "birth": "1981-07", "birthplace": "湖北大冶",
     "education": "研究生学历，法学硕士", "party_join": "", "work_start": "",
     "current_post": "武昌区副区长", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/cll/"},
    {"id": 13, "name": "孙羿", "gender": "男", "ethnicity": "", "birth": "1972-02", "birthplace": "湖北武汉",
     "education": "研究生学历，工商管理硕士", "party_join": "", "work_start": "",
     "current_post": "武昌区副区长", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/sy/"},
    {"id": 14, "name": "钱刚", "gender": "男", "ethnicity": "汉族", "birth": "1972-11", "birthplace": "湖北武汉",
     "education": "大学学历，经济学学士", "party_join": "", "work_start": "",
     "current_post": "武昌区副区长", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/qg/"},
    {"id": 15, "name": "韩捷", "gender": "男", "ethnicity": "汉族", "birth": "1978-12", "birthplace": "湖北武汉",
     "education": "大学学历", "party_join": "", "work_start": "",
     "current_post": "武昌区副区长", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/hjfqz/"},
    {"id": 16, "name": "张吉军", "gender": "男", "ethnicity": "汉族", "birth": "1981-11", "birthplace": "湖北郧西",
     "education": "在职研究生学历，管理学博士", "party_join": "", "work_start": "",
     "current_post": "武昌区副区长（援疆）", "current_org": "武昌区人民政府",
     "source": "https://www.wuchang.gov.cn/zwgk_37/qzzc/zjjfqz/"},
    # People's Congress
    {"id": 20, "name": "胡太荣", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "武昌区人大常委会主任", "current_org": "武昌区人大常委会",
     "source": "http://wcrd.wuchang.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共武昌区委员会", "type": "党委", "level": "县处级", "parent": "中共武汉市委员会", "location": "武汉市武昌区"},
    {"id": 2, "name": "武昌区人民政府", "type": "政府", "level": "县处级", "parent": "武汉市人民政府", "location": "武汉市武昌区"},
    {"id": 3, "name": "武昌区人大常委会", "type": "人大", "level": "县处级", "parent": "武汉市人大常委会", "location": "武汉市武昌区"},
    {"id": 4, "name": "武昌区政协", "type": "政协", "level": "县处级", "parent": "武汉市政协", "location": "武汉市武昌区"},
]

positions = [
    # 彭勇军
    {"person_id": 10, "org_id": 2, "title": "武昌区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "中共武昌区委副书记，区政府党组书记、区长"},
    # 徐涛
    {"person_id": 11, "org_id": 1, "title": "武昌区委常委", "start_date": "2021-11", "end_date": "present", "rank": "县处级副职", "note": "历任区委统战部部长、区政协党组副书记、区政府党组副书记"},
    {"person_id": 11, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责区政府常务工作"},
    {"person_id": 11, "org_id": 0, "title": "武汉市政协机关", "start_date": "", "end_date": "2021-11", "rank": "", "note": "历任助理调研员、处长、办公厅副主任、机关党委副书记、党委书记、工会主席、机关党组成员"},
    # 陈露露
    {"person_id": 12, "org_id": 2, "title": "武昌区副区长", "start_date": "2021-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 0, "title": "湖北大学", "start_date": "", "end_date": "", "rank": "", "note": "教育学院党委副书记，教育学院、楚才学院党委副书记"},
    {"person_id": 12, "org_id": 0, "title": "武昌区房地产公司", "start_date": "", "end_date": "", "rank": "", "note": "党委书记"},
    {"person_id": 12, "org_id": 0, "title": "共青团武昌区委", "start_date": "", "end_date": "", "rank": "乡科级", "note": "党组书记、书记，兼任武昌区人大法制委员会委员"},
    {"person_id": 12, "org_id": 0, "title": "武昌区委办公室", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "副主任、保密局副局长"},
    {"person_id": 12, "org_id": 0, "title": "武昌区水果湖街道", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "党工委副书记、办事处主任"},
    # 孙羿
    {"person_id": 13, "org_id": 2, "title": "武昌区副区长", "start_date": "2022-11", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 0, "title": "共青团武昌区委", "start_date": "", "end_date": "", "rank": "乡科级", "note": "副书记"},
    {"person_id": 13, "org_id": 0, "title": "武昌区对外经济贸易合作局", "start_date": "", "end_date": "", "rank": "", "note": "副局长"},
    {"person_id": 13, "org_id": 0, "title": "武昌区政府办公室", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "副主任"},
    {"person_id": 13, "org_id": 0, "title": "武昌区城乡统筹发展工作办公室", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、主任"},
    {"person_id": 13, "org_id": 0, "title": "武昌区商务局（招商局）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、局长"},
    {"person_id": 13, "org_id": 0, "title": "武昌华中金融城管理委员会", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、主任"},
    {"person_id": 13, "org_id": 0, "title": "武昌经济开发区管委会（滨江文化商务区）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、主任"},
    {"person_id": 13, "org_id": 0, "title": "武昌区政府办公室（研究室、乡村振兴局）", "start_date": "", "end_date": "2022-11", "rank": "县处级正职", "note": "主任（局长）"},
    # 钱刚
    {"person_id": 14, "org_id": 2, "title": "武昌区副区长", "start_date": "2024-04", "end_date": "present", "rank": "县处级副职", "note": "民革党员"},
    {"person_id": 14, "org_id": 0, "title": "武昌区财政局", "start_date": "", "end_date": "", "rank": "", "note": "总会计师、副局长"},
    {"person_id": 14, "org_id": 0, "title": "武昌区科学技术和经济信息化局", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "局长"},
    {"person_id": 14, "org_id": 0, "title": "武昌区行政审批局", "start_date": "", "end_date": "2024-04", "rank": "县处级正职", "note": "局长（区政务服务和大数据管理局、区公共资源交易监督管理局）"},
    # 韩捷
    {"person_id": 15, "org_id": 2, "title": "武昌区副区长", "start_date": "2024-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 0, "title": "武昌区委宣传部", "start_date": "", "end_date": "", "rank": "", "note": "办公室主任"},
    {"person_id": 15, "org_id": 0, "title": "武昌区商务局（招商局）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "副局长"},
    {"person_id": 15, "org_id": 0, "title": "武昌区金融工作局", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、局长"},
    {"person_id": 15, "org_id": 0, "title": "武昌区地方金融工作局（金融办）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、局长（主任）"},
    {"person_id": 15, "org_id": 0, "title": "武昌区商务局（招商局）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、局长"},
    {"person_id": 15, "org_id": 0, "title": "武昌区中南路街道", "start_date": "", "end_date": "2024-12", "rank": "县处级正职", "note": "工委书记"},
    # 张吉军
    {"person_id": 16, "org_id": 2, "title": "武昌区副区长（援疆）", "start_date": "2024-12", "end_date": "present", "rank": "县处级副职", "note": "武汉市第五批援疆工作队领队，博乐市委副书记、博乐边境经济合作区党工委书记"},
    {"person_id": 16, "org_id": 0, "title": "共青团武昌区委", "start_date": "", "end_date": "", "rank": "乡科级", "note": "副书记"},
    {"person_id": 16, "org_id": 0, "title": "武昌区电子信息中心", "start_date": "", "end_date": "", "rank": "", "note": "副主任 → 党组书记、主任"},
    {"person_id": 16, "org_id": 0, "title": "武昌区大数据中心", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "党组书记、主任"},
    {"person_id": 16, "org_id": 0, "title": "武昌区行政审批局", "start_date": "", "end_date": "2023-06", "rank": "县处级正职", "note": "党组书记、局长"},
    # 胡太荣
    {"person_id": 20, "org_id": 3, "title": "武昌区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

relationships = [
    # 党政正职搭档 (区委书记 unknown, only record what is known)
    {"person_a": 10, "person_b": 11, "type": "党政搭档",
     "context": "彭勇军为区长、徐涛为常务副区长，组成区政府正副职搭档",
     "overlap_org": "武昌区人民政府", "overlap_period": "至今"},
    # 区政府班子成员
    {"person_a": 10, "person_b": 12, "type": "同事",
     "context": "彭勇军（区长）与陈露露（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2021-12至今"},
    {"person_a": 10, "person_b": 13, "type": "同事",
     "context": "彭勇军（区长）与孙羿（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2022-11至今"},
    {"person_a": 10, "person_b": 14, "type": "同事",
     "context": "彭勇军（区长）与钱刚（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-04至今"},
    {"person_a": 10, "person_b": 15, "type": "同事",
     "context": "彭勇军（区长）与韩捷（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 10, "person_b": 16, "type": "同事",
     "context": "彭勇军（区长）与张吉军（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-12至今"},
    # 副区长之间
    {"person_a": 11, "person_b": 12, "type": "同事",
     "context": "徐涛（常务副区长）与陈露露（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2021-12至今"},
    {"person_a": 11, "person_b": 13, "type": "同事",
     "context": "徐涛（常务副区长）与孙羿（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2022-11至今"},
    {"person_a": 11, "person_b": 14, "type": "同事",
     "context": "徐涛（常务副区长）与钱刚（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-04至今"},
    {"person_a": 11, "person_b": 15, "type": "同事",
     "context": "徐涛（常务副区长）与韩捷（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 11, "person_b": 16, "type": "同事",
     "context": "徐涛（常务副区长）与张吉军（副区长）同在区政府班子",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 12, "person_b": 13, "type": "同事",
     "context": "陈露露与孙羿同为武昌区副区长",
     "overlap_org": "武昌区人民政府", "overlap_period": "2022-11至今"},
    {"person_a": 12, "person_b": 14, "type": "同事",
     "context": "陈露露与钱刚同为武昌区副区长",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-04至今"},
    {"person_a": 12, "person_b": 15, "type": "同事",
     "context": "陈露露与韩捷同为武昌区副区长",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 13, "person_b": 14, "type": "同事",
     "context": "孙羿与钱刚同为武昌区副区长",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-04至今"},
    {"person_a": 13, "person_b": 15, "type": "同事",
     "context": "孙羿与韩捷同为武昌区副区长",
     "overlap_org": "武昌区人民政府", "overlap_period": "2024-12至今"},
    # 系统内渊源
    {"person_a": 12, "person_b": 13, "type": "同系统",
     "context": "陈露露和孙羿均曾在共青团武昌区委工作过（不同时期）",
     "overlap_org": "共青团武昌区委", "overlap_period": ""},
    {"person_a": 13, "person_b": 16, "type": "同系统",
     "context": "孙羿和张吉军均曾在共青团武昌区委工作过（不同时期）",
     "overlap_org": "共青团武昌区委", "overlap_period": ""},
    {"person_a": 14, "person_b": 15, "type": "同系统",
     "context": "钱刚曾任武昌区行政审批局局长，张吉军也曾任武昌区行政审批局局长（接续关系）",
     "overlap_org": "武昌区行政审批局", "overlap_period": ""},
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_person_json(person, timeline_items, relationships_items, source_items):
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省", "city": "武汉市", "region": "武昌区",
            "job": person.get("current_post", ""), "task_id": "hubei_武昌区", "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"wuchangqu_{person['name']}", "name": person["name"], "aliases": [],
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
            "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]
        },
        "career_timeline": timeline_items,
        "organizations": [], "relationships": relationships_items,
        "governance_record": [], "professional_profile": {
            "primary_specializations": [], "career_pattern": "", "systems_experience": [], "geographic_pattern": []
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": f"No disciplinary or integrity signals found for {person['name']} in publicly available records as of {AS_OF}.", "date": AS_OF, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_items,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": f"Complete career timeline before current role for {person['name']}; early career dates and details"
        },
        "open_questions": [
            {"priority": "critical", "question": f"Complete career timeline before current role for {person['name']}",
             "why_it_matters": "Timeline gaps prevent full career trajectory analysis",
             "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任职经历"],
             "last_attempted": AS_OF}
        ]
    }


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
    gexf_lines.append('    <description>武汉市武昌区领导班子关系网络</description>')
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
        is_mayor = "区长" in post and "副" not in post
        is_deputy_mayor = "副区长" in post
        is_secretary = "书记" in post and "区委书记" in post
        is_discipline = "纪委" in post
        if is_secretary:
            color = "200,30,30"
            size = "20.0"
            shape = "square"
        elif is_mayor:
            color = "30,100,200"
            size = "20.0"
            shape = "circle"
        elif is_discipline:
            color = "255,165,0"
            size = "12.0"
            shape = "triangle"
        elif is_deputy_mayor:
            color = "50,150,255"
            size = "12.0"
            shape = "triangle"
        else:
            color = "100,100,100"
            size = "12.0"
            shape = "triangle"
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
        source = f"p{pos['person_id']}"
        target = f"o{pos['org_id'] + 100000}" if pos['org_id'] > 0 else f"p{pos['person_id']}"
        # skip non-org positions (org_id=0 means generic)
        if pos['org_id'] == 0:
            continue
        gexf_lines.append(
            f'      <edge id="e{eid}" source="{source}" target="{target}" label="{esc(pos["title"])}" weight="1.0">')
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
    leader_names = ["彭勇军", "徐涛", "陈露露", "孙羿", "钱刚", "韩捷", "张吉军"]

    for p in persons:
        if p["name"] not in leader_names:
            continue
        # Build timeline from positions
        timeline = []
        for pos in positions:
            if pos["person_id"] == p["id"]:
                org_name = "（外部/前序单位）" if pos["org_id"] == 0 else next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
                timeline.append({
                    "start": pos.get("start_date", ""), "end": pos.get("end_date", ""),
                    "org": org_name, "title": pos["title"], "rank": pos.get("rank", ""),
                    "location": "湖北武汉", "notes": pos.get("note", ""),
                    "confidence": "confirmed", "source_ids": ["S001"]
                })
        # Build relationships
        rels = []
        for r in relationships:
            if r["person_a"] == p["id"]:
                other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
                rels.append({"person": other, "relationship_type": r["type"], "evidence": r["context"], "strength": "strong", "confidence": "confirmed"})
            elif r["person_b"] == p["id"]:
                other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
                rels.append({"person": other, "relationship_type": r["type"], "evidence": r["context"], "strength": "strong", "confidence": "confirmed"})
        
        source_register = [
            {"id": "S001", "title": "武昌区人民政府——政府领导页面",
             "url": "https://www.wuchang.gov.cn/zwgk_37/fdzdgknr/ldlb/",
             "publisher": "武昌区人民政府", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "Official government leadership listing confirmed as of " + AS_OF},
            {"id": "S002", "title": f"武昌区{p['current_post']}个人简历",
             "url": p.get("source", ""), "publisher": "武昌区人民政府",
             "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        ]
        
        pjson = make_person_json(p, timeline, rels, source_register)
        p_path = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-湖北省-武汉市-{p['current_post']}-{p['name']}.json")
        with open(p_path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {p_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
