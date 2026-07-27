#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Gangbei District (港北区), Guigang, Guangxi.

港北区 — 贵港市市辖区，贵港市委、市政府驻地。

Covers: Party Secretary (区委书记), District Mayor (区长), leadership team,
predecessor/successor chains, and the district-level leadership network.

Sources:
- gbq.gov.cn: Official Gangbei district government website — directly accessible
- News articles from gbq.gov.cn (verified)

Generated: 2026-07-23

Important notes:
- A leadership transition occurred between late June and mid-July 2026:
  杨燕忠 (Yang Yanzhong) was Party Secretary until late June 2026.
  刘理 (Liu Li) was District Mayor until late June 2026, then promoted to Party Secretary in July 2026.
  The successor for 区长 (District Mayor) is not yet publicly identified on available sources.
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangxi_港北区")
DB_PATH = os.path.join(TMP, "港北区_network.db")
GEXF_PATH = os.path.join(TMP, "港北区_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-23"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership (as of July 2026) ──

    # 刘理 — 港北区委书记（2026.07-）
    {"id":1,"name":"刘理","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"港北区委书记","current_org":"中共贵港市港北区委员会",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930256.shtml"},

    # 杨燕忠 — 前任港北区委书记（~2026.06）
    {"id":2,"name":"杨燕忠","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"http://www.gbq.gov.cn/gdtt/t27760848.shtml"},

    # ── Deputy District Mayors (副区长, confirmed from gov disclosure page) ──
    {"id":3,"name":"刘锦棉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"港北区副区长","current_org":"贵港市港北区人民政府",
     "source":"http://www.gbq.gov.cn/xxgk/"},

    {"id":4,"name":"姚倩","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"港北区副区长","current_org":"贵港市港北区人民政府",
     "source":"http://www.gbq.gov.cn/xxgk/"},

    {"id":5,"name":"黄创鉴","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"港北区副区长","current_org":"贵港市港北区人民政府",
     "source":"http://www.gbq.gov.cn/xxgk/"},

    # ── Leadership team from July 2026 meeting signatures (班子成员) ──
    # These were listed as attending a 化解历史矛盾 work meeting chaired by 刘理 as party secretary
    {"id":6,"name":"陈宇韬","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":7,"name":"莫海华","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":8,"name":"甘孟","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":9,"name":"甘海松","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":10,"name":"黄科泉","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":11,"name":"宁鸿","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":12,"name":"李文杰","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":13,"name":"黄强","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":14,"name":"韦威华","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":15,"name":"范炳和","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":16,"name":"陈历南","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":17,"name":"谭健威","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},

    {"id":18,"name":"李娟","gender":"女","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"港北区领导","current_org":"贵港市港北区",
     "source":"http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930203.shtml"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共贵港市港北区委员会", "type": "党委", "level": "县处级", "parent": "中共贵港市委员会", "location": "广西贵港市港北区"},
    {"id": 2, "name": "贵港市港北区人民政府", "type": "政府", "level": "县处级", "parent": "贵港市人民政府", "location": "广西贵港市港北区"},
    {"id": 3, "name": "中共贵港市港北区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共贵港市港北区委员会", "location": "广西贵港市港北区"},
    {"id": 4, "name": "贵港市港北区监察委员会", "type": "纪委", "level": "县处级", "parent": "贵港市港北区人民政府", "location": "广西贵港市港北区"},
    {"id": 5, "name": "中共贵港市港北区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共贵港市港北区委员会", "location": "广西贵港市港北区"},
    {"id": 6, "name": "中共贵港市港北区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共贵港市港北区委员会", "location": "广西贵港市港北区"},
    {"id": 7, "name": "贵港市港北区人大常委会", "type": "人大", "level": "县处级", "parent": "贵港市人大常委会", "location": "广西贵港市港北区"},
    {"id": 8, "name": "贵港市港北区政协", "type": "政协", "level": "县处级", "parent": "贵港市政协", "location": "广西贵港市港北区"},
    {"id": 9, "name": "贵港市港北区人民法院", "type": "政府", "level": "县处级", "parent": "贵港市港北区人民政府", "location": "广西贵港市港北区"},
    {"id": 10, "name": "贵港市港北区人民检察院", "type": "政府", "level": "县处级", "parent": "贵港市港北区人民政府", "location": "广西贵港市港北区"},
    {"id": 11, "name": "港北区西江工业园区", "type": "开发区", "level": "县处级", "parent": "贵港市港北区人民政府", "location": "广西贵港市港北区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 刘理 — current
    {"person_id": 1, "org_id": 1, "title": "港北区委书记",
     "start_date": "2026-07", "end_date": "present", "rank": "县处级",
     "note": "晋升自港北区长。首次以区委书记身份出现在公开报道为2026年7月13日的区委常委会", "confidence": "confirmed"},

    # 刘理 — previous
    {"person_id": 1, "org_id": 2, "title": "港北区委副书记、区长",
     "start_date": "unknown", "end_date": "2026-07", "rank": "县处级",
     "note": "2026年6月25日仍以区长身份主持召开区政府常务会（第116次）", "confidence": "confirmed"},

    # 杨燕忠 — previous party secretary
    {"person_id": 2, "org_id": 1, "title": "港北区委书记",
     "start_date": "unknown", "end_date": "2026-06", "rank": "县处级",
     "note": "2026年6月5日仍以区委书记身份开展调研，6月26日检查中考备考工作。此后再无公开报道。随后刘理接任区委书记", "confidence": "confirmed"},

    # 刘锦棉
    {"person_id": 3, "org_id": 2, "title": "港北区副区长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "区政府信息公开页面显示为副区长，也在2026年7月会议列名", "confidence": "confirmed"},

    # 姚倩
    {"person_id": 4, "org_id": 2, "title": "港北区副区长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "区政府信息公开页面显示为副区长", "confidence": "confirmed"},

    # 黄创鉴
    {"person_id": 5, "org_id": 2, "title": "港北区副区长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "区政府信息公开页面显示为副区长", "confidence": "confirmed"},

    # Other leadership team members
    {"person_id": 6, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 7, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 8, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 9, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 10, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 11, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 12, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 13, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 14, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 15, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 16, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 17, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},

    {"person_id": 18, "org_id": 1, "title": "港北区领导",
     "start_date": "unknown", "end_date": "present", "rank": "",
     "note": "2026年7月化解历史矛盾工作推进会参会领导", "confidence": "confirmed"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 刘理 ↔ 杨燕忠 — 前后任书记
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "刘理接替杨燕忠任港北区委书记", "overlap_org": "中共贵港市港北区委员会", "overlap_period": "2026-07",
     "confidence": "confirmed"},

    # 刘理 — 刘锦棉 — 上下级（书记-副区长）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "刘理先后任区长、区委书记，刘锦棉为副区长", "overlap_org": "贵港市港北区", "overlap_period": "未知",
     "confidence": "confirmed"},

    # 刘理 — 姚倩 — 上下级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "刘理在职期间，姚倩为副区长", "overlap_org": "贵港市港北区", "overlap_period": "未知",
     "confidence": "confirmed"},

    # 刘理 — 黄创鉴 — 上下级
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "刘理在职期间，黄创鉴为副区长", "overlap_org": "贵港市港北区", "overlap_period": "未知",
     "confidence": "confirmed"},

    # 杨燕忠 — 刘理 — 党政搭档（杨为书记，刘为区长）
    {"person_a": 2, "person_b": 1, "type": "overlap",
     "context": "杨燕忠任区委书记期间刘理任区长，党政搭档", "overlap_org": "贵港市港北区", "overlap_period": "至2026-06",
     "confidence": "confirmed"},
]

# Remove confidence fields — they are for tracking, not for DB schema
for r in relationships:
    r.pop("confidence", None)

# =========================================================================
# HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "区长" in cp and "副" not in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "区长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    if "领导" in cp:
        return "120,120,120"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "区长" in cp and "副" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp and "区长" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "领导" in cp:
        return "10.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    """Return GEXF shape based on role."""
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    if "领导" in cp:
        return "circle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>贵港市港北区领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources, scope_job):
    """Build a single person graph JSON dict."""
    p = person
    is_party_sec = "书记" in (p.get("current_post", "")) and "副书记" not in (p.get("current_post", ""))
    rank = "县处级" if is_party_sec or "区长" in (p.get("current_post", "")) else "副县处级"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "港北区",
            "job": scope_job,
            "task_id": "guangxi_港北区",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"gangbei_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", "") if p.get("current_post") else "（已离任）",
            "current_org": p.get("current_org", ""),
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed" if p.get("current_post") else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium" if p.get("current_post") else "low",
            "biggest_gap": f"Complete career timeline, identity details (birth, birthplace, education) for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete identity details (birth date, birthplace, education, party join date) for {p['name']}",
                "why_it_matters": "Core biographical facts essential for deduplication and network analysis",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 百度百科", f"{p['name']} 出生"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"Full career timeline before current role for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 任职经历", f"{p['name']} 履历"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "港北区人民政府门户网站",
         "url": "http://www.gbq.gov.cn/", "publisher": "贵港市港北区人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Official Gangbei district government portal — directly accessible as of investigation date"},
        {"id": "S002", "title": "港北区政府信息公开-领导简介",
         "url": "http://www.gbq.gov.cn/xxgk/", "publisher": "贵港市港北区人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Government information disclosure page showing district leadership roster"},
        {"id": "S003", "title": "港北区六届人民政府第116次常务会",
         "url": "http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27824062.shtml",
         "publisher": "中国共产党贵港市港北区委员会宣传部",
         "published_at": "2026-06-26", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Confirmed 刘理 as 区长 (last known appearance in that role)"},
        {"id": "S004", "title": "港北区委常委会会议（2026-07-13）",
         "url": "http://www.gbq.gov.cn/xxgk/gzdt/zwdt2022/t27930188.shtml",
         "publisher": "中国共产党贵港市港北区委员会宣传部",
         "published_at": "2026-07-21", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Confirmed 刘理 as 区委书记 (first appearance in this role)"},
        {"id": "S005", "title": "杨燕忠开展企业纾困解难专题调研",
         "url": "http://www.gbq.gov.cn/gdtt/t27760848.shtml",
         "publisher": "中国共产党贵港市港北区委员会宣传部",
         "published_at": "2026-06-05", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Confirmed 杨燕忠 as 港北区委书记 during this period"},
    ]

    # ── 刘理 person JSON ──
    ll_timeline = [
        {"start": "2026-07", "end": "present",
         "org": "中共贵港市港北区委员会",
         "title": "港北区委书记", "level": "县处级",
         "location": "广西贵港市港北区", "system": "party",
         "rank": "县处级", "is_key_promotion": True,
         "notes": "晋升自港北区长。首次以区委书记身份出现在公开报道为2026年7月13日的区委常委会",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"start": "unknown", "end": "2026-07",
         "org": "贵港市港北区人民政府",
         "title": "港北区委副书记、区长", "level": "县处级",
         "location": "广西贵港市港北区", "system": "government",
         "rank": "县处级", "is_key_promotion": True,
         "notes": "2026年6月25日仍以区长身份主持召开区政府常务会（第116次）。此前完整履历待查",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到刘理在就任港北区长前的完整履历。其此前任职经历待查",
         "confidence": "unverified",
         "source_ids": []},
    ]
    ll_relationships = [
        {"person": "杨燕忠", "person_id": "gangbei_杨燕忠",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "刘理接替杨燕忠任港北区委书记（2026年7月）",
         "overlap_org": "中共贵港市港北区委员会",
         "overlap_period": "2026-07",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"person": "杨燕忠", "person_id": "gangbei_杨燕忠",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨燕忠任区委书记期间刘理任区长，党政搭档关系",
         "overlap_org": "贵港市港北区",
         "overlap_period": "至2026-06",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003", "S005"]},
    ]
    ll_json = build_person_json(persons[0], ll_timeline, ll_relationships, sources, "区委书记")
    ll_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-区委书记-刘理.json")
    with open(ll_path, "w", encoding="utf-8") as f:
        json.dump(ll_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {ll_path}")

    # ── 杨燕忠 person JSON ──
    yyz_timeline = [
        {"start": "unknown", "end": "2026-06",
         "org": "中共贵港市港北区委员会",
         "title": "港北区委书记", "level": "县处级",
         "location": "广西贵港市港北区", "system": "party",
         "rank": "县处级", "is_key_promotion": True,
         "notes": "2026年6月5日仍以区委书记身份开展企业调研，6月26日检查中考备考工作。此后无公开报道。去向待查",
         "confidence": "confirmed",
         "source_ids": ["S005"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到杨燕忠就任港北区委书记前的完整履历。其此前在何处任职、任港北区委书记的起始时间均待查",
         "confidence": "unverified",
         "source_ids": []},
    ]
    yyz_relationships = [
        {"person": "刘理", "person_id": "gangbei_刘理",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "刘理接替杨燕忠任港北区委书记（2026年7月）",
         "overlap_org": "中共贵港市港北区委员会",
         "overlap_period": "2026-07",
         "direction": "person_to_other",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"person": "刘理", "person_id": "gangbei_刘理",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨燕忠任区委书记期间刘理任区长，党政搭档关系",
         "overlap_org": "贵港市港北区",
         "overlap_period": "至2026-06",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003", "S005"]},
    ]
    yyz_json = build_person_json(persons[1], yyz_timeline, yyz_relationships, sources, "区委书记（前任）")
    yyz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-区委书记（前任）-杨燕忠.json")
    with open(yyz_path, "w", encoding="utf-8") as f:
        json.dump(yyz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yyz_path}")


def build():
    os.makedirs(TMP, exist_ok=True)
    print(f"=== Building {TMP} data ===")
    print(f"Staging dir: {TMP}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
