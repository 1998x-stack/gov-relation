#!/usr/bin/env python3
"""
当涂县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Dangtu County leadership network.

Task ID: anhui_当涂县
Province: 安徽省
Parent City: 马鞍山市
Level: 县
Targets: 县委书记 & 县长

Data sources:
  - 当涂县人民政府领导之窗 (dangtu.gov.cn/ldzc/) — official roster
  - 马鞍山市人民政府领导之窗 (mas.gov.cn) — city-level leaders
  - 阙方俊: previous 当涂县委书记, now 马鞍山市委常委
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.abspath(os.path.join(BASE_DIR, "../.."))
DB_PATH = os.path.join(BASE_DIR, "当涂县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "当涂县_network.gexf")

# ═══════════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════════

# Person ID convention: dangtu_{surname_givenname}
# For deduplication across the broader Ma'anshan network

persons = [
    # ═══ Top Leaders ═══
    {
        "id": "dangtu_weibangjun",
        "name": "魏邦军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共当涂县委书记",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "1975年10月出生，研究生学历。主持县委全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_wangwen",
        "name": "王文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共当涂县委副书记、县长",
        "current_org": "当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "1975年1月出生，大学学历。领导县政府全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_quefangjun",
        "name": "阙方俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "马鞍山市委常委（原当涂县委书记）",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "前当涂县委书记，现任马鞍山市委常委。具体分工待确认。",
        "confidence": "confirmed"
    },

    # ═══ Party Committee Deputy Secretaries ═══
    {
        "id": "dangtu_zhangqi",
        "name": "张麒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共当涂县委副书记",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委副书记。具体分工待确认。",
        "confidence": "confirmed"
    },

    # ═══ Standing Committee Members (县委常委) ═══
    {
        "id": "dangtu_zhangsimei",
        "name": "张四梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_maoyifeng",
        "name": "毛宜峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_huhongyang",
        "name": "胡宏扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共当涂县委员会/当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委、副县长。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_guochuanbao",
        "name": "郭传保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_zhouyihao",
        "name": "周义好",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_gengliangcheng",
        "name": "耿良成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_wangyanfeng",
        "name": "王岩峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_nihongzhen",
        "name": "倪洪振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共当涂县委员会",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },

    # ═══ Deputy County Magistrates (副县长) ═══
    {
        "id": "dangtu_tanglu",
        "name": "唐璐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "副县长。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_wuchao",
        "name": "吴超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "副县长。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_sunfagen",
        "name": "孙发根",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "副县长。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_xuyong",
        "name": "徐永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "副县长。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": "dangtu_bianxin",
        "name": "卞馨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "当涂县人民政府",
        "source": "https://www.dangtu.gov.cn/ldzc/",
        "notes": "副县长。具体分工待确认。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": "org_dangtu_party",
        "name": "中共当涂县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共马鞍山市委",
        "location": "安徽省马鞍山市当涂县"
    },
    {
        "id": "org_dangtu_gov",
        "name": "当涂县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "马鞍山市人民政府",
        "location": "安徽省马鞍山市当涂县"
    },
    {
        "id": "org_dangtu_discipline",
        "name": "中共当涂县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共当涂县委员会",
        "location": "安徽省马鞍山市当涂县"
    },
    {
        "id": "org_mas_party",
        "name": "中共马鞍山市委",
        "type": "党委",
        "level": "地级",
        "parent": "中共安徽省委",
        "location": "安徽省马鞍山市"
    },
]

positions = [
    # 魏邦军 - 县委书记
    {"person_id": "dangtu_weibangjun", "org_id": "org_dangtu_party",
     "title": "县委书记", "start": "", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。"},

    # 王文 - 县长
    {"person_id": "dangtu_wangwen", "org_id": "org_dangtu_gov",
     "title": "县长、县委副书记", "start": "", "end": "present", "rank": "正处级",
     "note": "领导县政府全面工作。负责审计方面工作。"},
    {"person_id": "dangtu_wangwen", "org_id": "org_dangtu_party",
     "title": "县委副书记", "start": "", "end": "present", "rank": "正处级",
     "note": "县委副书记。"},

    # 阙方俊 - 前县委书记，现市委常委
    {"person_id": "dangtu_quefangjun", "org_id": "org_dangtu_party",
     "title": "前县委书记", "start": "", "end": "present", "rank": "正处级→副厅级",
     "note": "此前担任当涂县委书记。现任马鞍山市委常委。"},
    {"person_id": "dangtu_quefangjun", "org_id": "org_mas_party",
     "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "马鞍山市委常委。"},

    # 张麒 - 县委副书记
    {"person_id": "dangtu_zhangqi", "org_id": "org_dangtu_party",
     "title": "县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "专职副书记。"},

    # 县委常委
    {"person_id": "dangtu_zhangsimei", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_maoyifeng", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_huhongyang", "org_id": "org_dangtu_party",
     "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "兼任副县长。"},
    {"person_id": "dangtu_huhongyang", "org_id": "org_dangtu_gov",
     "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "县委常委、副县长。"},
    {"person_id": "dangtu_guochuanbao", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_zhouyihao", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_gengliangcheng", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_wangyanfeng", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_nihongzhen", "org_id": "org_dangtu_party",
     "title": "县委常委", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},

    # 副县长
    {"person_id": "dangtu_tanglu", "org_id": "org_dangtu_gov",
     "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_wuchao", "org_id": "org_dangtu_gov",
     "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_sunfagen", "org_id": "org_dangtu_gov",
     "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_xuyong", "org_id": "org_dangtu_gov",
     "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
    {"person_id": "dangtu_bianxin", "org_id": "org_dangtu_gov",
     "title": "副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "具体分工待确认。"},
]

relationships = [
    # 魏邦军 ↔ 王文 (党政正职搭档)
    {"person_a": "dangtu_weibangjun", "person_b": "dangtu_wangwen",
     "type": "superior_subordinate",
     "context": "党政正职搭档：魏邦军任县委书记，王文任县长",
     "overlap_org": "当涂县党政领导班子",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},

    # 阙方俊 → 魏邦军 (前任→现任县委书记)
    {"person_a": "dangtu_quefangjun", "person_b": "dangtu_weibangjun",
     "type": "predecessor_successor",
     "context": "阙方俊此前担任当涂县委书记，魏邦军接任县委书记。阙方俊现任马鞍山市委常委。",
     "overlap_org": "中共当涂县委员会",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},

    # 魏邦军 → 张麒 (书记-副书记)
    {"person_a": "dangtu_weibangjun", "person_b": "dangtu_zhangqi",
     "type": "superior_subordinate",
     "context": "魏邦军为县委书记，张麒为县委副书记",
     "overlap_org": "中共当涂县委员会",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},

    # 王文 → 张麒 (县长-副书记)
    {"person_a": "dangtu_wangwen", "person_b": "dangtu_zhangqi",
     "type": "overlap",
     "context": "同为县委领导班子成员",
     "overlap_org": "中共当涂县委员会",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},

    # 魏邦军与各位县委常委的关系
    {"person_a": "dangtu_weibangjun", "person_b": "dangtu_huhongyang",
     "type": "superior_subordinate",
     "context": "魏邦军为县委书记，胡宏扬为县委常委",
     "overlap_org": "中共当涂县委员会",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════
# SQLite DATABASE
# ═══════════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
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
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        "end" TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════
# GEXF GRAPH
# ═══════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = p.get("current_post", "")
    if "县委书记" in title:
        return "255,50,50"
    if "县长" in title:
        return "50,100,255"
    return "100,100,100"

def is_top_leader(p):
    return "县委书记" in p.get("current_post", "") or "县长" in p.get("current_post", "")

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    return "200,200,200"

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>当涂县领导班子工作关系网络 - 安徽省马鞍山市当涂县</description>')
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
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization edges (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person edges (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH) or ".", exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("当涂县领导班子工作关系网络 - 数据构建")
    print("=" * 60)
    create_db()
    create_gexf()
    print()
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print()
    print("Done.")
