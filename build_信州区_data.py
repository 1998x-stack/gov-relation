#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 信州区 (Xinzhou District) leadership network.

上饶市信州区 - district-level administrative division of Shangrao City, Jiangxi Province.

Targets: 区委书记 & 区长

Current leadership (as of 2026-07):
- 区委书记: 毛志方 (former 区长, elevated to party secretary ~early 2026)
- 区委副书记、区长提名候选人: 张天乐 (b. 1985.07)
- Predecessor party secretary: 潘表光 (now 市人大常委会副主任)

Sources:
- 信州区政府门户网站: https://www.jxxz.gov.cn
- 信州区政府领导之窗: https://www.jxxz.gov.cn/jxxz/ldzc/ldzc_v2.shtml
- 信州区新闻: various reports from www.jxxz.gov.cn
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/信州区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/信州区_network.gexf")

# ── PERSONS ──
persons = [
    # ── Current top leaders ──
    {"id":1,"name":"毛志方","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"信州区委书记","current_org":"中共上饶市信州区委员会","source":"信州区政府官网: https://www.jxxz.gov.cn 信州新闻2026-06-29"},
    {"id":2,"name":"张天乐","gender":"男","ethnicity":"汉族","birth":"1985年7月","birthplace":"","education":"研究生学历，工学硕士学位","party_join":"中共党员","work_start":"","current_post":"信州区委副书记、区长提名候选人","current_org":"上饶市信州区人民政府","source":"信州区政府领导之窗: https://www.jxxz.gov.cn/jxxz/ztlzfld/ldhd_v2.shtml"},

    # ── Previous top leaders ──
    {"id":3,"name":"潘表光","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"上饶市人大常委会副主任（原信州区委书记）","current_org":"上饶市人大常委会","source":"信州新闻2025-09-11: 潘表光以市人大常委会副主任、区委书记身份主持会议"},

    # ── District party committee standing members ──
    {"id":4,"name":"程钧","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"信州区委副书记","current_org":"中共上饶市信州区委员会","source":"信州新闻2026-06-30: 区委副书记程钧参与走访慰问"},

    # ── District government (副区长) ──
    {"id":5,"name":"刘力强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"信州区副区长、上饶市公安局信州分局局长","current_org":"上饶市信州区人民政府","source":"信州区政府领导之窗"},
    {"id":6,"name":"龚桃","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区副区长","current_org":"上饶市信州区人民政府","source":"信州区政府领导之窗"},
    {"id":7,"name":"芮可文","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区副区长","current_org":"上饶市信州区人民政府","source":"信州区政府领导之窗"},
    {"id":8,"name":"龚敏","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区副区长","current_org":"上饶市信州区人民政府","source":"信州区政府领导之窗"},

    # ── People's Congress ──
    {"id":9,"name":"吴武华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"信州区人大常委会主任","current_org":"信州区人大常委会","source":"信州新闻2026-01-08: 区人大常委会主任吴武华主持人大常委会"},
    {"id":10,"name":"刘祖宏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区人大常委会副主任","current_org":"信州区人大常委会","source":"信州新闻2026-01-08"},
    {"id":11,"name":"柴莉萍","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区人大常委会副主任","current_org":"信州区人大常委会","source":"信州新闻2026-01-08"},
    {"id":12,"name":"蒋德贤","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"信州区人大常委会副主任","current_org":"信州区人大常委会","source":"信州新闻2026-01-08"},
    {"id":13,"name":"徐叶黎","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区人大常委会副主任","current_org":"信州区人大常委会","source":"信州新闻2025-08-24"},
    {"id":14,"name":"郑平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区人大常委会副主任","current_org":"信州区人大常委会","source":"信州新闻2026-01-08"},
    {"id":15,"name":"冯文斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区人大常委会副主任","current_org":"信州区人大常委会","source":"信州新闻2026-01-08"},
    {"id":16,"name":"盛巧明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区人大常委会四级调研员","current_org":"信州区人大常委会","source":"信州新闻2026-01-08"},

    # ── Political Consultative Conference ──
    {"id":17,"name":"刘山钰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"信州区政协主席","current_org":"政协信州区委员会","source":"信州新闻2025-08-24: 区政协主席刘山钰在主席台就座"},

    # ── District party committee leaders (additional) ──
    {"id":18,"name":"李磊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区委领导","current_org":"中共上饶市信州区委员会","source":"信州新闻2025-08-24"},
    {"id":19,"name":"江华荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区领导","current_org":"中共上饶市信州区委员会","source":"信州新闻2025-08-24"},
    {"id":20,"name":"邓登勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区领导","current_org":"中共上饶市信州区委员会","source":"信州新闻2025-08-24"},
    {"id":21,"name":"张军华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区领导","current_org":"中共上饶市信州区委员会","source":"信州新闻2025-08-24"},
    {"id":22,"name":"陈河龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区领导","current_org":"上饶市信州区人民政府","source":"信州新闻2025-08-24"},
    {"id":23,"name":"吴丽辉","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"信州区领导","current_org":"上饶市信州区人民政府","source":"信州新闻2025-08-24"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id":1,"name":"中共上饶市信州区委员会","type":"党委","level":"区级","parent":"中共上饶市委员会","location":"江西省上饶市信州区"},
    {"id":2,"name":"上饶市信州区人民政府","type":"政府","level":"区级","parent":"上饶市人民政府","location":"江西省上饶市信州区"},
    {"id":3,"name":"信州区人大常委会","type":"人大","level":"区级","parent":"上饶市人大常委会","location":"江西省上饶市信州区"},
    {"id":4,"name":"政协信州区委员会","type":"政协","level":"区级","parent":"政协上饶市委员会","location":"江西省上饶市信州区"},
    {"id":5,"name":"上饶市人大常委会","type":"人大","level":"地级","parent":"江西省人大常委会","location":"江西省上饶市"},
    {"id":6,"name":"中共上饶市委员会","type":"党委","level":"地级","parent":"中共江西省委员会","location":"江西省上饶市"},
    {"id":7,"name":"上饶市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省上饶市"},
    {"id":8,"name":"上饶市公安局信州分局","type":"政府","level":"区级","parent":"上饶市公安局","location":"江西省上饶市信州区"},
]

# ── POSITIONS ──
positions = [
    # 毛志方(1) - current party secretary
    {"id":1,"person_id":1,"org_id":1,"title":"信州区委书记","start":"~2026-03","end":"","rank":"正处级","note":"此前任信州区区长，约2026年初晋升区委书记。2026年6月以区委书记身份公开活动。"},
    {"id":2,"person_id":1,"org_id":2,"title":"信州区委副书记、区长","start":"2025-08","end":"~2026-03","rank":"正处级","note":"2025年8月24日在信州区第六届人大第六次会议上当选区长"},
    {"id":3,"person_id":1,"org_id":2,"title":"信州区代区长","start":"~2025-07","end":"2025-08","rank":"正处级","note":"此前为代区长，2025年8月正式当选"},

    # 张天乐(2) - current acting mayor/区长提名候选人
    {"id":4,"person_id":2,"org_id":1,"title":"信州区委副书记","start":"~2026-04","end":"","rank":"副处级","note":"任区委副书记、区长提名候选人"},
    {"id":5,"person_id":2,"org_id":2,"title":"信州区区长提名候选人","start":"~2026-04","end":"","rank":"正处级","note":"1985年7月出生，研究生学历，工学硕士"},

    # 潘表光(3) - former party secretary
    {"id":6,"person_id":3,"org_id":5,"title":"上饶市人大常委会副主任","start":"~2021","end":"","rank":"副厅级","note":"兼任信州区委书记直至2025年底/2026年初"},
    {"id":7,"person_id":3,"org_id":1,"title":"信州区委书记","start":"~2021","end":"~2026-03","rank":"正处级","note":"以市人大常委会副主任身份兼任信州区委书记，后由毛志方接任"},

    # 程钧(4) - deputy party secretary
    {"id":8,"person_id":4,"org_id":1,"title":"信州区委副书记","start":"~2024","end":"","rank":"副处级","note":"2026年6月以区委副书记身份参加走访慰问活动"},

    # 刘力强(5) - vice mayor
    {"id":9,"person_id":5,"org_id":2,"title":"信州区副区长、上饶市公安局信州分局局长","start":"","end":"","rank":"副处级","note":""},
    {"id":10,"person_id":5,"org_id":8,"title":"上饶市公安局信州分局局长","start":"","end":"","rank":"副处级","note":""},

    # 龚桃(6) - vice mayor
    {"id":11,"person_id":6,"org_id":2,"title":"信州区副区长","start":"","end":"","rank":"副处级","note":""},

    # 芮可文(7) - vice mayor
    {"id":12,"person_id":7,"org_id":2,"title":"信州区副区长","start":"","end":"","rank":"副处级","note":""},

    # 龚敏(8) - vice mayor
    {"id":13,"person_id":8,"org_id":2,"title":"信州区副区长","start":"","end":"","rank":"副处级","note":""},

    # 吴武华(9) - people's congress chair
    {"id":14,"person_id":9,"org_id":3,"title":"信州区人大常委会主任","start":"~2024","end":"","rank":"正处级","note":"2026年1月主持区人大常委会第41次会议"},

    # 人大副主任们
    {"id":15,"person_id":10,"org_id":3,"title":"信州区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":16,"person_id":11,"org_id":3,"title":"信州区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":17,"person_id":12,"org_id":3,"title":"信州区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":18,"person_id":13,"org_id":3,"title":"信州区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":19,"person_id":14,"org_id":3,"title":"信州区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":20,"person_id":15,"org_id":3,"title":"信州区人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"id":21,"person_id":16,"org_id":3,"title":"信州区人大常委会四级调研员","start":"","end":"","rank":"正科级/副处级","note":""},

    # 刘山钰(17) - CPPCC chair
    {"id":22,"person_id":17,"org_id":4,"title":"信州区政协主席","start":"","end":"","rank":"正处级","note":""},

    # 李磊(18) - party committee member
    {"id":23,"person_id":18,"org_id":1,"title":"信州区委领导","start":"","end":"","rank":"副处级","note":"在2025年8月人大会议主席台就座"},

    # 江华荣(19)
    {"id":24,"person_id":19,"org_id":1,"title":"信州区领导","start":"","end":"","rank":"","note":"在2025年8月人大会议主席台就座"},

    # 邓登勇(20)
    {"id":25,"person_id":20,"org_id":1,"title":"信州区领导","start":"","end":"","rank":"","note":""},

    # 张军华(21)
    {"id":26,"person_id":21,"org_id":1,"title":"信州区领导","start":"","end":"","rank":"","note":""},

    # 陈河龙(22)
    {"id":27,"person_id":22,"org_id":2,"title":"信州区领导","start":"","end":"","rank":"","note":""},

    # 吴丽辉(23)
    {"id":28,"person_id":23,"org_id":2,"title":"信州区领导","start":"","end":"","rank":"","note":""},
]

# ── RELATIONSHIPS ──
relationships = [
    # 党政搭档: 毛志方(书记) - 张天乐(区长)
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"毛志方（区委书记）与张天乐（区长提名候选人）为信州区党政一把手","overlap_org":"信州区","overlap_period":"2026年至今"},

    # 职务接替: 潘表光→毛志方(书记)
    {"id":2,"person_a":3,"person_b":1,"type":"职务接替","context":"潘表光（原书记）→ 毛志方接任信州区委书记","overlap_org":"信州区委","overlap_period":"不重叠（前后任）"},

    # 毛志方从区长到书记(自我接替)
    {"id":3,"person_a":1,"person_b":2,"type":"职务接替","context":"毛志方（原区长）→ 张天乐（区长提名候选人）接任区长","overlap_org":"信州区政府","overlap_period":"不重叠（前后任）"},

    # 潘表光在信州区任职
    {"id":4,"person_a":3,"person_b":1,"type":"上下级","context":"潘表光（原书记）与毛志方（原区长）曾为党政搭档","overlap_org":"信州区","overlap_period":"2025-08至2026-03"},

    # 毛志方与程钧(副书记)
    {"id":5,"person_a":1,"person_b":4,"type":"班子同事","context":"毛志方（书记）与程钧（副书记）为区委班子同事","overlap_org":"信州区委","overlap_period":"至今"},

    # 毛志方与人大主任吴武华
    {"id":6,"person_a":1,"person_b":9,"type":"班子同事","context":"毛志方（书记）与吴武华（人大常委会主任）在区四套班子共事","overlap_org":"信州区","overlap_period":"2025-08至今"},

    # 毛志方与政协主席刘山钰
    {"id":7,"person_a":1,"person_b":17,"type":"班子同事","context":"毛志方（书记）与刘山钰（政协主席）在区四套班子共事","overlap_org":"信州区","overlap_period":"2025-08至今"},

    # 潘表光与吴武华
    {"id":8,"person_a":3,"person_b":9,"type":"班子同事","context":"潘表光（原书记）与吴武华（人大主任）在信州区共事","overlap_org":"信州区","overlap_period":"~2021-~2026"},

    # 潘表光与刘山钰
    {"id":9,"person_a":3,"person_b":17,"type":"班子同事","context":"潘表光（原书记）与刘山钰（政协主席）在信州区共事","overlap_org":"信州区","overlap_period":"~2021-~2026"},

    # 张天乐与副区长班子
    {"id":10,"person_a":2,"person_b":5,"type":"上下级","context":"张天乐（区长人选）与刘力强（副区长）为政府班子同事","overlap_org":"信州区政府","overlap_period":"至今"},
    {"id":11,"person_a":2,"person_b":6,"type":"上下级","context":"张天乐（区长人选）与龚桃（副区长）为政府班子同事","overlap_org":"信州区政府","overlap_period":"至今"},
    {"id":12,"person_a":2,"person_b":7,"type":"上下级","context":"张天乐（区长人选）与芮可文（副区长）为政府班子同事","overlap_org":"信州区政府","overlap_period":"至今"},
    {"id":13,"person_a":2,"person_b":8,"type":"上下级","context":"张天乐（区长人选）与龚敏（副区长）为政府班子同事","overlap_org":"信州区政府","overlap_period":"至今"},
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
lines.append('    <description>上饶市信州区领导班子工作关系网络 — 2026年7月15日生成</description>')
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
