#!/usr/bin/env python3
"""
鸡冠区（黑龙江省鸡西市）领导班子工作关系网络 — 2026-08-05
Build script for Jiguan District, Jixi City, Heilongjiang Province.

Data sources:
- 鸡西市人民政府官网领导简介页 (鸡西市委常委、副市长兼任鸡冠区委书记):
  https://www.jixi.gov.cn/jixi/c100012/202603/c06_359134.shtml  (2026-03)
- 本地仓库既有产物 scripts/build/build_鸡西市_data.py（同源官方 bio 页）
- ACCESS NOTE: 本次调研处于退化网络环境（Exa rate-limited，百度/政府站点/Jina/Bing 全部超时）。
  区长身份及班子名录未能在受限访问下直接确认，按 partial-evidence 模式以"待查"精确编码缺口，
  不虚构日期/学历/籍贯。详见 data/tmp/heilongjiang_鸡冠区/checkpoint_01_research.md 与 report/open_gaps.md。

TASK: heilongjiang_鸡冠区
"""

import os
import sqlite3
from datetime import datetime

TODAY = "2026-08-05"
AS_OF = TODAY
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
# 暂存路径：先写入 data/tmp/<task>/，经 process_tmp.py 校验后再归档
IS_STAGED = "data/tmp" in os.path.abspath(__file__)
if IS_STAGED:
    _base = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(_base, "鸡冠区_network.db")
    GEXF_PATH = os.path.join(_base, "鸡冠区_network.gexf")
else:
    DB_PATH = os.path.join(REPO_ROOT, "data", "database", "鸡冠区_network.db")
    GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "鸡冠区_network.gexf")

# ── HELPERS ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(role):
    if role is None:
        role = ""
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "220,30,30"
    if "长" in role and "副" not in role:
        return "40,100,220"
    if "副" in role and "长" in role:
        return "40,140,220"
    if "常委" in role:
        return "120,80,180"
    if "公安" in role:
        return "60,120,60"
    return "160,160,160"


def is_top_leader(role):
    if role is None:
        return False
    return "书记" in role or ("长" in role and "副" not in role)


def person_size(role):
    return "20.0" if is_top_leader(role) else "12.0"


def org_color(org_type):
    if org_type is None:
        org_type = ""
    if "党委" in org_type:
        return "200,60,60"
    if "政府" in org_type:
        return "60,100,200"
    if "人大" in org_type:
        return "200,150,40"
    if "政协" in org_type:
        return "180,130,40"
    if "纪委" in org_type:
        return "160,120,40"
    return "120,120,120"


# =========================================================================
# DATA
# =========================================================================

# ── PERSONS ──
# [id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
#  current_post, current_org, source]

PERSONS = [
    # ── 区委书记 (Top Leader) ──
    # 于君：鸡西市委常委、副市长兼任鸡冠区委书记（官方领导简介页确认，见 build_鸡西市_data.py）
    ["heilongjiang_jiguan_yu_jun", "于君", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "鸡西市委常委、副市长，鸡冠区委书记",
     "中共鸡西市鸡冠区委员会/鸡西市人民政府",
     "鸡西市人民政府官网领导简介页 https://www.jixi.gov.cn/jixi/c100012/202603/c06_359134.shtml (2026-03, confirmed)"],
]

# ── ORGANIZATIONS ──
# [id, name, type, level, parent, location]

ORGANIZATIONS = [
    ["org_jiguan_party_committee", "中共鸡西市鸡冠区委员会", "党委", "县处级",
     "中共鸡西市委", "黑龙江省鸡西市鸡冠区"],
    ["org_jiguan_gov", "鸡西市鸡冠区人民政府", "政府", "县处级",
     "鸡西市人民政府", "黑龙江省鸡西市鸡冠区"],
    ["org_jiguan_discipline", "中共鸡西市鸡冠区纪律检查委员会", "纪委", "县处级",
     "中共鸡西市纪委", "黑龙江省鸡西市鸡冠区"],
]

# ── POSITIONS ──
# [person_id, org_id, title, start, end, rank, note]

POSITIONS = [
    # 于君 (区委书记)
    ["heilongjiang_jiguan_yu_jun", "org_jiguan_party_committee",
     "鸡冠区委书记", "待查", "present", "县处级",
     "confirmed via 鸡西市政府官网领导简介 (2026-03). 兼任鸡西市委常委、副市长."],
    # 于君 在市政府/市委常委的兼任（同一人跨组织任职，构成->双重身份）
    ["heilongjiang_jiguan_yu_jun", "org_jiguan_party_committee",
     "鸡西市委常委（兼任）", "待查", "present", "副厅级",
     "于君以鸡西市委常委身份兼任鸡冠区委书记，官方 bio. As of 2026-03."],
]

# ── RELATIONSHIPS ──
# [person_a, person_b, type, context, overlap_org, overlap_period, confidence]
# 在只有一名核心人物确认身份、区长待查的情况下，暂无可确证的 personnel 关系。
# 预留结构性占位，避免虚构关系；gap 记入 open_gaps。

RELATIONSHIPS = [
]


# =========================================================================
# SQLITE DATABASE
# =========================================================================

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
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
        )
    """)

    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")


# =========================================================================
# GEXF GRAPH
# =========================================================================

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>鸡冠区（黑龙江省鸡西市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[9]
        org = p[10]
        color = person_color(role)
        size = person_size(role)
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value="县处级"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        color = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o[3])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # person->organization (worked_at)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{pos[3]}~{pos[4]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person <-> person (relationship)
    for r in RELATIONSHIPS:
        lines.append(f'      <edge id="e{eid}" source="{r[0]}" target="{r[1]}" label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{r[5]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=== 鸡冠区（鸡西市）工作关系网络构建 ===")
    print(f"Date: {TODAY}")
    print()
    print("Building database...")
    build_db()
    print("Building GEXF graph...")
    build_gexf()

    print()
    print("Summary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print()
    print("Note: partial-evidence mode. 区长身份待查 (see open_gaps).")
    print("Done.")