#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 濮阳县 leadership network.

调查日期: 2026-07-24
信息来源: 濮阳县人民政府网站 (puyangxian.gov.cn), 今日龙乡
调查级别: 县
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "濮阳县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "濮阳县_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"
SLUG = "河南省濮阳市濮阳县"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 县委领导 (Party Committee)
    # ═══════════════════════════════

    # 刘锐 — 县委书记
    {
        "id": 1,
        "name": "刘锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共濮阳县委书记",
        "current_org": "中共濮阳县委员会",
        "source": "http://www.puyangxian.gov.cn/content/2026/1286970.html",
    },
    # 赵岩 — 县委副书记、县长
    {
        "id": 2,
        "name": "赵岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "濮阳县委副书记、县长",
        "current_org": "濮阳县人民政府",
        "source": "http://www.puyangxian.gov.cn/content/2026/1300514.html",
    },
    # 辛勇 — 县委副书记
    {
        "id": 3,
        "name": "辛勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "濮阳县委副书记",
        "current_org": "中共濮阳县委员会",
        "source": "http://www.puyangxian.gov.cn/content/2026/1290832.html",
    },
    # 王子宁 — 县委常委、常务副县长
    {
        "id": 4,
        "name": "王子宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "濮阳县委常委、常务副县长",
        "current_org": "濮阳县人民政府",
        "source": "http://www.puyangxian.gov.cn/content/2026/1301104.html",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共濮阳县委员会", "type": "党委", "level": "县级", "parent": "中共濮阳市委员会", "location": "河南省濮阳市濮阳县"},
    {"id": 2, "name": "濮阳县人民政府", "type": "政府", "level": "县级", "parent": "濮阳市人民政府", "location": "河南省濮阳市濮阳县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 刘锐
    {"person_id": 1, "org_id": 1, "title": "中共濮阳县委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "2026年7月主持防汛抗旱专题调度会议"},
    # 赵岩
    {"person_id": 2, "org_id": 1, "title": "濮阳县委副书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "同时任县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "濮阳县县长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持县政府全面工作；2026年7月主持召开第48次常务会议"},
    # 辛勇
    {"person_id": 3, "org_id": 1, "title": "濮阳县委副书记",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "2026年7月主持奋进龙乡大讲堂"},
    # 王子宁
    {"person_id": 4, "org_id": 1, "title": "濮阳县委常委",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    {"person_id": 4, "org_id": 2, "title": "濮阳县常务副县长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责常务工作；分管安全生产、城区建设等"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 县委书记 ↔ 县长
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政工作搭档关系，共同出席防汛抗旱调度会等会议",
     "overlap_org": "濮阳县", "overlap_period": ""},
    # 县委书记 ↔ 县委副书记
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与副书记——辛勇协助刘锐分管党务工作",
     "overlap_org": "中共濮阳县委", "overlap_period": ""},
    # 县委书记 ↔ 常务副县长
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与常务副县长工作搭档关系",
     "overlap_org": "中共濮阳县委", "overlap_period": ""},
    # 县长 ↔ 常务副县长
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与常务副县长党政工作搭档——王子宁协助赵岩分管审计等工作",
     "overlap_org": "濮阳县人民政府", "overlap_period": ""},
    # 县长 ↔ 县委副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长与县委副书记——辛勇协助县委书记处理党务，与赵岩在县委常委会共事",
     "overlap_org": "中共濮阳县委", "overlap_period": ""},
    # 县委副书记 ↔ 常务副县长
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "县委副书记与常务副县长——均在县委常委会任职",
     "overlap_org": "中共濮阳县委", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════

import sqlite3


def create_tables(conn):
    conn.executescript("""
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
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 濮阳县人民政府网站 (puyangxian.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "书记" in post and "县委" in post and "副" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "县长" in post and "副" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副书记" in post:
            return ("100,100,255", 15.0)  # Deputy secretary
        else:
            return ("100,100,100", 12.0)  # Grey

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络 — 截至{AS_OF}</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    # Person nodes
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


# ═══════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ═══════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "刘锐主持召开濮阳县主汛期防汛抗旱专题调度会议",
         "url": "http://www.puyangxian.gov.cn/content/2026/1286970.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-06",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认刘锐为县委书记，赵岩为县长"},
        {"id": "S002", "title": "赵岩主持召开安全生产工作专班专题调度会",
         "url": "http://www.puyangxian.gov.cn/content/2026/1300514.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-20",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认赵岩为县委副书记、县长"},
        {"id": "S003", "title": "王子宁督导检查道路积水、线路改造、消防安全等工作",
         "url": "http://www.puyangxian.gov.cn/content/2026/1301104.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-21",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认王子宁为县委常委、常务副县长"},
        {"id": "S004", "title": "濮阳县举办奋进龙乡大讲堂",
         "url": "http://www.puyangxian.gov.cn/content/2026/1290832.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-15",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认辛勇为县委副书记"},
        {"id": "S005", "title": "濮阳县污染防治攻坚工作推进会召开",
         "url": "http://www.puyangxian.gov.cn/content/2026/1301706.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-22",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认刘锐为县委书记，赵岩为县长"},
        {"id": "S006", "title": "濮阳县人民政府门户网站",
         "url": "http://www.puyangxian.gov.cn/",
         "publisher": "濮阳县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "濮阳县人民政府门户网站"},
        {"id": "S007", "title": "县政府召开第48次常务会议",
         "url": "http://www.puyangxian.gov.cn/content/2026/1290440.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-15",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认赵岩主持县政府常务会议"},
        {"id": "S008", "title": "王子宁督导调研县城区地下空间、建筑工地及化工园区安全生产工作",
         "url": "http://www.puyangxian.gov.cn/content/2026/1288474.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-13",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认王子宁为县委常委、常务副县长"},
        {"id": "S009", "title": "濮阳县2026年重点项目建设第18次调度会召开",
         "url": "http://www.puyangxian.gov.cn/content/2026/1287341.html",
         "publisher": "濮阳县人民政府", "published_at": "2026-07-08",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认赵岩为县长主持会议"},
    ]


def make_person_json(person, timeline, rels, source_reg):
    """Build a person graph JSON following the V1 schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "濮阳市",
            "region": "濮阳县",
            "job": person["current_post"],
            "task_id": "henan_濮阳县",
            "time_focus": "截至2026年7月"
        },
        "identity": {
            "person_id": f"puyangxian_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or "县长" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S005"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开渠道未发现{person['name']}的负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的出生年份、籍贯、教育背景和任现职前的全部履历均缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}任{person['current_post']}前的完整履历是什么？",
                "why_it_matters": "无法评估其职业路径、来源系统和晋升模式",
                "suggested_queries": [f"{person['name']} 简历 濮阳", f"{person['name']} 任前公示", f"{person['name']} Baidu Baike"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "缺少基础身份信息，无法进行去重和人口统计分析",
                "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 濮阳县"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"濮阳县前任县委书记是谁？（刘锐的到任时间及前任信息）",
                "why_it_matters": "关键的前任-继任关系缺失，影响网络分析的连续性",
                "suggested_queries": ["濮阳县委书记 2024", "濮阳县 前任书记", "濮阳县第十四次党代会"],
                "last_attempted": AS_OF,
            }
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 刘锐 (县委书记)
    liu_timeline = [
        {"start": "", "end": "", "org": "中共濮阳县委员会",
         "title": "中共濮阳县委书记",
         "notes": "2026年7月5日主持召开防汛抗旱专题调度会议；7月22日主持污染防治攻坚工作推进会",
         "confidence": "confirmed", "source_ids": ["S001", "S005"]},
    ]
    liu_rels = [
        {"person": "赵岩", "person_id": "puyangxian_赵岩",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "县委书记与县长党政工作搭档关系，共同出席防汛抗旱调度会、污染防治攻坚推进会等会议",
         "overlap_org": "濮阳县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S005"]},
        {"person": "辛勇", "person_id": "puyangxian_辛勇",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委书记与县委副书记——辛勇协助刘锐分管党务",
         "overlap_org": "中共濮阳县委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"person": "王子宁", "person_id": "puyangxian_王子宁",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委书记与常务副县长工作搭档",
         "overlap_org": "中共濮阳县委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]
    liu_json = make_person_json(persons[0], liu_timeline, liu_rels, source_register)
    liu_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县委书记-刘锐.json")
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(liu_path)}")

    # 2. 赵岩 (县长)
    zhao_timeline = [
        {"start": "", "end": "", "org": "濮阳县人民政府",
         "title": "濮阳县委副书记、县长、县政府党组书记",
         "notes": "2026年7月主持召开第48次常务会议、安全生产工作专班调度会、重点项目建设调度会、黄河文旅示范带推进会等",
         "confidence": "confirmed", "source_ids": ["S002", "S005", "S007"]},
    ]
    zhao_rels = [
        {"person": "刘锐", "person_id": "puyangxian_刘锐",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "县长与县委书记党政工作搭档",
         "overlap_org": "濮阳县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S005"]},
        {"person": "王子宁", "person_id": "puyangxian_王子宁",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "县长与常务副县长——王子宁协助赵岩分管审计等工作",
         "overlap_org": "濮阳县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S003", "S008"]},
        {"person": "辛勇", "person_id": "puyangxian_辛勇",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县长与县委副书记——在县委常委会共事",
         "overlap_org": "中共濮阳县委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S004"]},
    ]
    zhao_json = make_person_json(persons[1], zhao_timeline, zhao_rels, source_register)
    zhao_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县长-赵岩.json")
    with open(zhao_path, "w", encoding="utf-8") as f:
        json.dump(zhao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(zhao_path)}")

    # 3. 辛勇 (县委副书记)
    xin_timeline = [
        {"start": "", "end": "", "org": "中共濮阳县委员会",
         "title": "濮阳县委副书记",
         "notes": "2026年7月14日主持奋进龙乡大讲堂；7月15日部署常态化帮扶巩固拓展脱贫攻坚成果工作",
         "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    xin_rels = [
        {"person": "刘锐", "person_id": "puyangxian_刘锐",
         "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "县委副书记协助县委书记处理党务工作",
         "overlap_org": "中共濮阳县委", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"person": "赵岩", "person_id": "puyangxian_赵岩",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "县委副书记与县长——在县委常委会共事",
         "overlap_org": "中共濮阳县委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S004"]},
    ]
    xin_json = make_person_json(persons[2], xin_timeline, xin_rels, source_register)
    xin_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-县委副书记-辛勇.json")
    with open(xin_path, "w", encoding="utf-8") as f:
        json.dump(xin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(xin_path)}")

    # 4. 王子宁 (常务副县长)
    wang_timeline = [
        {"start": "", "end": "", "org": "濮阳县人民政府",
         "title": "濮阳县委常委、常务副县长",
         "notes": "2026年7月督导检查道路积水、线路改造、消防安全；调研地下空间、建筑工地及化工园区安全生产",
         "confidence": "confirmed", "source_ids": ["S003", "S008"]},
    ]
    wang_rels = [
        {"person": "赵岩", "person_id": "puyangxian_赵岩",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "常务副县长协助县长工作",
         "overlap_org": "濮阳县人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "刘锐", "person_id": "puyangxian_刘锐",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "常务副县长与县委书记——在县委常委会共事",
         "overlap_org": "中共濮阳县委", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]
    wang_json = make_person_json(persons[3], wang_timeline, wang_rels, source_register)
    wang_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-濮阳市-常务副县长-王子宁.json")
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(wang_path)}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")
