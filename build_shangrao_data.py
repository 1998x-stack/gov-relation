#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Shangrao City (上饶市) leadership network.

Covers: prefecture-level city leadership (party secretary, mayor, vice mayors,
party committee members), plus the predecessor chain (陈云→刘烁; 邱向军→李建涛),
and key organizational connections.

Research sources:
- https://zh.wikipedia.org/wiki/刘烁
- https://zh.wikipedia.org/wiki/邱向军
- https://zh.wikipedia.org/wiki/上饶市 (current leaders table)
- Baidu Baike: 陈云 (1976.12), 李建涛 (1977.05)
- district.ce.cn news reports
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/shangrao_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/shangrao_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    {"id":1,"name":"刘烁","gender":"男","ethnicity":"汉族","birth":"1970-02","birthplace":"山东诸城","education":"南开大学化学系化学专业+企业管理专业双学士","party_join":"1991-02","work_start":"1992-07","current_post":"上饶市委书记","current_org":"中共上饶市委员会","source":"https://zh.wikipedia.org/wiki/刘烁"},
    {"id":2,"name":"李建涛","gender":"男","ethnicity":"汉族","birth":"1977-05","birthplace":"河南方城","education":"研究生学历，理学博士","party_join":"中共党员","work_start":"","current_post":"上饶市委副书记、市长","current_org":"上饶市人民政府","source":"https://www.sr.gov.cn — 李建涛领导之窗 + 澎湃新闻2025-07-29"},
    {"id":3,"name":"李高兴","gender":"男","ethnicity":"汉族","birth":"1968-10","birthplace":"江西余干","education":"","party_join":"中共党员","work_start":"","current_post":"上饶市人大常委会主任","current_org":"上饶市人大常委会","source":"https://zh.wikipedia.org/wiki/上饶市"},

    # ── Vice mayors & key gov officials ──
    {"id":4,"name":"俞健","gender":"男","ethnicity":"汉族","birth":"1968-02","birthplace":"江西上饶广丰区","education":"","party_join":"中共党员","work_start":"","current_post":"上饶市政协主席","current_org":"政协上饶市委员会","source":"https://zh.wikipedia.org/wiki/上饶市"},
    {"id":5,"name":"饶清华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"江西上饶","education":"","party_join":"中共党员","work_start":"","current_post":"上饶市委常委、常务副市长（推定）","current_org":"上饶市人民政府","source":"上饶市政府官网 — 领导分工"},  # 2025 news confirms he was常务副市长

    # ── Previous leaders ──
    {"id":6,"name":"陈云","gender":"男","ethnicity":"汉族","birth":"1976-12","birthplace":"江西南昌","education":"江西师范大学","party_join":"中共党员","work_start":"1999-07","current_post":"九江市委书记（2026年5月调任）","current_org":"中共九江市委员会","source":"https://baike.baidu.com/item/陈云/24711030 + 政事儿2021-12-12"},
    {"id":7,"name":"邱向军","gender":"男","ethnicity":"汉族","birth":"1968-02","birthplace":"江西资溪","education":"江西师范大学政教系本科/江西财经大学MBA/江西师范大学法学博士","party_join":"1988-01","work_start":"1990-07","current_post":"江西省民政厅厅长","current_org":"江西省民政厅","source":"https://zh.wikipedia.org/wiki/邱向军"},
    {"id":8,"name":"史文斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"江西省委常委、省委秘书长（2021年升任）","current_org":"中共江西省委员会","source":"鲁网2021-12-12"},
    {"id":9,"name":"谢来发","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（原上饶市长，2020年离职）","current_org":"","source":"人民网2020-01-03"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共上饶市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":2,"name":"上饶市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省上饶市"},
    {"id":3,"name":"上饶市人大常委会","type":"人大","level":"地级","parent":"江西省人大常委会","location":"江西省上饶市"},
    {"id":4,"name":"政协上饶市委员会","type":"政协","level":"地级","parent":"政协江西省委员会","location":"江西省上饶市"},
    {"id":5,"name":"中共萍乡市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省萍乡市"},
    {"id":6,"name":"萍乡市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省萍乡市"},
    {"id":7,"name":"中华人民共和国公安部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":8,"name":"中共江西省委政法委员会","type":"党委","level":"省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":9,"name":"中共南昌市委员会","type":"党委","level":"副省级","parent":"中共江西省委员会","location":"江西省南昌市"},
    {"id":10,"name":"中共江西省委员会","type":"党委","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":11,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":12,"name":"中共九江市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省九江市"},
    {"id":13,"name":"江西省民政厅","type":"政府","level":"省级","parent":"江西省人民政府","location":"江西省南昌市"},
    {"id":14,"name":"河南省工业和信息化厅","type":"政府","level":"省级","parent":"河南省人民政府","location":"河南省郑州市"},
    {"id":15,"name":"中共漯河市委","type":"党委","level":"地级","parent":"中共河南省委员会","location":"河南省漯河市"},
    {"id":16,"name":"漯河市人民政府","type":"政府","level":"地级","parent":"河南省人民政府","location":"河南省漯河市"},
    {"id":17,"name":"卫辉市人民政府","type":"政府","level":"县级","parent":"新乡市人民政府","location":"河南省新乡市卫辉市"},
    {"id":18,"name":"共青团河南省委员会","type":"政府","level":"省级","parent":"","location":"河南省郑州市"},
    {"id":19,"name":"上饶经济技术开发区","type":"开发区","level":"国家级","parent":"上饶市人民政府","location":"江西省上饶市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘烁 (Liu Shuo) — current Shangrao party secretary ──
    {"id":1,"person_id":1,"org_id":1,"title":"上饶市委书记","start":"2026-05","end":"","rank":"正厅级","note":"2026年5月6日从萍乡调任"},
    {"id":2,"person_id":1,"org_id":5,"title":"萍乡市委书记","start":"2023-03","end":"2026-05","rank":"正厅级","note":"2023年3月30日升任"},
    {"id":3,"person_id":1,"org_id":6,"title":"萍乡市委副书记、市长","start":"2021-09","end":"2023-03","rank":"副厅级→正厅级","note":"2021年8月任代市长，9月任市长"},
    {"id":4,"person_id":1,"org_id":10,"title":"江西省委副秘书长、省委办公厅主任","start":"2019-12","end":"2021-09","rank":"正厅级","note":"2019年12月任命"},
    {"id":5,"person_id":1,"org_id":9,"title":"南昌市委副书记、市委组织部部长","start":"2019-09","end":"2019-12","rank":"副厅级","note":"在南昌市委任职不到一年"},
    {"id":6,"person_id":1,"org_id":8,"title":"江西省委政法委副书记、省综治办主任","start":"2017","end":"2019-09","rank":"副厅级","note":""},
    {"id":7,"person_id":1,"org_id":8,"title":"江西省委维稳办主任","start":"2016","end":"2017","rank":"副厅级","note":"从公安部空降江西"},
    {"id":8,"person_id":1,"org_id":7,"title":"公安部物证鉴定中心主任","start":"~2015","end":"2016","rank":"正处级/副厅级","note":"此前任公安部科技局副局长"},
    {"id":9,"person_id":1,"org_id":7,"title":"公安部科技局副局长","start":"~2006","end":"~2015","rank":"副处级/正处级","note":""},
    {"id":10,"person_id":1,"org_id":7,"title":"公安部第二研究所政治处副主任/主任","start":"1992-07","end":"~2006","rank":"","note":"在南开大学后进入公安部第二研究所，先后任团委书记、助理研究员、政治处副主任、物证鉴定中心政治处主任等职"},

    # ── 李建涛 (Li Jiantao) — current Shangrao mayor ──
    {"id":11,"person_id":2,"org_id":2,"title":"上饶市委副书记、市长","start":"2025-09","end":"","rank":"正厅级","note":"2025年7月任代市长，9月26日当选市长；跨省交流干部(河南→江西)"},
    {"id":12,"person_id":2,"org_id":14,"title":"河南省工信厅党组书记、厅长","start":"2023-01","end":"2025-07","rank":"正厅级","note":""},
    {"id":13,"person_id":2,"org_id":15,"title":"漯河市委常委、常务副市长","start":"~2021","end":"2023-01","rank":"副厅级","note":"市政府党组副书记"},
    {"id":14,"person_id":2,"org_id":15,"title":"漯河市委常委、市委秘书长","start":"~2019","end":"~2021","rank":"副厅级","note":""},
    {"id":15,"person_id":2,"org_id":18,"title":"共青团河南省委副书记","start":"~2015","end":"~2019","rank":"副厅级","note":""},
    {"id":16,"person_id":2,"org_id":17,"title":"卫辉市委副书记、市长","start":"~2013","end":"~2015","rank":"正处级","note":"2011年任卫辉市委常委、副市长，后任市长"},

    # ── 陈云 (Chen Yun) — previous Shangrao party secretary ──
    {"id":17,"person_id":6,"org_id":1,"title":"上饶市委书记","start":"2021-12","end":"2026-05","rank":"正厅级","note":"2021年12月任书记；2026年5月调离"},
    {"id":18,"person_id":6,"org_id":2,"title":"上饶市委副书记、市长","start":"2020-01","end":"2021-12","rank":"副厅级","note":"2020年1月提名为市长候选人"},
    {"id":19,"person_id":6,"org_id":12,"title":"九江市委书记","start":"2026-05","end":"","rank":"正厅级","note":"2026年5月从上海调任九江"},

    # ── 邱向军 (Qiu Xiangjun) — previous Shangrao mayor ──
    {"id":20,"person_id":7,"org_id":13,"title":"江西省民政厅党组书记、厅长","start":"2025-08","end":"","rank":"正厅级","note":"2025年7月任民政厅党组书记，8月任厅长"},
    {"id":21,"person_id":7,"org_id":2,"title":"上饶市委副书记、市长","start":"2021-12","end":"2025-07","rank":"正厅级","note":"2021年5月任市委副书记，12月任代市长，2022年1月正任"},
    {"id":22,"person_id":7,"org_id":11,"title":"江西省人民政府副秘书长","start":"2020-01","end":"2021-05","rank":"正厅级","note":""},
    {"id":23,"person_id":7,"org_id":9,"title":"南昌市委常委","start":"2016-09","end":"2020-01","rank":"副厅级","note":""},
    {"id":24,"person_id":7,"org_id":19,"title":"南昌高新区党工委书记","start":"2011-09","end":"2016-09","rank":"副厅级","note":"此前2008年12月任管委会主任"},
    {"id":25,"person_id":7,"org_id":19,"title":"南昌高新区管委会主任","start":"2008-12","end":"2011-09","rank":"副厅级","note":""},
    {"id":26,"person_id":7,"org_id":9,"title":"安义县委书记","start":"2005-05","end":"2008-12","rank":"正处级","note":"兼县人大常委会主任"},
    {"id":27,"person_id":7,"org_id":9,"title":"安义县委副书记、县长","start":"2001-09","end":"2005-05","rank":"正处级","note":"2001年9月任代县长，2002年1月任县长"},

    # ── 史文斌 (Shi Wenbin) ──
    {"id":28,"person_id":8,"org_id":1,"title":"上饶市委书记","start":"2021-02","end":"2021-11","rank":"正厅级","note":"2021年11月升任省委常委、秘书长"},

    # ── 李高兴 (Li Gaoxing) ──
    {"id":29,"person_id":3,"org_id":3,"title":"上饶市人大常委会主任","start":"2022-12","end":"","rank":"正厅级","note":""},

    # ── 俞健 (Yu Jian) ──
    {"id":30,"person_id":4,"org_id":4,"title":"上饶市政协主席","start":"2021-10","end":"","rank":"正厅级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Top leadership relationship
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"刘烁（市委书记）与李建涛（市长）为上饶市党政一把手。刘烁2026年5月从萍乡调任，李建涛2025年9月从河南跨省调任，两人均为新任","overlap_org":"上饶市","overlap_period":"2026-05至今（名义上）"},

    # Party secretary succession
    {"id":2,"person_a":6,"person_b":1,"type":"前后任","context":"陈云（2021-2026书记）→ 刘烁（2026年5月接任）。陈云调任九江市委书记","overlap_org":"中共上饶市委员会","overlap_period":"不重叠（前后任）"},
    {"id":3,"person_a":8,"person_b":6,"type":"前后任","context":"史文斌（2021书记）→ 陈云（2021-2026书记）。史文斌仅任职约9个月即升任省委常委","overlap_org":"中共上饶市委员会","overlap_period":"不重叠（前后任）"},

    # Mayor succession
    {"id":4,"person_a":7,"person_b":2,"type":"前后任","context":"邱向军（2021-2025市长）→ 李建涛（2025年9月接任）。邱向军调任省民政厅厅长","overlap_org":"上饶市人民政府","overlap_period":"不重叠（前后任）"},
    {"id":5,"person_a":9,"person_b":7,"type":"前后任","context":"谢来发（前市长）→ 邱向军（2021-2025市长）。谢来发2020年1月离职","overlap_org":"上饶市人民政府","overlap_period":"不重叠（前后任）"},

    # 陈云 & 邱向军 — former party-government duo
    {"id":6,"person_a":6,"person_b":7,"type":"党政搭档（前）","context":"陈云（书记）与邱向军（市长）在上饶市搭班子约3年半（2021.12-2025.07）","overlap_org":"上饶市","overlap_period":"2021-12至2025-07"},

    # Notable: 刘烁's path crosses with 陈云 via Pingxiang
    {"id":7,"person_a":1,"person_b":6,"type":"间接关联","context":"陈云和刘烁均与萍乡有交集——陈云在上饶任书记前曾在萍乡市委副书记；刘烁在任上饶书记前是萍乡书记。两人在萍乡市形成'前后任'关系","overlap_org":"萍乡市","overlap_period":"2023-03至2026-05"},
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
    if "书记" in post and ("市委" in post or "市人大" not in post) and "副" not in post.replace("常务副",""):
        return "230,50,50"  # red for top party secretary
    if "市长" in post and ("副" not in post or "常务副市长" in post):
        return "50,100,230"  # blue for gov leaders
    if "副市长" in post:
        return "80,140,230"
    if "人大" in post:
        return "180,200,255"
    if "政协" in post:
        return "200,180,255"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255","政协":"230,200,255","新区":"200,255,200","开发区":"200,255,200"}.get(otype,"200,200,200")

def node_sz(p):
    if p["current_org"] == "":
        return "8.0"
    cp = p.get("current_post","")
    if "市委书记" in cp and "副" not in cp:
        return "20.0"
    if "市长" in cp and "副" not in cp:
        return "20.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>上饶市（市级）领导班子工作关系网络 — 2026年7月14日生成</description>')
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
    sz = node_sz(p)
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
