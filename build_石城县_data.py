#!/usr/bin/env python3
"""Build script for 石城县 (Shicheng County) personnel network data.

石城县 is a county under 赣州市 (Ganzhou City), 江西省 (Jiangxi Province).

Research date: 2026-07-15
Data sources: 石城县人民政府网站 (www.shicheng.gov.cn), Baidu Baike, news reports

Leadership note: As of July 7, 2026, 刘诗河 was promoted from 县长 to 县委书记,
and 伍威 arrived as 县长候选人 (awaiting 人大 confirmation).
Previous: 尹忠 → 张小川 → 刘诗河 (县委书记 chain, each promoted from 县长).

Targets: 县委书记 & 县长
"""

import sqlite3
import os
from datetime import datetime

# When run via python3 data/tmp/jiangxi_石城县/build_石城县_data.py, __file__ is the full path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
STAGING_DIR = os.path.join(BASE, "data", "tmp", "jiangxi_石城县")
OUTPUT_DB = os.path.join(STAGING_DIR, "石城县_network.db")
OUTPUT_GEXF = os.path.join(STAGING_DIR, "石城县_network.gexf")

# process_tmp.py validation tokens
DB_PATH = OUTPUT_DB
GEXF_PATH = OUTPUT_GEXF

today = "2026-07-15"

# =========================================================================
# Persons
# =========================================================================
# id: integer, unique within this county
persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "刘诗河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委书记",
        "current_org": "中共石城县委员会",
        "source": "https://www.shicheng.gov.cn; Baidu Baike",
    },
    {
        "id": 2,
        "name": "伍威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-01",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委副书记、县长候选人",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn; Baidu Baike",
    },
    # ── Deputy Leaders (县委常委) ──
    {
        "id": 3,
        "name": "刘秋天",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委副书记（专职）",
        "current_org": "中共石城县委员会",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 4,
        "name": "钟本祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、常务副县长",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 5,
        "name": "刘雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-05",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、县纪委书记、县监委主任",
        "current_org": "中共石城县纪律检查委员会",
        "source": "https://www.shicheng.gov.cn; Baidu Baike",
    },
    {
        "id": 6,
        "name": "邓小兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、组织部部长",
        "current_org": "中共石城县委组织部",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 7,
        "name": "钟慧敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-09",
        "birthplace": "江西南康",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、宣传部部长",
        "current_org": "中共石城县委宣传部",
        "source": "Baidu Baike; government site",
    },
    {
        "id": 8,
        "name": "黄勇鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、政法委书记",
        "current_org": "中共石城县委政法委员会",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 9,
        "name": "彭长春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、统战部部长",
        "current_org": "中共石城县委统战部",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 10,
        "name": "宁雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、副县长",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn (profile page)",
    },
    {
        "id": 11,
        "name": "彭勃文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-06",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、副县长（挂职）",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 12,
        "name": "刘旭莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县委常委、副县长",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn",
    },
    # ── Other County Government Leaders ──
    {
        "id": 13,
        "name": "刘宾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-12",
        "birthplace": "",
        "education": "",
        "party_join": "农工党党员",
        "work_start": "",
        "current_post": "石城县副县长",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn (profile page)",
    },
    {
        "id": 14,
        "name": "郭景山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-01",
        "birthplace": "江西瑞金",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县副县长、县公安局局长",
        "current_org": "石城县公安局",
        "source": "https://www.shicheng.gov.cn (profile page)",
    },
    {
        "id": 15,
        "name": "李芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-07",
        "birthplace": "江西安远",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县副县长",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn (profile page)",
    },
    {
        "id": 16,
        "name": "赖小伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-06",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县副县长",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn (profile page)",
    },
    {
        "id": 17,
        "name": "吴陶晶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县副县长（挂职）",
        "current_org": "石城县人民政府",
        "source": "https://www.shicheng.gov.cn (profile page)",
    },
    # ── People's Congress & CPPCC ──
    {
        "id": 18,
        "name": "廖丽萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县人大常委会主任",
        "current_org": "石城县人民代表大会常务委员会",
        "source": "https://www.shicheng.gov.cn",
    },
    {
        "id": 19,
        "name": "赖松林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石城县政协主席",
        "current_org": "中国人民政治协商会议石城县委员会",
        "source": "https://www.shicheng.gov.cn",
    },
    # ── Predecessors ──
    {
        "id": 20,
        "name": "张小川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "江西赣州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原石城县委书记（已离任）",
        "current_org": "",
        "source": "https://www.shicheng.gov.cn; Baidu Baike",
    },
    {
        "id": 21,
        "name": "尹忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞金市委书记（原石城县委书记）",
        "current_org": "中共瑞金市委员会",
        "source": "Baidu Baike; news reports",
    },
]

# =========================================================================
# Organizations
# =========================================================================
orgs = [
    {"id": 1, "name": "中共石城县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州石城"},
    {"id": 2, "name": "石城县人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州石城"},
    {"id": 3, "name": "中共石城县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市纪律检查委员会", "location": "江西赣州石城"},
    {"id": 4, "name": "中共石城县委组织部", "type": "党委", "level": "县处级", "parent": "中共石城县委员会", "location": "江西赣州石城"},
    {"id": 5, "name": "中共石城县委宣传部", "type": "党委", "level": "县处级", "parent": "中共石城县委员会", "location": "江西赣州石城"},
    {"id": 6, "name": "中共石城县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共石城县委员会", "location": "江西赣州石城"},
    {"id": 7, "name": "中共石城县委统战部", "type": "党委", "level": "县处级", "parent": "中共石城县委员会", "location": "江西赣州石城"},
    {"id": 8, "name": "石城县公安局", "type": "政府", "level": "乡科级", "parent": "石城县人民政府", "location": "江西赣州石城"},
    {"id": 9, "name": "石城县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "赣州市人民代表大会常务委员会", "location": "江西赣州石城"},
    {"id": 10, "name": "中国人民政治协商会议石城县委员会", "type": "政协", "level": "县处级", "parent": "赣州市政协", "location": "江西赣州石城"},
    {"id": 11, "name": "中共瑞金市委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州瑞金"},
]

# =========================================================================
# Positions
# =========================================================================
positions = [
    # Current positions
    {"id": 1, "person_id": 1, "org_id": 1, "title": "石城县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "由县长晋升"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "石城县委副书记、县长候选人", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "待人大正式任命"},
    {"id": 3, "person_id": 3, "org_id": 1, "title": "石城县委副书记（专职）", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 4, "person_id": 4, "org_id": 2, "title": "石城县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 5, "org_id": 3, "title": "石城县委常委、县纪委书记、县监委主任", "start": "2023-09", "end": "", "rank": "县处级副职", "note": "2023年9月任纪委书记，2024年1月当选监委主任"},
    {"id": 6, "person_id": 6, "org_id": 4, "title": "石城县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 7, "org_id": 5, "title": "石城县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 8, "org_id": 6, "title": "石城县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 9, "org_id": 7, "title": "石城县委常委、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 10, "org_id": 2, "title": "石城县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责农业农村等工作"},
    {"id": 11, "person_id": 11, "org_id": 2, "title": "石城县委常委、副县长（挂职）", "start": "2024-06", "end": "", "rank": "县处级副职", "note": "博士，挂职"},
    {"id": 12, "person_id": 12, "org_id": 2, "title": "石城县委常委、副县长", "start": "2024-06", "end": "", "rank": "县处级副职", "note": "2024年6月任命"},
    {"id": 13, "person_id": 13, "org_id": 2, "title": "石城县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "农工党党员，分管教育、卫生、文旅"},
    {"id": 14, "person_id": 14, "org_id": 8, "title": "石城县副县长、县公安局局长", "start": "", "end": "", "rank": "乡科级正职", "note": "分管公安、信访"},
    {"id": 15, "person_id": 15, "org_id": 2, "title": "石城县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "分管住建、城管、自然资源"},
    {"id": 16, "person_id": 16, "org_id": 2, "title": "石城县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "分管工业、商贸、交通"},
    {"id": 17, "person_id": 17, "org_id": 2, "title": "石城县副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "博士，挂职"},
    {"id": 18, "person_id": 18, "org_id": 9, "title": "石城县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 19, "person_id": 19, "org_id": 10, "title": "石城县政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    # Historical positions
    {"id": 20, "person_id": 1, "org_id": 2, "title": "石城县委副书记、县长", "start": "2022", "end": "2026-07", "rank": "县处级正职", "note": "晋升县委书记"},
    {"id": 21, "person_id": 20, "org_id": 1, "title": "石城县委书记", "start": "2022-06", "end": "2026-07", "rank": "县处级正职", "note": ""},
    {"id": 22, "person_id": 20, "org_id": 2, "title": "石城县委副书记、县长", "start": "", "end": "2022-06", "rank": "县处级正职", "note": "晋升县委书记"},
    {"id": 23, "person_id": 21, "org_id": 1, "title": "石城县委书记", "start": "~2021", "end": "~2022", "rank": "县处级正职", "note": "前任书记"},
    {"id": 24, "person_id": 21, "org_id": 11, "title": "瑞金市委书记", "start": "2022-06", "end": "", "rank": "县处级正职", "note": "由石城县委书记调任"},
]

# =========================================================================
# Relationships
# =========================================================================
relationships = [
    # 党政搭档
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "刘诗河（县委书记）与伍威（县长候选人）党政搭档",
     "overlap_org": "石城县", "overlap_period": "2026-07至今"},
    {"id": 2, "person_a_id": 1, "person_b_id": 20, "type": "继任关系",
     "context": "刘诗河接替张小川任县委书记，此前张小川为县委书记时刘诗河为县长",
     "overlap_org": "石城县", "overlap_period": "2022-2026-07"},
    {"id": 3, "person_a_id": 20, "person_b_id": 21, "type": "继任关系",
     "context": "张小川接替尹忠任县委书记，此前张小川为县长尹忠为书记",
     "overlap_org": "石城县", "overlap_period": "~2021-2022"},
    {"id": 4, "person_a_id": 21, "person_b_id": 1, "type": "继任关系",
     "context": "尹忠、张小川、刘诗河三任县委书记均为县长升书记",
     "overlap_org": "石城县", "overlap_period": "~2021-2026"},
]

# =========================================================================
# SQLite Build
# =========================================================================

def build_sqlite(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a_id INTEGER, person_b_id INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a_id) REFERENCES persons(id),
        FOREIGN KEY(person_b_id) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in orgs:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?,?)""",
            (pos["id"], pos["person_id"], pos["org_id"],
             pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (id, person_a_id, person_b_id, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r["person_a_id"], r["person_b_id"],
             r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  SQLite: {db_path}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(orgs)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")


# =========================================================================
# GEXF Build
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = p.get("current_post", "")
    name = p.get("name", "")
    if "县委书记" in title or "书记" in title:
        return "255,50,50"
    if "县长" in title:
        return "50,100,255"
    if "纪委" in title:
        return "255,165,0"
    # Predecessors
    if name == "张小川" or name == "尹忠":
        return "200,100,100"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    pid = p["id"]
    return pid in (1, 2)  # 刘诗河 and 伍威

def is_prev_leader(p):
    return p["id"] in (20, 21)  # predecessors

def build_gexf(gexf_path):
    os.makedirs(os.path.dirname(gexf_path), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation build script</creator>')
    lines.append('    <description>石城县领导班子工作关系网络 - 2026-07-15</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        if is_top_leader(p):
            sz = "20.0"
        elif is_prev_leader(p):
            sz = "15.0"
        else:
            sz = "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in orgs:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        start = pos.get("start", "")
        end = pos.get("end", "")
        note = pos.get("note", "")
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(end)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(note)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {gexf_path}")
    print(f"    Nodes: {len(persons) + len(orgs)} ({len(persons)} persons + {len(orgs)} orgs)")
    print(f"    Edges: {eid} ({len(positions)} worked_at + {len(relationships)} relationship)")


# =========================================================================
# Main
# =========================================================================

def main():
    print(f"Building 石城县 personnel network data ({today})")
    print()
    print("Building SQLite database...")
    build_sqlite(OUTPUT_DB)
    print()
    print("Building GEXF graph...")
    build_gexf(OUTPUT_GEXF)
    print()
    print("Done. Files created:")
    print(f"  {OUTPUT_DB}")
    print(f"  {OUTPUT_GEXF}")
    print()
    print("Summary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()
