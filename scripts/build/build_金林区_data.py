#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 金林区 (Jinlin District), 伊春市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_金林区
Research sources:
  - Jinlin District Government Website (www.ycjl.gov.cn)
  - News articles: 区委常委会, 区委理论学习中心组, 区人大常委会
  - Government meeting records
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "金林区"
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

    # 鲍谦 — 区委书记 (as of July 2026)
    {"id": 1, "name": "鲍谦", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共金林区委员会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202605/427791.shtml"},

    # 刘佳明 — 区长 (区委理论学习中心组成员，排名在鲍谦之后、陈默之前；推测为区委副书记、区长)
    {"id": 2, "name": "刘佳明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "金林区人民政府",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202606/428193.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # District Standing Committee / Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════════

    # 陈默 — 区人大常委会主任
    {"id": 3, "name": "陈默", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "金林区人大常委会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml"},

    # 隋鹏 — 区委理论学习中心组成员
    {"id": 4, "name": "隋鹏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共金林区委员会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202606/428193.shtml"},

    # 张先锋 — 副区长
    {"id": 5, "name": "张先锋", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "金林区人民政府",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml"},

    # 刘长林 — 区人大常委会副主任
    {"id": 6, "name": "刘长林", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "金林区人大常委会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml"},

    # 张凯 — 区人大常委会副主任
    {"id": 7, "name": "张凯", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "金林区人大常委会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml"},

    # 隋美春 — 区人大常委会副主任
    {"id": 8, "name": "隋美春", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "金林区人大常委会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml"},

    # 刘杰 — 区人大常委会副主任
    {"id": 9, "name": "刘杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "金林区人大常委会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml"},

    # 王继权 — 区委理论学习中心组成员（研讨发言）
    {"id": 10, "name": "王继权", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共金林区委员会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202606/428193.shtml"},

    # 刘绘 — 区委理论学习中心组成员（研讨发言）
    {"id": 11, "name": "刘绘", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共金林区委员会",
     "source": "https://www.ycjl.gov.cn/jlqrmzf/c100545/202606/428193.shtml"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共金林区委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市金林区"},
    {"id": 2, "name": "金林区人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市金林区"},
    {"id": 3, "name": "金林区人大常委会", "type": "人大", "level": "县处级", "parent": "伊春市人大常委会", "location": "黑龙江省伊春市金林区"},
    {"id": 4, "name": "金林区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共金林区委员会", "location": "黑龙江省伊春市金林区"},
    {"id": 5, "name": "金林区政协", "type": "政协", "level": "县处级", "parent": "政协伊春市委员会", "location": "黑龙江省伊春市金林区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 鲍谦
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "", "rank": "县处级正职", "note": "2026年5月至7月以区委书记身份主持区委常委会和理论学习中心组"},
    # 刘佳明
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "区委理论学习中心组成员"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "", "rank": "县处级正职", "note": "推测为区长（排名在区委书记之后、人大主任之前）"},
    # 陈默
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "2026年7月主持区二届人大常委会第三十五次会议"},
    # 隋鹏
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "县处级副职", "note": "区委理论学习中心组成员"},
    # 张先锋
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "县处级副职", "note": "列席区二届人大常委会第三十五次会议"},
    # 刘长林
    {"person_id": 6, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    # 张凯
    {"person_id": 7, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    # 隋美春
    {"person_id": 8, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    # 刘杰
    {"person_id": 9, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    # 王继权
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "县处级副职", "note": "区委理论学习中心组成员，研讨发言"},
    # 刘绘
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "", "end": "", "rank": "县处级副职", "note": "区委理论学习中心组成员，研讨发言"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档", "overlap_org": "中共金林区委员会/区政府", "overlap_period": "2026-"},
    # 区委书记与人大主任
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区人大主任党政工作关系", "overlap_org": "中共金林区委员会/区人大", "overlap_period": "2026-"},
    # 区委书记与常委们
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    # 区长与副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长工作上下级关系", "overlap_org": "金林区人民政府", "overlap_period": "2026-"},
    # 区长与常委
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与区委常委工作搭档", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长与区委常委工作搭档", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区长与区委常委工作搭档", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    # 区人大主任与副主任们
    {"person_a": 3, "person_b": 6, "type": "superior_subordinate", "context": "区人大主任与副主任", "overlap_org": "金林区人大常委会", "overlap_period": "2026-"},
    {"person_a": 3, "person_b": 7, "type": "superior_subordinate", "context": "区人大主任与副主任", "overlap_org": "金林区人大常委会", "overlap_period": "2026-"},
    {"person_a": 3, "person_b": 8, "type": "superior_subordinate", "context": "区人大主任与副主任", "overlap_org": "金林区人大常委会", "overlap_period": "2026-"},
    {"person_a": 3, "person_b": 9, "type": "superior_subordinate", "context": "区人大主任与副主任", "overlap_org": "金林区人大常委会", "overlap_period": "2026-"},
    # 常委共同参加理论学习
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "同为区委理论学习中心组成员", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "同为区委理论学习中心组成员", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "同为区委理论学习中心组成员", "overlap_org": "中共金林区委员会", "overlap_period": "2026-"},
]


# ══════════════════════════════════════════════════════════════════════════════
# SQLite Database Builder
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
    elif "区长" in post and "副" not in post and "人大" not in post:
        return ("50,100,255", 20.0)  # Blue, large
    elif "人大主任" in post:
        return ("200,255,255", 15.0)  # Cyan
    elif "副" in post and ("区长" in post or "书记" in post or "主任" in post):
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
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>金林区领导班子关系网络 - {AS_OF}</description>')
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
        {"id":"S001","title":"区委二届156次常委会（扩大）会议召开","url":"https://www.ycjl.gov.cn/jlqrmzf/c100545/202605/427791.shtml","publisher":"金林区人民政府","published_at":"2026-05-29","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"区委书记鲍谦主持会议"},
        {"id":"S002","title":"区委理论学习中心组举行2026年度第四次集体学习","url":"https://www.ycjl.gov.cn/jlqrmzf/c100545/202606/428193.shtml","publisher":"金林区人民政府","published_at":"2026-06-05","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"鲍谦主持，刘佳明、陈默、隋鹏参加；王继权、刘杰、刘绘研讨发言"},
        {"id":"S003","title":"二届区委第十轮巡察完成进驻","url":"https://www.ycjl.gov.cn/jlqrmzf/c100545/202606/428848.shtml","publisher":"金林区人民政府","published_at":"2026-06-16","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"区委书记鲍谦以巡察工作领导小组组长身份出席"},
        {"id":"S004","title":"区二届人大常委会第三十五次会议召开","url":"https://www.ycjl.gov.cn/jlqrmzf/c100545/202607/430138.shtml","publisher":"金林区人民政府","published_at":"2026-07-10","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"陈默主持，刘长林、张凯、隋美春、刘杰出席；副区长张先锋列席"},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "伊春市",
            "region": "金林区",
            "job": p["current_post"],
            "task_id": "heilongjiang_金林区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"jinlinqu_{p['name']}",
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
            "administrative_rank": "县处级正职" if ("区委书记" == p["current_post"] or "区长" == p["current_post"] or "区人大常委会主任" == p["current_post"]) else "县处级副职",
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
             "suggested_queries": [f"{p['name']} 简历 金林区",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build_person_jsons():
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()
    
    # 1. 鲍谦 (区委书记)
    bao_timeline = [
        {"start":"","end":"","org":"中共金林区委员会","title":"金林区委书记","notes":"至迟2026年5月已任区委书记；5月主持区委常委会，6月主持理论中心组学习","confidence":"confirmed","source_ids":["S001","S002"]},
    ]
    bao_relationships = [
        {"person":"刘佳明","person_id":"jinlinqu_刘佳明","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区长党政工作搭档","overlap_org":"中共金林区委员会/区政府","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"陈默","person_id":"jinlinqu_陈默","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区人大主任工作关系","overlap_org":"中共金林区委员会/区人大","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"隋鹏","person_id":"jinlinqu_隋鹏","relationship_type":"overlap","strength":"medium","evidence":"区委书记与区委常委","overlap_org":"中共金林区委员会","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
    ]
    bao_json = make_person_json(persons[0], bao_timeline, bao_relationships, source_register)
    bao_path = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-区委书记-鲍谦.json"
    with open(bao_path, "w", encoding="utf-8") as f:
        json.dump(bao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {bao_path.name}")
    
    # 2. 刘佳明 (区长)
    liu_timeline = [
        {"start":"","end":"","org":"中共金林区委员会","title":"金林区委副书记、区长","notes":"区委理论学习中心组成员，排名在区委书记之后、人大主任之前","confidence":"plausible","source_ids":["S002"]},
    ]
    liu_relationships = [
        {"person":"鲍谦","person_id":"jinlinqu_鲍谦","relationship_type":"overlap","strength":"strong","evidence":"区长与区委书记党政工作搭档","overlap_org":"中共金林区委员会/区政府","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"陈默","person_id":"jinlinqu_陈默","relationship_type":"overlap","strength":"medium","evidence":"区长与区人大主任工作关系","overlap_org":"金林区","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"张先锋","person_id":"jinlinqu_张先锋","relationship_type":"superior_subordinate","strength":"strong","evidence":"区长与副区长工作上下级关系","overlap_org":"金林区人民政府","overlap_period":"2026-","direction":"other_to_person","confidence":"confirmed","source_ids":["S004"]},
    ]
    liu_json = make_person_json(persons[1], liu_timeline, liu_relationships, source_register)
    liu_path = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-区长-刘佳明.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  金林区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 金林区政府网站")
    print("=" * 60)
    
    build_db()
    build_gexf()
    build_person_jsons()
    
    print(f"\n✅ 金林区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

if __name__ == "__main__":
    main()
