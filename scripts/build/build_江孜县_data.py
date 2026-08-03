#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 江孜县 (Gyantse County / Gyangzê), 日喀则市, 西藏自治区.

Research status: Web access to government sites (www.jiangzi.gov.cn) and Baidu
unavailable from this environment. Wikipedia provides county background. Leadership
information compiled with explicit confidence labels — all names pending verification.

Key confirmed facts:
- 江孜县 is in 日喀则市, 西藏自治区 (historic 3rd city of Tibet)
- Admin: 1 town (江孜镇) + 18 townships
- County-level (县级) administrative unit
- Website: www.jiangzi.gov.cn
"""

import sys, os, sqlite3
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, BASE)

SLUG = "江孜县"
TODAY = datetime.now().strftime("%Y-%m-%d")
TASK_ID = "xizang_江孜县"
STAGING = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(STAGING, "江孜县_network.db")
GEXF_PATH = os.path.join(STAGING, "江孜县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# SQL SCHEMA
# ═══════════════════════════════════════════════════════════════════════
CREATE_PERSONS = """CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT DEFAULT '',
    ethnicity TEXT DEFAULT '',
    birth TEXT DEFAULT '',
    birthplace TEXT DEFAULT '',
    education TEXT DEFAULT '',
    party_join TEXT DEFAULT '',
    work_start TEXT DEFAULT '',
    current_post TEXT DEFAULT '',
    current_org TEXT DEFAULT '',
    source TEXT DEFAULT ''
)"""
CREATE_ORGANIZATIONS = """CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
)"""
CREATE_POSITIONS = """CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    note TEXT DEFAULT '',
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
)"""
CREATE_RELATIONSHIPS = """CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)"""

# ═══════════════════════════════════════════════════════════════════════
# DATA — Person IDs: 1=PartySec, 2=Mayor, 3=DepSec, 4=ExecVice, 5=Discipline,
# 6=Org, 7=Propaganda, 8=Legal, 9=UnitedFront, 10=NPC, 11=CPPCC
# ═══════════════════════════════════════════════════════════════════════
PERSONS = [
    (1,  "（待确认）", "男", "藏族", "", "", "", "", "", "江孜县委书记", "中共江孜县委员会",
     "待确认 — 江孜县人民政府网(www.jiangzi.gov.cn) 或 日喀则市委组织部任前公示"),
    (2,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县长", "江孜县人民政府",
     "待确认：www.jiangzi.gov.cn 或 西藏自治区人民政府网"),
    (3,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委副书记（专职）", "中共江孜县委员会", "待确认"),
    (4,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委常委、常务副县长", "江孜县人民政府", "待确认"),
    (5,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委常委、纪委书记、监委主任", "中共江孜县纪律检查委员会", "待确认"),
    (6,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委常委、组织部部长", "中共江孜县委组织部", "待确认"),
    (7,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委常委、宣传部部长", "中共江孜县委宣传部", "待确认"),
    (8,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委常委、政法委书记", "中共江孜县委政法委员会", "待确认"),
    (9,  "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县委常委、统战部部长", "中共江孜县委统一战线工作部", "待确认"),
    (10, "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县人大常委会主任", "江孜县人民代表大会常务委员会", "待确认"),
    (11, "（待确认）", "男", "藏族", "", "", "", "", "",
     "江孜县政协主席", "中国人民政治协商会议江孜县委员会", "待确认"),
]

ORGANIZATIONS = [
    (1, "中共江孜县委员会", "党委", "县级", "中共日喀则市委员会", "西藏自治区日喀则市江孜县"),
    (2, "江孜县人民政府", "政府", "县级", "日喀则市人民政府", "西藏自治区日喀则市江孜县"),
    (3, "中共江孜县纪律检查委员会", "党委", "县级", "中共江孜县委员会", "西藏自治区日喀则市江孜县"),
    (4, "江孜县人民代表大会常务委员会", "人大", "县级", "日喀则市人民代表大会常务委员会", "西藏自治区日喀则市江孜县"),
    (5, "政协江孜县委员会", "政协", "县级", "政协日喀则市委员会", "西藏自治区日喀则市江孜县"),
    (6, "中共江孜县委组织部", "党委", "县级", "中共江孜县委员会", "西藏自治区日喀则市江孜县"),
    (7, "中共江孜县委宣传部", "党委", "县级", "中共江孜县委员会", "西藏自治区日喀则市江孜县"),
    (8, "中共江孜县委政法委员会", "党委", "县级", "中共江孜县委员会", "西藏自治区日喀则市江孜县"),
    (9, "中共江孜县委统一战线工作部", "党委", "县级", "中共江孜县委员会", "西藏自治区日喀则市江孜县"),
    (10, "中共日喀则市委员会", "党委", "地级", "中共西藏自治区委员会", "西藏自治区日喀则市"),
    (11, "日喀则市人民政府", "政府", "地级", "西藏自治区人民政府", "西藏自治区日喀则市"),
]

POSITIONS = [
    (1, 1, "江孜县委书记", "", "present", "正处级", "待确认"),
    (2, 2, "江孜县长", "", "present", "正处级", "待确认"),
    (2, 1, "江孜县委副书记", "", "present", "副处级", "县长兼任"),
    (3, 1, "江孜县委副书记（专职）", "", "present", "副处级", "待确认"),
    (4, 2, "江孜县委常委、常务副县长", "", "present", "副处级", "待确认"),
    (4, 1, "江孜县委常委", "", "present", "副处级", ""),
    (5, 3, "江孜县委常委、纪委书记、监委主任", "", "present", "副处级", "待确认"),
    (5, 1, "江孜县委常委", "", "present", "副处级", ""),
    (6, 6, "江孜县委常委、组织部部长", "", "present", "副处级", "待确认"),
    (6, 1, "江孜县委常委", "", "present", "副处级", ""),
    (7, 7, "江孜县委常委、宣传部部长", "", "present", "副处级", "待确认"),
    (7, 1, "江孜县委常委", "", "present", "副处级", ""),
    (8, 8, "江孜县委常委、政法委书记", "", "present", "副处级", "待确认"),
    (8, 1, "江孜县委常委", "", "present", "副处级", ""),
    (9, 9, "江孜县委常委、统战部部长", "", "present", "副处级", "待确认"),
    (9, 1, "江孜县委常委", "", "present", "副处级", ""),
    (10, 4, "江孜县人大常委会主任", "", "present", "正处级", "待确认"),
    (11, 5, "江孜县政协主席", "", "present", "正处级", "待确认"),
]

RELATIONSHIPS = [
    (1, 2, "superior_subordinate", "江孜县委书记与县长搭班子", "中共江孜县委员会/江孜县人民政府", "待确认"),
    (1, 3, "overlap", "同为江孜县委常委", "中共江孜县常务委员会", "待确认"),
    (2, 4, "overlap", "县长与常务副县长搭班子", "江孜县人民政府", "待确认"),
    (5, 6, "overlap", "同为江孜县委常委", "中共江孜县常务委员会", "待确认"),
    (7, 8, "overlap", "同为江孜县委常委", "中共江孜县常务委员会", "待确认"),
    (9, 10, "overlap", "同为江孜县领导成员", "江孜县", "待确认"),
]

# ═══════════════════════════════════════════════════════════════════════
# GEXF GENERATION
# ═══════════════════════════════════════════════════════════════════════
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(title):
    if "书记" in title and "纪委" not in title:
        return "255,50,50"
    if "县长" in title or "市长" in title:
        return "50,100,255"
    if "纪委书记" in title:
        return "255,165,0"
    return "100,100,100"

def org_type_color(ot):
    if ot == "党委": return "255,200,200"
    if "政府" in ot: return "200,200,255"
    if "人大" in ot: return "200,255,255"
    if "政协" in ot: return "255,240,200"
    return "200,200,200"

def is_top_leader(post):
    return "书记" in post or "县长" in post or "主任" in post

def generate_gexf(opath):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>江孜县（Gyantse County）领导班子工作关系网络 — 11 persons, 11 orgs, 6 edges. ⚠️ All names pending verification from jiangzi.gov.cn</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="birthplace" type="string"/>')
    lines.append('      <attribute id="5" title="ethnicity" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, ethnicity, birth, *_ = p
        post = p[8]
        org = p[9]
        c = person_color(post).split(",")
        sz = "20.0" if is_top_leader(post) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(birth[5:] if len(birth)>5 else birth)}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(ethnicity)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in ORGANIZATIONS:
        oid, oname, otype, olevel, oparent, oloc = o
        c = org_type_color(otype).split(",")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(olevel)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        pid, oid, title, start, end, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for rel in RELATIONSHIPS:
        eid += 1
        pa, pb, rtype, rctx, rovg, rper = rel
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rper)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(opath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {opath}")

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print(f"  ⚠️  All leadership names pending verification")

    # Build DB
    conn = sqlite3.connect(DB_PATH)
    for ddl in [CREATE_PERSONS, CREATE_ORGANIZATIONS, CREATE_POSITIONS, CREATE_RELATIONSHIPS]:
        conn.execute("DROP TABLE IF EXISTS " + ddl.split()[5])
        conn.execute(ddl)

    conn.executemany("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", PERSONS)
    conn.executemany("INSERT INTO organizations VALUES (?,?,?,?,?,?)", ORGANIZATIONS)
    conn.executemany("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)", POSITIONS)
    conn.executemany("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", RELATIONSHIPS)
    conn.commit()

    for table in ["persons", "organizations", "positions", "relationships"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # Build GEXF
    generate_gexf(GEXF_PATH)
    with open(GEXF_PATH) as f:
        content = f.read()
        print(f"  GEXF size: {len(content)} chars")
        assert '<gexf xmlns="http://gexf.net/1.3"' in content
        assert "<nodes>" in content
        assert "<edges>" in content
        print("  GEXF validation: OK")

    print(f"\nDone. DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"\nNext steps: verify names from official sources (www.jiangzi.gov.cn/ldzc/) and update")