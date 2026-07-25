#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 镇赉县, 白城市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_镇赉县
Research sources:
  - All government websites (jlbc.gov.cn, jlbc.gov.cn/site/zkxzf/) — timed out
  - Baidu Baike — HTTP 403
  - Exa search API — rate limited
  - Jina Reader / Google / Bing — timed out or blocked

⚠️  FULLY DEGRADED WEB ACCESS — all names are placeholders.
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "镇赉县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Committee
    # ══════════════════════════════════════════════════════════════════════════

    # 待查 — 县委书记
    {"id": 1, "name": "待查_县委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共镇赉县委员会",
     "source": "所有官方来源不可达：jlbc.gov.cn超时，百度百科403，Exa限流",
     "notes": "姓名完全未知。需通过白城市委组织部任前公示或新闻报道确认。"},

    # 待查 — 县长
    {"id": 2, "name": "待查_县长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "镇赉县人民政府",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。需通过政府网站或新闻报道确认。"},

    # ══════════════════════════════════════════════════════════════════════════
    # County Government — Deputy Leaders (standard county-level cadre positions)
    # ══════════════════════════════════════════════════════════════════════════

    # 待查 — 常务副县长
    {"id": 3, "name": "待查_常务副县长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长（常务）", "current_org": "镇赉县人民政府",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。县级标配职务。"},

    # 待查 — 纪委书记
    {"id": 4, "name": "待查_纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县纪委书记、县监委主任", "current_org": "中共镇赉县纪律检查委员会",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。"},

    # 待查 — 组织部部长
    {"id": 5, "name": "待查_组织部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共镇赉县委组织部",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。"},

    # 待查 — 宣传部部长
    {"id": 6, "name": "待查_宣传部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共镇赉县委宣传部",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。"},

    # 待查 — 政法委书记
    {"id": 7, "name": "待查_政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共镇赉县委政法委员会",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。"},

    # 待查 — 副县长、公安局局长
    {"id": 8, "name": "待查_副县长公安局长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "镇赉县人民政府",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。兼任县公安局长。"},

    # ══════════════════════════════════════════════════════════════════════════
    # Other Key Leaders (standard county institutional positions)
    # ══════════════════════════════════════════════════════════════════════════

    # 待查 — 县人大常委会主任
    {"id": 9, "name": "待查_人大主任", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "镇赉县人大常委会",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。"},

    # 待查 — 县政协主席
    {"id": 10, "name": "待查_政协主席", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协镇赉县委员会",
     "source": "所有官方来源不可达",
     "notes": "姓名完全未知。"},

    # ══════════════════════════════════════════════════════════════════════════
    # Predecessors — unknown
    # ══════════════════════════════════════════════════════════════════════════

    # 待查 — 前任县委书记
    {"id": 11, "name": "待查_前任县委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任县委书记", "current_org": "中共镇赉县委员会",
     "source": "所有官方来源不可达",
     "notes": "前任县委书记，姓名和去向未知。"},

    # 待查 — 前任县长
    {"id": 12, "name": "待查_前任县长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任县长", "current_org": "镇赉县人民政府",
     "source": "所有官方来源不可达",
     "notes": "前任县长，姓名和去向未知。"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共镇赉县委员会", "type": "党委", "level": "县处级", "parent": "中共白城市委", "location": "镇赉县"},
    {"id": 2, "name": "镇赉县人民政府", "type": "政府", "level": "县处级", "parent": "白城市人民政府", "location": "镇赉县"},
    {"id": 3, "name": "镇赉县人大常委会", "type": "人大", "level": "县处级", "parent": "白城市人大常委会", "location": "镇赉县"},
    {"id": 4, "name": "政协镇赉县委员会", "type": "政协", "level": "县处级", "parent": "政协白城市委", "location": "镇赉县"},
    {"id": 5, "name": "中共镇赉县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共白城市纪委", "location": "镇赉县"},
    {"id": 6, "name": "中共镇赉县委组织部", "type": "党委", "level": "县处级", "parent": "中共镇赉县委", "location": "镇赉县"},
    {"id": 7, "name": "中共镇赉县委宣传部", "type": "党委", "level": "县处级", "parent": "中共镇赉县委", "location": "镇赉县"},
    {"id": 8, "name": "中共镇赉县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共镇赉县委", "location": "镇赉县"},
    {"id": 9, "name": "镇赉县公安局", "type": "政府", "level": "正科级", "parent": "镇赉县人民政府", "location": "镇赉县"},
    {"id": 10, "name": "中共白城市委", "type": "党委", "level": "地厅级", "parent": "中共吉林省委", "location": "白城市"},
    {"id": 11, "name": "白城市人民政府", "type": "政府", "level": "地厅级", "parent": "吉林省人民政府", "location": "白城市"},
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # 县委书记
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "", "end": "present",
     "rank": "县处级正职", "note": "姓名待查"},

    # 县长
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "", "end": "present",
     "rank": "县处级正职", "note": "姓名待查"},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 常务副县长
    {"person_id": "p3", "org_id": 2, "title": "县委常委、副县长（常务）", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": "p3", "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 纪委书记
    {"person_id": "p4", "org_id": 5, "title": "县纪委书记、县监委主任", "start": "", "end": "present",
     "rank": "县处级副职", "note": "同时任县委常委"},
    {"person_id": "p4", "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 组织部部长
    {"person_id": "p5", "org_id": 6, "title": "组织部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "同时任县委常委"},
    {"person_id": "p5", "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 宣传部部长
    {"person_id": "p6", "org_id": 7, "title": "宣传部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "同时任县委常委"},
    {"person_id": "p6", "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 政法委书记
    {"person_id": "p7", "org_id": 8, "title": "政法委书记", "start": "", "end": "present",
     "rank": "县处级副职", "note": "同时任县委常委"},
    {"person_id": "p7", "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 副县长、公安局长
    {"person_id": "p8", "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": "p8", "org_id": 9, "title": "县公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": ""},

    # 县人大常委会主任
    {"person_id": "p9", "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},

    # 县政协主席
    {"person_id": "p10", "org_id": 4, "title": "县政协主席", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},

    # 前任县委书记
    {"person_id": "p11", "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "",
     "rank": "县处级正职", "note": "姓名和去向未知"},

    # 前任县长
    {"person_id": "p12", "org_id": 2, "title": "县长（前任）", "start": "", "end": "",
     "rank": "县处级正职", "note": "姓名和去向未知"},
    {"person_id": "p12", "org_id": 1, "title": "县委副书记（前任）", "start": "", "end": "",
     "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # ===== Top Leader + Mayor =====
    {"person_a": "p1", "person_b": "p2", "type": "党政正职搭档",
     "context": "待查（县委书记）与待查（县长）为党政正职搭档",
     "overlap_org": "中共镇赉县委员会/镇赉县人民政府", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 书记 + 常务副县长 =====
    {"person_a": "p1", "person_b": "p3", "type": "党政协同",
     "context": "待查（县委书记）与待查（常务副县长）在常委会共事",
     "overlap_org": "中共镇赉县委常委会", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 县长 + 常务副县长 =====
    {"person_a": "p2", "person_b": "p3", "type": "政府正副职搭档",
     "context": "待查（县长）与待查（常务副县长）为政府正副职搭档",
     "overlap_org": "镇赉县人民政府", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 书记 + 前任书记 =====
    {"person_a": "p1", "person_b": "p11", "type": "前后任",
     "context": "待查接替前任县委书记",
     "overlap_org": "中共镇赉县委员会", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 县长 + 前任县长 =====
    {"person_a": "p2", "person_b": "p12", "type": "前后任",
     "context": "待查接替前任县长",
     "overlap_org": "镇赉县人民政府", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 书记 + 纪委书记 =====
    {"person_a": "p1", "person_b": "p4", "type": "党委班子成员",
     "context": "在县委常委会共事",
     "overlap_org": "中共镇赉县委常委会", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 书记 + 组织部长 =====
    {"person_a": "p1", "person_b": "p5", "type": "党委班子成员",
     "context": "在县委常委会共事",
     "overlap_org": "中共镇赉县委常委会", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 书记 + 宣传部长 =====
    {"person_a": "p1", "person_b": "p6", "type": "党委班子成员",
     "context": "在县委常委会共事",
     "overlap_org": "中共镇赉县委常委会", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 书记 + 政法委书记 =====
    {"person_a": "p1", "person_b": "p7", "type": "党委班子成员",
     "context": "在县委常委会共事",
     "overlap_org": "中共镇赉县委常委会", "overlap_period": "",
     "confidence": "unverified"},

    # ===== 县长 + 公安局长 =====
    {"person_a": "p2", "person_b": "p8", "type": "上下级",
     "context": "县长与副县长、公安局长为政府内部上下级关系",
     "overlap_org": "镇赉县人民政府", "overlap_period": "",
     "confidence": "unverified"},
]

# ── Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Normalize person ids: strip "p" prefix for DB
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid("p" + str(p["id"])), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post:
            return ("100,150,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>镇赉县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"镇赉县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
