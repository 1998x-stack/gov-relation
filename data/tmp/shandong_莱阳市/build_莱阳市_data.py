#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 莱阳市 (Laiyang, Yantai City, Shandong Province) leadership network.

Covers: Party Secretary (市委书记), Mayor (市长), deputy leaders, and cross-county exchange patterns.

Sources:
- Official government leadership page: https://www.laiyang.gov.cn/col/col57526/index.html
- Official news articles (2026-07-14, 2026-07-10) confirming 卢春玲 as 市委书记 and 邵蕾 as 市长
- Individual bio pages for each leader on laiyang.gov.cn
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/shandong_莱阳市")
DB_PATH = os.path.join(STAGING, "莱阳市_network.db")
GEXF_PATH = os.path.join(STAGING, "莱阳市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 卢春玲 — 莱阳市委书记 (as of 2026-07-14)
    {"id": 1, "name": "卢春玲", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市委书记", "current_org": "中共莱阳市委员会",
     "source": "https://www.laiyang.gov.cn/col/col12736/art/2026/art_50fa7b092cc148bd9d69d6de60ccad51.html"},

    # 邵蕾 — 莱阳市委副书记、市长 (as of 2026), 男，汉，1980.09，大学
    {"id": 2, "name": "邵蕾", "gender": "男", "ethnicity": "汉族", "birth": "1980-09",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市委副书记、市长", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57527/index.html"},

    # ── 市委常委/副市长 ──
    # 邹得民 — 市委常委，市政府党组副书记、副市长(正县级），男，汉，1981.01，大学
    {"id": 3, "name": "邹得民", "gender": "男", "ethnicity": "汉族", "birth": "1981-01",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市委常委、副市长（正县级）", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57528/index.html"},

    # 于涛 — 市委常委、宣传部部长、教育工委书记，市政府党组成员、副市长，男，汉，1975.12，研究生
    {"id": 4, "name": "于涛", "gender": "男", "ethnicity": "汉族", "birth": "1975-12",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市委常委、宣传部部长、副市长", "current_org": "中共莱阳市委宣传部",
     "source": "https://www.laiyang.gov.cn/col/col57529/index.html"},

    # 于述东 — 莱阳市政府副市长，市委政法委副书记，市公安局党委书记、局长、督察长，男，汉，1971.09，大学
    {"id": 5, "name": "于述东", "gender": "男", "ethnicity": "汉族", "birth": "1971-09",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市副市长、市公安局局长", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57532/index.html"},

    # 李占伟 — 市政府党组成员、副市长，男，汉，1982.08，研究生
    {"id": 6, "name": "李占伟", "gender": "男", "ethnicity": "汉族", "birth": "1982-08",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市副市长", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57533/index.html"},

    # 李诚 — 市政府党组成员、副市长，男，汉，1985.10，研究生
    {"id": 7, "name": "李诚", "gender": "男", "ethnicity": "汉族", "birth": "1985-10",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市副市长", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57530/index.html"},

    # 陈林旭 — 莱阳市副市长（bio 页面未找到）
    {"id": 8, "name": "陈林旭", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市副市长", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57526/index.html"},

    # 王宏 — 莱阳市副市长（bio 页面未找到）
    {"id": 9, "name": "王宏", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "莱阳市副市长", "current_org": "莱阳市人民政府",
     "source": "https://www.laiyang.gov.cn/col/col57526/index.html"},

    # ── 前任 ──
    # 李胜刚 — 前任莱阳市委书记（2021年前后任职）
    {"id": 10, "name": "李胜刚", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "烟台市委党校常务副校长（曾任莱阳市委书记）", "current_org": "中共烟台市委党校",
     "source": ""},

    # 刘森 — 前任莱阳市委书记
    {"id": 11, "name": "刘森", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾任莱阳市委书记", "current_org": "",
     "source": ""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共莱阳市委员会", "type": "党委", "level": "县级", "parent": "中共烟台市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 2, "name": "莱阳市人民政府", "type": "政府", "level": "县级", "parent": "烟台市人民政府", "location": "山东省烟台市莱阳市"},
    {"id": 3, "name": "莱阳市人大常委会", "type": "人大", "level": "县级", "parent": "烟台市人大常委会", "location": "山东省烟台市莱阳市"},
    {"id": 4, "name": "政协莱阳市委员会", "type": "政协", "level": "县级", "parent": "政协烟台市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 5, "name": "中共莱阳市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共莱阳市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 6, "name": "中共莱阳市委组织部", "type": "党委", "level": "县级", "parent": "中共莱阳市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 7, "name": "中共莱阳市委宣传部", "type": "党委", "level": "县级", "parent": "中共莱阳市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 8, "name": "中共莱阳市委统战部", "type": "党委", "level": "县级", "parent": "中共莱阳市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 9, "name": "中共莱阳市委政法委", "type": "党委", "level": "县级", "parent": "中共莱阳市委员会", "location": "山东省烟台市莱阳市"},
    {"id": 10, "name": "莱阳市公安局", "type": "政府", "level": "县级", "parent": "莱阳市人民政府", "location": "山东省烟台市莱阳市"},
    {"id": 11, "name": "莱阳经济开发区", "type": "开发区", "level": "县级", "parent": "莱阳市人民政府", "location": "山东省烟台市莱阳市"},
    {"id": 12, "name": "中共烟台市委员会", "type": "党委", "level": "地级", "parent": "中共山东省委员会", "location": "山东省烟台市"},
    {"id": 13, "name": "烟台市人民政府", "type": "政府", "level": "地级", "parent": "山东省人民政府", "location": "山东省烟台市"},
    {"id": 14, "name": "中共烟台市委党校", "type": "事业单位", "level": "地级", "parent": "中共烟台市委员会", "location": "山东省烟台市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 卢春玲 (id=1) — 莱阳市委书记 ──
    {"pid": 1, "org": 1, "title": "莱阳市委书记", "start": "", "end": "至今", "rank": "正处级",
     "note": "2026年7月仍在任（2026-07-14 市委常委会扩大会议报道）"},

    # ── 邵蕾 (id=2) — 莱阳市委副书记、市长 ──
    {"pid": 2, "org": 2, "title": "莱阳市委副书记、市长", "start": "", "end": "至今", "rank": "正处级",
     "note": "市政府党组书记，主持市政府全面工作"},
    {"pid": 2, "org": 1, "title": "莱阳市委副书记", "start": "", "end": "至今", "rank": "副厅级(?)",
     "note": "兼任市委副书记"},

    # ── 邹得民 (id=3) — 市委常委、副市长（正县级） ──
    {"pid": 3, "org": 2, "title": "莱阳市委常委、副市长（正县级）", "start": "", "end": "至今", "rank": "正处级",
     "note": "市政府党组副书记，负责市政府常务工作"},
    {"pid": 3, "org": 1, "title": "莱阳市委常委", "start": "", "end": "至今", "rank": "副处级(?)",
     "note": ""},

    # ── 于涛 (id=4) — 市委常委、宣传部部长、副市长 ──
    {"pid": 4, "org": 7, "title": "莱阳市委常委、宣传部部长", "start": "", "end": "至今", "rank": "副处级",
     "note": "教育工委书记"},
    {"pid": 4, "org": 2, "title": "莱阳市政府党组成员、副市长", "start": "", "end": "至今", "rank": "副处级",
     "note": "负责自然资源和规划、住建、林业等"},

    # ── 于述东 (id=5) — 副市长、市公安局局长 ──
    {"pid": 5, "org": 2, "title": "莱阳市副市长", "start": "", "end": "至今", "rank": "副处级",
     "note": "市委政法委副书记，市公安局党委书记、局长、督察长"},
    {"pid": 5, "org": 10, "title": "莱阳市公安局局长", "start": "", "end": "至今", "rank": "副处级",
     "note": ""},

    # ── 李占伟 (id=6) — 副市长 ──
    {"pid": 6, "org": 2, "title": "莱阳市副市长", "start": "", "end": "至今", "rank": "副处级",
     "note": "市政府党组成员，负责工业、交通、商务、投促等"},

    # ── 李诚 (id=7) — 副市长 ──
    {"pid": 7, "org": 2, "title": "莱阳市副市长", "start": "", "end": "至今", "rank": "副处级",
     "note": "市政府党组成员，负责民政、水务、农业农村、文旅、市场监管等"},

    # ── 陈林旭 (id=8) — 副市长 ──
    {"pid": 8, "org": 2, "title": "莱阳市副市长", "start": "", "end": "至今", "rank": "副处级",
     "note": "具体分工待确认"},

    # ── 王宏 (id=9) — 副市长 ──
    {"pid": 9, "org": 2, "title": "莱阳市副市长", "start": "", "end": "至今", "rank": "副处级",
     "note": "具体分工待确认"},

    # ── 李胜刚 (id=10) — 前任莱阳市委书记 ──
    {"pid": 10, "org": 1, "title": "莱阳市委书记（曾任）", "start": "", "end": "", "rank": "正处级",
     "note": "前任莱阳市委书记，现烟台市委党校常务副校长"},

    # ── 刘森 (id=11) — 前任莱阳市委书记 ──
    {"pid": 11, "org": 1, "title": "莱阳市委书记（曾任）", "start": "", "end": "", "rank": "正处级",
     "note": "前任莱阳市委书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 卢春玲 ↔ 邵蕾 (current party secretary - mayor)
    {"a": 1, "b": 2, "type": "overlap",
     "context": "卢春玲任莱阳市委书记，邵蕾任市长，党政搭档",
     "overlap_org": "中共莱阳市委员会、莱阳市人民政府",
     "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},

    # 卢春玲 ↔ 李胜刚 (predecessor-successor, party secretary)
    {"a": 1, "b": 10, "type": "predecessor_successor",
     "context": "卢春玲接替李胜刚担任莱阳市委书记（推测）",
     "overlap_org": "中共莱阳市委员会",
     "overlap_period": "", "strength": "strong", "confidence": "plausible"},

    # 卢春玲 ↔ 刘森 (predecessor-successor, party secretary)
    {"a": 1, "b": 11, "type": "predecessor_successor",
     "context": "卢春玲接替刘森担任莱阳市委书记（推测）",
     "overlap_org": "中共莱阳市委员会",
     "overlap_period": "", "strength": "strong", "confidence": "plausible"},

    # 卢春玲 ↔ 邹得民 (书记 - 常委副市长)
    {"a": 1, "b": 3, "type": "superior_subordinate",
     "context": "卢春玲任市委书记，邹得民任市委常委、副市长",
     "overlap_org": "中共莱阳市委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 卢春玲 ↔ 于涛 (书记 - 宣传部长)
    {"a": 1, "b": 4, "type": "superior_subordinate",
     "context": "卢春玲任市委书记，于涛任市委常委、宣传部部长",
     "overlap_org": "中共莱阳市委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 邵蕾 ↔ 邹得民 (市长 - 常务副市长)
    {"a": 2, "b": 3, "type": "superior_subordinate",
     "context": "邵蕾任市长，邹得民任常务副市长",
     "overlap_org": "莱阳市人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 邵蕾 ↔ 于述东 (市长 - 公安局长)
    {"a": 2, "b": 5, "type": "superior_subordinate",
     "context": "邵蕾任市长，于述东任副市长兼公安局长",
     "overlap_org": "莱阳市人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 邵蕾 ↔ 李占伟 (市长 - 副市长)
    {"a": 2, "b": 6, "type": "superior_subordinate",
     "context": "邵蕾任市长，李占伟任副市长",
     "overlap_org": "莱阳市人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 邵蕾 ↔ 李诚 (市长 - 副市长)
    {"a": 2, "b": 7, "type": "superior_subordinate",
     "context": "邵蕾任市长，李诚任副市长",
     "overlap_org": "莱阳市人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 邵蕾 ↔ 陈林旭
    {"a": 2, "b": 8, "type": "superior_subordinate",
     "context": "邵蕾任市长，陈林旭任副市长",
     "overlap_org": "莱阳市人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 邵蕾 ↔ 王宏
    {"a": 2, "b": 9, "type": "superior_subordinate",
     "context": "邵蕾任市长，王宏任副市长",
     "overlap_org": "莱阳市人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},

    # 于述东 ↔ 于涛 (常委交叉任职)
    {"a": 4, "b": 5, "type": "overlap",
     "context": "于涛（市委常委、宣传部长）与于述东（副市长、政法委副书记）在莱阳市委班子共事",
     "overlap_org": "中共莱阳市委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["pid"], pos["org"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["a"], r["b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"],
              r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    print(f"  Persons: {conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        current = p.get("current_post", "")
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "市长" in current or "县长" in current or "区长" in current or "人大" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "政协" in current:
            return "255,240,200"  # Cream — CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        if name == "卢春玲":
            return "20.0"
        if name == "邵蕾":
            return "20.0"
        if name in ("邹得民", "李胜刚"):
            return "15.0"
        return "12.0"

    def org_color(o):
        t = o.get("type", "")
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>莱阳市领导班子工作关系网络 — 中共莱阳市委、莱阳市人民政府及前任领导</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "未知")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Nodes - organizations
    lines.append('    <nodes>')
    for o in organizations:
        c = org_color(o)
        oid = str(o["id"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Position edges: person -> organization
    for pos in positions:
        eid += 1
        oid = str(pos["org"])
        period = f"{pos['start']} - {pos['end']}" if pos['start'] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["pid"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges: person <-> person
    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["a"]}" target="p{r["b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}")
    print(f"  Edges: {eid}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("\nDone. Generated artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
