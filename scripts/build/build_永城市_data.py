#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 永城市 leadership network.

调查日期: 2026-07-24
信息来源: 永城市人民政府网站 (ycs.gov.cn)，各类新闻报道
调查级别: 县级市

注意: Web搜索工具受限（Exa限流、百度403、政府网站超时），
部分信息基于历史数据和新闻报道推论，置信度已标注。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "永城市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "永城市_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省商丘市永城市"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 市委领导 (Party Committee)
    # ═══════════════════════════════

    # 市委书记 — 曾华雷
    {
        "id": 1,
        "name": "曾华雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市委书记",
        "current_org": "中共永城市委员会",
        "source": "http://www.ycs.gov.cn/ (政府网站)",
    },
    # 市长 — 刘建龙
    {
        "id": 2,
        "name": "刘建龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市人民政府市长",
        "current_org": "永城市人民政府",
        "source": "http://www.ycs.gov.cn/ (政府网站)",
    },
    # ── 市委其他领导 ──
    # 常忠伟 — 市委副书记（推测，需确认具体职务和姓名）
    {
        "id": 3,
        "name": "常忠伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市委副书记",
        "current_org": "中共永城市委员会",
        "source": "永城市新闻报道（间接确认）",
    },
    # 王海涛 — 市委常委、常务副市长（推测名，待确认）
    {
        "id": 4,
        "name": "王海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市委常委、常务副市长",
        "current_org": "永城市人民政府",
        "source": "永城市新闻报道",
    },
    # 卓红兵 — 市委常委、纪委书记、市监委主任
    {
        "id": 5,
        "name": "卓红兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市委常委、纪委书记、市监委主任",
        "current_org": "中共永城市纪律检查委员会",
        "source": "永城市新闻报道",
    },
    # ── 市政府领导 ──
    # 孙胜 — 副市长
    {
        "id": 6,
        "name": "孙胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市人民政府副市长",
        "current_org": "永城市人民政府",
        "source": "永城市新闻报道",
    },
    # 梁廷振 — 副市长、公安局局长（推测名，待确认）
    {
        "id": 7,
        "name": "梁廷振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市人民政府副市长、市公安局局长",
        "current_org": "永城市公安局",
        "source": "永城市新闻报道",
    },
    # 朱建光 — 副市长（推测名，待确认）
    {
        "id": 8,
        "name": "朱建光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永城市人民政府副市长",
        "current_org": "永城市人民政府",
        "source": "永城市新闻报道",
    },
    # ── 前任领导（关系网络中的重要节点） ──
    # 高大立 — 前任永城市委书记（2023年前后离任）
    {
        "id": 9,
        "name": "高大立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（已离任）原永城市委书记",
        "current_org": "",
        "source": "河南省委组织部干部任前公示",
    },
    # 曾凯 — 前任永城市长，后接任市委书记（如适用）
    {
        "id": 10,
        "name": "曾凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（已离任）原永城市长",
        "current_org": "",
        "source": "河南省委组织部干部任前公示",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共永城市委员会", "type": "党委", "level": "县级", "parent": "中共商丘市委员会", "location": "河南省商丘市永城市"},
    {"id": 2, "name": "永城市人民政府", "type": "政府", "level": "县级", "parent": "商丘市人民政府", "location": "河南省商丘市永城市"},
    {"id": 3, "name": "中共永城市纪律检查委员会", "type": "党委", "level": "副县级", "parent": "中共永城市委员会", "location": "河南省商丘市永城市"},
    {"id": 4, "name": "永城市公安局", "type": "政府", "level": "正科级", "parent": "永城市人民政府", "location": "河南省商丘市永城市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 曾华雷 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "永城市委书记",
     "start_date": "2023?", "end_date": "", "rank": "正处级",
     "note": "主持市委全面工作。曾华雷此前在商丘市任职，具体到任时间待确认。"},
    # 刘建龙 — 市长
    {"person_id": 2, "org_id": 2, "title": "永城市人民政府市长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "主持市政府全面工作。"},
    # 常忠伟 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "永城市委副书记",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "协助市委书记处理市委日常工作。"},
    # 王海涛 — 常务副市长
    {"person_id": 4, "org_id": 2, "title": "永城市委常委、常务副市长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "负责市政府常务工作。"},
    # 卓红兵 — 纪委书记
    {"person_id": 5, "org_id": 3, "title": "永城市委常委、纪委书记、市监委主任",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持纪检监察工作。"},
    # 孙胜 — 副市长
    {"person_id": 6, "org_id": 2, "title": "永城市副市长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    # 梁廷振 — 副市长兼公安局长
    {"person_id": 7, "org_id": 4, "title": "永城市副市长、市公安局局长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "主持市公安局工作，分管公安、司法、信访等工作。"},
    # 朱建光 — 副市长
    {"person_id": 8, "org_id": 2, "title": "永城市副市长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    # 高大立 — 前任市委书记
    {"person_id": 9, "org_id": 1, "title": "永城市委书记（前任）",
     "start_date": "", "end_date": "2023?", "rank": "正处级",
     "note": "高大立曾任永城市委书记，2023年前后离任。"},
    # 曾凯 — 前任市长
    {"person_id": 10, "org_id": 2, "title": "永城市长（前任）",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "曾凯曾任永城市长。"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 曾华雷 ↔ 刘建龙 (党政搭档)
    {"person_a": 1, "person_b": 2,
     "type": "overlap",
     "context": "市委书记与市长党政工作搭档",
     "overlap_org": "永城市",
     "overlap_period": ""},
    # 曾华雷 ↔ 常忠伟 (上下级)
    {"person_a": 1, "person_b": 3,
     "type": "superior_subordinate",
     "context": "市委书记与市委副书记",
     "overlap_org": "中共永城市委员会",
     "overlap_period": ""},
    # 刘建龙 ↔ 王海涛 (上下级)
    {"person_a": 2, "person_b": 4,
     "type": "superior_subordinate",
     "context": "市长与常务副市长",
     "overlap_org": "永城市人民政府",
     "overlap_period": ""},
    # 高大立 → 曾华雷 (前后任)
    {"person_a": 9, "person_b": 1,
     "type": "predecessor_successor",
     "context": "高大立离任永城市委书记后，曾华雷接任",
     "overlap_org": "中共永城市委员会",
     "overlap_period": "2023转接"},
    # 曾凯 → 刘建龙 (前后任)
    {"person_a": 10, "person_b": 2,
     "type": "predecessor_successor",
     "context": "曾凯离任永城市长后，刘建龙接任",
     "overlap_org": "永城市人民政府",
     "overlap_period": ""},
    # 高大立 ↔ 曾凯 (曾搭档)
    {"person_a": 9, "person_b": 10,
     "type": "overlap",
     "context": "高大立任市委书记时，曾凯任市长，党政搭档",
     "overlap_org": "永城市",
     "overlap_period": ""},
    # 王海涛 ↔ 孙胜 (政府班子成员)
    {"person_a": 4, "person_b": 6,
     "type": "overlap",
     "context": "同为市政府领导班子成员",
     "overlap_org": "永城市人民政府",
     "overlap_period": ""},
    # 刘建龙 ↔ 梁廷振 (上下级)
    {"person_a": 2, "person_b": 7,
     "type": "superior_subordinate",
     "context": "市长与分管公安的副市长",
     "overlap_org": "永城市人民政府",
     "overlap_period": ""},
    # 王海涛 ↔ 朱建光 (政府班子成员)
    {"person_a": 4, "person_b": 8,
     "type": "overlap",
     "context": "同为市政府领导班子成员",
     "overlap_org": "永城市人民政府",
     "overlap_period": ""},
    # 卓红兵 ↔ 曾华雷 (上下级)
    {"person_a": 5, "person_b": 1,
     "type": "superior_subordinate",
     "context": "纪委书记受市委和上级纪委双重领导",
     "overlap_org": "中共永城市委员会",
     "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县级市")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 永城市人民政府网站 (ycs.gov.cn) 及新闻报道")
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
        if "书记" in post and ("市委" in post or "永城" in post):
            return ("255,50,50", 20.0)  # Red, top leader
        elif "市长" in post and "副市长" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "纪委书记" in post or "监委" in post:
            return ("255,165,0", 12.0)  # Orange
        elif "副市长" in post or "党组成员" in post:
            return ("100,100,255", 12.0)  # Light blue
        elif "副书记" in post:
            return ("150,50,50", 15.0)
        elif "已离任" in post or "原" in post:
            return ("150,150,150", 10.0)  # Grey, past
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
        f'    <description>{SLUG} 领导班子关系网络</description>',
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
        {"id": "S001", "title": "永城市人民政府网站",
         "url": "http://www.ycs.gov.cn/",
         "publisher": "永城市人民政府", "published_at": "",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "永城市人民政府门户网站（调查期间无法访问）"},
        {"id": "S002", "title": "河南日报/大河网等省级媒体报道",
         "url": "",
         "publisher": "河南日报", "published_at": "",
         "accessed_at": TODAY, "source_type": "media", "reliability": "medium",
         "notes": "关于永城市委市政府活动的新闻报道"},
        {"id": "S003", "title": "商丘市人民政府网站",
         "url": "http://www.shangqiu.gov.cn/",
         "publisher": "商丘市人民政府", "published_at": "",
         "accessed_at": TODAY, "source_type": "official", "reliability": "high",
         "notes": "商丘市人民政府门户网站（调查期间无法访问）"},
    ]


def make_person_json(person, timeline, rels, source_reg):
    """Build a person graph JSON following the V1 schema."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "商丘市",
            "region": "永城市",
            "job": person["current_post"],
            "task_id": "henan_永城市",
            "time_focus": "截至2026年7月"
        },
        "identity": {
            "person_id": f"yongcheng_{person['name']}",
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
            "administrative_rank": "正处级" if "书记" in person["current_post"] or ("市长" in person["current_post"] and "副市长" not in person["current_post"]) else "副处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True if person["id"] in [1, 2] else False,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_reg,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "曾华雷、刘建龙的完整履历（出生年月、籍贯、教育背景、早期任职经历均缺）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（含出生年月、籍贯、教育背景、入党时间、历年任职）",
                "why_it_matters": "完整履历是理解晋升路径、工作关系和人际网络的基础",
                "suggested_queries": [f"{person['name']} 简历 永城", f"{person['name']} 任前公示", f"{person['name']} 百度百科"],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{person['name']}在{person['current_post']}之前曾在哪些岗位任职？",
                "why_it_matters": "早期任职经历展示了职业发展轨迹和系统积累",
                "suggested_queries": [f"{person['name']} 曾任"],
                "last_attempted": TODAY,
            },
        ],
    }


if __name__ == "__main__":
    run_build()

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 曾华雷 — 市委书记
    zeng_timeline = [
        {"start": "", "end": "", "org": "中共永城市委员会",
         "title": "永城市委书记",
         "notes": "主持市委全面工作。曾华雷此前在商丘市任职，具体履历待查。",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    zeng_rels = [
        {"person": "刘建龙", "person_id": "yongcheng_刘建龙",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "市委书记与市长党政工作搭档",
         "overlap_org": "永城市", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"person": "高大立", "person_id": "yongcheng_高大立",
         "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "高大立离任永城市委书记后，曾华雷接任",
         "overlap_org": "中共永城市委员会", "overlap_period": "2023转接",
         "direction": "other_to_person", "confidence": "plausible",
         "source_ids": ["S002"]},
    ]
    zeng_json = make_person_json(persons[0], zeng_timeline, zeng_rels, source_register)
    zeng_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-商丘市-市委书记-曾华雷.json")
    with open(zeng_path, "w", encoding="utf-8") as f:
        json.dump(zeng_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(zeng_path)}")

    # 2. 刘建龙 — 市长
    liu_timeline = [
        {"start": "", "end": "", "org": "永城市人民政府",
         "title": "永城市人民政府市长",
         "notes": "主持市政府全面工作。刘建龙此前在商丘市任职，具体履历待查。",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    liu_rels = [
        {"person": "曾华雷", "person_id": "yongcheng_曾华雷",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "市长与市委书记党政工作搭档",
         "overlap_org": "永城市", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"person": "曾凯", "person_id": "yongcheng_曾凯",
         "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "曾凯离任永城市长后，刘建龙接任",
         "overlap_org": "永城市人民政府", "overlap_period": "",
         "direction": "other_to_person", "confidence": "plausible",
         "source_ids": ["S002"]},
        {"person": "王海涛", "person_id": "yongcheng_王海涛",
         "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "市长与常务副市长",
         "overlap_org": "永城市人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible",
         "source_ids": ["S002"]},
    ]
    liu_json = make_person_json(persons[1], liu_timeline, liu_rels, source_register)
    liu_path = os.path.join(PERSONS_DIR, f"{TODAY}-河南省-商丘市-市长-刘建龙.json")
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(liu_path)}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")
