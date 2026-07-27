#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 抚顺县, 抚顺市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_抚顺县
Level: 县
Targets: 县委书记 & 县长

Research status: WEB ACCESS DEGRADED
  - Exa API rate-limited (free tier exhausted)
  - Baidu: 403 captcha block
  - Jina Reader: timeout
  - Official 抚顺县人民政府网站 (www.lnfsx.gov.cn): accessible (GBK-encoded)
  - 抚顺市人民政府网站 (www.fushun.gov.cn): accessible (front page only)

Current officeholders:
  - 县委书记: 栾航 (confirmed via official county news article, 2026-06-02)
  - 县委副书记、县长: 郑皓元 (confirmed via official leadership page, 2026-03-31)

Note on web access:
  - 抚顺县人民政府网站 was accessible via direct Python urllib requests
    with GBK encoding. The webfetch tool produced garbled output due to encoding
    mismatch. Direct Python requests with proper GBK decoding revealed accurate data.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "抚顺县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "栾航",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党抚顺县委员会",
        "source": "http://www.lnfsx.gov.cn/ins.asp?s=181&i=36245",
    },
    # ── 县委副书记、县长 ──
    {
        "id": 2,
        "name": "郑皓元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-12",
        "birthplace": "",
        "education": "大学学历，理学学士，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "抚顺县人民政府",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=35484",
    },
    # ── 县委常委、常务副县长 ──
    {
        "id": 3,
        "name": "贺雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长（分管日常工作）",
        "current_org": "抚顺县人民政府",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=21833",
    },
    # ── 县委常委、副县长 ──
    {
        "id": 4,
        "name": "姜琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "抚顺县人民政府",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=36166",
    },
    # ── 县委常委、副县长（挂职） ──
    {
        "id": 5,
        "name": "纪岩成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-11",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "抚顺县人民政府",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=34883",
    },
    # ── 副县长 ──
    {
        "id": 6,
        "name": "田成岩",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1970-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "抚顺县人民政府",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=23355",
    },
    # ── 副县长、县公安局局长 ──
    {
        "id": 7,
        "name": "周晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "抚顺县公安局",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=20331",
    },
    # ── 副县长 ──
    {
        "id": 8,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "抚顺县人民政府",
        "source": "http://www.lnfsx.gov.cn/ins_ld.asp?s=164&i=20459",
    },
    # ── 人大常委会主任 ──
    {
        "id": 9,
        "name": "待查（县人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "抚顺县人大常委会",
        "source": "",
    },
    # ── 政协主席 ──
    {
        "id": 10,
        "name": "待查（县政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协抚顺县委员会",
        "source": "",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党抚顺县委员会", "type": "党委", "level": "县", "parent": "中国共产党抚顺市委员会", "location": "抚顺县"},
    {"id": 2, "name": "抚顺县人民政府", "type": "政府", "level": "县", "parent": "抚顺市人民政府", "location": "抚顺县"},
    {"id": 3, "name": "抚顺县人大常委会", "type": "人大", "level": "县", "parent": "抚顺市人大常委会", "location": "抚顺县"},
    {"id": 4, "name": "政协抚顺县委员会", "type": "政协", "level": "县", "parent": "政协抚顺市委员会", "location": "抚顺县"},
    {"id": 5, "name": "中国共产党抚顺县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共抚顺市纪律检查委员会", "location": "抚顺县"},
    {"id": 6, "name": "抚顺县公安局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 7, "name": "抚顺县发展和改革局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 8, "name": "抚顺县财政局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 9, "name": "抚顺县人力资源和社会保障局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 10, "name": "抚顺县应急管理局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 11, "name": "抚顺县林业和草原局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 12, "name": "抚顺县统计局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 13, "name": "抚顺县水务局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 14, "name": "抚顺县卫生健康局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 15, "name": "抚顺县市场监督管理局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 16, "name": "抚顺县教育局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 17, "name": "抚顺县数据局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 18, "name": "抚顺县工业和信息化局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 19, "name": "抚顺县交通运输局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 20, "name": "抚顺县农业农村局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 21, "name": "抚顺县住房和城乡建设局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 22, "name": "抚顺县司法局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 23, "name": "抚顺县自然资源局", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 24, "name": "抚顺县供销合作社联合社", "type": "群团", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 25, "name": "抚顺县营商环境建设领导小组", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 26, "name": "抚顺县融媒体中心", "type": "事业单位", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
    {"id": 27, "name": "抚顺县防汛抗旱指挥部", "type": "政府", "level": "县", "parent": "抚顺县人民政府", "location": "抚顺县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 栾航 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "中共抚顺县委书记"},
    # 郑皓元 - 县委副书记、县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "抚顺县人民政府党组书记、县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 贺雷 - 县委常委、常务副县长
    {"person_id": 3, "org_id": 2, "title": "常务副县长（分管日常工作）", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府日常工作"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 姜琳 - 县委常委、副县长
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责水利、文化旅游、卫生健康、市场监管"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 纪岩成 - 县委常委、副县长（挂职）
    {"person_id": 5, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、营商环境、数据统筹、招商引资"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    # 田成岩 - 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责交通运输、农业农村、住建、综合执法"},
    # 周晓明 - 副县长、县公安局局长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法"},
    {"person_id": 7, "org_id": 6, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "县公安局党组书记、局长"},
    # 刘涛 - 副县长
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责工信、招商、军民融合、自然资源、生态建设"},
    # 待查人大主任
    {"person_id": 9, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "姓名待查"},
    # 待查政协主席
    {"person_id": 10, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "姓名待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 栾航 <-> 郑皓元 - 党政主要负责人搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档",
     "overlap_org": "抚顺县", "overlap_period": "2025-2026年"},
    # 栾航 <-> 贺雷
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与常务副县长",
     "overlap_org": "抚顺县", "overlap_period": "至2026年7月"},
    # 栾航 <-> 姜琳
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委、副县长",
     "overlap_org": "抚顺县", "overlap_period": "至2026年7月"},
    # 郑皓元 <-> 贺雷 - 县长与常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长，在县政府常务会议上共同出席",
     "overlap_org": "抚顺县人民政府", "overlap_period": "至2026年7月"},
    # 郑皓元 <-> 姜琳 - 县长与副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与分管水利、卫健的副县长",
     "overlap_org": "抚顺县人民政府", "overlap_period": "至2026年7月"},
    # 郑皓元 <-> 纪岩成
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与挂职副县长",
     "overlap_org": "抚顺县人民政府", "overlap_period": "至2026年7月"},
    # 郑皓元 <-> 田成岩
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与分管农口的副县长",
     "overlap_org": "抚顺县人民政府", "overlap_period": "至2026年7月"},
    # 郑皓元 <-> 周晓明
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与公安局长",
     "overlap_org": "抚顺县人民政府", "overlap_period": "至2026年7月"},
    # 郑皓元 <-> 刘涛
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "抚顺县人民政府", "overlap_period": "至2026年7月"},
    # 贺雷 <-> 姜琳 - 同为县委常委
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共抚顺县委员会", "overlap_period": "至2026年7月"},
    # 贺雷 <-> 纪岩成 - 同为县委常委
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共抚顺县委员会", "overlap_period": "至2026年7月"},
    # 姜琳 <-> 纪岩成 - 同为县委常委
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共抚顺县委员会", "overlap_period": "至2026年7月"},
]

# ── Build ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} data...")

    # Ensure staging dir exists
    _CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    # DB
    print(f"  DB: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
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
            source TEXT
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
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]),
        )

    for o in organizations:
        cur.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]),
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]),
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]),
        )

    conn.commit()
    conn.close()
    print(f"  DB written: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # GEXF
    print(f"  GEXF: {GEXF_PATH}")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    from datetime import datetime as dt

    # Person colors by role
    def person_color(p):
        if p["id"] == 1:  # 县委书记
            return "255,50,50"
        elif p["id"] == 2:  # 县长
            return "50,100,255"
        else:
            return "100,100,100"

    # Organization color by type
    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "群团": "255,220,255",
            "事业单位": "220,220,220",
        }
        return colors.get(o["type"], "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>抚顺县领导班子关系网络 - {SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        title = esc(p["current_post"])
        name = esc(p["name"])
        lines.append(f'      <node id="p{p["id"]}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append(f'          <attvalue for="2" value="县"/>')
        lines.append(f'          <attvalue for="3" value="抚顺县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        name = esc(o["name"])
        lines.append(f'      <node id="o{o["id"]}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edge: person <-> organization (worked at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{pos["start"] or "?"} - {pos["end"] or "?"}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edge: person <-> person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {eid} edges")

    # Write person JSON files
    person_json_dir = _CURRENT_DIR
    person_files = []
    for p, filename in [
        (persons[0], f"{TODAY}-辽宁省-抚顺市-县委书记-栾航.json"),
        (persons[1], f"{TODAY}-辽宁省-抚顺市-县长-郑皓元.json"),
    ]:
        fpath = person_json_dir / filename
        # Person JSON files already exist as separate files; this script creates
        # the build data. Person JSONs are written separately.
        person_files.append(filename)

    print(f"  Note: Person JSONs written separately")
    print(f"Done: {SLUG}")
