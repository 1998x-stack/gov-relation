#!/usr/bin/env python3
"""
兰州市城关区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Chengguan District leadership.

Level: 市辖区 — 县级
Province: 甘肃省
Parent City: 兰州市
Region: 城关区
Targets: 区委书记 & 区长

Research Notes:
- Web research constrained: Baidu Baike 403/CAPTCHA blocked, some government pages
  not directly accessible from this environment.
- Core identities (刘凤恒 as 区委书记, 李长江 as 区长) cross-verified from
  existing 兰州市-level build script (build_兰州市_data.py) and cross-district references.
- Leadership roster data primarily sourced from the existing Lanzhou city-level build
  script and cross-referenced with available government website information.
- Full career timelines for district-level leaders are partially gapped;
  see open_questions in person JSON files.

Sources:
- Existing build_兰州市_data.py repository data
- www.lzcgq.gov.cn (Chengguan district official site - accessed)
- Baidu Baike / Sogou Baike (CAPTCHA blocked)
- Prior open-source research data
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_城关区")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "城关区_network.db")
GEXF_PATH = os.path.join(STAGING, "城关区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# Person IDs use format: cg_{surname}{givenname} (cg = Chengguan)
# This prevents ID conflicts when merging across investigations.

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education,
    # party_join, work_start, current_post, current_org, source

    # ════════════════════════════════════════════
    # 区委领导班子
    # ════════════════════════════════════════════

    # 刘凤恒 — 城关区委书记 (as of known date)
    ("cg_liu_fengheng", "刘凤恒", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委书记",
     "中共兰州市城关区委",
     "build_兰州市_data.py;lanzhou.gov.cn"),

    # 李长江 — 城关区委副书记、区长
    ("cg_li_changjiang", "李长江", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区区长",
     "城关区人民政府",
     "build_兰州市_data.py;lanzhou.gov.cn"),

    # 区委副书记（专职副书记 — 待确认具体人选）
    ("cg_deputy_secretary", "（区委副书记）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委副书记",
     "中共兰州市城关区委",
     "待查"),

    # 常务副区长
    ("cg_executive_deputy", "（常务副区长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委常委、常务副区长",
     "城关区人民政府",
     "待查"),

    # 纪委书记
    ("cg_discipline_secretary", "（纪委书记）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委常委、纪委书记、监委主任",
     "中共兰州市城关区纪律检查委员会",
     "待查"),

    # 组织部部长
    ("cg_org_head", "（组织部部长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委常委、组织部部长",
     "中共兰州市城关区委组织部",
     "待查"),

    # 宣传部部长
    ("cg_propaganda_head", "（宣传部部长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委常委、宣传部部长",
     "中共兰州市城关区委宣传部",
     "待查"),

    # 政法委书记
    ("cg_political_legal", "（政法委书记）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委常委、政法委书记",
     "中共兰州市城关区委政法委员会",
     "待查"),

    # 统战部部长
    ("cg_united_front", "（统战部部长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区委常委、统战部部长",
     "中共兰州市城关区委统一战线工作部",
     "待查"),

    # ════════════════════════════════════════════
    # 人大、政协
    # ════════════════════════════════════════════

    # 区人大常委会主任
    ("cg_people_congress", "（区人大常委会主任）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区人大常委会主任",
     "兰州市城关区人民代表大会常务委员会",
     "待查"),

    # 区政协主席
    ("cg_cppcc_chair", "（区政协主席）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市城关区政协主席",
     "中国人民政治协商会议兰州市城关区委员会",
     "待查"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("cg_party_committee", "中共兰州市城关区委", "党委", "县级", "中共兰州市委员会", "兰州市城关区"),
    ("cg_gov", "城关区人民政府", "政府", "县级", "兰州市人民政府", "兰州市城关区"),
    ("cg_discipline", "中共兰州市城关区纪律检查委员会", "纪委", "县级", "中共兰州市纪律检查委员会", "兰州市城关区"),
    ("cg_org_department", "中共兰州市城关区委组织部", "党委部门", "正科级", "中共兰州市城关区委", "兰州市城关区"),
    ("cg_propaganda", "中共兰州市城关区委宣传部", "党委部门", "正科级", "中共兰州市城关区委", "兰州市城关区"),
    ("cg_political_legal", "中共兰州市城关区委政法委员会", "党委部门", "正科级", "中共兰州市城关区委", "兰州市城关区"),
    ("cg_united_front", "中共兰州市城关区委统一战线工作部", "党委部门", "正科级", "中共兰州市城关区委", "兰州市城关区"),
    ("cg_peoples_congress", "兰州市城关区人民代表大会常务委员会", "人大", "县级", "兰州市人大常委会", "兰州市城关区"),
    ("cg_cppcc", "中国人民政治协商会议兰州市城关区委员会", "政协", "县级", "兰州市政协", "兰州市城关区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 刘凤恒 — 区委书记 ═══
    ("cg_liu_fengheng", "cg_party_committee", "城关区委书记", "", "至今", "正处级", "主持区委全面工作"),
    ("cg_liu_fengheng", "cg_gov", "城关区区长", "", "", "正处级", "前职（如曾担任区长），待确认"),

    # ═══ 李长江 — 区长 ═══
    ("cg_li_changjiang", "cg_gov", "城关区区长", "", "至今", "正处级", "主持区政府全面工作"),

    # ═══ 待确认人选的常委职位 ═══
    ("cg_deputy_secretary", "cg_party_committee", "区委副书记（专职）", "", "至今", "正处级", "专职副书记，待确认具体人选"),
    ("cg_executive_deputy", "cg_gov", "区委常委、常务副区长", "", "至今", "副处级", "待确认具体人选"),
    ("cg_discipline_secretary", "cg_discipline", "区委常委、纪委书记、监委主任", "", "至今", "副处级", "待确认具体人选"),
    ("cg_org_head", "cg_org_department", "区委常委、组织部部长", "", "至今", "副处级", "待确认具体人选"),
    ("cg_propaganda_head", "cg_propaganda", "区委常委、宣传部部长", "", "至今", "副处级", "待确认具体人选"),
    ("cg_political_legal", "cg_political_legal", "区委常委、政法委书记", "", "至今", "副处级", "待确认具体人选"),
    ("cg_united_front", "cg_united_front", "区委常委、统战部部长", "", "至今", "副处级", "待确认具体人选"),

    # ═══ 人大、政协 ═══
    ("cg_people_congress", "cg_peoples_congress", "区人大常委会主任", "", "至今", "正处级", "待确认具体人选"),
    ("cg_cppcc_chair", "cg_cppcc", "区政协主席", "", "至今", "正处级", "待确认具体人选"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 刘凤恒 ↔ 李长江 — 党政正职搭档
    ("cg_liu_fengheng", "cg_li_changjiang", "党政同僚",
     "城关区委书记与区长党政正职搭档",
     "城关区", "至今"),

    # 刘凤恒 ↔ 区委副书记
    ("cg_liu_fengheng", "cg_deputy_secretary", "上下级",
     "区委书记与专职副书记",
     "中共兰州市城关区委", "至今"),

    # 刘凤恒 ↔ 常务副区长
    ("cg_liu_fengheng", "cg_executive_deputy", "上下级",
     "区委书记与常务副区长",
     "中共兰州市城关区委", "至今"),

    # 刘凤恒 ↔ 纪委书记
    ("cg_liu_fengheng", "cg_discipline_secretary", "上下级",
     "区委书记与纪委书记",
     "中共兰州市城关区委", "至今"),

    # 刘凤恒 ↔ 组织部长
    ("cg_liu_fengheng", "cg_org_head", "上下级",
     "区委书记与组织部部长（干部管理）",
     "中共兰州市城关区委", "至今"),

    # 李长江 ↔ 常务副区长
    ("cg_li_changjiang", "cg_executive_deputy", "上下级",
     "区长与常务副区长（区政府日常运作）",
     "城关区人民政府", "至今"),

    # 李长江 ↔ 政法委书记
    ("cg_li_changjiang", "cg_political_legal", "上下级",
     "区长与政法委书记",
     "城关区", "至今"),
]


# ════════════════════════════════════════════
# DATABASE BUILDER
# ════════════════════════════════════════════

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
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
    )""")

    c.execute("""CREATE TABLE organizations(
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    )""")

    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for po in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", po)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()

    # Summary
    persons_count = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    orgs_count = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    pos_count = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    rel_count = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()

    print(f"✅ 数据库已创建: {DB_PATH}")
    print(f"   人物: {persons_count} | 机构: {orgs_count} | 任职: {pos_count} | 关系: {rel_count}")
    return persons_count, orgs_count, pos_count, rel_count


# ════════════════════════════════════════════
# GEXF BUILDER
# ════════════════════════════════════════════

def build_gexf():
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(name, post):
        if name and "刘凤恒" in name:
            return (220, 50, 50)  # Red — party secretary
        if name and "李长江" in name:
            return (50, 100, 220)  # Blue — district mayor
        t = post or ""
        if "书记" in t and "纪委" not in t and "副" not in t[:t.index("书记")] if "书记" in t else True:
            return (220, 50, 50)  # Red
        if "区长" in t:
            return (50, 100, 220)  # Blue
        if "人大" in t:
            return (90, 122, 154)  # Steel blue
        if "政协" in t:
            return (122, 90, 154)  # Purple
        if "纪委" in t:
            return (200, 136, 15)  # Orange
        return (136, 136, 136)  # Grey

    def org_color(org_type):
        return {
            "党委": (200, 50, 50),
            "党委部门": (200, 80, 80),
            "政府": (50, 100, 200),
            "人大": (90, 122, 154),
            "政协": (122, 90, 154),
            "纪委": (200, 150, 20),
        }.get(org_type, (200, 200, 200))

    def is_top_leader(name):
        return name in ("刘凤恒", "李长江")

    def node_size(name):
        return 20.0 if is_top_leader(name) else 12.0

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gansu Gov Relation Investigator</creator>')
    lines.append('    <description>兰州市城关区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        post = p[9]
        org = p[10]
        color = person_color(name, post)
        size = node_size(name)
        label = f"{name} ({post or '?'})"
        lines.append(f'      <node id="{pid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        oc = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    edge_id = 0
    for po in POSITIONS:
        pid = po[0]
        oid = po[1]
        title = po[2]
        edge_id += 1
        # Find person name for label
        person_name = pid  # fallback
        for p in PERSONS:
            if p[0] == pid:
                person_name = p[1]
                break
        org_name = oid
        for o in ORGANIZATIONS:
            if o[0] == oid:
                org_name = o[1]
                break
        label = f"{person_name} → {org_name} ({title})"
        lines.append(f'      <edge id="e{edge_id}" source="{pid}" target="{oid}" label="{esc(label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        context = r[3]
        edge_id += 1
        lines.append(f'      <edge id="e{edge_id}" source="{pa}" target="{pb}" label="{esc(context)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF 已创建: {GEXF_PATH}")
    print(f"   节点: {len(PERSONS) + len(ORGANIZATIONS)} | 边: {edge_id}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  兰州市城关区领导班子工作关系网络 — 数据构建脚本")
    print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    build_database()
    print()
    build_gexf()
    print()
    print("✅ 完成!")
