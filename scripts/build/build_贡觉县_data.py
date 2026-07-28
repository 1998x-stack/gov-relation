#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 贡觉县 (Gonjo County) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/贡觉县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/贡觉县_network.gexf")

persons = [
    {"id": 1, "name": "郭建康", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委书记", "current_org": "中共贡觉县委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/f90c8aaeb378492cb07070ff355f3919.shtml"},
    {"id": 2, "name": "登巴杨培", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "中央民族大学藏学专业",
     "party_join": "", "work_start": "2002-07",
     "current_post": "贡觉县委副书记、县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202210/45d29447b2f444fb80b8f5af59b969b0.shtml"},
    {"id": 3, "name": "王树林", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委副书记", "current_org": "中共贡觉县委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/b5d826ab83ed425c86527ef0f2c96475.shtml"},
    {"id": 4, "name": "程亚荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "太原科技大学",
     "party_join": "", "work_start": "2006-07",
     "current_post": "昌都市政府副秘书长、贡觉县委常务副书记、常务副县长",
     "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202005/d1a1d74783cb4912bc1d18101dce670c.shtml"},
    {"id": 5, "name": "白朕纲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "天津科技大学",
     "party_join": "", "work_start": "2017-03",
     "current_post": "贡觉县委常务副书记、常务副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202508/210220dfb7374cd2ae59ea02519d211f.shtml"},
    {"id": 6, "name": "肖泽胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "西藏大学农牧学院",
     "party_join": "", "work_start": "2004-09",
     "current_post": "贡觉县委常委、常务副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202005/bfbe41b386534152b8ad34b45ef4b32d.shtml"},
    {"id": 7, "name": "王锦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "2004-12",
     "current_post": "贡觉县委常委、副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202210/9013223df322470f9ec34e131fda1fb4.shtml"},
    {"id": 8, "name": "洛松泽平", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "西藏大学农牧学院",
     "party_join": "", "work_start": "2004-09",
     "current_post": "贡觉县委常委、副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202607/b450162e2cf34dd58e53218d95b1cc98.shtml"},
    {"id": 9, "name": "李璞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委常委、组织部部长、党校校长",
     "current_org": "中共贡觉县委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/f90c8aaeb378492cb07070ff355f3919.shtml"},
    {"id": 10, "name": "刘国瑞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委常委、宣传部部长", "current_org": "中共贡觉县委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/b5d826ab83ed425c97527ec0f2c96475.shtml"},
    {"id": 11, "name": "孙文涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委常委、政法委书记、公安局党委书记",
     "current_org": "中共贡觉县委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/b5d826ab83ed425c865277ef0f2c96475.shtml"},
    {"id": 12, "name": "施展", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委常委、统战部部长", "current_org": "中共贡觉县委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/f90c8aaeb37840cb07070ff355f3917.shtml"},
    {"id": 13, "name": "黄彪", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贡觉县委常委、纪委书记、监委主任候选人",
     "current_org": "中共贡觉县纪律检查委员会",
     "source": "http://gongjue.changdu.gov.cn/gjx/c105702/202607/ff27c10e85d047f6b5680de796982b48.shtml"},
    {"id": 14, "name": "肖军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "2009-12",
     "current_post": "贡觉县副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202404/fa2422c57a5a4651812bf9a7e5d8cb93.shtml"},
    {"id": 15, "name": "益西多吉", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "西藏大学农牧学院",
     "party_join": "", "work_start": "2012-07",
     "current_post": "贡觉县副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202607/db4dc94dca654614be27f72392f396d7.shtml"},
    {"id": 16, "name": "周树勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "西北农林科技大学",
     "party_join": "", "work_start": "2009-07",
     "current_post": "贡觉县副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202305/8374b6a1e36943fd9fab214d93889a29.shtml"},
    {"id": 17, "name": "多吉占堆", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "2011-08",
     "current_post": "贡觉县副县长（重庆市挂职）", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202404/d74877d3307f4b2a97fcfd7025dd4707.shtml"},
    {"id": 18, "name": "徐霖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "2005-08",
     "current_post": "贡觉县副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202607/71661132fd9e45d29e254c3830bc509e.shtml"},
    {"id": 19, "name": "蒋晓兰", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "西藏民族学院",
     "party_join": "", "work_start": "2010-08",
     "current_post": "贡觉县副县长", "current_org": "贡觉县人民政府",
     "source": "http://gongjue.changdu.gov.cn/gjx/c101798/202607/f93d389e085b4d2ab9f8fd4ac446bfd6.shtml"},
]

organizations = [
    {"id": 1, "name": "中共贡觉县委员会", "type": "党委", "level": "县处级",
     "parent": "中共昌都市委员会", "location": "西藏昌都贡觉"},
    {"id": 2, "name": "贡觉县人民政府", "type": "政府", "level": "县处级",
     "parent": "昌都市人民政府", "location": "西藏昌都贡觉"},
    {"id": 3, "name": "中共贡觉县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共昌都市纪律检查委员会", "location": "西藏昌都贡觉"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "贡觉县委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "现任，2026年7月主持县第十一次党代会"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "贡觉县委副书记、县长",
     "start": "2023-04", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "贡觉县委副书记、代县长",
     "start": "2023-03", "end": "2023-04", "rank": "县处级正职", "note": "代理"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "贡觉县委副书记（县长人选）",
     "start": "2022-12", "end": "2023-03", "rank": "县处级副职", "note": ""},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "左贡县委副书记",
     "start": "2021-06", "end": "2022-12", "rank": "县处级副职", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "边坝县委常委、常务副县长",
     "start": "2019-04", "end": "2021-06", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 2, "org_id": 1, "title": "江达县委常委、宣传部部长",
     "start": "2016-03", "end": "2019-04", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 1, "title": "昌都市文化局非遗办公室主任",
     "start": "2014-12", "end": "2016-03", "rank": "正科级", "note": ""},
    {"id": 9, "person_id": 2, "org_id": 1, "title": "昌都地区文化局非遗办公室主任",
     "start": "2012-01", "end": "2014-12", "rank": "正科级", "note": ""},
    {"id": 10, "person_id": 2, "org_id": 1, "title": "昌都地区图书馆副馆长",
     "start": "2009-03", "end": "2012-01", "rank": "副科级", "note": ""},
    {"id": 11, "person_id": 2, "org_id": 1, "title": "昌都地区图书馆干部",
     "start": "2002-07", "end": "2009-03", "rank": "科员", "note": ""},
    {"id": 12, "person_id": 3, "org_id": 1, "title": "贡觉县委副书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 13, "person_id": 4, "org_id": 1, "title": "贡觉县委常务副书记",
     "start": "2025-07", "end": "", "rank": "县处级副职", "note": "东风汽车援藏"},
    {"id": 14, "person_id": 4, "org_id": 2, "title": "贡觉县常务副县长",
     "start": "2025-07", "end": "", "rank": "县处级副职", "note": "兼任"},
    {"id": 15, "person_id": 5, "org_id": 1, "title": "贡觉县委常务副书记",
     "start": "2025-07", "end": "", "rank": "县处级副职", "note": "天津宁河区援藏"},
    {"id": 16, "person_id": 5, "org_id": 2, "title": "贡觉县常务副县长",
     "start": "2025-07", "end": "", "rank": "县处级副职", "note": "兼任"},
    {"id": 17, "person_id": 6, "org_id": 1, "title": "贡觉县委常委",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": "新任常委"},
    {"id": 18, "person_id": 6, "org_id": 2, "title": "贡觉县常务副县长",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 19, "person_id": 6, "org_id": 2, "title": "贡觉县副县长",
     "start": "2021-07", "end": "2026-06", "rank": "县处级副职", "note": ""},
    {"id": 20, "person_id": 7, "org_id": 1, "title": "贡觉县委常委",
     "start": "2025-07", "end": "", "rank": "县处级副职", "note": "天津红桥区援藏"},
    {"id": 21, "person_id": 7, "org_id": 2, "title": "贡觉县副县长",
     "start": "2025-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 22, "person_id": 8, "org_id": 1, "title": "贡觉县委常委",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 23, "person_id": 8, "org_id": 2, "title": "贡觉县副县长",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 24, "person_id": 9, "org_id": 1, "title": "贡觉县委常委、组织部部长、党校校长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 25, "person_id": 10, "org_id": 1, "title": "贡觉县委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 26, "person_id": 11, "org_id": 1, "title": "贡觉县委常委、政法委书记、公安局党委书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 27, "person_id": 12, "org_id": 1, "title": "贡觉县委常委、统战部部长",
     "start": "2026-06", "end": "", "rank": "县处级副职", "note": "新任"},
    {"id": 28, "person_id": 13, "org_id": 3, "title": "贡觉县委常委、纪委书记、监委主任候选人",
     "start": "2026-06", "end": "", "rank": "县处级副职", "note": "新任"},
    {"id": 29, "person_id": 14, "org_id": 2, "title": "贡觉县副县长",
     "start": "2024-03", "end": "", "rank": "县处级副职", "note": "分管公安、司法"},
    {"id": 30, "person_id": 15, "org_id": 2, "title": "贡觉县副县长",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": "分管农业农村"},
    {"id": 31, "person_id": 16, "org_id": 2, "title": "贡觉县副县长",
     "start": "2025-08", "end": "", "rank": "县处级副职", "note": "分管林草、自然资源"},
    {"id": 32, "person_id": 17, "org_id": 2, "title": "贡觉县副县长（重庆市挂职）",
     "start": "2024-03", "end": "", "rank": "县处级副职", "note": "不负责具体工作"},
    {"id": 33, "person_id": 18, "org_id": 2, "title": "贡觉县副县长",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": "分管水利、交通"},
    {"id": 34, "person_id": 19, "org_id": 2, "title": "贡觉县副县长",
     "start": "2026-07", "end": "", "rank": "县处级副职", "note": "分管财政、国资"},
]

relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "郭建康（书记）与登巴杨培（县长）搭档",
     "overlap_org": "中共贡觉县委员会/贡觉县人民政府", "overlap_period": "2023至今"},
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "同僚",
     "context": "王树林（副书记）与登巴杨培（县长兼副书记）",
     "overlap_org": "中共贡觉县委员会", "overlap_period": "2026"},
    {"id": 3, "person_a_id": 4, "person_b_id": 5, "type": "同僚",
     "context": "程亚荣(东风)与白朕纲(天津)均为援藏常务副书记",
     "overlap_org": "贡觉县人民政府", "overlap_period": "2025-2026"},
    {"id": 4, "person_a_id": 4, "person_b_id": 7, "type": "同僚",
     "context": "程亚荣(东风汽车)与王锦(天津红桥)均为对口援藏干部",
     "overlap_org": "贡觉县人民政府", "overlap_period": ""},
    {"id": 5, "person_a_id": 9, "person_b_id": 1, "type": "上下级",
     "context": "李璞（组织部长）向郭建康（书记）汇报",
     "overlap_org": "中共贡觉县委员会", "overlap_period": ""},
    {"id": 6, "person_a_id": 9, "person_b_id": 10, "type": "同僚",
     "context": "李璞（组织）与刘国瑞（宣传）均为县委部门负责人",
     "overlap_org": "中共贡觉县委员会", "overlap_period": ""},
    {"id": 7, "person_a_id": 11, "person_b_id": 13, "type": "同僚",
     "context": "孙文涛（政法委）与黄彪（纪委）监督协作",
     "overlap_org": "中共贡觉县委员会", "overlap_period": "2026-06至今"},
    {"id": 8, "person_a_id": 11, "person_b_id": 14, "type": "上下级",
     "context": "肖军（公安副县长）向孙文涛（政法委书记兼公安局党委）汇报",
     "overlap_org": "贡觉县人民政府/县委政法委", "overlap_period": ""},
    {"id": 9, "person_a_id": 6, "person_b_id": 18, "type": "上下级",
     "context": "肖泽胜（常务副县长）指导徐霖（副县长，分管应急）",
     "overlap_org": "贡觉县人民政府", "overlap_period": "2026-07至今"},
    {"id": 10, "person_a_id": 19, "person_b_id": 2, "type": "上下级",
     "context": "蒋晓兰（副县长管财政）向登巴杨培（县长）汇报",
     "overlap_org": "贡觉县人民政府", "overlap_period": ""},
]

# BUILD SQLite DATABASE

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
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
);
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT,
    start_date TEXT,
    end_date TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
         p.get("birth",""), p.get("birthplace",""), p.get("education",""),
         p.get("party_join",""), p.get("work_start",""),
         p.get("current_post",""), p.get("current_org",""), p.get("source",""))
    )

for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
        (o["id"], o["name"], o.get("type",""), o.get("level",""), o.get("parent",""), o.get("location",""))
    )

for pos in positions:
    cur.execute(
        "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
        (pos["person_id"], pos["org_id"], pos["title"], pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note",""))
    )

for r in relationships:
    cur.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
        (r["person_a_id"], r["person_b_id"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()
conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")


# BUILD GEXF GRAPH

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    t = p.get("current_post","")
    if "县委书记" in t and "县委副书记" not in t.replace("县委书记","★"):
        return "255,50,50"
    elif "县长" in t:
        return "50,100,255"
    elif "纪委书记" in t or "监委" in t:
        return "255,165,0"
    elif "副书记" in t and "县委" in t:
        return "80,80,220"
    elif "常委" in t:
        return "60,120,60"
    else:
        return "100,150,255"

def person_size(p):
    t = p.get("current_post","")
    if "县委书记" in t or "县长" in t:
        return "20.0"
    elif "副书记" in t or "常务副县长" in t or "纪委书记" in t:
        return "15.0"
    elif "常委" in t:
        return "13.0"
    else:
        return "12.0"

def org_color(o):
    typ = o.get("type","")
    if "党委" in typ: return "255,200,200"
    elif "政府" in typ: return "200,200,255"
    elif "纪委" in typ: return "255,200,150"
    else: return "200,200,200"

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>贡觉县县级领导班子关系网络（2026年7月）</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="org_type" title="org_type" type="string"/>')
lines.append('      <attribute id="rank" title="rank" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('      <attribute id="period" title="period" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = person_size(p)
    rgb = c.split(",")
    pid = p["id"]
    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="org_type" value=""/>')
    lines.append(f'          <attvalue for="rank" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    oc = org_color(o)
    orgb = oc.split(",")
    oid = 1000 + o["id"]
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="org_type" value="{esc(o.get("type",""))}"/>')
    lines.append(f'          <attvalue for="rank" value="{esc(o.get("level",""))}"/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{orgb[0]}" g="{orgb[1]}" b="{orgb[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

lines.append('    <edges>')
eid = 1
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos.get("start","?")} \u2192 {pos.get("end","今")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

for r in relationships:
    lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r.get("overlap_period",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
