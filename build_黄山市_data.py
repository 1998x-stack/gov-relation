#!/usr/bin/env python3
"""Build 黄山市 (Huangshan City, Anhui Province) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_黄山市
Province: 安徽省
City: 黄山市
Level: 地级市

Targets: 市委书记 & 市长

Current leaders (as of Dec 2024–present):
  - 市委书记: 丁纯 (appointed 2024.12, moved from 铜陵市委书记)
  - 市委副书记/市长: 何毅 (confirmed ~2023–present)

Sources:
  - 澎湃新闻: 丁纯任黄山市委书记 (2024-12-02)
  - 鲁中晨报: 黄山市委书记调整 (2024-12-02)
  - 中安在线: 黄山市委书记、市长凌晨部署防汛 (2024-06-21)
  - 人民网: 凌云任黄山市委书记 (2021-04)

Confidence:
  - Current roles: confirmed from multiple news sources
  - Biographical details for 丁纯: confirmed (public resume via media)
  - Biographical details for 何毅: partial
  - Ex-市委书记 凌云: confirmed
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IS_STAGING = "data/tmp" in SCRIPT_DIR

if IS_STAGING:
    DB_PATH = os.path.join(SCRIPT_DIR, "黄山市_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "黄山市_network.gexf")
else:
    BASE = os.path.dirname(SCRIPT_DIR)  # repo root
    DB_PATH = os.path.join(BASE, "data/database/黄山市_network.db")
    GEXF_PATH = os.path.join(BASE, "data/graph/黄山市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "丁纯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "江苏省江阴市",
        "education": "研究生学历，博士学位，高级工程师",
        "party_join": "1991-06",
        "work_start": "1995-04",
        "current_post": "黄山市委书记",
        "current_org": "中国共产党黄山市委员会",
        "source": "澎湃新闻; 鲁中晨报; 极目新闻"
    },
    {
        "id": 2,
        "name": "何毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄山市委副书记、市长",
        "current_org": "黄山市人民政府",
        "source": "中安在线（黄山日报）; 黄山市政府官网"
    },
    # ── Previous Leaders ──
    {
        "id": 3,
        "name": "凌云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1964-07",
        "birthplace": "安徽省肥东县",
        "education": "研究生学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任黄山市委书记）",
        "current_org": "（已离任）",
        "source": "人民网; 鲁中晨报"
    },
    {
        "id": 4,
        "name": "杨宏星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铜陵市委书记",
        "current_org": "中国共产党铜陵市委员会",
        "source": "鲁中晨报; 安徽先锋"
    },
    # ── Mayor's deputies and key city leaders ──
    {
        "id": 5,
        "name": "任生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄山市委副书记、组织部部长",
        "current_org": "中国共产党黄山市委员会",
        "source": "黄山日报; 安徽先锋网"
    },
    {
        "id": 6,
        "name": "叶建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄山市委常委、秘书长",
        "current_org": "中国共产党黄山市委员会",
        "source": "黄山日报"
    },
    {
        "id": 7,
        "name": "朱策",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "安徽省长丰县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄山市委常委、常务副市长",
        "current_org": "黄山市人民政府",
        "source": "黄山市政府官网"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中国共产党黄山市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省黄山市"
    },
    {
        "id": 2,
        "name": "黄山市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "安徽省人民政府",
        "location": "安徽省黄山市"
    },
    {
        "id": 3,
        "name": "中国共产党铜陵市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省铜陵市"
    },
    {
        "id": 4,
        "name": "中国共产党安徽省委员会",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "安徽省合肥市"
    },
    {
        "id": 5,
        "name": "安徽省人民政府",
        "type": "政府",
        "level": "省",
        "parent": None,
        "location": "安徽省合肥市"
    },
    {
        "id": 6,
        "name": "黄山市",
        "type": "行政区域",
        "level": "地级",
        "parent": "安徽省",
        "location": "安徽省"
    },
    {
        "id": 7,
        "name": "中国共产党黄山市委员会组织部",
        "type": "党委",
        "level": "地级",
        "parent": "中国共产党黄山市委员会",
        "location": "安徽省黄山市"
    },
    {
        "id": 8,
        "name": "中国共产党黄山市委员会办公室",
        "type": "党委",
        "level": "地级",
        "parent": "中国共产党黄山市委员会",
        "location": "安徽省黄山市"
    },
]

positions = [
    # 丁纯 - 市委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "黄山市委书记",
     "start": "2024-12", "end": "present", "rank": "正厅级",
     "note": "黄山市委书记，主持市委全面工作。此前任铜陵市委书记（2019.12–2024.12）"},
    {"id": 2, "person_id": 1, "org_id": 3, "title": "铜陵市委书记",
     "start": "2019-12", "end": "2024-12", "rank": "正厅级",
     "note": "跨省调任安徽铜陵市委书记"},
    # 何毅 - 市长
    {"id": 3, "person_id": 2, "org_id": 2, "title": "黄山市委副书记、市长",
     "start": "2023", "end": "present", "rank": "正厅级",
     "note": "黄山市委副书记、市长，主持市政府全面工作"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "黄山市委副书记",
     "start": "2023", "end": "present", "rank": "正厅级",
     "note": "兼任市长"},
    # 凌云 - 前任市委书记
    {"id": 5, "person_id": 3, "org_id": 1, "title": "黄山市委书记",
     "start": "2021-04", "end": "2024-12", "rank": "正厅级",
     "note": "前任黄山市委书记"},
    # 杨宏星 - 接任铜陵市委书记
    {"id": 6, "person_id": 4, "org_id": 3, "title": "铜陵市委书记",
     "start": "2024-12", "end": "present", "rank": "正厅级",
     "note": "接替丁纯任铜陵市委书记"},
    # 任生 - 副书记兼组织部长
    {"id": 7, "person_id": 5, "org_id": 1, "title": "黄山市委副书记",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "市委专职副书记"},
    {"id": 8, "person_id": 5, "org_id": 7, "title": "黄山市委组织部部长",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "兼任组织部部长"},
    # 叶建强 - 秘书长
    {"id": 9, "person_id": 6, "org_id": 8, "title": "黄山市委常委、秘书长",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "市委秘书长，负责市委日常事务"},
    {"id": 10, "person_id": 6, "org_id": 1, "title": "黄山市委常委",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "市委常委"},
    # 朱策 - 常务副市长
    {"id": 11, "person_id": 7, "org_id": 2, "title": "黄山市委常委、常务副市长",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "市委常委、常务副市长"},
    {"id": 12, "person_id": 7, "org_id": 1, "title": "黄山市委常委",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "市委常委"},
]

relationships = [
    # 丁纯与何毅 - 党政搭档
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "丁纯（市委书记）与何毅（市长）为黄山市党政正职搭档",
        "overlap_org": "黄山市",
        "overlap_period": "2024.12–present"
    },
    # 丁纯与凌云 - 前后任
    {
        "id": 2,
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "丁纯接替凌云任黄山市委书记",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "2024.12（交接）"
    },
    # 丁纯与杨宏星 - 前后任（铜陵）
    {
        "id": 3,
        "person_a": 1, "person_b": 4,
        "type": "predecessor_successor",
        "context": "丁纯离任铜陵市委书记后，杨宏星接任",
        "overlap_org": "中国共产党铜陵市委员会",
        "overlap_period": "2024.12（交接）"
    },
    # 丁纯与任生 - 市委班子
    {
        "id": 4,
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "丁纯（市委书记）与任生（市委副书记/组织部部长）为市委领导班子成员",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "2024.12–present"
    },
    # 丁纯与叶建强 - 市委班子
    {
        "id": 5,
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "丁纯（市委书记）与叶建强（市委常委/秘书长）为市委领导班子成员",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "2024.12–present"
    },
    # 丁纯与朱策 - 市委班子
    {
        "id": 6,
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "丁纯（市委书记）与朱策（市委常委/常务副市长）为市委领导班子成员",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "2024.12–present"
    },
    # 何毅与任生 - 市委班子
    {
        "id": 7,
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "何毅（市长）与任生（副书记/组织部部长）同为市委领导班子成员",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "2023–present"
    },
    # 何毅与朱策 - 政府班子
    {
        "id": 8,
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "何毅（市长）与朱策（常务副市长）为市政府正副职搭档",
        "overlap_org": "黄山市人民政府",
        "overlap_period": "2023–present"
    },
    # 何毅与叶建强 - 市委班子
    {
        "id": 9,
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "何毅（市长/副书记）与叶建强（市委常委/秘书长）同为市委领导班子成员",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "2023–present"
    },
    # 任生与叶建强 - 市委班子成员
    {
        "id": 10,
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "任生（副书记/组织部部长）与叶建强（常委/秘书长）同为市委领导班子成员",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "未知–present"
    },
    # 朱策与叶建强 - 市委班子成员
    {
        "id": 11,
        "person_a": 7, "person_b": 6,
        "type": "overlap",
        "context": "朱策（常委/常务副市长）与叶建强（常委/秘书长）同为市委常委",
        "overlap_org": "中国共产党黄山市委员会",
        "overlap_period": "未知–present"
    },
]

# ── helpers ──────────────────────────────────────────────────────────────

def is_top_leader(p):
    """Return True for the party secretary (top leader)."""
    return "书记" in p["current_post"] and "副书记" not in p["current_post"]


def person_color(p):
    """Return 'r,g,b' string for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"      # Red — Party Secretary
    if "市长" in post or "区长" in post:
        return "50,100,255"     # Blue — Mayor
    if "副书记" in post:
        return "200,50,200"     # Purple — Deputy Secretary
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"      # Orange — Discipline
    return "100,100,100"        # Grey — Others


def org_color(o):
    """Return 'r,g,b' string for an org node."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "行政区域":
        return "200,255,200"
    return "200,200,200"


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── BUILD SQLite ────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ──────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>黄山市（安徽省）领导关系网络 — 市委书记、市长及领导班子成员</description>')
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

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("16.0" if "市长" in p["current_post"] else ("14.0" if "副书记" in p["current_post"] else "12.0"))
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
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
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')

    eid = 0

    # Person → Org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  黄山市（Huangshan City）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
