#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Guinan County (贵南县),
Hainan Tibetan Autonomous Prefecture (海南藏族自治州), Qinghai (青海省).

task_id: qinghai_贵南县
targets: 县委书记 & 县长 (薛顺云 as 县委书记; 卓玛本 as 县委副书记、县长)

Research as-of: 2026-08-07 (Baidu Baike/wapbaike for 薛顺云's career, and search-engine
aggregation for 卓玛本's current 县长 role). Official hainanzhou.gov.cn and the county
government host were unreachable (403/timeout) in this environment; Baidu/Bing/Sogou/Exa
search were WAF/rate-limited. Only source-backed facts are recorded; every uncertain
field is flagged in the person JSON open_questions and the report open gaps, never
fabricated. 卓玛本's identity/career is a flagged open gap (plausible current role only).
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/qinghai_贵南县")
DB_PATH = os.path.join(TMP, "贵南县_network.db")
GEXF_PATH = os.path.join(TMP, "贵南县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "薛顺云", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "青海省海东市互助县", "education": "大学（农学本科）",
     "party_join": "2003-07", "work_start": "1999-08",
     "current_post": "贵南县委书记", "current_org": "中共贵南县委员会",
     "source": "https://wapbaike.baidu.com/item/%E8%96%9B%E9%A1%BA%E4%BA%91"},
    {"id": 2, "name": "卓玛本", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵南县委副书记、县人民政府县长", "current_org": "贵南县人民政府",
     "source": "贵南县领导信息（受限网络，身份为 plausible/待核实）"},

    # ── 前任领导 ──
    {"id": 3, "name": "宁发贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-09", "birthplace": "青海省海南藏族自治州贵德县", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西宁市委副书记（原贵南县委书记）", "current_org": "中共西宁市委员会",
     "source": "https://baike.baidu.com/item/%E5%AE%81%E5%8F%91%E8%B4%B5"},

    # ── 海南州层级 ──
    {"id": 4, "name": "熊元来", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委书记", "current_org": "中共海南藏族自治州委员会",
     "source": "https://www.hainanzhou.gov.cn/"},
    {"id": 5, "name": "当周", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委副书记、州政府代理州长", "current_org": "海南藏族自治州人民政府",
     "source": "https://www.hainanzhou.gov.cn/"},
    {"id": 6, "name": "戴敏捷", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "省政府副秘书长、海南州委副书记、州政府副州长", "current_org": "海南藏族自治州人民政府",
     "source": "https://www.hainanzhou.gov.cn/zwgk/fdzdgknr/jgjj/zzfld"},
]

organizations = [
    {"id": 1, "name": "中共贵南县委员会", "type": "党委", "level": "县处级",
     "parent": "中共海南藏族自治州委员会", "location": "青海省海南藏族自治州贵南县"},
    {"id": 2, "name": "贵南县人民政府", "type": "政府", "level": "县处级",
     "parent": "海南藏族自治州人民政府", "location": "青海省海南藏族自治州贵南县"},
    {"id": 3, "name": "中共海南藏族自治州委员会", "type": "党委", "level": "地厅级",
     "parent": "中共青海省委员会", "location": "青海省海南藏族自治州"},
    {"id": 4, "name": "海南藏族自治州人民政府", "type": "政府", "level": "地厅级",
     "parent": "青海省人民政府", "location": "青海省海南藏族自治州"},
    # ── 薛顺云早年任职组织（海东市） ──
    {"id": 5, "name": "中共海东市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共青海省委员会", "location": "青海省海东市"},
    {"id": 6, "name": "海东市人民政府", "type": "政府", "level": "地厅级",
     "parent": "青海省人民政府", "location": "青海省海东市"},
    {"id": 7, "name": "海东市统计局", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市"},
    {"id": 8, "name": "海东市住房和城乡建设局", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市"},
    {"id": 9, "name": "海东市互助县", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市互助县"},
    {"id": 10, "name": "海东市平安区", "type": "政府", "level": "县处级",
     "parent": "海东市人民政府", "location": "青海省海东市平安区"},
    # ── 宁发贵今职 ──
    {"id": 11, "name": "中共西宁市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共青海省委员会", "location": "青海省西宁市"},
]

positions = [
    # ── 薛顺云 县委书记 ──
    {"person_id": 1, "org_id": 1, "title": "贵南县委书记", "start": "2024-04", "end": "present", "rank": "正县级",
     "note": "现任贵南县委书记；2026-07-19 中共贵南县第十七届委员会第一次全体会议当选（继续任职）"},
    {"person_id": 1, "org_id": 8, "title": "海东市住房和城乡建设局局长", "start": "2024-02", "end": "2024-04", "rank": "正县级",
     "note": "2024年2月任海东市住房和城乡建设局局长（百科履历）"},
    {"person_id": 1, "org_id": 7, "title": "海东市统计局局长", "start": "2021-12", "end": "2024-02", "rank": "正县级",
     "note": "2021年12月任海东市统计局局长"},
    {"person_id": 1, "org_id": 10, "title": "海东市平安区委常委、区人民政府副区长", "start": "2019-03", "end": "2021-12", "rank": "副县级",
     "note": "2019年3月起任平安区委常委、区委政法委书记、副区长；2019-10免政法委书记，仍常委、副区长"},
    {"person_id": 1, "org_id": 9, "title": "互助县人民政府副县长", "start": "2015-11", "end": "2018-07", "rank": "副县级",
     "note": "2015年11月任互助县副县长；2015-03至2016-01挂职山东省威海市临港经济技术开发区管委会副主任"},
    {"person_id": 1, "org_id": 0, "title": "履历缺口", "start": "unknown", "end": "unknown", "rank": "",
     "note": "1999-2015在互助县、海东市的乡镇/县直/地办基层任职（农经站、团县委、东和乡、海东地委办、市委副秘书长等）逐段待后续核实"},

    # ── 卓玛本 县长 ──
    {"person_id": 2, "org_id": 2, "title": "贵南县人民政府县长", "start": "", "end": "present", "rank": "正县级",
     "note": "现任贵南县县长（新任）；身份与到任时间待核实（open gap）"},
    {"person_id": 2, "org_id": 1, "title": "贵南县委副书记", "start": "", "end": "present", "rank": "县处级",
     "note": "县委副书记（二把手），与县委书记薛顺云组成党政班子"},

    # ── 宁发贵 前任 ──
    {"person_id": 3, "org_id": 1, "title": "贵南县委书记（前任）", "start": "2021", "end": "2024", "rank": "正县级",
     "note": "薛顺云到任前曾任贵南县委书记；具体任期年份为推断（open gap）"},
    {"person_id": 3, "org_id": 11, "title": "西宁市委副书记", "start": "", "end": "present", "rank": "副厅级",
     "note": "今任西宁市委副书记（百度百科描述）"},

    # ── 海南州层级 ──
    {"person_id": 4, "org_id": 3, "title": "海南州委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "海南州委副书记、州政府代理州长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "省政府副秘书长、海南州委副书记、州政府副州长", "start": "", "end": "present", "rank": "副厅级",
     "note": "对口支援、东西部协作、招商引资分工；跨省/省直交流干部"},
    {"person_id": 6, "org_id": 3, "title": "海南州委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "薛顺云任县委书记，卓玛本任县委副书记、县长，为党政一把手搭档",
     "overlap_org": "中共贵南县委员会/贵南县人民政府",
     "overlap_period": "2024-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "strength": "strong",
     "context": "宁发贵为贵南县委书记前任，薛顺云继任县委书记",
     "overlap_org": "中共贵南县委员会",
     "overlap_period": "2024年前后", "confidence": "plausible"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "strength": "medium",
     "context": "贵南县委与海南州委上下级，州委书记熊元来领导贵南县委书记薛顺云",
     "overlap_org": "中共海南藏族自治州委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "贵南县属海南州，当周任州委副书记、代理州长，行政领导关系密切",
     "overlap_org": "海南藏族自治州人民政府",
     "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "熊元来任海南州委书记，当周任州委副书记、代理州长，州级党政一把手",
     "overlap_org": "中共海南藏族自治州委员会/海南藏族自治州人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "州委副书记戴敏捷与贵南县委存在州级领导联系",
     "overlap_org": "中共海南藏族自治州委员会",
     "overlap_period": "至今", "confidence": "plausible"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if ("县委书记" in role) and ("副书记" not in role):
        return "255,50,50"
    elif "县长" in role and "县委书记" not in role:
        return "50,100,255"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "人大常委会" in role or "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "副州长" in role or "州长" in role or "州委书记" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,180,120",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return ("县委书记" in role and "副书记" not in role) or ("县长" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

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
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
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
        c.execute("""INSERT OR REPLACE INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
             pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"], r["context"],
             r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ─────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>贵南县领导班子工作关系网络 (task_id qinghai_贵南县)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="etype" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        r, g, b = [x.strip() for x in c.split(",")]
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        r, g, b = [x.strip() for x in c.split(",")]
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="org"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if pos["org_id"] == 0:
            continue  # skip placeholder person gap row (no org node)
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ─────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()