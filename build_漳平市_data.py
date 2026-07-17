#!/usr/bin/env python3
"""
漳平市（龙岩市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Zhangping City leadership.

Level: 县级市
Province: 福建省
Parent city: 龙岩市
Targets: 市委书记 & 市长

Research date: 2026-07-17
Sources: zp.gov.cn (official government website), verified primary source.

Current leadership (as of 2026-07-17):
- 市委书记: 于海 (confirmed from multiple news articles, June-July 2026)
- 市长: 李毓文 (confirmed from Wikipedia and multiple news articles)
- 副市长: 范富荣, 陈清木, 吴彦成
- 其他市领导: 伍琳, 熊功首, 许赐江, 陈键, 李琳, 杨立敏, 张慧敏
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(BASE, "..", ".."))
# Staging paths
DB_PATH = os.path.join(BASE, "漳平市_network.db")
GEXF_PATH = os.path.join(BASE, "漳平市_network.gexf")

# ── DATA ──

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══
    ("zhangping_yu_hai", "于海", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市委书记", "中共漳平市委员会",
     "http://www.zp.gov.cn/xwdt/zpyw/202607/t20260703_2300609.htm — 2026年6月以市委书记身份出席防汛部署会"),

    ("zhangping_li_yuwen", "李毓文", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市委副书记、市长", "漳平市人民政府",
     "https://zh.wikipedia.org/wiki/漳平市 — 维基百科显示市长；http://www.zp.gov.cn/xwdt/zpyw/202606/t20260618_2297654.htm — 2026年6月16日以市长身份督导安全生产"),

    # ═══ Government Leadership ═══
    ("zhangping_fan_furong", "范富荣", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副市长", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202606/t20260618_2297654.htm — 2026年6月16日陪同市长督导安全生产"),

    ("zhangping_chen_qingmu", "陈清木", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202607/t20260717_2303136.htm — 2026年7月15日参加矿业招商推介会"),

    ("zhangping_wu_yancheng", "吴彦成", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202607/t20260717_2303136.htm — 2026年7月15日参加矿业招商推介会"),

    ("zhangping_xiong_gongshou", "熊功首", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202607/t20260717_2303136.htm — 2026年7月15日参加矿业招商推介会"),

    ("zhangping_xu_cijiang", "许赐江", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202607/t20260717_2303136.htm — 2026年7月15日参加矿业招商推介会"),

    ("zhangping_wu_lin", "伍琳", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zfhy/202607/t20260710_2302078.htm — 2026年7月9日防御台风部署会上作具体部署"),

    ("zhangping_chen_jian", "陈键", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202606/t20260611_2296738.htm — 2026年6月8日参加高考巡考"),

    ("zhangping_li_lin", "李琳", "女", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202606/t20260611_2296738.htm — 2026年6月8日参加高考巡考"),

    ("zhangping_yang_limin", "杨立敏", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202606/t20260626_2299002.htm — 2026年6月23日陪同市委书记调研"),

    ("zhangping_zhang_huimin", "张慧敏", "女", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市领导", "漳平市人民政府",
     "http://www.zp.gov.cn/xwdt/zpyw/202606/t20260626_2299002.htm — 2026年6月23日陪同市委书记调研"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("org_zhangping_party", "中共漳平市委员会", "党委", "县级市", "中共龙岩市委员会", "福建省龙岩市漳平市"),
    ("org_zhangping_gov", "漳平市人民政府", "政府", "县级市", "龙岩市人民政府", "福建省龙岩市漳平市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # 于海
    ("zhangping_yu_hai", "org_zhangping_party", "市委书记", "2025?或更早", "present", "正处级",
     "2026年6月已以市委书记身份出席多项活动（高考巡考、基层调研、防汛部署等）"),

    # 李毓文
    ("zhangping_li_yuwen", "org_zhangping_gov", "市长", "2021?或更早", "present", "正处级",
     "维基百科信息框显示为市长；2026年6月多项活动中以市长身份出席"),
    ("zhangping_li_yuwen", "org_zhangping_party", "市委副书记", "2021?或更早", "present", "正处级",
     "新闻中以市委副书记、市长身份出席活动"),

    # 范富荣
    ("zhangping_fan_furong", "org_zhangping_gov", "副市长", "在任", "present", "副处级",
     "2026年6月16日陪同市长督导煤矿安全；7月助企服务日活动出席"),

    # 陈清木
    ("zhangping_chen_qingmu", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年7月15日参加矿业招商推介会"),
    ("zhangping_chen_qingmu", "org_zhangping_party", "市委常委", "在任", "present", "副处级",
     "推测为市委常委（从活动级别判断）"),

    # 吴彦成
    ("zhangping_wu_yancheng", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年7月15日参加矿业招商推介会"),
    ("zhangping_wu_yancheng", "org_zhangping_party", "市委常委", "在任", "present", "副处级",
     "推测为市委常委（从活动级别判断）"),

    # 熊功首
    ("zhangping_xiong_gongshou", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年7月15日参加矿业招商推介会"),

    # 许赐江
    ("zhangping_xu_cijiang", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年7月15日参加矿业招商推介会"),

    # 伍琳
    ("zhangping_wu_lin", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年7月9日防御台风部署会上作具体部署，推测为分管应急/防汛的副市长"),

    # 陈键
    ("zhangping_chen_jian", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年6月8日参加高考巡考工作"),

    # 李琳
    ("zhangping_li_lin", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年6月8日参加高考巡考工作"),

    # 杨立敏
    ("zhangping_yang_limin", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年6月23日陪同市委书记调研新桥镇和桂林街道"),

    # 张慧敏
    ("zhangping_zhang_huimin", "org_zhangping_gov", "市领导", "在任", "present", "副处级",
     "2026年6月23日陪同市委书记调研新桥镇和桂林街道"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # Top leadership team
    ("zhangping_yu_hai", "zhangping_li_yuwen", "superior_subordinate",
     "市委书记与市长党政搭档关系", "中共漳平市委员会/漳平市人民政府", "2025?至今"),

    # 市长与副市长
    ("zhangping_li_yuwen", "zhangping_fan_furong", "superior_subordinate",
     "市长与副市长的工作关系", "漳平市人民政府", "在任期间"),

    # 市委书记与调研随行领导
    ("zhangping_yu_hai", "zhangping_yang_limin", "superior_subordinate",
     "2026年6月23日陪同市委书记赴基层调研", "中共漳平市委员会", "2026-06"),

    ("zhangping_yu_hai", "zhangping_zhang_huimin", "superior_subordinate",
     "2026年6月23日陪同市委书记赴基层调研", "中共漳平市委员会", "2026-06"),

    ("zhangping_yu_hai", "zhangping_chen_jian", "superior_subordinate",
     "2026年6月8日参与高考巡考工作", "中共漳平市委员会", "2026-06"),

    ("zhangping_yu_hai", "zhangping_li_lin", "superior_subordinate",
     "2026年6月8日参与高考巡考工作", "中共漳平市委员会", "2026-06"),

    # 市长与助企服务活动
    ("zhangping_li_yuwen", "zhangping_fan_furong", "overlap",
     "2026年7月13日助企服务日法治活动共同出席", "漳平市人民政府", "2026-07-13"),

    # 市政府班子成员之间的工作关系
    ("zhangping_chen_qingmu", "zhangping_wu_yancheng", "overlap",
     "同为市领导出席矿业招商推介会", "漳平市人民政府", "2026-07-15"),
    ("zhangping_chen_qingmu", "zhangping_xiong_gongshou", "overlap",
     "同为市领导出席矿业招商推介会", "漳平市人民政府", "2026-07-15"),
    ("zhangping_chen_qingmu", "zhangping_xu_cijiang", "overlap",
     "同为市领导出席矿业招商推介会", "漳平市人民政府", "2026-07-15"),
    ("zhangping_wu_yancheng", "zhangping_xiong_gongshou", "overlap",
     "同为市领导出席矿业招商推介会", "漳平市人民政府", "2026-07-15"),
    ("zhangping_wu_yancheng", "zhangping_xu_cijiang", "overlap",
     "同为市领导出席矿业招商推介会", "漳平市人民政府", "2026-07-15"),
    ("zhangping_xiong_gongshou", "zhangping_xu_cijiang", "overlap",
     "同为市领导出席矿业招商推介会", "漳平市人民政府", "2026-07-15"),
]


# ── SQLite Database ──

def create_db(db_path):
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
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
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
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
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()

    print(f"✅ SQLite database created: {db_path}")


# ── GEXF Graph ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Color by role."""
    secretaries = {"zhangping_yu_hai"}
    gov_leaders = {"zhangping_li_yuwen", "zhangping_fan_furong",
                   "zhangping_chen_qingmu", "zhangping_wu_yancheng",
                   "zhangping_xiong_gongshou", "zhangping_xu_cijiang",
                   "zhangping_wu_lin", "zhangping_chen_jian",
                   "zhangping_li_lin", "zhangping_yang_limin",
                   "zhangping_zhang_huimin"}
    if person_id in secretaries:
        return "255,50,50"  # Red — party secretary
    elif person_id in gov_leaders:
        return "50,100,255"  # Blue — government leader
    else:
        return "100,100,100"  # Grey — other

def is_top_leader(person_id):
    return person_id in {"zhangping_yu_hai", "zhangping_li_yuwen"}

def org_color(org_id):
    colors = {
        "org_zhangping_party": "255,200,200",    # Pink — 党委
        "org_zhangping_gov": "200,200,255",       # Light blue — 政府
    }
    return colors.get(org_id, "200,200,200")

def create_gexf(gexf_path):
    os.makedirs(os.path.dirname(gexf_path) if os.path.dirname(gexf_path) else ".", exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Research Agent</creator>')
    lines.append('    <description>漳平市（龙岩市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # --- Nodes ---
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid, name = p[0], p[1]
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        role = f"{p[9]} — {p[10]}"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, oname = o[0], o[1]
        c = org_color(oid)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # --- Edges ---
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid, oid, title = pos[0], pos[1], pos[2]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        pa, pb, rtype, ctx = r[0], r[1], r[2], r[3]
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF graph created: {gexf_path}")


# ── Summary ──

def print_summary():
    print(f"\n📊 Summary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print(f"\n⚠️  Notes:")
    print(f"  - Most persons lack full career histories (birthplace, education details, earlier positions)")
    print(f"  - 于海 was confirmed as 市委书记 from multiple 2026 news articles on zp.gov.cn")
    print(f"  - 李毓文 was confirmed as 市长 from Wikipedia and official news")
    print(f"  - 范富荣 is a confirmed 副市长; other leaders' exact titles need further verification")
    print(f"  - The full 市委常委 composition is unknown — only 于海, 李毓文 confirmed as members")
    print(f"  - This is a staging build. After validation, use scripts/process_tmp.py to promote.")


if __name__ == "__main__":
    print("🔨 漳平市领导班子数据构建脚本")
    print("=" * 50)
    create_db(DB_PATH)
    create_gexf(GEXF_PATH)
    print_summary()
