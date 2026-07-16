#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 洛江区 (Luojing District), 泉州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Task: fujian_洛江区 — 区委书记 & 区长
Province: 福建省
Parent city: 泉州市 (prefecture-level)
Region: 洛江区
Level: 市辖区
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 区委书记: 唐春晓 — confirmed from qzlj.gov.cn news (May-July 2026)
- 原区长: 郭宁 — resigned July 6, 2026 (六届人大常委会第四十二次会议)
- 代区长: 洪金城 (born 1973.09) — appointed acting mayor July 6, 2026

Deputy district leaders (confirmed from official government page):
- 常务副区长: 王昭昭, 涂德望
- 副区长: 王洪杰, 郭莎娜, 沈艺程, 杜仁义, 林联华, 王泽勇
- 区人大常委会主任: 徐情根
- 区法院院长: 苏益铮
- 区检察院检察长: 洪藜莹

Sources:
- Luojing District Government official website (www.qzlj.gov.cn) — homepage leadership section
- qzlj.gov.cn news (July 8, 2026): 六届人大常委会第四十二次、四十三次会议

Confidence: Current leadership identity-level confirmed from official government sources.
Full career timelines require additional research.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "洛江区_network.db")
GEXF_PATH = os.path.join(BASE, "洛江区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──

    # 唐春晓 — 洛江区委书记 (confirmed from qzlj.gov.cn news, May-July 2026)
    {"id":1,"name":"唐春晓","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区委书记","current_org":"中共泉州市洛江区委员会",
     "source":"https://www.qzlj.gov.cn (verified via news: 联动校地企 贯通产学研 区委书记唐春晓走访黎明职业大学, 2026-05-28)"},

    # 洪金城 — 洛江区委副书记、代区长
    {"id":2,"name":"洪金城","gender":"男","ethnicity":"汉族",
     "birth":"1973年9月","birthplace":"",
     "education":"本科学历，经济学学士",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区委副书记、区政府党组书记、代区长","current_org": "泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/201905/t20190529_1713216.htm"},

    # 郭宁 — 原区长（已辞职）
    {"id":3,"name":"郭宁","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原洛江区区长（已辞职）","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议: 决定接受郭宁辞去区长职务, 2026-07-06)"},

    # ── Deputy district leaders ──

    # 王昭昭 — 常务副区长
    {"id":4,"name":"王昭昭","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区委常委、常务副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn (homepage leadership section)"},

    # 涂德望 — 常务副区长
    {"id":5,"name":"涂德望","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区委常委、常务副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/202308/t20230821_2923862.htm"},

    # 王洪杰 — 副区长
    {"id":6,"name":"王洪杰","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/201906/t20190603_1715974.htm"},

    # 郭莎娜 — 副区长
    {"id":7,"name":"郭莎娜","gender":"女","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/201905/t20190529_1713206.htm"},

    # 沈艺程 — 副区长
    {"id":8,"name":"沈艺程","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/202107/t20210727_2594196.htm"},

    # 杜仁义 — 副区长
    {"id":9,"name":"杜仁义","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/201907/t20190730_1824199.htm"},

    # 林联华 — 副区长
    {"id":10,"name":"林联华","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/201911/t20191128_1963677.htm"},

    # 王泽勇 — 副区长
    {"id":11,"name":"王泽勇","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区副区长","current_org":"泉州市洛江区人民政府",
     "source":"https://www.qzlj.gov.cn/ldzc/qzfld/201907/t20190730_1824201.htm"},

    # ── Other key leadership ──

    # 徐情根 — 区人大常委会主任
    {"id":12,"name":"徐情根","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人大常委会主任","current_org":"泉州市洛江区人民代表大会常务委员会",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # 杨文格 — 区人大常委会副主任
    {"id":13,"name":"杨文格","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人大常委会副主任","current_org":"泉州市洛江区人民代表大会常务委员会",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # 何雄峰 — 区人大常委会副主任
    {"id":14,"name":"何雄峰","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人大常委会副主任","current_org":"泉州市洛江区人民代表大会常务委员会",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # 赵艺忠 — 区人大常委会副主任
    {"id":15,"name":"赵艺忠","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人大常委会副主任","current_org":"泉州市洛江区人民代表大会常务委员会",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # 彭朝顺 — 区人大常委会副主任
    {"id":16,"name":"彭朝顺","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人大常委会副主任","current_org":"泉州市洛江区人民代表大会常务委员会",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # 苏益铮 — 区法院院长
    {"id":17,"name":"苏益铮","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人民法院院长","current_org":"泉州市洛江区人民法院",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # 洪藜莹 — 区检察院检察长
    {"id":18,"name":"洪藜莹","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"洛江区人民检察院检察长","current_org":"泉州市洛江区人民检察院",
     "source":"https://www.qzlj.gov.cn (六届人大常委会第四十二次会议, 2026-07-06)"},

    # ── City-level leadership (泉州市) ──
    # 张毅恭 — 泉州市委书记
    {"id":19,"name":"张毅恭","gender":"男","ethnicity":"汉族",
     "birth":"1968-10","birthplace":"福建厦门",
     "education":"大学学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"泉州市委书记","current_org":"中共泉州市委员会",
     "source":"https://baike.baidu.com/item/%E5%BC%A0%E6%AF%85%E6%81%AD/24717085"},

    # 蔡战胜 — 泉州市长
    {"id":20,"name":"蔡战胜","gender":"男","ethnicity":"汉族",
     "birth":"1970-10","birthplace":"陕西渭南",
     "education":"博士研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"泉州市委副书记、市长","current_org":"泉州市人民政府",
     "source":"https://baike.baidu.com/item/%E8%94%A1%E6%88%98%E8%83%9C/24546796"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共泉州市洛江区委员会","type":"党委","level":"县处级",
     "parent":"中共泉州市委员会","location":"福建省泉州市洛江区"},
    {"id":2,"name":"泉州市洛江区人民政府","type":"政府","level":"县处级",
     "parent":"泉州市人民政府","location":"福建省泉州市洛江区"},
    {"id":3,"name":"泉州市洛江区人民代表大会常务委员会","type":"人大","level":"县处级",
     "parent":"泉州市人大常委会","location":"福建省泉州市洛江区"},
    {"id":4,"name":"泉州市洛江区人民法院","type":"政府","level":"县处级",
     "parent":"泉州市中级人民法院","location":"福建省泉州市洛江区"},
    {"id":5,"name":"泉州市洛江区人民检察院","type":"政府","level":"县处级",
     "parent":"泉州市人民检察院","location":"福建省泉州市洛江区"},
    {"id":6,"name":"中共泉州市委员会","type":"党委","level":"地市级",
     "parent":"中共福建省委员会","location":"福建省泉州市"},
    {"id":7,"name":"泉州市人民政府","type":"政府","level":"地市级",
     "parent":"福建省人民政府","location":"福建省泉州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 唐春晓 — 区委书记
    {"person_id":1,"org_id":1,"title":"洛江区委书记","start":"","end":"present",
     "rank":"县处级正职","note":"confirmed from qzlj.gov.cn news"},
    # 洪金城 — 代区长（兼区委副书记）
    {"person_id":2,"org_id":2,"title":"代区长","start":"2026-07","end":"present",
     "rank":"县处级正职","note":"六届人大常委会第四十三次会议任命, 2026-07-06"},
    {"person_id":2,"org_id":1,"title":"区委副书记","start":"2026-07","end":"present",
     "rank":"县处级正职","note":"兼任"},
    # 郭宁 — 原区长
    {"person_id":3,"org_id":2,"title":"区长","start":"","end":"2026-07",
     "rank":"县处级正职","note":"2026-07-06辞职"},
    {"person_id":3,"org_id":1,"title":"区委副书记","start":"","end":"2026-07",
     "rank":"县处级正职","note":"兼任"},
    # 王昭昭 — 常务副区长
    {"person_id":4,"org_id":2,"title":"常务副区长","start":"","end":"present",
     "rank":"县处级副职","note":"confirmed from homepage"},
    {"person_id":4,"org_id":1,"title":"区委常委","start":"","end":"present",
     "rank":"县处级副职","note":"兼任"},
    # 涂德望 — 常务副区长
    {"person_id":5,"org_id":2,"title":"常务副区长","start":"","end":"present",
     "rank":"县处级副职","note":"confirmed from homepage"},
    {"person_id":5,"org_id":1,"title":"区委常委","start":"","end":"present",
     "rank":"县处级副职","note":"兼任"},
    # 副区长们
    {"person_id":6,"org_id":2,"title":"副区长","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":7,"org_id":2,"title":"副区长","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":8,"org_id":2,"title":"副区长","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":9,"org_id":2,"title":"副区长","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":10,"org_id":2,"title":"副区长","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":11,"org_id":2,"title":"副区长","start":"","end":"present",
     "rank":"县处级副职","note":""},
    # 人大
    {"person_id":12,"org_id":3,"title":"主任","start":"","end":"present",
     "rank":"县处级正职","note":"区人大常委会主任"},
    {"person_id":13,"org_id":3,"title":"副主任","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":14,"org_id":3,"title":"副主任","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":15,"org_id":3,"title":"副主任","start":"","end":"present",
     "rank":"县处级副职","note":""},
    {"person_id":16,"org_id":3,"title":"副主任","start":"","end":"present",
     "rank":"县处级副职","note":""},
    # 法院、检察院
    {"person_id":17,"org_id":4,"title":"院长","start":"","end":"present",
     "rank":"县处级正职","note":"区人民法院院长"},
    {"person_id":18,"org_id":5,"title":"检察长","start":"","end":"present",
     "rank":"县处级正职","note":"区人民检察院检察长"},
    # 泉州市级
    {"person_id":19,"org_id":6,"title":"市委书记","start":"","end":"present",
     "rank":"正厅级","note":""},
    {"person_id":20,"org_id":7,"title":"市长","start":"","end":"present",
     "rank":"正厅级","note":"兼市委副书记"},
    {"person_id":20,"org_id":6,"title":"市委副书记","start":"","end":"present",
     "rank":"正厅级","note":"兼任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 唐春晓 ↔ 洪金城 (区委书记 ↔ 代区长, 党政正职搭档)
    {"person_a":1,"person_b":2,"type":"党政正职搭档",
     "context":"唐春晓任洛江区委书记，洪金城任代区长，为当前党政正职搭档",
     "overlap_org":"洛江区","overlap_period":"2026-07至今"},
    # 唐春晓 ↔ 郭宁 (区委书记 ↔ 原区长, 前任搭档)
    {"person_a":1,"person_b":3,"type":"党政正职搭档（已结束）",
     "context":"唐春晓任区委书记，郭宁任区长，为前任党政正职搭档",
     "overlap_org":"洛江区","overlap_period":"至2026-07"},
    # 郭宁 ↔ 洪金城 (前后任区长)
    {"person_a":3,"person_b":2,"type":"前后任",
     "context":"郭宁辞去区长职务，洪金城接任代区长",
     "overlap_org":"泉州市洛江区人民政府","overlap_period":"2026-07"},
    # 唐春晓 ↔ 王昭昭 (区委书记 ↔ 常委)
    {"person_a":1,"person_b":4,"type":"上下级",
     "context":"唐春晓为区委书记，王昭昭为区委常委",
     "overlap_org":"中共洛江区委员会","overlap_period":"至今"},
    # 唐春晓 ↔ 涂德望 (区委书记 ↔ 常委)
    {"person_a":1,"person_b":5,"type":"上下级",
     "context":"唐春晓为区委书记，涂德望为区委常委",
     "overlap_org":"中共洛江区委员会","overlap_period":"至今"},
    # 洪金城 ↔ 王昭昭 (代区长 ↔ 常务副区长)
    {"person_a":2,"person_b":4,"type":"上下级",
     "context":"洪金城为代区长，王昭昭为常务副区长",
     "overlap_org":"洛江区人民政府","overlap_period":"2026-07至今"},
    # 洪金城 ↔ 涂德望 (代区长 ↔ 常务副区长)
    {"person_a":2,"person_b":5,"type":"上下级",
     "context":"洪金城为代区长，涂德望为常务副区长",
     "overlap_org":"洛江区人民政府","overlap_period":"2026-07至今"},
    # 唐春晓 ↔ 徐情根 (区委书记 ↔ 人大主任)
    {"person_a":1,"person_b":12,"type":"四套班子同事",
     "context":"区委书记与人大主任同为区四套班子主要领导",
     "overlap_org":"洛江区","overlap_period":"至今"},
    # 洛江区 ↔ 泉州市级
    {"person_a":1,"person_b":19,"type":"上下级",
     "context":"唐春晓为洛江区委书记，受张毅恭（泉州市委书记）领导",
     "overlap_org":"泉州市","overlap_period":"至今"},
    {"person_a":2,"person_b":20,"type":"上下级",
     "context":"洪金城为洛江区代区长，受蔡战胜（泉州市长）领导",
     "overlap_org":"泉州市","overlap_period":"2026-07至今"},
    {"person_a":3,"person_b":20,"type":"上下级",
     "context":"郭宁此前为洛江区区长，受蔡战胜（泉州市长）领导",
     "overlap_org":"泉州市","overlap_period":"至2026-07"},
    # 副区长同事关系
    {"person_a":4,"person_b":6,"type":"同事","context":"同属洛江区政府领导班子",
     "overlap_org":"洛江区人民政府","overlap_period":"至今"},
    {"person_a":4,"person_b":7,"type":"同事","context":"同属洛江区政府领导班子",
     "overlap_org":"洛江区人民政府","overlap_period":"至今"},
    {"person_a":4,"person_b":8,"type":"同事","context":"同属洛江区政府领导班子",
     "overlap_org":"洛江区人民政府","overlap_period":"至今"},
    {"person_a":4,"person_b":9,"type":"同事","context":"同属洛江区政府领导班子",
     "overlap_org":"洛江区人民政府","overlap_period":"至今"},
    {"person_a":4,"person_b":10,"type":"同事","context":"同属洛江区政府领导班子",
     "overlap_org":"洛江区人民政府","overlap_period":"至今"},
    {"person_a":4,"person_b":11,"type":"同事","context":"同属洛江区政府领导班子",
     "overlap_org":"洛江区人民政府","overlap_period":"至今"},
]

# =========================================================================
# HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_role_color(person):
    post = person.get("current_post","")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"   # Red for Party Secretary
    if "区长" in post or "代区长" in post:
        return "50,100,255"  # Blue for Government head
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"   # Orange for Discipline
    if "主任" in post and "人大" in person.get("current_org",""):
        return "200,255,255" # Cyan for NPC
    return "100,100,100"    # Grey for others

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(person):
    return person["id"] in [1, 2, 3, 19, 20]

# =========================================================================
# BUILD SQLite
# =========================================================================

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                 p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"[OK] SQLite database written: {DB_PATH}")

# =========================================================================
# BUILD GEXF
# =========================================================================

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>China Gov Network Investigator</creator>')
lines.append('    <description>洛江区领导班子工作关系网络 - 福建省泉州市洛江区</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attribute declarations
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: persons
lines.append('    <nodes>')
for p in persons:
    c = person_role_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: organizations
for o in organizations:
    c = org_color(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="org"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# person -> organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person <-> person (relationship)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
print(f"[OK] GEXF graph written: {GEXF_PATH}")

# =========================================================================
# SUMMARY
# =========================================================================

print(f"\nSummary:")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print(f"  Edges (total):   {eid}")
print(f"\n  DB:   {DB_PATH}")
print(f"  GEXF: {GEXF_PATH}")
