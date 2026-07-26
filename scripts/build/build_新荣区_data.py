#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 新荣区, 大同市, 山西省."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/shanxi_新荣区")
DB_PATH = os.path.join(TMP, "新荣区_network.db")
GEXF_PATH = os.path.join(TMP, "新荣区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "刘中文", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "", "education": "大学",
     "party_join": "", "work_start": "",
     "current_post": "大同市新荣区委书记", "current_org": "中共大同市新荣区委员会",
     "source": "https://baike.baidu.com/item/%E5%88%98%E4%B8%AD%E6%96%87/19929556"},
    {"id": 2, "name": "解廷师", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "大同市新荣区委副书记、区长", "current_org": "大同市新荣区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%96%B0%E8%8D%A3%E5%8C%BA"},

    # ── Previous Leaders ──
    {"id": 3, "name": "邓志蓉", "gender": "女", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "山西省神池县", "education": "大学本科/法学硕士, 山西大学",
     "party_join": "2000-03", "work_start": "1993-07",
     "current_post": "晋城市委常委、宣传部部长（原新荣区委书记）", "current_org": "中共晋城市委员会",
     "source": "https://baike.baidu.com/item/%E9%82%93%E5%BF%97%E8%93%89"},
    {"id": 4, "name": "郭立东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原新荣区委副书记、区长", "current_org": "",
     "source": "https://www.xr.gov.cn/xrqrmzfz/tzbh/202506/a5048364bf604fe8b89820c426e5aeca.shtml"},

    # ── Leadership Roster ──
    {"id": 5, "name": "任宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区委副书记、政法委书记", "current_org": "中共大同市新荣区委员会",
     "source": "https://baike.baidu.com/item/%E4%BB%BB%E5%AE%87"},
    {"id": 6, "name": "孙利生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区委常委、副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 7, "name": "赵瑞冬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区委常委、副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 8, "name": "王超", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "新荣区副区长（挂职）", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 9, "name": "张娟娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 10, "name": "张麒", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区副区长、公安分局局长", "current_org": "大同市公安局新荣分局",
     "source": "https://www.xr.gov.cn"},
    {"id": 11, "name": "李兴宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 12, "name": "尉武华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 13, "name": "王宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 14, "name": "何伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区副区长", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
    {"id": 15, "name": "孙敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新荣区政府党组成员", "current_org": "大同市新荣区人民政府",
     "source": "https://www.xr.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共大同市新荣区委员会", "type": "党委", "level": "县处级", "parent": "中共大同市委员会",
     "location": "山西省大同市新荣区"},
    {"id": 2, "name": "大同市新荣区人民政府", "type": "政府", "level": "县处级", "parent": "大同市人民政府",
     "location": "山西省大同市新荣区"},
    {"id": 3, "name": "大同市公安局新荣分局", "type": "政府", "level": "乡科级", "parent": "大同市公安局",
     "location": "山西省大同市新荣区"},
    {"id": 4, "name": "中共晋城市委员会", "type": "党委", "level": "地厅级", "parent": "中共山西省委",
     "location": "山西省晋城市"},
    {"id": 5, "name": "大同市新荣区人大常委会", "type": "人大", "level": "县处级", "parent": "大同市人大常委会",
     "location": "山西省大同市新荣区"},
    {"id": 6, "name": "大同市新荣区政协", "type": "政协", "level": "县处级", "parent": "大同市政协",
     "location": "山西省大同市新荣区"},
]

positions = [
    # 刘中文 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "大同市新荣区委书记",
     "start_date": "2021-12", "end_date": "至今", "rank": "县处级正职",
     "note": "2021年12月山西省委组织部任前公示, 2022年1月以区委书记身份公开报道"},
    {"person_id": 1, "org_id": 1, "title": "大同市南郊区委常委",
     "start_date": "", "end_date": "", "rank": "",
     "note": "南郊区已并入云冈区"},
    {"person_id": 1, "org_id": 1, "title": "大同市委政法委常务副书记",
     "start_date": "", "end_date": "", "rank": "",
     "note": "任区委书记前的职务"},

    # 解廷师 - 区长
    {"person_id": 2, "org_id": 2, "title": "大同市新荣区委副书记、区长",
     "start_date": "2025", "end_date": "至今", "rank": "县处级正职",
     "note": "接替郭立东, 截至2025年10月维基百科记载"},

    # 邓志蓉 - 前区委书记
    {"person_id": 3, "org_id": 1, "title": "大同市新荣区委书记",
     "start_date": "2016-08", "end_date": "2021-11", "rank": "县处级正职",
     "note": ""},
    {"person_id": 3, "org_id": 4, "title": "晋城市委常委、宣传部部长",
     "start_date": "2025-09", "end_date": "至今", "rank": "地厅级副职",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "晋城市人民政府副市长",
     "start_date": "2021-11", "end_date": "2025-09", "rank": "地厅级副职",
     "note": ""},
    {"person_id": 3, "org_id": 1, "title": "高平市委副书记（挂职）",
     "start_date": "2014-03", "end_date": "2016-08", "rank": "",
     "note": ""},

    # 郭立东 - 前区长
    {"person_id": 4, "org_id": 2, "title": "大同市新荣区委副书记、区长",
     "start_date": "", "end_date": "2025", "rank": "县处级正职",
     "note": "截至2025年4月仍在任（新政办发〔2025〕21号）, 后由解廷师接替"},

    # 任宇 - 区委副书记
    {"person_id": 5, "org_id": 1, "title": "新荣区委副书记、政法委书记",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": ""},

    # 区政府领导
    {"person_id": 6, "org_id": 2, "title": "新荣区委常委、副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责财税金融住建城管应急交通"},
    {"person_id": 7, "org_id": 2, "title": "新荣区委常委、副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责自然资源行政审批招商引资经开区"},
    {"person_id": 8, "org_id": 2, "title": "新荣区副区长（挂职）",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责科技招商工信"},
    {"person_id": 9, "org_id": 2, "title": "新荣区副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责教育市场监管妇女儿童"},
    {"person_id": 10, "org_id": 3, "title": "新荣区副区长、公安分局局长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责公安司法信访"},
    {"person_id": 11, "org_id": 2, "title": "新荣区副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责农业农村水务乡村振兴"},
    {"person_id": 12, "org_id": 2, "title": "新荣区副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责卫健生态环境能源"},
    {"person_id": 13, "org_id": 2, "title": "新荣区副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责发改工业统计民政"},
    {"person_id": 14, "org_id": 2, "title": "新荣区副区长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "负责退役军人文旅广电"},
    {"person_id": 15, "org_id": 2, "title": "新荣区政府党组成员",
     "start_date": "", "end_date": "至今", "rank": "",
     "note": "负责林业人社医保"},
]

relationships = [
    # 区委书记-区长工作搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "刘中文（区委书记）与解廷师（区长）为党政正职搭档",
     "overlap_org": "新荣区", "overlap_period": "2025-至今"},
    # 区委书记-前任搭档
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "刘中文（区委书记）与郭立东（原区长）曾为党政正职搭档",
     "overlap_org": "新荣区", "overlap_period": "2022-2025"},
    # 前后任区委书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "邓志蓉是新荣区前区委书记, 刘中文接任",
     "overlap_org": "新荣区", "overlap_period": "2021-12交接"},
    # 前后任区长
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "郭立东是前区长, 解廷师接任",
     "overlap_org": "新荣区", "overlap_period": "2025交接"},
    # 区委书记-副书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "刘中文（区委书记）与任宇（区委副书记、政法委书记）为上下级",
     "overlap_org": "中共新荣区委", "overlap_period": ""},
]

# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    if "区委书记" in p["current_post"] and "原" not in p["current_post"]:
        return "255,50,50"
    if "区长" in p["current_post"] and "原" not in p["current_post"] and "政法委" not in p["current_post"]:
        return "50,100,255"
    if "政法委" in p["current_post"]:
        return "255,165,0"
    if "原" in p["current_post"]:
        return "180,180,180"
    return "100,100,100"

def is_top_leader(p):
    return p["id"] in (1, 2)

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id,org_id,title,start_date,end_date,rank,note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a,person_b,type,context,overlap_org,overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"✓ Database: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>新荣区领导班子工作关系网络 - 山西省大同市新荣区</description>')
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

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # worked_at edges (person → organization) from positions
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # relationship edges (person ↔ person)
    for r in relationships:
        eid += 1
        w = "2.0" if r["type"] in ("overlap",) else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}, Edges: {eid}")

if __name__ == "__main__":
    print(f"=== 新荣区 数据构建 ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    build_db()
    build_gexf()
    print()
    print("Done.")
