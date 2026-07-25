#!/usr/bin/env python3
"""Build script for 蒲城县 cadre exchange network investigation."""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-25"

# Paths
TMP = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(TMP, "蒲城县_network.db")
GEXF_PATH = os.path.join(TMP, "蒲城县_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

AS_OF_SHORT = AS_OF.replace("-", "")

# ── Persons ──
persons = [
    {"id": 1, "name": "薛斌", "gender": "男", "ethnicity": "汉", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委书记", "current_org": "中共蒲城县委员会",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 2, "name": "李少博", "gender": "男", "ethnicity": "汉", "birth": "1980-05", "birthplace": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "蒲城县县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/lsb/"},
    {"id": 18, "name": "张毅锋", "gender": "男", "ethnicity": "汉", "birth": "1970-03", "birthplace": "陕西华州",
     "education": "研究生", "party_join": "1992-04", "work_start": "1992-10",
     "current_post": "渭南市副市长", "current_org": "渭南市人民政府",
     "source": "https://baike.so.com/doc/5473645-5711494.html"},
    {"id": 3, "name": "李红伟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县人大常委会主任", "current_org": "蒲城县人大常委会",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 4, "name": "钟磊", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县政协主席", "current_org": "蒲城县政协",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 5, "name": "赵立朝", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委", "current_org": "中共蒲城县委员会",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 6, "name": "任武志", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委", "current_org": "中共蒲城县委员会",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 7, "name": "宋小娜", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委、副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 8, "name": "屈建宁", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委、副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 9, "name": "朱忠民", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委", "current_org": "中共蒲城县委员会",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 10, "name": "田雨", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委、副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 11, "name": "吕长江", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县委常委、副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html"},
    {"id": 12, "name": "吴永军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/"},
    {"id": 13, "name": "冯新", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/"},
    {"id": 14, "name": "上官腾飞", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/"},
    {"id": 15, "name": "高武国", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/"},
    {"id": 16, "name": "吴巍", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/"},
    {"id": 17, "name": "李杰", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "蒲城县副县长", "current_org": "蒲城县人民政府",
     "source": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共蒲城县委员会", "type": "党委", "level": "县处级", "parent": "中共渭南市委员会", "location": "蒲城县"},
    {"id": 2, "name": "蒲城县人民政府", "type": "政府", "level": "县处级", "parent": "渭南市人民政府", "location": "蒲城县"},
    {"id": 3, "name": "蒲城县人大常委会", "type": "人大", "level": "县处级", "parent": "渭南市人大常委会", "location": "蒲城县"},
    {"id": 4, "name": "蒲城县政协", "type": "政协", "level": "县处级", "parent": "渭南市政协", "location": "蒲城县"},
    {"id": 5, "name": "渭南市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "渭南市"},
    {"id": 6, "name": "渭南市纪委（监察局）", "type": "纪委", "level": "地厅级", "parent": "中共渭南市纪律检查委员会", "location": "渭南市"},
    {"id": 7, "name": "中共潼关县委员会", "type": "党委", "level": "县处级", "parent": "中共渭南市委员会", "location": "潼关县"},
    {"id": 8, "name": "陕西蒲城卤阳湖现代产业综合开发区", "type": "开发区", "level": "县处级", "parent": "渭南市人民政府", "location": "蒲城县"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "蒲城县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "蒲城县县长", "start_date": "2021-08", "end_date": "", "rank": "县处级正职", "note": "2021年8月被任命为蒲城县县长人选，后升任县委书记"},
    {"person_id": 2, "org_id": 1, "title": "蒲城县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "蒲城县县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作，分管财政局、审计局"},
    {"person_id": 3, "org_id": 3, "title": "蒲城县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "蒲城县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "蒲城县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "蒲城县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 前任县委书记张毅锋
    {"person_id": 18, "org_id": 5, "title": "渭南市副市长", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": "原蒲城县委书记，现任渭南市副市长"},
    {"person_id": 18, "org_id": 1, "title": "蒲城县委书记", "start_date": "2021-08", "end_date": "", "rank": "县处级正职", "note": "2021年8月被任命为蒲城县委书记"},
    {"person_id": 18, "org_id": 8, "title": "党工委书记", "start_date": "2021-08", "end_date": "", "rank": "县处级正职", "note": "兼任卤阳湖现代产业综合开发区党工委书记"},
    {"person_id": 18, "org_id": 2, "title": "蒲城县县长", "start_date": "2016-06", "end_date": "2021-08", "rank": "县处级正职", "note": "2016年6月任蒲城县委副书记、县长"},
    {"person_id": 18, "org_id": 7, "title": "潼关县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 7, "title": "潼关县委常委、纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 6, "title": "渭南市纪委办公室副主任、主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 6, "title": "渭南市纪委副科级、正科级纪检监察员", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "薛斌为县委书记、李少博为县长兼县委副书记，组成蒲城县党政正职搭档",
     "overlap_org": "蒲城县党政班子", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "同事",
     "context": "李少博（县长）与宋小娜（县委常委、副县长）同在县政府班子",
     "overlap_org": "蒲城县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "同事",
     "context": "李少博（县长）与吕长江（县委常委、副县长）同在县政府班子",
     "overlap_org": "蒲城县人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "同届领导",
     "context": "薛斌（县委书记）和李红伟（人大常委会主任）共同出席全县重要会议",
     "overlap_org": "蒲城县四套班子", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "同届领导",
     "context": "李少博（县长）与李红伟（人大常委会主任）共同在蒲城县任职",
     "overlap_org": "蒲城县四套班子", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "同事",
     "context": "赵立朝与任武志同为蒲城县委常委",
     "overlap_org": "中共蒲城县委员会", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 7, "type": "同事",
     "context": "赵立朝与宋小娜同为蒲城县委常委",
     "overlap_org": "中共蒲城县委员会", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 10, "type": "同事",
     "context": "屈建宁与田雨同为县委常委、副县长",
     "overlap_org": "中共蒲城县委员会/蒲城县人民政府", "overlap_period": "至今"},
    # 前任县委书记
    {"person_a": 1, "person_b": 18, "type": "前任-继任",
     "context": "张毅锋（原县委书记，现渭南市副市长）将县委书记职务交接给薛斌",
     "overlap_org": "中共蒲城县委员会", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 18, "type": "前任-继任",
     "context": "张毅锋曾任蒲城县县长（2016-2021），后薛斌继任县长，李少博为现任县长",
     "overlap_org": "蒲城县人民政府", "overlap_period": "2016-2026"},
    {"person_a": 1, "person_b": 18, "type": "前任-继任(县长)",
     "context": "薛斌于2021年8月接替张毅锋任蒲城县县长",
     "overlap_org": "蒲城县人民政府", "overlap_period": "2021"},
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_person_json(person, timeline_items, relationships_items, source_items):
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省", "city": "渭南市", "region": "蒲城县",
            "job": person.get("current_post", ""), "task_id": "shaanxi_蒲城县", "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"pucheng_{person['name']}", "name": person["name"], "aliases": [],
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
        "source_register": source_items,
        "open_questions": [
            {"priority": "critical", "question": f"Complete career timeline before current role for {person['name']}",
             "suggested_queries": [f"{person['name']} 简历 蒲城", f"{person['name']} 任职经历"]},
            {"priority": "critical", "question": f"Birth year, birthplace, education details for {person['name']}",
             "suggested_queries": [f"{person['name']} 出生年月", f"{person['name']} 籍贯"]}
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
    gexf_lines.append('    <description>蒲城县领导班子关系网络</description>')
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
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else "书记" in post and "副" not in post
        is_mayor = post in ["蒲城县县长"] or ("县长" in post and "副" not in post)
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
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        color_map = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
                      "政协": "255,240,200", "纪委": "255,200,150"}
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
        {"id": "S001", "title": "蒲城县召开两优一先暨目标责任考核表彰大会",
         "url": "https://www.pucheng.gov.cn/xwzx/ttxw/2073955071430713345.html",
         "publisher": "蒲城县人民政府", "published_at": "2026-07-03", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S002", "title": "蒲城县人民政府——县政府领导页面",
         "url": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/",
         "publisher": "蒲城县人民政府", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S003", "title": "李少博个人简历页面",
         "url": "https://www.pucheng.gov.cn/zfxxgk/fdzdgknr/pz/xzfld/lsb/",
         "publisher": "蒲城县人民政府", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S004", "title": "张毅锋360百科",
         "url": "https://baike.so.com/doc/5473645-5711494.html",
         "publisher": "360百科", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium"},
        {"id": "S005", "title": "蒲城县（渭南经开区）警示教育会议",
         "url": "https://www.pucheng.gov.cn/xwzx/ttxw/2073941968665133058.html",
         "publisher": "蒲城县人民政府", "published_at": "2026-07-03", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
    ]
    # Person JSONs for key figures
    for p in persons:
        if p["name"] in ["薛斌", "李少博", "张毅锋"]:
            timeline = []
            for pos in positions:
                if pos["person_id"] == p["id"]:
                    org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
                    timeline.append({
                        "start": pos.get("start_date", ""), "end": pos.get("end_date", ""),
                        "org": org_name, "title": pos["title"], "rank": pos.get("rank", ""),
                        "location": "陕西省渭南市蒲城县", "notes": pos.get("note", ""),
                        "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]
                    })
            rels = []
            for r in relationships:
                if r["person_a"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
                    rels.append({"person": other, "relationship_type": r["type"], "evidence": r["context"], "confidence": "confirmed"})
                elif r["person_b"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
                    rels.append({"person": other, "relationship_type": r["type"], "evidence": r["context"], "confidence": "confirmed"})
            pjson = make_person_json(p, timeline, rels, source_register)
            p_path = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-陕西省-渭南市-{p['current_post']}-{p['name']}.json")
            with open(p_path, "w", encoding="utf-8") as f:
                json.dump(pjson, f, ensure_ascii=False, indent=2)
            print(f"Person JSON written: {p_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
