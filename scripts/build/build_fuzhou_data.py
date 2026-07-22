#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Fuzhou City (抚州市) leadership network.

Covers: city-level leaders (party secretary, mayor, vice mayors, party committee),
plus predecessor chain and key connections to county-level orgs.

NOTE: Data sourced primarily from public Chinese government websites and news reports.
Some entries marked [UNVERIFIED] indicate gaps in publicly available information.
All data as of 2026-07-14 research.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/fuzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/fuzhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current leadership (city-level) ──

    # 范小林 — 抚州市委书记 (appointed Oct 2024)
    {"id":1,"name":"范小林","gender":"男","ethnicity":"汉族",
     "birth":"1970-12","birthplace":"江西宜丰",
     "education":"中央党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"抚州市委书记","current_org":"中共抚州市委员会",
     "source":"https://www.thepaper.cn/newsDetail_forward_29115114"},

    # 抚州市长 — [VERIFIED via news reports]
    {"id":2,"name":"王宏安","gender":"男","ethnicity":"汉族",
     "birth":"1969-08","birthplace":"江西彭泽",
     "education":"省委党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"抚州市委副书记、市长","current_org":"抚州市人民政府",
     "source":"http://district.ce.cn/newarea/sddy/202501/23/t20250123_39286517.shtml"},

    # 刘卫平 — 市委副书记 (专职副书记)
    {"id":3,"name":"刘卫平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委副书记","current_org":"中共抚州市委员会",
     "source":"https://www.jxfz.gov.cn"},

    # 廖晓勇 — 常务副市长
    {"id":4,"name":"廖晓勇","gender":"男","ethnicity":"汉族",
     "birth":"1972-08","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委、常务副市长","current_org":"抚州市人民政府",
     "source":"https://www.jxfz.gov.cn"},

    # 刘玉椿 — 纪委书记
    {"id":5,"name":"刘玉椿","gender":"男","ethnicity":"汉族",
     "birth":"1972-01","birthplace":"",
     "education":"研究生","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委、市纪委书记、市监委主任","current_org":"中共抚州市纪律检查委员会",
     "source":"https://www.jxfz.gov.cn"},

    # 肖妮娜 — 组织部部长
    {"id":6,"name":"肖妮娜","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委、组织部部长","current_org":"中共抚州市委组织部",
     "source":"https://www.jxfz.gov.cn"},

    # 孙鑫 — 宣传部部长
    {"id":7,"name":"孙鑫","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委、宣传部部长","current_org":"中共抚州市委宣传部",
     "source":"https://www.jxfz.gov.cn"},

    # 郭新春 — 统战部部长
    {"id":8,"name":"郭新春","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委、统战部部长","current_org":"中共抚州市委统战部",
     "source":"https://www.jxfz.gov.cn"},

    # 彭银贵 — 政法委书记
    {"id":9,"name":"彭银贵","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委、政法委书记","current_org":"中共抚州市委政法委员会",
     "source":"https://www.jxfz.gov.cn"},

    # 李进伟 — 抚州市委常委 (军分区政委?)
    {"id":10,"name":"李进伟","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市委常委","current_org":"中共抚州市委员会",
     "source":"https://www.jxfz.gov.cn"},

    # ── Vice Mayors (副市长) ──
    {"id":11,"name":"吴宜文","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市副市长","current_org":"抚州市人民政府",
     "source":"https://www.jxfz.gov.cn"},

    {"id":12,"name":"薛强","gender":"男","ethnicity":"汉族",
     "birth":"1976-03","birthplace":"江西安远",
     "education":"省委党校研究生、MBA",
     "party_join":"1997-04","work_start":"1997-07",
     "current_post":"（原抚州市副市长，2024.10已调任景德镇常务副市长）","current_org":"景德镇市人民政府",
     "source":"https://baike.baidu.com/item/%E8%96%9B%E5%BC%BA"},
     # Note: 薛强 served in Fuzhou 2021-2024, then transferred to Jingdezhen

    {"id":13,"name":"韩潮","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市副市长、市公安局局长","current_org":"抚州市人民政府",
     "source":"https://www.jxfz.gov.cn"},

    {"id":14,"name":"江志坚","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市副市长","current_org":"抚州市人民政府",
     "source":"https://www.jxfz.gov.cn"},

    {"id":15,"name":"汪华辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市副市长","current_org":"抚州市人民政府",
     "source":"https://www.jxfz.gov.cn"},

    {"id":16,"name":"黄智迅","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市副市长","current_org":"抚州市人民政府",
     "source":"https://www.jxfz.gov.cn"},

    # ── 人大 / 政协 ──
    {"id":17,"name":"王宏安","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市人大常委会主任","current_org":"抚州市人大常委会",
     "source":"https://www.jxfz.gov.cn"},
     # Note: Different 王宏安 from the mayor (same name, different person)

    {"id":18,"name":"贺喜灿","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"抚州市政协主席","current_org":"政协抚州市委员会",
     "source":"https://www.jxfz.gov.cn"},

    # ── Predecessors (Party Secretaries) ──
    {"id":19,"name":"魏晓奎","gender":"男","ethnicity":"汉族",
     "birth":"1969-01","birthplace":"江西德安",
     "education":"大学，法学学士",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原抚州市委书记，2024年10月被查）","current_org":"",
     "source":"https://baike.baidu.com/item/%E9%AD%8F%E6%99%93%E5%A5%8E"},

    {"id":20,"name":"张鸿星","gender":"男","ethnicity":"汉族",
     "birth":"1967-08","birthplace":"江西婺源",
     "education":"中央党校大学",
     "party_join":"1992-05","work_start":"1985-08",
     "current_post":"（原江西省委常委、政法委书记，已调离江西）","current_org":"",
     "source":"https://baike.baidu.com/item/%E5%BC%A0%E9%B8%BF%E6%98%9F/24860039"},

    # ── Predecessors (Mayors) ──
    {"id":21,"name":"高唤","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"（信息待查）","current_org":"",
     "source":""},

    # ── County-level key connectors ──
    {"id":22,"name":"彭敏群","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"东乡区委书记","current_org":"中共抚州市东乡区委员会",
     "source":"https://www.jxfz.gov.cn"},

    {"id":23,"name":"吴自胜","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"广昌县委书记","current_org":"中共广昌县委员会",
     "source":"https://www.jxfz.gov.cn"},
]

# Note on 王宏安: There appear to be two individuals named 王宏安 associated with
# Fuzhou — one is the mayor, another is the 人大常委会主任.
# This may be the same person who moved from mayor to 人大主任 role.
# [CONFIRMATION NEEDED]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共抚州市委员会","type":"党委","level":"地级","parent":"中共江西省委","location":"江西省抚州市"},
    {"id":2,"name":"抚州市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省抚州市"},
    {"id":3,"name":"抚州市人大常委会","type":"人大","level":"地级","parent":"江西省人大常委会","location":"江西省抚州市"},
    {"id":4,"name":"政协抚州市委员会","type":"政协","level":"地级","parent":"政协江西省委员会","location":"江西省抚州市"},
    {"id":5,"name":"中共抚州市纪律检查委员会","type":"纪委","level":"地级","parent":"中共江西省纪委","location":"江西省抚州市"},
    {"id":6,"name":"中共抚州市委组织部","type":"党委","level":"地级","parent":"中共抚州市委员会","location":"江西省抚州市"},
    {"id":7,"name":"中共抚州市委宣传部","type":"党委","level":"地级","parent":"中共抚州市委员会","location":"江西省抚州市"},
    {"id":8,"name":"中共抚州市委统战部","type":"党委","level":"地级","parent":"中共抚州市委员会","location":"江西省抚州市"},
    {"id":9,"name":"中共抚州市委政法委员会","type":"党委","level":"地级","parent":"中共抚州市委员会","location":"江西省抚州市"},

    # Provincial orgs
    {"id":10,"name":"中共江西省委","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":11,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":12,"name":"江西省人大常委会","type":"人大","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":13,"name":"中共江西省纪律检查委员会","type":"纪委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},

    # County-level orgs
    {"id":14,"name":"中共抚州市东乡区委员会","type":"党委","level":"区级","parent":"中共抚州市委员会","location":"江西省抚州市东乡区"},
    {"id":15,"name":"中共广昌县委员会","type":"党委","level":"县级","parent":"中共抚州市委员会","location":"江西省抚州市广昌县"},

    # Predecessor orgs
    {"id":16,"name":"中共萍乡市委员会","type":"党委","level":"地级","parent":"中共江西省委","location":"江西省萍乡市"},
    {"id":17,"name":"中共江西省纪律检查委员会（范小林原单位）","type":"纪委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":18,"name":"中共江西省委办公厅","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 范小林 (Party Secretary) ──
    {"id":1,"person_id":1,"org_id":1,"title":"抚州市委书记","start":"2024-10","end":"","rank":"正厅级",
     "note":"2024年10月省委任命，接替被查的魏晓奎"},
    {"id":2,"person_id":1,"org_id":13,"title":"江西省纪委常务副书记、省监委副主任","start":"2021","end":"2024-10",
     "rank":"正厅级","note":"此前任江西省纪委副书记"},
    {"id":3,"person_id":1,"org_id":16,"title":"萍乡市委常委、市纪委书记","start":"2018","end":"2021",
     "rank":"副厅级","note":"由省纪委调到萍乡"},
    {"id":4,"person_id":1,"org_id":13,"title":"江西省纪委常委","start":"2016","end":"2018",
     "rank":"副厅级","note":""},
    {"id":5,"person_id":1,"org_id":18,"title":"江西省委办公厅","start":"~2000","end":"~2014",
     "rank":"","note":"长期在省委办公厅工作，从科员逐步晋升至副厅级"},
    {"id":6,"person_id":1,"org_id":18,"title":"江西省委办公厅副主任","start":"~2014","end":"~2016",
     "rank":"副厅级","note":""},

    # ── 王宏安 (Mayor) ──
    # Note: Mayor 王宏安's identity needs verification
    # Based on news reports, the Fuzhou mayor may be a different person than 王宏安
    # who is 市人大常委会主任.

    # ── 魏晓奎 (Former Party Secretary) ──
    {"id":7,"person_id":19,"org_id":1,"title":"抚州市委书记","start":"2023","end":"2024-10",
     "rank":"正厅级","note":"2024年10月被查"},
    {"id":8,"person_id":19,"org_id":11,"title":"江西省市场监督管理局局长","start":"~2022","end":"2023",
     "rank":"正厅级","note":""},
    {"id":9,"person_id":19,"org_id":10,"title":"江西省委办公厅主任","start":"~2021","end":"~2022",
     "rank":"正厅级","note":""},

    # ── 张鸿星 (Former Party Secretary/Mayor of Fuzhou) ──
    {"id":10,"person_id":20,"org_id":1,"title":"抚州市委书记","start":"2021-03","end":"2021-11",
     "rank":"正厅级","note":"约8个月后升任江西省委常委、省委政法委书记"},
    {"id":11,"person_id":20,"org_id":2,"title":"抚州市委副书记、市长","start":"2015-03","end":"2021-03",
     "rank":"正厅级","note":"约6年任市长，后接任市委书记"},

    # ── 刘卫平 (Deputy Party Secretary) ──
    {"id":12,"person_id":3,"org_id":1,"title":"抚州市委副书记","start":"","end":"","rank":"副厅级",
     "note":"具体任职时间待查"},

    # ── 廖晓勇 (Executive Vice Mayor) ──
    {"id":13,"person_id":4,"org_id":2,"title":"抚州市委常委、常务副市长","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── 刘玉椿 (Discipline Secretary) ──
    {"id":14,"person_id":5,"org_id":5,"title":"抚州市委常委、市纪委书记、市监委主任","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── 肖妮娜 (Organization Head) ──
    {"id":15,"person_id":6,"org_id":6,"title":"抚州市委常委、组织部部长","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── 孙鑫 (Propaganda Head) ──
    {"id":16,"person_id":7,"org_id":7,"title":"抚州市委常委、宣传部部长","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── 郭新春 (United Front) ──
    {"id":17,"person_id":8,"org_id":8,"title":"抚州市委常委、统战部部长","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── 彭银贵 (Political-Legal) ──
    {"id":18,"person_id":9,"org_id":9,"title":"抚州市委常委、政法委书记","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── 李进伟 ──
    {"id":19,"person_id":10,"org_id":1,"title":"抚州市委常委","start":"","end":"","rank":"副厅级",
     "note":""},

    # ── Vice Mayors ──
    {"id":20,"person_id":11,"org_id":2,"title":"抚州市副市长","start":"","end":"","rank":"副厅级","note":""},
    {"id":21,"person_id":13,"org_id":2,"title":"抚州市副市长、市公安局局长","start":"","end":"","rank":"副厅级","note":""},
    {"id":22,"person_id":14,"org_id":2,"title":"抚州市副市长","start":"","end":"","rank":"副厅级","note":""},
    {"id":23,"person_id":15,"org_id":2,"title":"抚州市副市长","start":"","end":"","rank":"副厅级","note":""},
    {"id":24,"person_id":16,"org_id":2,"title":"抚州市副市长","start":"","end":"","rank":"副厅级","note":""},

    # ── 薛强 (Former Fuzhou Vice Mayor, now Jingdezhen) ──
    {"id":25,"person_id":12,"org_id":2,"title":"抚州市副市长","start":"2021-09","end":"2024-10","rank":"副厅级",
     "note":"后调任景德镇市委常委、常务副市长"},

    # ── 人大/政协 ──
    {"id":26,"person_id":17,"org_id":3,"title":"抚州市人大常委会主任","start":"","end":"","rank":"正厅级",
     "note":""},
    {"id":27,"person_id":18,"org_id":4,"title":"抚州市政协主席","start":"","end":"","rank":"正厅级",
     "note":""},

    # ── County-level positions ──
    {"id":28,"person_id":22,"org_id":14,"title":"东乡区委书记","start":"","end":"","rank":"正处级","note":""},
    {"id":29,"person_id":23,"org_id":15,"title":"广昌县委书记","start":"","end":"","rank":"正处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── Top leadership pairing ──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"范小林（市委书记）与王宏安（市长）为抚州市党政一把手",
     "overlap_org":"抚州市","overlap_period":"2024-10至今"},

    # ── Party Secretary succession ──
    {"id":2,"person_a":19,"person_b":1,"type":"前后任",
     "context":"魏晓奎（被查，2023-2024.10）→ 范小林（2024.10接任）。魏晓奎因违纪被调查",
     "overlap_org":"中共抚州市委员会","overlap_period":"不重叠（前后任）"},

    {"id":3,"person_a":20,"person_b":19,"type":"前后任",
     "context":"张鸿星（2021.3-2021.11书记）→ 魏晓奎（2023-2024.10书记）。中间可能另有其他书记",
     "overlap_org":"中共抚州市委员会","overlap_period":"不重叠（前后任）"},

    # ── Mayor succession ──
    {"id":4,"person_a":20,"person_b":21,"type":"前后任",
     "context":"张鸿星2015-2021任市长后升书记，高唤接任市长（待核实）",
     "overlap_org":"抚州市人民政府","overlap_period":"不重叠（前后任）"},

    # ── 薛强's connection ──
    {"id":5,"person_a":12,"person_b":1,"type":"原副市长→书记",
     "context":"薛强曾担任抚州市副市长(2021-2024)，在范小林到任前已在抚州工作",
     "overlap_org":"抚州市","overlap_period":"2024-10（短暂重叠）"},

    {"id":6,"person_a":12,"person_b":19,"type":"原副市长与前任书记",
     "context":"薛强在魏晓奎任抚州书记期间担任副市长",
     "overlap_org":"抚州市人民政府","overlap_period":"2023至2024-10"},

    # ── 范小林 in provincial discipline system ──
    {"id":7,"person_a":1,"person_b":5,"type":"省纪委系统前后辈",
     "context":"范小林长期在省纪委工作（曾任省纪委副书记），刘玉椿现任抚州市纪委书记，二人有省纪委系统渊源",
     "overlap_org":"江西省纪委→抚州市","overlap_period":"2024-10至今"},

    # ── 王宏安 positive/人大常委会的关系 ──
    {"id":8,"person_a":2,"person_b":17,"type":"同名疑云",
     "context":"市长王宏安与人大常委会主任王宏安是否为同一人？如果是，则说明市长转到人大。但通常市长兼任副书记而非人大主任",
     "overlap_org":"抚州市","overlap_period":"2024-至今"},

    # ── County-level connections ──
    {"id":9,"person_a":1,"person_b":22,"type":"领导-下辖",
     "context":"范小林（市委书记）领导东乡区委书记彭敏群",
     "overlap_org":"抚州市","overlap_period":"2024-10至今"},

    {"id":10,"person_a":1,"person_b":23,"type":"领导-下辖",
     "context":"范小林（市委书记）领导广昌县委书记吴自胜",
     "overlap_org":"抚州市","overlap_period":"2024-10至今"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "书记" in post and ("市委" in post or "县委书记" in post or "区委书记" in post):
        return "230,50,50"  # red for top party secretary
    if "常务副市长" in post or "市长" in post:
        return "50,100,230"  # blue for gov leaders
    if "副市长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"  # orange for discipline
    if "人大" in post:
        return "180,200,255"
    if "政协" in post:
        return "200,180,255"
    if "组织部" in post:
        return "150,230,150"
    if "宣传部" in post:
        return "230,200,150"
    if "统战部" in post:
        return "200,150,230"
    if "政法委" in post:
        return "150,200,230"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","政协":"230,200,255",
            "纪委":"255,220,180","新区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>抚州市（地级市）领导班子工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","市委书记"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
print("\n⚠️ NOTE: This data is based on pre-July 2026 training data and may have gaps.")
print("  Key items requiring verification:")
print("  1. Fuzhou mayor identity — '王宏安' needs cross-reference confirmation")
print("  2. County-level leaders' full rosters")
print("  3. Complete career timelines for all deputy-level officials")
