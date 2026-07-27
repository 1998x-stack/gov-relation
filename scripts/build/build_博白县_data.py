#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博白县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 玉林市
Region: 博白县
Targets: 县委书记 & 县长

Research status: PARTIAL EVIDENCE MODE
- Confirmed from bobai.gov.cn: 县委书记覃挺（截至2026年7月在任，多次新闻确认）
- All other data based on pre-training knowledge，除覃挺外均未核实

Confirmed sources:
- https://www.bobai.gov.cn/ (2026-07-23 首页新闻确认覃挺为县委书记)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "博白县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记 — CONFIRMED
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "覃挺",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "广西（推测）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博白县委书记",
        "current_org": "中共博白县委员会",
        "source": "https://www.bobai.gov.cn/（2026-07-23确认——多篇新闻提及覃挺为县委书记）"
    },
    # ════════════════════════════════════════
    # 核心领导：县长 — UNVERIFIED（推测）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "覃挺（推测兼任或已任命）",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "广西（推测）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博白县委副书记、县长（推测）",
        "current_org": "博白县人民政府/中共博白县委员会",
        "source": "待核实——博白县人民政府网站领导之窗暂无法访问"
    },
    # ════════════════════════════════════════
    # 前任县委书记：孙国梁（推测）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "孙国梁（推测前任）",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "",
        "current_org": "",
        "source": "公开网络资料（推测）——前博白县委书记，覃挺的前任"
    },
    # ════════════════════════════════════════
    # 前任县长：周印章（推测）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "周印章（推测前任县长）",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "",
        "current_org": "",
        "source": "公开网络资料（推测）——2021年左右曾任博白县代县长/县长"
    },
    # ════════════════════════════════════════
    # 县委常委、人武部领导（CONFIRMED）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李晶",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博白县委常委、县人武部领导",
        "current_org": "中共博白县委员会/博白县人民武装部",
        "source": "https://www.bobai.gov.cn/（2026-07-22 博白县'八一'军政座谈会新闻提及）"
    },
    # ════════════════════════════════════════
    # 县政府党组成员、县公安局党委书记（CONFIRMED）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "陈浩富",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博白县政府党组成员、县公安局党委书记",
        "current_org": "博白县人民政府/博白县公安局",
        "source": "https://www.bobai.gov.cn/（2026-07-22 博白县'八一'军政座谈会新闻提及）"
    },
    # ════════════════════════════════════════
    # 玉林市领导（上级）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "王琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委书记（推测）",
        "current_org": "中共玉林市委员会",
        "source": "公开网络资料（推测）"
    },
    {
        "id": 8,
        "name": "张惠强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委副书记、市长",
        "current_org": "玉林市人民政府/中共玉林市委员会",
        "source": "https://www.yulin.gov.cn/（据已有资料确认在任）"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共博白县委员会", "type": "党委", "level": "县级", "parent": "中共玉林市委员会", "location": "广西玉林博白县"},
    {"id": 2, "name": "博白县人民政府", "type": "政府", "level": "县级", "parent": "玉林市人民政府", "location": "广西玉林博白县"},
    {"id": 3, "name": "博白县人大常委会", "type": "人大", "level": "县级", "parent": "玉林市人大常委会", "location": "广西玉林博白县"},
    {"id": 4, "name": "政协博白县委员会", "type": "政协", "level": "县级", "parent": "政协玉林市委员会", "location": "广西玉林博白县"},
    {"id": 5, "name": "博白县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "玉林市纪委监委/中共博白县委员会", "location": "广西玉林博白县"},
    {"id": 6, "name": "博白县监察委员会", "type": "纪委", "level": "县级", "parent": "玉林市纪委监委/博白县人民代表大会", "location": "广西玉林博白县"},
    {"id": 7, "name": "博白县人民武装部", "type": "政府", "level": "县级", "parent": "玉林军分区", "location": "广西玉林博白县"},
    {"id": 8, "name": "博白县公安局", "type": "政府", "level": "县级", "parent": "博白县人民政府/玉林市公安局", "location": "广西玉林博白县"},
    {"id": 9, "name": "中共玉林市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西玉林"},
    {"id": 10, "name": "玉林市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西玉林"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 覃挺 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "博白县委书记", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "主持县委全面工作。2026年7月多次新闻确认为现任县委书记。"},

    # 覃挺兼任县长（推测）
    {"person_id": 2, "org_id": 1, "title": "博白县委副书记", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "推测"},
    {"person_id": 2, "org_id": 2, "title": "博白县县长", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "推测——县长姓名待核实。覃挺升任县委书记后，县长人选存疑。"},

    # 孙国梁 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "博白县委书记", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "前任县委书记，推测覃挺的前任"},

    # 周印章 — 前任县长
    {"person_id": 4, "org_id": 2, "title": "博白县代县长/县长", "start_date": "2021?", "end_date": "", "rank": "正处级",
     "note": "推测曾任博白县代县长/县长"},

    # 李晶 — 县委常委/人武部
    {"person_id": 5, "org_id": 1, "title": "博白县委常委", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年7月新闻确认在任"},
    {"person_id": 5, "org_id": 7, "title": "博白县人武部领导", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年7月新闻确认在任"},

    # 陈浩富 — 县政府党组成员/公安局党委书记
    {"person_id": 6, "org_id": 2, "title": "博白县政府党组成员", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年7月新闻确认在任"},
    {"person_id": 6, "org_id": 8, "title": "博白县公安局党委书记", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "2026年7月新闻确认在任"},

    # 王琛 — 玉林市委书记
    {"person_id": 7, "org_id": 9, "title": "玉林市委书记", "start_date": "2023?", "end_date": "present", "rank": "正厅级",
     "note": "根据已有玉州区资料推测在任"},

    # 张惠强 — 玉林市长
    {"person_id": 8, "org_id": 9, "title": "玉林市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": ""},
    {"person_id": 8, "org_id": 10, "title": "玉林市市长", "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "据已有玉州区资料确认在任"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政核心搭档
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "博白县现任县委书记与县长党政搭档关系（推测）",
     "overlap_org": "中共博白县委员会/博白县人民政府",
     "overlap_period": "present"},

    # 前后任：覃挺 ← 孙国梁
    {"person_a": 1, "person_b": 3, "type": "前后任",
     "context": "覃挺接替孙国梁为博白县委书记（推测）",
     "overlap_org": "中共博白县委员会",
     "overlap_period": ""},

    # 前后任：覃挺（从县长升任书记，若有）→ 新任县长
    {"person_a": 1, "person_b": 4, "type": "前后任",
     "context": "推测覃挺曾任博白县县长，后升任县委书记；周印章可能为前后任关系",
     "overlap_org": "博白县人民政府",
     "overlap_period": ""},

    # 县委书记 — 县委常委
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "县委书记与县委常委/人武部领导",
     "overlap_org": "中共博白县委员会",
     "overlap_period": "present"},

    # 县委书记 — 县政府党组成员
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "县委书记与县政府党组成员/公安局党委书记",
     "overlap_org": "中共博白县委员会/博白县人民政府",
     "overlap_period": "present"},

    # 县委书记 — 市委领导
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "博白县委书记受玉林市委书记领导",
     "overlap_org": "中共玉林市委员会",
     "overlap_period": "present"},

    # 县委书记 — 市长
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "博白县委书记与玉林市长党政关系",
     "overlap_org": "中共玉林市委员会",
     "overlap_period": "present"},

    # 县长（推测）— 市长
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "博白县县长（推测）受玉林市长领导",
     "overlap_org": "玉林市人民政府",
     "overlap_period": "present"},
]

# =========================================================================
# 5. HELPERS
# =========================================================================


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "县长" in cp or "市长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "县长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    if "公安" in cp or "政法" in cp:
        return "50,50,150"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "县长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(org_type, "200,200,200")


def make_person_json(person, timeline, relationships_list, source_register):
    """Create a person depth graph JSON structure."""
    now = AS_OF.replace("-", "")
    person_id = f"bobai_{person['name']}"
    is_confirmed = 1 <= person["id"] <= 1  # Only person 1 (覃挺) is confirmed
    career_completeness = "partial" if is_confirmed else "thin"
    identity_conf = "confirmed" if is_confirmed else "unverified"
    role_conf = "confirmed" if is_confirmed else "unverified"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "玉林市",
            "region": "博白县",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_博白县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if person["id"] <= 2 else "待查",
            "as_of": AS_OF,
            "is_current_confirmed": is_confirmed,
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
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": identity_conf,
            "current_role": role_conf,
            "career_completeness": career_completeness,
            "relationship_confidence": "low",
            "biggest_gap": "除覃挺在任县委书记由bobai.gov.cn确认外，所有其他信息均未核实。网络工具全部不可用（Exa限流、百度403、Jina不可用）。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
                "why_it_matters": "无法建立身份标识",
                "suggested_queries": [f"{person['name']} 简历 博白县"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历",
                "why_it_matters": "无法追溯其任职路径",
                "suggested_queries": [f"{person['name']} 博白县 任职经历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}是否仍在现任职位",
                "why_it_matters": "可能已调整",
                "suggested_queries": [f"{person['name']} 博白县 {person.get('current_post', '')} 2025 2026"],
                "last_attempted": AS_OF
            },
        ]
    }


# =========================================================================
# 6. BUILD
# =========================================================================


def build():
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
    lines.append('    <description>博白县领导班子关系网络（部分证据模式 — 仅覃挺现任县委书记已由bobai.gov.cn确认）</description>')
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
        c = person_color(post)
        sz = person_size(post)
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
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
        {
            "id": "S001",
            "title": "博白县人民政府门户网站",
            "url": "https://www.bobai.gov.cn/",
            "publisher": "博白县人民政府",
            "published_at": "持续更新",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "首页新闻确认覃挺为县委书记（2026年7月多篇新闻）"
        },
        {
            "id": "S002",
            "title": "博白县'八一'军政座谈会新闻",
            "url": "https://www.bobai.gov.cn/",
            "publisher": "博白县人民政府",
            "published_at": "2026-07-22",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认李晶（县委常委、人武部领导）和陈浩富（县政府党组成员、公安局党委书记）在任"
        },
    ]

    # 覃挺 person JSON
    qt_timeline = [
        {"start": "", "end": "present", "org": "中共博白县委员会", "title": "博白县委书记",
         "level": "县级", "location": "广西玉林博白县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "根据bobai.gov.cn确认，2026年7月在任",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    qt_relationships = [
        {"person": "县长（推测）", "person_id": "bobai_覃挺（推测兼任或已任命）", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "覃挺（县委书记）与县长为博白县党政主要搭档",
         "overlap_org": "博白县党政班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
        {"person": "孙国梁（推测前任）", "person_id": "bobai_孙国梁（推测前任）", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "推测覃挺接替孙国梁任博白县委书记",
         "overlap_org": "中共博白县委员会",
         "overlap_period": "",
         "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
        {"person": "李晶", "person_id": "bobai_李晶", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "共事于中共博白县委员会",
         "overlap_org": "中共博白县委员会",
         "overlap_period": "present",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "陈浩富", "person_id": "bobai_陈浩富", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "共事于博白县党政班子",
         "overlap_org": "博白县人民政府",
         "overlap_period": "present",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    qt_json = make_person_json(persons[0], qt_timeline, qt_relationships, source_register)
    qt_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县委书记-覃挺.json")
    with open(qt_path, "w", encoding="utf-8") as f:
        json.dump(qt_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {qt_path}")

    # 县长 person JSON (partial)
    mayor_timeline = [
        {"start": "", "end": "present", "org": "博白县人民政府", "title": "博白县县长（推测）",
         "level": "县级", "location": "广西玉林博白县", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "县长姓名待核实。bobai.gov.cn领导之窗不可访问。",
         "confidence": "unverified", "source_ids": []},
    ]
    mayor_relationships = [
        {"person": "覃挺", "person_id": "bobai_覃挺", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县长与覃挺（县委书记）为博白县党政主要搭档",
         "overlap_org": "博白县党政班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
    ]
    mayor_json = make_person_json(persons[1], mayor_timeline, mayor_relationships, source_register)
    mayor_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县长-待查.json")
    with open(mayor_path, "w", encoding="utf-8") as f:
        json.dump(mayor_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {mayor_path}")

    print("\nBuild complete (partial evidence mode). Qin Ting confirmed as county party secretary via bobai.gov.cn.")
    print("County mayor's name UNKNOWN — leadership page inaccessible. All other data unverified.")
    print("See open_questions and gaps for details.")


if __name__ == "__main__":
    build()
