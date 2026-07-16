#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 漳州市 (Zhangzhou City, Fujian) leadership network.

漳州市 — 地级市, 福建省下辖, 位于福建省南部, 辖2区1市8县.
Research date: 2026-07-16

Sources:
- Wikipedia (zh.wikipedia.org/wiki/漳州市) — leadership table
- Wikipedia individual pages for top leaders
- Baidu Baike (partial, via curl_cffi)
- China Economic Net (district.ce.cn) — appointment notices

Coverage:
- Current top 2 leaders: 市委书记 王进足, 市长 魏东
- Current 市委常委 standing committee members
- 市人大常委会, 市政协, 市纪委 leaders
- Predecessor/successor chains (2013-present)
- Key organizational nodes

Confidence notes:
- 王进足 (Party Secretary): career timeline confirmed from Wikipedia
- 魏东 (Mayor): identity confirmed; early career (~2016前) is an open gap
- 郑立敏: career timeline confirmed from Baidu Baike
- Other 常委 members: current titles confirmed; detailed bios are partial
- 廖卓文, 余向红, 胡栋良: current roles confirmed; career timelines need further research
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_漳州市")
DB_PATH = os.path.join(STAGING, "漳州市_network.db")
GEXF_PATH = os.path.join(STAGING, "漳州市_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 王进足 — 漳州市委书记 (since 2023.08)
    {"id":1,"name":"王进足","gender":"男","ethnicity":"汉族",
     "birth":"1967-01","birthplace":"福建泉州",
     "education":"中央党校大学学历",
     "party_join":"1992-08","work_start":"1988",
     "current_post":"漳州市委书记",
     "current_org":"中共漳州市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E8%BF%9B%E8%B6%B3"},
    # 魏东 — 漳州市市长 (since 2023.08)
    {"id":2,"name":"魏东","gender":"男","ethnicity":"汉族",
     "birth":"1970-01","birthplace":"云南镇雄",
     "education":"研究生学历",
     "party_join":"中共党员","work_start":"未详",
     "current_post":"漳州市委副书记、市长",
     "current_org":"漳州市人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E6%BC%B3%E5%B7%9E%E5%B8%82"},

    # ── 2. Current 市委常委 ──
    # 廖卓文 — 市委常委、常务副市长 (confirmed 2025.12)
    {"id":3,"name":"廖卓文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市委常委、常务副市长",
     "current_org":"漳州市人民政府",
     "source":"https://baike.baidu.com/item/%E5%BB%96%E5%8D%93%E6%96%87/64435157"},
    # 郑立敏 — 市委常委、副市长、古雷开发区党工委书记
    {"id":4,"name":"郑立敏","gender":"男","ethnicity":"汉族",
     "birth":"1976-08","birthplace":"福建仙游",
     "education":"在职研究生学历，法学硕士",
     "party_join":"1997-01","work_start":"1998-08",
     "current_post":"漳州市委常委、副市长、古雷开发区党工委书记",
     "current_org":"漳州市人民政府",
     "source":"https://baike.baidu.com/item/%E9%83%91%E7%AB%8B%E6%95%8F/5803278"},
    # 余向红 — 市委常委、宣传部部长 (confirmed 2025.12)
    {"id":5,"name":"余向红","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市委常委、宣传部部长",
     "current_org":"中共漳州市委宣传部",
     "source":"news.cctv.com (搜索)"},
    # 胡栋良 — 市委常委、统战部部长 (confirmed 2025.08)
    {"id":6,"name":"胡栋良","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市委常委、统战部部长、市政协党组副书记",
     "current_org":"中共漳州市委统战部",
     "source":"news.cctv.com (搜索)"},
    # 陈文聪 — 市委常委、市纪委书记、市监委主任 (since 2021.08)
    {"id":7,"name":"陈文聪","gender":"男","ethnicity":"汉族",
     "birth":"1972-01","birthplace":"福建惠安",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市委常委、市纪委书记、市监委主任",
     "current_org":"中共漳州市纪律检查委员会",
     "source":"http://district.ce.cn/newarea/sddy/202108/24/t20210824_36841392.shtml"},

    # ── 3. 市人大/市政协/市纪委 leaders ──
    # 吴卫红 — 市人大常委会主任 (since 2025.01)
    {"id":8,"name":"吴卫红","gender":"女","ethnicity":"汉族",
     "birth":"1966-11","birthplace":"福建龙岩永定",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市人大常委会主任",
     "current_org":"漳州市人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E6%BC%B3%E5%B7%9E%E5%B8%82"},
    # 刘革生 — 市政协主席 (since 2025.12)
    {"id":9,"name":"刘革生","gender":"男","ethnicity":"汉族",
     "birth":"1967-04","birthplace":"江苏南京",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"漳州市政协主席",
     "current_org":"政协漳州市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E6%BC%B3%E5%B7%9E%E5%B8%82"},

    # ── 4. 市委书记 predecessors ──
    # 张国旺 — 前市委书记 (2021.06-2023.08), 现厦门市政协主席
    {"id":10,"name":"张国旺","gender":"男","ethnicity":"汉族",
     "birth":"1964-10","birthplace":"福建建瓯",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市政协主席",
     "current_org":"政协厦门市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E5%BC%A0%E5%9B%BD%E6%97%BA"},
    # 邵玉龙 — 前市委书记 (2019.03-2021.06)
    {"id":11,"name":"邵玉龙","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"（原漳州市委书记）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E6%BC%B3%E5%B7%9E%E5%B8%82"},
    # 檀云坤 — 前市委书记 (2016.12-2019.03), 前市长 (2013.12-2016.12)
    {"id":12,"name":"檀云坤","gender":"男","ethnicity":"汉族",
     "birth":"1963-01","birthplace":"福建永泰",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"福建省人大常委会副主任",
     "current_org":"福建省人大常委会",
     "source":"https://zh.wikipedia.org/wiki/%E6%AA%80%E4%BA%91%E5%9D%A4"},
    # 陈家东 — 前市委书记 (2013.07-2016.12), 后落马
    {"id":13,"name":"陈家东","gender":"男","ethnicity":"汉族",
     "birth":"1959-08","birthplace":"福建长乐",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"（原厦门市人大常委会主任，2023年判无期）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E9%99%88%E5%AE%B6%E4%B8%9C"},

    # ── 5. 市长 predecessors ──
    # 刘远 — 前市长 (2016.12-2021.06)
    {"id":14,"name":"刘远","gender":"男","ethnicity":"汉族",
     "birth":"1963-03","birthplace":"福建长汀",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"福建省政协常委、经济委副主任",
     "current_org":"福建省政协",
     "source":"https://zh.wikipedia.org/wiki/%E5%88%98%E8%BF%9C"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Zhangzhou市级组织
    {"id":1,"name":"中共漳州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省漳州市"},
    {"id":2,"name":"漳州市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省漳州市"},
    {"id":3,"name":"漳州市人大常委会","type":"人大","level":"地级","parent":"","location":"福建省漳州市"},
    {"id":4,"name":"政协漳州市委员会","type":"政协","level":"地级","parent":"","location":"福建省漳州市"},
    {"id":5,"name":"中共漳州市纪律检查委员会","type":"党委","level":"地级","parent":"中共漳州市委员会","location":"福建省漳州市"},
    {"id":6,"name":"中共漳州市委宣传部","type":"党委","level":"地级","parent":"中共漳州市委员会","location":"福建省漳州市"},
    {"id":7,"name":"中共漳州市委统战部","type":"党委","level":"地级","parent":"中共漳州市委员会","location":"福建省漳州市"},
    {"id":8,"name":"漳州古雷港经济开发区","type":"开发区","level":"地级","parent":"漳州市人民政府","location":"福建省漳州市古雷港"},
    {"id":9,"name":"中共漳州市委组织部","type":"党委","level":"地级","parent":"中共漳州市委员会","location":"福建省漳州市"},

    # Predecessors' organizations
    {"id":10,"name":"中共龙岩市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省龙岩市"},
    {"id":11,"name":"龙岩市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省龙岩市"},
    {"id":12,"name":"政协厦门市委员会","type":"政协","level":"副省级","parent":"","location":"福建省厦门市"},
    {"id":13,"name":"福建省人大常委会","type":"人大","level":"省级","parent":"","location":"福建省福州市"},
    {"id":14,"name":"福建省政协","type":"政协","level":"省级","parent":"","location":"福建省福州市"},
    {"id":15,"name":"福建省人民政府办公厅","type":"政府","level":"省级","parent":"福建省人民政府","location":"福建省福州市"},
    {"id":16,"name":"福建省生态环境厅","type":"政府","level":"省级","parent":"福建省人民政府","location":"福建省福州市"},
    {"id":17,"name":"中共福州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":18,"name":"中共三明市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省三明市"},

    # Earlier career orgs for 王进足
    {"id":19,"name":"泉州市鲤城区地产公司","type":"政府","level":"县级","parent":"中共泉州市委员会","location":"福建省泉州市"},
    {"id":20,"name":"中共林芝地区工布江达县委员会","type":"党委","level":"县级","parent":"中共西藏自治区委员会","location":"西藏林芝市"},
    {"id":21,"name":"平潭综合实验区管委会","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省平潭"},
    {"id":22,"name":"中共福清市委员会","type":"党委","level":"县级","parent":"中共福州市委员会","location":"福建省福州市"},
    {"id":23,"name":"中共连江县委员会","type":"党委","level":"县级","parent":"中共福州市委员会","location":"福建省福州市"},

    # 郑立敏 earlier orgs
    {"id":24,"name":"中共福建省委统战部","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":25,"name":"共青团福州市委员会","type":"群团","level":"地级","parent":"中共福州市委员会","location":"福建省福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 王进足 career timeline ──
    {"id":1,"person_id":1,"org_id":19,"title":"泉州市鲤城区地产公司总经理等","start":"1988","end":"1998","rank":"","note":"鲤城区地产公司总经理、土地局副局长、万安开发区管委会副主任"},
    {"id":2,"person_id":1,"org_id":1,"title":"泉州市洛江区乡镇领导","start":"1998","end":"2006","rank":"","note":"双阳镇镇长、河市镇党委书记、马甲镇党委书记"},
    {"id":3,"person_id":1,"org_id":1,"title":"泉州市洛江区政府副区长","start":"2006","end":"2007-07","rank":"副处","note":""},
    {"id":4,"person_id":1,"org_id":20,"title":"援藏：西藏工布江达县委副书记、书记","start":"2007-07","end":"2013-07","rank":"正处","note":"6年援藏经历"},
    {"id":5,"person_id":1,"org_id":21,"title":"平潭综合实验区党工委委员、管委会副主任","start":"2013-10","end":"2016-03","rank":"","note":""},
    {"id":6,"person_id":1,"org_id":17,"title":"福州市委常委、福清市委书记","start":"2016-03","end":"2019-11","rank":"副厅","note":""},
    {"id":7,"person_id":1,"org_id":18,"title":"三明市委副书记","start":"2019-11","end":"2021-06","rank":"副厅","note":""},
    {"id":8,"person_id":1,"org_id":2,"title":"漳州市委副书记、市政府党组书记、市长","start":"2021-06","end":"2023-08","rank":"正厅","note":""},
    {"id":9,"person_id":1,"org_id":1,"title":"漳州市委书记","start":"2023-08","end":"present","rank":"正厅","note":"现任"},

    # ── 魏东 career timeline（partial） ──
    {"id":10,"person_id":2,"org_id":15,"title":"福建省政府副秘书长（正厅长级）、办公厅党组成员","start":"~2021","end":"2023-08","rank":"正厅","note":"具体时间待核实"},
    {"id":11,"person_id":2,"org_id":2,"title":"漳州市副市长、代市长","start":"2023-08-02","end":"2023-08-29","rank":"正厅","note":""},
    {"id":12,"person_id":2,"org_id":2,"title":"漳州市委副书记、市长、市政府党组书记","start":"2023-08-29","end":"present","rank":"正厅","note":"现任"},

    # ── 郑立敏 career timeline ──
    {"id":13,"person_id":4,"org_id":24,"title":"福建省委统战部宣传信息办副主任科员、主任科员","start":"2004","end":"2012","rank":"","note":""},
    {"id":14,"person_id":4,"org_id":25,"title":"共青团福州市委书记、晋安区委副书记（正处级）","start":"2012-12","end":"2016-06","rank":"正处","note":""},
    {"id":15,"person_id":4,"org_id":23,"title":"连江县委副书记、县长","start":"2016-06","end":"2021-08","rank":"正处","note":""},
    {"id":16,"person_id":4,"org_id":2,"title":"漳州市政府党组成员、副市长","start":"2021-08","end":"2025","rank":"副厅","note":""},
    {"id":17,"person_id":4,"org_id":1,"title":"漳州市委常委、副市长、古雷开发区党工委书记","start":"2025","end":"present","rank":"副厅","note":"现任"},

    # ── 陈文聪 ──
    {"id":18,"person_id":7,"org_id":5,"title":"漳州市委常委、市纪委书记、市监委代主任","start":"2021-08","end":"2021-08","rank":"副厅","note":""},
    {"id":19,"person_id":7,"org_id":5,"title":"漳州市委常委、市纪委书记、市监委主任","start":"2021-08","end":"present","rank":"副厅","note":"现任"},

    # ── 吴卫红 ──
    {"id":20,"person_id":8,"org_id":2,"title":"漳州市副市长（曾任常务副市长）","start":"~2016","end":"2021-08","rank":"副厅","note":"此前曾任常务副市长"},
    {"id":21,"person_id":8,"org_id":3,"title":"漳州市人大常委会主任","start":"2025-01","end":"present","rank":"正厅","note":"现任"},

    # ── 廖卓文 ──
    {"id":22,"person_id":3,"org_id":2,"title":"漳州市委常委、常务副市长","start":"2025-12","end":"present","rank":"副厅","note":"现任"},

    # ── 余向红 ──
    {"id":23,"person_id":5,"org_id":6,"title":"漳州市委常委、宣传部部长","start":"2025-12","end":"present","rank":"副厅","note":"现任"},

    # ── 胡栋良 ──
    {"id":24,"person_id":6,"org_id":7,"title":"漳州市委常委、统战部部长、市政协党组副书记","start":"2025-08","end":"present","rank":"副厅","note":"现任"},

    # ── 刘革生 ──
    {"id":25,"person_id":9,"org_id":4,"title":"漳州市政协主席","start":"2025-12","end":"present","rank":"正厅","note":"现任"},

    # ── Predecessors ──
    # 张国旺
    {"id":26,"person_id":10,"org_id":11,"title":"龙岩市市长（来漳州前）","start":"","end":"2021-06","rank":"","note":""},
    {"id":27,"person_id":10,"org_id":1,"title":"漳州市委书记","start":"2021-06","end":"2023-08","rank":"正厅","note":""},
    {"id":28,"person_id":10,"org_id":12,"title":"厦门市政协主席","start":"2025-01","end":"present","rank":"副省级","note":"现任"},
    # 邵玉龙
    {"id":29,"person_id":11,"org_id":1,"title":"漳州市委书记","start":"2019-03","end":"2021-06","rank":"正厅","note":""},
    # 檀云坤
    {"id":30,"person_id":12,"org_id":2,"title":"漳州市市长","start":"2013-12","end":"2016-12","rank":"正厅","note":""},
    {"id":31,"person_id":12,"org_id":1,"title":"漳州市委书记","start":"2016-12","end":"2019-03","rank":"正厅","note":""},
    {"id":32,"person_id":12,"org_id":13,"title":"福建省人大常委会副主任","start":"2019-03","end":"present","rank":"副省级","note":"现任"},
    # 陈家东
    {"id":33,"person_id":13,"org_id":1,"title":"漳州市委书记","start":"2013-07","end":"2016-12","rank":"正厅","note":""},
    # 刘远
    {"id":34,"person_id":14,"org_id":2,"title":"漳州市市长","start":"2016-12","end":"2021-06","rank":"正厅","note":""},
    {"id":35,"person_id":14,"org_id":14,"title":"福建省政协常委、经济委副主任","start":"","end":"present","rank":"正厅","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王进足 ←→ 魏东 (mayor, current partners)
    {"id":1,"person_a":1,"person_b":2,"type":"overlap","context":"漳州市委书记-市长搭档","overlap_org":"中共漳州市委员会/漳州市人民政府","overlap_period":"2023.08-至今"},
    # 王进足 → 张国旺 (predecessor in Secretary position)
    {"id":2,"person_a":10,"person_b":1,"type":"predecessor_successor","context":"张国旺→王进足 漳州市委书记交接","overlap_org":"中共漳州市委员会","overlap_period":"2023.08"},
    # 王进足 → 魏东 (predecessor in Mayor position)
    {"id":3,"person_a":1,"person_b":2,"type":"predecessor_successor","context":"王进足升书记后、魏东接任市长","overlap_org":"漳州市人民政府","overlap_period":"2023.08"},
    # 郑立敏 与 陈文聪 (同届常委)
    {"id":4,"person_a":4,"person_b":7,"type":"overlap","context":"漳州市委常委同僚","overlap_org":"中共漳州市委员会","overlap_period":"2025-至今"},
    # 郑立敏 与 廖卓文 (政府班子)
    {"id":5,"person_a":4,"person_b":3,"type":"overlap","context":"漳州市政府正副市长","overlap_org":"漳州市人民政府","overlap_period":"2025-至今"},
    # 檀云坤 → 王进足 (indirect: both were Mayor then Secretary)
    {"id":6,"person_a":12,"person_b":1,"type":"overlap","context":"同为漳州从市长升书记路径","overlap_org":"中共漳州市委员会","overlap_period":"不同时期"},
    # 张国旺 → 陈家东 → 檀云坤 → 邵玉龙 (书记链)
    {"id":7,"person_a":13,"person_b":12,"type":"predecessor_successor","context":"陈家东→檀云坤 漳州市委书记交接","overlap_org":"中共漳州市委员会","overlap_period":"2016.12"},
    {"id":8,"person_a":12,"person_b":11,"type":"predecessor_successor","context":"檀云坤→邵玉龙 漳州市委书记交接","overlap_org":"中共漳州市委员会","overlap_period":"2019.03"},
    {"id":9,"person_a":11,"person_b":10,"type":"predecessor_successor","context":"邵玉龙→张国旺 漳州市委书记交接","overlap_org":"中共漳州市委员会","overlap_period":"2021.06"},
    # 刘远 → 王进足 → 魏东 (市长链)
    {"id":10,"person_a":14,"person_b":1,"type":"predecessor_successor","context":"刘远→王进足 漳州市长交接","overlap_org":"漳州市人民政府","overlap_period":"2021.06"},
]

# =========================================================================
# SQLITE DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                      p["education"],p["party_join"],p["work_start"],p["current_post"],
                      p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for ps in positions:
        cur.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                     (ps["id"],ps["person_id"],ps["org_id"],ps["title"],ps["start"],ps["end"],ps["rank"],ps["note"]))
    for r in relationships:
        cur.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                     (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")

# =========================================================================
# GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return 'r,g,b' string based on person's role."""
    post = p.get("current_post","")
    if "书记" in post and "纪委" not in post and "人大" not in post and "政协" not in post:
        return "255,50,50"     # Red: Party Secretary
    if "市长" in post or "副" in post and "政府" in post:
        return "50,100,255"    # Blue: Government
    if "纪委" in post or "监委" in post:
        return "255,165,0"     # Orange: Discipline
    if "人大" in post:
        return "200,255,255"   # Cyan: People's Congress
    if "政协" in post:
        return "255,240,200"   # Cream: Political Consultative
    return "100,100,100"       # Grey: Others

def is_top_leader(p):
    return p["id"] in [1, 2]  # 王进足 and 魏东

def org_color(o):
    t = o.get("type","")
    m = {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200",
         "乡镇/街道":"255,255,200","事业单位":"220,220,220","群团":"255,220,255",
         "人大":"200,255,255","政协":"255,240,200"}
    return m.get(t,"200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>漳州市领导工作关系网络 - Zhangzhou City Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="subtype" type="string"/>')
    lines.append('      <attribute id="2" title="job_title" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
    lines.append('      <attribute id="5" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"][:20])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="3" value="地级"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person → Organization edges (worked_at)
    for ps in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{ps["person_id"]}" target="o{ps["org_id"]}" label="{esc(ps["title"][:30])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ps["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(ps["start"])}-{esc(ps["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring("\n".join(lines))
        print("    XML well-formed: OK")
    except Exception as e:
        print(f"    XML validation: {e}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("Building 漳州市 leadership network...")
    build_db()
    build_gexf()
    print("Done.")
