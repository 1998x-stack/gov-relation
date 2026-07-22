#!/usr/bin/env python3
"""
马山县（南宁市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Mashan County leadership.

Research note: Due to geo-restrictions, DNS resolution for mashan.gov.cn failed
and Chinese search engines (Baidu, Exa) were rate-limited or blocked from this
environment. No official sources were accessible. All data is ⚠️ UNVERIFIED /
需要确认, and marked with confidence "unverified" / "待确认".

Primary sources to consult when access is restored:
  - https://www.mashan.gov.cn/ (official county portal — DNS did not resolve)
  - 南宁市人民政府门户网站 (nanning.gov.cn — accessible but leadership subpage missing)
  - Baidu Baike: 马山县
  - 南宁市委组织部任前公示
  - The Paper (thepaper.cn) and People's Daily political news sections

Last updated: 2026-07-22
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(STAGING_DIR, "..", ".."))
DB_PATH = os.path.join(STAGING_DIR, "马山县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "马山县_network.gexf")

TODAY = "2026-07-22"


# ═══════════════════════════════════════════════════════════
# DATA — ⚠️ ALL UNVERIFIED (待确认)
# ═══════════════════════════════════════════════════════════

# Person ID convention: mashan_{role_key}
# Due to complete DNS resolution failure of mashan.gov.cn, no official source
# could be accessed to confirm current officeholders' names.

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education,
    #  party_join, work_start, current_post, current_org, source)

    # ═══ TOP LEADERS (⚠️ 待确认) ═══
    ("mashan_party_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中国共产党马山县委员会",
     "⚠️ 待确认：mashan.gov.cn DNS无法解析，需从南宁市委组织部或县政府网站确认"),

    ("mashan_county_mayor", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县长", "马山县人民政府",
     "⚠️ 待确认：同上"),

    # ═══ STANDING COMMITTEE (县委常委会标准配置) ═══
    ("mashan_deputy_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记（专职）", "中国共产党马山县委员会",
     "⚠️ 待确认"),

    ("mashan_exec_vice_mayor", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "马山县人民政府",
     "⚠️ 待确认"),

    ("mashan_discipline", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县纪委书记、县监委主任", "中共马山县纪律检查委员会",
     "⚠️ 待确认"),

    ("mashan_organization", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、组织部部长", "中共马山县委组织部",
     "⚠️ 待确认"),

    ("mashan_propaganda", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共马山县委宣传部",
     "⚠️ 待确认"),

    ("mashan_legal_political", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、政法委书记", "中共马山县委政法委员会",
     "⚠️ 待确认"),

    ("mashan_united_front", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、统战部部长", "中共马山县委统战部",
     "⚠️ 待确认"),

    # ═══ COUNTY GOVERNMENT DEPUTY LEADERS ═══
    ("mashan_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "马山县人民政府",
     "⚠️ 待确认"),

    ("mashan_vice_mayor_02", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "马山县人民政府",
     "⚠️ 待确认"),

    ("mashan_vice_mayor_03", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "马山县人民政府",
     "⚠️ 待确认"),

    # ═══ OTHER KEY POSITIONS ═══
    ("mashan_military", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县人武部部长", "马山县人民武装部",
     "⚠️ 待确认"),

    ("mashan_party_secretary_general", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县委办公室主任", "中共马山县委办公室",
     "⚠️ 待确认"),

    # ═══ PEOPLE'S CONGRESS & CPPCC ═══
    ("mashan_npc_chair", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县人大常委会主任", "马山县人民代表大会常务委员会",
     "⚠️ 待确认"),

    ("mashan_cppcc_chair", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县政协主席", "中国人民政治协商会议马山县委员会",
     "⚠️ 待确认"),
]

# Person ID constants for building positions and relationships
P_PARTY_SEC = 0
P_COUNTY_MAYOR = 1
P_DEPUTY_SEC = 2
P_EXEC_VICE_MAYOR = 3
P_DISCIPLINE = 4
P_ORGANIZATION = 5
P_PROPAGANDA = 6
P_LEGAL_POLITICAL = 7
P_UNITED_FRONT = 8
P_VICE_MAYOR_01 = 9
P_VICE_MAYOR_02 = 10
P_VICE_MAYOR_03 = 11
P_MILITARY = 12
P_PARTY_SECRETARY_GENERAL = 13
P_NPC_CHAIR = 14
P_CPPCC_CHAIR = 15


ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    (1, "中国共产党马山县委员会", "党委", "县级", "中国共产党南宁市委员会", "南宁市马山县"),
    (2, "马山县人民政府", "政府", "县级", "南宁市人民政府", "南宁市马山县"),
    (3, "中共马山县纪律检查委员会", "纪律检查", "县级", "中共南宁市纪律检查委员会", "南宁市马山县"),
    (4, "中共马山县委组织部", "党委部门", "科级", "中国共产党马山县委员会", "南宁市马山县"),
    (5, "中共马山县委宣传部", "党委部门", "科级", "中国共产党马山县委员会", "南宁市马山县"),
    (6, "中共马山县委政法委员会", "党委部门", "科级", "中国共产党马山县委员会", "南宁市马山县"),
    (7, "中共马山县委统战部", "党委部门", "科级", "中国共产党马山县委员会", "南宁市马山县"),
    (8, "马山县人民武装部", "军事", "县级", "南宁警备区", "南宁市马山县"),
    (9, "中共马山县委办公室", "党委部门", "科级", "中国共产党马山县委员会", "南宁市马山县"),
    (10, "马山县人民代表大会常务委员会", "人大", "县级", "南宁市人大常委会", "南宁市马山县"),
    (11, "中国人民政治协商会议马山县委员会", "政协", "县级", "南宁市政协", "南宁市马山县"),
]

POSITIONS_TEMPLATE = [
    # (person_index, org_id, title, start, end, rank, note)
    (P_PARTY_SEC, 1, "县委书记", "待确认", "present", "正处级", "县域最高领导职务；马山县党政正职"),
    (P_COUNTY_MAYOR, 2, "县长", "待确认", "present", "正处级", "县政府主要负责人"),
    (P_DEPUTY_SEC, 1, "县委副书记（专职）", "待确认", "present", "副处级", "协助书记分管党建工作"),
    (P_EXEC_VICE_MAYOR, 2, "常务副县长", "待确认", "present", "副处级", "县政府常务工作"),
    (P_DISCIPLINE, 3, "县纪委书记、县监委主任", "待确认", "present", "副处级", "纪检监察工作"),
    (P_ORGANIZATION, 4, "组织部部长", "待确认", "present", "副处级", "干部任免与组织建设"),
    (P_PROPAGANDA, 5, "宣传部部长", "待确认", "present", "副处级", "宣传思想文化工作"),
    (P_LEGAL_POLITICAL, 6, "政法委书记", "待确认", "present", "副处级", "政法维稳工作"),
    (P_UNITED_FRONT, 7, "统战部部长", "待确认", "present", "副处级", "统一战线工作"),
    (P_VICE_MAYOR_01, 2, "副县长", "待确认", "present", "副处级", "分管领域待确认"),
    (P_VICE_MAYOR_02, 2, "副县长", "待确认", "present", "副处级", "分管领域待确认"),
    (P_VICE_MAYOR_03, 2, "副县长", "待确认", "present", "副处级", "分管领域待确认"),
    (P_MILITARY, 8, "县人武部部长", "待确认", "present", "副处级", "武装工作"),
    (P_PARTY_SECRETARY_GENERAL, 9, "县委办公室主任", "待确认", "present", "副处级", "县委日常工作运转"),
    (P_NPC_CHAIR, 10, "县人大常委会主任", "待确认", "present", "正处级", "县人大负责人"),
    (P_CPPCC_CHAIR, 11, "县政协主席", "待确认", "present", "正处级", "县政协负责人"),
]

POSITIONS = []
for pi, oi, title, start, end, rank, note in POSITIONS_TEMPLATE:
    POSITIONS.append({
        "person_id": PERSONS[pi][0],
        "org_id": oi,
        "title": title,
        "start_date": start,
        "end_date": end,
        "rank": rank,
        "note": note,
    })

# ⚠️ No confirmed relationships until names are known
# Template: party secretary ↔ county mayor (co-leadership dyad)
# Template: secretary ↔ discipline (supervision relation)
RELATIONSHIPS = []


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
    role_colors = {
        "party_sec": (255, 50, 50),         # Red — party secretary
        "county_mayor": (50, 100, 255),     # Blue — government leader
        "discipline": (255, 165, 0),        # Orange — discipline inspection
        "military": (100, 100, 100),        # Grey
        "npc": (200, 255, 255),             # Cyan — people's congress
        "cppcc": (255, 240, 200),           # Cream — political consultative
    }
    for key, color in role_colors.items():
        if key in pid:
            return f"{color[0]},{color[1]},{color[2]}"
    return "100,100,100"


def is_top_leader(pid):
    return pid in ("mashan_party_sec", "mashan_county_mayor")


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
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    for r in RELATIONSHIPS:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
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
    lines.append('    <description>马山县（南宁市）领导班子工作关系网络 — ⚠️ 数据待确认</description>')
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
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos["title"]
        lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Only add co-leadership edge if names are known
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
    print("  马山县（南宁市）领导班子网络数据构建")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("  ⚠️  所有数据待确认 — 参见脚本顶部说明")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\nDone. Next steps:")
    print("  1. Restore web access and confirm names from official sources")
    print("     - https://www.mashan.gov.cn/ (DNS failed in this environment)")
    print("     - Baidu Baike: 马山县")
    print("     - 南宁市委组织部任前公示")
    print("  2. Update PERSONS list with confirmed names and bios")
    print("  3. Add RELATIONSHIPS with overlap evidence")
    print("  4. Add career_timeline entries after biographies found")
    print("  5. Regenerate DB/GEXF to reflect confirmed data")


if __name__ == "__main__":
    main()
