#!/usr/bin/env python3
"""
隆安县（南宁市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Long'an County leadership.

Research note: Due to geo-restrictions and rate limits, Chinese government websites
(gxlongan.gov.cn, baike.baidu.com) and Chinese search engines were inaccessible from
this environment. All data marked with ⚠️ "待确认" requires verification from:
  - 隆安县人民政府门户网站 (longanxian.gov.cn — could not resolve)
  - 南宁市领导之窗页面
  - Baidu Baike entries for each individual
  - 南宁市委组织部任前公示

Last updated: 2026-07-22
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(STAGING_DIR, "..", ".."))
DB_PATH = os.path.join(STAGING_DIR, "隆安县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "隆安县_network.gexf")


# ═══════════════════════════════════════════════════════════
# DATA — All entries are ⚠️ UNVERIFIED / NEEDS CONFIRMATION
# ═══════════════════════════════════════════════════════════

# --- Person ID convention: longan_{surname_givenname} ---

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders (⚠️ 待确认) ═══
    ("longan_party_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共隆安县委员会",
     "⚠️ 待确认：需从隆安县政府网站或南宁市委组织部确认"),

    ("longan_county_mayor", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县长", "隆安县人民政府",
     "⚠️ 待确认：需从隆安县政府网站或南宁市委组织部确认"),

    # ═══ Standing Committee (县委常委会标配) ═══
    ("longan_deputy_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记（专职）", "中共隆安县委员会",
     "⚠️ 待确认"),

    ("longan_exec_vice_mayor", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "隆安县人民政府",
     "⚠️ 待确认"),

    ("longan_discipline", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县纪委书记、县监委主任", "中共隆安县纪律检查委员会",
     "⚠️ 待确认"),

    ("longan_organization", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、组织部部长", "中共隆安县委组织部",
     "⚠️ 待确认"),

    ("longan_propaganda", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共隆安县委宣传部",
     "⚠️ 待确认"),

    ("longan_legal_political", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、政法委书记", "中共隆安县委政法委员会",
     "⚠️ 待确认"),

    ("longan_united_front", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、统战部部长", "中共隆安县委统战部",
     "⚠️ 待确认"),

    # ═══ County Government Deputy Leaders ═══
    ("longan_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "隆安县人民政府",
     "⚠️ 待确认"),

    ("longan_vice_mayor_02", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "隆安县人民政府",
     "⚠️ 待确认"),

    ("longan_vice_mayor_03", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "隆安县人民政府",
     "⚠️ 待确认"),

    # ═══ Other Key Positions ═══
    ("longan_military", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县人武部部长", "隆安县人民武装部",
     "⚠️ 待确认"),

    ("longan_party_secretary_general", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县委办公室主任", "中共隆安县委办公室",
     "⚠️ 待确认"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    (1, "中国共产党隆安县委员会", "党委", "县级", "中国共产党南宁市委员会", "南宁市隆安县"),
    (2, "隆安县人民政府", "政府", "县级", "南宁市人民政府", "南宁市隆安县"),
    (3, "中共隆安县纪律检查委员会", "纪律检查", "县级", "中共南宁市纪律检查委员会", "南宁市隆安县"),
    (4, "中共隆安县委组织部", "党委部门", "科级", "中共隆安县委员会", "南宁市隆安县"),
    (5, "中共隆安县委宣传部", "党委部门", "科级", "中共隆安县委员会", "南宁市隆安县"),
    (6, "中共隆安县委政法委员会", "党委部门", "科级", "中共隆安县委员会", "南宁市隆安县"),
    (7, "中共隆安县委统战部", "党委部门", "科级", "中共隆安县委员会", "南宁市隆安县"),
    (8, "隆安县人民武装部", "军事", "县级", "南宁警备区", "南宁市隆安县"),
    (9, "中共隆安县委办公室", "党委部门", "科级", "中共隆安县委员会", "南宁市隆安县"),
    (10, "隆安县人大常委会", "人大", "县级", "南宁市人大常委会", "南宁市隆安县"),
    (11, "隆安县政协", "政协", "县级", "南宁市政协", "南宁市隆安县"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)
    # All positions are ⚠️ template / unverified
]

POSITIONS_TEMPLATE = [
    (0, 1, "县委书记", "待确认", "present", "正处级", "县域最高领导职务"),
    (1, 2, "县长", "待确认", "present", "正处级", "县政府主要负责人"),
    (2, 1, "县委副书记（专职）", "待确认", "present", "副处级", "协助书记分管党建工作"),
    (3, 2, "常务副县长", "待确认", "present", "副处级", "县政府常务工作"),
    (4, 3, "县纪委书记、县监委主任", "待确认", "present", "副处级", "纪检监察工作"),
    (5, 4, "组织部部长", "待确认", "present", "副处级", "干部任免与组织建设"),
    (6, 5, "宣传部部长", "待确认", "present", "副处级", "宣传思想文化工作"),
    (7, 6, "政法委书记", "待确认", "present", "副处级", "政法维稳工作"),
    (8, 7, "统战部部长", "待确认", "present", "副处级", "统一战线工作"),
    (9, 2, "副县长", "待确认", "present", "副处级", "分管领域待确认"),
    (10, 2, "副县长", "待确认", "present", "副处级", "分管领域待确认"),
    (11, 2, "副县长", "待确认", "present", "副处级", "分管领域待确认"),
    (12, 8, "县人武部部长", "待确认", "present", "副处级", "武装工作"),
    (13, 9, "县委办公室主任", "待确认", "present", "副处级", "县委日常工作运转"),
]

for i, (pi, oi, title, start, end, rank, note) in enumerate(POSITIONS_TEMPLATE):
    POSITIONS.append((i + 1, PERSONS[pi][0], oi, title, start, end, rank, note))

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)
    # All template relationships rely on position structure — strength low until confirmed
]

# Template: party secretary ↔ county mayor (co-leadership dyad)
# Template: secretary ↔ discipline (supervision relation)
# Template: secretary ↔ organization (party personnel management)


# ═══════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(pid):
    """Return 'r,g,b' for a person node based on role."""
    names_to_role = {
        "party_sec": (255, 50, 50),       # Red — party secretary
        "county_mayor": (50, 100, 255),   # Blue — government leader
        "discipline": (255, 165, 0),      # Orange — discipline
        "military": (100, 100, 100),      # Grey
    }
    for key, color in names_to_role.items():
        if key in pid:
            return f"{color[0]},{color[1]},{color[2]}"
    return "100,100,100"


def is_top_leader(pid):
    return pid in ("longan_party_sec", "longan_county_mayor")


def build_db():
    """Create SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
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
            person_id TEXT,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        cur.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            p
        )

    for o in ORGANIZATIONS:
        cur.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            o
        )

    for pos in POSITIONS:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            pos[1:]
        )

    for r in RELATIONSHIPS:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            r
        )

    conn.commit()
    conn.close()
    print(f"[OK] Database: {DB_PATH}")
    print(f"       Persons: {len(PERSONS)}, Orgs: {len(ORGANIZATIONS)}, Positions: {len(POSITIONS)}, Relationships: {len(RELATIONSHIPS)}")


def build_gexf():
    """Generate GEXF graph file using string formatting."""
    lines = []
    ts = datetime.now().strftime("%Y-%m-%d")

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{ts}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>隆安县（南宁市）领导班子工作关系网络 — ⚠️ 数据待确认</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name = p[0], p[1]
        role = p[9]
        src = p[11]
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(src)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — Organizations
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪律检查": "255,220,200",
        "党委部门": "255,230,230",
        "军事": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in ORGANIZATIONS:
        oid, oname, otype = o[0], o[1], o[2]
        oc = org_colors.get(otype, "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges — person → organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        pid = pos[1]
        oid = pos[2]
        title = pos[3]
        lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Template edges — co-leadership dyad connections (where person names are known)
    # Only add if both names differ from "（待确认）"
    if PERSONS[0][1] != "（待确认）" and PERSONS[1][1] != "（待确认）":
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(PERSONS[0][0])}" target="{esc(PERSONS[1][0])}" label="党政正职同岗" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="co_leadership"/>')
        lines.append('          <attvalue for="1" value="县委与县政府正职领导关系"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF: {GEXF_PATH}")


def main():
    print("=" * 60)
    print("  隆安县（南宁市）领导班子网络数据构建")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("  ⚠️  所有数据待确认 — 参见脚本顶部说明")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\nDone. Next steps:")
    print("  1. Confirm names and bios from official sources")
    print("  2. Update PERSONS list with confirmed data")
    print("  3. Add RELATIONSHIPS with overlap evidence")
    print("  4. Add career_timeline entries after biographies found")
    print("  5. Regenerate DB/GEXF to reflect confirmed data")


if __name__ == "__main__":
    main()
