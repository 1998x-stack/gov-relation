#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Ang'angxi District (昂昂溪区), Qiqihar, Heilongjiang.

NOTE: Web access to Chinese government sites (qqhr.gov.cn, angangxi.gov.cn) was completely
unreachable from this environment (timeouts, DNS failures, firewall blocks). Baidu Baike
was also inaccessible. Data below is compiled from training knowledge and the Qiqihar
Baike page (via Wikipedia), with all confidence levels explicitly marked. This is a
partial-evidence artifact per the fallback playbook.

Expected artifact paths:
  staging_dir:   data/tmp/heilongjiang_昂昂溪区/
  build_script:  data/tmp/heilongjiang_昂昂溪区/build_昂昂溪区_data.py
  database:      data/tmp/heilongjiang_昂昂溪区/昂昂溪区_network.db
  gexf:          data/tmp/heilongjiang_昂昂溪区/昂昂溪区_network.gexf
  person_json:   data/tmp/heilongjiang_昂昂溪区/persons/YYYYMMDD-*.json
"""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-24"
TODAY = "20260724"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR  # We are already in data/tmp/heilongjiang_昂昂溪区/
DB_PATH = os.path.join(STAGING, "昂昂溪区_network.db")
GEXF_PATH = os.path.join(STAGING, "昂昂溪区_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

os.makedirs(PERSONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# DATA — All entries with confidence levels
# ═══════════════════════════════════════════════════════════════════════

# ── Note on research status ──
# Due to complete inaccessibility of Chinese government websites (qqhr.gov.cn,
# angangxi.gov.cn), Baidu Baike, and news portals (thepaper.cn) from this
# environment, the leadership data below comes from training knowledge.
# Names and roles should be verified against official sources.

persons = [
    # ── Current Top Leaders (待确认 — may be outdated or incorrect) ──
    {
        "id": 1,
        "name": "待确认区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共齐齐哈尔市昂昂溪区委书记",
        "current_org": "中共齐齐哈尔市昂昂溪区委员会",
        "source": "https://www.qqhr.gov.cn/（无法访问）",
        "confidence": "unverified",
        "notes": "因政府网站无法访问，当前区委书记姓名未能确认。可能需要通过齐齐哈尔市委组织部任前公示检索确认。"
    },
    {
        "id": 2,
        "name": "待确认区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市昂昂溪区委副书记、区长",
        "current_org": "齐齐哈尔市昂昂溪区人民政府",
        "source": "https://www.qqhr.gov.cn/（无法访问）",
        "confidence": "unverified",
        "notes": "因政府网站无法访问，当前区长姓名未能确认。"
    },
]

organizations = [
    {"id": 1, "name": "中共齐齐哈尔市昂昂溪区委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 2, "name": "齐齐哈尔市昂昂溪区人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 3, "name": "齐齐哈尔市昂昂溪区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 4, "name": "中国人民政治协商会议齐齐哈尔市昂昂溪区委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 5, "name": "中共齐齐哈尔市昂昂溪区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 6, "name": "中共齐齐哈尔市昂昂溪区委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委政法委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 7, "name": "中共齐齐哈尔市昂昂溪区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委组织部", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 8, "name": "中共齐齐哈尔市昂昂溪区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委宣传部", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 9, "name": "齐齐哈尔市昂昂溪区监察委员会", "type": "纪委", "level": "县处级",
     "parent": "齐齐哈尔市监察委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 10, "name": "齐齐哈尔市昂昂溪区人民法院", "type": "事业单位", "level": "县处级",
     "parent": "齐齐哈尔市中级人民法院", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 11, "name": "齐齐哈尔市昂昂溪区人民检察院", "type": "事业单位", "level": "县处级",
     "parent": "齐齐哈尔市人民检察院", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    # Subordinate organizations
    {"id": 12, "name": "中共昂昂溪区新兴街道工作委员会", "type": "党委", "level": "乡科级",
     "parent": "中共齐齐哈尔市昂昂溪区委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 13, "name": "中共昂昂溪区新建街道工作委员会", "type": "党委", "level": "乡科级",
     "parent": "中共齐齐哈尔市昂昂溪区委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 14, "name": "中共昂昂溪区林机街道工作委员会", "type": "党委", "level": "乡科级",
     "parent": "中共齐齐哈尔市昂昂溪区委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 15, "name": "中共昂昂溪区道北街道工作委员会", "type": "党委", "level": "乡科级",
     "parent": "中共齐齐哈尔市昂昂溪区委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区"},
    {"id": 16, "name": "中共昂昂溪区水师营满族镇委员会", "type": "党委", "level": "乡科级",
     "parent": "中共齐齐哈尔市昂昂溪区委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区水师营满族镇"},
    {"id": 17, "name": "中共昂昂溪区榆树屯镇委员会", "type": "党委", "level": "乡科级",
     "parent": "中共齐齐哈尔市昂昂溪区委员会", "location": "黑龙江省齐齐哈尔市昂昂溪区榆树屯镇"},
]

positions = [
    # Top leaders (unknown names, placeholder)
    {"person_id": 1, "org_id": 1, "title": "昂昂溪区委书记", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": "当前姓名待确认。需访问政府网站确认。"},
    {"person_id": 2, "org_id": 2, "title": "昂昂溪区委副书记、区长", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": "当前姓名待确认。"},
]

relationships = []

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "255,50,50"
    if "区长" in post and "副" not in post and "人大" not in post and "政协" not in post:
        return "50,100,255"
    if "纪委书记" in post or "纪委" in post:
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
           ("区长" in post and "副" not in post and "人大" not in post and "政协" not in post)


def person_shape(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "square"
    if "区长" in post and "副" not in post and "人大" not in post and "政协" not in post:
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
        "开发区": "200,255,200",
        "事业单位": "220,220,220",
    }
    return colors.get(otype, "200,200,200")


def build():
    os.makedirs(STAGING, exist_ok=True)
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
        pid = f"angangxi_{p['name']}"
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
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>昂昂溪区领导班子关系网络（基于不完全公开信息，所有领导信息待确认）</description>')
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

    # Person → organization
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

    # Person ↔ person
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
    source_register = [
        {"id": "S001", "title": "维基百科 - 昂昂溪区", "url": "https://zh.wikipedia.org/wiki/%E6%98%82%E6%98%82%E6%BA%AA%E5%8C%BA",
         "publisher": "维基百科", "published_at": "2026-07-09", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium",
         "notes": "提供昂昂溪区行政区划、人口等基本信息"},
        {"id": "S002", "title": "快懂百科 - 昂昂溪区", "url": "http://www.baike.com/wiki/%E6%98%82%E6%98%82%E6%BA%AA%E5%8C%BA",
         "publisher": "快懂百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "low",
         "notes": "提供昂昂溪区经济地理数据"},
        {"id": "S003", "title": "齐齐哈尔市人民政府 - 领导之窗", "url": "https://www.qqhr.gov.cn/zfxxgk/ldzc/（无法访问）",
         "publisher": "齐齐哈尔市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "网站完全不可访问，无法获取领导信息"},
        {"id": "S004", "title": "昂昂溪区人民政府官方网站", "url": "https://www.angangxi.gov.cn/（无法访问）",
         "publisher": "昂昂溪区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "网站完全不可访问，无法获取领导信息"},
    ]

    def make_person_json(p, timeline, relationships_list):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "齐齐哈尔市",
                "region": "昂昂溪区",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_昂昂溪区",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"angangxi_{p['name']}",
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
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
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
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的姓名、出生年月、籍贯、教育、完整履历全部缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的真实姓名",
                 "why_it_matters": "核心目标人物姓名未知，无法进行任何后续调查",
                 "suggested_queries": [f"昂昂溪区 区委书记", f"昂昂溪区 区长", "昂昂溪区 领导分工"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"昂昂溪区 区委书记 简历", f"昂昂溪区 区长 简历"],
                 "last_attempted": AS_OF},
                {"priority": "high",
                 "question": "昂昂溪区全体领导班子成员",
                 "why_it_matters": "常委员会成员、副区长、人大主任、政协主席全部未知",
                 "suggested_queries": ["昂昂溪区 领导班子", "昂昂溪区 区委常委"],
                 "last_attempted": AS_OF},
            ]
        }
        return result

    # ── Person JSON: 区委书记 (placeholder) ──
    sj_timeline = [
        {"start": "unknown", "end": "", "org": "中共齐齐哈尔市昂昂溪区委员会", "title": "区委书记",
         "notes": "当前区委书记姓名未知", "confidence": "unverified", "source_ids": []},
    ]
    sj_rels = []
    sj_json = make_person_json(persons[0], sj_timeline, sj_rels)
    sj_path = os.path.join(PERSONS_DIR, f"{TODAY}-黑龙江省-齐齐哈尔市-区委书记-daiqueren区委书记.json")
    with open(sj_path, "w", encoding="utf-8") as f:
        json.dump(sj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {sj_path}")

    # ── Person JSON: 区长 (placeholder) ──
    qz_timeline = [
        {"start": "unknown", "end": "", "org": "齐齐哈尔市昂昂溪区人民政府", "title": "区长",
         "notes": "当前区长姓名未知", "confidence": "unverified", "source_ids": []},
    ]
    qz_rels = []
    qz_json = make_person_json(persons[1], qz_timeline, qz_rels)
    qz_path = os.path.join(PERSONS_DIR, f"{TODAY}-黑龙江省-齐齐哈尔市-区长-daiqueren区长.json")
    with open(qz_path, "w", encoding="utf-8") as f:
        json.dump(qz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {qz_path}")

    print("\nDone. Summary:")
    print(f"  DB:        {DB_PATH}")
    print(f"  GEXF:      {GEXF_PATH}")
    print(f"  Persons:   {PERSONS_DIR}/")


if __name__ == "__main__":
    build()
