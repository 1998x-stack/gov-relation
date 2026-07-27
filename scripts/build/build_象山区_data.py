#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
象山区领导班子工作关系网络 — 数据构建脚本 (staging)
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广西壮族自治区
Parent City: 桂林市
Region: 象山区
Targets: 区委书记 & 区长

Research Date: 2026-07-22
Sources: 象山区人民政府官网, 百度百科, 搜狗搜索, 360搜索, 桂林晚报, 澎湃新闻
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

SLUG = "象山区"
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # --- Current Top Leaders ---
    {"id": 1, "name": "蒋玲荣", "gender": "女", "ethnicity": "汉族",
     "birth": "1978-05", "birthplace": "广西全州",
     "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "区委书记",
     "current_org": "中国共产党桂林市象山区委员会",
     "source": "https://baike.baidu.com/item/%E8%92%8B%E7%8E%B2%E8%8D%A3"},
    # --- Predecessors (区委书记) ---
    {"id": 2, "name": "莫振华", "gender": "男", "ethnicity": "壮族",
     "birth": "1970-07", "birthplace": "广西临桂",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桂林市政协副主席（前任区委书记）",
     "current_org": "桂林市政协",
     "source": "360搜索/桂林晚报 2025.04.11"},
    {"id": 3, "name": "唐小忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-11", "birthplace": "广西全州",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原象山区委书记（去向待查）",
     "current_org": "待查",
     "source": "https://baike.baidu.com/item/%E5%94%90%E5%B0%8F%E5%BF%A0"},
    {"id": 4, "name": "蒋伟名", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-09", "birthplace": "广西全州",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桂林市民政局党组书记、局长（曾拟任县区委书记）",
     "current_org": "桂林市民政局",
     "source": "https://baike.baidu.com/item/%E8%92%8B%E4%BC%9F%E5%90%8D"},
    # --- Predecessors (区长) ---
    {"id": 5, "name": "梁红", "gender": "女", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "广西贵港",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任象山区长（去向待查）",
     "current_org": "待查",
     "source": "人民网广西频道/360搜索"},
    {"id": 6, "name": "经友新", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "前任象山区长（去向待查）",
     "current_org": "待查",
     "source": "微信文章搜索"},
]

organizations = [
    {"id": 0, "name": "中国共产党桂林市象山区委员会", "type": "党委",
     "level": "县处级", "parent": "桂林市委", "location": "桂林市象山区"},
    {"id": 1, "name": "象山区人民政府", "type": "政府",
     "level": "县处级", "parent": "桂林市人民政府", "location": "桂林市象山区"},
    {"id": 2, "name": "象山区人大常委会", "type": "人大",
     "level": "县处级", "parent": "", "location": "桂林市象山区"},
    {"id": 3, "name": "象山区政协", "type": "政协",
     "level": "县处级", "parent": "", "location": "桂林市象山区"},
    {"id": 4, "name": "桂林市政协", "type": "政协",
     "level": "地厅级", "parent": "桂林市", "location": "桂林市"},
    {"id": 5, "name": "桂林市民政局", "type": "政府",
     "level": "县处级", "parent": "桂林市人民政府", "location": "桂林市"},
]

positions = [
    # 蒋玲荣
    {"person_id": 1, "org_id": 0, "title": "区委书记",
     "start_date": "2026", "end_date": "present",
     "rank": "正处级", "note": "从区长升任区委书记，2026年任命"},
    {"person_id": 1, "org_id": 1, "title": "区长",
     "start_date": "2025-05", "end_date": "2026",
     "rank": "正处级", "note": "2025年4月任代区长，5月当选区长"},
    {"person_id": 1, "org_id": 0, "title": "区委副书记",
     "start_date": "~2024", "end_date": "2026",
     "rank": "副处级", "note": "此前曾任永福县委常委、组织部部长"},
    # 莫振华
    {"person_id": 2, "org_id": 4, "title": "桂林市政协副主席",
     "start_date": "~2025", "end_date": "present",
     "rank": "副厅级", "note": "2025年4月已以该身份出席活动"},
    {"person_id": 2, "org_id": 0, "title": "区委书记",
     "start_date": "~2020", "end_date": "~2025/2026",
     "rank": "正处级", "note": "从雁山区委书记调任，后兼任市政协副主席"},
    # 唐小忠
    {"person_id": 3, "org_id": 0, "title": "区委书记",
     "start_date": "~2016", "end_date": "~2020",
     "rank": "正处级", "note": "原象山区委书记，从区长升任"},
    {"person_id": 3, "org_id": 1, "title": "区长",
     "start_date": "", "end_date": "~2016",
     "rank": "正处级", "note": "先任区长后升书记"},
    # 蒋伟名
    {"person_id": 4, "org_id": 5, "title": "党组书记、局长",
     "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "桂林市民政局局长"},
    {"person_id": 4, "org_id": 0, "title": "拟任县（区）委书记",
     "start_date": "2020-09", "end_date": "",
     "rank": "正处级", "note": "2020年9月任前公示，具体是否有实际任职待查"},
    # 梁红
    {"person_id": 5, "org_id": 1, "title": "区长",
     "start_date": "~2021-06", "end_date": "~2025-04",
     "rank": "正处级", "note": "2021年6月拟任正处级，2025年4月离任"},
    # 经友新
    {"person_id": 6, "org_id": 1, "title": "区长",
     "start_date": "", "end_date": "~2021",
     "rank": "正处级", "note": "前任区长，在梁红之前任职"},
]

relationships = [
    # 区委书记前任链
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "蒋玲荣接替莫振华担任象山区委书记",
     "overlap_org": "中国共产党桂林市象山区委员会", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "莫振华接替唐小忠担任象山区委书记",
     "overlap_org": "中国共产党桂林市象山区委员会", "overlap_period": "~2020"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "唐小忠之前，蒋伟名曾拟任县委/区委书记",
     "overlap_org": "中国共产党桂林市象山区委员会", "overlap_period": "2020"},
    # 区长前任链
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor",
     "context": "蒋玲荣接替梁红担任象山区长",
     "overlap_org": "象山区人民政府", "overlap_period": "2025-04"},
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor",
     "context": "梁红接替经友新担任象山区长",
     "overlap_org": "象山区人民政府", "overlap_period": "~2021"},
    # 同一职务不同时期
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "蒋玲荣现任区委书记，唐小忠曾任该职",
     "overlap_org": "中国共产党桂林市象山区委员会", "overlap_period": "不同时期"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "莫振华任区委书记时，梁红任区长",
     "overlap_org": "象山区", "overlap_period": "~2021-2025"},
    # 全州籍贯网络
    {"person_a": 1, "person_b": 3, "type": "same_native_place",
     "context": "均来自广西全州",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "same_native_place",
     "context": "均来自广西全州",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "same_native_place",
     "context": "均来自广西全州",
     "overlap_org": "", "overlap_period": ""},
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
    if "书记" in post and "副" not in post and "副" not in post: return "255,50,50"
    if "区长" in post or ("长" in post and "副" not in post): return "50,100,255"
    if "纪委" in post: return "255,165,0"
    return "100,100,100"

def person_sz(post):
    if ("书记" in post and "副" not in post) or ("长" in post and "副" not in post and "副" not in post):
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
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络</description>')
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

if __name__ == "__main__":
    main()
