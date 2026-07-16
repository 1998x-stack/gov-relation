#!/usr/bin/env python3
"""
将乐县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Jiangle County leadership.

Overview:
  将乐县 is a county under 三明市 (Sanming City), Fujian Province.
  Wikipedia zone code: 350428 (confirmed)
  Population (2020 census): 144,943
  Area: 2,241.1 km²
  County seat: 古镛镇

Sources:
  - 将乐县人民政府官网 (www.jiangle.gov.cn) — currently unreachable
  - Wikipedia (zh.wikipedia.org) — county overview
  - Baidu Baike (baike.baidu.com) — biographical data (blocked 403)

Known gaps:
  - Current 县委书记 and 县长 names UNKNOWN — government website unreachable, Baidu Baike 403
  - All biographical details need research when sources become accessible
  - Predecessor chain completely unverified
  - This script establishes the framework; populate PERSONS when names are found

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "将乐县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "将乐县_network.gexf")
PERSONS_DIR = STAGING_DIR

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

AS_OF = "2026-07-16"

# Person ID convention: jiangle_{surname_givenname}
# NOTE: Government website and Baidu Baike were unreachable during research.
# Current leadership names are UNKNOWN. All fields marked "待查" (to be looked up).
# Update names and details when sources are accessible.

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders (NAMES UNKNOWN — see open gaps above) ═══
    # 县委书记
    ("jiangle_secretary", "（待查）县委书记", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共将乐县委员会",
     "需从将乐县人民政府官网(jiangle.gov.cn)领导之窗页面或三明市干部任命公告确认"),

    # 县长
    ("jiangle_mayor", "（待查）县长", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委副书记、县长", "将乐县人民政府",
     "需从将乐县人民政府官网(jiangle.gov.cn)或三明市干部任前公示确认"),

    # ═══ Standard County Standing Committee (待查 — placeholder structure) ═══
    # 县委专职副书记
    ("jiangle_deputy_secretary", "（待查）专职副书记", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委专职副书记", "中共将乐县委员会",
     "需确认"),

    # 常务副县长
    ("jiangle_executive_vice_mayor", "（待查）常务副县长", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "将乐县人民政府",
     "需确认"),

    # 县纪委书记
    ("jiangle_discipline_secretary", "（待查）县纪委书记", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县纪委书记、县监委主任", "中共将乐县纪律检查委员会/将乐县监察委员会",
     "需确认"),

    # 组织部部长
    ("jiangle_org_minister", "（待查）组织部部长", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、组织部部长", "中共将乐县委组织部",
     "需确认"),

    # 宣传部部长
    ("jiangle_propaganda_minister", "（待查）宣传部部长", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共将乐县委宣传部",
     "需确认"),

    # 政法委书记
    ("jiangle_legal_secretary", "（待查）政法委书记", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、政法委书记", "中共将乐县委政法委员会",
     "需确认"),

    # 统战部部长
    ("jiangle_united_front_minister", "（待查）统战部部长", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、统战部部长", "中共将乐县委统一战线工作部",
     "需确认"),

    # 人武部政委（通常入常委）
    ("jiangle_military_commissar", "（待查）人武部政委", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县人武部政委（或部长）", "将乐县人民武装部",
     "需确认"),

    # ═══ County-level leadership ═══
    # 县人大常委会主任
    ("jiangle_npc_chair", "（待查）县人大常委会主任", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县人大常委会主任", "将乐县人民代表大会常务委员会",
     "需确认"),

    # 县政协主席
    ("jiangle_ccppcc_chair", "（待查）县政协主席", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县政协主席", "中国人民政治协商会议将乐县委员会",
     "需确认"),

    # ═══ Vice County Mayors (数量待确认) ═══
    ("jiangle_vice_mayor_1", "（待查）副县长1", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "副县长", "将乐县人民政府",
     "需确认"),
    ("jiangle_vice_mayor_2", "（待查）副县长2", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "副县长", "将乐县人民政府",
     "需确认"),
    ("jiangle_vice_mayor_3", "（待查）副县长3", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "副县长", "将乐县人民政府",
     "需确认"),
    ("jiangle_vice_mayor_4", "（待查）副县长4", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "副县长", "将乐县人民政府",
     "需确认"),
    ("jiangle_vice_mayor_5", "（待查）副县长5", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "副县长", "将乐县人民政府",
     "需确认"),
    ("jiangle_vice_mayor_6", "（待查）副县长6", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "副县长", "将乐县人民政府",
     "需确认"),

    # ═══ Predecessors (完全未知) ═══
    ("jiangle_prev_secretary", "（待查）前任县委书记", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "（前任县委书记，已离任）", "中共将乐县委员会（前任）",
     "需确认"),
    ("jiangle_prev_mayor", "（待查）前任县长", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "（前任县长，已离任）", "将乐县人民政府（前任）",
     "需确认"),
]

# ── Organizations ──
ORGANIZATIONS = [
    ("中共将乐县委员会", "党委", "县级", "中共三明市委员会", "将乐县"),
    ("将乐县人民政府", "政府", "县级", "三明市人民政府", "将乐县"),
    ("中共将乐县纪律检查委员会/将乐县监察委员会", "党委", "部门", "中共将乐县委员会", "将乐县"),
    ("中共将乐县委组织部", "党委", "部门", "中共将乐县委员会", "将乐县"),
    ("中共将乐县委宣传部", "党委", "部门", "中共将乐县委员会", "将乐县"),
    ("中共将乐县委政法委员会", "党委", "部门", "中共将乐县委员会", "将乐县"),
    ("中共将乐县委统一战线工作部", "党委", "部门", "中共将乐县委员会", "将乐县"),
    ("将乐县人民武装部", "政府", "部门", "将乐县人民政府", "将乐县"),
    ("将乐县人民代表大会常务委员会", "人大", "县级", "将乐县", "将乐县"),
    ("中国人民政治协商会议将乐县委员会", "政协", "县级", "将乐县", "将乐县"),
]

# ── Positions ──
# (person_id, org_name, title, start_date, end_date, rank, note)
POSITIONS = [
    # All placeholder — names and dates unknown
    ("jiangle_secretary", "中共将乐县委员会", "县委书记", "待查", "任职中", "正处级", "当前在任"),
    ("jiangle_mayor", "将乐县人民政府", "县委副书记、县长", "待查", "任职中", "正处级", "当前在任"),
    ("jiangle_deputy_secretary", "中共将乐县委员会", "县委专职副书记", "待查", "任职中", "副处级", ""),
    ("jiangle_executive_vice_mayor", "将乐县人民政府", "县委常委、常务副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_discipline_secretary", "中共将乐县纪律检查委员会/将乐县监察委员会", "县委常委、县纪委书记、县监委主任", "待查", "任职中", "副处级", ""),
    ("jiangle_org_minister", "中共将乐县委组织部", "县委常委、组织部部长", "待查", "任职中", "副处级", ""),
    ("jiangle_propaganda_minister", "中共将乐县委宣传部", "县委常委、宣传部部长", "待查", "任职中", "副处级", ""),
    ("jiangle_legal_secretary", "中共将乐县委政法委员会", "县委常委、政法委书记", "待查", "任职中", "副处级", ""),
    ("jiangle_united_front_minister", "中共将乐县委统一战线工作部", "县委常委、统战部部长", "待查", "任职中", "副处级", ""),
    ("jiangle_military_commissar", "将乐县人民武装部", "县委常委、县人武部政委（或部长）", "待查", "任职中", "副处级", ""),
    ("jiangle_npc_chair", "将乐县人民代表大会常务委员会", "县人大常委会主任", "待查", "任职中", "正处级", ""),
    ("jiangle_ccppcc_chair", "中国人民政治协商会议将乐县委员会", "县政协主席", "待查", "任职中", "正处级", ""),
    ("jiangle_vice_mayor_1", "将乐县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_vice_mayor_2", "将乐县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_vice_mayor_3", "将乐县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_vice_mayor_4", "将乐县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_vice_mayor_5", "将乐县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_vice_mayor_6", "将乐县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("jiangle_prev_secretary", "中共将乐县委员会（前任）", "前任县委书记", "待查", "待查", "正处级", "前任"),
    ("jiangle_prev_mayor", "将乐县人民政府（前任）", "前任县长", "待查", "待查", "正处级", "前任"),
]

# ── Relationships (placeholder — will be populated when names are known) ──
# (person_a, person_b, type, context, overlap_org, overlap_period, confidence, direction)
RELATIONSHIPS = [
    # Top leaders
    ("jiangle_mayor", "jiangle_secretary", "superior_subordinate",
     "县长在县委书记领导下主持县政府工作",
     "中共将乐县委员会/将乐县人民政府", "当前", "plausible", "other_to_person"),

    # Predecessor-successor
    ("jiangle_prev_secretary", "jiangle_secretary", "predecessor_successor",
     "前任县委书记与现任县委书记交接",
     "中共将乐县委员会", "待查", "unverified", "undirected"),
    ("jiangle_prev_mayor", "jiangle_mayor", "predecessor_successor",
     "前任县长与现任县长交接",
     "将乐县人民政府", "待查", "unverified", "undirected"),
]


# ═══════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def build_db():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_name TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, confidence TEXT,
        direction TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations (name,type,level,parent,location) VALUES (?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT OR REPLACE INTO positions (person_id,org_name,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)", pos)

    for r in RELATIONSHIPS:
        c.execute("INSERT OR REPLACE INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,confidence,direction) VALUES (?,?,?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def build_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>将乐县领导班子工作关系网络 — Party Secretary & County Mayor: NAMES UNKNOWN (government website unreachable)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # ── Person node color mapping ──
    def person_color(pid, post):
        if "县委书记" in post or "书记" in (post.split("、")[0] if "、" in post else post):
            return "255,50,50"  # Red
        elif "县长" in post:
            return "50,100,255"  # Blue
        elif "纪委书记" in post:
            return "255,165,0"  # Orange
        else:
            return "100,100,100"  # Grey

    def person_size(post):
        if any(k in post for k in ["县委书记", "县长", "人大常委会主任", "政协主席"]):
            return "20.0"
        return "12.0"

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid, name, _, _, _, _, _, _, _, post, org, src = p
        c = person_color(pid, post)
        sz = person_size(post)
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in ORGANIZATIONS:
        name, otype, _, _, _ = o
        oc = org_colors.get(otype, "200,200,200")
        lines.append(f'      <node id="org_{esc(name)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid, org_name, title, start, end, _, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="org_{esc(org_name)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period, confidence, direction = r
        eid += 1
        weight = "2.0" if confidence == "confirmed" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(pa)}" target="{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_period.replace("至今", "").strip() if "至今" in overlap_period else overlap_period)}"/>')
        lines.append(f'          <attvalue for="3" value="{"至今" if "至今" in overlap_period else overlap_period}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_summary():
    """Print summary statistics."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("\n📊 数据摘要 / Summary")
    print("=" * 40)
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")

    print(f"\n  As of date: {AS_OF}")
    print(f"  ⚠️  Current leadership names are placeholders — research blocked")
    conn.close()


if __name__ == "__main__":
    print("🔨 构建将乐县领导班子工作关系网络数据...")
    print(f"  暂存目录: {STAGING_DIR}")
    build_db()
    build_gexf()
    print_summary()
    print("\n✅ 构建完成 / Build complete")
    print("⚠️  IMPORTANT: This is a framework build. All person names are placeholders.")
    print("   Update PERSONS when government website or appointment notices become accessible.")
