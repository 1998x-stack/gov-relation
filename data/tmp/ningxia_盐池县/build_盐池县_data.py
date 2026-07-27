#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yanchi County (盐池县) leadership network.

盐池县位于宁夏回族自治区吴忠市，地处宁夏东部。
"""
import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/盐池县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/盐池县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Yanchi County Leaders: County Committee ──
    {"id": 1, "name": "刘娜", "gender": "女", "ethnicity": "汉族",
     "birth": "1986-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共盐池县委书记", "current_org": "中共盐池县委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 2, "name": "王学冕", "gender": "男", "ethnicity": "满族",
     "birth": "1976-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委副书记、县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 3, "name": "马泽新", "gender": "男", "ethnicity": "回族",
     "birth": "1983-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委副书记、政法委书记", "current_org": "中共盐池县委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 4, "name": "蔡俊龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委副书记、副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 5, "name": "张飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-04", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、武装部政委", "current_org": "盐池县人民武装部",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 6, "name": "王大鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-04", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、常务副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 7, "name": "王生彦", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-04", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 8, "name": "郑慧玲", "gender": "女", "ethnicity": "汉族",
     "birth": "1976-07", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、宣传部部长", "current_org": "中共盐池县委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 9, "name": "安建冲", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-07", "birthplace": "", "education": "中央党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 10, "name": "赵亚东", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-01", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 11, "name": "马莉", "gender": "女", "ethnicity": "回族",
     "birth": "1980-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、纪委书记、监委主任", "current_org": "中共盐池县纪律检查委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 12, "name": "马小牛", "gender": "男", "ethnicity": "回族",
     "birth": "1985-07", "birthplace": "", "education": "宁夏党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委、组织部部长", "current_org": "中共盐池县委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 13, "name": "杨威", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县委常委", "current_org": "中共盐池县委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},

    # ── County Government Leaders ──
    {"id": 14, "name": "郑参", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 15, "name": "李渊", "gender": "男", "ethnicity": "回族",
     "birth": "1977-07", "birthplace": "", "education": "大学",
     "party_join": "民盟盟员", "work_start": "",
     "current_post": "盐池县副县长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 16, "name": "马涛", "gender": "男", "ethnicity": "回族",
     "birth": "1986-05", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县副县长（福建省石狮市挂职）", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 17, "name": "马林", "gender": "男", "ethnicity": "回族",
     "birth": "1975-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县副县长、公安局局长", "current_org": "盐池县人民政府",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},

    # ── Predecessors (from historical records) ──
    {"id": 18, "name": "龚雪飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%BE%9A%E9%9B%AA%E9%A3%9E"},
    {"id": 19, "name": "滑志敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
    {"id": 20, "name": "戴培吉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    # ── People's Congress and CPPCC Leaders ──
    {"id": 21, "name": "吴科", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县人大常委会主任", "current_org": "盐池县人民代表大会常务委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
    {"id": 22, "name": "刘新生", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐池县政协主席", "current_org": "中国人民政治协商会议盐池县委员会",
     "source": "http://www.yanchi.gov.cn/xxgk/ldzc/"},
]

organizations = [
    {"id": 1, "name": "中共盐池县委员会", "type": "党委", "level": "县处级", "parent": "中共吴忠市委员会", "location": "宁夏吴忠盐池"},
    {"id": 2, "name": "盐池县人民政府", "type": "政府", "level": "县处级", "parent": "吴忠市人民政府", "location": "宁夏吴忠盐池"},
    {"id": 3, "name": "中共盐池县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共吴忠市纪律检查委员会", "location": "宁夏吴忠盐池"},
    {"id": 4, "name": "盐池县人民武装部", "type": "军事", "level": "县处级", "parent": "", "location": "宁夏吴忠盐池"},
    {"id": 5, "name": "盐池县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "宁夏吴忠盐池"},
    {"id": 6, "name": "中国人民政治协商会议盐池县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "宁夏吴忠盐池"},
    {"id": 7, "name": "盐池县公安局", "type": "政府", "level": "乡科级", "parent": "盐池县人民政府", "location": "宁夏吴忠盐池"},
]

positions = [
    # ── Liu Na (刘娜) - Party Secretary ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共盐池县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，曾任盐池县委副书记、县长"},
    # Prior role: Yanchi County Magistrate (县长)
    {"id": 2, "person_id": 1, "org_id": 2, "title": "盐池县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "前任职务，后转任县委书记"},

    # ── Wang Xuemian (王学冕) - County Magistrate ──
    {"id": 3, "person_id": 2, "org_id": 2, "title": "盐池县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "盐池县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "前任职务"},

    # ── Standing Committee members ──
    {"id": 5, "person_id": 3, "org_id": 1, "title": "盐池县委副书记、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "盐池县委副书记、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（闽宁协作挂职）"},
    {"id": 7, "person_id": 5, "org_id": 4, "title": "盐池县委常委、武装部政委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 6, "org_id": 2, "title": "盐池县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 7, "org_id": 2, "title": "盐池县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 8, "org_id": 1, "title": "盐池县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 9, "org_id": 2, "title": "盐池县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（中国航油定点帮扶）"},
    {"id": 12, "person_id": 10, "org_id": 2, "title": "盐池县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（中石油帮扶）"},
    {"id": 13, "person_id": 11, "org_id": 3, "title": "盐池县委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 12, "org_id": 1, "title": "盐池县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 13, "org_id": 1, "title": "盐池县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Deputy County Mayors ──
    {"id": 16, "person_id": 14, "org_id": 2, "title": "盐池县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 15, "org_id": 2, "title": "盐池县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（民盟）"},
    {"id": 18, "person_id": 16, "org_id": 2, "title": "盐池县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（福建石狮挂职）"},
    {"id": 19, "person_id": 17, "org_id": 2, "title": "盐池县副县长、公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 17, "org_id": 7, "title": "盐池县公安局局长", "start": "", "end": "", "rank": "乡科级正职", "note": "兼任"},

    # ── Predecessors (Party Secretaries) ──
    {"id": 21, "person_id": 18, "org_id": 1, "title": "中共盐池县委书记", "start": "2021", "end": "", "rank": "县处级正职", "note": "刘娜前任"},
    {"id": 22, "person_id": 19, "org_id": 1, "title": "中共盐池县委书记", "start": "2018", "end": "2021", "rank": "县处级正职", "note": "龚雪飞前任"},
    {"id": 23, "person_id": 20, "org_id": 2, "title": "盐池县县长", "start": "", "end": "", "rank": "县处级正职", "note": "王学冕前任"},

    # ── NPC and CPPCC ──
    {"id": 24, "person_id": 21, "org_id": 5, "title": "盐池县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 25, "person_id": 22, "org_id": 6, "title": "盐池县政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
]

relationships = [
    # ── Party Secretary ↔ County Magistrate (党政搭档) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "刘娜（县委书记）与王学冕（县长）为现任党政领导班子搭档", "overlap_org": "盐池县人民政府", "overlap_period": "2026"},

    # ── Predecessor–Successor (Party Secretary) ──
    {"id": 2, "person_a_id": 18, "person_b_id": 1, "type": "交接", "context": "龚雪飞→刘娜 盐池县委书记交接", "overlap_org": "中共盐池县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 19, "person_b_id": 18, "type": "交接", "context": "滑志敏→龚雪飞 盐池县委书记交接", "overlap_org": "中共盐池县委员会", "overlap_period": ""},

    # ── Predecessor–Successor (County Magistrate) ──
    {"id": 4, "person_a_id": 20, "person_b_id": 1, "type": "党政搭档", "context": "戴培吉任县长时，刘娜曾任副县长/副书记", "overlap_org": "盐池县人民政府", "overlap_period": ""},

    # ── Standing Committee Colleagues ──
    {"id": 5, "person_a_id": 3, "person_b_id": 6, "type": "同僚", "context": "马泽新（副书记、政法委书记）与王大鹏（常务副县长）均为县委领导班子成员", "overlap_org": "中共盐池县委员会", "overlap_period": ""},
    {"id": 6, "person_a_id": 8, "person_b_id": 11, "type": "同僚", "context": "郑慧玲（宣传部部长）与马莉（纪委书记）同为县委常委", "overlap_org": "中共盐池县委员会", "overlap_period": ""},
    {"id": 7, "person_a_id": 12, "person_b_id": 11, "type": "同僚", "context": "马小牛（组织部部长）与马莉（纪委书记）均为县委常委", "overlap_org": "中共盐池县委员会", "overlap_period": ""},
    {"id": 8, "person_a_id": 6, "person_b_id": 7, "type": "同僚", "context": "王大鹏与王生彦均为县委常委、副县长", "overlap_org": "盐池县人民政府", "overlap_period": ""},
    {"id": 9, "person_a_id": 9, "person_b_id": 10, "type": "同僚", "context": "安建冲与赵亚东均为县委常委、副县长（挂职帮扶类）", "overlap_org": "盐池县人民政府", "overlap_period": ""},
    {"id": 10, "person_a_id": 13, "person_b_id": 6, "type": "同僚", "context": "杨威（县委常委）与王大鹏（常务副县长）", "overlap_org": "中共盐池县委员会", "overlap_period": ""},

    # ── Deputy County Mayors ──
    {"id": 11, "person_a_id": 14, "person_b_id": 15, "type": "同僚", "context": "郑参与李渊均为县政府副县长", "overlap_org": "盐池县人民政府", "overlap_period": ""},
    {"id": 12, "person_a_id": 15, "person_b_id": 16, "type": "同僚", "context": "李渊与马涛均为县政府副县长", "overlap_org": "盐池县人民政府", "overlap_period": ""},
    {"id": 13, "person_a_id": 17, "person_b_id": 6, "type": "上下级", "context": "马林（副县长、公安局长）在王大鹏（常务副县长）分管下工作", "overlap_org": "盐池县人民政府", "overlap_period": ""},

    # ── NPC / CPPCC leaders with county leaders ──
    {"id": 14, "person_a_id": 21, "person_b_id": 1, "type": "上下级", "context": "县人大常委会主任吴科与县委书记刘娜为县领导班子", "overlap_org": "盐池县", "overlap_period": ""},
    {"id": 15, "person_a_id": 22, "person_b_id": 1, "type": "上下级", "context": "县政协主席刘新生与县委书记刘娜为县领导班子", "overlap_org": "盐池县", "overlap_period": ""},

    # ── Liu Na's transition from Magistrate to Secretary ──
    {"id": 16, "person_a_id": 1, "person_b_id": 20, "type": "交接", "context": "刘娜接替戴培吉任盐池县县长，后接任县委书记", "overlap_org": "盐池县人民政府", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

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
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>盐池县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    # Color by role
    if pid == 1:  # Party Secretary
        r, g, b = 255, 50, 50
        size = 20.0
    elif pid == 2:  # County Magistrate
        r, g, b = 50, 100, 255
        size = 20.0
    elif pid == 11:  # Discipline Inspection
        r, g, b = 255, 165, 0
        size = 16.0
    elif pid == 21:  # NPC
        r, g, b = 200, 255, 255
        size = 14.0
    elif pid == 22:  # CPPCC
        r, g, b = 255, 240, 200
        size = 14.0
    elif pid in [18, 19, 20]:  # Predecessors
        r, g, b = 150, 150, 150
        size = 10.0
    else:
        r, g, b = 100, 100, 100
        size = 12.0

    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
org_colors = {
    "党委": (255, 200, 200),
    "政府": (200, 200, 255),
    "纪委": (255, 200, 200),
    "军事": (220, 220, 220),
    "人大": (200, 255, 255),
    "政协": (255, 240, 200),
}
for o in organizations:
    oid = 1000 + o["id"]
    cr, cg, cb = org_colors.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

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
