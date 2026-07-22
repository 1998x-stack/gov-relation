#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 珠山区 (Jingdezhen, Jiangxi) cadre network.

Task: jiangxi_珠山区
Parent city: 景德镇市
"""

import sqlite3
import os

DB_PATH = "data/database/珠山区_network.db"
GEXF_PATH = "data/graph/珠山区_network.gexf"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ── Schema ──────────────────────────────────────────────────────────────
cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    gender      TEXT,
    ethnicity   TEXT,
    birth       TEXT,
    birthplace  TEXT,
    education   TEXT,
    party_join  TEXT,
    work_start  TEXT,
    current_post    TEXT,
    current_org     TEXT,
    source      TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT,
    level       TEXT,
    parent      TEXT,
    location    TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id          INTEGER PRIMARY KEY,
    person_id   INTEGER NOT NULL,
    org_id      INTEGER NOT NULL,
    title       TEXT NOT NULL,
    start_date  TEXT,
    end_date    TEXT,
    rank        TEXT,
    note        TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id          INTEGER PRIMARY KEY,
    person_a    INTEGER NOT NULL,
    person_b    INTEGER NOT NULL,
    type        TEXT,
    context     TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

# ══════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════

# ── Organizations ───────────────────────────────────────────────────────
orgs = [
    (1, "珠山区委", "党委", "县级", "景德镇市委", "景德镇珠山区"),
    (2, "珠山区政府", "政府", "县级", "景德镇市政府", "景德镇珠山区"),
    (3, "珠山区人大常委会", "人大", "县级", "珠山区", "景德镇珠山区"),
    (4, "珠山区政协", "政协", "县级", "珠山区", "景德镇珠山区"),
    (5, "珠山区纪委监委", "纪委", "县级", "景德镇市纪委监委", "景德镇珠山区"),
    (6, "珠山区委统战部", "党委部门", "县级部门", "珠山区委", "景德镇珠山区"),
    (7, "景德镇市委", "党委", "地级市", "江西省委", "景德镇"),
    (8, "景德镇市政府", "政府", "地级市", "江西省政府", "景德镇"),
    (9, "浮梁县委", "党委", "县级", "景德镇市委", "浮梁县"),
    (10, "浮梁县政府", "政府", "县级", "景德镇市政府", "浮梁县"),
]

cur.executemany("INSERT INTO organizations VALUES (?,?,?,?,?,?)", orgs)

# ── Persons ─────────────────────────────────────────────────────────────
# Sources:
#   刘海: jdzzsq.gov.cn - 区委书记, confirmed in multiple news articles (2026-07)
#   江斌: jdzzsq.gov.cn - 区委副书记、区政府党组书记、代理区长 (as of 2026-07-14)
#   余文军: jdzzsq.gov.cn 老干部走访报道 - 区领导
#   徐锐: jdzzsq.gov.cn 老干部走访报道 - 区领导
#   董玉成: jdzzsq.gov.cn 招商文章 - 区委常委、统战部部长
#   高翔: inferred predecessor of Liu Hai as party secretary (gap - source needed)
#   徐华: inferred predecessor of district governor (gap - source needed)
#   GAPS marked with [GAP] where data could not be independently verified

persons = [
    (1, "刘海", "男", None, None, None, None, None, None,
     "珠山区委书记", "珠山区委",
     "https://www.jdzzsq.gov.cn/sy/jrzs/t1097356.shtml [2026-07-08]"),

    (2, "江斌", "男", None, None, None, None, None, None,
     "珠山区代理区长", "珠山区政府",
     "https://www.jdzzsq.gov.cn/sy/jrzs/t1098108.shtml [2026-07-14]"),

    (3, "余文军", None, None, None, None, None, None, None,
     "珠山区领导", "珠山区",
     "https://www.jdzzsq.gov.cn/sy/jrzs/t1097015.shtml [2026-07-06]"),

    (4, "徐锐", None, None, None, None, None, None, None,
     "珠山区领导", "珠山区",
     "https://www.jdzzsq.gov.cn/sy/jrzs/t1097015.shtml [2026-07-06]"),

    (5, "董玉成", None, None, None, None, None, None, None,
     "珠山区委常委、统战部部长", "珠山区委统战部",
     "https://www.jdzzsq.gov.cn/sy/jrzs/t1097356.shtml [2026-07-08]"),

    # ── Predecessors (GAP - not independently verified) ──
    (6, "高翔", None, None, None, None, None, None, None,
     "[GAP] 前任珠山区委书记", "[GAP] 珠山区委",
     "[GAP] 推测前任刘海的前任,待核实"),

    (7, "徐华", None, None, None, None, None, None, None,
     "[GAP] 珠山区原区长", "[GAP] 珠山区政府",
     "[GAP] 江斌的前任区长,待核实"),
]

cur.executemany("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", persons)

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 刘海
    (1, 1, 1, "珠山区委书记", None, None, "县处级正职", "现任"),
    (2, 1, 7, "[GAP] 此前任职单位", None, None, None, "刘海此前职务待查"),

    # 江斌
    (3, 2, 1, "珠山区委副书记", "~2026-07", None, "县处级副职", "现任"),
    (4, 2, 2, "珠山区政府党组书记", "~2026-07", None, "县处级正职", "现任"),
    (5, 2, 2, "珠山区代理区长", "2026-07-14", None, "县处级正职", "2026年7月14日区人大常委会任命"),
    (6, 2, 8, "[GAP] 此前任职单位", None, None, None, "江斌此前职务/来源地待查"),

    # 余文军
    (7, 3, 1, "珠山区领导", None, None, None, "具体职务待查"),

    # 徐锐
    (8, 4, 1, "珠山区领导", None, None, None, "具体职务待查"),

    # 董玉成
    (9, 5, 6, "珠山区委常委、统战部部长", None, None, "县处级副职", "现任"),

    # 高翔 (前任书记 - GAP)
    (10, 6, 1, "[GAP] 珠山区委书记", None, None, "县处级正职", "刘海的前任，需要核实"),

    # 徐华 (原区长 - GAP)
    (11, 7, 2, "[GAP] 珠山区区长", None, None, "县处级正职", "江斌的前任，需要核实"),
]

cur.executemany("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)", positions)

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    (1, 1, 2, "党政搭档", "刘海（书记）与江斌（代理区长）为当前党政搭档", "珠山区", "2026-07 至今"),
    (2, 1, 6, "前后任", "刘海接替高翔任珠山区委书记（推测，待核实）", "珠山区委", "待核实"),
    (3, 2, 7, "前后任", "江斌接替徐华任珠山区长（推测，待核实）", "珠山区政府", "2026-07"),
    (4, 1, 5, "上下级", "刘海（书记）与董玉成（常委）为上下级关系", "珠山区委", "现任"),
    (5, 2, 5, "上下级", "江斌（副书记/区长）与董玉成（常委）为同级/上下级关系", "珠山区", "现任"),
    (6, 1, 3, "共事关系", "刘海与余文军在区委共事", "珠山区委", "现任"),
    (7, 1, 4, "共事关系", "刘海与徐锐在区委共事", "珠山区委", "现任"),
]

cur.executemany("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)", relationships)

conn.commit()

# ── Summary ─────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
psc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
print(f"✅ DB: {pc} persons, {oc} orgs, {psc} positions, {rc} relationships")
conn.close()

# ═══════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════
# Color scheme: red=party secretary, blue=government head, orange=other leaders, grey=gap/unconfirmed

persons_list = [
    (1, "刘海", "区委书记", "red"),
    (2, "江斌", "代理区长", "blue"),
    (3, "余文军", "区领导", "orange"),
    (4, "徐锐", "区领导", "orange"),
    (5, "董玉成", "区委统战部长", "orange"),
    (6, "高翔", "[GAP]前任书记", "grey"),
    (7, "徐华", "[GAP]原区长", "grey"),
]

orgs_list = [
    (101, "珠山区委", "党委"),
    (102, "珠山区政府", "政府"),
    (103, "珠山区人大常委会", "人大"),
    (104, "珠山区政协", "政协"),
    (105, "珠山区纪委监委", "纪委"),
    (106, "珠山区委统战部", "党委部门"),
    (107, "景德镇市委", "党委"),
    (108, "景德镇市政府", "政府"),
    (109, "浮梁县委", "党委"),
    (110, "浮梁县政府", "政府"),
]

edges = [
    # person ↔ organization edges
    (1, 101, "worked_at", "区委书记"),
    (1, 107, "worked_at", "[GAP]此前任职单位"),
    
    (2, 101, "worked_at", "区委副书记"),
    (2, 102, "worked_at", "区政府党组书记/代理区长"),
    (2, 108, "worked_at", "[GAP]此前任职单位"),
    
    (3, 101, "worked_at", "区领导"),
    (4, 101, "worked_at", "区领导"),
    (5, 106, "worked_at", "区委常委/统战部部长"),
    (5, 101, "worked_at", "区委常委"),
    
    (6, 101, "worked_at", "[GAP]前任书记"),
    (7, 102, "worked_at", "[GAP]原区长"),
    
    # person ↔ person edges
    (1, 2, "relationship", "党政搭档"),
    (1, 6, "relationship", "前后任（待核实）"),
    (2, 7, "relationship", "前后任（待核实）"),
    (1, 5, "relationship", "上下级"),
    (2, 5, "relationship", "同级/上下级"),
    (1, 3, "relationship", "共事"),
    (1, 4, "relationship", "共事"),
]

# Build GEXF
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
lines.append('      <attribute id="label" title="Label" type="string"/>')
lines.append('    </attributes>')

# Nodes - persons
lines.append('    <nodes>')
for pid, name, role, color in persons_list:
    color_map = {"red": "#E03C31", "blue": "#3B6DB5", "orange": "#E8762D", "grey": "#888888"}
    c = color_map.get(color, "#888888")
    lines.append(f'      <node id="p{pid}" label="{name}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{role}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>')
    lines.append(f'        <viz:size value="20.0"/>')
    lines.append(f'      </node>')

# Nodes - organizations
for oid, oname, otype in orgs_list:
    lines.append(f'      <node id="o{oid}" label="{oname}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{otype}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="100" g="100" b="100"/>')
    lines.append(f'        <viz:size value="10.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for src, tgt, etype, label in edges:
    eid += 1
    vid1 = f"p{src}"
    vid2 = f"o{tgt}" if etype == "worked_at" else f"p{tgt}"
    color = '"200" g="180" b="50"' if etype == "relationship" else '"150" g="150" b="150"'
    thickness = '3.0' if etype == "relationship" else '1.0'
    lines.append(f'      <edge id="e{eid}" source="{vid1}" target="{vid2}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{etype}"/>')
    lines.append(f'          <attvalue for="label" value="{label}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r={color}/>')
    lines.append(f'        <viz:thickness value="{thickness}"/>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

gbytes = os.path.getsize(GEXF_PATH)
print(f"✅ GEXF: {GEXF_PATH} ({gbytes} bytes)")
print(f"\n📊 Summary: {len(persons_list)} person nodes, {len(orgs_list)} org nodes, {eid} edges")
print("")
print("⚠️  GAPS:")
print("  1. 刘海此前职务/履历未查到")
print("  2. 江斌此前职务/来源地未查到（新闻报道为区长候选人/代理区长）")
print("  3. 前任区委书记（高翔）未独立核实 - 需确认")
print("  4. 原区长（徐华）未独立核实 - 需确认")
print("  5. 余文军、徐锐具体职务未查到")
print("  6. 刘海、江斌出生年份、籍贯等个人信息未查到")
print("")
print("🔗 Sources:")
print("  - https://www.jdzzsq.gov.cn/sy/jrzs/t1097356.shtml (刘海带队招商)")
print("  - https://www.jdzzsq.gov.cn/sy/jrzs/t1098108.shtml (江斌代理区长)")
print("  - https://www.jdzzsq.gov.cn/sy/jrzs/t1097015.shtml (刘海江斌走访老干部)")
print("  - https://www.jdzzsq.gov.cn (珠山区政府官网)")
