#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汝南县 (Runan County), 河南省.

Investigation date: 2026-07-25
Task ID: henan_汝南县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.runan.gov.cn — 汝南县人民政府网站 (primary, accessed 2026-07-25)
  - 政务公开 > 领导信息 (runan.gov.cn/zwgk/) — confirmed 县政府领导班子
  - 县级要闻 news articles confirming 刘光辉 as 县长

Confidence notes:
  - 刘光辉: confirmed as 县委副书记、县政府县长 via official government website (as of 2026-07-24)
  - 孙伟/王文斌/廖向东/郭海亮/陈鹏/姚树祎: confirmed as 县政府领导 via official website
  - 县委书记: NOT identified from fetched pages — county party secretary page not accessible
  - Full career timelines missing — only current roles confirmed from official sources
  - Detailed biographical data (birthdate, birthplace, education) marked as unverified
  - Exa API rate-limited, Baidu/Google blocked, Jina reader timeout — degraded web access
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ├─ Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "汝南县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ├─ Source Register ────────────────────────────────────────────────────────
sources = [
    {
        "id": "S001",
        "title": "汝南县人民政府 > 政务公开 > 领导信息",
        "url": "http://www.runan.gov.cn/zwgk/",
        "publisher": "汝南县人民政府",
        "published_at": "2026-07-25",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 县政府领导班子: 刘光辉(县长), 孙伟, 王文斌, 廖向东, 郭海亮, 陈鹏, 姚树祎"
    },
    {
        "id": "S002",
        "title": "汝南县人民政府 — 县级要闻: 刘光辉到开发区调研高质量发展重点项目建设工作",
        "url": "http://www.runan.gov.cn/",
        "publisher": "汝南县人民政府",
        "published_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 刘光辉(县委副书记、县长) acting in executive capacity"
    },
    {
        "id": "S003",
        "title": "汝南县人民政府 — 十四届县委常委会第129次（扩大）会议召开",
        "url": "http://www.runan.gov.cn/",
        "publisher": "汝南县人民政府",
        "published_at": "2026-07-15",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 十四届汝南县委 standing committee in session"
    },
]

# ├─ Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (县政府领导 — from official website)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县长",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Confirmed as 县委副书记、县政府县长、党组书记 via official leadership page. Also active in news articles (2026-07-23 调研开发区). Public biographical details unavailable from official sources."
    },
    {
        "id": 2,
        "name": "孙伟",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府领导",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Listed as 县政府领导 on official website. Specific role/division unclear."
    },
    {
        "id": 3,
        "name": "王文斌",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府领导",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Listed as 县政府领导 on official website. Specific role/division unclear."
    },
    {
        "id": 4,
        "name": "廖向东",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府领导",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Listed as 县政府领导 on official website. Specific role/division unclear."
    },
    {
        "id": 5,
        "name": "郭海亮",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府领导",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Listed as 县政府领导 on official website. Specific role/division unclear."
    },
    {
        "id": 6,
        "name": "陈鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府领导",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Listed as 县政府领导 on official website. Specific role/division unclear."
    },
    {
        "id": 7,
        "name": "姚树祎",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府领导",
        "current_org": "汝南县人民政府",
        "source": "http://www.runan.gov.cn/zwgk/",
        "notes": "Listed as 县政府领导 on official website. Specific role/division unclear."
    },
]

# ├─ Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共汝南县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共驻马店市委员会",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 2,
        "name": "汝南县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "驻马店市人民政府",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 3,
        "name": "汝南县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 4,
        "name": "汝南县政协委员会",
        "type": "政协",
        "level": "县级",
        "parent": "",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 5,
        "name": "中共汝南县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汝南县委员会",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 6,
        "name": "汝南县监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 7,
        "name": "汝南县人民法院",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "河南省驻马店市汝南县",
    },
    {
        "id": 8,
        "name": "汝南县人民检察院",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "河南省驻马店市汝南县",
    },
]

# ├─ Positions ──────────────────────────────────────────────────────────────

positions = [
    # ---- 刘光辉 ----
    {
        "person_id": 1,
        "org_id": 2,
        "title": "县长",
        "start": "待查",
        "end": "present",
        "rank": "正处级",
        "note": "also serves as 县委副书记、县政府党组书记. Confirmed as of 2026-07-24."
    },
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委副书记",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "Deputy secretary of 中共汝南县委."
    },
    # ---- 孙伟 ----
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县政府领导",
        "start": "待查",
        "end": "present",
        "rank": "待查",
        "note": "Listed on government leadership page."
    },
    # ---- 王文斌 ----
    {
        "person_id": 3,
        "org_id": 2,
        "title": "县政府领导",
        "start": "待查",
        "end": "present",
        "rank": "待查",
        "note": "Listed on government leadership page."
    },
    # ---- 廖向东 ----
    {
        "person_id": 4,
        "org_id": 2,
        "title": "县政府领导",
        "start": "待查",
        "end": "present",
        "rank": "待查",
        "note": "Listed on government leadership page."
    },
    # ---- 郭海亮 ----
    {
        "person_id": 5,
        "org_id": 2,
        "title": "县政府领导",
        "start": "待查",
        "end": "present",
        "rank": "待查",
        "note": "Listed on government leadership page."
    },
    # ---- 陈鹏 ----
    {
        "person_id": 6,
        "org_id": 2,
        "title": "县政府领导",
        "start": "待查",
        "end": "present",
        "rank": "待查",
        "note": "Listed on government leadership page."
    },
    # ---- 姚树祎 ----
    {
        "person_id": 7,
        "org_id": 2,
        "title": "县政府领导",
        "start": "待查",
        "end": "present",
        "rank": "待查",
        "note": "Listed on government leadership page."
    },
]

# ├─ Relationships ─────────────────────────────────────────────────────────

relationships = [
    {
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "overlap",
        "context": "Current colleagues in 汝南县人民政府 leadership team",
        "overlap_org": "汝南县人民政府",
        "overlap_period": "截至2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "overlap",
        "context": "Current colleagues in 汝南县人民政府 leadership team",
        "overlap_org": "汝南县人民政府",
        "overlap_period": "截至2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "overlap",
        "context": "Current colleagues in 汝南县人民政府 leadership team",
        "overlap_org": "汝南县人民政府",
        "overlap_period": "截至2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a_id": 1,
        "person_b_id": 5,
        "type": "overlap",
        "context": "Current colleagues in 汝南县人民政府 leadership team",
        "overlap_org": "汝南县人民政府",
        "overlap_period": "截至2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a_id": 1,
        "person_b_id": 6,
        "type": "overlap",
        "context": "Current colleagues in 汝南县人民政府 leadership team",
        "overlap_org": "汝南县人民政府",
        "overlap_period": "截至2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a_id": 1,
        "person_b_id": 7,
        "type": "overlap",
        "context": "Current colleagues in 汝南县人民政府 leadership team",
        "overlap_org": "汝南县人民政府",
        "overlap_period": "截至2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Database & Graph Build
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    import sqlite3
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
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
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
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
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )
    for o in organizations:
        c.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    for pos in positions:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
        )
    for r in relationships:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a_id"], r["person_b_id"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"✅ Database written: {DB_PATH}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent (iagent/standard)</creator>')
    lines.append(f'    <description>汝南县领导工作关系网络 — 截至{AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="level" type="string"/>')
    lines.append('      <attribute id="2" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        if p["current_post"] in ("县委书记", "县长"):
            c = "255,50,50" if "书记" in p["current_post"] else "50,100,255"
            sz = "20.0"
        else:
            c = "100,100,100"
            sz = "12.0"
        node_id = f"p{p['id']}"
        lines.append(f'      <node id="{node_id}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="河南省驻马店市汝南县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in organizations:
        node_id = f"o{o['id']}"
        c = color_map.get(o["type"], "200,200,200")
        lines.append(f'      <node id="{node_id}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"] or "未知")}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"] or "未知")}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a_id']}"
        tgt = f"p{r['person_b_id']}"
        w = "2.0"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="present"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("confidence", "unverified"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF written: {GEXF_PATH}")


def print_summary():
    print(f"\n{'='*60}")
    print(f"  汝南县 领导班子关系网络 — 构建完成")
    print(f"{'='*60}")
    print(f"  人员: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
    print(f"  信息来源: {len(sources)} 条")
    print(f"{'='*60}")
    print(f"  ⚠ 县委书记身份未获取 — 县委领导页面不可访问")
    print(f"  ⚠ 所有核心人物详细履历缺失 — 需后续深度调研")
    print(f"  ⚠ Exa API 限流, 百度/Google 被屏蔽 — 降级网络访问模式")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
