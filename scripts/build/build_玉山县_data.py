#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 玉山县 (Yushan County) leadership network.

上饶市玉山县 - county-level administrative division of Shangrao City, Jiangxi Province.

Targets: 县委书记 & 县长

Current leadership (as of 2026-07):
- 县委书记: 余洪雷 (前县长, 约2026年上半年晋升县委书记)
- 县委副书记、代县长: 占长远
- Predecessor party secretary: 郑国良 (前任县委书记)

Sources:
- 玉山县政府门户网站: https://www.zgys.gov.cn
- 玉山县新闻: various reports from www.zgys.gov.cn (2026-06/07)
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/jiangxi_玉山县/玉山县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/jiangxi_玉山县/玉山县_network.gexf")

# ── PERSONS ──
persons = [
    # ── Current top leaders ──
    {"id":1,"name":"余洪雷","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县委书记","current_org":"中共玉山县委员会","source":"玉山县政府官网: https://www.zgys.gov.cn 2026-07-06头条: 县委书记余洪雷调研生态环保督察问题整改工作; 2026-07-13: 县委书记余洪雷主持召开县委常委会会议"},
    {"id":2,"name":"占长远","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县委副书记、代县长","current_org":"玉山县人民政府","source":"玉山县政府官网: https://www.zgys.gov.cn 2026-07-14: 县委副书记、代县长占长远调研; 2026-07-06: 县委副书记、县长提名人选占长远调研督导安全生产工作"},

    # ── Previous top leaders ──
    {"id":3,"name":"郑国良","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"前任玉山县委书记","current_org":"（已离任）","source":"玉山县政府官网历史页(已注释的领导之窗片段): 原县委书记郑国良; 玉山县新闻2025年报道"},

    # ── County party committee standing members / leaders ──
    {"id":4,"name":"韩庆云","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县委常委/县政府领导","current_org":"中共玉山县委员会","source":"玉山县政府官网2026-07-09: 全县防台风工作会议, 韩庆云出席; 2026-07-06: 余洪雷调研生态环保督察, 韩庆云参加"},

    # ── County government (deputy mayors) ──
    {"id":5,"name":"祝晓光","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县副县长、玉山高新区党工委书记","current_org":"玉山县人民政府","source":"玉山县政府官网2026-07-14: 占长远到衢饶示范区调研, 副县长祝晓光参加; 2026-07-06: 余洪雷调研生态环保督察, 祝晓光参加"},
    {"id":6,"name":"吴承材","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县副县长","current_org":"玉山县人民政府","source":"玉山县政府官网2026-06-30: 副市长郭峰到玉山走访慰问, 副县长吴承材陪同; 2026-07-09: 全县防台风工作会议, 吴承材出席"},
    {"id":7,"name":"李媛媛","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县领导/县委常委","current_org":"中共玉山县委员会","source":"玉山县政府官网2026-07-09: 全县防台风工作会议, 李媛媛出席"},
    {"id":8,"name":"杨建伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"玉山县领导/县委常委","current_org":"中共玉山县委员会","source":"玉山县政府官网2026-07-09: 全县防台风工作会议, 杨建伟出席"},

    # ── People's Congress and CPPCC (inferred from county standard pattern) ──
    # Note: specific names for 人大主任 and 政协主席 not found in recent news
    {"id":9,"name":"玉山县人大常委会主任","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"玉山县人大常委会主任","current_org":"玉山县人民代表大会常务委员会","source":"待补(参照县级标准配置)"},
    {"id":10,"name":"玉山县政协主席","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"玉山县政协主席","current_org":"政协玉山县委员会","source":"待补(参照县级标准配置)"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共玉山县委员会","type":"党委","level":"县级","parent":"中共上饶市委员会","location":"江西省上饶市玉山县"},
    {"id":2,"name":"玉山县人民政府","type":"政府","level":"县级","parent":"上饶市人民政府","location":"江西省上饶市玉山县"},
    {"id":3,"name":"玉山县人民代表大会常务委员会","type":"人大","level":"县级","parent":"上饶市人大常委会","location":"江西省上饶市玉山县"},
    {"id":4,"name":"政协玉山县委员会","type":"政协","level":"县级","parent":"政协上饶市委员会","location":"江西省上饶市玉山县"},
    {"id":5,"name":"玉山高新技术产业园区","type":"开发区","level":"省级","parent":"玉山县人民政府","location":"江西省上饶市玉山县"},
    {"id":6,"name":"中共上饶市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":7,"name":"上饶市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省上饶市"},
    {"id":8,"name":"上饶市人大常委会","type":"人大","level":"地级","parent":"江西省人大常委会","location":"江西省上饶市"},
    {"id":9,"name":"政协上饶市委员会","type":"政协","level":"地级","parent":"政协江西省委员会","location":"江西省上饶市"},
]

# ── POSITIONS ──
positions = [
    # 余洪雷(1) - current party secretary
    {"id":1,"person_id":1,"org_id":1,"title":"玉山县委书记","start":"~2026-03","end":"","rank":"正处级","note":"此前为玉山县县长，约2026年初晋升县委书记。2026年6月-7月以县委书记身份多次公开活动。"},
    {"id":2,"person_id":1,"org_id":2,"title":"玉山县县长","start":"~2021","end":"~2026-03","rank":"正处级","note":"此前为玉山县县长，约2026年初晋升为县委书记。前任县委书记为郑国良。"},

    # 占长远(2) - current acting mayor
    {"id":3,"person_id":2,"org_id":1,"title":"玉山县委副书记","start":"~2026-04","end":"","rank":"副处级","note":"任县委副书记、代县长/县长提名人选"},
    {"id":4,"person_id":2,"org_id":2,"title":"玉山县代县长","start":"~2026-04","end":"","rank":"正处级","note":"2026年7月以县委副书记、代县长身份公开活动。此前为县长提名人选。"},

    # 郑国良(3) - former party secretary
    {"id":5,"person_id":3,"org_id":1,"title":"玉山县委书记","start":"~2020","end":"~2026-03","rank":"正处级","note":"前任县委书记，被余洪雷接任。具体去向待查。"},

    # 韩庆云(4)
    {"id":6,"person_id":4,"org_id":1,"title":"玉山县委常委/县政府领导","start":"","end":"","rank":"副处级","note":"2026年7月参加全县防台风工作会议、生态环保督察调研"},

    # 祝晓光(5) - vice mayor + 高新区书记
    {"id":7,"person_id":5,"org_id":2,"title":"玉山县副县长","start":"","end":"","rank":"副处级","note":"2026年7月参加衢饶示范区调研"},
    {"id":8,"person_id":5,"org_id":5,"title":"玉山高新区党工委书记","start":"","end":"","rank":"副处级","note":"兼任玉山高新区党工委书记"},

    # 吴承材(6) - vice mayor
    {"id":9,"person_id":6,"org_id":2,"title":"玉山县副县长","start":"","end":"","rank":"副处级","note":"2026年6月陪同副市长郭峰走访慰问"},

    # 李媛媛(7)
    {"id":10,"person_id":7,"org_id":1,"title":"玉山县领导","start":"","end":"","rank":"","note":"2026年7月参加全县防台风工作会议"},

    # 杨建伟(8)
    {"id":11,"person_id":8,"org_id":1,"title":"玉山县领导","start":"","end":"","rank":"","note":"2026年7月参加全县防台风工作会议"},

    # 人大主任(9)
    {"id":12,"person_id":9,"org_id":3,"title":"玉山县人大常委会主任","start":"","end":"","rank":"正处级","note":"姓名待核实"},

    # 政协主席(10)
    {"id":13,"person_id":10,"org_id":4,"title":"玉山县政协主席","start":"","end":"","rank":"正处级","note":"姓名待核实"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 党政搭档: 余洪雷(书记) - 占长远(县长)
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"余洪雷（县委书记）与占长远（代县长）为玉山县当前党政一把手","overlap_org":"玉山县","overlap_period":"2026年至今"},

    # 职务接替: 郑国良→余洪雷(书记)
    {"id":2,"person_a":3,"person_b":1,"type":"职务接替","context":"郑国良（原书记）→ 余洪雷（接任玉山县委书记）。余洪雷此前为县长，晋升接替","overlap_org":"玉山县委","overlap_period":"不重叠（前后任）"},

    # 余洪雷从县长到书记(自我接替)
    {"id":3,"person_a":1,"person_b":2,"type":"职务接替","context":"余洪雷（原县长，现书记）→ 占长远（代县长）接替县长职务","overlap_org":"玉山县政府","overlap_period":"不重叠（前后任）"},

    # 余洪雷与党政班子成员
    {"id":4,"person_a":1,"person_b":4,"type":"班子同事","context":"余洪雷（书记）与韩庆云为县委班子同事","overlap_org":"玉山县委","overlap_period":"至今"},
    {"id":5,"person_a":1,"person_b":5,"type":"上下级","context":"余洪雷（书记）与祝晓光（副县长）为县领导","overlap_org":"玉山县","overlap_period":"至今"},
    {"id":6,"person_a":1,"person_b":6,"type":"上下级","context":"余洪雷（书记）与吴承材（副县长）为县领导","overlap_org":"玉山县","overlap_period":"至今"},
    {"id":7,"person_a":1,"person_b":7,"type":"班子同事","context":"余洪雷（书记）与李媛媛为县委班子同事","overlap_org":"玉山县委","overlap_period":"至今"},
    {"id":8,"person_a":1,"person_b":8,"type":"班子同事","context":"余洪雷（书记）与杨建伟为县委班子同事","overlap_org":"玉山县委","overlap_period":"至今"},

    # 占长远与副职们
    {"id":9,"person_a":2,"person_b":5,"type":"上下级","context":"占长远（代县长）与祝晓光（副县长）为政府班子同事","overlap_org":"玉山县政府","overlap_period":"至今"},
    {"id":10,"person_a":2,"person_b":6,"type":"上下级","context":"占长远（代县长）与吴承材（副县长）为政府班子同事","overlap_org":"玉山县政府","overlap_period":"至今"},

    # 郑国良与余洪雷曾有党政搭档关系(郑任书记时, 余为县长)
    {"id":11,"person_a":3,"person_b":1,"type":"上下级","context":"郑国良（原书记）与余洪雷（原县长）曾为党政搭档","overlap_org":"玉山县","overlap_period":"~2021-~2026-03"},
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
    if "县委书记" in post: return "255,50,50"
    elif "县长" in post or "副县长" in post: return "50,100,255"
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
lines.append('    <description>上饶市玉山县领导班子工作关系网络 — 2026年7月15日生成</description>')
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
    if "县委书记" in post and "纪委" not in post:
        sz = "20.0"
    elif "县长" in post and "代县长" in post:
        sz = "20.0"
    elif "副县长" in post:
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
