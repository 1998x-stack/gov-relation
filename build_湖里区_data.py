#!/usr/bin/env python3
"""
厦门市湖里区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Huli District (湖里区) leadership.
"""

import sqlite3
import os
from datetime import datetime

# ── CONFIG ──
SLUG = "湖里区"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{SLUG}_network.db")
GEXF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{SLUG}_network.gexf")

# ── DATA ──
# Person ID convention: huli_{surname_givenname}

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # 区委书记 — NAME UNVERIFIED, marked as open gap
    ("huli_party_secretary", "（待查）", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "区委书记（待查）", "中共厦门市湖里区委员会", "open_gap"),

    # 区长 — confirmed from government website
    ("huli_xiao_feng", "肖峰", "男", "汉族", "1976年12月", "待查",
     "大学/经济学学士", "中共党员", "待查",
     "区委副书记、区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    # 常务副区长
    ("huli_he_hanfeng", "何汉峰", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "区委常委、常务副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    # 副区长
    ("huli_cai_chengguo", "蔡成果", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    ("huli_wei_xinbin", "韦信斌", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    ("huli_lv_fang", "吕方", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    ("huli_jiao_yang", "焦杨", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    ("huli_zhu_xiaoyuan", "朱校园", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    ("huli_chen_wei", "陈炜", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    ("huli_zeng_guohui", "曾国辉", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副区长", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    # 党组成员
    ("huli_lian_youren", "连友仁", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "区政府党组成员", "厦门市湖里区人民政府", "huli.gov.cn/official"),

    # 厦门市领导（上下文）
    ("xiamen_lin_tao", "林涛", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市委书记", "中共厦门市委员会", "xm.gov.cn/official"),

    ("xiamen_wu_xinkui", "吴新奎", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市委常委、秘书长", "中共厦门市委员会", "xm.gov.cn/official"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("huli_party_committee", "中共厦门市湖里区委员会", "党委", "县级", "中共厦门市委", "厦门市湖里区"),
    ("huli_gov", "厦门市湖里区人民政府", "政府", "县级", "厦门市人民政府", "厦门市湖里区"),
    ("huli_gov_party_group", "湖里区人民政府党组", "党委", "县级", "中共厦门市湖里区委员会", "厦门市湖里区"),
    ("xiamen_party_committee", "中共厦门市委员会", "党委", "副省级", "中共福建省委", "厦门市"),
    ("xiamen_gov", "厦门市人民政府", "政府", "副省级", "福建省人民政府", "厦门市"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note
    # 区长
    ("huli_xiao_feng", "huli_gov", "区长", "待查", "present", "正处级", "主持区政府全面工作"),
    ("huli_xiao_feng", "huli_gov_party_group", "区政府党组书记", "待查", "present", "正处级", ""),
    ("huli_xiao_feng", "huli_party_committee", "区委副书记", "待查", "present", "正处级", ""),

    # 常务副区长
    ("huli_he_hanfeng", "huli_gov", "常务副区长", "待查", "present", "副处级", ""),
    ("huli_he_hanfeng", "huli_party_committee", "区委常委", "待查", "present", "副处级", ""),

    # 副区长
    ("huli_cai_chengguo", "huli_gov", "副区长", "待查", "present", "副处级", ""),
    ("huli_wei_xinbin", "huli_gov", "副区长", "待查", "present", "副处级", ""),
    ("huli_lv_fang", "huli_gov", "副区长", "待查", "present", "副处级", ""),
    ("huli_jiao_yang", "huli_gov", "副区长", "待查", "present", "副处级", ""),
    ("huli_zhu_xiaoyuan", "huli_gov", "副区长", "待查", "present", "副处级", ""),
    ("huli_chen_wei", "huli_gov", "副区长", "待查", "present", "副处级", ""),
    ("huli_zeng_guohui", "huli_gov", "副区长", "待查", "present", "副处级", ""),

    # 党组成员
    ("huli_lian_youren", "huli_gov_party_group", "党组成员", "待查", "present", "副处级", ""),

    # 市领导
    ("xiamen_lin_tao", "xiamen_party_committee", "市委书记", "待查", "present", "副省级", ""),
    ("xiamen_wu_xinkui", "xiamen_party_committee", "市委常委、秘书长", "待查", "present", "正厅级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    ("huli_xiao_feng", "huli_he_hanfeng", "superior_subordinate",
     "区长与常务副区长工作搭档", "湖里区人民政府", "待查-present"),
    ("huli_xiao_feng", "xiamen_lin_tao", "superior_subordinate",
     "厦门市委书记与湖里区长上下级关系", "厦门市/湖里区", "待查-present"),
    ("huli_he_hanfeng", "huli_cai_chengguo", "overlap",
     "常务副区长与副区长共事", "湖里区人民政府", "待查-present"),
    ("huli_he_hanfeng", "huli_wei_xinbin", "overlap",
     "常务副区长与副区长共事", "湖里区人民政府", "待查-present"),
]


# ── HELPER ──
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return node color based on role."""
    post = p[8]  # current_post
    if "书记" in post and "区委" in post:
        return "255,50,50"  # Red — Party secretary
    if "区长" in post or "副区长" in post or "区长" in post:
        return "50,100,255"  # Blue — Government
    return "100,100,100"  # Grey — Others

def is_top_leader(p):
    return "区长" in p[8] and "副" not in p[8]

def org_color(org):
    org_type = org[2]
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "政府机构": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(org_type, "200,200,200")

def build_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
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
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
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
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6]))

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r[0], r[1], r[2], r[3], r[4], r[5]))

    conn.commit()
    conn.close()


def build_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>厦门市湖里区领导班子工作关系网络</description>')
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
        post = p[8]
        org_name = p[9]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org_name)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{pos[0]}" target="{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[2])} @ {esc(pos[1])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{r[0]}" target="{r[1]}" label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    print(f"Building {SLUG} network...")
    build_database()
    print(f"  ✓ Database: {DB_PATH}")
    build_gexf()
    print(f"  ✓ GEXF graph: {GEXF_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM persons")
    print(f"  Persons: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Organizations: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions")
    print(f"  Positions: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Relationships: {c.fetchone()[0]}")
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
