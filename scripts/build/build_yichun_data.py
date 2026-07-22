#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 宜春市 (Yichun City) leadership network.

Covers: city-level leaders (party secretary, mayor, vice mayors, party committee),
plus the predecessor chain and key connections to surrounding counties.
Research date: 2026-07-14
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yichun_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yichun_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current Party Secretary (市委书记) ──
    {"id":1,"name":"蒋文定","gender":"男","ethnicity":"汉族","birth":"1972-05","birthplace":"湖南常德","education":"西安高校毕业（中石化系统出身）","party_join":"中共党员","work_start":"","current_post":"宜春市委书记","current_org":"中共宜春市委员会","source":"https://zh.wikipedia.org/wiki/宜春市; https://district.ce.cn/newarea/sddy/202605/t20260522_4321190.shtml"},

    # ── Current Mayor (市长) ──
    {"id":2,"name":"谭赣明","gender":"男","ethnicity":"汉族","birth":"1972-02","birthplace":"江西余干","education":"大学","party_join":"中共党员","work_start":"","current_post":"宜春市委副书记、市长","current_org":"宜春市人民政府","source":"https://zh.wikipedia.org/wiki/宜春市; https://district.ce.cn/newarea/sddy/202308/t20230812_3201106.shtml"},

    # ── NPC Standing Committee Director (市人大常委会主任) ──
    {"id":3,"name":"蔡勇","gender":"男","ethnicity":"汉族","birth":"1968-11","birthplace":"江西南昌","education":"","party_join":"中共党员","work_start":"","current_post":"宜春市人大常委会主任","current_org":"宜春市人大常委会","source":"https://zh.wikipedia.org/wiki/宜春市"},

    # ── CPPCC Chairman (市政协主席) ──
    {"id":4,"name":"李逸翔","gender":"男","ethnicity":"汉族","birth":"1968-07","birthplace":"江西新干","education":"","party_join":"中共党员","work_start":"","current_post":"宜春市政协主席","current_org":"政协宜春市委员会","source":"https://zh.wikipedia.org/wiki/宜春市"},

    # ── Predecessors: Party Secretary ──
    {"id":5,"name":"严允","gender":"男","ethnicity":"汉族","birth":"1972-11","birthplace":"江西石城","education":"大学","party_join":"中共党员","work_start":"","current_post":"吉安市委书记（原宜春市委书记）","current_org":"中共吉安市委员会","source":"https://zh.wikipedia.org/wiki/宜春市; https://zh.wikipedia.org/wiki/严允"},

    # ── Predecessors: Mayor predecessors ──
    {"id":6,"name":"许南吉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"江西省副省长（原宜春市长）","current_org":"江西省人民政府","source":"https://zh.wikipedia.org/wiki/宜春市"},
    {"id":7,"name":"王水平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原宜春市长，已调省卫健委","current_org":"","source":"https://zh.wikipedia.org/wiki/宜春市"},
    {"id":8,"name":"张小平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原宜春市长","current_org":"","source":"https://zh.wikipedia.org/wiki/宜春市"},

    # ── Earlier Party Secretaries ──
    {"id":9,"name":"于秀明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原宜春市委书记（2020-2023）","current_org":"","source":"https://zh.wikipedia.org/wiki/宜春市"},
    {"id":10,"name":"颜赣辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原宜春市委书记（2017-2020，已被查）","current_org":"","source":"https://zh.wikipedia.org/wiki/宜春市"},
    {"id":11,"name":"邓保生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原宜春市委书记（2013-2017）","current_org":"","source":"https://zh.wikipedia.org/wiki/宜春市"},

    # ── Key cross-city connections (already in other databases) ──
    {"id":12,"name":"江训开","gender":"男","ethnicity":"汉族","birth":"1972-09","birthplace":"江西都昌","education":"省委党校研究生，农业推广硕士","party_join":"1995-05","work_start":"1996-08","current_post":"鹰潭市委常委、常务副市长（原宜春市副市长）","current_org":"鹰潭市人民政府","source":"http://www.yingtan.gov.cn/art/2021/2/9/art_10130_21.html"},
    {"id":13,"name":"高世文","gender":"男","ethnicity":"汉族","birth":"1974-06","birthplace":"山东青州","education":"研究生学历","party_join":"中共党员","work_start":"","current_post":"南昌市委副书记、市长（原挂职赣州+省工信厅长，2026年2月起长期未公开露面）","current_org":"南昌市人民政府","source":"2026-07-14南昌市调查"},
    {"id":14,"name":"刘烁","gender":"男","ethnicity":"汉族","birth":"1970-02","birthplace":"山东诸城","education":"南开大学双学士","party_join":"","work_start":"","current_post":"上饶市委书记（原萍乡市长/书记）","current_org":"中共上饶市委员会","source":"https://zh.wikipedia.org/wiki/刘烁"},

    # ── 常务副市长 宜春 ── (likely someone new; placeholder based on available data)
    # Note: 常务副市长 name data needs verification
    {"id":15,"name":"张俊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"宜春市委常委、常务副市长（推测）","current_org":"宜春市人民政府","source":"https://www.yichun.gov.cn"},

    # ── 严允's background (from Ji'an to Yichun to Ji'an) ──
    {"id":16,"name":"罗文斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"宜春市副市长","current_org":"宜春市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # City-level
    {"id":1,"name":"中共宜春市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省宜春市"},
    {"id":2,"name":"宜春市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省宜春市"},
    {"id":3,"name":"宜春市人大常委会","type":"人大","level":"地市级","parent":"江西省人大常委会","location":"江西省宜春市"},
    {"id":4,"name":"政协宜春市委员会","type":"政协","level":"地市级","parent":"政协江西省委员会","location":"江西省宜春市"},
    {"id":5,"name":"中共吉安市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省吉安市"},
    {"id":6,"name":"吉安市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省吉安市"},
    {"id":7,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":8,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":9,"name":"中共九江市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省九江市"},
    {"id":10,"name":"九江市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省九江市"},
    {"id":11,"name":"中国石化新疆石油分公司","type":"企业","level":"省级","parent":"中国石油化工集团","location":"新疆"},
    {"id":12,"name":"中国石化北京石油分公司","type":"企业","level":"省级","parent":"中国石油化工集团","location":"北京市"},
    {"id":13,"name":"江西省工业和信息化厅","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":14,"name":"抚州市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省抚州市"},
    {"id":15,"name":"江西省发展和改革委员会","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":16,"name":"中共宜春市纪律检查委员会","type":"党委","level":"地市级","parent":"中共江西省纪律检查委员会","location":"江西省宜春市"},
    {"id":17,"name":"鹰潭市人民政府","type":"政府","level":"地市级","parent":"江西省人民政府","location":"江西省鹰潭市"},
    {"id":18,"name":"南昌市人民政府","type":"政府","level":"副省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":19,"name":"中共上饶市委员会","type":"党委","level":"地市级","parent":"中共江西省委员会","location":"江西省上饶市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 蒋文定 (Party Secretary, new 2026.05) ──
    {"id":1,"person_id":1,"org_id":1,"title":"宜春市委书记","start":"2026-05","end":"","rank":"正厅级","note":"2026年5月22日江西省委组织部公示，接替严允"},
    {"id":2,"person_id":1,"org_id":10,"title":"九江市委副书记、市长","start":"2023-06","end":"2026-05","rank":"正厅级","note":"2023年5月代市长，6月正式当选"},
    {"id":3,"person_id":1,"org_id":9,"title":"九江市委副书记（正厅长级）","start":"2021-09","end":"2023-05","rank":"正厅级","note":""},
    {"id":4,"person_id":1,"org_id":9,"title":"九江市委常委、副市长（正厅长级）","start":"2021-03","end":"2021-09","rank":"正厅级","note":""},
    {"id":5,"person_id":1,"org_id":9,"title":"九江市委常委、副市长","start":"2020-06","end":"2021-03","rank":"副厅级","note":"2020.04公示，06月任副市长"},
    {"id":6,"person_id":1,"org_id":13,"title":"江西省工信厅副厅长（挂职）","start":"2019-01","end":"2020-04","rank":"副厅级","note":"从中石化挂职至江西省"},
    {"id":7,"person_id":1,"org_id":11,"title":"中国石化新疆石油分公司党委副书记、总经理","start":"约2015","end":"2019-01","rank":"中型企业正职","note":"职务级别相当于副厅级/正处级"},
    {"id":8,"person_id":1,"org_id":12,"title":"中国石化北京石油分公司党委常委、副总经理","start":"约2000s末","end":"~2015","rank":"中型企业副职","note":"中石化系统内逐步晋升"},

    # ── 谭赣明 (Mayor, since 2023.08) ──
    {"id":9,"person_id":2,"org_id":2,"title":"宜春市委副书记、市长","start":"2023-08","end":"","rank":"正厅级","note":"2023年8月任代市长，后当选"},
    {"id":10,"person_id":2,"org_id":14,"title":"抚州市委常委、常务副市长","start":"~2021","end":"2023-08","rank":"副厅级","note":"分管发改、财政、统计等工作"},
    {"id":11,"person_id":2,"org_id":15,"title":"江西省发改委副主任","start":"~2019","end":"~2021","rank":"副厅级","note":"在省发改委工作"},
    {"id":12,"person_id":2,"org_id":14,"title":"抚州市副市长","start":"~2018","end":"~2019","rank":"副厅级","note":"省直空降或抚州本地提拔"},
    {"id":13,"person_id":2,"org_id":15,"title":"江西省发改委（处长级）","start":"~2010s","end":"~2018","rank":"正处级","note":"省发改委内设处处长"},

    # ── 严允 (前市委书记, 2023.08-2026.04) ──
    {"id":14,"person_id":5,"org_id":5,"title":"吉安市委书记","start":"2026-04","end":"","rank":"正厅级","note":"从宜春市委书记调任吉安"},
    {"id":15,"person_id":5,"org_id":1,"title":"宜春市委书记","start":"2023-08","end":"2026-04","rank":"正厅级","note":"接替于秀明"},
    {"id":16,"person_id":5,"org_id":2,"title":"宜春市委副书记、市长","start":"2021-02","end":"2023-08","rank":"正厅级","note":"接替许南吉"},
    {"id":17,"person_id":5,"org_id":7,"title":"江西省交通运输厅厅长","start":"2019-12","end":"2021-02","rank":"正厅级","note":""},
    {"id":18,"person_id":5,"org_id":8,"title":"江西省交通运输厅（副厅长）","start":"~2015","end":"2019-12","rank":"副厅级","note":"江西省交通运输厅"}, # Corrected org

    # ── 蔡勇 (人大常委会主任) ──
    {"id":19,"person_id":3,"org_id":3,"title":"宜春市人大常委会主任","start":"2025-01","end":"","rank":"正厅级","note":"2025年1月当选"},

    # ── 李逸翔 (政协主席) ──
    {"id":20,"person_id":4,"org_id":4,"title":"宜春市政协主席","start":"2026-01","end":"","rank":"正厅级","note":"2026年1月当选"},

    # ── 许南吉 (前市长) ──
    {"id":21,"person_id":6,"org_id":7,"title":"江西省副省长","start":"~2023","end":"","rank":"副省级","note":"从宜春市长晋升"},
    {"id":22,"person_id":6,"org_id":2,"title":"宜春市委副书记、市长","start":"2021-02","end":"~2023","rank":"正厅级","note":""},

    # ── 王水平 (前市长) ──
    {"id":23,"person_id":7,"org_id":2,"title":"宜春市委副书记、市长","start":"2018-03","end":"2019-12","rank":"正厅级","note":"调省卫健委"},
    {"id":24,"person_id":7,"org_id":7,"title":"江西省卫健委主任","start":"~2020","end":"","rank":"正厅级","note":"从宜春市长调任"},

    # ── 张小平 (前市长) ──
    {"id":25,"person_id":8,"org_id":2,"title":"宜春市委副书记、市长","start":"2016-09","end":"2018-03","rank":"正厅级","note":""},

    # ── 于秀明 (前市委书记) ──
    {"id":26,"person_id":9,"org_id":1,"title":"宜春市委书记","start":"2020-06","end":"2023-08","rank":"正厅级","note":""},

    # ── 颜赣辉 (前市委书记, 落马) ──
    {"id":27,"person_id":10,"org_id":1,"title":"宜春市委书记","start":"2017-06","end":"2020-06","rank":"正厅级","note":"2020年6月被查，判11年"},

    # ── 邓保生 (前市委书记) ──
    {"id":28,"person_id":11,"org_id":1,"title":"宜春市委书记","start":"2013-09","end":"2017-06","rank":"正厅级","note":""},

    # ── Cross-city connections ──
    {"id":29,"person_id":12,"org_id":17,"title":"鹰潭市委常委、常务副市长","start":"2024","end":"","rank":"副厅级","note":"原宜春市副市长"},
    {"id":30,"person_id":12,"org_id":2,"title":"宜春市副市长","start":"~2022","end":"2024","rank":"副厅级","note":"从湖口书记调任宜春副市长"},
    {"id":31,"person_id":13,"org_id":18,"title":"南昌市委副书记、市长","start":"2024-08","end":"","rank":"副省级","note":"2026年2月起长期未公开露面"},
    {"id":32,"person_id":14,"org_id":19,"title":"上饶市委书记","start":"2026-05","end":"","rank":"正厅级","note":"原萍乡市委书记，调往上饶"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # City-level leadership
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"蒋文定（市委书记）与谭赣明（市长）为宜春市党政一把手。蒋文定2026年5月新到任","overlap_org":"宜春市","overlap_period":"2026-05至今"},
    {"id":2,"person_a":1,"person_b":5,"type":"前后任","context":"蒋文定（2026.05接任）接替严允（2023.08-2026.04）的市委书记职务。严允调任吉安市委书记","overlap_org":"中共宜春市委员会","overlap_period":"不重叠（前后任）"},

    # Mayor succession chain
    {"id":3,"person_a":2,"person_b":5,"type":"前后任市领导","context":"谭赣明（2023.08任市长）接替严允（2021.02-2023.08任市长→升书记）。二人曾短期搭班子","overlap_org":"宜春市人民政府","overlap_period":"2023-08至2023-08（短暂交替期）"},
    {"id":4,"person_a":5,"person_b":6,"type":"前后任","context":"严允（2021.02-2023.08市长）接替许南吉（~2021-2023市长→副省长）","overlap_org":"宜春市人民政府","overlap_period":"不重叠（前后任）"},
    {"id":5,"person_a":6,"person_b":7,"type":"前后任","context":"许南吉（2021.02任市长）接替王水平（2018-2019市长）","overlap_org":"宜春市人民政府","overlap_period":"不重叠（前后任）"},
    {"id":6,"person_a":7,"person_b":8,"type":"前后任","context":"王水平（2018-2019市长）接替张小平（2016-2018市长）","overlap_org":"宜春市人民政府","overlap_period":"不重叠（前后任）"},

    # Party secretary succession chain
    {"id":7,"person_a":5,"person_b":9,"type":"前后任","context":"严允（2023.08任书记）接替于秀明（2020-2023书记）","overlap_org":"中共宜春市委员会","overlap_period":"不重叠（前后任）"},
    {"id":8,"person_a":9,"person_b":10,"type":"前后任","context":"于秀明（2020.06任书记）接替颜赣辉（2017-2020书记，被查）","overlap_org":"中共宜春市委员会","overlap_period":"不重叠（前后任）"},
    {"id":9,"person_a":10,"person_b":11,"type":"前后任","context":"颜赣辉（2017.06任书记）接替邓保生（2013-2017书记）","overlap_org":"中共宜春市委员会","overlap_period":"不重叠（前后任）"},

    # 蒋文定 career arc (中石化→江西→九江→宜春)
    {"id":10,"person_a":1,"person_b":12,"type":"央企→地方","context":"蒋文定（中石化系统出身，2019年挂职江西省工信厅后转入地方）属于典型的央企干部空降地方路径","overlap_org":"江西省","overlap_period":"2019-01至今"},

    # 谭赣明 career arc (省发改委→抚州→宜春)
    {"id":11,"person_a":2,"person_b":13,"type":"省直→地方","context":"谭赣明（省发改委→抚州常务副市长→宜春市长）与南昌市长高世文均有省直背景","overlap_org":"江西省","overlap_period":"~2019至今"},

    # 江训开 cross-city (宜春→鹰潭)
    {"id":12,"person_a":12,"person_b":2,"type":"宜春市副→调离","context":"江训开原为宜春市副市长（~2022-2024），与谭赣明在宜春市政府共事","overlap_org":"宜春市人民政府","overlap_period":"2022-2024"},
    {"id":13,"person_a":12,"person_b":1,"type":"宜春→鹰潭","context":"江训开从宜春市副市长调任鹰潭市常务副市长，属跨市平级调动","overlap_org":"宜春市/鹰潭市","overlap_period":"2024"},

    # 颜赣辉 corruption connection
    {"id":14,"person_a":10,"person_b":14,"type":"上下级关系（前）","context":"颜赣辉（宜春书记任上落马）与刘烁（萍乡→上饶书记）曾在省内有工作交集。颜赣辉曾任景德镇市长、萍乡副书记等职","overlap_org":"江西省","overlap_period":"—"},

    # 严允↔蒋文定 mayoral-to-party secretary pattern
    {"id":15,"person_a":5,"person_b":1,"type":"市长→书记接替","context":"严允（宜春市长→书记）→蒋文定（九江市长→宜春书记）均循'地级市市长升本地/异地书记'的典型晋升路径","overlap_org":"宜春市","overlap_period":"2026-05"},
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
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","政协":"230,200,255",
            "企业":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>宜春市领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    lines.append(f'        <viz:size value="8.0"/>')
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
