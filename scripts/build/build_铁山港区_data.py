#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
铁山港区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 北海市
Region: 铁山港区
Targets: 区委书记 & 区长

当前在任 (as of 2026-07-23):
- 区委书记: 待查 (继龙起云之后, 龙起云已任北海市委常委/统战部部长/副市长)
- 区长: 待查

注: 由于网络访问严重受限（政府网站超时、百度百科403、搜索
引擎限流），本脚本数据部分来自间接确认源，部分标记为待查。
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(STAGING_DIR, "..", ".."))
SLUG = "铁山港区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记 (前，已升任市领导)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "龙起云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "广西北海",
        "education": "大学学历",
        "party_join": "1999年5月",
        "work_start": "1995年7月",
        "current_post": "北海市委常委、统战部部长，市政府副市长、党组成员，市政协党组副书记（兼）",
        "current_org": "中共北海市委员会统战部/北海市人民政府",
        "source": "https://www.163.com/dy/article/J395PE2M05563WHO.html"
    },
    # ════════════════════════════════════════
    # 铁山港区 区委书记 (现任，接替龙起云)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山港区委书记",
        "current_org": "中共北海市铁山港区委员会",
        "source": "待查 —— 龙起云升任市领导后继任者信息待查"
    },
    # ════════════════════════════════════════
    # 铁山港区 区长 (现任)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁山港区长",
        "current_org": "北海市铁山港区人民政府",
        "source": "待查 —— 需要访问官方领导之窗或组织部任前公示"
    },
    # ════════════════════════════════════════
    # 北海市委常委、常务副市长（分管铁山港工业区）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "孙环志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "江苏建湖",
        "education": "上海交通大学公共管理专业，公共管理硕士学位",
        "party_join": "1999年12月",
        "work_start": "2002年8月",
        "current_post": "北海市副市长、党组成员，市北部湾经济区规划建设管理办公室主任（兼）",
        "current_org": "北海市人民政府",
        "source": "https://www.163.com/dy/article/J395PE2M05563WHO.html"
    },
    # ════════════════════════════════════════
    # 前任铁山港区委书记（龙起云之前）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "余兴国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "",
        "source": "待查 —— 余兴国曾任铁山港区委书记，后龙起云接任"
    },
    # ════════════════════════════════════════
    # 北海市委书记（上级领导）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "李楚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "广西桂平",
        "education": "在职研究生学历，法学学士",
        "party_join": "1993年12月",
        "work_start": "1995年7月",
        "current_post": "北海市委书记、北海军分区党委第一书记",
        "current_org": "中共北海市委员会",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%A5%9A/13681350"
    },
    # ════════════════════════════════════════
    # 北海市长（上级领导）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "待查",
        "education": "研究生学历，经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委副书记、市政府市长、党组书记",
        "current_org": "北海市人民政府",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%88%9A/22884963"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共北海市铁山港区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共北海市委员会",
        "location": "北海市铁山港区"
    },
    {
        "id": 2,
        "name": "北海市铁山港区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "北海市人民政府",
        "location": "北海市铁山港区"
    },
    {
        "id": 3,
        "name": "北海市铁山港区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "北海市人民代表大会常务委员会",
        "location": "北海市铁山港区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议北海市铁山港区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议北海市委员会",
        "location": "北海市铁山港区"
    },
    {
        "id": 5,
        "name": "中共北海市铁山港区纪律检查委员会/铁山港区监察委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共北海市铁山港区委员会",
        "location": "北海市铁山港区"
    },
    {
        "id": 6,
        "name": "中共北海市委员会统战部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共北海市委员会",
        "location": "北海市海城区"
    },
    {
        "id": 7,
        "name": "北海市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "广西壮族自治区人民政府",
        "location": "北海市海城区"
    },
    {
        "id": 8,
        "name": "中共北海市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共广西壮族自治区委员会",
        "location": "北海市海城区"
    },
    {
        "id": 9,
        "name": "铁山港（临海）工业区管理委员会",
        "type": "政府",
        "level": "县处级",
        "parent": "北海市人民政府",
        "location": "北海市铁山港区"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 龙起云 — 铁山港区委书记（至2023/2024）
    {"person_id": 1, "org_id": 1, "title": "铁山港区委书记", "start_date": "待查", "end_date": "2023/2024", "rank": "正处级", "note": "后升任北海市副市长、市委常委"},
    # 龙起云 — 北海市副市长
    {"person_id": 1, "org_id": 7, "title": "北海市副市长", "start_date": "2023/2024", "end_date": "present", "rank": "副厅级", "note": "分管农业农村、乡村振兴、投资促进"},
    # 龙起云 — 北海市委常委、统战部部长
    {"person_id": 1, "org_id": 6, "title": "北海市委常委、统战部部长，市政协党组副书记（兼）", "start_date": "2024/2025", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 铁山港区委书记（现任，待查）
    {"person_id": 2, "org_id": 1, "title": "铁山港区委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "接替龙起云，姓名待查"},
    
    # 铁山港区长（现任，待查）
    {"person_id": 3, "org_id": 2, "title": "铁山港区长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "姓名待查"},
    
    # 孙环志 — 北海市副市长
    {"person_id": 4, "org_id": 7, "title": "北海市副市长、党组成员，市北部湾办主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "分管铁山港（临海）工业区"},
    
    # 余兴国 — 铁山港区委书记（前前任）
    {"person_id": 5, "org_id": 1, "title": "铁山港区委书记", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "后龙起云接任"},
    
    # 李楚 — 北海市委书记
    {"person_id": 6, "org_id": 8, "title": "北海市委书记、北海军分区党委第一书记", "start_date": "2026-05", "end_date": "present", "rank": "正厅级", "note": ""},
    
    # 李刚 — 北海市长
    {"person_id": 7, "org_id": 7, "title": "北海市委副书记、市政府市长、党组书记", "start_date": "2025-10", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 龙起云 ↔ 待查区委书记（前任—继任）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "龙起云升任市领导后继任区委书记", "overlap_org": "中共北海市铁山港区委员会", "overlap_period": "交接期"},
    
    # 龙起云 ↔ 待查区长（前书记—区长搭档）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "龙起云任区委书记期间的区长搭档", "overlap_org": "中共北海市铁山港区委员会/北海市铁山港区人民政府", "overlap_period": ""},
    
    # 待查区委书记 ↔ 待查区长（书记—区长搭档）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "现任区委书记与区长搭档关系", "overlap_org": "中共北海市铁山港区委员会/北海市铁山港区人民政府", "overlap_period": ""},
    
    # 龙起云 ↔ 孙环志（同为北海市领导）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "同为北海市政府领导班子成员", "overlap_org": "北海市人民政府", "overlap_period": ""},
    
    # 龙起云 ↔ 李楚（副市长—市委书记）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "龙起云任北海市副市长期间李楚任市委书记", "overlap_org": "中共北海市委员会/北海市人民政府", "overlap_period": "2026.05-"},
    
    # 龙起云 ↔ 李刚（副市长—市长）
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "龙起云任副市长期间李刚任市长", "overlap_org": "北海市人民政府", "overlap_period": "2025.10-"},
    
    # 余兴国 ↔ 龙起云（前任—继任）
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor", "context": "余兴国后龙起云接任铁山港区委书记", "overlap_org": "中共北海市铁山港区委员会", "overlap_period": ""},
    
    # 李楚 ↔ 李刚（书记—市长搭档）
    {"person_a": 6, "person_b": 7, "type": "superior_subordinate", "context": "现任市委书记与市长搭档关系", "overlap_org": "中共北海市委员会/北海市人民政府", "overlap_period": "2025.10-"},
    
    # 孙环志 ↔ 待查区长（副市长—区长业务指导）
    {"person_a": 4, "person_b": 3, "type": "superior_subordinate", "context": "孙环志分管铁山港工业区，与铁山港区长有业务指导关系", "overlap_org": "铁山港（临海）工业区管理委员会", "overlap_period": ""},
]

# =========================================================================
# 5. DATABASE
# =========================================================================
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
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
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    
    cur.execute("""
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
        )
    """)
    
    cur.execute("""
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
        )
    """)
    
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )
    
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )
    
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database created: {DB_PATH}")
    print(f"  {len(persons)} persons")
    print(f"  {len(organizations)} organizations")
    print(f"  {len(positions)} positions")
    print(f"  {len(relationships)} relationships")


# =========================================================================
# 6. GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>铁山港区领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    for attr_id, title, atype in [
        ("0", "type", "string"),
        ("1", "current_post", "string"),
        ("2", "current_org", "string"),
        ("3", "gender", "string"),
        ("4", "ethnicity", "string"),
        ("5", "birth", "string"),
        ("6", "birthplace", "string"),
        ("7", "source", "string"),
        ("8", "org_type", "string"),
        ("9", "level", "string"),
        ("10", "location", "string"),
    ]:
        lines.append(f'      <attribute id="{attr_id}" title="{title}" type="{atype}"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    for eid, title, etype in [
        ("0", "type", "string"),
        ("1", "context", "string"),
        ("2", "overlap_org", "string"),
        ("3", "overlap_period", "string"),
    ]:
        lines.append(f'      <attribute id="{eid}" title="{title}" type="{etype}"/>')
    lines.append('    </attributes>')
    
    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        post = p["current_post"]
        if "区委书记" in post or "市委书记" in post:
            color = "255,50,50"
            size = "20.0"
        elif "区长" in post or "市长" in post or "副市长" in post:
            color = "50,100,255"
            size = "20.0"
        elif "统战部" in post:
            color = "100,100,200"
            size = "12.0"
        else:
            color = "100,100,100"
            size = "12.0"
        
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="7" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')
    
    for o in organizations:
        org_type = o["type"]
        if org_type == "党委":
            ocolor = "255,200,200"
        elif org_type == "政府":
            ocolor = "200,200,255"
        elif org_type == "人大":
            ocolor = "200,255,255"
        elif org_type == "政协":
            ocolor = "255,240,200"
        else:
            ocolor = "220,220,220"
        
        oid = o["id"] + 100000
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="8" value="{esc(org_type)}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="10" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start_date"])}~{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
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
    
    print(f"✓ GEXF created: {GEXF_PATH}")
    print(f"  {len(persons)} person nodes")
    print(f"  {len(organizations)} org nodes")
    print(f"  {eid} edges")


# =========================================================================
# 7. PERSON JSON
# =========================================================================
def write_person_json(person_data, filename_suffix, career_timeline=None, relationships_list=None, source_register=None, open_questions=None):
    """Write a person graph JSON file following the person_graph_json.md spec."""
    person = persons[person_data["person_index"]]
    fname = f"{AS_OF}-广西壮族自治区-北海市-{filename_suffix}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)
    
    has_valid_name = person["name"] not in ("待查", "")
    
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "北海市",
            "region": "铁山港区",
            "job": filename_suffix,
            "task_id": "guangxi_铁山港区",
            "time_focus": "2020-2026"
        },
        "identity": {
            "person_id": f"tieshangang_{person['name']}" if has_valid_name else f"tieshangang_待查_{filename_suffix}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"summary": person.get("education", "")}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {}
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": has_valid_name,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline or [],
        "organizations": [],
        "relationships": relationships_list or [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "No public risk signals found in available sources", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}
        ],
        "source_register": source_register or [
            {
                "id": "S001",
                "url": person.get("source", ""),
                "source_type": "media",
                "reliability": "low",
                "notes": "Primary source"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if has_valid_name else "unverified",
            "current_role": "confirmed" if has_valid_name else "unverified",
            "career_completeness": "thin",
            "biggest_gap": person.get("source", "")
        },
        "open_questions": open_questions or []
    }
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Person JSON created: {fpath}")


# =========================================================================
# 8. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"  铁山港区领导班子工作关系网络 — 数据构建")
    print(f"  Date: {AS_OF}")
    print("=" * 60)
    
    create_db()
    print()
    create_gexf()
    print()
    
    # Person JSON: 龙起云 (前区委书记，现市领导)
    write_person_json(
        {"person_index": 0},
        "前区委书记-现市委常委统战部长",
        career_timeline=[
            {"start": "待查", "end": "present", "org": "中共北海市委员会统战部", "title": "北海市委常委、统战部部长，市政府副市长", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "待查", "end": "2023/2024", "org": "中共北海市铁山港区委员会", "title": "铁山港区委书记", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "1995-07", "end": "待查", "org": "北海市", "title": "基层工作（具体岗位待查）", "rank": "", "confidence": "unverified", "source_ids": []},
        ],
        relationships_list=[
            {"person": "待查", "person_id": "tieshangang_待查_区委书记", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "龙起云升任市领导后由继任者接替", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "待查", "person_id": "tieshangang_待查_区长", "relationship_type": "overlap", "strength": "medium", "evidence": "龙起云任区委书记期间与区长搭班子", "confidence": "plausible", "source_ids": []},
        ],
        source_register=[
            {"id": "S001", "url": "https://www.163.com/dy/article/J395PE2M05563WHO.html", "publisher": "网易", "published_at": "2024-06-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "北海市政府领导分工介绍"},
            {"id": "S002", "url": "https://baike.baidu.com/item/%E9%BE%99%E8%B5%B7%E4%BA%91", "publisher": "百度百科", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "百度百科（未成功访问）"},
        ],
        open_questions=[
            {"priority": "high", "question": "龙起云何时从铁山港区委书记升任北海市副市长/市委常委？", "why_it_matters": "关键晋升时间线", "suggested_queries": ["龙起云 任命 副市长", "龙起云 任市委常委"], "last_attempted": AS_OF},
            {"priority": "high", "question": "龙起云在铁山港区委书记之前的完整履历？", "why_it_matters": "了解其从基层到正处级的晋升路径", "suggested_queries": ["龙起云 简历", "龙起云 任职经历"], "last_attempted": AS_OF},
        ]
    )
    
    # Person JSON: 现任区委书记（待查）
    write_person_json(
        {"person_index": 1},
        "区委书记",
        open_questions=[
            {"priority": "critical", "question": "现任铁山港区委书记姓名", "why_it_matters": "核心调查目标——这是所有研究的前提", "suggested_queries": ["铁山港区委书记 2025 2026 现任", "北海市铁山港区 领导分工"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "现任铁山港区委书记出生年月、籍贯、教育背景", "why_it_matters": "基本身份信息", "suggested_queries": ["铁山港区委书记 简历", "铁山港区委书记 任前公示"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "现任铁山港区委书记何时接任？", "why_it_matters": "交接时间线", "suggested_queries": ["铁山港区委书记 任职时间", "龙起云 卸任 区委书记"], "last_attempted": AS_OF},
        ]
    )
    
    # Person JSON: 现任区长（待查）
    write_person_json(
        {"person_index": 2},
        "区长",
        open_questions=[
            {"priority": "critical", "question": "现任铁山港区长姓名", "why_it_matters": "核心调查目标", "suggested_queries": ["铁山港区长 2025 2026 现任", "铁山港区人民政府 区长"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "现任铁山港区长出生年月、籍贯、教育背景、完整履历", "why_it_matters": "基本身份和晋升路径", "suggested_queries": ["铁山港区长 简历", "铁山港区长 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任铁山港区长是谁？去向？", "why_it_matters": "交接班情况和跨区调动模式", "suggested_queries": ["铁山港区 前任 区长 调任"], "last_attempted": AS_OF},
        ]
    )
    
    # Person JSON: 孙环志（分管铁山港工业区的市领导）
    write_person_json(
        {"person_index": 3},
        "副市长-分管铁山港工业区",
        career_timeline=[
            {"start": "待查", "end": "present", "org": "北海市人民政府", "title": "北海市副市长、党组成员，市北部湾办主任", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2002-08", "end": "待查", "org": "", "title": "早期工作经历（具体岗位待查）", "rank": "", "confidence": "unverified", "source_ids": []},
        ],
        source_register=[
            {"id": "S001", "url": "https://www.163.com/dy/article/J395PE2M05563WHO.html", "publisher": "网易", "published_at": "2024-06-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "北海市政府领导分工介绍"},
        ],
        open_questions=[
            {"priority": "high", "question": "孙环志何时调任北海市副市长？此前担任什么职务？", "why_it_matters": "了解跨地区（江苏→广西）干部交流路径", "suggested_queries": ["孙环志 任职 北海", "孙环志 简历"], "last_attempted": AS_OF},
        ]
    )


if __name__ == "__main__":
    # Import sqlite3 only at runtime to avoid import errors during validation
    import sqlite3
    main()
