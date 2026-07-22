#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Songxi County (松溪县), Nanping City, Fujian Province.

Covers: Party Secretary (县委书记), County Mayor (县长), key deputy positions
(县委副书记, 常务副县长, 组织部长, 纪委书记, 政法委书记),
predecessor/successor chains, and the county-level leadership network.

Sources:
- People.cn (福建频道): Appointment announcements
- Southeast Network (东南网): Local news
- Songxi News Network (松溪新闻网): Official local media
- Wikipedia (Chinese): 松溪县

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_松溪县")
DB_PATH = os.path.join(TMP, "松溪县_network.db")
GEXF_PATH = os.path.join(TMP, "松溪县_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 吴伟 — 松溪县委书记 (2026.2-)
    {"id":1,"name":"吴伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委书记","current_org":"中共松溪县委员会",
     "source":"http://www.songxixww.com/2026-02/09/content_2309136.htm"},
    # 张田怡 — 松溪县人民政府代县长/县长 (2025.5-)
    {"id":2,"name":"张田怡","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县人民政府县长","current_org":"松溪县人民政府",
     "source":"http://www.songxixww.com/2025-05/29/content_2216294.htm"},

    # ── Other top leaders ──
    # 谢利富 — 松溪县人大常委会主任
    {"id":3,"name":"谢利富","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县人大常委会主任","current_org":"松溪县人民代表大会常务委员会",
     "source":"http://www.songxixww.com/2025-05/28/content_2215491.htm"},

    # ── Key deputies (the 5 target positions) ──

    # 吴孔盛 — 县委副书记 (即将离任/已离任，拟升市级正处长级)
    {"id":4,"name":"吴孔盛","gender":"男","ethnicity":"汉族","birth":"1977-10","birthplace":"",
     "education":"大学","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委副书记（拟任市委工作机关正处长级）","current_org":"中共松溪县委员会",
     "source":"http://fj.people.com.cn/n2/2025/0626/c181466-41272638.html"},

    # 万超 — 县委常委、常务副县长
    {"id":5,"name":"万超","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委常委、常务副县长","current_org":"松溪县人民政府",
     "source":"http://np.fjsen.com/wap/2023-08/01/content_31376438.htm"},

    # 许华荣 — 县委常委、组织部部长
    {"id":6,"name":"许华荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委常委、组织部部长","current_org":"中共松溪县委组织部",
     "source":"https://np.fjsen.com/wap/2025-05/23/content_31910032.htm"},

    # 陈远浩 — 县委常委（推测为纪委书记）
    {"id":7,"name":"陈远浩","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委常委","current_org":"中共松溪县委员会",
     "source":"http://www.songxixww.com/2026-02/09/content_2309136.htm"},

    # 吴芳 — 县委常委、统战部部长、副县长
    {"id":8,"name":"吴芳","gender":"女","ethnicity":"汉族","birth":"1980-12","birthplace":"",
     "education":"在职大学","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委常委、统战部部长、副县长","current_org":"中共松溪县委统战部",
     "source":"http://fj.people.com.cn/n2/2025/0626/c181466-41272638.html"},

    # 吴其福 — 县委常委
    {"id":9,"name":"吴其福","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委常委","current_org":"中共松溪县委员会",
     "source":"http://www.songxixww.com/2026-02/09/content_2309136.htm"},

    # 陈建斌 — 县委常委、宣传部部长
    {"id":10,"name":"陈建斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县委常委、宣传部部长","current_org":"中共松溪县委宣传部",
     "source":"http://np.fjsen.com/wap/2022-02/22/content_30965910.htm"},

    # ── Predecessors — 县委书记 ──
    # 张行书 — 前任松溪县委书记 (2021-2026)
    {"id":11,"name":"张行书","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://np.fjsen.com/wap/2025-07/02/content_31935848.htm"},

    # ── Predecessors — 县长 ──
    # 吴英杰 — 前任松溪县长
    {"id":12,"name":"吴英杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"http://np.fjsen.com/wap/2023-08/01/content_31376438.htm"},
    # 苏建旗 — 更早前任县长 (2021年前)
    {"id":13,"name":"苏建旗","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"http://np.fjsen.com/2021-01/08/content_30605838.htm"},

    # ── Predecessors — 副书记 ──
    # 王贵 — 前任松溪县委副书记 (2021年前)
    {"id":14,"name":"王贵","gender":"男","ethnicity":"汉族","birth":"1981-06","birthplace":"浙江省永嘉县（福建武夷山出生）",
     "education":"福建农林大学，在职研究生，农业推广硕士",
     "party_join":"中共党员","work_start":"",
     "current_post":"光泽县委书记","current_org":"中共光泽县委员会",
     "source":"https://baike.baidu.com/item/%E7%8E%8B%E8%B4%B5/58525535"},

    # ── Predecessors — 组织部长 ──
    # 邓华梁 — 前任组织部长 (2022)
    {"id":15,"name":"邓华梁","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"http://np.fjsen.com/wap/2022-02/22/content_30965910.htm"},
    # 张勤 — 更早前任组织部长 (2020)
    {"id":16,"name":"张勤","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"http://np.fjsen.com/wap/2020-08/24/content_30455390.htm"},

    # ── Predecessors — 纪委书记 ──
    # 虞朝兵 — 前任纪委书记 (2020)
    {"id":17,"name":"虞朝兵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"松溪县政协主席","current_org":"政协松溪县委员会",
     "source":"http://np.fjsen.com/wap/2020-08/24/content_30455390.htm"},

    # ── Predecessors — 常务副县长 ──
    # 谢利富 — 前任常务副县长 (2021)
    # (same person as id=3, already listed as 人大主任)
]

# =========================================================================
# ORGANIZATIONS (deduplicate with existing data)
# =========================================================================
organizations = [
    {"id":1,"name":"中共松溪县委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市松溪县"},
    {"id":2,"name":"松溪县人民政府","type":"政府","level":"县级","parent":"南平市人民政府","location":"福建省南平市松溪县"},
    {"id":3,"name":"松溪县人民代表大会常务委员会","type":"人大","level":"县级","parent":"","location":"福建省南平市松溪县"},
    {"id":4,"name":"政协松溪县委员会","type":"政协","level":"县级","parent":"","location":"福建省南平市松溪县"},
    {"id":5,"name":"中共松溪县委组织部","type":"党委","level":"县级","parent":"中共松溪县委员会","location":"福建省南平市松溪县"},
    {"id":6,"name":"中共松溪县委宣传部","type":"党委","level":"县级","parent":"中共松溪县委员会","location":"福建省南平市松溪县"},
    {"id":7,"name":"中共松溪县委统战部","type":"党委","level":"县级","parent":"中共松溪县委员会","location":"福建省南平市松溪县"},
    {"id":8,"name":"中共南平市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省南平市"},
    {"id":9,"name":"南平市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省南平市"},
    {"id":10,"name":"中共光泽县委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市光泽县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 吴伟 — 县委书记 (current)
    {"person_id":1,"org_id":1,"title":"松溪县委书记","start":"2026-01","end":"present","rank":"正处级",
     "note":"2026年1-2月间任松溪县委书记，接替张行书"},

    # 张田怡 — 县长 (current)
    {"person_id":2,"org_id":2,"title":"松溪县人民政府县长","start":"2025-05","end":"present","rank":"正处级",
     "note":"2025年5月任松溪县代县长，后去代转正"},
    {"person_id":2,"org_id":1,"title":"松溪县委副书记","start":"2025-05","end":"present","rank":"副处级",
     "note":"2025年5月起任松溪县委副书记、代县长"},

    # 谢利富 — 人大主任 (current)
    {"person_id":3,"org_id":3,"title":"松溪县人大常委会主任","start":"2021-11","end":"present","rank":"正处级",
     "note":"2021年11月已任松溪县人大常委会党组书记，此前任县委常委、常务副县长"},

    # 吴孔盛 — 县委副书记 (即将离任)
    {"person_id":4,"org_id":1,"title":"松溪县委副书记、三级调研员","start":"2021","end":"2025-06","rank":"副处级",
     "note":"2025年6月公示拟任南平市委工作机关正处长级职务"},
    {"person_id":4,"org_id":8,"title":"南平市委工作机关正处长级","start":"2025-06","end":"present","rank":"正处级",
     "note":"2025年6月任前公示，拟任市委工作机关正处长级职务"},

    # 万超 — 常务副县长
    {"person_id":5,"org_id":2,"title":"松溪县委常委、常务副县长","start":"2022","end":"present","rank":"副处级",
     "note":"最早2022年5月以常务副县长身份公开出席活动"},

    # 许华荣 — 组织部长
    {"person_id":6,"org_id":5,"title":"松溪县委常委、组织部部长","start":"2025","end":"present","rank":"副处级",
     "note":"最早2025年5月以组织部长身份公开出席活动"},

    # 陈远浩 — 县委常委
    {"person_id":7,"org_id":1,"title":"松溪县委常委","start":"2026","end":"present","rank":"副处级",
     "note":"2026年2月以县委常委身份出席述职评议会议，具体分工待确认"},

    # 吴芳 — 统战部长/副县长
    {"person_id":8,"org_id":7,"title":"松溪县委常委、统战部部长","start":"2022","end":"present","rank":"副处级",
     "note":"2022年2月以统战部长身份出席县委工作会议"},
    {"person_id":8,"org_id":2,"title":"松溪县人民政府副县长","start":"2025","end":"present","rank":"副处级",
     "note":"兼任副县长，2025年6月公示拟进一步使用"},

    # 吴其福 — 县委常委
    {"person_id":9,"org_id":1,"title":"松溪县委常委","start":"2026","end":"present","rank":"副处级",
     "note":"2026年2月以县委常委身份出席述职评议会议，具体分工待确认"},

    # 陈建斌 — 宣传部长
    {"person_id":10,"org_id":6,"title":"松溪县委常委、宣传部部长","start":"2022","end":"present","rank":"副处级",
     "note":"2022年2月以宣传部长身份出席县委工作会议"},

    # 张行书 — 前任县委书记
    {"person_id":11,"org_id":1,"title":"松溪县委书记","start":"2021","end":"2025-12","rank":"正处级",
     "note":"2021年任松溪县委书记，2025年底/2026年初卸任"},

    # 吴英杰 — 前任县长
    {"person_id":12,"org_id":2,"title":"松溪县人民政府县长","start":"2021","end":"2025-05","rank":"正处级",
     "note":"2021年11月任代县长，后去代转正，2025年5月卸任"},
    {"person_id":12,"org_id":1,"title":"松溪县委副书记","start":"2021-11","end":"2025-05","rank":"副处级",
     "note":"2021年11月任松溪县委副书记、代县长"},

    # 苏建旗 — 更早前任县长
    {"person_id":13,"org_id":2,"title":"松溪县人民政府县长","start":"","end":"2021","rank":"正处级",
     "note":"2021年1月仍以县长身份出席活动"},

    # 王贵 — 前任副书记
    {"person_id":14,"org_id":1,"title":"松溪县委副书记","start":"","end":"2021-06","rank":"副处级",
     "note":"2021年6月前曾任松溪县委副书记，后调任光泽县长"},
    {"person_id":14,"org_id":1,"title":"松溪县委常委、组织部部长","start":"","end":"","rank":"副处级",
     "note":"王贵曾任松溪县委常委、组织部部长"},

    # 邓华梁 — 前任组织部长
    {"person_id":15,"org_id":5,"title":"松溪县委常委、组织部部长","start":"2022","end":"","rank":"副处级",
     "note":"2022年2月以组织部长身份出席县委工作会议"},

    # 张勤 — 更早前任组织部长
    {"person_id":16,"org_id":5,"title":"松溪县委常委、组织部部长","start":"","end":"2020","rank":"副处级",
     "note":"2020年8月以组织部长身份作动员讲话"},

    # 虞朝兵 — 前任纪委书记
    {"person_id":17,"org_id":1,"title":"松溪县委常委、县纪委书记、县监委主任","start":"","end":"2021","rank":"副处级",
     "note":"2020年8月以纪委书记身份主持会议"},
    {"person_id":17,"org_id":4,"title":"松溪县政协主席","start":"2021-11","end":"present","rank":"正处级",
     "note":"2021年11月已任松溪县政协党组书记"},

    # 谢利富 — 前任常务副县长 (also id=3)
    {"person_id":3,"org_id":2,"title":"松溪县委常委、常务副县长","start":"","end":"2021","rank":"副处级",
     "note":"2021年1月以常务副县长身份出席绿色发展考评推进会"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 吴伟 ↔ 张行书 (县委书记接替)
    {"person_a":1,"person_b":11,"type":"predecessor_successor",
     "context":"吴伟接替张行书任松溪县委书记",
     "overlap_org":"中共松溪县委员会","overlap_period":"2026-01","strength":"strong"},

    # 张田怡 ↔ 吴英杰 (县长接替)
    {"person_a":2,"person_b":12,"type":"predecessor_successor",
     "context":"张田怡接替吴英杰任松溪县长",
     "overlap_org":"松溪县人民政府","overlap_period":"2025-05","strength":"strong"},

    # 吴英杰 ↔ 苏建旗 (县长接替)
    {"person_a":12,"person_b":13,"type":"predecessor_successor",
     "context":"吴英杰接替苏建旗任松溪县长",
     "overlap_org":"松溪县人民政府","overlap_period":"2021","strength":"strong"},

    # 吴孔盛 ↔ 张行书 (上下级)
    {"person_a":4,"person_b":11,"type":"superior_subordinate",
     "context":"吴孔盛任副书记时，张行书任书记",
     "overlap_org":"中共松溪县委员会","overlap_period":"2021-2025","strength":"strong"},

    # 吴孔盛 ↔ 王贵 (副书记接替)
    {"person_a":4,"person_b":14,"type":"predecessor_successor",
     "context":"吴孔盛接替王贵任松溪县委副书记",
     "overlap_org":"中共松溪县委员会","overlap_period":"2021","strength":"strong"},

    # 万超 ↔ 谢利富 (常务副县长接替)
    {"person_a":5,"person_b":3,"type":"predecessor_successor",
     "context":"万超接替谢利富任松溪县委常委、常务副县长",
     "overlap_org":"松溪县人民政府","overlap_period":"2022","strength":"strong"},

    # 许华荣 ↔ 邓华梁 (组织部长接替)
    {"person_a":6,"person_b":15,"type":"predecessor_successor",
     "context":"许华荣接替邓华梁任松溪县委组织部部长",
     "overlap_org":"中共松溪县委组织部","overlap_period":"2025","strength":"strong"},

    # 邓华梁 ↔ 张勤 (组织部长接替)
    {"person_a":15,"person_b":16,"type":"predecessor_successor",
     "context":"邓华梁接替张勤任松溪县委组织部部长",
     "overlap_org":"中共松溪县委组织部","overlap_period":"2022","strength":"strong"},

    # 虞朝兵 ↔ 陈远浩 (推测纪委书记接替)
    {"person_a":17,"person_b":7,"type":"predecessor_successor",
     "context":"虞朝兵转任政协后，陈远浩可能接任纪委书记",
     "overlap_org":"中共松溪县委员会","overlap_period":"2021-2022","strength":"medium"},

    # 张行书 ↔ 吴英杰 (党政搭档)
    {"person_a":11,"person_b":12,"type":"overlap",
     "context":"张行书任县委书记期间，吴英杰任县长",
     "overlap_org":"中共松溪县委员会","overlap_period":"2021-2025","strength":"strong"},

    # 吴芳 ↔ 吴孔盛 (共事)
    {"person_a":8,"person_b":4,"type":"overlap",
     "context":"吴芳任统战部长期间，吴孔盛任副书记",
     "overlap_org":"中共松溪县委员会","overlap_period":"2022-2025","strength":"medium"},

    # 谢利富 ↔ 虞朝兵 (同届转岗)
    {"person_a":3,"person_b":17,"type":"overlap",
     "context":"谢利富由常务副县长转人大主任，虞朝兵由纪委书记转政协主席，2021年同期转岗",
     "overlap_org":"中共松溪县委员会","overlap_period":"2021-11","strength":"medium"},

    # 吴伟 ↔ 张田怡 (现任党政搭档)
    {"person_a":1,"person_b":2,"type":"overlap",
     "context":"吴伟任县委书记，张田怡任县长，现任党政搭档",
     "overlap_org":"中共松溪县委员会","overlap_period":"2025-05至今","strength":"strong"},

    # 王贵 ↔ 张行书 (上下级)
    {"person_a":14,"person_b":11,"type":"superior_subordinate",
     "context":"王贵任松溪县委副书记期间，张行书任县委书记",
     "overlap_org":"中共松溪县委员会","overlap_period":"2021-06前","strength":"strong"},
]


# =========================================================================
# BUILD FUNCTIONS - Same pattern as 光泽县
# =========================================================================

def create_database():
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
    
    for o in organizations:
        c.execute('''INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)''',
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))
    
    for pos in positions:
        c.execute('''INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)''',
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))
    
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
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    
    def person_color(p):
        post = p.get("current_post", "")
        name = p["name"]
        if "书记" in post and "纪委" not in post and name in ("吴伟", "张行书"):
            return "255,50,50"
        elif "县长" in post or ("政府" in post and "常务" in post):
            return "50,100,255"
        elif "人大" in post:
            return "200,255,255"
        elif "政协" in post:
            return "255,240,200"
        elif "纪委" in post:
            return "255,150,50"
        elif "组织" in post:
            return "150,255,150"
        elif "统战" in post:
            return "200,150,255"
        else:
            return "100,100,100"
    
    def is_top_leader(p):
        return p["name"] in ("吴伟", "张田怡", "张行书", "吴英杰")
    
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
        else:
            return "200,200,200"
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>松溪县领导班子工作关系网络 - 福建省南平市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')
    
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('      <attribute id="4" title="strength" type="string"/>')
    lines.append('    </attributes>')
    
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        note = pos.get("note", "")
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    for r in relationships:
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
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


def main():
    print("=" * 60)
    print("松溪县领导班子工作关系网络 - 数据构建")
    print("=" * 60)
    print()
    
    create_database()
    print()
    
    create_gexf()
    print()
    
    print("=" * 60)
    print("构建完成!")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
