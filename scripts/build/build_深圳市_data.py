#!/usr/bin/env python3
"""
深圳市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Shenzhen City leadership network.

Level: 地级市 (副省级城市)
Province: 广东省
Region: 深圳市
Targets: 市委书记 & 市长

Research Sources:
- Wikipedia — 靳磊, 覃伟中, 孟凡利, 陈如桂
- 深圳市人民政府官网 — 领导之窗
- 新华网 — 任免公告
- 人民网 — 地方领导资料库

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "深圳市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "深圳市_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "靳磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "河南济源",
        "native_place": "河南济源",
        "education": "大学(武汉大学政治学系行政管理专业)/经济学硕士(厦门大学财金系金融学)",
        "party_join": "中共党员(1999年10月加入)",
        "work_start": "1992年7月",
        "current_post": "广东省委常委、深圳市委书记",
        "current_org": "中共深圳市委员会",
        "source": "Wikipedia: 靳磊; 新华网: 任深圳市委书记报道; 人民网: 靳磊简历",
        "person_id": "shenzhen_jin_lei"
    },
    {
        "id": "p02",
        "name": "覃伟中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "吉林吉林市",
        "native_place": "广西玉林",
        "education": "清华大学化学工程系高分子化工/自动化双学士、高分子材料硕士、在职工学博士",
        "party_join": "中共党员(2001年加入)",
        "work_start": "1996年7月",
        "current_post": "深圳市委副书记、市长",
        "current_org": "深圳市人民政府",
        "source": "Wikipedia: 覃伟中; 深圳新闻网; 中国经济网",
        "person_id": "shenzhen_qin_weizhong"
    },
    # ════════════════════════════════════════
    # Key Deputies (市委常委 / 副市长)
    # ════════════════════════════════════════
    # Note: Shenzhen deputy leadership changes frequently.
    # The following are sourced from public records.
    {
        "id": "p03",
        "name": "戴运龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "湖北黄梅",
        "native_place": "湖北黄梅",
        "education": "大学(中南财经大学)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "深圳市人大常委会主任",
        "current_org": "深圳市人民代表大会常务委员会",
        "source": "Wikipedia: 戴运龙",
        "person_id": "shenzhen_dai_yunlong"
    },
    {
        "id": "p04",
        "name": "林洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1964年",
        "birthplace": "广东英德",
        "native_place": "广东英德",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "深圳市政协主席",
        "current_org": "中国人民政治协商会议深圳市委员会",
        "source": "Wikipedia: 林洁",
        "person_id": "shenzhen_lin_jie"
    },
    # ════════════════════════════════════════
    # Predecessors (for context)
    # ════════════════════════════════════════
    {
        "id": "p05",
        "name": "孟凡利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年9月",
        "birthplace": "山东临沂",
        "native_place": "山东临沂",
        "education": "山东经济学院会计学本科/南开大学会计学硕士/天津财经学院会计学博士",
        "party_join": "中共党员(1986年3月加入)",
        "work_start": "1986年7月",
        "current_post": "广东省委副书记、省长",
        "current_org": "广东省人民政府",
        "source": "Wikipedia: 孟凡利; 南方日报",
        "person_id": "shenzhen_meng_fanli"
    },
    {
        "id": "p06",
        "name": "王伟中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年3月",
        "birthplace": "山西朔州",
        "native_place": "山西朔州",
        "education": "清华大学水文水资源专业博士",
        "party_join": "中共党员(1983年10月加入)",
        "work_start": "1979年9月",
        "current_post": "中央组织部副部长",
        "current_org": "中共中央组织部",
        "source": "Wikipedia: 王伟中",
        "person_id": "shenzhen_wang_weizhong"
    },
    {
        "id": "p07",
        "name": "陈如桂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年9月",
        "birthplace": "广东廉江",
        "native_place": "广东廉江",
        "education": "中南工业大学工学博士",
        "party_join": "中共党员(1986年4月加入)",
        "work_start": "1983年8月",
        "current_post": "被调查(原深圳市市长、广东省人大常委会副主任)",
        "current_org": "",
        "source": "Wikipedia: 陈如桂; 中央纪委国家监委网站",
        "person_id": "shenzhen_chen_rugui"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共深圳市委员会", "type": "党委", "level": "副省级", "parent": "中共广东省委员会", "location": "深圳市福田区"},
    {"id": 2, "name": "深圳市人民政府", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "深圳市福田区"},
    {"id": 3, "name": "深圳市人民代表大会常务委员会", "type": "人大", "level": "副省级", "parent": "", "location": "深圳市福田区"},
    {"id": 4, "name": "中国人民政治协商会议深圳市委员会", "type": "政协", "level": "副省级", "parent": "", "location": "深圳市福田区"},
    {"id": 5, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广州市"},
    {"id": 6, "name": "中共广东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "广州市"},
    {"id": 7, "name": "中共四川省委组织部", "type": "党委", "level": "省级", "parent": "中共四川省委员会", "location": "成都市"},
    {"id": 8, "name": "中共德阳市委员会", "type": "党委", "level": "地级", "parent": "中共四川省委员会", "location": "德阳市"},
    {"id": 9, "name": "安阳市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "安阳市"},
    {"id": 10, "name": "山东省鲁信投资控股集团有限公司", "type": "事业单位", "level": "省属", "parent": "山东省人民政府", "location": "济南市"},
    {"id": 11, "name": "烟台市人民政府", "type": "政府", "level": "地级", "parent": "山东省人民政府", "location": "烟台市"},
    {"id": 12, "name": "青岛市人民政府", "type": "政府", "level": "副省级", "parent": "山东省人民政府", "location": "青岛市"},
    {"id": 13, "name": "中共包头市委员会", "type": "党委", "level": "地级", "parent": "中共内蒙古自治区委员会", "location": "包头市"},
    {"id": 14, "name": "中国石油天然气集团公司", "type": "事业单位", "level": "央企", "parent": "", "location": "北京市"},
    {"id": 15, "name": "中国石化九江石油化工总厂", "type": "事业单位", "level": "央企下属", "parent": "中石化", "location": "九江市"},
    {"id": 16, "name": "中共郑州市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "郑州市"},
    {"id": 17, "name": "中共周口市委组织部", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "周口市"},
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # Current positions
    ("p01", 1, "广东省委常委、深圳市委书记", "2026-03", "至今", "副省级", "2026年3月从四川调任广东"),
    ("p01", 7, "四川省委组织部部长", "2025-01", "2026-03", "副省级", ""),
    ("p01", 8, "德阳市委书记", "2019-12", "2022-07", "正厅级", ""),
    ("p01", 9, "安阳市市长", "2018-09", "2019-12", "正厅级", ""),
    ("p01", 16, "郑州市委副书记、秘书长", "2016-09", "2018-09", "副厅级", ""),
    ("p01", 17, "周口市委常委、组织部部长", "2015-04", "2016-09", "副厅级", ""),
    ("p02", 2, "深圳市委副书记、市长", "2021-04", "至今", "副省级", "第二十届中央候补委员"),
    ("p02", 5, "广东省副省长", "2019-03", "2021-04", "副省级", ""),
    ("p02", 14, "中国石油天然气集团公司副总经理", "2017-03", "2019-03", "副部级央企", ""),
    ("p02", 15, "九江石化总厂厂长、党委副书记", "2010-07", "2017-03", "正厅级央企", ""),
    ("p03", 3, "深圳市人大常委会主任", "2024", "至今", "副省级", ""),
    ("p04", 4, "深圳市政协主席", "2021", "至今", "副省级", ""),
    ("p05", 5, "广东省委副书记、省长", "2025-10", "至今", "正省级", ""),
    ("p05", 6, "广东省委副书记、深圳市委书记", "2022-04", "2026-03", "副省级", ""),
    ("p05", 1, "深圳市委书记", "2022-04", "2026-03", "副省级", ""),
    ("p05", 13, "包头市委书记", "2020-09", "2022-04", "正厅级", ""),
    ("p05", 12, "青岛市市长", "2017-03", "2020-09", "副省级", ""),
    ("p05", 11, "烟台市市长", "2013-08", "2015-05", "正厅级", ""),
    ("p06", 1, "深圳市委书记", "2017", "2022-04", "副省级", ""),
    ("p06", 5, "广东省省长", "2022", "2025-10", "正省级", ""),
    ("p07", 2, "深圳市市长", "2017-08", "2021-04", "副省级", "2022年6月被调查"),
]

# 4. Relationships
relationships = [
    # 靳磊 ↔ 覃伟中: Current top leadership team
    ("p01", "p02", "共事", "市委书记—市长搭档", "中共深圳市委员会/深圳市人民政府", "2026-03至今"),
    # 孟凡利 ↔ 覃伟中: Former secretary-mayor partnership
    ("p05", "p02", "共事", "前任市委书记—市长搭档", "中共深圳市委员会/深圳市人民政府", "2022-04~2026-03"),
    # 王伟中 ↔ 覃伟中: Predecessor relationship
    ("p06", "p02", "前继", "王伟中曾任深圳市委书记，覃伟中继任市长", "中共深圳市委员会", "2017~2021"),
    # 陈如桂 ↔ 覃伟中: Predecessor-successor as mayor
    ("p07", "p02", "前后任", "陈如桂卸任市长，覃伟中接任", "深圳市人民政府", "2021"),
    # 孟凡利 ↔ 王伟中: Predecessor-successor as Shenzhen secretary
    ("p05", "p06", "前后任", "王伟中调任广东省长，孟凡利接任深圳市委书记", "中共深圳市委员会", "2022"),
    # 靳磊 ↔ 孟凡利: Predecessor-successor as Shenzhen secretary
    ("p01", "p05", "前后任", "孟凡利不再兼任深圳市委书记，靳磊接任", "中共深圳市委员会", "2026-03"),
    # 王伟中 ↔ 孟凡利: Guangdong governor succession
    ("p06", "p05", "前后任", "王伟中卸任广东省长，孟凡利接任", "广东省人民政府", "2025-10"),
    # 覃伟中 ← 陈如桂: Mayoral corruption context
    ("p02", "p07", "前后任", "覃伟中接替被调查的陈如桂", "深圳市人民政府", "2021"),
    # 戴运龙 ↔ 林洁: Legislative leaders
    ("p03", "p04", "共事", "人大主任—政协主席", "深圳市", "2024至今"),
]

# ── Helper functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_top_leader(name):
    return name in ("靳磊", "覃伟中", "孟凡利", "王伟中")

def person_color(name, post):
    if "书记" in post and "副书记" not in post:
        return (255, 50, 50)  # Red - Party Secretary
    if "市长" in post or "省长" in post:
        return (50, 100, 255)  # Blue - Government leader
    if "人大" in post:
        return (200, 255, 255)  # Cyan
    if "政协" in post:
        return (255, 240, 200)  # Cream
    return (100, 100, 100)  # Grey

def org_color(org_type):
    colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "事业单位": (220, 220, 220),
    }
    return colors.get(org_type, (200, 200, 200))

# ── Build SQLite database ──

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start_date TEXT, end_date TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (int(p["id"][1:]), p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        pid = int(pos[0][1:])
        oid = pos[1]
        title = pos[2]
        start_d = pos[3]
        end_d = pos[4]
        rank = pos[5]
        note = pos[6]
        c.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (pid, oid, title, start_d, end_d, rank, note))

    # Insert relationships
    for r in relationships:
        pa = int(r[0][1:])
        pb = int(r[1][1:])
        rtype = r[2]
        ctx = r[3]
        oorg = r[4]
        oper = r[5]
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (pa, pb, rtype, ctx, oorg, oper))

    conn.commit()
    conn.close()
    print(f"  Database created: {DB_PATH}")


# ── Build GEXF graph ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>深圳市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('      <attribute id="5" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = int(p["id"][1:])
        c = person_color(p["name"], p["current_post"])
        sz = "20.0" if is_top_leader(p["name"]) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — Organizations
    for o in organizations:
        oid = o["id"]
        c = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="5" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges — Person→Organization (worked_at)
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        pid = int(pos[0][1:])
        oid = pos[1]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[2])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos[4] or "")}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos[3])}～{esc(pos[4] or "至今")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges — Person↔Person (relationship)
    for r in relationships:
        eid += 1
        pa = int(r[0][1:])
        pb = int(r[1][1:])
        rel = r[2]
        ctx = r[3]
        oorg = r[4]
        oper = r[5]
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rel)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oorg)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(oper)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF graph created: {GEXF_PATH}")


# ── Main ──

if __name__ == "__main__":
    print("Building 深圳市 network data...")
    build_db()
    build_gexf()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print("\nSummary:")
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  {table}: {count}")
    conn.close()
    print("\nDone.")
