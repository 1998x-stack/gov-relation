#!/usr/bin/env python3
"""当雄县（Damxung County）领导班子工作关系网络 — 构建脚本

Level: 县
Province: 西藏自治区
Parent City: 拉萨市
Region: 当雄县
Targets: 县委书记 & 县长

Research date: 2026-08-03
Sources:
- www.dangxiong.gov.cn (当雄县人民政府官方网站)
- www.dangxiong.gov.cn/ldbdj/ (县领导报道集)
- Baidu Baike 当雄县词条 — 政治 section
"""

import sqlite3, os, sys
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
SLUG = "当雄县"
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "当雄县_network.db")
GEXF_PATH = os.path.join(STAGING, "当雄县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    # ── 当前主要领导 ──
    {
        "id": 1,
        "name": "图登佩杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "当雄县委书记",
        "current_org": "中共当雄县委员会",
        "source": "dangxiong.gov.cn - 领导活动: 调研县城景观建设(2026-07-30), 八一慰问(2026-07-31), 人大闭幕讲话(2026-07-09); Baidu Baike 当雄县"
    },
    {
        "id": 2,
        "name": "胡克",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "当雄县委副书记、县长",
        "current_org": "当雄县人民政府",
        "source": "dangxiong.gov.cn - 领导活动: 主持政府工作例会(2026-08-03), 政府全体会议(2026-07-14), 防汛调研(2026-07-23)"
    },
    # ── 县四大班子主要领导 ──
    {
        "id": 3,
        "name": "巴桑次仁",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "当雄县人大常委会主任",
        "current_org": "当雄县人大常委会",
        "source": "Baidu Baike 当雄县; dangxiong.gov.cn - 人大开幕会(2026-07-07)"
    },
    {
        "id": 4,
        "name": "刘刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "当雄县政协主席",
        "current_org": "中国人民政治协商会议当雄县委员会",
        "source": "Baidu Baike 当雄县; dangxiong.gov.cn - 政协第四届一次会议(2026-07-06)"
    },
    # ── 前任县委书记 ──
    {
        "id": 5,
        "name": "姚俊亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（原当雄县委书记）",
        "current_org": "中共当雄县委员会（原）",
        "source": "dangxiong.gov.cn(2022): 走访调研巴嘎当村(2022-04-01), 县委中心组学习(2022-03-25)"
    },
    # ── 前任（2022年）副职领导 ──
    {
        "id": 6,
        "name": "宁洪海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "当雄县委常委、副县长（原）",
        "current_org": "当雄县人民政府（原）",
        "source": "dangxiong.gov.cn(2022): 陪同图登佩杰调研5100水厂(2022-03-29)"
    },
    {
        "id": 7,
        "name": "尹正岷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "当雄县委常委、副县长（原）",
        "current_org": "当雄县人民政府（原）",
        "source": "dangxiong.gov.cn(2022): 陪同调研5100水厂(2022-03-29)"
    },
]

organizations = [
    {"id": 1, "name": "中共当雄县委员会", "type": "党委", "level": "县", "parent": "中共拉萨市委员会", "location": "西藏自治区拉萨市当雄县"},
    {"id": 2, "name": "当雄县人民政府", "type": "政府", "level": "县", "parent": "拉萨市人民政府", "location": "西藏自治区拉萨市当雄县"},
    {"id": 3, "name": "当雄县人大常委会", "type": "人大", "level": "县", "parent": "拉萨市人大常委会", "location": "西藏自治区拉萨市当雄县"},
    {"id": 4, "name": "中国人民政治协商会议当雄县委员会", "type": "政协", "level": "县", "parent": "政协拉萨市委员会", "location": "西藏自治区拉萨市当雄县"},
]

positions = [
    # 图登佩杰 — 现任县委书记（原县长）
    {"person_id": 1, "org_id": 1, "title": "当雄县委书记", "start_date": "2025?", "end_date": "present", "rank": "正县级", "note": "2022年时任县长，后晋升县委书记"},
    {"person_id": 1, "org_id": 2, "title": "当雄县委副书记、县长", "start_date": "2022?", "end_date": "2025?", "rank": "正县级", "note": "2022年3月以县长身份活动"},
    # 胡克 — 现任县长
    {"person_id": 2, "org_id": 2, "title": "当雄县委副书记、县长", "start_date": "2025?", "end_date": "present", "rank": "正县级", "note": "2026年以县长身份主持政府工作"},
    # 巴桑次仁 — 人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "当雄县人大常委会主任", "start_date": "2026-07", "end_date": "present", "rank": "正县级", "note": "2026年7月县十四届人大一次会议选举产生"},
    # 刘刚 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "当雄县政协主席", "start_date": "2026-07?", "end_date": "present", "rank": "正县级", "note": "代表政协第三届常委会作工作报告(2026-07-06)"},
    # 姚俊亮 — 前任县委书记
    {"person_id": 5, "org_id": 1, "title": "当雄县委书记", "start_date": "2021?", "end_date": "2025?", "rank": "正县级", "note": "2022年3月以县委书记身份活动"},
    # 宁洪海 — 前任副职
    {"person_id": 6, "org_id": 2, "title": "当雄县委常委、副县长", "start_date": "2022?", "end_date": "unknown", "rank": "副县级", "note": "2022年3月时任职"},
    # 尹正岷 — 前任副职
    {"person_id": 7, "org_id": 2, "title": "当雄县委常委、副县长", "start_date": "2022?", "end_date": "unknown", "rank": "副县级", "note": "2022年3月时任职"},
]

relationships = [
    # 图登佩杰 ↔ 胡克（上下级关系：书记-县长搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长工作搭档", "overlap_org": "中共当雄县委员会/当雄县人民政府", "overlap_period": "2025?-present"},
    # 图登佩杰 ↔ 姚俊亮 — 前后任
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "姚俊亮卸任县委书记后由图登佩杰接任", "overlap_org": "中共当雄县委员会", "overlap_period": "2021?-2025?"},
    # 图登佩杰 ↔ 巴桑次仁 — 党政-人大关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与人大常委会主任班子协作", "overlap_org": "当雄县四大班子", "overlap_period": "2026-07-至今"},
    # 胡克 ↔ 巴桑次仁 — 政府-人大关系
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长向人大报告工作", "overlap_org": "当雄县第十四届人大一次会议", "overlap_period": "2026-07"},
    # 图登佩杰 ↔ 刘刚 — 党委-政协关系
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与政协主席班子协作", "overlap_org": "当雄县政协第四届一次会议", "overlap_period": "2026-07"},
    # 图登佩杰 ↔ 宁洪海 — 原共事关系（2022年）
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县长与县委常委副县长共事", "overlap_org": "当雄县人民政府", "overlap_period": "2022"},
    # 图登佩杰 ↔ 尹正岷 — 原共事关系（2022年）
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县长与县委常委副县长共事", "overlap_org": "当雄县人民政府", "overlap_period": "2022"},
    # 姚俊亮 ↔ 宁洪海 — 原共事关系
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "前任书记与常委副县长共事", "overlap_org": "中共当雄县委员会/当雄县人民政府", "overlap_period": "2022"},
    # 姚俊亮 ↔ 尹正岷 — 原共事关系
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "前任书记与常委副县长共事", "overlap_org": "中共当雄县委员会/当雄县人民政府", "overlap_period": "2022"},
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(post):
    if "书记" in post and "县委" in post:
        return ("255,50,50", 20.0)
    elif "县长" in post:
        return ("50,100,255", 20.0)
    elif "人大常委会主任" in post:
        return ("200,255,255", 15.0)
    elif "政协主席" in post:
        return ("255,240,200", 15.0)
    elif "常委" in post or "副县长" in post:
        return ("100,100,255", 12.0)
    else:
        return ("100,100,100", 12.0)

def org_color(typ):
    return {
        "党委": ("255,200,200"),
        "政府": ("200,200,255"),
        "人大": ("200,255,255"),
        "政协": ("255,240,200"),
    }.get(typ, ("200,200,200"))

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_db():
    conn = sqlite3.connect(DB_PATH)

    # Create tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start_date TEXT, end_date TEXT, rank TEXT, note TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT
        )
    """)

    # Insert persons
    for p in persons:
        conn.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in organizations:
        conn.execute(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")


def build_gexf():
    print("\n--- Building GEXF graph ---")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    # Person nodes
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 当雄县人民政府网站 (dangxiong.gov.cn)")
    print("=" * 60)

    build_db()
    build_gexf()

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()