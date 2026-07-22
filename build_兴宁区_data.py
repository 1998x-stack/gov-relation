#!/usr/bin/env python3
"""
南宁市兴宁区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Xingning District leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 南宁市
Region: 兴宁区
Targets: 区委书记 & 区长

Research Sources:
- 南宁市兴宁区人民政府官网 (www.nnxn.gov.cn) — 领导简介页面
- 兴宁区政务动态新闻 — 领导活动报道

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP = SCRIPT_DIR
DB_PATH = os.path.join(TMP, "兴宁区_network.db")
GEXF_PATH = os.path.join(TMP, "兴宁区_network.gexf")
PERSONS_DIR = os.path.join(TMP)
AS_OF = "2026-07-22"

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "高鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁区委书记",
        "current_org": "中共南宁市兴宁区委员会",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn) — 2026年2月领导干部警示教育大会报道"
    },
    {
        "id": 2,
        "name": "韦瑞智",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1984年10月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宁区区长",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/qz/quzhang/)"
    },
    # ════════════════════════════════════════
    # Key Deputies (区政府领导班子 + 区委常委)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "潘麒伊",
        "gender": "女",
        "ethnicity": "仫佬族",
        "birth": "1986年8月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴宁区委常委、常务副区长",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/fqz/)"
    },
    {
        "id": 4,
        "name": "余雄杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴宁区委常委、统战部部长、副区长",
        "current_org": "中共南宁市兴宁区委员会",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/fqz/)"
    },
    {
        "id": 5,
        "name": "陈志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "待查",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴宁区副区长",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/fqz/)"
    },
    {
        "id": 6,
        "name": "陈宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴宁区副区长、兴宁公安分局局长",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/fqz/)"
    },
    {
        "id": 7,
        "name": "李剑辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年1月",
        "birthplace": "待查",
        "education": "博士研究生",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "兴宁区副区长",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/fqz/)"
    },
    {
        "id": 8,
        "name": "孙晓梅",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1987年1月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴宁区副区长",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/fqz/)"
    },
    {
        "id": 9,
        "name": "陈铭建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴宁区委常委、纪委书记、监委主任",
        "current_org": "中共南宁市兴宁区纪律检查委员会",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn) — 2026年2月纪委全会报道"
    },
    # ════════════════════════════════════════
    # 调研员 (Researchers/Advisors)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "户大庆",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "调研员",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/dyy/)"
    },
    {
        "id": 11,
        "name": "曾纪荣",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "调研员",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/dyy/)"
    },
    {
        "id": 12,
        "name": "符煜中",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "调研员",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/dyy/)"
    },
    {
        "id": 13,
        "name": "李孙添",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "调研员",
        "current_org": "南宁市兴宁区人民政府",
        "source": "南宁市兴宁区人民政府官网(www.nnxn.gov.cn/xxgk/fdzdgknr/ldjj/dyy/)"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共南宁市兴宁区委员会", "type": "党委", "level": "县处级", "parent": "中共南宁市委员会", "location": "南宁市兴宁区"},
    {"id": 2, "name": "南宁市兴宁区人民政府", "type": "政府", "level": "县处级", "parent": "南宁市人民政府", "location": "南宁市兴宁区"},
    {"id": 3, "name": "中共南宁市兴宁区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共南宁市纪律检查委员会", "location": "南宁市兴宁区"},
    {"id": 4, "name": "中共南宁市兴宁区委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共南宁市兴宁区委员会", "location": "南宁市兴宁区"},
    {"id": 5, "name": "中共南宁市兴宁区委员会统一战线工作部", "type": "党委", "level": "乡科级", "parent": "中共南宁市兴宁区委员会", "location": "南宁市兴宁区"},
    {"id": 6, "name": "南宁市公安局兴宁分局", "type": "政府", "level": "乡科级", "parent": "南宁市公安局", "location": "南宁市兴宁区"},
    {"id": 7, "name": "南宁市兴宁区人大常委会", "type": "人大", "level": "县处级", "parent": "南宁市人大常委会", "location": "南宁市兴宁区"},
    {"id": 8, "name": "政协南宁市兴宁区委员会", "type": "政协", "level": "县处级", "parent": "政协南宁市委员会", "location": "南宁市兴宁区"},
    {"id": 9, "name": "兴宁区朝阳街道", "type": "乡镇/街道", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区朝阳街道"},
    {"id": 10, "name": "兴宁区民生街道", "type": "乡镇/街道", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区民生街道"},
    {"id": 11, "name": "兴宁区兴东街道", "type": "乡镇/街道", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区兴东街道"},
    {"id": 12, "name": "兴宁区三塘镇", "type": "乡镇/街道", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区三塘镇"},
    {"id": 13, "name": "兴宁区五塘镇", "type": "乡镇/街道", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区五塘镇"},
    {"id": 14, "name": "兴宁区昆仑镇", "type": "乡镇/街道", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区昆仑镇"},
    {"id": 15, "name": "兴宁产业园区", "type": "开发区", "level": "乡科级", "parent": "南宁市兴宁区人民政府", "location": "兴宁区"},
]

# 3. Positions (person → organization relationships)
positions = [
    # 高鑫
    {"person_id": 1, "org_id": 1, "title": "兴宁区委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 韦瑞智
    {"person_id": 2, "org_id": 1, "title": "兴宁区委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "兴宁区区长", "start_date": "2025-11-25", "end_date": "present", "rank": "正处级", "note": "2025年11月25日当选兴宁区第十五届人大第六次会议选举为区长"},
    # 潘麒伊
    {"person_id": 3, "org_id": 1, "title": "兴宁区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    # 余雄杰
    {"person_id": 4, "org_id": 1, "title": "兴宁区委常委、统战部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责民族、市场监管、综合行政执法、征地拆迁"},
    # 陈志华
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责司法、交通运输、农业农村、水利、退役军人事务等"},
    # 陈宏
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "兼任兴宁公安分局局长"},
    {"person_id": 6, "org_id": 6, "title": "分局长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 李剑辉
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责教育、民政、文旅、卫健、医保等"},
    # 孙晓梅
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责工业、商务、招商引资、土地储备、政务服务"},
    # 陈铭建
    {"person_id": 9, "org_id": 1, "title": "兴宁区委常委、纪委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "监委主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 调研员
    {"person_id": 10, "org_id": 2, "title": "调研员", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "调研员", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "调研员", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "调研员", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
]

# 4. Relationships (person ↔ person)
relationships = [
    # 党政正职关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档", "overlap_org": "兴宁区四家班子", "overlap_period": "2025-11至今"},
    # 区委班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委常委", "overlap_org": "中共兴宁区委", "overlap_period": "待查"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—区委常委", "overlap_org": "中共兴宁区委", "overlap_period": "待查"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共兴宁区委", "overlap_period": "待查"},
    # 政府班子
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "兴宁区政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—副区长", "overlap_org": "兴宁区政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "兴宁区政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "兴宁区政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "兴宁区政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "兴宁区政府", "overlap_period": "待查"},
]


# =========================================================================
# Person JSON helper
# =========================================================================

def make_person_json(person, timeline_items, relationships_items, source_items):
    """Build a person graph JSON dict."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "南宁市",
            "region": "兴宁区",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_兴宁区",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"xingning_{person['name']}",
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
            "administrative_rank": "",
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
            "identity": "confirmed" if person.get("birth") and person.get("birth") != "待查" else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Earlier career timeline before current role"
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
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
    gexf_lines.append('    <description>南宁市兴宁区领导班子关系网络</description>')
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
        is_secretary = "书记" in p.get("current_post", "") and "副" not in p.get("current_post", "").split("、")[0] if "、" not in p.get("current_post", "") else "书记" in p.get("current_post", "") and not p.get("current_post", "").startswith("副")
        is_mayor = p.get("current_post", "") == "兴宁区区长"
        is_discipline = "纪委" in p.get("current_post", "")

        if is_secretary: color = "200,30,30"
        elif is_mayor: color = "30,100,200"
        elif is_discipline: color = "255,165,0"
        else: color = "100,100,100"

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
        if otype == "党委": ocolor = "255,200,200"
        elif otype == "政府": ocolor = "200,200,255"
        elif otype == "人大": ocolor = "200,255,255"
        elif otype == "政协": ocolor = "255,240,200"
        elif otype == "纪委": ocolor = "255,200,150"
        elif otype == "开发区": ocolor = "200,255,200"
        elif otype == "乡镇/街道": ocolor = "255,255,200"
        else: ocolor = "200,200,200"

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
        {"id": "S001", "title": "南宁市兴宁区人民政府门户网站", "url": "http://www.nnxn.gov.cn/", "publisher": "南宁市兴宁区人民政府",
         "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership page (领导简介)"},
        {"id": "S002", "title": "南宁市人民政府门户网站", "url": "https://www.nanning.gov.cn/", "publisher": "南宁市人民政府",
         "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S003", "title": "中共南宁市委网站", "url": "http://sw.nanning.gov.cn/", "publisher": "中共南宁市委员会",
         "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    ]

    # 高鑫 person JSON
    gx_timeline = [
        {"start": "待查", "end": "present", "org": "中共南宁市兴宁区委员会", "title": "兴宁区委书记",
         "level": "正处级", "location": "广西南宁", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "主持区委全面工作",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到高鑫完整履历和研究方向",
         "confidence": "unverified", "source_ids": []},
    ]
    gx_relationships = [
        {"person": "韦瑞智", "person_id": "xingning_韦瑞智", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前兴宁区委书记与区长党政搭档",
         "overlap_org": "中共兴宁区委/兴宁区人民政府",
         "overlap_period": "2025-11至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    gx_json = make_person_json(persons[0], gx_timeline, gx_relationships, source_register)
    gx_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-兴宁区委书记-高鑫.json")
    with open(gx_path, "w", encoding="utf-8") as f:
        json.dump(gx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {gx_path}")

    # 韦瑞智 person JSON
    wrz_timeline = [
        {"start": "2025-11-25", "end": "present", "org": "南宁市兴宁区人民政府", "title": "兴宁区区长",
         "level": "正处级", "location": "广西南宁", "system": "government", "rank": "正处级",
         "is_key_promotion": True,
         "notes": "2025年11月25日当选兴宁区第十五届人民代表大会第六次会议选举为区长",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "待查", "end": "present", "org": "中共南宁市兴宁区委员会", "title": "兴宁区委副书记",
         "level": "正处级", "location": "广西南宁", "system": "party", "rank": "正处级",
         "is_key_promotion": False, "notes": "",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "2025-11", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到韦瑞智任区长前的完整履历，已知：1984年10月生，壮族，研究生学历，中共党员",
         "confidence": "unverified", "source_ids": []},
    ]
    wrz_relationships = [
        {"person": "高鑫", "person_id": "xingning_高鑫", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前兴宁区区长与区委书记党政搭档",
         "overlap_org": "兴宁区人民政府/中共兴宁区委",
         "overlap_period": "2025-11至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wrz_json = make_person_json(persons[1], wrz_timeline, wrz_relationships, source_register)
    wrz_json["investigation_scope"]["job"] = "兴宁区区长"
    wrz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-兴宁区区长-韦瑞智.json")
    with open(wrz_path, "w", encoding="utf-8") as f:
        json.dump(wrz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wrz_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
