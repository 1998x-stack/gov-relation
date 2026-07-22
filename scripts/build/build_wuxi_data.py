#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 无锡市 (Wuxi City) leadership network.

Covers: City-level leadership (市委书记, 市长, 副市长, etc.),
7 districts/counties (区委书记 + 区长/市长), predecessors,
and the city-level leadership structure.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/wuxi_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/wuxi_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 杜小刚 — 无锡市委书记
    {"id":1,"name":"杜小刚","gender":"男","ethnicity":"汉族","birth":"1976-06","birthplace":"江苏常州","education":"南京大学国际金融本科","party_join":"","work_start":"","current_post":"无锡市委书记","current_org":"中共无锡市委员会","source":"https://zh.wikipedia.org/wiki/%E6%9D%9C%E5%B0%8F%E5%88%9A"},
    # 蒋锋 — 无锡市代市长
    {"id":2,"name":"蒋锋","gender":"男","ethnicity":"汉族","birth":"1972-07","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市代市长","current_org":"无锡市人民政府","source":""},
    # 赵建军 — 前无锡市长
    {"id":3,"name":"赵建军","gender":"男","ethnicity":"汉族","birth":"1972-02","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"前无锡市长","current_org":"无锡市人民政府","source":"https://zh.wikipedia.org/wiki/%E8%B5%B5%E5%BB%BA%E5%86%9B"},
    # 马良 — 无锡市副市长
    {"id":4,"name":"马良","gender":"男","ethnicity":"汉族","birth":"1976-01","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长","current_org":"无锡市人民政府","source":""},
    # 张镇 — 无锡市副市长
    {"id":5,"name":"张镇","gender":"男","ethnicity":"汉族","birth":"1973-12","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长","current_org":"无锡市人民政府","source":""},
    # 周文栋 — 无锡市副市长
    {"id":6,"name":"周文栋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长","current_org":"无锡市人民政府","source":""},
    # 张立军 — 无锡市副市长
    {"id":7,"name":"张立军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长","current_org":"无锡市人民政府","source":""},
    # 卢敏 — 无锡市副市长（女，九三学社）
    {"id":8,"name":"卢敏","gender":"女","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长","current_org":"无锡市人民政府","source":""},
    # 谭永生 — 无锡市副市长/公安局长
    {"id":9,"name":"谭永生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长、公安局长","current_org":"无锡市人民政府","source":""},
    # 孙玮 — 无锡市副市长
    {"id":10,"name":"孙玮","gender":"男","ethnicity":"汉族","birth":"1982-01","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"无锡市副市长","current_org":"无锡市人民政府","source":""},
    # 黄钦 — 前无锡市委书记（退休）
    {"id":11,"name":"黄钦","gender":"男","ethnicity":"汉族","birth":"1962-01","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"前无锡市委书记（退休）","current_org":"中共无锡市委员会","source":"https://zh.wikipedia.org/wiki/%E9%BB%84%E9%92%A6"},

    # ── District/County leadership ──
    # 锡山区 — 待查
    {"id":12,"name":"锡山区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"锡山区区委书记","current_org":"中共锡山区委员会","source":""},
    {"id":13,"name":"锡山区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"锡山区区长","current_org":"锡山区人民政府","source":""},

    # 惠山区
    {"id":14,"name":"吴建元","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"惠山区委书记","current_org":"中共惠山区委员会","source":""},
    {"id":15,"name":"惠山区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"惠山区区长","current_org":"惠山区人民政府","source":""},

    # 滨湖区
    {"id":16,"name":"滨湖区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"滨湖区区委书记","current_org":"中共滨湖区委员会","source":""},
    {"id":17,"name":"高佩","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"滨湖区区长","current_org":"滨湖区人民政府","source":""},

    # 梁溪区
    {"id":18,"name":"许立新","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"梁溪区委书记","current_org":"中共梁溪区委员会","source":""},
    {"id":19,"name":"梁溪区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"梁溪区区长","current_org":"梁溪区人民政府","source":""},

    # 新吴区
    {"id":20,"name":"魏多","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"新吴区委书记","current_org":"中共新吴区委员会","source":""},
    {"id":21,"name":"新吴区区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"新吴区区长","current_org":"新吴区人民政府","source":""},

    # 江阴市（县级市）
    {"id":22,"name":"方力","gender":"男","ethnicity":"汉族","birth":"1977-07","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"江阴市委书记","current_org":"中共江阴市委员会","source":""},
    {"id":23,"name":"江阴市市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"江阴市市长","current_org":"江阴市人民政府","source":""},

    # 宜兴市（县级市）
    {"id":24,"name":"封晓春","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"宜兴市委书记","current_org":"中共宜兴市委员会","source":""},
    {"id":25,"name":"宜兴市市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"宜兴市市长","current_org":"宜兴市人民政府","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Wuxi city-level core ──
    {"id":1,"name":"中共无锡市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省无锡市"},
    {"id":2,"name":"无锡市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省无锡市"},
    {"id":3,"name":"无锡市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省无锡市"},
    {"id":4,"name":"政协无锡市委员会","type":"政协","level":"地级","parent":"","location":"江苏省无锡市"},
    {"id":5,"name":"中共无锡市纪律检查委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市"},
    {"id":6,"name":"无锡市公安局","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市"},

    # ── 5 Districts — Party committees ──
    {"id":7,"name":"中共锡山区委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市锡山区"},
    {"id":8,"name":"中共惠山区委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市惠山区"},
    {"id":9,"name":"中共滨湖区委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市滨湖区"},
    {"id":10,"name":"中共梁溪区委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市梁溪区"},
    {"id":11,"name":"中共新吴区委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市新吴区"},

    # ── 2 County-level cities — Party committees ──
    {"id":12,"name":"中共江阴市委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市江阴市"},
    {"id":13,"name":"中共宜兴市委员会","type":"党委","level":"地级","parent":"中共无锡市委员会","location":"江苏省无锡市宜兴市"},

    # ── 5 Districts — Governments ──
    {"id":14,"name":"锡山区人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市锡山区"},
    {"id":15,"name":"惠山区人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市惠山区"},
    {"id":16,"name":"滨湖区人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市滨湖区"},
    {"id":17,"name":"梁溪区人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市梁溪区"},
    {"id":18,"name":"新吴区人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市新吴区"},

    # ── 2 County-level cities — Governments ──
    {"id":19,"name":"江阴市人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市江阴市"},
    {"id":20,"name":"宜兴市人民政府","type":"政府","level":"地级","parent":"无锡市人民政府","location":"江苏省无锡市宜兴市"},

    # ── External / other orgs needed ──
    {"id":21,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":22,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 杜小刚 ──
    {"id":1,"person_id":1,"org_id":1,"title":"无锡市委书记","start":"2021-07","end":"","rank":"副部级","note":"苏州系统成长，曾任昆山市委书记、无锡市长"},
    {"id":2,"person_id":1,"org_id":2,"title":"无锡市市长","start":"2020-01","end":"2021-07","rank":"副部级","note":"升任市委书记"},
    {"id":3,"person_id":1,"org_id":1,"title":"无锡市委副书记","start":"2019-12","end":"2021-07","rank":"副部级","note":""},

    # ── 蒋锋 ──
    {"id":4,"person_id":2,"org_id":2,"title":"无锡市代市长","start":"2025-07","end":"","rank":"副部级","note":"2025.07到任"},
    {"id":5,"person_id":2,"org_id":1,"title":"无锡市委副书记","start":"2025-07","end":"","rank":"副部级","note":""},

    # ── 赵建军 ──
    {"id":6,"person_id":3,"org_id":2,"title":"无锡市市长","start":"2021-07","end":"2025-07","rank":"副部级","note":"2021.07-2025.07任市长，去向待查"},
    {"id":7,"person_id":3,"org_id":1,"title":"无锡市委副书记","start":"2021-07","end":"2025-07","rank":"副部级","note":""},

    # ── 马良 ──
    {"id":8,"person_id":4,"org_id":2,"title":"无锡市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 张镇 ──
    {"id":9,"person_id":5,"org_id":2,"title":"无锡市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 周文栋 ──
    {"id":10,"person_id":6,"org_id":2,"title":"无锡市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 张立军 ──
    {"id":11,"person_id":7,"org_id":2,"title":"无锡市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 卢敏 ──
    {"id":12,"person_id":8,"org_id":2,"title":"无锡市副市长","start":"","end":"","rank":"副部级","note":"九三学社，党外人士"},

    # ── 谭永生 ──
    {"id":13,"person_id":9,"org_id":2,"title":"无锡市副市长、公安局长","start":"","end":"","rank":"副部级","note":""},

    # ── 孙玮 ──
    {"id":14,"person_id":10,"org_id":2,"title":"无锡市副市长","start":"","end":"","rank":"副部级","note":""},

    # ── 黄钦 ──
    {"id":15,"person_id":11,"org_id":1,"title":"无锡市委书记","start":"2019-12","end":"2021-07","rank":"副部级","note":"2019.12-2021.07任无锡市委书记，已退休"},
    {"id":16,"person_id":11,"org_id":1,"title":"无锡市委副书记、市长","start":"","end":"2019-12","rank":"副部级","note":"前任无锡市长，后任书记"},

    # ── 锡山区委书记（placeholder）──
    {"id":17,"person_id":12,"org_id":7,"title":"锡山区区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 锡山区区长（placeholder）──
    {"id":18,"person_id":13,"org_id":14,"title":"锡山区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 吴建元（惠山区委书记）──
    {"id":19,"person_id":14,"org_id":8,"title":"惠山区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 惠山区区长（placeholder）──
    {"id":20,"person_id":15,"org_id":15,"title":"惠山区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 滨湖区委书记（placeholder）──
    {"id":21,"person_id":16,"org_id":9,"title":"滨湖区区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 高佩（滨湖区区长）──
    {"id":22,"person_id":17,"org_id":16,"title":"滨湖区区长","start":"","end":"","rank":"正厅级","note":""},

    # ── 许立新（梁溪区委书记）──
    {"id":23,"person_id":18,"org_id":10,"title":"梁溪区委书记","start":"","end":"","rank":"正厅级","note":"可能已过时"},

    # ── 梁溪区区长（placeholder）──
    {"id":24,"person_id":19,"org_id":17,"title":"梁溪区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 魏多（新吴区委书记）──
    {"id":25,"person_id":20,"org_id":11,"title":"新吴区委书记","start":"","end":"","rank":"正厅级","note":"可能已过时"},

    # ── 新吴区区长（placeholder）──
    {"id":26,"person_id":21,"org_id":18,"title":"新吴区区长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 方力（江阴市委书记）──
    {"id":27,"person_id":22,"org_id":12,"title":"江阴市委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 江阴市市长（placeholder）──
    {"id":28,"person_id":23,"org_id":19,"title":"江阴市市长","start":"","end":"","rank":"正厅级","note":"信息待查"},

    # ── 封晓春（宜兴市委书记）──
    {"id":29,"person_id":24,"org_id":13,"title":"宜兴市委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 宜兴市市长（placeholder）──
    {"id":30,"person_id":25,"org_id":20,"title":"宜兴市市长","start":"","end":"","rank":"正厅级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 杜小刚 ↔ 蒋锋（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"杜小刚（无锡市委书记）与蒋锋（代市长）为无锡市党政一把手搭档","overlap_org":"无锡市","overlap_period":"2025-07至今"},

    # ── 赵建军→蒋锋（前后任市长）──
    {"id":2,"person_a":3,"person_b":2,"type":"前后任","context":"赵建军（2021-2025无锡市长）→ 蒋锋（2025.07接任代市长）","overlap_org":"无锡市人民政府","overlap_period":"不重叠（前后任）"},

    # ── 黄钦→杜小刚（前后任书记）──
    {"id":3,"person_a":11,"person_b":1,"type":"前后任","context":"黄钦（2019-2021无锡市委书记）→ 杜小刚（2021.07接任书记）","overlap_org":"中共无锡市委员会","overlap_period":"不重叠（前后任）"},

    # ── 杜小刚苏州系统——─
    {"id":4,"person_a":1,"person_b":21,"type":"隶属关系","context":"杜小刚苏州系统成长（昆山书记→无锡市长→无锡书记）","overlap_org":"江苏省","overlap_period":""},

    # ── 各区委书记↔区长（党政搭档）──
    {"id":5,"person_a":12,"person_b":13,"type":"党政搭档","context":"锡山区区委书记与锡山区区长党政搭档","overlap_org":"锡山区","overlap_period":""},
    {"id":6,"person_a":14,"person_b":15,"type":"党政搭档","context":"吴建元（惠山区委书记）与惠山区区长党政搭档","overlap_org":"惠山区","overlap_period":""},
    {"id":7,"person_a":16,"person_b":17,"type":"党政搭档","context":"滨湖区区委书记与高佩（滨湖区区长）党政搭档","overlap_org":"滨湖区","overlap_period":""},
    {"id":8,"person_a":18,"person_b":19,"type":"党政搭档","context":"许立新（梁溪区委书记）与梁溪区区长党政搭档","overlap_org":"梁溪区","overlap_period":""},
    {"id":9,"person_a":20,"person_b":21,"type":"党政搭档","context":"魏多（新吴区委书记）与新吴区区长党政搭档","overlap_org":"新吴区","overlap_period":""},
    {"id":10,"person_a":22,"person_b":23,"type":"党政搭档","context":"方力（江阴市委书记）与江阴市市长党政搭档","overlap_org":"江阴市","overlap_period":""},
    {"id":11,"person_a":24,"person_b":25,"type":"党政搭档","context":"封晓春（宜兴市委书记）与宜兴市市长党政搭档","overlap_org":"宜兴市","overlap_period":""},

    # ── 市区联系：各区委向市委汇报 ──
    {"id":12,"person_a":1,"person_b":12,"type":"隶属关系","context":"杜小刚（市委书记）领导锡山区区委书记","overlap_org":"无锡市","overlap_period":""},
    {"id":13,"person_a":1,"person_b":14,"type":"隶属关系","context":"杜小刚（市委书记）领导吴建元（惠山区委书记）","overlap_org":"无锡市","overlap_period":""},
    {"id":14,"person_a":1,"person_b":16,"type":"隶属关系","context":"杜小刚（市委书记）领导滨湖区区委书记","overlap_org":"无锡市","overlap_period":""},
    {"id":15,"person_a":1,"person_b":18,"type":"隶属关系","context":"杜小刚（市委书记）领导许立新（梁溪区委书记）","overlap_org":"无锡市","overlap_period":""},
    {"id":16,"person_a":1,"person_b":20,"type":"隶属关系","context":"杜小刚（市委书记）领导魏多（新吴区委书记）","overlap_org":"无锡市","overlap_period":""},
    {"id":17,"person_a":1,"person_b":22,"type":"隶属关系","context":"杜小刚（市委书记）领导方力（江阴市委书记）","overlap_org":"无锡市","overlap_period":""},
    {"id":18,"person_a":1,"person_b":24,"type":"隶属关系","context":"杜小刚（市委书记）领导封晓春（宜兴市委书记）","overlap_org":"无锡市","overlap_period":""},
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
    if "市委书记" in post and "市委" in post:
        return "200,30,30"  # deep red for party secretary
    if "市长" in post or "区长" in post:
        return "30,80,200"  # deep blue for mayor/district head
    if "副书记" in post:
        return "220,60,60"
    if "副市长" in post or "副区长" in post:
        return "60,120,220"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>无锡市（地级市）领导班子 + 5区2县市工作关系网络 — 2026年7月14日生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"]) else "12.0"
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
