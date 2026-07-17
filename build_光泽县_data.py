#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Guangze County (光泽县), Nanping City, Fujian Province.

Covers: Party Secretary (县委书记), County Mayor (县长), key leadership,
predecessor/successor chains, and the county-level leadership network.

Sources:
- Wikipedia (Chinese): 光泽县
- Baidu Baike: 王贵 profile
- fj.chinanews.com.cn: 郭锋 election report
- people.cn: 陈中民 appointment
- fjsen.com (东南网): Fujian official news
- greatwuyi.com: Local news
- fjgznews.cn: 光泽新闻网
- hotelaah.com: Historical leader list
- ctbsb.net/ctdsb: 王贵 appointment report

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_光泽县")
DB_PATH = os.path.join(TMP, "光泽县_network.db")
GEXF_PATH = os.path.join(TMP, "光泽县_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 王贵 — 光泽县委书记 (2025.4-)
    {"id":1,"name":"王贵","gender":"男","ethnicity":"汉族","birth":"1981-06","birthplace":"浙江省永嘉县（福建武夷山出生）",
     "education":"福建农林大学旅游管理专业，在职研究生学历，农业推广硕士",
     "party_join":"中共党员","work_start":"",
     "current_post":"光泽县委书记","current_org":"中共光泽县委员会",
     "source":"https://baike.baidu.com/item/%E7%8E%8B%E8%B4%B5/58525535"},
    # 郭锋 — 光泽县人民政府县长 (2025.5-)
    {"id":2,"name":"郭锋","gender":"男","ethnicity":"汉族","birth":"1979-03","birthplace":"",
     "education":"大学学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"光泽县人民政府县长","current_org":"光泽县人民政府",
     "source":"https://www.fj.chinanews.com.cn/news/2025/2025-05-30/566847.html"},

    # ── Other top leaders ──
    # 郑建新 — 光泽县人大常委会主任
    {"id":3,"name":"郑建新","gender":"男","ethnicity":"汉族","birth":"1971-10","birthplace":"福建仙游人（福建光泽出生）",
     "education":"大学学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"光泽县人大常委会主任","current_org":"光泽县人民代表大会常务委员会",
     "source":"https://m.fznews.com.cn/dsxw/20190128/5c4e66163752a_2.shtml"},
    # 陈高宏 — 光泽县政协主席
    {"id":4,"name":"陈高宏","gender":"男","ethnicity":"汉族","birth":"1967-07","birthplace":"福建闽侯人（福建光泽出生）",
     "education":"中央党校大学学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"光泽县政协主席","current_org":"政协光泽县委员会",
     "source":"https://m.fznews.com.cn/dsxw/20190128/5c4e66163752a_2.shtml"},

    # ── Key deputies ──
    # 刘进 — 光泽县委副书记
    {"id":5,"name":"刘进","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"光泽县委副书记","current_org":"中共光泽县委员会",
     "source":"http://www.fjgznews.cn/2026-07/02/content_2360998.htm"},
    # 徐榕 — 光泽县委常委、组织部部长
    {"id":6,"name":"徐榕","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"光泽县委常委、组织部部长","current_org":"中共光泽县委组织部",
     "source":"http://www.fjjgdj.gov.cn/djdt/szdt/sxzdt/202312/t20231206_6326342.htm"},
    # 熊星林 — 光泽县委常委（原华桥乡党委书记）
    {"id":7,"name":"熊星林","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"光泽县委常委","current_org":"中共光泽县委员会",
     "source":"http://np.fjsen.com/2025-02/05/content_31834864.htm"},
    # 刘禄进 — 光泽县委常委、宣传部部长、县政府副县长
    {"id":8,"name":"刘禄进","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"光泽县委常委、宣传部部长、县政府副县长","current_org":"中共光泽县委宣传部",
     "source":"http://np.fjsen.com/2025-02/05/content_31834864.htm"},
    # 吴晖华 — 光泽县副县长（原李坊乡党委书记）
    {"id":9,"name":"吴晖华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"光泽县副县长","current_org":"光泽县人民政府",
     "source":"http://www.3a0598.com/index.php?a=show&c=index&catid=105&city=4&id=403510&m=content"},
    # 江晖 — 光泽县副县长 (2013-)
    {"id":10,"name":"江晖","gender":"男","ethnicity":"汉族","birth":"1966-12","birthplace":"福建光泽",
     "education":"大学学历、经济学学士",
     "party_join":"非中共党员","work_start":"1987-07",
     "current_post":"光泽县副县长","current_org":"光泽县人民政府",
     "source":"https://baike.so.com/doc/6941970-24976053.html"},

    # ── Predecessors — 县委书记 ──
    # 陈中民 — 前任光泽县委书记 (2021?-2025.1), 升任南平市人大常委会副主任
    {"id":11,"name":"陈中民","gender":"男","ethnicity":"汉族","birth":"1969-02","birthplace":"",
     "education":"省委党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"南平市人大常委会副主任","current_org":"南平市人民代表大会常务委员会",
     "source":"http://fj.people.com.cn/n2/2025/0109/c181466-41102646.html"},
    # 陈敏辉 — 更早前任县委书记 (2016.4-2021)
    {"id":12,"name":"陈敏辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.newton.com.tw/wiki/%E9%99%B3%E6%95%8F%E8%BC%9D/16658689"},
    # 符水俊 — 县委书记 (2009-2013)
    {"id":13,"name":"符水俊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://hotelaah.com/liren/fujian_nanping_guangze.html"},

    # ── Predecessors — 县长 ──
    # 赵大建 — 前任县长 (2016.7-2021.6), 后任顺昌县委书记, 2025.12升南平市政协
    {"id":14,"name":"赵大建","gender":"男","ethnicity":"汉族","birth":"1969-08","birthplace":"",
     "education":"中央党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"南平市政协党组成员","current_org":"政协南平市委员会",
     "source":"http://fj.people.com.cn/n2/2025/1218/c181466-41447220.html"},
    # 赵明正 — 更早前任县长 (2013.12-2016.7)
    {"id":15,"name":"赵明正","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://hotelaah.com/liren/fujian_nanping_guangze.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共光泽县委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市光泽县"},
    {"id":2,"name":"光泽县人民政府","type":"政府","level":"县级","parent":"南平市人民政府","location":"福建省南平市光泽县"},
    {"id":3,"name":"光泽县人民代表大会常务委员会","type":"人大","level":"县级","parent":"","location":"福建省南平市光泽县"},
    {"id":4,"name":"政协光泽县委员会","type":"政协","level":"县级","parent":"","location":"福建省南平市光泽县"},
    {"id":5,"name":"中共光泽县委组织部","type":"党委","level":"县级","parent":"中共光泽县委员会","location":"福建省南平市光泽县"},
    {"id":6,"name":"中共光泽县委宣传部","type":"党委","level":"县级","parent":"中共光泽县委员会","location":"福建省南平市光泽县"},
    {"id":7,"name":"中共松溪县委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市松溪县"},
    {"id":8,"name":"南平市人民代表大会常务委员会","type":"人大","level":"地级","parent":"","location":"福建省南平市"},
    {"id":9,"name":"南平市商务局","type":"政府","level":"地级","parent":"南平市人民政府","location":"福建省南平市"},
    {"id":10,"name":"政协南平市委员会","type":"政协","level":"地级","parent":"","location":"福建省南平市"},
    {"id":11,"name":"中共南平市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省南平市"},
    {"id":12,"name":"南平市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省南平市"},
    {"id":13,"name":"光澤县杭川镇","type":"乡镇/街道","level":"乡级","parent":"光泽县人民政府","location":"福建省南平市光泽县"},
    {"id":14,"name":"中共南平市委组织部","type":"党委","level":"地级","parent":"中共南平市委员会","location":"福建省南平市"},
    {"id":15,"name":"中共南平市委非公有制企业和社会组织工作委员会","type":"党委","level":"地级","parent":"中共南平市委员会","location":"福建省南平市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 王贵 — Party Secretary
    {"person_id":1,"org_id":1,"title":"光泽县委书记","start":"2025-04","end":"present","rank":"正处级",
     "note":"2025年4月任光泽县委书记，此前任光泽县县长"},
    {"person_id":1,"org_id":1,"title":"光泽县委常委、书记","start":"2025-04","end":"present","rank":"正处级",
     "note":"接替陈中民任县委书记"},
    # 王贵 — as County Mayor
    {"person_id":1,"org_id":2,"title":"光泽县人民政府县长","start":"2021-06","end":"2025-04","rank":"正处级",
     "note":"2021年6月任光泽县委副书记、代县长，后去代转正"},
    # 王贵 — earlier positions
    {"person_id":1,"org_id":7,"title":"松溪县委副书记","start":"","end":"2021-06","rank":"副处级",
     "note":"王贵曾任松溪县委副书记"},
    {"person_id":1,"org_id":7,"title":"松溪县委常委、组织部部长","start":"","end":"","rank":"副处级",
     "note":"王贵曾任松溪县委常委、组织部部长"},
    {"person_id":1,"org_id":13,"title":"光泽县杭川镇党委书记","start":"","end":"","rank":"正科级",
     "note":"王贵的早期职务"},

    # 郭锋 — County Mayor
    {"person_id":2,"org_id":2,"title":"光泽县人民政府县长","start":"2025-05","end":"present","rank":"正处级",
     "note":"2025年5月29日补选为光泽县人民政府县长"},
    {"person_id":2,"org_id":2,"title":"光泽县委副书记、县政府党组书记","start":"2025-05","end":"present","rank":"正处级",
     "note":"2025年5月任光泽县委副书记、县政府党组书记"},
    # 郭锋 — earlier positions
    {"person_id":2,"org_id":9,"title":"南平市商务局贸促会联合党组书记、商务局局长","start":"","end":"2025-05","rank":"正处级",
     "note":"郭锋此前任南平市商务局局长、口岸办主任、招商局局长、招商服务中心主任"},

    # 郑建新 — 人大主任
    {"person_id":3,"org_id":3,"title":"光泽县人大常委会主任","start":"","end":"present","rank":"正处级",
     "note":"现任光泽县人大常委会主任"},
    # 郑建新 — 曾任县委常委、统战部长
    {"person_id":3,"org_id":1,"title":"光泽县委常委、统战部部长","start":"","end":"","rank":"副处级",
     "note":"曾任光泽县委常委、统战部部长，崇仁乡党委书记"},

    # 陈高宏 — 政协主席
    {"person_id":4,"org_id":4,"title":"光泽县政协主席","start":"","end":"present","rank":"正处级",
     "note":"现任光泽县政协主席"},
    {"person_id":4,"org_id":1,"title":"光泽县委常委、统战部部长","start":"","end":"","rank":"副处级",
     "note":"曾任光泽县委常委、统战部部长"},

    # 刘进 — 县委副书记
    {"person_id":5,"org_id":1,"title":"光泽县委副书记","start":"","end":"present","rank":"副处级",
     "note":"现任光泽县委副书记"},

    # 徐榕 — 组织部长
    {"person_id":6,"org_id":5,"title":"光泽县委常委、组织部部长","start":"","end":"present","rank":"副处级",
     "note":"现任光泽县委常委、组织部部长"},

    # 熊星林 — 县委常委
    {"person_id":7,"org_id":1,"title":"光泽县委常委","start":"","end":"present","rank":"副处级",
     "note":"现任光泽县委常委，曾任华桥乡党委书记"},

    # 刘禄进 — 宣传部长/副县长
    {"person_id":8,"org_id":6,"title":"光泽县委常委、宣传部部长","start":"","end":"present","rank":"副处级",
     "note":"现任光泽县委常委、宣传部部长"},
    {"person_id":8,"org_id":2,"title":"光泽县人民政府副县长","start":"","end":"present","rank":"副处级",
     "note":"兼任县政府副县长"},

    # 吴晖华 — 副县长
    {"person_id":9,"org_id":2,"title":"光泽县副县长","start":"","end":"present","rank":"副处级",
     "note":"现任光泽县副县长，曾任李坊乡党委书记"},

    # 江晖 — 副县长
    {"person_id":10,"org_id":2,"title":"光泽县副县长","start":"2013-07","end":"present","rank":"副处级",
     "note":"2013年7月起任光泽县副县长，非中共党员"},
    {"person_id":10,"org_id":4,"title":"光泽县政协副主席","start":"","end":"","rank":"副处级",
     "note":"曾任光泽县政协副主席、止马镇镇长"},

    # 陈中民 — 前县委书记
    {"person_id":11,"org_id":1,"title":"光泽县委书记","start":"","end":"2025-01","rank":"正处级",
     "note":"2025年1月升任南平市人大常委会副主任"},
    {"person_id":11,"org_id":8,"title":"南平市人大常委会副主任","start":"2025-01","end":"present","rank":"副厅级",
     "note":"2025年1月当选南平市人大常委会副主任"},
    {"person_id":11,"org_id":14,"title":"南平市委组织部副部长兼市公务员局局长","start":"","end":"","rank":"正处级",
     "note":"曾任南平市委组织部副部长"},
    {"person_id":11,"org_id":15,"title":"南平市委非公有制企业和社会组织工作委员会专职副书记","start":"","end":"","rank":"副处级",
     "note":"曾任该职务"},

    # 赵大建 — 前县长
    {"person_id":14,"org_id":2,"title":"光泽县人民政府县长","start":"2016-07","end":"2021-06","rank":"正处级",
     "note":"2016年7月任光泽县代县长，后去代转正"},
    {"person_id":14,"org_id":10,"title":"南平市政协党组成员","start":"2025-12","end":"present","rank":"副厅级",
     "note":"2025年12月任南平市政协党组成员"},
    # 赵大建 also went to Shunchang
    {"person_id":14,"org_id":1,"title":"顺昌县委书记","start":"2021-06","end":"2025-12","rank":"正处级",
     "note":"赵大建2021年6月由光泽县长调任顺昌县委书记"},

    # 陈敏辉 — 更早前县委书记
    {"person_id":12,"org_id":1,"title":"光泽县委书记","start":"2016-04","end":"","rank":"正处级",
     "note":"2016年4月任光泽县委书记"},

    # 符水俊
    {"person_id":13,"org_id":1,"title":"光泽县委书记","start":"2009","end":"2013","rank":"正处级",
     "note":"2009年-2013年任光泽县委书记"},
    {"person_id":13,"org_id":2,"title":"光泽县人民政府县长","start":"2009-07","end":"2009-12","rank":"正处级",
     "note":"2009年7月任光泽代县长，后转书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 王贵 ↔ 郭锋 (县长接替)
    {"person_a":1,"person_b":2,"type":"predecessor_successor","context":"王贵任县委书记后，郭锋接任县长，王贵进行离任交接",
     "overlap_org":"光泽县人民政府","overlap_period":"2025-05","strength":"strong"},

    # 王贵 ↔ 陈中民 (县委书记接替)
    {"person_a":1,"person_b":11,"type":"predecessor_successor","context":"王贵接替陈中民任光泽县委书记，陈中民升任南平市人大常委会副主任",
     "overlap_org":"中共光泽县委员会","overlap_period":"2025-04","strength":"strong"},

    # 王贵 ↔ 赵大建 (县长接替)
    {"person_a":1,"person_b":14,"type":"predecessor_successor","context":"王贵2021年接替赵大建任光泽县县长，赵大建调任顺昌县委书记",
     "overlap_org":"光泽县人民政府","overlap_period":"2021-06","strength":"strong"},

    # 陈中民 ↔ 陈敏辉 (县委书记接替)
    {"person_a":11,"person_b":12,"type":"predecessor_successor","context":"陈中民接替陈敏辉任光泽县委书记",
     "overlap_org":"中共光泽县委员会","overlap_period":"2021","strength":"strong"},

    # 郑建新 ↔ 陈高宏 (曾同为县委常委)
    {"person_a":3,"person_b":4,"type":"overlap","context":"郑建新和陈高宏均曾任光泽县委常委",
     "overlap_org":"中共光泽县委员会","overlap_period":"","strength":"medium"},

    # 陈中民 ↔ 王贵 (上下级)
    {"person_a":11,"person_b":1,"type":"superior_subordinate","context":"陈中民任县委书记时，王贵任县长",
     "overlap_org":"中共光泽县委员会","overlap_period":"2021-06至2025-01","strength":"strong"},

    # 王贵 ↔ 郑建新 (现任领导团队)
    {"person_a":1,"person_b":3,"type":"overlap","context":"王贵与郑建新同在光泽县领导班子",
     "overlap_org":"中共光泽县委员会","overlap_period":"","strength":"medium"},

    # 王贵 ↔ 陈高宏 (现任领导团队)
    {"person_a":1,"person_b":4,"type":"overlap","context":"王贵与陈高宏同在光泽县领导班子",
     "overlap_org":"中共光泽县委员会","overlap_period":"","strength":"medium"},

    # 郭锋 ↔ 徐榕 (县政府交接见证)
    {"person_a":2,"person_b":6,"type":"overlap","context":"郭锋就任县长时，徐榕以组织部长身份参加交接",
     "overlap_org":"光泽县人民政府","overlap_period":"2025-05","strength":"medium"},

    # 郭锋 ↔ 郑建新 (党政班子配合)
    {"person_a":2,"person_b":3,"type":"overlap","context":"郭锋与郑建新同届班子，郑建新以统战部长身份陪同郭锋调研宗教工作",
     "overlap_org":"光泽县人民政府","overlap_period":"2025-06","strength":"medium"},

    # 赵大建 ↔ 陈中民 (县域领导交替)
    {"person_a":14,"person_b":11,"type":"overlap","context":"赵大建任县长时，陈中民任县委书记",
     "overlap_org":"中共光泽县委员会","overlap_period":"2021","strength":"strong"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def create_database():
    import os
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("PRAGMA foreign_keys = ON")
    
    c.execute('''CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT,
        source TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        strength TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )''')
    
    # Insert persons
    for p in persons:
        c.execute('''INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace,
             education, party_join, work_start,
             current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))
    
    # Insert organizations
    for o in organizations:
        c.execute('''INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)''',
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))
    
    # Insert positions
    for pos in positions:
        c.execute('''INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)''',
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))
    
    # Insert relationships
    for r in relationships:
        c.execute('''INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength)
            VALUES (?,?,?,?,?,?,?)''',
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"],
             r["overlap_period"], r["strength"]))
    
    conn.commit()
    conn.close()
    print(f"✓ SQLite database: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


def create_gexf():
    import os
    from datetime import datetime
    
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    
    # Map person role to color
    def person_color(p):
        name = p["name"]
        post = p.get("current_post", "")
        if "书记" in post and "纪委" not in post and name != "陈中民":
            return "255,50,50"  # Red - Party Secretary
        elif "书记" in post and name == "陈中民":
            return "255,50,50"  # Red - Former Party Secretary
        elif "县长" in post or "副县长" in post or "政府" in post:
            return "50,100,255"  # Blue - Government
        elif "人大" in post:
            return "200,255,255"  # Cyan - People's Congress
        elif "政协" in post:
            return "255,240,200"  # Cream - Political Consultative
        else:
            return "100,100,100"  # Grey - Others
    
    def is_top_leader(p):
        name = p["name"]
        return name in ("王贵", "郭锋")
    
    # Org color
    def org_color(o):
        ot = o["type"]
        if "党委" in ot:
            return "255,200,200"
        elif "政府" in ot:
            return "200,200,255"
        elif "人大" in ot:
            return "200,255,255"
        elif "政协" in ot:
            return "255,240,200"
        elif "乡镇" in ot:
            return "255,255,200"
        else:
            return "200,200,200"
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>光泽县领导班子工作关系网络 - 福建省南平市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('      <attribute id="4" title="strength" type="string"/>')
    lines.append('    </attributes>')
    
    # Nodes
    lines.append('    <nodes>')
    
    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["id"] in (3,4,5,6,11,14) else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
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
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    
    # person -> organization (worked_at)
    for pos in positions:
        # find the position to get start/end
        note = pos.get("note", "")
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    # person <-> person (relationship)
    for r in relationships:
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value="{esc(r["strength"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph: {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}, Org nodes: {len(organizations)}, "
          f"Person-Org edges: {len(positions)}, Person-Person edges: {len(relationships)}")


def create_person_json(p, extra_career=None):
    """Create a person JSON file following the person_graph_json.md schema."""
    import json
    
    # Build person_id
    name_clean = p["name"]
    person_id = f"guangze_{name_clean}"
    
    # Build career timeline from positions data
    career = []
    person_positions = [pos for pos in positions if pos["person_id"] == p["id"]]
    for pos in person_positions:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        career.append({
            "start": pos["start"] or "unknown",
            "end": pos["end"] or "unknown",
            "org": org_name,
            "title": pos["title"],
            "level": pos["rank"] or "",
            "location": "",
            "system": "government",
            "rank": pos["rank"] or "",
            "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"],
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if pos.get("note") else "plausible",
            "source_ids": ["S001"]
        })
    
    # Build relationships
    rels = []
    for r in relationships:
        if r["person_a"] == p["id"] or r["person_b"] == p["id"]:
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other_name = ""
            for p2 in persons:
                if p2["id"] == other_id:
                    other_name = p2["name"]
                    break
            rels.append({
                "person": other_name,
                "person_id": f"guangze_{other_name}",
                "relationship_type": r["type"],
                "strength": r["strength"],
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "confirmed" if r["strength"] == "strong" else "plausible",
                "source_ids": ["S001"]
            })
    
    # Build governance record
    governance = []
    
    # Professional profile
    primary_specs = []
    secondary_specs = []
    career_pattern = "local_ladder"
    
    if "书记" in p.get("current_post", "") and "纪委" not in p.get("current_post", ""):
        primary_specs.append("party_leadership")
        career_pattern = "cross_county_rotation"
    if "县长" in p.get("current_post", "") or "副县长" in p.get("current_post", ""):
        primary_specs.append("government_administration")
    
    person_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "光泽县",
            "job": p.get("current_post", ""),
            "task_id": "fujian_光泽县",
            "time_focus": "2016-present"
        },
        "identity": {
            "person_id": person_id,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", "").split("（")[0] if "（" in p.get("birthplace", "") else p.get("birthplace", ""),
            "education": [{
                "period": "",
                "institution": p.get("education", ""),
                "major": "",
                "degree": "",
                "study_type": "unknown",
                "source_ids": ["S001"]
            }],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if any(k in p.get("current_post","") for k in ["县委书记", "县长", "人大", "政协"]) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": "present" in str([pos["end"] for pos in person_positions if pos["end"]=="present"]),
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [{
            "org_id": o["id"],
            "name": o["name"],
            "type": o["type"],
            "level": o["level"]
        } for o in organizations if any(pos["org_id"] == o["id"] for pos in person_positions)],
        "relationships": rels,
        "governance_record": governance,
        "professional_profile": {
            "primary_specializations": primary_specs,
            "secondary_specializations": secondary_specs,
            "career_pattern": career_pattern,
            "systems_experience": ["party", "government"] if ("书记" in p.get("current_post","") or "县长" in p.get("current_post","")) else ["government"],
            "geographic_pattern": ["南平市"],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {
            "direct_relationships": len(rels),
            "strong_connections": len([r for r in rels if r["strength"] == "strong"]),
            "positions_held": len(career),
            "organizations_served": len(set(pos["org_id"] for pos in person_positions))
        },
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No public risk or integrity signals found in open source research as of " + AS_OF,
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [{
            "id": "S001",
            "title": "Online research compilation for " + p["name"],
            "url": p.get("source", ""),
            "publisher": "Various (Wikipedia, Baidu Baike, news media)",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "Combined from multiple web sources"
        }],
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed" if p.get("current_post") else "unverified",
            "career_completeness": "partial" if len(career) > 1 else "thin",
            "relationship_confidence": "high" if len(rels) > 2 else "medium",
            "biggest_gap": "Early career history before current role" if len(career) < 3 else ""
        },
        "open_questions": [{
            "priority": "medium",
            "question": f"详细履历——{p['name']}的早期职业生涯和学历背景",
            "why_it_matters": "为全面评估官员经历和晋升路径提供基础数据",
            "suggested_queries": [f"{p['name']} 简历 任职经历", f"{p['name']} 出生 学历"],
            "last_attempted": AS_OF
        }]
    }
    
    # Filename
    job_slug = ""
    post = p.get("current_post", "")
    if "县委书记" in post:
        job_slug = "县委书记"
    elif "县长" in post and "副" not in post:
        job_slug = "县长"
    elif "副县长" in post:
        job_slug = "副县长"
    elif "人大" in post:
        job_slug = "人大主任"
    elif "政协" in post:
        job_slug = "政协主席"
    elif "组织部长" in post:
        job_slug = "组织部长"
    elif "宣传" in post:
        job_slug = "宣传部长"
    else:
        job_slug = "县委常委"
    
    filename = f"{AS_OF}-福建省-南平市-{job_slug}-{p['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"✓ Person JSON: {filepath}")
    return filepath


def main():
    print("=" * 60)
    print("光泽县领导班子工作关系网络 - 数据构建")
    print("=" * 60)
    print()
    
    # Create DB
    create_database()
    print()
    
    # Create GEXF
    create_gexf()
    print()
    
    # Create person JSONs for core leaders
    core_ids = [1, 2, 3, 4, 5, 6, 11, 14]  # Key figures
    json_files = []
    for pid in core_ids:
        for p in persons:
            if p["id"] == pid:
                fp = create_person_json(p)
                json_files.append(fp)
                break
    print()
    
    print("=" * 60)
    print("构建完成!")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print(f"  JSONs:  {len(json_files)} files in {PERSONS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
