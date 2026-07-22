#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 田家庵区 (Tianjia'an District) leadership network.

淮南市田家庵区 - district-level administrative division of Huainan City, Anhui Province.

Targets: 区委书记 & 区长

Current leadership (as of 2026-07):
- 区委书记: 朱光 (b. 1975-02)
- 区委副书记、区长: 魏颖颖
- Predecessor party secretary: unknown (朱光 succession details)

Sources:
- 淮南市田家庵区人民政府 领导之窗: https://www.tja.gov.cn/zwgk/ldzc/
- 田家庵区人民政府: https://www.tja.gov.cn
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/田家庵区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/田家庵区_network.gexf")

# ── PERSONS ──
persons = [
    # ── Current top leaders ──
    {"id":1,"name":"朱光","gender":"男","ethnicity":"汉族","birth":"1975年2月","birthplace":"","education":"大学学历，工学学士","party_join":"中共党员","work_start":"","current_post":"田家庵区委书记","current_org":"中共淮南市田家庵区委员会","source":"田家庵区政府官网领导之窗: https://www.tja.gov.cn/zwgk/ldzc/"},
    {"id":2,"name":"魏颖颖","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委副书记、区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗: https://www.tja.gov.cn/zwgk/ldzc/"},

    # ── District party committee standing members ──
    {"id":3,"name":"房鲲鹏","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委副书记、区委党校校长","current_org":"中共淮南市田家庵区委员会","source":"田家庵区政府官网领导之窗"},
    {"id":4,"name":"王庆祝","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、政法委书记、区委社会工作部部长","current_org":"中共淮南市田家庵区委员会","source":"田家庵区政府官网领导之窗"},
    {"id":5,"name":"郑克玉","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、纪委书记、监委副主任、代理主任","current_org":"中共淮南市田家庵区纪律检查委员会","source":"田家庵区政府官网领导之窗"},
    {"id":6,"name":"姚文海","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、常务副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":7,"name":"刘庆武","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":8,"name":"黄峰峻","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、组织部部长","current_org":"中共淮南市田家庵区委员会","source":"田家庵区政府官网领导之窗"},
    {"id":9,"name":"潘冬波","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、区人武部上校部长","current_org":"淮南市田家庵区人民武装部","source":"田家庵区政府官网领导之窗"},
    {"id":10,"name":"戴宜娜","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、统战部部长","current_org":"中共淮南市田家庵区委员会","source":"田家庵区政府官网领导之窗"},
    {"id":11,"name":"李云","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"田家庵区委常委、宣传部部长","current_org":"中共淮南市田家庵区委员会","source":"田家庵区政府官网领导之窗"},

    # ── District government (副区长) ──
    {"id":12,"name":"夏多明","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"田家庵区副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":13,"name":"吴杰敏","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"田家庵区副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":14,"name":"徐永锋","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"田家庵区副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":15,"name":"曹震","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"田家庵区副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":16,"name":"缪国鹏","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"田家庵区副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
    {"id":17,"name":"毛汉霖","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"田家庵区副区长","current_org":"淮南市田家庵区人民政府","source":"田家庵区政府官网领导之窗"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共淮南市田家庵区委员会","type":"党委","level":"区级","parent":"中共淮南市委员会","location":"安徽省淮南市田家庵区"},
    {"id":2,"name":"淮南市田家庵区人民政府","type":"政府","level":"区级","parent":"淮南市人民政府","location":"安徽省淮南市田家庵区"},
    {"id":3,"name":"中共淮南市田家庵区纪律检查委员会","type":"党委","level":"区级","parent":"中共淮南市纪律检查委员会","location":"安徽省淮南市田家庵区"},
    {"id":4,"name":"淮南市田家庵区人民武装部","type":"军队","level":"区级","parent":"淮南军分区","location":"安徽省淮南市田家庵区"},
    {"id":5,"name":"田家庵区人大常委会","type":"人大","level":"区级","parent":"淮南市人大常委会","location":"安徽省淮南市田家庵区"},
    {"id":6,"name":"政协田家庵区委员会","type":"政协","level":"区级","parent":"政协淮南市委员会","location":"安徽省淮南市田家庵区"},
    {"id":7,"name":"中共淮南市委员会","type":"党委","level":"地级","parent":"中共安徽省委员会","location":"安徽省淮南市"},
    {"id":8,"name":"淮南市人民政府","type":"政府","level":"地级","parent":"安徽省人民政府","location":"安徽省淮南市"},
    {"id":9,"name":"淮南市城市管理行政执法支队直属大队","type":"政府","level":"科级","parent":"淮南市城市管理行政执法局","location":"安徽省淮南市"},
    {"id":10,"name":"淮南市城市管理行政执法支队田家庵区一大队","type":"政府","level":"科级","parent":"淮南市城市管理行政执法局","location":"安徽省淮南市田家庵区"},
    {"id":11,"name":"田家庵区城管行政执法局","type":"政府","level":"科级","parent":"田家庵区人民政府","location":"安徽省淮南市田家庵区"},
    {"id":12,"name":"大通区人民政府","type":"政府","level":"区级","parent":"淮南市人民政府","location":"安徽省淮南市大通区"},
    {"id":13,"name":"中共大通区委员会","type":"党委","level":"区级","parent":"中共淮南市委员会","location":"安徽省淮南市大通区"},
    {"id":14,"name":"毛集实验区管理委员会","type":"政府","level":"县级","parent":"淮南市人民政府","location":"安徽省淮南市毛集实验区"},
    {"id":15,"name":"中共毛集实验区工作委员会","type":"党委","level":"县级","parent":"中共淮南市委员会","location":"安徽省淮南市毛集实验区"},
    {"id":16,"name":"淮南市城乡建设局","type":"政府","level":"处级","parent":"淮南市人民政府","location":"安徽省淮南市"},
    {"id":17,"name":"淮南市住房和城乡建设局","type":"政府","level":"处级","parent":"淮南市人民政府","location":"安徽省淮南市"},
]

# ── POSITIONS ──
positions = [
    # 朱光(1) - current party secretary
    {"id":1,"person_id":1,"org_id":1,"title":"田家庵区委书记","start":"","end":"","rank":"正处级","note":"一级调研员。主持区委全面工作。"},
    {"id":2,"person_id":1,"org_id":17,"title":"淮南市住房和城乡建设局党组书记、局长","start":"","end":"","rank":"正处级","note":"任区委书记前职务"},
    {"id":3,"person_id":1,"org_id":16,"title":"淮南市城乡建设局党组书记、局长","start":"","end":"","rank":"正处级","note":"机构改革前职务"},
    {"id":4,"person_id":1,"org_id":14,"title":"毛集实验区党工委副书记、管委会主任","start":"","end":"","rank":"正处级","note":""},
    {"id":5,"person_id":1,"org_id":13,"title":"大通区委常委","start":"","end":"","rank":"副处级","note":""},
    {"id":6,"person_id":1,"org_id":12,"title":"大通区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":7,"person_id":1,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":8,"person_id":1,"org_id":11,"title":"田家庵区城管行政执法局党委副书记","start":"","end":"","rank":"科级","note":"同时兼任市城管行政执法支队田家庵区一大队大队长、教导员"},
    {"id":9,"person_id":1,"org_id":10,"title":"淮南市城市管理行政执法支队田家庵区一大队教导员","start":"","end":"","rank":"科级","note":""},
    {"id":10,"person_id":1,"org_id":10,"title":"淮南市城市管理行政执法支队田家庵区一大队大队长","start":"","end":"","rank":"科级","note":""},
    {"id":11,"person_id":1,"org_id":9,"title":"淮南市城市管理行政执法支队直属大队副大队长","start":"","end":"","rank":"科级","note":"早期职务"},

    # 魏颖颖(2) - current district mayor
    {"id":12,"person_id":2,"org_id":2,"title":"田家庵区区长","start":"","end":"","rank":"正处级","note":"区委副书记、区长，区政府党组书记"},
    {"id":13,"person_id":2,"org_id":1,"title":"田家庵区委副书记","start":"","end":"","rank":"副处级","note":""},

    # 房鲲鹏(3) - deputy party secretary
    {"id":14,"person_id":3,"org_id":1,"title":"田家庵区委副书记、区委党校校长","start":"","end":"","rank":"副处级","note":""},

    # 王庆祝(4) -政法委书记
    {"id":15,"person_id":4,"org_id":1,"title":"田家庵区委常委、政法委书记、区委社会工作部部长","start":"","end":"","rank":"副处级","note":""},

    # 郑克玉(5) - 纪委书记
    {"id":16,"person_id":5,"org_id":3,"title":"田家庵区纪委书记、监委副主任、代理主任","start":"","end":"","rank":"副处级","note":"代理主任身份，可能尚未经人大正式任命"},

    # 姚文海(6) - 常务副区长
    {"id":17,"person_id":6,"org_id":2,"title":"田家庵区常务副区长","start":"","end":"","rank":"副处级","note":"区委常委、常务副区长"},
    {"id":18,"person_id":6,"org_id":1,"title":"田家庵区委常委","start":"","end":"","rank":"副处级","note":""},

    # 刘庆武(7) - 副区长(常委)
    {"id":19,"person_id":7,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":"区委常委、副区长"},
    {"id":20,"person_id":7,"org_id":1,"title":"田家庵区委常委","start":"","end":"","rank":"副处级","note":""},

    # 黄峰峻(8) - 组织部长
    {"id":21,"person_id":8,"org_id":1,"title":"田家庵区委组织部部长","start":"","end":"","rank":"副处级","note":"区委常委、组织部部长"},

    # 潘冬波(9) - 人武部长
    {"id":22,"person_id":9,"org_id":4,"title":"田家庵区人武部上校部长","start":"","end":"","rank":"正团级","note":"区委常委、区人武部上校部长"},

    # 戴宜娜(10) - 统战部长
    {"id":23,"person_id":10,"org_id":1,"title":"田家庵区委统战部部长","start":"","end":"","rank":"副处级","note":"区委常委、统战部部长"},

    # 李云(11) - 宣传部长
    {"id":24,"person_id":11,"org_id":1,"title":"田家庵区委宣传部部长","start":"","end":"","rank":"副处级","note":"区委常委、宣传部部长"},

    # 副区长们
    {"id":25,"person_id":12,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":26,"person_id":13,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":27,"person_id":14,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":28,"person_id":15,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":29,"person_id":16,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
    {"id":30,"person_id":17,"org_id":2,"title":"田家庵区副区长","start":"","end":"","rank":"副处级","note":""},
]

# ── RELATIONSHIPS ──
relationships = [
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate","context":"区委书记与区长搭档","overlap_org":"田家庵区","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":2,"person_a":1,"person_b":6,"type":"superior_subordinate","context":"区委书记与常务副区长","overlap_org":"田家庵区","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":3,"person_a":2,"person_b":6,"type":"superior_subordinate","context":"区长与常务副区长","overlap_org":"田家庵区政府","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":4,"person_a":1,"person_b":3,"type":"superior_subordinate","context":"区委书记与专职副书记","overlap_org":"田家庵区委","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":5,"person_a":1,"person_b":4,"type":"superior_subordinate","context":"区委书记与政法委书记","overlap_org":"田家庵区委","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":6,"person_a":1,"person_b":5,"type":"superior_subordinate","context":"区委书记与纪委书记","overlap_org":"田家庵区委","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":7,"person_a":1,"person_b":8,"type":"superior_subordinate","context":"区委书记与组织部长","overlap_org":"田家庵区委","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
    {"id":8,"person_a":2,"person_b":7,"type":"superior_subordinate","context":"区长与副区长(常委)","overlap_org":"田家庵区政府","overlap_period":"2026至今","confidence":"confirmed","strength":"strong"},
]


# ══════════════════════════════════════
# DATABASE
# ══════════════════════════════════════
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""CREATE TABLE persons(
id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,
birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,
current_post TEXT,current_org TEXT,source TEXT)""")

c.execute("""CREATE TABLE organizations(
id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT)""")

c.execute("""CREATE TABLE positions(
id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,
start TEXT,"end" TEXT,rank TEXT,note TEXT)""")

c.execute("""CREATE TABLE relationships(
id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,
context TEXT,overlap_org TEXT,overlap_period TEXT)""")

for p in persons:
    c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
               p["education"],p["party_join"],p["work_start"],p["current_post"],
               p["current_org"],p["source"]))

for o in organizations:
    c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

for pos in positions:
    c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],
               pos["start"],pos["end"],pos["rank"],pos["note"]))

for r in relationships:
    c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],
               r["context"],r["overlap_org"],r["overlap_period"]))

conn.commit()
conn.close()

print(f"DB: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Orgs: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# ══════════════════════════════════════
# GEXF
# ══════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "区委书记" in post and "纪委" not in post: return "255,50,50"
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
lines.append('    <description>淮南市田家庵区领导班子工作关系网络 — 2026年7月15日生成</description>')
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
    elif "区长" in post and "副" not in post:
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
