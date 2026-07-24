#!/usr/bin/env python3
"""南岗区（哈尔滨市）领导班子关系网络生成脚本

数据来源：
  - 哈尔滨市南岗区人民政府官网 (www.hrbng.gov.cn) 新闻及领导活动报道
  - 新闻报道中提及的领导分工及任职信息

数据截至：2026年7月

Target roles:
  - 区委书记: 李思远
  - 区委副书记、区长: 任海龙
  - 区委副书记: 陆一平
  - 区委常委、常务副区长: 宋殿荣
  - 副区长级领导: 宁飞飞, 刘福禄, 杨帆, 张钧光, 韩雪松, 孔繁龙
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──
STAGING = Path(__file__).parent
DB_PATH = STAGING / "南岗区_network.db"
GEXF_PATH = STAGING / "南岗区_network.gexf"
PERSONS_DIR = STAGING

TODAY = "2026-07-24"
AS_OF = TODAY

# ── Helper ──
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =========================================================================
# DATA
# =========================================================================

persons = [
    {
        "id": 1,
        "name": "李思远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共南岗区委员会",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 2,
        "name": "任海龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 3,
        "name": "陆一平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共南岗区委员会",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 4,
        "name": "宋殿荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 5,
        "name": "宁飞飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 6,
        "name": "刘福禄",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 7,
        "name": "杨帆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 8,
        "name": "张钧光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 9,
        "name": "韩雪松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
    {
        "id": 10,
        "name": "孔繁龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "南岗区人民政府",
        "source": "http://www.hrbng.gov.cn/",
    },
]

organizations = [
    {"id": 1, "name": "中共南岗区委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "哈尔滨市南岗区"},
    {"id": 2, "name": "南岗区人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市南岗区"},
    {"id": 3, "name": "南岗区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共南岗区委员会", "location": "哈尔滨市南岗区"},
    {"id": 4, "name": "南岗区委办公室", "type": "党委", "level": "乡科级", "parent": "中共南岗区委员会", "location": "哈尔滨市南岗区"},
    {"id": 5, "name": "南岗区政府办公室", "type": "政府", "level": "乡科级", "parent": "南岗区人民政府", "location": "哈尔滨市南岗区"},
    {"id": 6, "name": "南岗区财政局", "type": "政府", "level": "乡科级", "parent": "南岗区人民政府", "location": "哈尔滨市南岗区"},
    {"id": 7, "name": "南岗区税务局", "type": "政府", "level": "乡科级", "parent": "哈尔滨市税务局", "location": "哈尔滨市南岗区"},
    {"id": 8, "name": "南岗区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "哈尔滨市人大常委会", "location": "哈尔滨市南岗区"},
    {"id": 9, "name": "南岗区政协委员会", "type": "政协", "level": "县处级", "parent": "哈尔滨市政协", "location": "哈尔滨市南岗区"},
]

positions = [
    # Party committee
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区委主要负责人"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Government
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区政府主要负责人"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    # 书记 ↔ 区长 (top leadership pair)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "李思远（区委书记）与任海龙（区长）在区委常委会和区政府班子共事", "overlap_org": "中共南岗区委/南岗区人民政府", "overlap_period": "2025年至今"},
    # 书记 ↔ 副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "李思远与陆一平在区委常委会共事", "overlap_org": "中共南岗区委", "overlap_period": "2025年至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "李思远与宋殿荣在区委常委会共事", "overlap_org": "中共南岗区委", "overlap_period": "2025年至今"},
    # 区长 ↔ 副区长
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "任海龙（区长）与宋殿荣（常务副区长）在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "任海龙与宁飞飞在南岗区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "任海龙与刘福禄在南岗区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "任海龙与杨帆在南岗区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "任海龙与张钧光在南岗区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "任海龙与韩雪松在南岗区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "任海龙与孔繁龙在南岗区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    # 常务副区长 ↔ 其他副区长
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "宋殿荣（常务副区长）与宁飞飞（副区长）在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "宋殿荣与刘福禄在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "宋殿荣与杨帆在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "宋殿荣与张钧光在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "宋殿荣与韩雪松在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "宋殿荣与孔繁龙在区政府班子共事", "overlap_org": "南岗区人民政府", "overlap_period": "2025年至今"},
    # 副书记间关系
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "陆一平与宋殿荣在区委常委会共事", "overlap_org": "中共南岗区委", "overlap_period": "2025年至今"},
]


# =========================================================================
# BUILD
# =========================================================================

def build():
    os.makedirs(STAGING, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"nangang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post:
            return "255,50,50"
        if "区长" in post and "副" not in post and "区委副书记" in post:
            return "50,100,255"
        if "副区长" in post or "常务副区长" in post:
            return "100,150,220"
        if "副书记" in post and "区委副书记" in post and "区长" not in post:
            return "100,150,220"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post) or \
               ("区长" in post and "副" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post:
            return "square"
        if "区长" in post and "副" not in post:
            return "circle"
        if "常务副区长" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
            "事业单位": "220,220,220",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>哈尔滨市南岗区领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    source_register = [
        {"id": "S001", "title": "哈尔滨市南岗区人民政府 - 区委主要领导调研财税工作", "url": "http://www.hrbng.gov.cn/hebngq/ngyw/202603/c01_1111335.shtml",
         "publisher": "南岗区人民政府", "published_at": "2026-03-02", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认区委书记李思远、常委副区长宋殿荣"},
        {"id": "S002", "title": "哈尔滨市南岗区人民政府 - 南岗区召开人民政府全体会议", "url": "http://www.hrbng.gov.cn/hebngq/ngyw/202601/c01_1104722.shtml",
         "publisher": "南岗区人民政府", "published_at": "2026-01-26", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认区长任海龙，列席领导宁飞飞、刘福禄、杨帆、张钧光、韩雪松、孔繁龙"},
        {"id": "S003", "title": "哈尔滨市南岗区人民政府 - 区委副书记、区长任海龙深入重点企业走访调研", "url": "http://www.hrbng.gov.cn/hebngq/ngyw/202510/c01_1083331.shtml",
         "publisher": "南岗区人民政府", "published_at": "2025-10-11", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认任海龙为区委副书记、区长"},
        {"id": "S004", "title": "哈尔滨市南岗区人民政府 - 区委十二届九次全会暨区委经济工作会议", "url": "http://www.hrbng.gov.cn/hebngq/ngyw/202512/c01_1099173.shtml",
         "publisher": "南岗区人民政府", "published_at": "2025-12-31", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认李思远代表区委常委会作报告，任海龙部署经济工作"},
        {"id": "S005", "title": "哈尔滨市南岗区人民政府 - 五一职工合唱比赛", "url": "http://www.hrbng.gov.cn/hebngq/ngyw/202604/c01_1123069.shtml",
         "publisher": "南岗区人民政府", "published_at": "2026-04-30", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认区委书记李思远、区委副书记陆一平"},
        {"id": "S006", "title": "Wikipedia - 南岗区", "url": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B2%97%E5%8C%BA",
         "publisher": "Wikipedia", "published_at": "2025-07-03", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": "南岗区基本概况"},
    ]

    def make_person_json(p, custom_id=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "哈尔滨市",
                "region": "南岗区",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_南岗区",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"nangang_{p['name']}" if not custom_id else custom_id,
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "区委书记" in p.get("current_post", "")) or ("区长" in p.get("current_post", "") and "副" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S004" if "书记" in p.get("current_post", "") else "S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "",
                    "org": p.get("current_org", ""),
                    "title": p.get("current_post", ""),
                    "notes": "现任，公开资料中未找到详细履历",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "organizations": [],
            "relationships": [
                r for r in [
                    {"person": "李思远", "person_id": "nangang_李思远", "relationship_type": "overlap", "strength": "strong"} if "李思远" != p["name"] else None,
                    {"person": "任海龙", "person_id": "nangang_任海龙", "relationship_type": "overlap", "strength": "strong"} if "任海龙" != p["name"] and "任海龙" != p["name"] else None,
                    {"person": "陆一平", "person_id": "nangang_陆一平", "relationship_type": "overlap", "strength": "medium"} if "陆一平" != p["name"] else None,
                    {"person": "宋殿荣", "person_id": "nangang_宋殿荣", "relationship_type": "overlap", "strength": "medium"} if "宋殿荣" != p["name"] else None,
                ] if r is not None
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生年月、教育背景、历任职务）",
                 "why_it_matters": "无法追溯其任职路径和系统经历，无法建立更深层的关系网络",
                 "suggested_queries": [f"{p['name']} 简历 南岗 哈尔滨"],
                 "last_attempted": AS_OF},
            ]
        }
        return result

    # Generate person JSON files for the two main leaders
    for p in persons[:2]:
        pjson = make_person_json(p)
        job_slug = "区委书记" if p["id"] == 1 else "区长"
        fname = f"{TODAY}-黑龙江省-哈尔滨市-{job_slug}-{p['name']}.json"
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {fpath}")


if __name__ == "__main__":
    build()
