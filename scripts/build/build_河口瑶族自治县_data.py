#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 河口瑶族自治县, 红河哈尼族彝族自治州, 云南省.

Investigation date: 2026-07-28
Task ID: yunnan_河口瑶族自治县
Level: 县
Targets: 县委书记 & 县长

Research status: COMPLETED (sources: official government website hhhk.gov.cn)
As of: 2026-07-28

Current leadership (as of July 2026):
- 县委书记: 黄杰 (male, Han, unknown birth, unknown birthplace) - also 自贸试验区红河片区党工委副书记、管委会主任
- 县长: 田成 (male, Yao, 1987-03, Yunnan Jinping)

Key predecessor transitions:
- 邓瑞 (former 县长, as of Jan 2026) → succeeded by 田成
- 黄杰 is current 县委书记 (confirmed by multiple news articles Jul 2026)
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "河口瑶族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Person Data ────────────────────────────────────────────────────────────
# Source confidence:
#   confirmed = official government website (www.hhhk.gov.cn) or multiple sources
#   plausible = single reliable source (media)
#   unverified = inferred or uncorroborated

persons = [
    # ═══════ Current Core Leadership ═══════
    {
        "id": 1,
        "name": "黄杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县委书记",
        "current_org": "中共河口瑶族自治县委员会",
        "source": "https://www.hhhk.gov.cn/ 新闻报道; 河口县人民武装部党委第一书记任职宣布大会 (2026-07-17)"
    },
    {
        "id": 2,
        "name": "田成",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1987-03",
        "birthplace": "云南省金平苗族瑶族傣族自治县",
        "education": "大学学历",
        "party_join": "",
        "work_start": "2010-07",
        "current_post": "河口县人民政府县长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/info/2881/397121.htm (田成官方简历)"
    },
    # ═══════县委领导 ═══════
    {
        "id": 3,
        "name": "张恩崎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县委副书记",
        "current_org": "中共河口瑶族自治县委员会",
        "source": "https://www.hhhk.gov.cn/ 田成率队赴广州、昆明等地开展招商考察活动 (2026-07-27)"
    },
    {
        "id": 4,
        "name": "李季",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县委常委、县委办公室主任",
        "current_org": "中共河口瑶族自治县委员会",
        "source": "https://www.hhhk.gov.cn/ 黄杰到县人大常委会走访调研 (2026-07-20)"
    },
    # ═══════县政府领导 ═══════
    {
        "id": 5,
        "name": "朱宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县委常委、常务副县长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm; 河政发〔2026〕1号 领导工作分工"
    },
    {
        "id": 6,
        "name": "邓海江",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "1996-08",
        "current_post": "河口县人民政府党组成员",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/info/2881/397161.htm (邓海江官方简历)"
    },
    {
        "id": 7,
        "name": "张虎彪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府党组成员",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    {
        "id": 8,
        "name": "李维",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府副县长（挂职）",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    {
        "id": 9,
        "name": "李华梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府副县长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    {
        "id": 10,
        "name": "卢光荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府副县长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    {
        "id": 11,
        "name": "仇群钻",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府副县长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    {
        "id": 12,
        "name": "刘小艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府副县长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    {
        "id": 13,
        "name": "李颖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人民政府副县长、县公安局局长",
        "current_org": "河口瑶族自治县人民政府",
        "source": "https://www.hhhk.gov.cn/zfxxgk/fdzdgknr/zfld.htm"
    },
    # ═══════ Predecessors ═══════
    {
        "id": 14,
        "name": "邓瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任县长，2026年1月仍在任）",
        "current_org": "河口瑶族自治县人民政府（前任）",
        "source": "https://www.hhhk.gov.cn/info/2911/389061.htm 河政发〔2026〕1号 (2026-01-19)"
    },
    # ═══════人大/政协领导 ═══════
    {
        "id": 15,
        "name": "李开祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县人大常委会主任",
        "current_org": "河口瑶族自治县人大常委会",
        "source": "https://www.hhhk.gov.cn/ 县委全面深化改革委员会召开会议 (2026-07-23)"
    },
    {
        "id": 16,
        "name": "杨光云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河口县政协主席",
        "current_org": "中国人民政治协商会议河口瑶族自治县委员会",
        "source": "https://www.hhhk.gov.cn/ 县委全面深化改革委员会召开会议 (2026-07-23)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共河口瑶族自治县委员会", "type": "党委", "level": "县级", "parent": "中共红河哈尼族彝族自治州委员会", "location": "云南省红河州河口县"},
    {"id": 2, "name": "河口瑶族自治县人民政府", "type": "政府", "level": "县级", "parent": "红河哈尼族彝族自治州人民政府", "location": "云南省红河州河口县"},
    {"id": 3, "name": "中共中国（云南）自由贸易试验区红河片区工作委员会", "type": "开发区", "level": "国家级片区", "parent": "", "location": "云南省红河州河口县"},
    {"id": 4, "name": "河口瑶族自治县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "云南省红河州河口县"},
    {"id": 5, "name": "政协河口瑶族自治县委员会", "type": "政协", "level": "县级", "parent": "", "location": "云南省红河州河口县"},
    {"id": 6, "name": "河口县人民武装部", "type": "事业单位", "level": "县级", "parent": "", "location": "云南省红河州河口县"},
    {"id": 7, "name": "河口县纪委监委", "type": "党委", "level": "县级", "parent": "中共红河哈尼族彝族自治州纪律检查委员会", "location": "云南省红河州河口县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 黄杰
    {"person_id": 1, "org_id": 1, "title": "河口县委书记", "start": "", "end": "present", "rank": "正处级", "note": "县委书记 confirmed as of 2026-07-28"},
    {"person_id": 1, "org_id": 3, "title": "自贸试验区红河片区党工委副书记、管委会主任", "start": "", "end": "present", "rank": "", "note": "黄杰同时兼任自贸区职务"},
    {"person_id": 1, "org_id": 6, "title": "河口县人民武装部党委第一书记", "start": "2026-07", "end": "present", "rank": "", "note": "2026年7月15日任职大会宣布"},

    # 田成
    {"person_id": 2, "org_id": 2, "title": "河口县人民政府县长", "start": "2026", "end": "present", "rank": "正处级", "note": "田成在2026年接替邓瑞任县长"},
    {"person_id": 2, "org_id": 1, "title": "河口县委副书记", "start": "2026", "end": "present", "rank": "", "note": "田成兼任县委副书记"},
    {"person_id": 2, "org_id": 3, "title": "自贸试验区红河片区管委会副主任（兼）", "start": "", "end": "present", "rank": "", "note": "田成兼任自贸区管委会副主任"},

    # 张恩崎
    {"person_id": 3, "org_id": 1, "title": "河口县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李季
    {"person_id": 4, "org_id": 1, "title": "河口县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 朱宏
    {"person_id": 5, "org_id": 2, "title": "河口县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 邓海江
    {"person_id": 6, "org_id": 2, "title": "河口县人民政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": "兼自贸试验区红河片区管委会副主任"},

    # 张虎彪
    {"person_id": 7, "org_id": 2, "title": "河口县人民政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李维
    {"person_id": 8, "org_id": 2, "title": "河口县人民政府副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},

    # 李华梅
    {"person_id": 9, "org_id": 2, "title": "河口县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 卢光荣
    {"person_id": 10, "org_id": 2, "title": "河口县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 仇群钻
    {"person_id": 11, "org_id": 2, "title": "河口县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 刘小艳
    {"person_id": 12, "org_id": 2, "title": "河口县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李颖
    {"person_id": 13, "org_id": 2, "title": "河口县人民政府副县长、县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 邓瑞（前任县长）
    {"person_id": 14, "org_id": 2, "title": "河口县人民政府县长", "start": "", "end": "2026", "rank": "正处级", "note": "前任县长，2026年1月仍在职"},

    # 李开祥
    {"person_id": 15, "org_id": 4, "title": "河口县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 杨光云
    {"person_id": 16, "org_id": 5, "title": "河口县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 黄杰 ↔ 田成 (上下级)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "中共河口县委/河口县人民政府", "overlap_period": "2026-至今"},
    # 黄杰 ↔ 张恩崎 (县委领导)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记政治搭档", "overlap_org": "中共河口县委", "overlap_period": ""},
    # 田成 ↔ 邓瑞 (前后任)
    {"person_a": 2, "person_b": 14, "type": "predecessor_successor", "context": "田成接替邓瑞任河口县长", "overlap_org": "河口县人民政府", "overlap_period": ""},
    # 田成 ↔ 朱宏 (正副配合)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务副县长的日常工作配合", "overlap_org": "河口县人民政府", "overlap_period": "2026-至今"},
    # 黄杰 ↔ 李季 (办公室主任)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委办公室主任为县委书记服务", "overlap_org": "中共河口县委", "overlap_period": ""},
]

# ── Build Database ─────────────────────────────────────────────────────────
def build_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, "end" TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()

    # Summary
    print(f"Database: {DB_PATH}")
    print(f"  Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()


# ── Build GEXF ─────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "县委" in role:
        return "255,50,50"   # Party Secretary - Red
    if "县长" in role:
        return "50,100,255"  # Government head - Blue
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"   # Discipline - Orange
    return "100,100,100"     # Others - Grey

def is_top_leader(p):
    role = p.get("current_post", "")
    return "书记" in role or "县长" in role and ("副" not in role)

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_org", ""))}"/>')
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
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person -> person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")


# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_db()
    print("---")
    build_gexf()
    print("Done.")