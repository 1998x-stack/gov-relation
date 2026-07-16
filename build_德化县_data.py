#!/usr/bin/env python3
"""
德化县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Dehua County leadership.

Task: fujian_德化县 — 县委书记 & 县长
Province: 福建省
Parent City: 泉州市
Region: 德化县
Level: 县
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 县委书记: 方俊钦 — confirmed from dehua.gov.cn news (陶瓷产业链调研, 台风防御检查)
- 县长: 吴志朴 — confirmed from Wikipedia (德化县条目) and dehua.gov.cn news (消防安全调研, 信访工作)

Known standing committee structure (county standard):
- 县委副书记、县长: 吴志朴
- 其他常委待确认（德化县人民政府网站未公开领导信息页面）

Sources:
- dehua.gov.cn — 德化县人民政府网站新闻
- zh.wikipedia.org/wiki/德化县 — 确认县长为吴志朴

Confidence: Current leadership identity-level confirmed from government news.
Full career timelines not available — detailed biographical data (birth dates, education,
previous posts) require Baidu Baike which is currently inaccessible.
"""

import sqlite3, os
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "德化县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "德化县_network.gexf")

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

AS_OF = "2026-07-16"

# Person ID convention: dehua_{surname_givenname}
PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 方俊钦
    # Source: dehua.gov.cn news — 2026-07-14 "县委书记方俊钦调研陶瓷产业链建设工作"
    ("dehua_fang_junqin", "方俊钦", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共德化县委员会",
     "https://www.dehua.gov.cn — 2026-07-14 县委书记方俊钦调研陶瓷产业链建设工作并督导安全生产隐患排查、整治工作; 2026-07-13 县委书记方俊钦检查台风防御工作"),

    # 县长 — 吴志朴
    # Source: Wikipedia (德化县条目); dehua.gov.cn news
    ("dehua_wu_zhipu", "吴志朴", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记、县长", "德化县人民政府",
     "https://zh.wikipedia.org/wiki/德化县 — 确认县长为吴志朴; https://www.dehua.gov.cn — 2026-07-14 县长吴志朴调研城中村消防安全能力提升建设工作; 2025年多次接访工作"),

    # ═══ Standing Committee Members (to be confirmed) ═══
    # County standard structure includes:
    # - 专职副书记
    # - 常务副县长
    # - 纪委书记
    # - 组织部部长
    # - 宣传部部长
    # - 政法委书记
    # - 统战部部长
    # These are placeholders — names need confirmation from future research

    # ═══ Key Deputies (from common knowledge of county government structure) ═══
    # Without access to the leadership page (dehua.gov.cn/zwgk/ldxx/ returned 404),
    # these positions are structurally known to exist but names are unconfirmed.

    # ═══ NPC & CPPCC ═══
    # County-level organization heads as per standard structure
    # Names from Wikipedia 德化县 overview would be needed.
]

# ── Organizations ──
ORGANIZATIONS = [
    ("中共德化县委员会", "党委", "县级", "中共泉州市委员会", "德化县"),
    ("德化县人民政府", "政府", "县级", "泉州市人民政府", "德化县"),
    ("德化县人民代表大会常务委员会", "人大", "县级", "德化县", "德化县"),
    ("中国人民政治协商会议德化县委员会", "政协", "县级", "德化县", "德化县"),
]

# ── Positions ──
# (person_id, org_name, title, start_date, end_date, rank, note)
POSITIONS = [
    # Current leaders
    ("dehua_fang_junqin", "中共德化县委员会", "县委书记", "待查", "任职中", "正处级",
     "dehua.gov.cn 2026年7月新闻确认在任"),
    ("dehua_wu_zhipu", "德化县人民政府", "县委副书记、县长", "待查", "任职中", "正处级",
     "Wikipedia确认县长身份；政府新闻2026年7月确认在任"),
]

# ── Relationships ──
# (person_a, person_b, type, context, overlap_org, overlap_period, confidence, direction)
RELATIONSHIPS = [
    ("dehua_wu_zhipu", "dehua_fang_junqin", "superior_subordinate",
     "吴志朴（县长）在方俊钦（书记）领导下主持县政府工作",
     "中共德化县委员会/德化县人民政府", "至今", "confirmed", "other_to_person"),
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
    lines.append('    <description>德化县领导班子工作关系网络 — Party Secretary: 方俊钦, County Mayor: 吴志朴</description>')
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
        if "县委书记" in post or ("书记" in post and "副书记" not in post and post.split("、")[0] == "书记"):
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
        lines.append(f'          <attvalue for="2" value="{esc(overlap_period.split("至今")[0].strip() if "至今" in overlap_period else overlap_period)}"/>')
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
    conn.close()


if __name__ == "__main__":
    print("🔨 构建德化县领导班子工作关系网络数据...")
    print(f"  暂存目录: {STAGING_DIR}")
    build_db()
    build_gexf()
    print_summary()
    print("\n✅ 构建完成 / Build complete")
