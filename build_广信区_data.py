#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 广信区 (Guangxin District) leadership network.

上饶市广信区 - district-level administrative division of Shangrao City, Jiangxi Province.
Formerly 上饶县, renamed to 广信区 in 2019.

Targets: 区委书记 & 区长

Current leadership (as of 2026-07):
- 区委书记: 叶文华
- 区委副书记、区长: 顾海敏 (b. 1982.01)

Sources:
- 广信区政府门户网站: https://www.srx.gov.cn
- 广信区领导信息: https://www.srx.gov.cn/srx/ldxxx/ldxx.shtml
- 广信新闻: various reports from www.srx.gov.cn
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/广信区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/广信区_network.gexf")

# ── PERSONS ──
persons = [
    # ── Current top leaders ──
    {"id":1,"name":"叶文华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"广信区委书记","current_org":"中共上饶市广信区委员会","source":"广信区政府官网新闻: https://www.srx.gov.cn 2026-07-13/2026-07-15报道"},
    {"id":2,"name":"顾海敏","gender":"男","ethnicity":"汉族","birth":"1982年1月","birthplace":"","education":"大学本科学历","party_join":"中共党员","work_start":"2004年7月","current_post":"广信区委副书记、区政府区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn/srx/ldxxx/202012/2c51581b2f7f4bd09e7f707f9fe82821.shtml"},

    # ── District government vice leaders ──
    {"id":3,"name":"刘均勇","gender":"男","ethnicity":"汉族","birth":"1982年7月","birthplace":"","education":"大学学历","party_join":"中共党员","work_start":"2000年10月","current_post":"广信区委常委、常务副区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
    {"id":4,"name":"刘茹","gender":"女","ethnicity":"汉族","birth":"1971年2月","birthplace":"","education":"大学本科学历","party_join":"中共党员","work_start":"1990年","current_post":"广信区委常委、副区长（挂职）","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
    {"id":5,"name":"洪岳善","gender":"男","ethnicity":"汉族","birth":"1968年11月","birthplace":"","education":"江西工业大学学士学位","party_join":"无党派人士","work_start":"1992年8月","current_post":"广信区副区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
    {"id":6,"name":"李玮","gender":"男","ethnicity":"汉族","birth":"1977年11月","birthplace":"山东省泰安市","education":"大学本科学历","party_join":"中共党员","work_start":"1997年8月","current_post":"广信区副区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
    {"id":7,"name":"汪志真","gender":"女","ethnicity":"汉族","birth":"1981年8月","birthplace":"","education":"硕士研究生学历","party_join":"中共党员","work_start":"2008年7月","current_post":"广信区副区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
    {"id":8,"name":"黄华雄","gender":"男","ethnicity":"汉族","birth":"1980年11月","birthplace":"","education":"大专学历","party_join":"中共党员","work_start":"1999年10月","current_post":"广信区副区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
    {"id":9,"name":"项漪","gender":"女","ethnicity":"汉族","birth":"1985年4月","birthplace":"","education":"在职研究生学历","party_join":"中共党员","work_start":"2002年8月","current_post":"广信区副区长","current_org":"上饶市广信区人民政府","source":"广信区政府领导信息: https://www.srx.gov.cn"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共上饶市广信区委员会","type":"党委","level":"区级","parent":"中共上饶市委员会","location":"江西省上饶市广信区"},
    {"id":2,"name":"上饶市广信区人民政府","type":"政府","level":"区级","parent":"上饶市人民政府","location":"江西省上饶市广信区"},
    {"id":3,"name":"中共上饶市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":4,"name":"上饶市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省上饶市"},
    {"id":5,"name":"广信区人大常委会","type":"人大","level":"区级","parent":"上饶市人大常委会","location":"江西省上饶市广信区"},
    {"id":6,"name":"政协广信区委员会","type":"政协","level":"区级","parent":"政协上饶市委员会","location":"江西省上饶市广信区"},
]

# ── POSITIONS ──
positions = [
    # 叶文华(1) - party secretary
    {"id":1,"person_id":1,"org_id":1,"title":"广信区委书记","start":"","end":"","rank":"正处级","note":"2026年7月以区委书记身份公开活动。此前任职履历待查。"},

    # 顾海敏(2) - district mayor
    {"id":2,"person_id":2,"org_id":1,"title":"广信区委副书记","start":"","end":"","rank":"副处级","note":"区委副书记、区政府区长"},
    {"id":3,"person_id":2,"org_id":2,"title":"广信区政府区长","start":"","end":"","rank":"正处级","note":"1982年1月出生，大学本科学历，2004年7月参加工作。负责区政府全面工作。"},

    # 刘均勇(3) - executive vice mayor
    {"id":4,"person_id":3,"org_id":2,"title":"广信区委常委、常务副区长","start":"","end":"","rank":"副处级","note":"1982年7月出生，大学学历，2000年10月参加工作。负责区政府常务工作。"},

    # 刘茹(4) - vice mayor (seconded)
    {"id":5,"person_id":4,"org_id":2,"title":"广信区委常委、副区长（挂职）","start":"","end":"","rank":"副处级","note":"1971年2月出生，大学本科学历，1990年参加工作。挂职副区长。"},

    # 洪岳善(5) - vice mayor
    {"id":6,"person_id":5,"org_id":2,"title":"广信区副区长","start":"","end":"","rank":"副处级","note":"1968年11月出生，江西工业大学学士，无党派，1992年8月参加工作。"},

    # 李玮(6) - vice mayor
    {"id":7,"person_id":6,"org_id":2,"title":"广信区副区长","start":"","end":"","rank":"副处级","note":"1977年11月出生，山东泰安人，大学本科学历，1997年8月参加工作，2001年12月入党。"},

    # 汪志真(7) - vice mayor
    {"id":8,"person_id":7,"org_id":2,"title":"广信区副区长","start":"","end":"","rank":"副处级","note":"1981年8月出生，硕士研究生学历，2008年7月参加工作。"},

    # 黄华雄(8) - vice mayor
    {"id":9,"person_id":8,"org_id":2,"title":"广信区副区长","start":"","end":"","rank":"副处级","note":"1980年11月出生，大专学历，1999年10月参加工作。"},

    # 项漪(9) - vice mayor
    {"id":10,"person_id":9,"org_id":2,"title":"广信区副区长","start":"","end":"","rank":"副处级","note":"1985年4月出生，在职研究生学历，2002年8月参加工作。"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 党政搭档: 叶文华(书记) - 顾海敏(区长)
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"叶文华（区委书记）与顾海敏（区长）为广信区党政一把手","overlap_org":"广信区","overlap_period":"至今"},

    # 叶文华与刘均勇
    {"id":2,"person_a":1,"person_b":3,"type":"上下级","context":"叶文华（书记）与刘均勇（常务副区长）为区委班子同事","overlap_org":"广信区委","overlap_period":"至今"},

    # 顾海敏与刘均勇（政府班子）
    {"id":3,"person_a":2,"person_b":3,"type":"上下级","context":"顾海敏（区长）与刘均勇（常务副区长）为政府班子上下级","overlap_org":"广信区政府","overlap_period":"至今"},

    # 顾海敏与副区长们
    {"id":4,"person_a":2,"person_b":4,"type":"上下级","context":"顾海敏（区长）与刘茹（挂职副区长）为政府班子同事","overlap_org":"广信区政府","overlap_period":"至今"},
    {"id":5,"person_a":2,"person_b":5,"type":"上下级","context":"顾海敏（区长）与洪岳善（副区长）为政府班子同事","overlap_org":"广信区政府","overlap_period":"至今"},
    {"id":6,"person_a":2,"person_b":6,"type":"上下级","context":"顾海敏（区长）与李玮（副区长）为政府班子同事","overlap_org":"广信区政府","overlap_period":"至今"},
    {"id":7,"person_a":2,"person_b":7,"type":"上下级","context":"顾海敏（区长）与汪志真（副区长）为政府班子同事","overlap_org":"广信区政府","overlap_period":"至今"},
    {"id":8,"person_a":2,"person_b":8,"type":"上下级","context":"顾海敏（区长）与黄华雄（副区长）为政府班子同事","overlap_org":"广信区政府","overlap_period":"至今"},
    {"id":9,"person_a":2,"person_b":9,"type":"上下级","context":"顾海敏（区长）与项漪（副区长）为政府班子同事","overlap_org":"广信区政府","overlap_period":"至今"},
]

# ── BUILD SQLITE ──
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

# ── BUILD GEXF ──
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "区委书记" in post: return "255,50,50"
    elif "区长" in post or "副区长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    elif "人大" in post: return "100,200,200"
    elif "政协" in post: return "200,200,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220","开发区":"200,255,200","国企":"255,255,200","军队":"180,180,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>上饶市广信区领导班子工作关系网络 — 2026年7月15日生成</description>')
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
    post = p.get("current_post","")
    if "区委书记" in post and "纪委" not in post:
        sz = "20.0"
    elif "区长" in post:
        sz = "20.0"
    elif "副区长" in post:
        sz = "14.0"
    elif "常委" in post or "副书记" in post:
        sz = "12.0"
    elif "人大" in post or "政协" in post:
        sz = "12.0"
    else:
        sz = "12.0"
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
    lines.append('      </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
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
