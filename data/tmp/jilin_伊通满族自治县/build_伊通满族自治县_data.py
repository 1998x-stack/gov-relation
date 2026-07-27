#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 伊通满族自治县, 四平市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_伊通满族自治县
Research sources:
  - Baidu search results (2026-07-25) — county leadership in news reports
  - 百度百科 — county overview
  - Sogou search — personnel info

Evidence confidence:
  - Current 县委书记: UNCLEAR — 孙立阳 was 县委书记 as of most reports,
    but some evidence suggests he may have moved to 四平市政协.
    The current secretary needs confirmation from official sources.
  - Current 县长: 付巍 — confirmed acting appointment Oct 2024,
    formally elected at 人代会.
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "伊通满族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING) / "persons"
PERSONS_DIR.mkdir(parents=True, exist_ok=True)


# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ═══════════════════════════════════════════════════════════════════════════

    # 孙立阳 — 县委书记 (possibly former — gap: need current status as of 2026)
    # Source: Baidu search — appeared in news alongside 付巍 as 县委书记
    # Some evidence suggests moved to 四平市政协党组成员、秘书长
    {"id": 1, "name": "孙立阳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记（待确认）", "current_org": "中共伊通满族自治县委员会",
     "source": "百度搜索结果 — 2024-2025年伊通新闻活动"},

    # 付巍 — 县委副书记、县长 (confirmed)
    # Source: 2024年10月任副县长、代县长；2025年1月以县长身份出席活动
    {"id": 2, "name": "付巍", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "伊通满族自治县人民政府",
     "source": "2024年10月被任命为代县长，2025年1月正式当选县长"},

    # 张亚冰 — 县政协主席
    {"id": 3, "name": "张亚冰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协伊通满族自治县委员会",
     "source": "伊通新闻活动报道"},

    # 赵春飞 — 县人大常委会主任
    {"id": 4, "name": "赵春飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "伊通满族自治县人大常委会",
     "source": "伊通满族自治县第八届人民代表大会公告"},

    # 孙宇 — 县监察委员会主任
    {"id": 5, "name": "孙宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县监察委员会主任", "current_org": "伊通满族自治县监察委员会",
     "source": "伊通满族自治县第八届人民代表大会公告"},

    # ═══════════════════════════════════════════════════════════════════════════
    # Party Committee Standing Members (县委常委)
    # ═══════════════════════════════════════════════════════════════════════════

    # 孙大太 — 县委常委、宣传部部长
    {"id": 6, "name": "孙大太", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共伊通满族自治县委员会宣传部",
     "source": "伊通新闻活动报道"},

    # ═══════════════════════════════════════════════════════════════════════════
    # County Government — Deputy Leaders
    # ═══════════════════════════════════════════════════════════════════════════

    # 李宇嘉 — 县政府副县长
    {"id": 7, "name": "李宇嘉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "伊通满族自治县人民政府",
     "source": "伊通新闻活动报道"},

    # ═══════════════════════════════════════════════════════════════════════════
    # Former Leaders (Predecessors)
    # ═══════════════════════════════════════════════════════════════════════════

    # 张恒 — 前县委书记 (moved to 四平市副市长)
    {"id": 8, "name": "张恒", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "四平市副市长（原伊通县委书记）", "current_org": "四平市人民政府",
     "source": "百度百科/媒体报道 — 2021年7月任四平市副市长"},

    # 叶永兴 — 前县长
    {"id": 9, "name": "叶永兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原伊通县长（已离任）", "current_org": "",
     "source": "2021年、2023年9月报道显示为伊通县长"},

    # 杨洪波 — 前县委书记 (2015年)
    {"id": 10, "name": "杨洪波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原伊通县委书记（2015年任职）", "current_org": "",
     "source": "报道显示2015年7月担任伊通县委书记"},

    # 杨枫 — 前县委书记 (更早，全国人大代表)
    {"id": 11, "name": "杨枫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原伊通县委书记（全国人大代表）", "current_org": "",
     "source": "全国人大代表报道 — '访全国人大代表、吉林伊通满族自治县县委书记杨枫'"},
]


# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共伊通满族自治县委员会", "type": "党委", "level": "县级", "parent": "中共四平市委", "location": "伊通满族自治县"},
    {"id": 2, "name": "伊通满族自治县人民政府", "type": "政府", "level": "县级", "parent": "四平市人民政府", "location": "伊通满族自治县"},
    {"id": 3, "name": "中共伊通满族自治县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共伊通满族自治县委员会", "location": "伊通满族自治县"},
    {"id": 4, "name": "伊通满族自治县监察委员会", "type": "监察", "level": "县级", "parent": "", "location": "伊通满族自治县"},
    {"id": 5, "name": "伊通满族自治县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "伊通满族自治县"},
    {"id": 6, "name": "政协伊通满族自治县委员会", "type": "政协", "level": "县级", "parent": "", "location": "伊通满族自治县"},
    {"id": 7, "name": "中共伊通满族自治县委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中共伊通满族自治县委员会", "location": "伊通满族自治县"},
    {"id": 8, "name": "四平市人民政府", "type": "政府", "level": "地市级", "parent": "吉林省人民政府", "location": "四平市"},
    {"id": 9, "name": "中共四平市委", "type": "党委", "level": "地市级", "parent": "中共吉林省委", "location": "四平市"},
]


# ── Positions (person_id, org_id, title, start_date, end_date, rank, note) ───

positions = [
    # 孙立阳 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "约2020-2021", "end_date": "未知", "rank": "正处级", "note": "任职时间需确认；部分信息显示已调任四平市政协"},

    # 付巍 — 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "2024-10", "end_date": "至今", "rank": "正处级", "note": "2024年10月任代县长，后正式当选"},

    # 张亚冰 — 政协主席
    {"person_id": 3, "org_id": 6, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # 赵春飞 — 人大主任
    {"person_id": 4, "org_id": 5, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "第八届人大常委会主任"},

    # 孙宇 — 监委主任
    {"person_id": 5, "org_id": 4, "title": "县监察委员会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "补选为监察委员会主任"},

    # 孙大太 — 宣传部长
    {"person_id": 6, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 李宇嘉 — 副县长
    {"person_id": 7, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 张恒 — 前县委书记
    {"person_id": 8, "org_id": 1, "title": "县委书记（前）", "start_date": "约2018-2019", "end_date": "2021-07", "rank": "正处级", "note": "后任四平市副市长"},
    {"person_id": 8, "org_id": 8, "title": "四平市副市长", "start_date": "2021-07", "end_date": "至今", "rank": "副厅级", "note": "从伊通县委书记升任"},

    # 叶永兴 — 前县长
    {"person_id": 9, "org_id": 2, "title": "县委副书记、县长（前）", "start_date": "约2021", "end_date": "约2024", "rank": "正处级", "note": "2021年、2023年9月报道中为县长"},

    # 杨洪波 — 前县委书记 (2015)
    {"person_id": 10, "org_id": 1, "title": "县委书记（前）", "start_date": "2015-07", "end_date": "约2018", "rank": "正处级", "note": "2015年7月任伊通县委书记"},

    # 杨枫 — 前县委书记 (更早)
    {"person_id": 11, "org_id": 1, "title": "县委书记（前）", "start_date": "约2012", "end_date": "约2015", "rank": "正处级", "note": "全国人大代表；'要形成劳务业品牌效应'报道"},
]


# ── Relationships (person_a, person_b, type, context, overlap_org, overlap_period) ──

relationships = [
    # 孙立阳 ↔ 付巍 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "孙立阳任县委书记期间，付巍任县长", "overlap_org": "伊通满族自治县", "overlap_period": "2024-至今"},

    # 张恒 ↔ 叶永兴 (前任党政搭档)
    {"person_a": 8, "person_b": 9, "type": "党政搭档", "context": "张恒任县委书记时，叶永兴任县长", "overlap_org": "伊通满族自治县", "overlap_period": "2021-2024"},

    # 张恒 → 孙立阳 (前后任县委书记)
    {"person_a": 8, "person_b": 1, "type": "前后任", "context": "张恒调任四平市副市长后，孙立阳接任县委书记", "overlap_org": "中共伊通满族自治县委员会", "overlap_period": "2021-2022"},

    # 叶永兴 → 付巍 (前后任县长)
    {"person_a": 9, "person_b": 2, "type": "前后任", "context": "叶永兴离任后，付巍接任县长", "overlap_org": "伊通满族自治县人民政府", "overlap_period": "2024"},

    # 杨洪波 → 张恒 (前后任县委书记)
    {"person_a": 10, "person_b": 8, "type": "前后任", "context": "杨洪波之后张恒接任县委书记", "overlap_org": "中共伊通满族自治县委员会", "overlap_period": "约2018-2019"},

    # 杨枫 → 杨洪波 (前后任县委书记)
    {"person_a": 11, "person_b": 10, "type": "前后任", "context": "杨枫之后杨洪波接任县委书记", "overlap_org": "中共伊通满族自治县委员会", "overlap_period": "约2015"},

    # 孙立阳 → 张亚冰 (党政—政协)
    {"person_a": 1, "person_b": 3, "type": "同僚", "context": "孙立阳任县委书记期间，张亚冰任政协主席", "overlap_org": "伊通满族自治县", "overlap_period": "2022-至今"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Database & GEXF Build
# ═══════════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
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
        )
    """)

    # Insert data
    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 education, party_join, work_start,
                                 current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start_date", ""), pos.get("end_date", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Database built: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b string for node color based on role."""
    role = p.get("current_post", "")
    if "书记" in role and "纪委书记" not in role:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in role or "副县长" in role or "区长" in role or "市长" in role:
        return "50,100,255"  # Blue — Government
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange — Discipline
    if "政协" in role:
        return "255,240,200"  # Cream
    if "人大" in role:
        return "200,255,255"  # Cyan
    return "100,100,100"  # Grey — Other


def is_top_leader(p):
    role = p.get("current_post", "")
    return "县委书记" in role or "县长" in role


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — Organizations
    org_color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "监察": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "党委部门": "255,200,200",
    }
    for o in organizations:
        oid = o["id"] + 100  # offset org IDs
        c = org_color_map.get(o.get("type", ""), "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges — person->organization (worked_at) from positions
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"] + 100
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos.get("title",""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="任职"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date",""))}-{esc(pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges — person<->person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type",""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph built: {GEXF_PATH}")


# ── Person JSON Writer ────────────────────────────────────────────────────────

def write_person_json(person, extra_career=None, extra_relationships=None):
    """Write a person JSON file to staging/persons/."""
    today = datetime.now().strftime("%Y%m%d")

    # Build career timeline from positions data
    career = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career.append({
                "start": pos.get("start_date", "") or "unknown",
                "end": pos.get("end_date", "") or "unknown",
                "org": org_name,
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "notes": pos.get("note", ""),
                "confidence": "plausible" if "待确认" in person.get("current_post", "") or "前" in person.get("current_post", "") else "confirmed",
            })
    if extra_career:
        career.extend(extra_career)

    # Build relationships for this person
    rels = []
    for r in relationships:
        if r["person_a"] == person["id"] or r["person_b"] == person["id"]:
            other_id = r["person_b"] if r["person_a"] == person["id"] else r["person_a"]
            other_name = ""
            for p in persons:
                if p["id"] == other_id:
                    other_name = p["name"]
                    break
            rels.append({
                "person": other_name,
                "person_id": f"yitong_{other_name}",
                "relationship_type": r.get("type", ""),
                "strength": "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "confidence": "plausible",
            })
    if extra_relationships:
        rels.extend(extra_relationships)

    job_slug = person.get("current_post", "unknown").replace("/", "、").replace("（", "(").replace("）", ")")[:30]
    fname = f"{today}-吉林省-四平市-{job_slug}-{person['name']}.json"
    fpath = PERSONS_DIR / fname

    person_data = {
        "schema_version": "1.0",
        "generated_at": today,
        "investigation_scope": {
            "province": "吉林省",
            "city": "四平市",
            "region": "伊通满族自治县",
            "job": job_slug,
            "task_id": "jilin_伊通满族自治县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"yitong_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if any(k in person.get("current_post", "") for k in ["书记", "县长", "主任", "主席"]) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": "待确认" not in person.get("current_post", ""),
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [{"org_id": o["id"], "org_name": o["name"], "org_type": o.get("type", "")} for o in organizations if any(pos["person_id"] == person["id"] and pos["org_id"] == o["id"] for pos in positions)],
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
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "百度搜索 — 伊通满族自治县领导活动报道",
                "url": "https://www.baidu.com/s?wd=伊通满族自治县+县委书记+2024+现任",
                "publisher": "百度",
                "published_at": "2026-07-25",
                "accessed_at": "2026-07-25",
                "source_type": "database",
                "reliability": "medium",
                "notes": "从百度搜索结果中提取的领导活动信息"
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "缺少完整履历信息；部分领导出生年份、教育背景等基本信息缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年份、教育背景、任职时间线）",
                "why_it_matters": "核心人物基本信息确认",
                "suggested_queries": [f"{person['name']} 简历 吉林", f"{person['name']} 百度百科"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": f"{person['name']}的现任职务和任职时间",
                "why_it_matters": "确认当前职务的准确性",
                "suggested_queries": [f"{person['name']} 现任", f"{person['name']} 任职"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {fpath}")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(STAGING, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)
    build_db()
    build_gexf()
    # Write person JSON for core figures
    for p in persons:
        if p["id"] in [1, 2]:  # 县委书记 and 县长
            write_person_json(p)
    print(f"\nAll artifacts built in {STAGING}")
    print("Files:")
    for f in os.listdir(STAGING):
        fpath = os.path.join(STAGING, f)
        if os.path.isfile(fpath):
            print(f"  {f} ({os.path.getsize(fpath)} bytes)")
        elif os.path.isdir(fpath):
            for sf in os.listdir(fpath):
                sfpath = os.path.join(fpath, sf)
                print(f"  {f}/{sf} ({os.path.getsize(sfpath)} bytes)")


if __name__ == "__main__":
    main()
