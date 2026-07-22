#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
永福县领导班子工作关系网络 — 数据构建脚本 (staging)
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 永福县
Targets: 县委书记 & 县长

Research Date: 2026-07-22
Web Access: Degraded (Government site http://www.glyf.gov.cn/ unreachable,
             Baidu/Google/Jina Reader all timed out, Exa rate-limited)
Sources: Repository artifacts, cross-references from 象山区/桂林市 investigations

Status: Partial evidence — core leader names unconfirmed from online sources.
        Names below are placeholders pending web access restoration.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

SLUG = "永福县"
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

# Region: 永福县, 桂林市, 广西壮族自治区
# Confirmed organizations and known cross-county connections.
# Core leaders (县委书记, 县长) need web access to confirm names.

persons = [
    # --- Core Leaders (NAMES UNCONFIRMED - placeholders) ---
    {
        "id": 1,
        "name": "待确认—永福县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永福县委书记",
        "current_org": "中国共产党永福县委员会",
        "source": "需访问 glyf.gov.cn 或桂林市委组织部任前公示确认",
    },
    {
        "id": 2,
        "name": "待确认—永福县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永福县长",
        "current_org": "永福县人民政府",
        "source": "需访问 glyf.gov.cn 或桂林市委组织部任前公示确认",
    },
    # --- Cross-County Connection: 蒋玲荣 (confirmed 永福县委 connection) ---
    {
        "id": 3,
        "name": "蒋玲荣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "广西全州",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "象山区委书记（原永福县委常委、组织部部长）",
        "current_org": "中国共产党桂林市象山区委员会",
        "source": "象山区政府官网/百度百科 (from 象山区 investigation)",
    },
    # --- Potential predecessor clues ---
    # 廖照德 (previous 永福县委书记 from ~2016-2021, later 桂林市副市长)
    # 莫振华 (previous 永福县委书记 from ~2011-2016, later 雁山区委书记, 象山区委书记, 桂林市政协副主席)
    # Names above are unconfirmed — need verification
]

organizations = [
    {"id": 0, "name": "中国共产党永福县委员会", "type": "党委",
     "level": "县处级", "parent": "桂林市委", "location": "桂林市永福县"},
    {"id": 1, "name": "永福县人民政府", "type": "政府",
     "level": "县处级", "parent": "桂林市人民政府", "location": "桂林市永福县"},
    {"id": 2, "name": "永福县人大常委会", "type": "人大",
     "level": "县处级", "parent": "", "location": "桂林市永福县"},
    {"id": 3, "name": "永福县政协", "type": "政协",
     "level": "县处级", "parent": "", "location": "桂林市永福县"},
    {"id": 4, "name": "永福县纪委监委", "type": "党委",
     "level": "县处级", "parent": "永福县委", "location": "桂林市永福县"},
    {"id": 5, "name": "中国共产党桂林市象山区委员会", "type": "党委",
     "level": "县处级", "parent": "桂林市委", "location": "桂林市象山区"},
]

positions = [
    # 永福县委书记
    {"person_id": 1, "org_id": 0, "title": "县委书记",
     "start_date": "待查", "end_date": "present",
     "rank": "正处级", "note": "当前永福县委书记，信息待确认"},
    # 永福县长
    {"person_id": 2, "org_id": 1, "title": "县长",
     "start_date": "待查", "end_date": "present",
     "rank": "正处级", "note": "当前永福县长，信息待确认"},
    # 蒋玲荣 - 曾任永福县委常委、组织部部长
    {"person_id": 3, "org_id": 5, "title": "区委书记",
     "start_date": "2026", "end_date": "present",
     "rank": "正处级", "note": "2026年升任象山区委书记"},
    {"person_id": 3, "org_id": 5, "title": "区长",
     "start_date": "2025-05", "end_date": "2026",
     "rank": "正处级", "note": "2025年4月任代区长，5月当选区长"},
    {"person_id": 3, "org_id": 5, "title": "区委副书记",
     "start_date": "~2024", "end_date": "2026",
     "rank": "副处级", "note": "象山区委副书记"},
    {"person_id": 3, "org_id": 0, "title": "县委常委、组织部部长",
     "start_date": "未知", "end_date": "~2024",
     "rank": "副处级", "note": "此前曾任永福县委常委、组织部部长"},
]

relationships = [
    # 蒋玲荣与永福县的工作关系
    {"person_a": 3, "person_b": 1, "type": "organizational_overlap",
     "context": "蒋玲荣曾任永福县委常委、组织部部长，与永福县委书记为县委常委班子成员",
     "overlap_org": "中国共产党永福县委员会", "overlap_period": "~2024前"},
    {"person_a": 3, "person_b": 2, "type": "organizational_overlap",
     "context": "蒋玲荣曾任永福县委常委、组织部部长，与永福县长为领导班子成员",
     "overlap_org": "中国共产党永福县委员会", "overlap_period": "~2024前"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# SQLITE
# ═══════════════════════════════════════════════════════════════════════════════

def build_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '', current_org TEXT DEFAULT '',
            source TEXT DEFAULT '');
        CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            type TEXT DEFAULT '', level TEXT DEFAULT '', parent TEXT DEFAULT '',
            location TEXT DEFAULT '');
        CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id));
        CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id));
    """)

    pcols = ["id","name","gender","ethnicity","birth","birthplace",
             "education","party_join","work_start","current_post","current_org","source"]
    for p in persons:
        conn.execute(f"INSERT INTO persons ({','.join(pcols)}) VALUES ({','.join(['?']*len(pcols))})",
                     [p.get(c,"") for c in pcols])

    ocols = ["id","name","type","level","parent","location"]
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join(['?']*len(ocols))})",
                     [o.get(c,"") for c in ocols])

    pscols = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(pscols)}) VALUES ({','.join(['?']*len(pscols))})",
                     [pos.get(c,"") for c in pscols])

    rcols = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join(['?']*len(rcols))})",
                     [r.get(c,"") for c in rcols])

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(post):
    if "书记" in post and "副" not in post: return "255,50,50"
    if "县长" in post or ("长" in post and "副" not in post): return "50,100,255"
    if "纪委" in post: return "255,165,0"
    return "100,100,100"

def person_sz(post):
    if ("书记" in post and "副" not in post) or ("长" in post and "副" not in post):
        return "20.0"
    return "12.0"

def org_color(t):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
            "政协":"255,240,200"}.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Investigator</creator>')
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络（调查中：网络搜索不可用，核心领导姓名待确认）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    for aid,aname,atype in [("0","type","string"),("1","current_post","string"),
                            ("2","current_org","string"),("3","birth","string"),
                            ("4","birthplace","string"),("5","source","string")]:
        lines.append(f'      <attribute id="{aid}" title="{aname}" type="{atype}"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for eid,ename,etype in [("0","type","string"),("1","context","string"),
                            ("2","overlap_org","string"),("3","overlap_period","string")]:
        lines.append(f'      <attribute id="{eid}" title="{ename}" type="{etype}"/>')
    lines.append('    </attributes>')

    # nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = person_sz(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"][:80])}"/>')
        if p["birth"]: lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        if p["birthplace"]: lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["source"][:80])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        if o["parent"]: lines.append(f'          <attvalue for="3" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        if pos.get("start_date"): lines.append(f'          <attvalue for="2" value="{esc(pos["start_date"])}"/>')
        if pos.get("end_date"): lines.append(f'          <attvalue for="3" value="{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r["type"] in ("predecessor_successor","superior_subordinate") else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        if r["overlap_org"]: lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        if r["overlap_period"]: lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    GEXF_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    build_db()
    build_gexf()
    print(f"Summary: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print("Build complete!")
    print()
    print("⚠️  Web access was severely degraded during this build.")
    print("   永福县核心领导（县委书记、县长）姓名未能在本次调查中确认。")
    print("   建议在以下来源恢复访问后更新：")
    print("   - https://www.glyf.gov.cn/zwgk/ldzc/ (永福县政府领导之窗)")
    print("   - 桂林市委组织部任前公示")
    print("   - 百度百科")

if __name__ == "__main__":
    main()
