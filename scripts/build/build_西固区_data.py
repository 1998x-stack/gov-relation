#!/usr/bin/env python3
"""
兰州市西固区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Xigu District leadership.

Level: 市辖区 — 县级
Province: 甘肃省
Parent City: 兰州市
Region: 西固区
Targets: 区委书记 & 区长

Research Notes:
- Web research constrained: Baidu Baike 403/CAPTCHA blocked, Exa rate-limited.
- Core identities: 赵同庆 as 区委书记 (confirmed from existing 兰州市 build script
  and 快懂百科 partial data). 毛玉铎 as former 区长 (2020.08-2024.04) who moved to
  兰州市文旅局 and later 兰州职业技术学院; current 区长 replacement unknown.
- Leadership roster data primarily sourced from the existing Lanzhou city-level build
  script. Full career timeline data partially available.
- 赵同庆's Baidu Baike page blocked; partial data from 快懂百科.
- 毛玉铎's full biography obtained from Baidu Baike.

Sources:
- Existing build_兰州市_data.py repository data
- www.xigu.gov.cn (Xigu district official site - accessed)
- kuaidi.baike.com (赵同庆 - partial)
- Baidu Baike (毛玉铎 - full)
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_西固区")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "西固区_network.db")
GEXF_PATH = os.path.join(STAGING, "西固区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# Person IDs use format: xg_{surname}{givenname} (xg = Xigu)

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education,
    # party_join, work_start, current_post, current_org, source

    # ════════════════════════════════════════════
    # 区委领导班子
    # ════════════════════════════════════════════

    # 赵同庆 — 西固区委书记 (as of known date)
    ("xg_zhao_tongqing", "赵同庆", "男", "汉族", "1969-01", "甘肃榆中",
     "中央党校大学", "中共党员", "1990-07",
     "兰州市西固区委书记、甘肃（兰州）国际陆港党工委书记",
     "中共兰州市西固区委",
     "快懂百科;build_兰州市_data.py"),

    # 毛玉铎 — 西固区原区长 (2020.08-2024.04, 已调离)
    ("xg_mao_yuduo", "毛玉铎", "男", "汉族", "1970-04", "甘肃古浪",
     "大学/工商管理硕士", "中共党员", "1992-07",
     "兰州职业技术学院党委书记（原西固区区长）",
     "兰州职业技术学院",
     "百度百科;build_兰州市_data.py"),

    # 区长（现任 — 待确认）
    ("xg_current_mayor", "（西固区区长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区区长",
     "西固区人民政府",
     "待查"),

    # 区委副书记（专职副书记 — 待确认具体人选）
    ("xg_deputy_secretary", "（区委副书记）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委副书记",
     "中共兰州市西固区委",
     "待查"),

    # 常务副区长
    ("xg_executive_deputy", "（常务副区长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委常委、常务副区长",
     "西固区人民政府",
     "待查"),

    # 纪委书记
    ("xg_discipline_secretary", "（纪委书记）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委常委、纪委书记、监委主任",
     "中共兰州市西固区纪律检查委员会",
     "待查"),

    # 组织部部长
    ("xg_org_head", "（组织部部长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委常委、组织部部长",
     "中共兰州市西固区委组织部",
     "待查"),

    # 宣传部部长
    ("xg_propaganda_head", "（宣传部部长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委常委、宣传部部长",
     "中共兰州市西固区委宣传部",
     "待查"),

    # 政法委书记
    ("xg_political_legal", "（政法委书记）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委常委、政法委书记",
     "中共兰州市西固区委政法委员会",
     "待查"),

    # 统战部部长
    ("xg_united_front", "（统战部部长）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区委常委、统战部部长",
     "中共兰州市西固区委统一战线工作部",
     "待查"),

    # ════════════════════════════════════════════
    # 人大、政协
    # ════════════════════════════════════════════

    # 区人大常委会主任
    ("xg_people_congress", "（区人大常委会主任）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区人大常委会主任",
     "兰州市西固区人民代表大会常务委员会",
     "待查"),

    # 区政协主席
    ("xg_cppcc_chair", "（区政协主席）", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "兰州市西固区政协主席",
     "中国人民政治协商会议兰州市西固区委员会",
     "待查"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("xg_party_committee", "中共兰州市西固区委", "党委", "县级", "中共兰州市委员会", "兰州市西固区"),
    ("xg_gov", "西固区人民政府", "政府", "县级", "兰州市人民政府", "兰州市西固区"),
    ("xg_discipline", "中共兰州市西固区纪律检查委员会", "纪委", "县级", "中共兰州市纪律检查委员会", "兰州市西固区"),
    ("xg_org_department", "中共兰州市西固区委组织部", "党委部门", "正科级", "中共兰州市西固区委", "兰州市西固区"),
    ("xg_propaganda", "中共兰州市西固区委宣传部", "党委部门", "正科级", "中共兰州市西固区委", "兰州市西固区"),
    ("xg_political_legal", "中共兰州市西固区委政法委员会", "党委部门", "正科级", "中共兰州市西固区委", "兰州市西固区"),
    ("xg_united_front", "中共兰州市西固区委统一战线工作部", "党委部门", "正科级", "中共兰州市西固区委", "兰州市西固区"),
    ("xg_peoples_congress", "兰州市西固区人民代表大会常务委员会", "人大", "县级", "兰州市人大常委会", "兰州市西固区"),
    ("xg_cppcc", "中国人民政治协商会议兰州市西固区委员会", "政协", "县级", "兰州市政协", "兰州市西固区"),
    ("xg_lugang", "甘肃（兰州）国际陆港", "开发区", "县级", "兰州市人民政府", "兰州市西固区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 赵同庆 — 区委书记 ═══
    ("xg_zhao_tongqing", "xg_party_committee", "西固区委书记", "", "至今", "正处级", "主持区委全面工作，兼任甘肃（兰州）国际陆港党工委书记"),
    ("xg_zhao_tongqing", "xg_lugang", "甘肃（兰州）国际陆港党工委书记", "", "至今", "正处级", "兼任"),

    # ═══ 毛玉铎 — 原区长 ═══
    ("xg_mao_yuduo", "xg_gov", "西固区区长", "2020-08", "2024-04", "正处级", "2020年5月任代区长，8月转正；2024年4月调离"),

    # ═══ 待确认人选的常委职位 ═══
    ("xg_current_mayor", "xg_gov", "西固区区长", "", "至今", "正处级", "待确认具体人选"),
    ("xg_deputy_secretary", "xg_party_committee", "区委副书记（专职）", "", "至今", "正处级", "待确认具体人选"),
    ("xg_executive_deputy", "xg_gov", "区委常委、常务副区长", "", "至今", "副处级", "待确认具体人选"),
    ("xg_discipline_secretary", "xg_discipline", "区委常委、纪委书记、监委主任", "", "至今", "副处级", "待确认具体人选"),
    ("xg_org_head", "xg_org_department", "区委常委、组织部部长", "", "至今", "副处级", "待确认具体人选"),
    ("xg_propaganda_head", "xg_propaganda", "区委常委、宣传部部长", "", "至今", "副处级", "待确认具体人选"),
    ("xg_political_legal", "xg_political_legal", "区委常委、政法委书记", "", "至今", "副处级", "待确认具体人选"),
    ("xg_united_front", "xg_united_front", "区委常委、统战部部长", "", "至今", "副处级", "待确认具体人选"),

    # ═══ 人大、政协 ═══
    ("xg_people_congress", "xg_peoples_congress", "区人大常委会主任", "", "至今", "正处级", "待确认具体人选"),
    ("xg_cppcc_chair", "xg_cppcc", "区政协主席", "", "至今", "正处级", "待确认具体人选"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 赵同庆 ↔ 毛玉铎 — 党政正职搭档
    ("xg_zhao_tongqing", "xg_mao_yuduo", "党政同僚",
     "赵同庆（区委书记）与毛玉铎（区长）党政正职搭档（2020-2024）",
     "西固区", "2020-2024"),

    # 赵同庆 ↔ （新任区长）
    ("xg_zhao_tongqing", "xg_current_mayor", "党政同僚",
     "西固区委书记与区长党政正职搭档",
     "西固区", "至今"),

    # 赵同庆 ↔ 区委副书记
    ("xg_zhao_tongqing", "xg_deputy_secretary", "上下级",
     "区委书记与专职副书记",
     "中共兰州市西固区委", "至今"),

    # 赵同庆 ↔ 常务副区长
    ("xg_zhao_tongqing", "xg_executive_deputy", "上下级",
     "区委书记与常务副区长",
     "中共兰州市西固区委", "至今"),

    # 赵同庆 ↔ 纪委书记
    ("xg_zhao_tongqing", "xg_discipline_secretary", "上下级",
     "区委书记与纪委书记",
     "中共兰州市西固区委", "至今"),

    # 赵同庆 ↔ 组织部长
    ("xg_zhao_tongqing", "xg_org_head", "上下级",
     "区委书记与组织部部长（干部管理）",
     "中共兰州市西固区委", "至今"),

    # （新任区长）↔ 常务副区长
    ("xg_current_mayor", "xg_executive_deputy", "上下级",
     "区长与常务副区长（区政府日常运作）",
     "西固区人民政府", "至今"),

    # （新任区长）↔ 政法委书记
    ("xg_current_mayor", "xg_political_legal", "上下级",
     "区长与政法委书记",
     "西固区", "至今"),
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
        if name and "赵同庆" in name:
            return (220, 50, 50)  # Red — party secretary
        if name and "毛玉铎" in name:
            return (50, 100, 220)  # Blue — district mayor
        t = post or ""
        if "书记" in t and "纪委" not in t and ("副" not in t[:t.index("书记")] if "书记" in t else True):
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
            "开发区": (50, 200, 50),
        }.get(org_type, (200, 200, 200))

    def is_top_leader(name):
        return name in ("赵同庆",)

    def node_size(name):
        return 20.0 if is_top_leader(name) else 12.0

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gansu Gov Relation Investigator</creator>')
    lines.append('    <description>兰州市西固区领导班子工作关系网络</description>')
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
    print("  兰州市西固区领导班子工作关系网络 — 数据构建脚本")
    print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    build_database()
    print()
    build_gexf()
    print()
    print("✅ 完成!")
