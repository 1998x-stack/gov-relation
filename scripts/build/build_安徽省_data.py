#!/usr/bin/env python3
"""Build Anhui Province (安徽省) leadership network database and GEXF graph.

Output:
  DB_PATH:   ../data/database/安徽省_network.db
  GEXF_PATH: ../data/graph/安徽省_network.gexf

Targets: 省委书记 (2024.06–present), 省长 (2021.02–present)
"""

import json, os, sqlite3, subprocess, sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
DB_PATH    = os.path.join(REPO_ROOT, "data", "database", "安徽省_network.db")
GEXF_PATH  = os.path.join(REPO_ROOT, "data", "graph", "安徽省_network.gexf")
PERSONS_DIR = os.path.join(REPO_ROOT, "data", "persons")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

persons = [
    {
        "id": 1,
        "name": "梁言顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-12",
        "birthplace": "山东省泰安市",
        "native_place": "山东泰安",
        "education": "山东农业机械化学院（现山东理工大学）农业机械化专业本科（1979–1983）；辽宁大学经济学硕士（1989–1992）",
        "party_join": "1985-02",
        "work_start": "1983-07",
        "current_post": "安徽省委书记",
        "current_org": "中国共产党安徽省委员会",
        "source": "Wikipedia; 新华网; 人民网"
    },
    {
        "id": 2,
        "name": "王清宪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-07",
        "birthplace": "河北省邯郸市永年区",
        "native_place": "河北永年",
        "education": "南开大学哲学系本科（1979–1983）；中国社会科学院研究生院法学硕士（1987–1990）；中国社会科学院研究生院经济学博士（2003）",
        "party_join": "1986-08",
        "work_start": "1983-07",
        "current_post": "安徽省省长",
        "current_org": "安徽省人民政府",
        "source": "Wikipedia; 新华网; 安徽省政府官网"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中国共产党安徽省委员会",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "安徽省合肥市"
    },
    {
        "id": 2,
        "name": "安徽省人民政府",
        "type": "政府",
        "level": "省",
        "parent": None,
        "location": "安徽省合肥市"
    },
    {
        "id": 3,
        "name": "中国共产党宁夏回族自治区委员会",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "宁夏银川"
    },
    {
        "id": 4,
        "name": "中共中央党校",
        "type": "事业单位",
        "level": "部",
        "parent": None,
        "location": "北京市"
    },
    {
        "id": 5,
        "name": "中共甘肃省委宣传部",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "甘肃省兰州市"
    },
    {
        "id": 6,
        "name": "中共甘肃省委组织部",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "甘肃省兰州市"
    },
    {
        "id": 7,
        "name": "中央和国家机关工委",
        "type": "党委",
        "level": "部",
        "parent": None,
        "location": "北京市"
    },
    {
        "id": 8,
        "name": "中共中央宣传部",
        "type": "党委",
        "level": "部",
        "parent": None,
        "location": "北京市"
    },
    {
        "id": 9,
        "name": "山西省政府",
        "type": "政府",
        "level": "省",
        "parent": None,
        "location": "山西省太原市"
    },
    {
        "id": 10,
        "name": "晋城市人民政府",
        "type": "政府",
        "level": "地市",
        "parent": None,
        "location": "山西省晋城市"
    },
    {
        "id": 11,
        "name": "运城市人民政府",
        "type": "政府",
        "level": "地市",
        "parent": None,
        "location": "山西省运城市"
    },
    {
        "id": 12,
        "name": "中共吕梁市委",
        "type": "党委",
        "level": "地市",
        "parent": None,
        "location": "山西省吕梁市"
    },
    {
        "id": 13,
        "name": "中共山西省委宣传部",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "山西省太原市"
    },
    {
        "id": 14,
        "name": "中共山东省委",
        "type": "党委",
        "level": "省",
        "parent": None,
        "location": "山东省济南市"
    },
    {
        "id": 15,
        "name": "中共青岛市委",
        "type": "党委",
        "level": "副省",
        "parent": None,
        "location": "山东省青岛市"
    },
    {
        "id": 16,
        "name": "黑龙江日报社",
        "type": "事业单位",
        "level": "省",
        "parent": None,
        "location": "黑龙江省哈尔滨市"
    },
    {
        "id": 17,
        "name": "人民日报社",
        "type": "事业单位",
        "level": "部",
        "parent": None,
        "location": "北京市"
    },
]

positions = [
    # 梁言顺 positions
    {"person_id": 1, "org_id": 4,  "title": "中央党校校务委员会委员", "start": "1992-07", "end": "2016-01", "rank": "副部级", "note": ""},
    {"person_id": 1, "org_id": 5,  "title": "甘肃省委常委、宣传部部长", "start": "2016-01", "end": "2017-02", "rank": "副部级", "note": "2017-02转任组织部长"},
    {"person_id": 1, "org_id": 6,  "title": "甘肃省委常委、组织部部长", "start": "2017-02", "end": "2017-12", "rank": "副部级", "note": "任职约10个月"},
    {"person_id": 1, "org_id": 7,  "title": "中央和国家机关工委副书记", "start": "2017-12", "end": "2018-07", "rank": "副部级", "note": "分管日常工作"},
    {"person_id": 1, "org_id": 8,  "title": "中央宣传部副部长", "start": "2018-07", "end": "2020-10", "rank": "副部级", "note": ""},
    {"person_id": 1, "org_id": 7,  "title": "中央和国家机关工委分管日常工作的副书记", "start": "2020-10", "end": "2022-03", "rank": "正部级", "note": ""},
    {"person_id": 1, "org_id": 3,  "title": "宁夏回族自治区党委书记", "start": "2022-03-28", "end": "2024-06-28", "rank": "正部级", "note": ""},
    {"person_id": 1, "org_id": 1,  "title": "安徽省委书记", "start": "2024-06-28", "end": "present", "rank": "正部级", "note": "现任"},

    # 王清宪 positions
    {"person_id": 2, "org_id": 16, "title": "黑龙江日报社助理记者", "start": "1983-07", "end": "1987-09", "rank": "", "note": "毕业后分配"},
    {"person_id": 2, "org_id": 17, "title": "人民日报经济部编辑/主任记者", "start": "1990-07", "end": "2004-09", "rank": "", "note": "历任编辑、副主任编辑、主编"},
    {"person_id": 2, "org_id": 9,  "title": "山西省政府副秘书长/研究室主任", "start": "2004-09", "end": "2011-01", "rank": "正厅级", "note": "开始从政"},
    {"person_id": 2, "org_id": 10, "title": "晋城市代市长/市长", "start": "2011-01", "end": "2013-02", "rank": "正厅级", "note": "2011-04当选市长"},
    {"person_id": 2, "org_id": 11, "title": "运城市代市长/市长", "start": "2013-02", "end": "2016-05", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "吕梁市委书记", "start": "2016-05", "end": "2016-11", "rank": "正厅级", "note": "任职约6个月"},
    {"person_id": 2, "org_id": 13, "title": "山西省委宣传部部长", "start": "2016-11", "end": "2017-11", "rank": "副部级", "note": "入列省委常委"},
    {"person_id": 2, "org_id": 14, "title": "山东省委常委、宣传部部长", "start": "2017-11", "end": "2019-01", "rank": "副部级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "青岛市委书记", "start": "2019-01-29", "end": "2021-01-29", "rank": "副部级", "note": ""},
    {"person_id": 2, "org_id": 1,  "title": "安徽省委副书记、省长", "start": "2021-01", "end": "present", "rank": "正部级", "note": "2021-02-01当选省长"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "省委书记与省长党政搭档", "overlap_org": "中国共产党安徽省委员会/安徽省人民政府", "overlap_period": "2024-06至今"},
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
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
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")


# ---------------------------------------------------------------------------
# GEXF
# ---------------------------------------------------------------------------
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Red for party sec, blue for governor, grey for others."""
    if p["current_post"] == "安徽省委书记":
        return "255,50,50"
    if p["current_post"] == "安徽省省长":
        return "50,100,255"
    return "100,100,100"

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
    }
    return colors.get(o["type"], "200,200,200")

def is_top_leader(p):
    return p["current_post"] in ("安徽省委书记", "安徽省省长")

def create_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>安徽省领导关系网络 — 省委书记梁言顺、省长王清宪</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="level" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="省部级"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship), weight="2.0"
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="working_relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    create_database()
    create_gexf()
    print("Done.")

if __name__ == "__main__":
    main()
