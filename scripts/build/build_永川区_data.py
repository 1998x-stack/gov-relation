#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yongchuan District (永川区) leadership network."""

import sqlite3
import os
import json
from datetime import datetime

STAGING = "/workspace/data/xieming/other-codes/gov-relation/data/tmp/chongqing_永川区"
BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(STAGING, "永川区_network.db")
GEXF_PATH = os.path.join(STAGING, "永川区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

today = "2026-07-16"

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "关衷效", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共重庆市永川区委书记", "current_org": "中共重庆市永川区委员会",
     "source": "https://www.cqyc.gov.cn/zwgk_204/"},
    # Note: 关衷效 is confirmed as the current Party Secretary from news articles (July 2026) on the official government website.
    # Detailed bio (birth year, birthplace, education) not available on the government profile page.

    # ── District Government Leaders ──
    {"id": 2, "name": "许宏球", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-01", "birthplace": "", "education": "研究生，管理学硕士、公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共重庆市永川区委副书记、区政府区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/zfxxgk/zfxxgkml/jgzn/fzrxx/xhq/202511/t20251119_15174449.html"},

    {"id": 3, "name": "李洁", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "", "education": "研究生，管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共重庆市永川区委常委、区政府常务副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/zfxxgk/zfxxgkml/jgzn/fzrxx/lijie/202412/t20241230_14032914.html"},

    {"id": 4, "name": "宋文", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共重庆市永川区委常委、区政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/zfxxgk/zfxxgkml/jgzn/fzrxx/yh/201912/t20191219_1731069.html"},

    {"id": 5, "name": "宋朝均", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市永川区人民政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/zfxxgk/zfxxgkml/jgzn/fzrxx/scj/201912/t20191219_1731606.html"},

    {"id": 6, "name": "徐秀霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市永川区人民政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/"},

    {"id": 7, "name": "漆远英", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市永川区人民政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/"},

    {"id": 8, "name": "甘宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市永川区人民政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/"},

    {"id": 9, "name": "唐永红", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市永川区人民政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/zfxxgk/zfxxgkml/jgzn/fzrxx/tyh/202503/t20250324_14434820.html"},

    {"id": 10, "name": "冯昭华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市永川区人民政府副区长", "current_org": "重庆市永川区人民政府",
     "source": "https://www.cqyc.gov.cn/zwgk_204/"},  # 2026-01-13 免职通知 confirmed

    # ── Previous Leaders ──
    {"id": 11, "name": "张智奎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
    # Note: 张智奎 was the previous party secretary of Yongchuan District before 关衷效 took over.
    # Further details about his current position need additional research.

    {"id": 12, "name": "常晓勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-04", "birthplace": "", "education": "研究生，历史学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
    # Note: 常晓勇 was the previous district mayor before 许宏球 took over.
    # Born 1974-04, served as Yongchuan District Mayor before being transferred.
]

organizations = [
    {"id": 1, "name": "中共重庆市永川区委员会", "type": "党委", "level": "市辖区", "parent": "中共重庆市委", "location": "重庆市永川区"},
    {"id": 2, "name": "重庆市永川区人民政府", "type": "政府", "level": "市辖区", "parent": "重庆市人民政府", "location": "重庆市永川区"},
    {"id": 3, "name": "重庆市永川区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "重庆市人大常委会", "location": "重庆市永川区"},
    {"id": 4, "name": "中国人民政治协商会议重庆市永川区委员会", "type": "政协", "level": "市辖区", "parent": "重庆市政协", "location": "重庆市永川区"},
]

positions = [
    # 关衷效
    {"person_id": 1, "org_id": 1, "title": "中共重庆市永川区委书记", "start": "", "end": "", "rank": "正厅级", "note": "现任，2025年起任职"},

    # 许宏球
    {"person_id": 2, "org_id": 1, "title": "中共重庆市永川区委副书记", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "重庆市永川区人民政府区长", "start": "", "end": "", "rank": "副厅级", "note": "区政府党组书记"},

    # 李洁
    {"person_id": 3, "org_id": 1, "title": "中共重庆市永川区委常委", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "重庆市永川区人民政府常务副区长", "start": "", "end": "", "rank": "副厅级", "note": "区政府党组副书记，永川高新区、综保区党工委书记"},

    # 宋文
    {"person_id": 4, "org_id": 1, "title": "中共重庆市永川区委常委", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "", "rank": "副厅级", "note": "区政府党组成员"},

    # 宋朝均
    {"person_id": 5, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "", "rank": "副厅级", "note": "区政府党组成员"},

    # 徐秀霞
    {"person_id": 6, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "", "rank": "副厅级", "note": ""},

    # 漆远英
    {"person_id": 7, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "", "rank": "副厅级", "note": ""},

    # 甘宇
    {"person_id": 8, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "", "rank": "副厅级", "note": ""},

    # 唐永红
    {"person_id": 9, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "", "rank": "副厅级", "note": "区政府党组成员"},

    # 冯昭华
    {"person_id": 10, "org_id": 2, "title": "重庆市永川区人民政府副区长", "start": "", "end": "2026-01", "rank": "副厅级", "note": "2026年1月免职"},
]

relationships = [
    # Work relationships between key leaders
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长", "overlap_org": "中共永川区委/永川区政府", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与常务副区长", "overlap_org": "中共永川区委", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与区委常委副区长", "overlap_org": "中共永川区委", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 3, "type": "政府搭档", "context": "区长与常务副区长", "overlap_org": "永川区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "政府搭档", "context": "区长与副区长", "overlap_org": "永川区政府", "overlap_period": "至今"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string for a person based on role."""
    title = p["current_post"]
    if "书记" in title and "区委书记" in title:
        return "255,50,50"  # Red for Party Secretary
    elif "区长" in title and "区委" not in title:
        return "50,100,255"  # Blue for District Mayor
    elif "常务副区长" in title or "常委" in title:
        return "50,100,255"  # Blue for deputy leaders
    else:
        return "100,100,100"  # Grey for others


def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def is_top_leader(p):
    return "区委书记" in p["current_post"] or "区长" in p["current_post"]


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
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
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"],
             p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    posc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]
    conn.close()
    print(f"DB OK — {pc} persons, {oc} orgs, {posc} positions, {rc} relationships")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>永川区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        if not p["name"]:
            continue
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = ""
        if "区委书记" in p["current_post"]:
            role = "party_secretary"
        elif "区长" in p["current_post"]:
            role = "district_mayor"
        elif "副区长" in p["current_post"]:
            role = "deputy_mayor"
        elif "常委" in p["current_post"]:
            role = "committee_member"
        else:
            role = "other"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        # person -> organization
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF OK — {eid} edges written")


def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")


if __name__ == "__main__":
    main()
