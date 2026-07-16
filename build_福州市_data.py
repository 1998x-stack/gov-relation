#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 福州市 (Fuzhou City), 福建省 (Fujian Province) leadership network.

Covers: city-level leaders (party secretary, mayor, vice mayors, party committee),
plus predecessor chain and key connections to county/district-level orgs.

Sources:
- Fuzhou Municipal Government official website (fuzhou.gov.cn) — current leaders
- Baidu Baike — biographical data
- News reports from people.cn, thepaper.cn
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# When running from staging, write DB and GEXF relative to script location
# After promotion they'll be at canonical paths
DB_PATH = os.path.join(BASE, "福州市_network.db")
GEXF_PATH = os.path.join(BASE, "福州市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 郭宁宁 — 福建省委常委、福州市委书记 (appointed May 2024)
    {"id":1,"name":"郭宁宁","gender":"女","ethnicity":"汉族",
     "birth":"1970-07","birthplace":"辽宁沈阳",
     "education":"清华大学经济管理学院管理信息系统专业本科、清华经管学院技术经济及管理专业博士",
     "party_join":"中共党员","work_start":"1994-07",
     "current_post":"福建省委常委、福州市委书记","current_org":"中共福州市委员会",
     "source":"https://baike.baidu.com/item/%E9%83%AD%E5%AE%81%E5%AE%81/16884738"},

    # 吴贤德 — 福州市委副书记、市长
    {"id":2,"name":"吴贤德","gender":"男","ethnicity":"汉族",
     "birth":"1969-08","birthplace":"福建福清",
     "education":"中央党校研究生",
     "party_join":"中共党员","work_start":"1991-08",
     "current_post":"福州市委副书记、市长","current_org":"福州市人民政府",
     "source":"https://baike.baidu.com/item/%E5%90%B4%E8%B4%A4%E5%BE%B7/23312464"},

    # ── Other standing committee members ──
    # 陈云水 — 市委副书记 (专职)
    {"id":3,"name":"陈云水","gender":"男","ethnicity":"汉族",
     "birth":"1969-10","birthplace":"福建福清",
     "education":"中央党校大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市委副书记","current_org":"中共福州市委员会",
     "source":"https://www.fuzhou.gov.cn"},

    # 张定锋 — 常务副市长
    {"id":4,"name":"张定锋","gender":"男","ethnicity":"汉族",
     "birth":"1971-09","birthplace":"福建晋安",
     "education":"省委党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市委常委、常务副市长","current_org":"福州市人民政府",
     "source":"https://www.fuzhou.gov.cn"},

    # 傅藏荣 — 市纪委书记
    {"id":5,"name":"傅藏荣","gender":"男","ethnicity":"汉族",
     "birth":"1971-04","birthplace":"福建龙岩",
     "education":"中央党校研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市委常委、市纪委书记、市监委主任","current_org":"中共福州市纪律检查委员会",
     "source":"https://www.fuzhou.gov.cn"},

    # 蔡亚东 — 组织部部长
    {"id":6,"name":"蔡亚东","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市委常委、组织部部长","current_org":"中共福州市委组织部",
     "source":"https://www.fuzhou.gov.cn"},

    # 黄建雄 — 宣传部部长
    {"id":7,"name":"黄建雄","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市委常委、宣传部部长","current_org":"中共福州市委宣传部",
     "source":"https://www.fuzhou.gov.cn"},

    # 林治良 — 统战部部长
    {"id":8,"name":"林治良","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"福州市委常委、统战部部长","current_org":"中共福州市委统战部",
     "source":"https://www.fuzhou.gov.cn"},

    # 朱训志 — 政法委书记
    {"id":9,"name":"朱训志","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福州市委常委、政法委书记","current_org":"中共福州市委政法委员会",
     "source":"https://www.fuzhou.gov.cn"},

    # ── Vice mayors ──
    {"id":10,"name":"兰文","gender":"男","ethnicity":"畲族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"福州市副市长","current_org":"福州市人民政府",
     "source":"https://www.fuzhou.gov.cn"},
    {"id":11,"name":"黄建雄","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"福州市副市长","current_org":"福州市人民政府",
     "source":"https://www.fuzhou.gov.cn"},
    {"id":12,"name":"郑鸿","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"福州市副市长","current_org":"福州市人民政府",
     "source":"https://www.fuzhou.gov.cn"},

    # ── Predecessors — 市委书记 ──
    # 林宝金 — 前任福州市委书记 (2020-2024)，后任福建省委副书记
    {"id":13,"name":"林宝金","gender":"男","ethnicity":"汉族",
     "birth":"1964-03","birthplace":"福建平和",
     "education":"中央党校研究生",
     "party_join":"中共党员","work_start":"1985-08",
     "current_post":"福建省委副书记、政法委书记（原福州市委书记）","current_org":"中共福建省委员会",
     "source":"https://baike.baidu.com/item/%E6%9E%97%E5%AE%9D%E9%87%91/16663034"},

    # 王宁 — 前任福州市委书记 (2018-2020)，后任福建省省长、现任云南省委书记
    {"id":14,"name":"王宁","gender":"男","ethnicity":"汉族",
     "birth":"1961-04","birthplace":"湖南湘乡",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"云南省委书记（原福州市委书记、福建省省长）","current_org":"中共云南省委员会",
     "source":"https://baike.baidu.com/item/%E7%8E%8B%E5%AE%81/23745021"},

    # 尤猛军 — 前任福州市市长 (2016-2021)
    {"id":15,"name":"尤猛军","gender":"男","ethnicity":"汉族",
     "birth":"1962-08","birthplace":"福建永春",
     "education":"中央党校大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福建省人大常委会（原福州市市长）","current_org":"福建省人大常委会",
     "source":"https://baike.baidu.com/item/%E5%B0%A4%E7%8C%9B%E5%86%9B"},

    # 杨益民 — 前任福州市市长 (2011-2016)
    {"id":16,"name":"杨益民","gender":"男","ethnicity":"汉族",
     "birth":"1957-09","birthplace":"福建南安",
     "education":"省委党校大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"已退休（原福州市市长）","current_org":"",
     "source":"https://baike.baidu.com/item/%E6%9D%A8%E7%9B%8A%E6%B0%91"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市委员会","type":"党委","level":"地级市","parent":"中共福建省委员会","location":"福州市"},
    {"id":2,"name":"福州市人民政府","type":"政府","level":"地级市","parent":"福建省人民政府","location":"福州市"},
    {"id":3,"name":"中共福州市纪律检查委员会","type":"纪委","level":"地级市","parent":"中共福建省纪律检查委员会","location":"福州市"},
    {"id":4,"name":"中共福州市委组织部","type":"党委","level":"地级市","parent":"中共福州市委员会","location":"福州市"},
    {"id":5,"name":"中共福州市委宣传部","type":"党委","level":"地级市","parent":"中共福州市委员会","location":"福州市"},
    {"id":6,"name":"中共福州市委统战部","type":"党委","level":"地级市","parent":"中共福州市委员会","location":"福州市"},
    {"id":7,"name":"中共福州市委政法委员会","type":"党委","level":"地级市","parent":"中共福州市委员会","location":"福州市"},
    {"id":8,"name":"福建省人民代表大会常务委员会","type":"人大","level":"省级","parent":"福建省","location":"福州市"},
    {"id":9,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"中共中央","location":"福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 郭宁宁 — 福州市委书记
    {"id":1,"person_id":1,"org_id":1,"title":"福建省委常委、福州市委书记","start":"2024-05","end":"至今","rank":"副省级","note":"2024年5月任命"},
    # 吴贤德 — 市长
    {"id":2,"person_id":2,"org_id":2,"title":"福州市委副书记、市长","start":"2021-08","end":"至今","rank":"正厅级","note":"2021年8月任代市长，后转正"},
    # 陈云水 — 专职副书记
    {"id":3,"person_id":3,"org_id":1,"title":"福州市委副书记","start":"","end":"至今","rank":"正厅级","note":""},
    # 张定锋 — 常务副市长
    {"id":4,"person_id":4,"org_id":2,"title":"福州市委常委、常务副市长","start":"","end":"至今","rank":"副厅级","note":""},
    # 傅藏荣 — 纪委书记
    {"id":5,"person_id":5,"org_id":3,"title":"福州市委常委、市纪委书记、市监委主任","start":"","end":"至今","rank":"副厅级","note":""},
    # 蔡亚东 — 组织部部长
    {"id":6,"person_id":6,"org_id":4,"title":"福州市委常委、组织部部长","start":"","end":"至今","rank":"副厅级","note":""},
    # 黄建雄 — 宣传部部长
    {"id":7,"person_id":7,"org_id":5,"title":"福州市委常委、宣传部部长","start":"","end":"至今","rank":"副厅级","note":""},
    # 林治良 — 统战部部长
    {"id":8,"person_id":8,"org_id":6,"title":"福州市委常委、统战部部长","start":"","end":"至今","rank":"副厅级","note":""},
    # 朱训志 — 政法委书记
    {"id":9,"person_id":9,"org_id":7,"title":"福州市委常委、政法委书记","start":"","end":"至今","rank":"副厅级","note":""},
    # 兰文 — 副市长
    {"id":10,"person_id":10,"org_id":2,"title":"福州市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"id":11,"person_id":11,"org_id":2,"title":"福州市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    {"id":12,"person_id":12,"org_id":2,"title":"福州市副市长","start":"","end":"至今","rank":"副厅级","note":""},
    # 林宝金 — 前任书记
    {"id":13,"person_id":13,"org_id":1,"title":"福州市委书记","start":"2020-09","end":"2024-05","rank":"副省级","note":"后任福建省委副书记"},
    {"id":14,"person_id":13,"org_id":9,"title":"福建省委副书记、政法委书记","start":"2024-05","end":"至今","rank":"副省级","note":""},
    # 王宁 — 前任书记
    {"id":15,"person_id":14,"org_id":1,"title":"福州市委书记","start":"2018-05","end":"2020-07","rank":"副省级","note":"后任福建省省长"},
    # 尤猛军 — 前任市长
    {"id":16,"person_id":15,"org_id":2,"title":"福州市市长","start":"2016-08","end":"2021-08","rank":"正厅级","note":""},
    # 杨益民 — 前任市长
    {"id":17,"person_id":16,"org_id":2,"title":"福州市市长","start":"2011-01","end":"2016-08","rank":"正厅级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 郭宁宁 vs 吴贤德 (current party-gov duo)
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"郭宁宁（市委书记）与吴贤德（市长）在福州市共事",
     "overlap_org":"福州市","overlap_period":"2024-05至今"},

    # ── Party Secretary succession
    {"id":2,"person_a":13,"person_b":1,"type":"前后任",
     "context":"林宝金（2020-2024书记）→ 郭宁宁（2024接任）",
     "overlap_org":"中共福州市委员会","overlap_period":"不重叠（前后任）"},

    {"id":3,"person_a":14,"person_b":13,"type":"前后任",
     "context":"王宁（2018-2020书记）→ 林宝金（2020-2024书记）",
     "overlap_org":"中共福州市委员会","overlap_period":"不重叠（前后任）"},

    # ── Mayor succession
    {"id":4,"person_a":15,"person_b":2,"type":"前后任",
     "context":"尤猛军（2016-2021市长）→ 吴贤德（2021接任市长）",
     "overlap_org":"福州市人民政府","overlap_period":"不重叠（前后任）"},

    {"id":5,"person_a":16,"person_b":15,"type":"前后任",
     "context":"杨益民（2011-2016市长）→ 尤猛军（2016-2021市长）",
     "overlap_org":"福州市人民政府","overlap_period":"不重叠（前后任）"},

    # ── 王宁 vs 尤猛军 — 曾在福州搭档
    {"id":6,"person_a":14,"person_b":15,"type":"党政搭档",
     "context":"王宁（书记）与尤猛军（市长）曾在福州共事（2018-2020）",
     "overlap_org":"福州市","overlap_period":"2018-2020"},

    # ── 郭宁宁与省里领导关系
    {"id":7,"person_a":1,"person_b":13,"type":"前后任-省领导",
     "context":"郭宁宁接替林宝金任福州市委书记；林宝金后任省委副书记",
     "overlap_org":"福建省","overlap_period":"前后任关系"},
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
    if "书记" in post and ("市委" in post or "省委" in post):
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
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>福州市（地级市）领导班子工作关系网络 — 2026年7月生成</description>')
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
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","福州市委书记","市长","福州市市长"]) else "12.0"
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
print("\n⚠️ NOTE: This data requires verification. Key items:")
print("  1. Verify current party secretary and mayor against latest news")
print("  2. Verify all standing committee members' full names and roles")
print("  3. Complete career timelines for all officials")
