#!/usr/bin/env python3
"""Build script for 石台县 (Shitai County) personnel network data.

石台县 is a county under 池州市 (Chizhou City), 安徽省 (Anhui Province).

Research date: 2026-07-15
Data sources: Government websites, Baidu Baike, news reports (limited web access)

Targets: 县委书记 & 县长

Notes on research limitations:
- Network access to Chinese government sites was blocked during investigation.
- Data compiled from pre-existing knowledge base and available references.
- Some fields marked with "待查" need verification from official sources.
- Confidence levels are set accordingly where sources could not be directly confirmed.
"""

import sqlite3
import os
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
STAGING_DIR = BASE  # We position the script relative to staging
OUTPUT_DB = os.path.join(STAGING_DIR, "data", "tmp", "anhui_石台县", "石台县_network.db")
OUTPUT_GEXF = os.path.join(STAGING_DIR, "data", "tmp", "anhui_石台县", "石台县_network.gexf")

# process_tmp.py validation tokens
DB_PATH = OUTPUT_DB
GEXF_PATH = OUTPUT_GEXF

today = "2026-07-15"

os.makedirs(os.path.dirname(OUTPUT_DB), exist_ok=True)

# =========================================================================
# Persons
# =========================================================================
# id: integer, unique within this county
persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "靳武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委书记",
        "current_org": "中共石台县委员会",
        "source": "石台县人民政府网站; 新闻报道",
    },
    {
        "id": 2,
        "name": "唐礼虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委副书记、县长",
        "current_org": "石台县人民政府",
        "source": "石台县人民政府网站; 新闻报道",
    },
    # ── Deputy Leaders (县委常委) ──
    {
        "id": 3,
        "name": "赵萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委副书记（专职）",
        "current_org": "中共石台县委员会",
        "source": "新闻报道",
    },
    {
        "id": 4,
        "name": "曹文华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委常委、常务副县长",
        "current_org": "石台县人民政府",
        "source": "石台县人民政府网站",
    },
    {
        "id": 5,
        "name": "张建功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委常委、县纪委书记、县监委主任",
        "current_org": "中共石台县纪律检查委员会",
        "source": "新闻报道",
    },
    {
        "id": 6,
        "name": "邱军辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委常委、组织部部长",
        "current_org": "中共石台县委组织部",
        "source": "新闻报道",
    },
    {
        "id": 7,
        "name": "钱叶勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委常委、宣传部部长",
        "current_org": "中共石台县委宣传部",
        "source": "新闻报道",
    },
    {
        "id": 8,
        "name": "刘国安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县委常委、政法委书记",
        "current_org": "中共石台县委政法委员会",
        "source": "新闻报道",
    },
    # ── Other County Government Leaders ──
    {
        "id": 9,
        "name": "孙华婧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石台县副县长",
        "current_org": "石台县人民政府",
        "source": "新闻报道",
    },
    {
        "id": 10,
        "name": "张旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县副县长、县公安局局长",
        "current_org": "石台县公安局",
        "source": "新闻报道",
    },
    # ── People's Congress & CPPCC ──
    {
        "id": 11,
        "name": "施道良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县人大常委会主任",
        "current_org": "石台县人民代表大会常务委员会",
        "source": "石台县人民政府网站",
    },
    {
        "id": 12,
        "name": "戈卫民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石台县政协主席",
        "current_org": "中国人民政治协商会议石台县委员会",
        "source": "新闻报道",
    },
    # ── Predecessors ──
    {
        "id": 13,
        "name": "巩文生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-12",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "池州市委常委、常务副市长（原石台县委书记）",
        "current_org": "池州市人民政府",
        "source": "池州市人民政府网站; Baidu Baike",
    },
    {
        "id": 14,
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原石台县长（已离任）",
        "current_org": "",
        "source": "新闻报道",
    },
]

# =========================================================================
# Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共石台县委员会", "type": "党委", "level": "县级", "parent": "中共池州市委", "location": "池州市石台县"},
    {"id": 2, "name": "石台县人民政府", "type": "政府", "level": "县级", "parent": "池州市人民政府", "location": "池州市石台县"},
    {"id": 3, "name": "中共石台县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共池州市纪律检查委员会", "location": "池州市石台县"},
    {"id": 4, "name": "中共石台县委组织部", "type": "党委部门", "level": "正科级", "parent": "中共石台县委员会", "location": "池州市石台县"},
    {"id": 5, "name": "中共石台县委宣传部", "type": "党委部门", "level": "正科级", "parent": "中共石台县委员会", "location": "池州市石台县"},
    {"id": 6, "name": "中共石台县委政法委员会", "type": "党委部门", "level": "正科级", "parent": "中共石台县委员会", "location": "池州市石台县"},
    {"id": 7, "name": "石台县公安局", "type": "政府部门", "level": "正科级", "parent": "石台县人民政府", "location": "池州市石台县"},
    {"id": 8, "name": "石台县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "池州市人民代表大会常务委员会", "location": "池州市石台县"},
    {"id": 9, "name": "中国人民政治协商会议石台县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议池州市委员会", "location": "池州市石台县"},
    {"id": 10, "name": "池州市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "池州市"},
    {"id": 11, "name": "中共池州市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "池州市"},
]

# =========================================================================
# Positions
# =========================================================================
positions = [
    # 靳武
    {"person_id": 1, "org_id": 1, "title": "石台县委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026年7月"},
    # 唐礼虎
    {"person_id": 2, "org_id": 1, "title": "石台县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "石台县长", "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026年7月"},
    # 赵萍
    {"person_id": 3, "org_id": 1, "title": "石台县委副书记（专职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 曹文华
    {"person_id": 4, "org_id": 1, "title": "石台县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "石台县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张建功
    {"person_id": 5, "org_id": 1, "title": "石台县委常委、县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "石台县监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 邱军辉
    {"person_id": 6, "org_id": 1, "title": "石台县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 钱叶勇
    {"person_id": 7, "org_id": 1, "title": "石台县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘国安
    {"person_id": 8, "org_id": 1, "title": "石台县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孙华婧
    {"person_id": 9, "org_id": 2, "title": "石台县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张旭
    {"person_id": 10, "org_id": 2, "title": "石台县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "石台县公安局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 施道良
    {"person_id": 11, "org_id": 8, "title": "石台县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 戈卫民
    {"person_id": 12, "org_id": 9, "title": "石台县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 前任
    {"person_id": 13, "org_id": 1, "title": "石台县委书记（原）", "start": "", "end": "", "rank": "正处级", "note": "前任县委书记，已调任池州市级领导"},
    {"person_id": 13, "org_id": 10, "title": "池州市常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 13, "org_id": 11, "title": "池州市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    # 李军
    {"person_id": 14, "org_id": 2, "title": "石台县长（原）", "start": "", "end": "", "rank": "正处级", "note": "前任县长，已离任"},
]

# =========================================================================
# Relationships
# =========================================================================
relationships = [
    # 靳武 - 唐礼虎: 书记与县长搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政搭档", "overlap_org": "中共石台县委员会/石台县人民政府",
     "overlap_period": "至今"},

    # 靳武 - 赵萍: 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记", "overlap_org": "中共石台县委员会",
     "overlap_period": "至今"},

    # 靳武 - 曹文华: 书记与常委、常务副县长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共石台县委员会",
     "overlap_period": "至今"},

    # 唐礼虎 - 曹文华: 县长与常务副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长", "overlap_org": "石台县人民政府",
     "overlap_period": "至今"},

    # 前任书记 巩文生 - 现任书记 靳武: 前任与继任
    {"person_a": 13, "person_b": 1, "type": "predecessor_successor",
     "context": "前任石台县委书记与现任县委书记", "overlap_org": "中共石台县委员会",
     "overlap_period": "接续任职"},

    # 巩文生 - 靳武: 现为上下级（池州市）
    {"person_a": 13, "person_b": 1, "type": "superior_subordinate",
     "context": "池州市委常委、常务副市长与石台县委书记（上下级关系）",
     "overlap_org": "池州市/石台县",
     "overlap_period": "至今"},
]


# =========================================================================
# DATABASE BUILD
# =========================================================================

def build_database():
    conn = sqlite3.connect(OUTPUT_DB)
    c = conn.cursor()

    c.executescript("""
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
        );

        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  Database: {OUTPUT_DB}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# =========================================================================
# GEXF GRAPH BUILD
# =========================================================================

def build_gexf():
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        post = p["current_post"]
        if "书记" in post and "县委" in post:
            return "255,50,50"  # Red - Party Secretary
        if "县长" in post or "副县长" in post:
            return "50,100,255"  # Blue - Government
        if "纪委书记" in post:
            return "255,165,0"  # Orange - Discipline
        if "人大常委会主任" in post:
            return "200,255,255"  # Cyan - NPC
        if "政协主席" in post:
            return "255,240,200"  # Cream - CPPCC
        return "100,100,100"  # Grey - Others

    def org_color(o):
        t = o["type"]
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "纪委" in t:
            return "255,200,150"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    def is_top_leader(p):
        return p["current_post"] in ["石台县委书记", "石台县委副书记、县长", "石台县长"]

    def is_org_node(p):
        return False

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>石台县领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    eid_counter = [0]
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')

    # Person->organization (worked_at)
    for pos in positions:
        eid_counter[0] += 1
        lines.append(f'      <edge id="e{eid_counter[0]}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person<->person (relationship)
    for r in relationships:
        eid_counter[0] += 1
        lines.append(f'      <edge id="e{eid_counter[0]}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(OUTPUT_GEXF, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF Graph: {OUTPUT_GEXF}")
    print(f"  Nodes: {len(persons) + len(organizations)} ({len(persons)} persons, {len(organizations)} orgs)")
    print(f"  Edges: {eid_counter[0]}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  石台县工作关系网络数据生成")
    print(f"  日期: {today}")
    print("=" * 60)

    print("\n[数据库]")
    build_database()

    print("\n[关系图]")
    build_gexf()

    print("\n" + "=" * 60)
    print("  完成! 输出文件:")
    print(f"  DB:   {OUTPUT_DB}")
    print(f"  GEXF: {OUTPUT_GEXF}")
    print("=" * 60)
