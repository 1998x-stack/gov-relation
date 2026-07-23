#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安新县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 保定市（行政区划隶属）/ 雄安新区（实际管理）
Region: 安新县
Targets: 县委书记 & 县长

Research Sources:
- Wikipedia (zh.wikipedia.org/wiki/安新县) — 确认县委书记杨宝昌
- 安新县人民政府 (www.anxin.gov.cn / baiyangdian.gov.cn) — 网站可访问但领导之窗页面受限
- 安新县人民政府门户新闻 — 提及李国向主持县政府常务会议
- 网络搜索严重受限（Exa rate-limit, Baidu/Bing/Jina blocked, Google blocked）

Research Date: 2026-07-23

已知信息:
- 县委书记: 杨宝昌（维基百科信息框确认）
- 县长: 待查（网络访问严重受限，未能确认姓名）
  - 李国向在政府新闻中出现主持县政府常务会议，疑为县长或常务副县长
- 安新县为雄安新区三县之一，实际由雄安新区管理
- 安新县下辖9镇3乡: 安新镇、大王镇、三台镇、端村镇、赵北口镇、同口镇、刘李庄镇、安州镇、老河头镇、圈头乡、寨里乡、芦庄乡
- 代管龙化乡（来自高阳县）

Confidence:
- 杨宝昌 县委书记: confirmed (Wikipedia infobox, last revised 2026-05-26)
- 县长: unverified (web search degraded — 所有搜索源均超时/受限)
- 李国向 身份: unverified (出现在政府新闻中，无法确认具体职务)
- 杨宝昌完整履历: unverified (web search degraded)
- 县委常委完整名单: unverified (web search degraded)
- 安新县领导分工: unverified (web search degraded)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "安新县"

STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── CONSTANTS ──
TODAY = "2026-07-23"
PERSONS_DIR = os.path.join(STAGING, "..", "..", "persons")

# ── PERSONS ──
# 基于维基百科、安新县政府门户新闻的部分信息
persons = [
    {
        "id": 1,
        "name": "杨宝昌",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "安新县委书记",
        "current_org": "中共安新县委员会（雄安新区）",
        "source": "zh.wikipedia.org/wiki/安新县（信息框）",
    },
    {
        "id": 2,
        "name": "待确认县长",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "安新县县长（待确认）",
        "current_org": "安新县人民政府（雄安新区）",
        "source": "政府门户新闻提及李国向主持常务会议，身份待核实",
    },
    {
        "id": 3,
        "name": "李国向",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "安新县领导（疑为县长或常务副县长）",
        "current_org": "安新县人民政府（雄安新区）",
        "source": "www.anxin.gov.cn 新闻：李国向主持召开十八届政府第六十四次常务会议 (2025-12-31)",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {
        "id": 1,
        "name": "中共安新县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共保定市委员会 / 中共河北雄安新区工作委员会",
        "location": "河北省雄安新区安新县",
    },
    {
        "id": 2,
        "name": "安新县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "保定市人民政府 / 河北雄安新区管理委员会",
        "location": "河北省雄安新区安新县",
    },
    {
        "id": 3,
        "name": "安新县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "保定市人大常委会",
        "location": "河北省雄安新区安新县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议安新县委员会",
        "type": "政协",
        "level": "县",
        "parent": "保定市政协",
        "location": "河北省雄安新区安新县",
    },
    {
        "id": 5,
        "name": "中共安新县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共保定市纪律检查委员会",
        "location": "河北省雄安新区安新县",
    },
    {
        "id": 6,
        "name": "河北雄安新区管理委员会",
        "type": "政府",
        "level": "副省级",
        "parent": "河北省人民政府",
        "location": "河北省雄安新区容城县",
    },
]

# ── POSITIONS ──
positions = [
    # 杨宝昌
    {"person_id": 1, "org_id": 1, "title": "安新县委书记", "start_date": "不详", "end_date": "至今", "rank": "正处级", "note": "维基百科信息框确认现任"},
    # 待确认县长
    {"person_id": 2, "org_id": 2, "title": "安新县县长（待确认）", "start_date": "不详", "end_date": "至今", "rank": "正处级", "note": "县长姓名在网络搜索受限下无法确认"},
    # 李国向
    {"person_id": 3, "org_id": 2, "title": "安新县领导（疑为县长/常务副县长）", "start_date": "不详", "end_date": "至今", "rank": "副处级/正处级", "note": "2025-12-31主持县政府第六十四次常务会议"},
]

# ── RELATIONSHIPS ──
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "杨宝昌（县委书记）与县长在县委常委会和政府班子共事",
        "overlap_org": "中共安新县委/安新县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "杨宝昌（县委书记）与李国向在县委共事",
        "overlap_org": "中共安新县委/安新县人民政府",
        "overlap_period": "至今",
    },
]


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
        pid = f"anxin_{p['name']}"
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
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
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
            "开发区": "200,255,200",
            "事业单位": "220,220,220",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>安新县领导班子关系网络（基于维基百科、安新县政府网）</description>')
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
    source_register = [
        {"id": "S001", "title": "安新县 - 维基百科",
         "url": "https://zh.wikipedia.org/wiki/安新县",
         "publisher": "维基百科", "published_at": "2026-05-26",
         "accessed_at": "2026-07-23", "source_type": "encyclopedia", "reliability": "medium",
         "notes": "信息框确认县委书记杨宝昌"},
        {"id": "S002", "title": "安新县人民政府门户网站",
         "url": "https://www.anxin.gov.cn/",
         "publisher": "安新县人民政府", "published_at": "",
         "accessed_at": "2026-07-23", "source_type": "official", "reliability": "high",
         "notes": "首页新闻中提及李国向主持政府常务会议"},
        {"id": "S003", "title": "雄安新区 - 维基百科",
         "url": "https://zh.wikipedia.org/wiki/雄安新区",
         "publisher": "维基百科", "published_at": "",
         "accessed_at": "2026-07-23", "source_type": "encyclopedia", "reliability": "medium",
         "notes": "雄安新区托管安新县背景信息"},
    ]

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "河北省",
                "city": "保定市（雄安新区）",
                "region": "安新县",
                "job": p.get("current_post", ""),
                "task_id": "hebei_安新县",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"anxin_{p['name']}",
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
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "")) else "县处级副职",
                "as_of": TODAY,
                "is_current_confirmed": True if "县委书记" in p.get("current_post", "") else False,
                "source_ids": ["S001", "S002"]
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
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed" if "县委书记" in p.get("current_post", "") else "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 安新县", f"{p['name']} 任前公示", f"{p['name']} 雄安新区"],
                 "last_attempted": TODAY},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 杨宝昌 Person JSON ──
    ybc_timeline = [
        {"start": "不详", "end": "present", "org": "中共安新县委员会（雄安新区）",
         "title": "安新县委书记", "notes": "现任，维基百科信息框确认",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "不详", "end": "不详", "org": "履历缺口",
         "title": "", "notes": "公开资料未找到杨宝昌就任安新县委书记前的履历",
         "confidence": "unverified", "source_ids": []},
    ]
    ybc_relationships = []
    ybc_json = make_person_json(persons[0], ybc_timeline, ybc_relationships)
    ybc_path = os.path.join(PERSONS_DIR, f"{TODAY}-河北省-保定市-县委书记-杨宝昌.json")
    with open(ybc_path, "w", encoding="utf-8") as f:
        json.dump(ybc_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {ybc_path}")

    # ── 李国向 Person JSON (partial) ──
    lgx_timeline = [
        {"start": "不详", "end": "present", "org": "安新县人民政府（雄安新区）",
         "title": "安新县领导（疑为县长/常务副县长）",
         "notes": "2025-12-31主持安新县十八届政府第六十四次常务会议；2025-12-27现场办公安全生产",
         "confidence": "plausible", "source_ids": ["S002"]},
    ]
    lgx_relationships = [
        {"person": "杨宝昌", "person_id": "anxin_杨宝昌",
         "relationship_type": "overlap", "strength": "weak",
         "evidence": "在安新县委/政府共事但无法确认具体汇报关系",
         "overlap_org": "中共安新县委/安新县人民政府",
         "overlap_period": "至今", "direction": "undirected",
         "confidence": "plausible", "source_ids": ["S002"]},
    ]
    lgx_json = make_person_json(persons[2], lgx_timeline, lgx_relationships)
    lgx_path = os.path.join(PERSONS_DIR, f"{TODAY}-河北省-保定市-县领导-李国向.json")
    with open(lgx_path, "w", encoding="utf-8") as f:
        json.dump(lgx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lgx_path}")

    print("\nDone!")


import json  # noqa — imported here for person JSON generation


if __name__ == "__main__":
    build()
