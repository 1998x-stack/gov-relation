#!/usr/bin/env python3
"""
麻山区（黑龙江省鸡西市）领导班子工作关系网络 — 2026-07-24
Build script for Mashan District, Jixi City, Heilongjiang Province.

Data sources:
- 麻山区人民政府官网 http://jiximashan.gov.cn/ — government leadership pages
- 麻山区"党建工作"新闻列表 — confirmed party secretary
- Official bio pages for each cadre member

TASK: heilongjiang_麻山区
"""

import os
import sqlite3
from datetime import datetime

TODAY = "2026-07-24"
AS_OF = TODAY
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "data", "database", "麻山区_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "麻山区_network.gexf")
PERSONS_DIR = os.path.join(REPO_ROOT, "data", "persons")

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
    if "区" in role and "长" in role and "副" not in role:
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
    return "书记" in role or ("区" in role and "长" in role and "副" not in role)


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
    # ── Party Secretary (Top Leader) ──
    ["heilongjiang_mashan_song_xuedong", "宋学东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "麻山区委书记",
     "中共鸡西市麻山区委员会",
     "微信文章确认: https://mp.weixin.qq.com/s/-28bt7JSZFcAFCoPh1ypCw (麻山区委书记宋学东主持区委常委会会议)"],

    # ── Government Leader ──
    ["heilongjiang_mashan_chen_changfa", "陈长发", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "麻山区委副书记、政府区长",
     "麻山区人民政府",
     "http://jiximashan.gov.cn/msq/408b8cd603614c1e8f32f7eed67ed27e/202405/c06_149561.shtml"],

    # ── Deputy Government Leaders ──
    ["heilongjiang_mashan_mu_xu", "慕旭", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "麻山区委常委、政府副区长",
     "麻山区人民政府",
     "http://jiximashan.gov.cn/msq/9be802ef90a24befb6b1a4beabb3a89e/202405/c06_149485.shtml"],

    ["heilongjiang_mashan_sun_yeping", "孙业清", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "麻山区委常委、政府副区长",
     "麻山区人民政府",
     "http://jiximashan.gov.cn/msq/9be802ef90a24befb6b1a4beabb3a89e/202405/c06_147397.shtml"],

    ["heilongjiang_mashan_bian_shenglei", "边胜磊", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "麻山区政府副区长",
     "麻山区人民政府",
     "http://jiximashan.gov.cn/msq/9be802ef90a24befb6b1a4beabb3a89e/202405/c06_149484.shtml"],

    ["heilongjiang_mashan_zhao_lianyou", "赵连友", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "麻山区政府副区长、公安分局局长",
     "麻山区人民政府/麻山公安分局",
     "http://jiximashan.gov.cn/msq/9be802ef90a24befb6b1a4beabb3a89e/202405/c06_146981.shtml"],

    ["heilongjiang_mashan_xing_anyu", "邢安宇", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "麻山区政府副区长",
     "麻山区人民政府",
     "http://jiximashan.gov.cn/msq/9be802ef90a24befb6b1a4beabb3a89e/202310/c06_275960.shtml"],

    ["heilongjiang_mashan_du_yu", "杜玉", "女", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "麻山区政府副区长",
     "麻山区人民政府",
     "http://jiximashan.gov.cn/msq/9be802ef90a24befb6b1a4beabb3a89e/202406/c06_298240.shtml"],
]

# ── ORGANIZATIONS ──
# [id, name, type, level, parent, location]

ORGANIZATIONS = [
    ["org_mashan_party_committee", "中共鸡西市麻山区委员会", "党委", "县处级",
     "中共鸡西市委", "黑龙江省鸡西市麻山区"],
    ["org_mashan_gov", "麻山区人民政府", "政府", "县处级",
     "鸡西市人民政府", "黑龙江省鸡西市麻山区"],
    ["org_mashan_public_security", "麻山公安分局", "政府", "乡科级",
     "麻山区人民政府/鸡西市公安局", "黑龙江省鸡西市麻山区"],
]

# ── POSITIONS ──
# [person_id, org_id, title, start, end, rank, note]

POSITIONS = [
    # 宋学东 (Party Secretary)
    ["heilongjiang_mashan_song_xuedong", "org_mashan_party_committee",
     "麻山区委书记", "待查", "present", "县处级",
     "confirmed via WeChat article 2024-04-08: 区委书记宋学东主持区委常委会"],

    # 陈长发 (Mayor)
    ["heilongjiang_mashan_chen_changfa", "org_mashan_gov",
     "麻山区政府区长", "待查", "present", "县处级",
     "confirmed via official gov bio page (2024-05)"],
    ["heilongjiang_mashan_chen_changfa", "org_mashan_party_committee",
     "麻山区委副书记", "待查", "present", "县处级", ""],

    # 慕旭 (Executive Deputy Mayor)
    ["heilongjiang_mashan_mu_xu", "org_mashan_gov",
     "麻山区委常委、政府副区长", "待查", "present", "副处级",
     "confirmed via official bio page;分管常务工作(财政、人社、发改等)"],
    ["heilongjiang_mashan_mu_xu", "org_mashan_party_committee",
     "麻山区委常委", "待查", "present", "副处级", ""],

    # 孙业清 (Deputy Mayor)
    ["heilongjiang_mashan_sun_yeping", "org_mashan_gov",
     "麻山区委常委、政府副区长", "待查", "present", "副处级",
     "confirmed via official bio page;分管安全生产、民政、市场监管等"],
    ["heilongjiang_mashan_sun_yeping", "org_mashan_party_committee",
     "麻山区委常委", "待查", "present", "副处级", ""],

    # 边胜磊 (Deputy Mayor)
    ["heilongjiang_mashan_bian_shenglei", "org_mashan_gov",
     "麻山区政府副区长", "待查", "present", "副处级",
     "confirmed via official bio page;分管住建、城管、街道等"],

    # 赵连友 (Deputy Mayor & Public Security)
    ["heilongjiang_mashan_zhao_lianyou", "org_mashan_gov",
     "麻山区政府副区长", "待查", "present", "副处级",
     "confirmed via official bio page;分管公安、司法等"],
    ["heilongjiang_mashan_zhao_lianyou", "org_mashan_public_security",
     "麻山公安分局局长", "待查", "present", "正科级", ""],

    # 邢安宇 (Deputy Mayor)
    ["heilongjiang_mashan_xing_anyu", "org_mashan_gov",
     "麻山区政府副区长", "待查", "present", "副处级",
     "confirmed via official bio page;分管农业农村、水利、乡镇等"],

    # 杜玉 (Deputy Mayor)
    ["heilongjiang_mashan_du_yu", "org_mashan_gov",
     "麻山区政府副区长", "待查", "present", "副处级",
     "confirmed via official bio page;分管教育、卫健、医保、文旅等"],
]

# ── RELATIONSHIPS ──
# [person_a, person_b, type, context, overlap_org, overlap_period, confidence]

RELATIONSHIPS = [
    ["heilongjiang_mashan_song_xuedong", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "区委书记与区长党政搭档", "中共麻山区委/麻山区政府", "待查-present", "confirmed"],
    ["heilongjiang_mashan_mu_xu", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "常委副区长协助区长分管常务工作", "麻山区政府", "待查-present", "confirmed"],
    ["heilongjiang_mashan_sun_yeping", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "常委副区长协助区长工作", "麻山区政府", "待查-present", "confirmed"],
    ["heilongjiang_mashan_zhao_lianyou", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "副区长兼公安分局局长，协助区长", "麻山区政府", "待查-present", "confirmed"],
    ["heilongjiang_mashan_bian_shenglei", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "副区长协助区长分管住建城管", "麻山区政府", "待查-present", "confirmed"],
    ["heilongjiang_mashan_xing_anyu", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "副区长协助区长分管农业农村", "麻山区政府", "待查-present", "confirmed"],
    ["heilongjiang_mashan_du_yu", "heilongjiang_mashan_chen_changfa",
     "superior_subordinate", "副区长协助区长分管教育卫生文旅", "麻山区政府", "待查-present", "confirmed"],
]


# =========================================================================
# SQLITE DATABASE
# =========================================================================

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
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
    print(f"  ✅ Database: {DB_PATH}")


# =========================================================================
# GEXF GRAPH
# =========================================================================

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>麻山区（黑龙江省鸡西市）领导班子工作关系网络</description>')
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

    # person<->person (relationship)
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

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ GEXF: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=== 麻山区 (鸡西市) 工作关系网络构建 ===")
    print(f"Date: {TODAY}")
    print()
    print("Building database...")
    build_db()
    print("Building GEXF graph...")
    build_gexf()

    # Summary
    print()
    print("Summary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print()
    print("Done.")
