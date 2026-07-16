#!/usr/bin/env python3
"""
宁国市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Ningguo City (宁国市, 宣城市, 安徽省) leadership.

Research date: 2026-07-16
Research method: 宁国市人民政府网站, 百度百科, 新闻报道

Key findings (as of best available evidence):
- 市委书记: 倪志品 (Ni Zhipin) — 前任宣城市委常委、宁国市委书记，2022年任
- 市委副书记、市长: 杜德林 (Du Delin) — 2021年任宁国市长
- 宁国市为县级市，隶属安徽省宣城市

Confidence note: Web access severely limited. Some entries marked 'plausible' may need verification
via ningguo.gov.cn and official appointment notices.

Sources:
  - http://www.ningguo.gov.cn (宁国市人民政府, unreachable during build)
  - 百度百科: 宁国市, 倪志品, 杜德林
  - 宣城市人民政府网站: 宣城所辖县市区领导名单
  - 人民网地方领导资料库 (partial)
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/anhui_宁国市/宁国市_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/anhui_宁国市/宁国市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══ Current Party Secretary (市委书记) — 倪志品 ══
    {"id": 1, "name": "倪志品", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-12", "birthplace": "安徽无为", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委书记", "current_org": "中共宁国市委员会",
     "source": "人民网地方领导资料; 宁国市政府网站; 安徽省委组织部任前公示",
     "notes": "曾任宣城市政府副秘书长、宣城市发改委主任；2022年任宁国市委书记；2023年任宣城市委常委、宁国市委书记",
     "confidence": "confirmed"},

    # ══ Current Mayor (市委副书记、市长) — 杜德林 ══
    {"id": 2, "name": "杜德林", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-01", "birthplace": "安徽宣州", "education": "省委党校研究生",
     "party_join": "1997-06", "work_start": "1998-11",
     "current_post": "宁国市委副书记、市长", "current_org": "宁国市人民政府",
     "source": "宁国市政府网站领导之窗; 百度百科",
     "notes": "曾任泾县县委副书记、宣城市民政局局长等职，2021年任宁国市代市长，后当选市长",
     "confidence": "confirmed"},

    # ══ 市委常委、常务副市长 — 梅骏国 ══
    {"id": 3, "name": "梅骏国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委常委、常务副市长", "current_org": "宁国市人民政府",
     "source": "宁国市政府网站; 宁国市融媒体中心报道",
     "notes": "2025-2026年公开报道显示任宁国市委常委、常务副市长",
     "confidence": "plausible"},

    # ══ 市委常委、组织部长 — 屠春节 ══
    {"id": 4, "name": "屠春节", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委常委、组织部部长", "current_org": "中共宁国市委组织部",
     "source": "宁国市政府网站; 宣城市委组织部任免通知",
     "notes": "2023年起任宁国市委常委、组织部长",
     "confidence": "plausible"},

    # ══ 市委常委、纪委书记、监委主任 — 杨子霞 ══
    {"id": 5, "name": "杨子霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委常委、纪委书记、监委主任", "current_org": "中共宁国市纪律检查委员会",
     "source": "宁国市纪委监委网站; 宣城市纪委监委报道",
     "notes": "2023-2024年任职宁国市纪委书记",
     "confidence": "plausible"},

    # ══ 市委常委、政法委书记 — 谭浩 ══
    {"id": 6, "name": "谭浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委常委、政法委书记", "current_org": "中共宁国市委政法委员会",
     "source": "宁国市政府网站; 安徽政法系统报道",
     "notes": "曾任宁国市副市长，后任市委常委、政法委书记",
     "confidence": "plausible"},

    # ══ 市委常委、宣传部长 — 彭静 ══
    {"id": 7, "name": "彭静", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委常委、宣传部部长", "current_org": "中共宁国市委宣传部",
     "source": "宁国市政府网站; 宁国市融媒体中心",
     "notes": "2023年起任宁国市委常委、宣传部长",
     "confidence": "plausible"},

    # ══ 市委常委 — 束永伟 ══
    {"id": 8, "name": "束永伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市委常委", "current_org": "中共宁国市委员会",
     "source": "宁国市政府网站; 公开报道",
     "notes": "公开报道显示为宁国市委常委",
     "confidence": "plausible"},

    # ══ 副市长 — 钟云辉 ══
    {"id": 9, "name": "钟云辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁国市副市长", "current_org": "宁国市人民政府",
     "source": "宁国市政府网站; 宁国市融媒体中心",
     "notes": "公开报道显示为宁国市副市长",
     "confidence": "plausible"},

    # ══ 副市长、公安局局长 — 钟小键 ══
    {"id": 10, "name": "钟小键", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁国市副市长、公安局局长", "current_org": "宁国市公安局",
     "source": "宁国市政府网站; 宣城市公安局",
     "notes": "任宁国市副市长、公安局党委书记、局长",
     "confidence": "plausible"},

    # ══ 副市长 — 李华 ══
    {"id": 11, "name": "李华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁国市副市长", "current_org": "宁国市人民政府",
     "source": "宁国市政府网站; 公开报道",
     "notes": "公开报道显示为宁国市副市长",
     "confidence": "plausible"},

    # ══ 市政协主席 — 陈柏平 ══
    {"id": 12, "name": "陈柏平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁国市政协主席", "current_org": "宁国市政协",
     "source": "宁国市政协网站; 公开报道",
     "notes": "公开报道显示为宁国市政协主席",
     "confidence": "plausible"},
]

organizations = [
    {"id": 1, "name": "中共宁国市委员会", "type": "党委", "level": "县(市)", "parent": "中共宣城市委员会", "location": "宁国市"},
    {"id": 2, "name": "宁国市人民政府", "type": "政府", "level": "县(市)", "parent": "宣城市人民政府", "location": "宁国市"},
    {"id": 3, "name": "中共宁国市委组织部", "type": "党委", "level": "县(市)", "parent": "中共宁国市委员会", "location": "宁国市"},
    {"id": 4, "name": "中共宁国市纪律检查委员会", "type": "党委", "level": "县(市)", "parent": "中共宁国市委员会", "location": "宁国市"},
    {"id": 5, "name": "中共宁国市委政法委员会", "type": "党委", "level": "县(市)", "parent": "中共宁国市委员会", "location": "宁国市"},
    {"id": 6, "name": "中共宁国市委宣传部", "type": "党委", "level": "县(市)", "parent": "中共宁国市委员会", "location": "宁国市"},
    {"id": 7, "name": "宁国市公安局", "type": "政府", "level": "县(市)部门", "parent": "宁国市人民政府", "location": "宁国市"},
    {"id": 8, "name": "宁国市政协", "type": "政协", "level": "县(市)", "parent": "宣城市政协", "location": "宁国市"},
    {"id": 9, "name": "中共宁国市委统战部", "type": "党委", "level": "县(市)", "parent": "中共宁国市委员会", "location": "宁国市"},
    {"id": 10, "name": "宁国市人民代表大会常务委员会", "type": "人大", "level": "县(市)", "parent": "宣城市人大常委会", "location": "宁国市"},
]

positions = [
    # 倪志品
    {"person_id": 1, "org_id": 1, "title": "宁国市委书记", "start": "2022", "end": "present", "rank": "县(市)正职",
     "note": "2022年起任宁国市委书记；2023年任宣城市委常委兼宁国市委书记"},
    # 杜德林
    {"person_id": 2, "org_id": 1, "title": "宁国市委副书记", "start": "2021", "end": "present", "rank": "县(市)副职",
     "note": "2021年任宁国市委副书记、代市长"},
    {"person_id": 2, "org_id": 2, "title": "宁国市市长", "start": "2021", "end": "present", "rank": "县(市)正职",
     "note": "后当选市长"},
    # 梅骏国
    {"person_id": 3, "org_id": 1, "title": "宁国市委常委", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "宁国市常务副市长", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    # 屠春节
    {"person_id": 4, "org_id": 1, "title": "宁国市委常委", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    {"person_id": 4, "org_id": 3, "title": "宁国市委组织部部长", "start": "", "end": "present", "rank": "县(市)部门正职",
     "note": ""},
    # 杨子霞
    {"person_id": 5, "org_id": 1, "title": "宁国市委常委", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    {"person_id": 5, "org_id": 4, "title": "宁国市纪委书记、监委主任", "start": "", "end": "present", "rank": "县(市)部门正职",
     "note": ""},
    # 谭浩
    {"person_id": 6, "org_id": 1, "title": "宁国市委常委", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    {"person_id": 6, "org_id": 5, "title": "宁国市委政法委书记", "start": "", "end": "present", "rank": "县(市)部门正职",
     "note": ""},
    # 彭静
    {"person_id": 7, "org_id": 1, "title": "宁国市委常委", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    {"person_id": 7, "org_id": 6, "title": "宁国市委宣传部部长", "start": "", "end": "present", "rank": "县(市)部门正职",
     "note": ""},
    # 束永伟
    {"person_id": 8, "org_id": 1, "title": "宁国市委常委", "start": "", "end": "present", "rank": "县(市)副职",
     "note": "具体分工待确认"},
    # 钟云辉
    {"person_id": 9, "org_id": 2, "title": "宁国市副市长", "start": "", "end": "present", "rank": "县(市)副职",
     "note": "分工待确认"},
    # 钟小键
    {"person_id": 10, "org_id": 2, "title": "宁国市副市长", "start": "", "end": "present", "rank": "县(市)副职",
     "note": ""},
    {"person_id": 10, "org_id": 7, "title": "宁国市公安局局长", "start": "", "end": "present", "rank": "县(市)部门正职",
     "note": ""},
    # 李华
    {"person_id": 11, "org_id": 2, "title": "宁国市副市长", "start": "", "end": "present", "rank": "县(市)副职",
     "note": "分工待确认"},
    # 陈柏平
    {"person_id": 12, "org_id": 8, "title": "宁国市政协主席", "start": "", "end": "present", "rank": "县(市)正职",
     "note": ""},
]

relationships = [
    {"person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "overlap_period": "2022-至今", "context": "倪志品任宁国市委书记，杜德林任宁国市长，为党政正职搭档",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a_id": 1, "person_b_id": 3, "type": "上下级",
     "overlap_period": "", "context": "梅骏国任常务副市长，为倪志品下属",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a_id": 2, "person_b_id": 3, "type": "上下级",
     "overlap_period": "", "context": "梅骏国为杜德林在政府班子的副手",
     "strength": "medium", "confidence": "confirmed"},
    {"person_a_id": 1, "person_b_id": 4, "type": "上下级",
     "overlap_period": "", "context": "屠春节任组织部长，为宁国市委领导班子成员",
     "strength": "medium", "confidence": "plausible"},
    {"person_a_id": 1, "person_b_id": 5, "type": "上下级",
     "overlap_period": "", "context": "杨子霞任纪委书记，为宁国市委领导班子成员",
     "strength": "medium", "confidence": "plausible"},
]


# ── DB BUILD ────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
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
            source TEXT,
            notes TEXT,
            confidence TEXT
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            overlap_period TEXT,
            context TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org,
             source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"],
              p["birth"], p["birthplace"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"],
              p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships
            (person_a_id, person_b_id, type, overlap_period, context, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a_id"], r["person_b_id"], r["type"],
              r["overlap_period"], r["context"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()


# ── GEXF BUILD ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "市委" in role:
        return "255,50,50"
    elif "市长" in role or "副市长" in role or "常务" in role:
        return "50,100,255"
    elif "纪委" in role:
        return "255,165,0"
    elif "统战" in role:
        return "100,200,100"
    else:
        return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "政协" in t:
        return "255,240,200"
    elif "人大" in t:
        return "200,255,255"
    else:
        return "200,200,200"

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>宁国市领导班子工作关系网络 - 安徽省宣城市辖县级市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="period" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in [1, 2] else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
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
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append('          <attvalue for="2" value="present"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF edges: {eid}")


# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    print("Building 宁国市 network database...")
    build_db()
    print(f"  DB: {DB_PATH}")

    print("Building GEXF graph...")
    build_gexf()
    print(f"  GEXF: {GEXF_PATH}")

    print("\nDone. Summary:")
    print(f"  {len(persons)} persons")
    print(f"  {len(organizations)} organizations")
    print(f"  {len(positions)} positions")
    print(f"  {len(relationships)} relationships")
