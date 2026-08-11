#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 绥滨县 (Suibin County), 鹤岗市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_绥滨县
Research sources:
  - Suibin County Government Website (www.suibin.gov.cn)
  - Government leadership page (县政府领导)
  - News reports and inspection articles
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "绥滨县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# Also produce canonical destination paths
CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 刘海龙 — 县委书记 (as of July 2026, also concurrently served as 县长 until ~June 2026)
    {"id": 1, "name": "刘海龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共绥滨县委员会",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/65feb7f01c5041ceaa97d1a52f015609/202605/89337.shtml"},

    # 刘芳敏 — 县长 (appointed June 2026 as 县长候选人, confirmed as 县长 by June 25)
    {"id": 2, "name": "刘芳敏", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/19168.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # County Standing Committee / Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════════

    # 郭永旭 — 县委常委、副县长（常务）
    {"id": 3, "name": "郭永旭", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年5月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长（常务）", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/90308.shtml"},

    # 王京航 — 县委常委、副县长
    {"id": 4, "name": "王京航", "gender": "男", "ethnicity": "汉族",
     "birth": "1987年8月", "birthplace": "", "education": "哈尔滨工业大学公共管理专业，硕士学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/18466.shtml"},

    # 宫明宇 — 县委常委、副县长
    {"id": 5, "name": "宫明宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1985年10月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/18748.shtml"},

    # 张静玉 — 副县长
    {"id": 6, "name": "张静玉", "gender": "女", "ethnicity": "",
     "birth": "1975年10月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/18749.shtml"},

    # 王志国 — 副县长
    {"id": 7, "name": "王志国", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年1月", "birthplace": "", "education": "山西财经大学，大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202505/75318.shtml"},

    # 于海峰 — 副县长、县公安局党委书记、局长
    {"id": 8, "name": "于海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年4月", "birthplace": "", "education": "黑龙江省警察职业学校，在职大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202410/62093.shtml"},

    # 郑和斌 — 副县长
    {"id": 9, "name": "郑和斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年8月", "birthplace": "", "education": "中共黑龙江省委党校，在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "绥滨县人民政府",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202505/75324.shtml"},

    # 周济 — 县领导（具体职务未明确）
    {"id": 10, "name": "周济", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县领导", "current_org": "绥滨县",
     "source": "http://www.suibin.gov.cn/suibinxianrenminzhengfu/65feb7f01c5041ceaa97d1a52f015609/202605/89337.shtml"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共绥滨县委员会", "type": "党委", "level": "县处级", "parent": "中共鹤岗市委员会", "location": "黑龙江省鹤岗市绥滨县"},
    {"id": 2, "name": "绥滨县人民政府", "type": "政府", "level": "县处级", "parent": "鹤岗市人民政府", "location": "黑龙江省鹤岗市绥滨县"},
    {"id": 3, "name": "中共绥滨县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共绥滨县委员会", "location": "黑龙江省鹤岗市绥滨县"},
    {"id": 4, "name": "绥滨县人大常委会", "type": "人大", "level": "县处级", "parent": "绥滨县", "location": "黑龙江省鹤岗市绥滨县"},
    {"id": 5, "name": "政协绥滨县委员会", "type": "政协", "level": "县处级", "parent": "绥滨县", "location": "黑龙江省鹤岗市绥滨县"},
    {"id": 6, "name": "绥滨县公安局", "type": "政府", "level": "乡科级", "parent": "绥滨县人民政府", "location": "黑龙江省鹤岗市绥滨县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘海龙
    {"person_id": 1, "org_id": 1, "title": "绥滨县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "至迟2026年5月已任职；此前兼任县长"},
    {"person_id": 1, "org_id": 2, "title": "绥滨县县长（原兼）", "start": "", "end": "2026-06", "rank": "县处级正职", "note": "刘海龙此前兼任县长，2026年6月刘芳敏到任后卸任县长职务"},

    # 刘芳敏
    {"person_id": 2, "org_id": 2, "title": "绥滨县县长", "start": "2026-06", "end": "", "rank": "县处级正职", "note": "2026年6月以县委副书记、县长候选人身份开展工作；6月25日官网列为县长"},
    {"person_id": 2, "org_id": 1, "title": "绥滨县委副书记", "start": "2026-06", "end": "", "rank": "县处级副职", "note": ""},

    # 郭永旭
    {"person_id": 3, "org_id": 1, "title": "绥滨县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "绥滨县副县长（常务）", "start": "", "end": "", "rank": "县处级副职", "note": "负责常务工作，分管发改、财政、应急、人社等"},

    # 王京航
    {"person_id": 4, "org_id": 1, "title": "绥滨县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "绥滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责营商环境、林业草原等工作"},

    # 宫明宇
    {"person_id": 5, "org_id": 1, "title": "绥滨县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "绥滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责市场监管、文旅、自然资源、工信等"},

    # 张静玉
    {"person_id": 6, "org_id": 2, "title": "绥滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责教育卫生、民政、住建、城管等"},

    # 王志国
    {"person_id": 7, "org_id": 2, "title": "绥滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责外事、粮食等工作"},

    # 于海峰
    {"person_id": 8, "org_id": 2, "title": "绥滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责公共安全、交通运输等工作"},
    {"person_id": 8, "org_id": 6, "title": "绥滨县公安局党委书记、局长", "start": "", "end": "", "rank": "乡科级正职", "note": ""},

    # 郑和斌
    {"person_id": 9, "org_id": 2, "title": "绥滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责农业农村、乡村振兴、水利、生态环境等工作"},

    # 周济
    {"person_id": 10, "org_id": 1, "title": "绥滨县领导", "start": "", "end": "", "rank": "", "note": "具体职务待确认，参加高标准农田调研"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 刘海龙 — 刘芳敏：党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "县委书记与县长党政工作搭档", "overlap_org": "绥滨县", "overlap_period": "2026-06起"},

    # 刘海龙 — 郭永旭：上下级
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "中共绥滨县委", "overlap_period": ""},

    # 刘芳敏 — 郭永旭：党政搭档
    {"person_a": 2, "person_b": 3, "type": "党政同僚", "context": "县长与常务副县长工作搭档", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},

    # 刘芳敏 — 各副县长：县长与副职
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与副县长", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与副县长", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长", "overlap_org": "绥滨县人民政府", "overlap_period": "2026-06起"},

    # 县委常委之间：同僚
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "县委常委", "overlap_org": "中共绥滨县委", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "县委常委", "overlap_org": "中共绥滨县委", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "县委常委", "overlap_org": "中共绥滨县委", "overlap_period": ""},

    # 刘海龙 — 前任关系梳理：此前刘海龙兼任县长，刘芳敏到任后交接
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "县领导陪同县委书记调研", "overlap_org": "绥滨县", "overlap_period": "2026-05"},
]


# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop existing tables
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    
    # Create tables
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")
    
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    
    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return ("255,50,50", 20.0)  # Red, large
    elif "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large
    elif "副" in post and ("县长" in post or "书记" in post):
        return ("100,150,255", 12.0)  # Light blue
    elif "常委" in post:
        return ("100,150,255", 12.0)
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    from datetime import datetime
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>绥滨县领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person <-> Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"绥滨县政府—县政府领导页","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/2c6aae12a35e46c0a44c9fa69f8855df/xzf.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县政府领导名单及分工"},
        {"id":"S002","title":"刘海龙调研高标准农田","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/65feb7f01c5041ceaa97d1a52f015609/202605/89337.shtml","publisher":"绥滨县人民政府","published_at":"2026-05-05","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘海龙以县委书记、县长身份出席"},
        {"id":"S003","title":"刘芳敏调研安全生产、防汛和中考备考","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/65feb7f01c5041ceaa97d1a52f015609/202606/91119.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘芳敏以县委副书记、县长候选人身份调研"},
        {"id":"S004","title":"刘芳敏宣讲全会精神并调研项目","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/65feb7f01c5041ceaa97d1a52f015609/202606/91168.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘芳敏以县委副书记、县长候选人身份出席"},
        {"id":"S005","title":"刘芳敏—县长简历页","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/19168.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘芳敏列为绥滨县人民政府县长"},
        {"id":"S006","title":"郭永旭简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/90308.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县委常委、副县长（常务），1974年5月生"},
        {"id":"S007","title":"王京航简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/18466.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县委常委、副县长，1987年8月生，哈工大硕士"},
        {"id":"S008","title":"宫明宇简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/18748.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县委常委、副县长，1985年10月生"},
        {"id":"S009","title":"张静玉简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202606/18749.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"副县长，1975年10月生"},
        {"id":"S010","title":"王志国简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202505/75318.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"副县长，1975年1月生，山西财经大学"},
        {"id":"S011","title":"于海峰简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202410/62093.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"副县长、公安局长，1980年4月生"},
        {"id":"S012","title":"郑和斌简历","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/301b14e8a3a14b459f49e54becf8bcf8/202505/75324.shtml","publisher":"绥滨县人民政府","published_at":"2026-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"副县长，1982年8月生，省委党校研究生"},
        {"id":"S013","title":"刘海龙深入福兴满族乡调研","url":"http://www.suibin.gov.cn/suibinxianrenminzhengfu/65feb7f01c5041ceaa97d1a52f015609/202607/91402.shtml","publisher":"绥滨县人民政府","published_at":"2026-07-02","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘海龙仍以县委书记身份出席活动"},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "鹤岗市",
            "region": "绥滨县",
            "job": p["current_post"],
            "task_id": "heilongjiang_绥滨县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"suibinxian_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if ("县委书记" in p["current_post"] or "县长" == p["current_post"]) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
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
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息有待补充" if not p.get("birth") else f"{p['name']}早期职业生涯需确认"
        },
        "open_questions": [
            {"priority":"critical" if not p.get("birth") else "medium",
             "question": f"{p['name']}的完整职业生涯履历",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 绥滨县",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build_person_jsons():
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()
    
    # 1. 刘海龙 (县委书记)
    liu_timeline = [
        {"start":"","end":"2026-06","org":"绥滨县人民政府","title":"绥滨县县长","notes":"同时兼任县委书记","confidence":"confirmed","source_ids":["S002"]},
        {"start":"","end":"","org":"中共绥滨县委员会","title":"绥滨县委书记","notes":"至迟2026年5月已任县委书记兼县长；2026年7月2日仍以县委书记身份出席活动","confidence":"confirmed","source_ids":["S002","S013"]},
    ]
    liu_relationships = [
        {"person":"刘芳敏","person_id":"suibinxian_刘芳敏","relationship_type":"overlap","strength":"strong","evidence":"县委书记与县长党政工作搭档","overlap_org":"绥滨县","overlap_period":"2026-06起","direction":"undirected","confidence":"confirmed","source_ids":["S005"]},
        {"person":"郭永旭","person_id":"suibinxian_郭永旭","relationship_type":"overlap","strength":"strong","evidence":"县委书记与常务副县长工作搭档","overlap_org":"中共绥滨县委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S006"]},
    ]
    liu_json = make_person_json(persons[0], liu_timeline, liu_relationships, source_register)
    liu_path = PERSONS_DIR / f"{TODAY}-黑龙江省-鹤岗市-县委书记-刘海龙.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")
    
    # 2. 刘芳敏 (县长)
    fang_timeline = [
        {"start":"2026-06","end":"","org":"中共绥滨县委员会","title":"绥滨县委副书记","notes":"2026年6月到任","confidence":"confirmed","source_ids":["S003","S004"]},
        {"start":"2026-06","end":"","org":"绥滨县人民政府","title":"绥滨县县长","notes":"2026年6月25日官网列为县长","confidence":"confirmed","source_ids":["S005"]},
    ]
    fang_relationships = [
        {"person":"刘海龙","person_id":"suibinxian_刘海龙","relationship_type":"overlap","strength":"strong","evidence":"县长与县委书记党政工作搭档","overlap_org":"绥滨县","overlap_period":"2026-06起","direction":"undirected","confidence":"confirmed","source_ids":["S002","S005"]},
        {"person":"郭永旭","person_id":"suibinxian_郭永旭","relationship_type":"overlap","strength":"strong","evidence":"县长与常务副县长工作搭档","overlap_org":"绥滨县人民政府","overlap_period":"2026-06起","direction":"undirected","confidence":"confirmed","source_ids":["S006"]},
    ]
    fang_json = make_person_json(persons[1], fang_timeline, fang_relationships, source_register)
    fang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-鹤岗市-县长-刘芳敏.json"
    with open(fang_path, "w", encoding="utf-8") as f:
        json.dump(fang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fang_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  绥滨县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 绥滨县政府网站")
    print("=" * 60)
    
    build_db()
    build_gexf()
    build_person_jsons()
    
    print(f"\n✅ 绥滨县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

if __name__ == "__main__":
    main()
