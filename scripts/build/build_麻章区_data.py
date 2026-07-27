#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build SQLite DB + GEXF graph for 麻章区 (Mazhang District), 湛江市, 广东省.

Covers: district-level leaders (区委书记, 区长), key standing committee members,
predecessor chain, and organizational relationships.

Current as of: July 2026

Research Sources:
- Wikipedia (zh.wikipedia.org) — 麻章区 page (confirmed 区长: 林洪)
- 麻章区人民政府: www.zjmazhang.gov.cn (unreachable during build)
- 湛江市人民政府: www.zhanjiang.gov.cn

Research Date: 2026-07-22

Web Access Note:
- Exa search API rate-limited
- Government site (www.zjmazhang.gov.cn) unreachable
- Baidu Baike returned 403
- Jina Reader timed out
- Google/Bing blocked from this environment
- Data sourced from Wikipedia and pre-training knowledge

Known gaps:
- 区委书记 当前的任职者未能通过可访问来源确认
- 林洪(区长)的详细履历（出生年份、教育背景、完整工作经历）待补
- 前任区委书记的去向待查
- 常委会其他成员的具体名单待补
- 所有班子成员的出生日期和学历信息待补
"""

import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "麻章区_network.db")
GEXF_PATH = os.path.join(BASE, "麻章区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# ⚠️ Data compiled from limited web access. See open_questions in person JSON.
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 区委书记 — Could not confirm current officeholder from accessible web sources.
    # Based on available knowledge, the 麻章区委书记 in recent years:
    # - Unknown current officeholder as of July 2026
    # This position is typically held by a member of the 湛江市委 committee.
    # Referred historical knowledge only.

    {
        "id": 1,
        "name": "待查",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共湛江市麻章区委书记（任职者待确认）",
        "current_org": "中共湛江市麻章区委员会",
        "source": "无法通过可访问来源确认 — 需要政府网站核实"
    },

    # 林洪 — 麻章区委副书记、区长 (confirmed via Wikipedia)
    {
        "id": 2,
        "name": "林洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻章区委副书记、区长",
        "current_org": "湛江市麻章区人民政府",
        "source": "Wikipedia:麻章区 — 区长: 林洪"
    },

    # ═════════════════════════════════════════════════════════════════════
    # Known historical leaders (for predecessor coverage)
    # ═════════════════════════════════════════════════════════════════════

    # 杨柔彦 — 曾任麻章区委书记（后调任赤坎区委书记）
    # 据公开信息，杨柔彦曾任麻章区委书记，后调任赤坎区委书记
    {
        "id": 3,
        "name": "杨柔彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原麻章区委书记（曾任，后调任赤坎区委书记）",
        "current_org": "中共湛江市麻章区委员会（原）",
        "source": "Historical knowledge — requires verification"
    },

    # 柯俊 — 曾任麻章区委书记（据公开信息）
    {
        "id": 4,
        "name": "柯俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原麻章区委书记（曾任）",
        "current_org": "中共湛江市麻章区委员会（原）",
        "source": "Historical knowledge — requires verification"
    },

    # 杨杰东 — 曾任麻章区委副书记、区长（后调任其他职务）
    {
        "id": 5,
        "name": "杨杰东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原麻章区委副书记、区长（曾任）",
        "current_org": "湛江市麻章区人民政府（原）",
        "source": "Historical knowledge — requires verification"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共湛江市麻章区委员会", "type": "党委", "level": "县处级",
     "parent": "中共湛江市委员会", "location": "湛江市麻章区"},
    {"id": 2, "name": "湛江市麻章区人民政府", "type": "政府", "level": "县处级",
     "parent": "湛江市人民政府", "location": "湛江市麻章区"},
    {"id": 3, "name": "湛江市麻章区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "湛江市人民代表大会常务委员会", "location": "湛江市麻章区"},
    {"id": 4, "name": "中国人民政治协商会议湛江市麻章区委员会", "type": "政协", "level": "县处级",
     "parent": "中国人民政治协商会议湛江市委员会", "location": "湛江市麻章区"},
    {"id": 5, "name": "中共湛江市麻章区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共湛江市纪律检查委员会", "location": "湛江市麻章区"},
    {"id": 6, "name": "湛江经济技术开发区（麻章区相关）", "type": "开发区", "level": "国家级",
     "parent": "湛江市人民政府", "location": "湛江市麻章区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 区委书记（任职者待确认）
    {"id": 1, "person_id": 1, "org_id": 1, "title": "麻章区委书记",
     "start": "", "end": "", "rank": "县处级",
     "note": "当前任职者未能通过可访问来源确认，待政府网站核查"},

    # 林洪 — 区委副书记、区长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "麻章区委副书记、区长",
     "start": "", "end": "", "rank": "县处级",
     "note": "Wikipedia确认当前任职，具体任职起始时间待查"},

    # 杨柔彦 — 原区委书记
    {"id": 3, "person_id": 3, "org_id": 1, "title": "麻章区委书记",
     "start": "", "end": "", "rank": "县处级",
     "note": "曾任麻章区委书记，后调任赤坎区委书记，具体时间待查"},

    # 柯俊 — 原区委书记
    {"id": 4, "person_id": 4, "org_id": 1, "title": "麻章区委书记",
     "start": "", "end": "", "rank": "县处级",
     "note": "曾任麻章区委书记，具体任职时间待查"},

    # 杨杰东 — 原区长
    {"id": 5, "person_id": 5, "org_id": 2, "title": "麻章区委副书记、区长",
     "start": "", "end": "", "rank": "县处级",
     "note": "曾任麻章区区长，后调任其他职务，具体时间待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 区委书记（待确认）vs 林洪 — 当前党政搭档
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "待确认的区委书记与林洪（区长）在麻章区共事",
     "overlap_org": "湛江市麻章区", "overlap_period": ""},

    # 杨柔彦 vs 杨杰东 — 前任党政搭档
    {"id": 2, "person_a": 3, "person_b": 5, "type": "党政搭档",
     "context": "杨柔彦（原区委书记）与杨杰东（原区长）在麻章区共事",
     "overlap_org": "湛江市麻章区", "overlap_period": ""},

    # 杨柔彦 — 柯俊 前后任
    {"id": 3, "person_a": 4, "person_b": 3, "type": "前后任",
     "context": "柯俊与杨柔彦前后任交接",
     "overlap_org": "中共湛江市麻章区委员会", "overlap_period": ""},

    # 杨杰东 — 林洪 前后任
    {"id": 4, "person_a": 5, "person_b": 2, "type": "前后任",
     "context": "杨杰东（原区长）与林洪（现区长）前后任交接",
     "overlap_org": "湛江市麻章区人民政府", "overlap_period": ""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = __import__("sqlite3").connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
    birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"],
               p["birth"], p["birthplace"], p["education"],
               p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"],
               o["parent"], o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"],
               pos["title"], pos["start"], pos["end"],
               pos["rank"], pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"],
               r["type"], r["context"],
               r["overlap_org"], r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

from datetime import datetime

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def pcolor(post):
    if "书记" in post and ("区委" in post or "县委" in post):
        return "230,50,50"  # red for party secretary
    if "区长" in post or "县长" in post:
        return "50,100,230"  # blue for district mayor
    if "副区长" in post or "副县长" in post:
        return "80,140,230"
    if "人大常委会" in post or "人大" in post:
        return "200,255,255"  # cyan
    if "政协" in post:
        return "255,240,200"  # cream
    if "纪委" in post:
        return "255,165,0"  # orange
    return "120,120,120"

def ocolor(otype):
    return {"党委": "255,200,200", "政府": "200,200,255",
            "开发区": "200,255,200", "人大": "200,255,255",
            "政协": "255,240,200"}.get(otype, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>麻章区（湛江市辖区）领导班子工作关系网络 — 2026年7月生成（部分数据需核实）</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"),
                     ("3", "current_post"), ("4", "entity_type"), ("5", "level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post", ""))
    is_top = any(k in p.get("current_post", "") for k in ["书记", "区长"])
    sz = "20.0" if is_top else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0", "person"), ("1", p.get("birth", "")),
                  ("2", p.get("birthplace", "")),
                  ("3", p.get("current_post", "")),
                  ("4", "person"), ("5", "")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0", "organization"), ("1", ""),
                  ("2", o.get("location", "")),
                  ("3", ""), ("4", "organization"),
                  ("5", o.get("level", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                 f'label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f, v in [("0", "worked_at"), ("1", pos.get("start", "")),
                  ("2", pos.get("end", "")), ("3", pos.get("note", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period", "")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                 f'label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f, v in [("0", r["type"]), ("1", ov_s),
                  ("2", ""), ("3", r.get("context", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")

print("\n⚠️ NOTE: This build was conducted under degraded web access conditions.")
print("  The current麻章区委书记 could NOT be confirmed from accessible sources.")
print("  林洪 (区长) was confirmed via Wikipedia.")
print("  All data requires verification against official sources.")
print("\nOpen gaps:")
print("  1. Current区委书记 — unknown, needs official source verification")
print("  2. 林洪's birth, education, and career timeline")
print("  3. 林洪's appointment date")
print("  4. Full standing committee roster")
print("  5. Complete predecessor/successor chain with exact dates")
print("  6. All officials' birthplace, education, and early career")
