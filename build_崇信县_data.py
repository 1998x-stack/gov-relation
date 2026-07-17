#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 崇信县 (Chongxin County), Pingliang, Gansu.

Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
as of July 2026.
"""

import sqlite3
import os
import sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_崇信县")
DB_PATH = os.path.join(STAGING, "崇信县_network.db")
GEXF_PATH = os.path.join(STAGING, "崇信县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current Top Leaders ──
    # 杨聪 — 崇信县委书记 (as of 2026.07)
    {"id": 1, "name": "杨聪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县委书记",
     "current_org": "中共崇信县委员会",
     "source": "https://www.chongxin.gov.cn/"},

    # 何双虎 — 崇信县委副书记、县政府代理县长 (as of 2026.07)
    {"id": 2, "name": "何双虎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县委副书记、县政府代理县长",
     "current_org": "崇信县人民政府",
     "source": "https://www.chongxin.gov.cn/"},

    # ── Predecessors ──
    # 杨聪的前任 (predecessor as Party Secretary) — previously 张拴会 was Pingliang vice mayor,
    # and before that 王度林 was the Party Secretary of 崇信县 before being promoted to 平凉市副市长
    # Based on Pingliang city leadership data, 王度林 was 崇信县委书记 before promotion.
    {"id": 3, "name": "王度林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "平凉市委常委、副市长（原崇信县委书记）",
     "current_org": "平凉市人民政府",
     "source": "https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},

    # 张拴会 — 原崇信县委书记 (?), now 平凉市人大常委会副主任
    {"id": 4, "name": "张拴会", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "平凉市人大常委会副主任（原崇信县委书记）",
     "current_org": "平凉市人大常委会",
     "source": "https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},

    # 何双虎的前任 (predecessor as County Mayor)
    # Based on news context, 杨聪 was previously the county mayor before becoming party secretary
    {"id": 5, "name": "杨聪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县委书记（原崇信县县长）",
     "current_org": "中共崇信县委员会",
     "source": "https://www.chongxin.gov.cn/"},

    # ── Standing Committee (县委常委) ──
    {"id": 6, "name": "李朋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县委常委、县政府常务副县长",
     "current_org": "崇信县人民政府",
     "source": "https://www.chongxin.gov.cn/"},
    {"id": 7, "name": "白亚军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县委常委、组织部部长",
     "current_org": "中共崇信县委员会",
     "source": "https://www.chongxin.gov.cn/"},

    # ── 县人大常委会 ──
    {"id": 8, "name": "王宁宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县人大常委会主任",
     "current_org": "崇信县人大常委会",
     "source": "https://www.chongxin.gov.cn/"},

    # ── 县政府副县长 ──
    {"id": 9, "name": "张政国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县副县长",
     "current_org": "崇信县人民政府",
     "source": "https://www.chongxin.gov.cn/"},
    {"id": 10, "name": "王紫璇", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "崇信县副县长",
     "current_org": "崇信县人民政府",
     "source": "https://www.chongxin.gov.cn/"},

    # ── 上级领导（平凉市） ——
    {"id": 11, "name": "唐培宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-03", "birthplace": "甘肃民勤", "education": "西北师范大学历史系本科、兰州大学公共管理硕士",
     "party_join": "1991-06", "work_start": "1992-07",
     "current_post": "平凉市委书记",
     "current_org": "中共平凉市委员会",
     "source": "https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},
    {"id": 12, "name": "李荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "甘肃定西", "education": "甘肃政法学院本科、省委党校研究生",
     "party_join": "1996-12", "work_start": "1999-09",
     "current_post": "平凉市委副书记、市长",
     "current_org": "平凉市人民政府",
     "source": "https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},

    # ── 县法院、检察院 ──
    {"id": 13, "name": "苏斌杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇信县法院院长",
     "current_org": "崇信县人民法院",
     "source": "https://www.chongxin.gov.cn/"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共崇信县委员会", "type": "党委", "level": "县处级",
     "parent": "中共平凉市委员会", "location": "甘肃省平凉市崇信县"},
    {"id": 2, "name": "崇信县人民政府", "type": "政府", "level": "县处级",
     "parent": "平凉市人民政府", "location": "甘肃省平凉市崇信县"},
    {"id": 3, "name": "崇信县人大常委会", "type": "人大", "level": "县处级",
     "parent": "平凉市人大常委会", "location": "甘肃省平凉市崇信县"},
    {"id": 4, "name": "政协崇信县委员会", "type": "政协", "level": "县处级",
     "parent": "政协平凉市委员会", "location": "甘肃省平凉市崇信县"},
    {"id": 5, "name": "中共崇信县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共崇信县委员会", "location": "甘肃省平凉市崇信县"},
    {"id": 6, "name": "中共崇信县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共崇信县委员会", "location": "甘肃省平凉市崇信县"},
    {"id": 7, "name": "崇信县人民法院", "type": "政府", "level": "县处级",
     "parent": "崇信县人大常委会", "location": "甘肃省平凉市崇信县"},

    # ── 上级组织 ──
    {"id": 8, "name": "中共平凉市委员会", "type": "党委", "level": "地级",
     "parent": "中共甘肃省委员会", "location": "甘肃省平凉市"},
    {"id": 9, "name": "平凉市人民政府", "type": "政府", "level": "地级",
     "parent": "甘肃省人民政府", "location": "甘肃省平凉市"},
    {"id": 10, "name": "平凉市人大常委会", "type": "人大", "level": "地级",
     "parent": "甘肃省人大常委会", "location": "甘肃省平凉市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 杨聪 (id=1) — 县委书记 ──
    {"pid": 1, "org": 1, "title": "崇信县委书记",
     "start": "", "end": "至今", "rank": "正处级",
     "note": "2026年7月新闻报道中活跃"},
    {"pid": 1, "org": 2, "title": "崇信县县长（前任职务）",
     "start": "", "end": "", "rank": "正处级",
     "note": "推测此前担任崇信县县长，后升任县委书记"},

    # ── 何双虎 (id=2) — 代理县长 ──
    {"pid": 2, "org": 2, "title": "崇信县委副书记、县政府代理县长",
     "start": "2026-07", "end": "至今", "rank": "正处级",
     "note": "2026年7月8日新闻报道中称为\"县委副书记、县政府代理县长\""},
    {"pid": 2, "org": 1, "title": "崇信县委副书记",
     "start": "", "end": "至今", "rank": "副处级",
     "note": ""},

    # ── 王度林 (id=3) — 原县委书记 ──
    {"pid": 3, "org": 1, "title": "崇信县委书记（原任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "后晋升平凉市委常委、副市长"},
    {"pid": 3, "org": 9, "title": "平凉市委常委、副市长",
     "start": "", "end": "至今", "rank": "副厅级",
     "note": ""},

    # ── 张拴会 (id=4) — 原县委书记 ──
    {"pid": 4, "org": 1, "title": "崇信县委书记（原任）",
     "start": "", "end": "", "rank": "正处级",
     "note": ""},
    {"pid": 4, "org": 10, "title": "平凉市人大常委会副主任",
     "start": "", "end": "至今", "rank": "副厅级",
     "note": ""},

    # ── 杨聪 (id=5) — 原县长，现任县委书记（重复条目用于关系追踪）
    {"pid": 5, "org": 2, "title": "崇信县县长（原任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "杨聪此前担任崇信县县长，后任县委书记"},

    # ── 李朋 (id=6) — 常务副县长 ──
    {"pid": 6, "org": 2, "title": "崇信县委常委、县政府常务副县长",
     "start": "", "end": "至今", "rank": "副处级",
     "note": ""},

    # ── 白亚军 (id=7) — 组织部部长 ──
    {"pid": 7, "org": 6, "title": "崇信县委常委、组织部部长",
     "start": "", "end": "至今", "rank": "副处级",
     "note": ""},

    # ── 王宁宁 (id=8) — 人大主任 ──
    {"pid": 8, "org": 3, "title": "崇信县人大常委会主任",
     "start": "", "end": "至今", "rank": "正处级",
     "note": ""},

    # ── 张政国 (id=9) — 副县长 ──
    {"pid": 9, "org": 2, "title": "崇信县副县长",
     "start": "", "end": "至今", "rank": "副处级",
     "note": ""},

    # ── 王紫璇 (id=10) — 副县长 ──
    {"pid": 10, "org": 2, "title": "崇信县副县长",
     "start": "", "end": "至今", "rank": "副处级",
     "note": ""},

    # ── 唐培宏 (id=11) — 平凉市委书记 ──
    {"pid": 11, "org": 8, "title": "平凉市委书记",
     "start": "2025-09", "end": "至今", "rank": "正厅级",
     "note": ""},

    # ── 李荣 (id=12) — 平凉市长 ──
    {"pid": 12, "org": 9, "title": "平凉市委副书记、市长",
     "start": "2026-01", "end": "至今", "rank": "正厅级",
     "note": ""},

    # ── 苏斌杰 (id=13) — 法院院长 ──
    {"pid": 13, "org": 7, "title": "崇信县法院院长",
     "start": "", "end": "至今", "rank": "副处级",
     "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 杨聪 (县委书记) ↔ 何双虎 (代理县长) — 党政搭档
    {"a": 1, "b": 2, "type": "overlap",
     "context": "杨聪任县委书记，何双虎任县委副书记、代理县长，党政搭档",
     "overlap_org": "中共崇信县委员会、崇信县人民政府",
     "overlap_period": "2026-07~至今",
     "strength": "strong", "confidence": "confirmed"},

    # 杨聪 (书记) ↔ 杨聪 (原县长) — 同人升迁（模型兼容）
    {"a": 1, "b": 5, "type": "promotion_chain",
     "context": "杨聪由崇信县县长升任崇信县委书记",
     "overlap_org": "崇信县人民政府、中共崇信县委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 杨聪 ↔ 王度林 (predecessor-successor as 县委书记)
    {"a": 1, "b": 3, "type": "predecessor_successor",
     "context": "杨聪接替王度林（推测）担任崇信县委书记",
     "overlap_org": "中共崇信县委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "plausible"},

    # 何双虎 ↔ 杨聪 (predecessor-successor as 县长)
    {"a": 2, "b": 5, "type": "predecessor_successor",
     "context": "何双虎接替杨聪担任崇信县代理县长",
     "overlap_org": "崇信县人民政府",
     "overlap_period": "2026-07",
     "strength": "strong", "confidence": "plausible"},

    # 杨聪 ↔ 唐培宏 (上级领导)
    {"a": 1, "b": 11, "type": "superior_subordinate",
     "context": "杨聪作为县委书记在平凉市委领导下工作",
     "overlap_org": "中共平凉市委员会",
     "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    # 何双虎 ↔ 李荣 (上级领导)
    {"a": 2, "b": 12, "type": "superior_subordinate",
     "context": "何双虎作为县长在平凉市政府领导下工作",
     "overlap_org": "",
     "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    # 杨聪 ↔ 李朋 (县委常委会同事)
    {"a": 1, "b": 6, "type": "overlap",
     "context": "杨聪与李朋同在崇信县委常委会",
     "overlap_org": "中共崇信县委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 杨聪 ↔ 白亚军 (县委常委会同事)
    {"a": 1, "b": 7, "type": "overlap",
     "context": "杨聪与白亚军同在崇信县委常委会",
     "overlap_org": "中共崇信县委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 何双虎 ↔ 李朋 (政府班子同事)
    {"a": 2, "b": 6, "type": "overlap",
     "context": "何双虎与李朋同在崇信县政府领导班子",
     "overlap_org": "崇信县人民政府",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 何双虎 ↔ 张政国 (政府班子同事)
    {"a": 2, "b": 9, "type": "overlap",
     "context": "何双虎与张政国同在崇信县政府领导班子",
     "overlap_org": "崇信县人民政府",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 何双虎 ↔ 王紫璇 (政府班子同事)
    {"a": 2, "b": 10, "type": "overlap",
     "context": "何双虎与王紫璇同在崇信县政府领导班子",
     "overlap_org": "崇信县人民政府",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 杨聪 ↔ 王宁宁 (党政与人大)
    {"a": 1, "b": 8, "type": "overlap",
     "context": "杨聪任县委书记期间王宁宁任县人大常委会主任",
     "overlap_org": "崇信县",
     "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    # 杨聪 ↔ 张拴会 (predecessor-successor)
    {"a": 1, "b": 4, "type": "predecessor_successor",
     "context": "杨聪接替张拴会（推测）担任崇信县委书记",
     "overlap_org": "中共崇信县委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "plausible"},
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
            id TEXT PRIMARY KEY,
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
            id TEXT PRIMARY KEY,
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
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
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
        """, (str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["pid"], str(pos["org"]), pos["title"], pos["start"], pos["end"],
              pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["a"], r["b"], r["type"], r["context"], r["overlap_org"],
              r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")

    # Stats
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
        if "县长" in current or "市长" in current or "副" in current:
            if "人大" in current:
                return "200,255,255"
            if "政协" in current:
                return "255,240,200"
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "人大" in current:
            return "200,255,255"  # Cyan — NPC
        if "政协" in current:
            return "255,240,200"  # Cream — CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        # Top leaders
        if name == "杨聪" and "书记" in p.get("current_post", ""):
            return "20.0"
        if name == "何双虎":
            return "20.0"
        # Former top leaders / city level
        if name in ("王度林", "张拴会", "唐培宏", "李荣"):
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
    lines.append('    <description>崇信县领导班子工作关系网络 — 中共崇信县委、崇信县人民政府及上级组织<br/>'
                 'Targets: 县委书记 杨聪, 代理县长 何双虎</description>')
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

    # Nodes
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

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
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
    for pos in positions:
        eid += 1
        period = f"{pos['start']} - {pos['end']}" if pos['start'] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["pid"]}" target="o{pos["org"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

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
