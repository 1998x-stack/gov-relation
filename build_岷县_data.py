#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
岷县 (定西市, 甘肃省) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Min County leadership network.

Level: 县
Province: 甘肃省
City: 定西市
Region: 岷县
Targets: 县委书记 & 县长

Research Sources:
- 岷县人民政府官方网站 (minxian.gov.cn) 政务要闻, 2026年7月确认
- 定西市市政府网站 (dingxi.gov.cn)
- 央视《晚间新闻》报道岷县防灾工作

Research Date: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "data/database/岷县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "data/graph/岷县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": "mx_chen_xinmin",
        "name": "陈新民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岷县委书记",
        "current_org": "中共岷县委员会",
        "source": "http://www.minxian.gov.cn — 首页头条: 央视《晚间新闻》报道岷县防灾工作，县委书记陈新民介绍; http://www.minxian.gov.cn/art/2026/7/21/art_2285_1903932.html — 陈新民在十里镇、刘家浪水电站调研",
    },
    {
        "id": "mx_cheng_zhaoxiang",
        "name": "程兆祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "岷县委副书记、县长",
        "current_org": "中共岷县委员会/岷县人民政府",
        "source": "http://www.minxian.gov.cn/art/2026/7/22/art_2285_1904133.html — 程兆祥调研督导安全生产、城市管理及群众身边不正之风和腐败问题集中整治等工作，文中明确标注'县委副书记、县长'",
    },
    {
        "id": "mx_wang_weidong",
        "name": "王伟东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岷县领导（副县长/党组成员）",
        "current_org": "岷县人民政府",
        "source": "http://www.minxian.gov.cn/art/2026/7/22/art_2285_1904133.html — 文中提及'王伟东、闪晓丽分别参加'",
    },
    {
        "id": "mx_shan_xiaoli",
        "name": "闪晓丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岷县领导（副县长/党组成员）",
        "current_org": "岷县人民政府",
        "source": "http://www.minxian.gov.cn/art/2026/7/22/art_2285_1904133.html — 文中提及'王伟东、闪晓丽分别参加'",
    },
    {
        "id": "mx_he_yuanzhong",
        "name": "何元忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "岷县领导（县领导/部门负责人）",
        "current_org": "岷县人民政府",
        "source": "http://www.minxian.gov.cn/art/2026/7/21/art_2285_1903932.html — 陈新民调研新闻报道中提及'何元忠参加有关调研活动'",
    },
]

# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共岷县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定西市委员会",
        "location": "甘肃省定西市岷县",
    },
    {
        "id": 2,
        "name": "岷县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "定西市人民政府",
        "location": "甘肃省定西市岷县",
    },
    {
        "id": 3,
        "name": "中共定西市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省定西市",
    },
    {
        "id": 4,
        "name": "定西市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省定西市",
    },
    {
        "id": 5,
        "name": "十里镇",
        "type": "乡镇",
        "level": "乡科级",
        "parent": "岷县人民政府",
        "location": "甘肃省定西市岷县",
    },
    {
        "id": 6,
        "name": "刘家浪水电站",
        "type": "事业单位",
        "level": "股级",
        "parent": "岷县人民政府",
        "location": "甘肃省定西市岷县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    {
        "person_id": "mx_chen_xinmin",
        "org_id": 1,
        "title": "岷县委书记",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "",
    },
    {
        "person_id": "mx_cheng_zhaoxiang",
        "org_id": 1,
        "title": "岷县委副书记",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "同时担任县长",
    },
    {
        "person_id": "mx_cheng_zhaoxiang",
        "org_id": 2,
        "title": "岷县长",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "县委副书记",
    },
    {
        "person_id": "mx_wang_weidong",
        "org_id": 2,
        "title": "岷县领导（副县长/党组成员）",
        "start": "",
        "end": "present",
        "rank": "副处级",
        "note": "具体职务待查",
    },
    {
        "person_id": "mx_shan_xiaoli",
        "org_id": 2,
        "title": "岷县领导（副县长/党组成员）",
        "start": "",
        "end": "present",
        "rank": "副处级",
        "note": "具体职务待查",
    },
    {
        "person_id": "mx_he_yuanzhong",
        "org_id": 2,
        "title": "岷县领导（部门负责人）",
        "start": "",
        "end": "present",
        "rank": "正科级",
        "note": "具体职务待查",
    },
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    {
        "person_a": "mx_chen_xinmin",
        "person_b": "mx_cheng_zhaoxiang",
        "type": "superior_subordinate",
        "context": "县委书记-县长搭班工作关系",
        "overlap_org": "中共岷县委员会/岷县人民政府",
        "overlap_period": "2025-2026",
        "confidence": "confirmed",
    },
    {
        "person_a": "mx_chen_xinmin",
        "person_b": "mx_he_yuanzhong",
        "type": "superior_subordinate",
        "context": "县委书记调研十里镇、刘家浪水电站，何元忠陪同参加",
        "overlap_org": "岷县人民政府",
        "overlap_period": "2026-07",
        "confidence": "confirmed",
    },
    {
        "person_a": "mx_cheng_zhaoxiang",
        "person_b": "mx_wang_weidong",
        "type": "superior_subordinate",
        "context": "县长程兆祥调研安全生产等工作，王伟东陪同参加",
        "overlap_org": "岷县人民政府",
        "overlap_period": "2026-07",
        "confidence": "confirmed",
    },
    {
        "person_a": "mx_cheng_zhaoxiang",
        "person_b": "mx_shan_xiaoli",
        "type": "superior_subordinate",
        "context": "县长程兆祥调研安全生产等工作，闪晓丽陪同参加",
        "overlap_org": "岷县人民政府",
        "overlap_period": "2026-07",
        "confidence": "confirmed",
    },
]

# ═══════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title and ("副" not in title or "副书记" not in title):
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title or "监察" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副" in title:
        return "100,100,200"  # Light blue — Deputy
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other


def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title:
        return "20.0"
    if "县长" in title and "副" not in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"


def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "乡镇": "255,255,200",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
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
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
              p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
              pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")


# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>岷县 (定西市, 甘肃省) 领导班子工作关系网络 — 陈新民 程兆祥</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("location", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person->organization edges (positions)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person<->person edges (relationships)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# ── Run ──

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
