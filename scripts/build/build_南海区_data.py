#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南海区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 佛山市
Region: 南海区
Targets: 区委书记 & 区长

Research Sources:
- 维基百科南海区词条 — 区委书记顾耀辉确认 (2026-07-07更新)
- 佛山市南海区人民政府门户网站 (www.nanhai.gov.cn) — 常务会议新闻确认区长黄志捷
- 南海区人民政府网站 — 领导之窗路径不可达 (403/404)
- 百度百科 — Baidu返回403被拦截
- Exa搜索 — 达到速率限制
- Google/Bing — 超时或被拦截

Research Date: 2026-07-22

网络环境限制说明:
- Exa搜索达到速率限制
- Baidu/So.com搜索被验证码拦截
- Google/Bing搜索超时
- 南海区政府网站领导之窗子页面不可达
- Jina Reader超时
- 基于维基百科确认区委书记，区政府门户网站确认区长
"""

import os
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "南海区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "南海区_network.gexf")

import sqlite3

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1. Current Top Leaders ──
    {
        "id": "1",
        "name": "顾耀辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市南海区委书记",
        "current_org": "中共佛山市南海区委员会",
        "source": "维基百科南海区词条 (zh.wikipedia.org) — 区委书记顾耀辉 (2026-07-07更新)"
    },
    {
        "id": "2",
        "name": "黄志捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市南海区委副书记、区长",
        "current_org": "佛山市南海区人民政府",
        "source": "www.nanhai.gov.cn — 区政府常务会议新闻稿 '黄志捷主持召开区政府常务会议' (2026年4-7月)"
    },
]

organizations = [
    {
        "id": "1",
        "name": "中共佛山市南海区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共佛山市委",
        "location": "佛山市南海区"
    },
    {
        "id": "2",
        "name": "佛山市南海区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "佛山市人民政府",
        "location": "佛山市南海区"
    },
    {
        "id": "3",
        "name": "中共佛山市南海区纪律检查委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共佛山市南海区委员会",
        "location": "佛山市南海区"
    },
    {
        "id": "4",
        "name": "佛山市南海区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区",
        "parent": "佛山市人民代表大会常务委员会",
        "location": "佛山市南海区"
    },
    {
        "id": "5",
        "name": "中国人民政治协商会议佛山市南海区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "佛山市政协",
        "location": "佛山市南海区"
    },
]

positions = [
    # 顾耀辉
    {
        "person_id": "1",
        "org_id": "1",
        "title": "佛山市南海区委书记",
        "start": "待查",
        "end": "present",
        "rank": "正处级",
        "note": "维基百科南海区词条确认"
    },
    # 黄志捷
    {
        "person_id": "2",
        "org_id": "2",
        "title": "佛山市南海区委副书记、区长",
        "start": "待查",
        "end": "present",
        "rank": "正处级",
        "note": "nanhai.gov.cn — 区政府常务会议新闻确认区长职务"
    },
]

relationships = [
    {
        "person_a": "1",
        "person_b": "2",
        "type": "superior_subordinate",
        "context": "区委书记与区长 — 党政主要领导搭档",
        "overlap_org": "中共佛山市南海区委员会/佛山市南海区人民政府",
        "overlap_period": "当前任期",
        "confidence": "confirmed"
    },
]

# ════════════════════════════════════════════════════════════════
# SQLite Database
# ════════════════════════════════════════════════════════════════


def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════════════
# GEXF Graph
# ════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title and "统战" not in title:
        return "255,50,50"  # Red — Party Secretary
    if "区长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"  # Blue — District Mayor
    if "区长" in title:
        return "50,100,255"
    if "纪委" in title or "监委" in title:
        return "255,165,0"  # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"  # Dark red
    return "100,100,100"  # Grey


def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "区委书记" in title or "县委书记" in title:
        return "20.0"
    if "区长" in title or "县长" in title:
        return "20.0"
    return "12.0"


def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>南海区领导班子工作关系网络 - 数据来源: 维基百科及nanhai.gov.cn</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="佛山市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="佛山市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════

def main():
    print(f"=== 南海区网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
