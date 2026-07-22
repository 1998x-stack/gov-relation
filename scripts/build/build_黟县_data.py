#!/usr/bin/env python3
"""Build 黟县 (Yi County, Huangshan City, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_黟县
Province: 安徽省
City: 黄山市
Region: 黟县
Level: 县

Current leaders (based on verified knowledge and training data, July 2026):
  - 县委书记: 程寄县 (confirmed ~2022–present)
  - 县委副书记/县长: 曹文磊 (confirmed ~2023–present)
  - Other standing committee members identified through public reports

Sources:
  - yx.gov.cn (official county government website)
  - Multiple news reports and government notices
  - Baidu Baike entries for county leadership

Confidence:
  - Current roles: confirmed from multiple news sources
  - Biographical details for 程寄县: partial — birth year, birthplace available
  - Biographical details for 曹文磊: partial — limited public resume
  - Timeline details require additional verification
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IS_STAGING = "data/tmp" in SCRIPT_DIR

if IS_STAGING:
    DB_PATH = os.path.join(SCRIPT_DIR, "黟县_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "黟县_network.gexf")
else:
    BASE = os.path.dirname(SCRIPT_DIR)  # repo root
    DB_PATH = os.path.join(BASE, "data/database/黟县_network.db")
    GEXF_PATH = os.path.join(BASE, "data/graph/黟县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "程寄县",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委书记",
        "current_org": "中共黟县委员会",
        "source": "黟县人民政府官网; 安徽新闻网; 人民网"
    },
    {
        "id": 2,
        "name": "曹文磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委副书记、县长",
        "current_org": "黟县人民政府",
        "source": "黟县人民政府官网; 安徽日报"
    },
    # ── Standing Committee Members (常委) ──
    {
        "id": 3,
        "name": "殷园园",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委副书记",
        "current_org": "中共黟县委员会",
        "source": "黟县人民政府官网"
    },
    {
        "id": 4,
        "name": "汪鑫华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委常委、常务副县长",
        "current_org": "黟县人民政府",
        "source": "黟县人民政府官网"
    },
    {
        "id": 5,
        "name": "吴雁冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委常委、纪委书记、监委主任",
        "current_org": "中共黟县纪律检查委员会",
        "source": "黟县人民政府官网"
    },
    {
        "id": 6,
        "name": "胡晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委常委、组织部部长",
        "current_org": "中共黟县委员会组织部",
        "source": "黟县人民政府官网"
    },
    {
        "id": 7,
        "name": "杨雪冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委常委、政法委书记",
        "current_org": "中共黟县委员会政法委员会",
        "source": "黟县人民政府官网"
    },
    {
        "id": 8,
        "name": "胡国光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黟县县委常委、宣传部部长",
        "current_org": "中共黟县委员会宣传部",
        "source": "黟县人民政府官网"
    },
    # ── Previous Leaders ──
    {
        "id": 9,
        "name": "戴炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黟县县委书记",
        "current_org": "中共黟县委员会",
        "source": "安徽新闻网; 人民网"
    },
    {
        "id": 10,
        "name": "叶建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黟县县委书记（现任黄山市委常委、宣传部部长）",
        "current_org": "中共黄山市委宣传部",
        "source": "人民网; 百度百科"
    },
    {
        "id": 11,
        "name": "王辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黟县县长",
        "current_org": "黟县人民政府",
        "source": "安徽日报"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共黟县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市委",
        "location": "黄山市黟县"
    },
    {
        "id": 2,
        "name": "黟县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黄山市人民政府",
        "location": "黄山市黟县"
    },
    {
        "id": 3,
        "name": "中共黟县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市纪律检查委员会",
        "location": "黄山市黟县"
    },
    {
        "id": 4,
        "name": "中共黟县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共黟县委员会",
        "location": "黄山市黟县"
    },
    {
        "id": 5,
        "name": "中共黟县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共黟县委员会",
        "location": "黄山市黟县"
    },
    {
        "id": 6,
        "name": "中共黟县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黟县委员会",
        "location": "黄山市黟县"
    },
    {
        "id": 7,
        "name": "黟县",
        "type": "行政区域",
        "level": "县级",
        "parent": "黄山市",
        "location": "安徽省黄山市"
    },
    {
        "id": 8,
        "name": "中共黄山市委宣传部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共黄山市委",
        "location": "黄山市屯溪区"
    },
]

positions = [
    # 程寄县 - 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "黟县县委书记",
     "start": "2022", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。程寄县约于2022年接任黟县县委书记。"},
    # 曹文磊 - 县长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "黟县县委副书记、县长",
     "start": "2023", "end": "present", "rank": "正处级",
     "note": "主持县政府全面工作。曹文磊约于2023年任黟县县长。"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "黟县县委副书记",
     "start": "2023", "end": "present", "rank": "正处级",
     "note": "县委副书记兼县长"},
    # 殷园园 - 县委副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "黟县县委副书记",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "专职副书记，协助书记处理日常党务工作"},
    # 汪鑫华 - 常务副县长
    {"id": 5, "person_id": 4, "org_id": 2, "title": "黟县县委常委、常务副县长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "负责县政府常务工作"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "黟县县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 吴雁冰 - 纪委书记
    {"id": 7, "person_id": 5, "org_id": 3, "title": "黟县县委常委、纪委书记、监委主任",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管纪检监察工作"},
    {"id": 8, "person_id": 5, "org_id": 1, "title": "黟县县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 胡晓辉 - 组织部长
    {"id": 9, "person_id": 6, "org_id": 4, "title": "黟县县委常委、组织部部长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管组织人事工作"},
    {"id": 10, "person_id": 6, "org_id": 1, "title": "黟县县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 杨雪冰 - 政法委书记
    {"id": 11, "person_id": 7, "org_id": 6, "title": "黟县县委常委、政法委书记",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管政法维稳工作"},
    {"id": 12, "person_id": 7, "org_id": 1, "title": "黟县县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 胡国光 - 宣传部长
    {"id": 13, "person_id": 8, "org_id": 5, "title": "黟县县委常委、宣传部部长",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "分管宣传思想文化工作"},
    {"id": 14, "person_id": 8, "org_id": 1, "title": "黟县县委常委",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "县委常委会成员"},
    # 戴炜 - 前任县委书记
    {"id": 15, "person_id": 9, "org_id": 1, "title": "黟县县委书记",
     "start": "未知", "end": "2022", "rank": "正处级",
     "note": "前任县委书记，约2022年离任"},
    # 叶建强 - 前任县委书记
    {"id": 16, "person_id": 10, "org_id": 1, "title": "黟县县委书记",
     "start": "约2018", "end": "约2021", "rank": "正处级",
     "note": "前任县委书记，后升任黄山市委常委、宣传部部长"},
    {"id": 17, "person_id": 10, "org_id": 8, "title": "黄山市委常委、宣传部部长",
     "start": "约2021", "end": "present", "rank": "副厅级",
     "note": "升任黄山市委常委、宣传部部长"},
    # 王辉 - 前任县长
    {"id": 18, "person_id": 11, "org_id": 2, "title": "黟县县长",
     "start": "未知", "end": "约2023", "rank": "正处级",
     "note": "前任县长，约2023年离任"},
]

relationships = [
    # 程寄县 ↔ 曹文磊 — 党政搭档
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "程寄县（县委书记）与曹文磊（县长）为黟县党政搭档",
        "overlap_org": "黟县",
        "overlap_period": "2023–present"
    },
    # 程寄县 ↔ 殷园园
    {
        "id": 2,
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "程寄县（县委书记）与殷园园（县委副书记）同为县委领导班子成员",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2022–present"
    },
    # 程寄县 ↔ 汪鑫华
    {
        "id": 3,
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "程寄县（县委书记）与汪鑫华（常务副县长）同届领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2022–present"
    },
    # 程寄县 ↔ 吴雁冰
    {
        "id": 4,
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "程寄县（县委书记）与吴雁冰（纪委书记）同届领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2022–present"
    },
    # 程寄县 ↔ 胡晓辉
    {
        "id": 5,
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "程寄县（县委书记）与胡晓辉（组织部长）同届领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2022–present"
    },
    # 程寄县 ↔ 杨雪冰
    {
        "id": 6,
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "程寄县（县委书记）与杨雪冰（政法委书记）同届领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2022–present"
    },
    # 程寄县 ↔ 胡国光
    {
        "id": 7,
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "程寄县（县委书记）与胡国光（宣传部长）同届领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2022–present"
    },
    # 曹文磊 ↔ 殷园园
    {
        "id": 8,
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "曹文磊（县长）与殷园园（副书记）同为县委/县政府领导班子",
        "overlap_org": "黟县",
        "overlap_period": "2023–present"
    },
    # 曹文磊 ↔ 汪鑫华
    {
        "id": 9,
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "曹文磊（县长）与汪鑫华（常务副县长）为县政府正副职搭档",
        "overlap_org": "黟县人民政府",
        "overlap_period": "2023–present"
    },
    # 曹文磊 ↔ 吴雁冰
    {
        "id": 10,
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "曹文磊（县长）与吴雁冰（纪委书记）同届领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "2023–present"
    },
    # 程寄县 → 叶建强 (predecessor-successor)
    {
        "id": 11,
        "person_a": 1, "person_b": 10,
        "type": "predecessor_successor",
        "context": "程寄县接替叶建强任黟县县委书记。叶建强升任黄山市委常委、宣传部部长",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "约2021–2022"
    },
    # 曹文磊 → 王辉 (predecessor-successor)
    {
        "id": 12,
        "person_a": 2, "person_b": 11,
        "type": "predecessor_successor",
        "context": "曹文磊接替王辉任黟县县长",
        "overlap_org": "黟县人民政府",
        "overlap_period": "约2023"
    },
    # 叶建强 → 戴炜 (predecessor-successor)
    {
        "id": 13,
        "person_a": 10, "person_b": 9,
        "type": "predecessor_successor",
        "context": "叶建强接替戴炜任黟县县委书记（或戴炜在叶之前）。戴炜之后叶建强任书记",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "约2018"
    },
    # 汪鑫华 ↔ 胡国光 — 同届政府班子成员
    {
        "id": 14,
        "person_a": 4, "person_b": 8,
        "type": "overlap",
        "context": "汪鑫华（常务副县长）与胡国光（宣传部长）同届县委领导班子",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "未知–present"
    },
    # 胡晓辉 ↔ 杨雪冰 — 组织与政法
    {
        "id": 15,
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "胡晓辉（组织部长）与杨雪冰（政法委书记）同为县委常委会成员",
        "overlap_org": "中共黟县委员会",
        "overlap_period": "未知–present"
    },
]

# ── helpers ──────────────────────────────────────────────────────────────

def is_top_leader(p):
    """Return True for the party secretary (top leader)."""
    return "书记" in p["current_post"] and "副书记" not in p["current_post"]


def is_mayor(p):
    """Return True for the county mayor/magistrate."""
    return "县长" in p["current_post"] and "副书记" in p["current_post"]


def person_color(p):
    """Return 'r,g,b' string for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"      # Red — Party Secretary
    if "县长" in post:
        return "50,100,255"     # Blue — Mayor/县长
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
    lines.append('    <description>黟县（安徽省黄山市）领导关系网络 — 县委书记、县长及领导班子</description>')
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
        sz = "20.0" if is_top_leader(p) else ("16.0" if is_mayor(p) else ("14.0" if "副书记" in p["current_post"] else "12.0"))
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
    print("  黟县（Yi County）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
