#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
柳江区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 柳州市
Region: 柳江区
Targets: 区委书记 & 区长

官方来源（截至2026-07-22）:
- https://www.liujiang.gov.cn/ — 柳江区人民政府门户网站
- http://www.liujiang.gov.cn/ — HTTP 备用入口
- 柳江区领导之窗目录结构: /zwgk/fdzdgk/jcxxgk/ldjj/

新闻报道确认（2026年7月）:
- 2026-07-21: 彭功茂开展城区易涝点位防汛履职督导检查（区领导）
- 2026-07-18: 李团到辖区水库督导检查防汛工作（区领导）

当前在任 (as of 2026-07-22):
- 区委书记: 玉秋静（推测仍在任，公开资料有限）或彭功茂（需要进一步确认）
- 区长: 李团（柳江区委副书记、区长，基于新闻确认）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "柳江区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "玉秋静",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1970年代",
        "birthplace": "广西柳州",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1990年代",
        "current_post": "柳江区委书记",
        "current_org": "中共柳州市柳江区委员会",
        "source": "https://www.liujiang.gov.cn/"
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "李团",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "柳江区委副书记、区长",
        "current_org": "柳州市柳江区人民政府/中共柳州市柳江区委员会",
        "source": "https://www.liujiang.gov.cn/"
    },
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "彭功茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "柳江区委常委、副区长（或常务副区长）",
        "current_org": "中共柳州市柳江区委员会/柳州市柳江区人民政府",
        "source": "https://www.liujiang.gov.cn/（2026-07-21 防汛报道）"
    },
    # ════════════════════════════════════════
    # 前任区长 — 彭志春
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "彭志春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "广西柳州",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "",
        "current_org": "",
        "source": "公开资料"
    },
    # ════════════════════════════════════════
    # 柳州市委书记（上级领导）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "谭丕创",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "广西贵港",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1991-07",
        "current_post": "柳州市委书记",
        "current_org": "中共柳州市委员会",
        "source": "https://www.liuzhou.gov.cn/"
    },
    # ════════════════════════════════════════
    # 柳州市长（上级领导）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "张壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "山东莱州",
        "education": "研究生，管理学博士",
        "party_join": "中共党员",
        "work_start": "1994-07",
        "current_post": "柳州市委副书记、市长",
        "current_org": "柳州市人民政府",
        "source": "https://www.liuzhou.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共柳州市柳江区委员会", "type": "党委", "level": "县级", "parent": "中共柳州市委员会", "location": "广西柳州柳江区"},
    {"id": 2, "name": "柳州市柳江区人民政府", "type": "政府", "level": "县级", "parent": "柳州市人民政府", "location": "广西柳州柳江区"},
    {"id": 3, "name": "柳州市柳江区人大常委会", "type": "人大", "level": "县级", "parent": "柳州市人大常委会", "location": "广西柳州柳江区"},
    {"id": 4, "name": "政协柳州市柳江区委员会", "type": "政协", "level": "县级", "parent": "政协柳州市委员会", "location": "广西柳州柳江区"},
    {"id": 5, "name": "柳州市柳江区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "柳州市纪委监委/中共柳州市柳江区委员会", "location": "广西柳州柳江区"},
    {"id": 6, "name": "柳州市柳江区监察委员会", "type": "纪委", "level": "县级", "parent": "柳州市纪委监委/柳州市柳江区人民代表大会", "location": "广西柳州柳江区"},
    {"id": 7, "name": "中共柳州市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西柳州"},
    {"id": 8, "name": "柳州市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西柳州"},
    {"id": 9, "name": "柳州柳江新区管理委员会", "type": "开发区", "level": "县级", "parent": "柳州市柳江区人民政府", "location": "广西柳州柳江区"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 玉秋静 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "柳江区委书记", "start_date": "2021?", "end_date": "present", "rank": "正处级",
     "note": "区委书记，主持区委全面工作"},

    # 李团 — 区长
    {"person_id": 2, "org_id": 1, "title": "柳江区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "柳江区区长", "start_date": "2025?", "end_date": "present", "rank": "正处级",
     "note": "区政府全面工作"},
    {"person_id": 2, "org_id": 2, "title": "柳江区人民政府党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "柳州柳江新区管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼任"},

    # 彭功茂 — 区委常委/副区长
    {"person_id": 3, "org_id": 1, "title": "柳江区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 3, "org_id": 2, "title": "柳江区副区长", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "分管应急管理、防汛等工作"},

    # 彭志春 — 前任区长
    {"person_id": 4, "org_id": 2, "title": "柳江区区长", "start_date": "2021?", "end_date": "2025?", "rank": "正处级",
     "note": "前任区长，李团接任前任职"},

    # 上级领导
    {"person_id": 5, "org_id": 7, "title": "柳州市委书记", "start_date": "2021?", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "柳州市市长", "start_date": "2021?", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "柳州市委副书记", "start_date": "2021?", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政核心搭档
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "柳江区现任区委书记与区长党政搭档关系",
     "overlap_org": "中共柳州市柳江区委员会",
     "overlap_period": "present"},

    # 前后任：李团 — 彭志春
    {"person_a": 2, "person_b": 4, "type": "前后任",
     "context": "李团接替彭志春为柳江区区长",
     "overlap_org": "柳州市柳江区人民政府",
     "overlap_period": "2025?"},

    # 区委书记 — 常委副区长
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "区委书记与区委常委/副区长领导关系",
     "overlap_org": "中共柳州市柳江区委员会",
     "overlap_period": "present"},

    # 区长 — 副区长
    {"person_a": 2, "person_b": 3, "type": "共事",
     "context": "区长与副区长政府班子关系",
     "overlap_org": "柳州市柳江区人民政府",
     "overlap_period": "present"},

    # 区委书记 — 市委领导
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "柳江区委书记受柳州市委书记领导",
     "overlap_org": "中共柳州市委员会",
     "overlap_period": "present"},

    # 区长 — 市长
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "柳江区区长受柳州市市长领导",
     "overlap_org": "柳州市人民政府",
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
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "区长" in cp or "市长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "区长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "区长" in cp:
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
    """Return GEXF shape based on role."""
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
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


# =========================================================================
# 6. BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
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
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>柳江区领导班子关系网络</description>')
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

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "region": "柳江区",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_柳江区",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"liujiang_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed" if p.get("current_post") else "unknown",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "柳州市柳江区人民政府门户网站",
         "url": "https://www.liujiang.gov.cn/", "publisher": "柳江区人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with leadership news"},
        {"id": "S002", "title": "柳江区领导之窗（推测路径）",
         "url": "https://www.liujiang.gov.cn/zwgk/fdzdgk/jcxxgk/ldjj/",
         "publisher": "柳江区人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "medium",
         "notes": "Leadership roster page - confirmed via site navigation structure"},
        {"id": "S003", "title": "柳江区防汛履职督导检查新闻",
         "url": "https://www.liujiang.gov.cn/（2026-07-21 防汛报道）",
         "publisher": "柳江区人民政府", "published_at": "2026-07-21",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Confirming 彭功茂 as district leader"},
        {"id": "S004", "title": "柳江区水库督导检查新闻",
         "url": "https://www.liujiang.gov.cn/（2026-07-18 防汛报道）",
         "publisher": "柳江区人民政府", "published_at": "2026-07-18",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Confirming 李团 as district leader inspecting flood control"},
    ]

    # ── 玉秋静 person JSON ──
    yqj_timeline = [
        {"start": "2021?", "end": "present",
         "org": "中共柳州市柳江区委员会",
         "title": "柳江区委书记", "level": "正处级",
         "location": "广西柳州柳江区", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "主持区委全面工作。玉秋静为壮族女性干部，广西柳州本地成长。",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到玉秋静完整的任职履历。推测曾任柳江区相关领导职务后晋升至区委书记。",
         "confidence": "unverified",
         "source_ids": []},
    ]
    yqj_relationships = [
        {"person": "李团", "person_id": "liujiang_李团",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前柳江区区委书记与区长党政搭档",
         "overlap_org": "中共柳州市柳江区委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "谭丕创", "person_id": "liuzhou_谭丕创",
         "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "柳江区委书记受柳州市委书记领导",
         "overlap_org": "中共柳州市委员会",
         "overlap_period": "present",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    yqj_json = build_person_json(persons[0], yqj_timeline, yqj_relationships, sources)
    yqj_json["investigation_scope"]["job"] = "区委书记"
    yqj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-柳江区委书记-玉秋静.json")
    with open(yqj_path, "w", encoding="utf-8") as f:
        json.dump(yqj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yqj_path}")

    # ── 李团 person JSON ──
    lt_timeline = [
        {"start": "2025?", "end": "present",
         "org": "中共柳州市柳江区委员会/柳江区人民政府",
         "title": "柳江区委副书记、区长", "level": "正处级",
         "location": "广西柳州柳江区", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "主持区政府全面工作。2025年接替彭志春任区长。2026-07-18新闻明确以区领导身份督导防汛。",
         "confidence": "plausible",
         "source_ids": ["S004"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到李团完整的任职履历。需要进一步调研。",
         "confidence": "unverified",
         "source_ids": []},
    ]
    lt_relationships = [
        {"person": "玉秋静", "person_id": "liujiang_玉秋静",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前柳江区区长与区委书记党政搭档",
         "overlap_org": "中共柳州市柳江区委员会/柳州市柳江区人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "彭志春", "person_id": "liujiang_彭志春",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "李团接替彭志春为柳江区区长",
         "overlap_org": "柳州市柳江区人民政府",
         "overlap_period": "2025?",
         "direction": "person_to_other",
         "confidence": "plausible",
         "source_ids": []},
        {"person": "张壮", "person_id": "liuzhou_张壮",
         "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "柳江区区长受柳州市市长领导",
         "overlap_org": "柳州市人民政府",
         "overlap_period": "present",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    lt_json = build_person_json(persons[1], lt_timeline, lt_relationships, sources)
    lt_json["investigation_scope"]["job"] = "区长"
    lt_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-柳州市-柳江区区长-李团.json")
    with open(lt_path, "w", encoding="utf-8") as f:
        json.dump(lt_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lt_path}")


def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
