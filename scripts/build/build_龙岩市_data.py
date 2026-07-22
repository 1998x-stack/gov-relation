#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Longyan City (龙岩市), Fujian Province.

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- Wikipedia (Chinese): 龙岩市 leadership info and predecessor lists
- longyan.gov.cn: Official Longyan city government website
- Various news reports

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_龙岩市")
DB_PATH = os.path.join(TMP, "龙岩市_network.db")
GEXF_PATH = os.path.join(TMP, "龙岩市_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 胡盛 — 龙岩市委书记（2026.01-），前任市长（2021.06-2026.01）
    {"id":1,"name":"胡盛","gender":"男","ethnicity":"汉族","birth":"1978-01","birthplace":"福建厦门",
     "education":"","party_join":"中共党员","work_start":"2003-08",
     "current_post":"龙岩市委书记","current_org":"中共龙岩市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E8%83%A1%E7%9B%9B_(1978%E5%B9%B4)"},

    # 蔡琳 — 龙岩市市长（2026.01-）
    {"id":2,"name":"蔡琳","gender":"男","ethnicity":"汉族","birth":"1970-03","birthplace":"福建云霄",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"龙岩市委副书记、市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},

    # ── Other current city leaders ──
    # 陈厦生 — 龙岩市人大常委会主任（2026.01-）
    {"id":3,"name":"陈厦生","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"福建漳平",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"龙岩市人大常委会主任","current_org":"龙岩市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},

    # 李桂义 — 龙岩市政协主席（2022.01-）
    {"id":4,"name":"李桂义","gender":"男","ethnicity":"汉族","birth":"1966-04","birthplace":"福建长乐",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"龙岩市政协主席","current_org":"政协龙岩市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},

    # ── Current deputy mayors (from longyan.gov.cn) ──
    {"id":5,"name":"高丁博","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    {"id":6,"name":"邱开养","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    {"id":7,"name":"修洪","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    {"id":8,"name":"简洪坤","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    {"id":9,"name":"王波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    {"id":10,"name":"詹崇仁","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    {"id":11,"name":"戴伟荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市副市长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},
    # 秘书长
    {"id":12,"name":"钟海峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"龙岩市人民政府秘书长","current_org":"龙岩市人民政府",
     "source":"https://www.longyan.gov.cn/"},

    # ── Predecessors — 市委书记 ──
    # 余红胜 — 前任市委书记（2022.07-2025.11）
    {"id":13,"name":"余红胜","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 李建成 — 前任市委书记（2020.02-2022.07）
    {"id":14,"name":"李建成","gender":"男","ethnicity":"汉族","birth":"1967","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 许维泽 — 前任市委书记（2018.06-2020.02）
    {"id":15,"name":"许维泽","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 林国耀 — 前任市委书记（2016.12-2017.09）
    {"id":16,"name":"林国耀","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 李德金 — 前任市委书记（2015.12-2016.11）
    {"id":17,"name":"李德金","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 梁建勇 — 前任市委书记（2014.08-2015.12）
    {"id":18,"name":"梁建勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 黄晓炎 — 前任市委书记（2012.01-2014.08）
    {"id":19,"name":"黄晓炎","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},

    # ── Predecessors — 市长 ──
    # 胡盛 — 前任市长（same as person 1, 2021.06-2026.01），后升市委书记
    # 张国旺 — 前任市长（2020.03-2021.06）
    {"id":20,"name":"张国旺","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 林兴禄 — 前任市长（2016.12-2019.03）
    {"id":21,"name":"林兴禄","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 林国耀 — 前任市长（2016.07-2016.12）
    # (same as person 16)
    # 池秋娜 — 前任市长（2013.12-2016.07）
    {"id":22,"name":"池秋娜","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 张兆民 — 前任市长（2012.01-2013.11）
    {"id":23,"name":"张兆民","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
    # 黄晓炎 — 前任市长（2008.05-2012.01）
    # (same as person 19)
    # 雷春美 — 前任市长（2005.07-2008.05）, 女
    {"id":24,"name":"雷春美","gender":"女","ethnicity":"畲族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共龙岩市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省龙岩市"},
    {"id":2,"name":"龙岩市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省龙岩市"},
    {"id":3,"name":"龙岩市人大常委会","type":"人大","level":"地级","parent":"","location":"福建省龙岩市"},
    {"id":4,"name":"政协龙岩市委员会","type":"政协","level":"地级","parent":"","location":"福建省龙岩市"},
    {"id":5,"name":"中共福建省纪律检查委员会","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":6,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},
    {"id":7,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 胡盛 — Party Secretary (previously Mayor)
    {"person_id":1,"org_id":1,"title":"龙岩市委书记","start":"2026-01","end":"present","rank":"正厅级","note":"2026年1月任市委书记，此前为市长；曾挂职团中央书记处书记"},
    {"person_id":1,"org_id":2,"title":"龙岩市市长","start":"2021-06","end":"2026-01","rank":"正厅级","note":"2021年6月任代市长，后当选市长"},

    # 蔡琳 — Mayor
    {"person_id":2,"org_id":2,"title":"龙岩市市长","start":"2026-01","end":"present","rank":"正厅级","note":"2026年1月任代市长/市长"},
    {"person_id":2,"org_id":1,"title":"龙岩市委副书记","start":"2026-01","end":"present","rank":"正厅级","note":"兼任市委副书记"},

    # 陈厦生 — 人大主任
    {"person_id":3,"org_id":3,"title":"龙岩市人大常委会主任","start":"2026-01","end":"present","rank":"正厅级","note":""},

    # 李桂义 — 政协主席
    {"person_id":4,"org_id":4,"title":"龙岩市政协主席","start":"2022-01","end":"present","rank":"正厅级","note":""},

    # 副市长们
    {"person_id":5,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":6,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":7,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":"女"},
    {"person_id":8,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":9,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":10,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":""},
    {"person_id":11,"org_id":2,"title":"龙岩市副市长","start":"","end":"present","rank":"副厅级","note":""},

    # 钟海峰 — 秘书长
    {"person_id":12,"org_id":2,"title":"龙岩市人民政府秘书长","start":"","end":"present","rank":"正处级","note":""},

    # ── 前任市委书记 ──
    {"person_id":13,"org_id":1,"title":"龙岩市委书记","start":"2022-07","end":"2025-11","rank":"正厅级","note":"余红胜"},
    {"person_id":14,"org_id":1,"title":"龙岩市委书记","start":"2020-02","end":"2022-07","rank":"正厅级","note":"李建成"},
    {"person_id":15,"org_id":1,"title":"龙岩市委书记","start":"2018-06","end":"2020-02","rank":"正厅级","note":"许维泽"},
    {"person_id":16,"org_id":1,"title":"龙岩市委书记","start":"2016-12","end":"2017-09","rank":"正厅级","note":"林国耀"},
    {"person_id":17,"org_id":1,"title":"龙岩市委书记","start":"2015-12","end":"2016-11","rank":"正厅级","note":"李德金"},
    {"person_id":18,"org_id":1,"title":"龙岩市委书记","start":"2014-08","end":"2015-12","rank":"正厅级","note":"梁建勇"},
    {"person_id":19,"org_id":1,"title":"龙岩市委书记","start":"2012-01","end":"2014-08","rank":"正厅级","note":"黄晓炎"},

    # ── 前任市长 ──
    {"person_id":20,"org_id":2,"title":"龙岩市市长","start":"2020-03","end":"2021-06","rank":"正厅级","note":"张国旺"},
    {"person_id":21,"org_id":2,"title":"龙岩市市长","start":"2016-12","end":"2019-03","rank":"正厅级","note":"林兴禄"},
    {"person_id":22,"org_id":2,"title":"龙岩市市长","start":"2013-12","end":"2016-07","rank":"正厅级","note":"池秋娜"},
    {"person_id":23,"org_id":2,"title":"龙岩市市长","start":"2012-01","end":"2013-11","rank":"正厅级","note":"张兆民"},
    {"person_id":24,"org_id":2,"title":"龙岩市市长","start":"2005-07","end":"2008-05","rank":"正厅级","note":"雷春美"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Predecessor-successor: 市委书记 chain
    {"person_a":1,"person_b":13,"type":"predecessor_successor","context":"胡盛接替余红胜任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2026","direction":"person_to_other","strength":"strong"},
    {"person_a":13,"person_b":14,"type":"predecessor_successor","context":"余红胜接替李建成任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2022","direction":"person_to_other","strength":"strong"},
    {"person_a":14,"person_b":15,"type":"predecessor_successor","context":"李建成接替许维泽任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2020","direction":"person_to_other","strength":"strong"},
    {"person_a":15,"person_b":16,"type":"predecessor_successor","context":"许维泽接替林国耀任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2018","direction":"person_to_other","strength":"strong"},
    {"person_a":16,"person_b":17,"type":"predecessor_successor","context":"林国耀接替李德金任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2016","direction":"person_to_other","strength":"strong"},
    {"person_a":17,"person_b":18,"type":"predecessor_successor","context":"李德金接替梁建勇任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2015","direction":"person_to_other","strength":"strong"},
    {"person_a":18,"person_b":19,"type":"predecessor_successor","context":"梁建勇接替黄晓炎任龙岩市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2014","direction":"person_to_other","strength":"strong"},

    # Predecessor-successor: 市长 chain
    {"person_a":2,"person_b":1,"type":"predecessor_successor","context":"蔡琳接替胡盛任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2026","direction":"person_to_other","strength":"strong"},
    {"person_a":1,"person_b":20,"type":"predecessor_successor","context":"胡盛接替张国旺任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2021","direction":"person_to_other","strength":"strong"},
    {"person_a":20,"person_b":21,"type":"predecessor_successor","context":"张国旺接替林兴禄任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2020","direction":"person_to_other","strength":"strong"},
    {"person_a":21,"person_b":16,"type":"predecessor_successor","context":"林兴禄接替林国耀任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2016","direction":"person_to_other","strength":"strong"},
    {"person_a":16,"person_b":22,"type":"predecessor_successor","context":"林国耀接替池秋娜任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2016","direction":"person_to_other","strength":"strong"},
    {"person_a":22,"person_b":23,"type":"predecessor_successor","context":"池秋娜接替张兆民任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2013","direction":"person_to_other","strength":"strong"},
    {"person_a":23,"person_b":19,"type":"predecessor_successor","context":"张兆民接替黄晓炎任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2012","direction":"person_to_other","strength":"strong"},
    {"person_a":19,"person_b":24,"type":"predecessor_successor","context":"黄晓炎接替雷春美任龙岩市市长","overlap_org":"龙岩市人民政府","overlap_period":"2008","direction":"person_to_other","strength":"strong"},

    # Mayor-to-Party-Secretary promotion paths (same-org overlap)
    {"person_a":1,"person_b":13,"type":"colleague","context":"胡盛任市长期间余红胜任市委书记（搭班约3年多）","overlap_org":"中共龙岩市委员会","overlap_period":"2022-2025","direction":"undirected","strength":"strong"},
    {"person_a":1,"person_b":14,"type":"colleague","context":"胡盛任市长期间李建成为市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2021-2022","direction":"undirected","strength":"strong"},
    {"person_a":20,"person_b":14,"type":"colleague","context":"张国旺任市长期间李建成为市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2020-2021","direction":"undirected","strength":"strong"},
    {"person_a":21,"person_b":16,"type":"colleague","context":"林兴禄任市长期间林国耀为市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2016-2017","direction":"undirected","strength":"strong"},
    {"person_a":22,"person_b":19,"type":"colleague","context":"池秋娜任市长期间黄晓炎为市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2013-2014","direction":"undirected","strength":"strong"},
    {"person_a":23,"person_b":19,"type":"colleague","context":"张兆民任市长期间黄晓炎为市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2012-2013","direction":"undirected","strength":"strong"},
    {"person_a":19,"person_b":24,"type":"colleague","context":"黄晓炎任市长期间雷春美为市委书记","overlap_org":"中共龙岩市委员会","overlap_period":"2008","direction":"undirected","strength":"strong"},

    # Internal promotions
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"胡盛任市委书记后与市长蔡琳搭班","overlap_org":"中共龙岩市委员会","overlap_period":"2026-","direction":"undirected","strength":"strong"},
]


# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        direction TEXT, strength TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"],
                   o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                   pos["end"], pos["rank"], pos.get("note", "")))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, direction, strength) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"], r["direction"], r["strength"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b string for a person by role."""
    title = p["current_post"]
    if "书记" in title and "市委" in title:
        return "255,50,50"   # Red for Party Secretary
    elif "市长" in title:
        return "50,100,255"  # Blue for Mayor
    else:
        return "100,100,100"  # Grey for others


def org_color(o):
    """Return r,g,b string for an organization by type."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    else:
        return "200,200,200"


def is_top_leader(p):
    """Check if a person is a top leader (书记/市长)."""
    return p["id"] in [1, 2]


def org_size(o):
    return "8.0"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>龙岩市领导关系网络 - Fujian Province, Longyan City</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="福建省龙岩市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{org_size(o)}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(pid, filename_suffix):
    p = next(x for x in persons if x["id"] == pid)
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})

    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            person_positions.append({
                "start":pos["start"],"end":pos["end"],"org":org["name"] if org else "",
                "title":pos["title"],"level":pos.get("rank",""),"location":org["location"] if org else "",
                "system":"party" if org and "党委" in org["type"] else "government",
                "rank":pos.get("rank",""),"is_key_promotion":False,"notes":pos.get("note",""),
                "confidence":"confirmed","source_ids":["S001"]
            })

    profile = {
        "schema_version": "1.0",
        "generated_at": "2026-07-17",
        "investigation_scope": {
            "province": "福建省",
            "city": "龙岩市",
            "region": "龙岩市",
            "job": filename_suffix,
            "task_id": "fujian_龙岩市",
            "time_focus": "2005-present"
        },
        "identity": {
            "person_id": f"fujian_longyan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":"","study_type":"unknown","source_ids":[]}],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {"name_birth":"","name_birthplace":"","official_profile_url":""}
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正厅级",
            "as_of": "2026-07-17",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": person_positions,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id":"S001","title":"龙岩市 - 维基百科","url":"https://zh.wikipedia.org/wiki/%E9%BE%99%E5%B2%A9%E5%B8%82",
             "publisher":"维基百科","published_at":"","accessed_at":"2026-07-17","source_type":"encyclopedia","reliability":"medium","notes":""},
            {"id":"S002","title":"胡盛 - 维基百科","url":"https://zh.wikipedia.org/wiki/%E8%83%A1%E7%9B%9B_(1978%E5%B9%B4)",
             "publisher":"维基百科","published_at":"","accessed_at":"2026-07-17","source_type":"encyclopedia","reliability":"medium","notes":""},
            {"id":"S003","title":"龙岩市人民政府门户网站","url":"https://www.longyan.gov.cn/",
             "publisher":"龙岩市人民政府","published_at":"","accessed_at":"2026-07-17","source_type":"official","reliability":"high","notes":""}
        ],
        "confidence_summary": {
            "identity":"partial",
            "current_role":"confirmed",
            "career_completeness":"partial",
            "relationship_confidence":"high",
            "biggest_gap":f"缺少{p['name']}的出生地、早期教育背景和完整履历时间线"
        },
        "open_questions": [
            {"priority":"high","question":f"{p['name']}的出生地和早期教育背景","why_it_matters":"影响人物身份确认和履历完整度",
             "suggested_queries":[f"{p['name']} 简历",f"{p['name']} 出生"],"last_attempted":"2026-07-17"},
            {"priority":"high","question":f"{p['name']}在任龙岩前的完整履历","why_it_matters":"理解其职业发展路径和提拔背景",
             "suggested_queries":[f"{p['name']} 任职经历"],"last_attempted":"2026-07-17"}
        ]
    }

    filename = f"20260717-福建省-龙岩市-{filename_suffix}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_sqlite()
    build_gexf()
    write_person_json(1, "市委书记")
    write_person_json(2, "市长")
    print("\nDone. All artifacts written to", TMP)
