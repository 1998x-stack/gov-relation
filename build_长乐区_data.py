#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 长乐区 (Changle District), 福州市, 福建省.

Covers: district-level leaders (party secretary, district mayor, standing committee,
vice mayors), plus predecessor chain and key connections.

Sources:
- Changle District Government official website (fzcl.gov.cn) — leadership bios and news
- Fuzhou New Area government website (fzxq.fuzhou.gov.cn)
- News reports from mainstream media

Current as of: July 2026

Key findings:
- 区委书记: 兰文 (succeeded 张帆, ~2025)
- 代区长: 胡旭彬 (succeeded 廖海军, 2026年5月, 正厅长级兼任)

Note: 长乐区 is co-located with 福州新区 (Fuzhou New Area), a national-level new area.
The区委书记 and 区长 both hold concurrent high-level 福州新区 posts.
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "长乐区_network.db")
GEXF_PATH = os.path.join(BASE, "长乐区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current top leadership
    # ═════════════════════════════════════════════════════════════════════

    # 兰文 — 长乐区委书记 (confirmed from district news, May-July 2026)
    {"id":1,"name":"兰文","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区委书记、福州新区党工委分管日常工作的副书记","current_org":"中共福州市长乐区委员会",
     "source":"https://www.fzcl.gov.cn"},

    # 胡旭彬 — 长乐区委副书记、代区长 (confirmed from official leadership page, 2026年7月)
    {"id":2,"name":"胡旭彬","gender":"男","ethnicity":"汉族",
     "birth":"1971-02","birthplace":"",
     "education":"在职研究生学历，经济学博士",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区委副书记、区政府代区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/hxb/"},

    # ═════════════════════════════════════════════════════════════════════
    # Current government leadership team (区政府领导)
    # ═════════════════════════════════════════════════════════════════════

    # 游昕 — 区委常委、副区长
    {"id":3,"name":"游昕","gender":"男","ethnicity":"汉族",
     "birth":"1973-09","birthplace":"",
     "education":"在职研究生学历，工商管理硕士",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区委常委、副区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/yx/"},

    # 林宇 — 副区长
    {"id":4,"name":"林宇","gender":"男","ethnicity":"汉族",
     "birth":"1972-07","birthplace":"",
     "education":"大学学士学历",
     "party_join":"农工党党员","work_start":"",
     "current_post":"长乐区副区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/ly/"},

    # 周勇 — 副区长
    {"id":5,"name":"周勇","gender":"男","ethnicity":"汉族",
     "birth":"1972-11","birthplace":"",
     "education":"省委党校研究生学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区副区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/zy/"},

    # 陈爱玉 — 副区长
    {"id":6,"name":"陈爱玉","gender":"女","ethnicity":"汉族",
     "birth":"1977-06","birthplace":"",
     "education":"省委党校研究生学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区副区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/cay/"},

    # 邹亮 — 副区长
    {"id":7,"name":"邹亮","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"长乐区副区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/zl/"},

    # 曹可 — 副区长
    {"id":8,"name":"曹可","gender":"男","ethnicity":"汉族",
     "birth":"1973-02","birthplace":"",
     "education":"省委党校研究生学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区副区长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/ck/"},

    # 李继志 — 副区长、公安分局局长
    {"id":9,"name":"李继志","gender":"男","ethnicity":"汉族",
     "birth":"1978-03","birthplace":"",
     "education":"大学学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"长乐区副区长、公安分局局长","current_org":"福州市长乐区人民政府",
     "source":"https://www.fzcl.gov.cn/xjwz/zwgk/ldzc/ljz/"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors — 区委书记
    # ═════════════════════════════════════════════════════════════════════

    # 张帆 — 前任长乐区委书记 (~2021-2025, 升正厅长级)
    {"id":10,"name":"张帆","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福建正厅级（原长乐区委书记）","current_org":"",
     "source":"https://www.fzcl.gov.cn"},

    # 何杰民 — 前前任长乐区委书记 (~2016-2021, 后任福州市副市长、宜春市长)
    {"id":11,"name":"何杰民","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"江西省宜春市委副书记、市长（原长乐区委书记）","current_org":"江西省宜春市人民政府",
     "source":"https://www.fzcl.gov.cn"},

    # 许南吉 — 前长乐市委书记 (~2015-2016, 后升江西省副省长)
    {"id":12,"name":"许南吉","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"江西省副省长（原长乐市委书记）","current_org":"江西省人民政府",
     "source":"https://www.fzcl.gov.cn"},

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors — 区长
    # ═════════════════════════════════════════════════════════════════════

    # 廖海军 — 前任长乐区长 (2021.6-2026, 调任华安县委书记)
    {"id":13,"name":"廖海军","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"华安县委书记（原长乐区长）","current_org":"中共华安县委员会",
     "source":"https://www.fzcl.gov.cn"},

    # 蔡劲松 — 前长乐市长/区长 (~2016-2021)
    {"id":14,"name":"蔡劲松","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原长乐市长/区长）","current_org":"",
     "source":"https://www.fzcl.gov.cn"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福州市长乐区委员会","type":"党委","level":"县处级","parent":"中共福州市委员会","location":"福州市长乐区"},
    {"id":2,"name":"福州市长乐区人民政府","type":"政府","level":"县处级","parent":"福州市人民政府","location":"福州市长乐区"},
    {"id":3,"name":"福州新区党工委","type":"党委","level":"副省级","parent":"中共福建省委员会","location":"福州市长乐区"},
    {"id":4,"name":"福州新区管委会","type":"政府","level":"副省级","parent":"福建省人民政府","location":"福州市长乐区"},
    {"id":5,"name":"福州市公安局长乐分局","type":"政府","level":"县处级","parent":"福州市长乐区人民政府","location":"福州市长乐区"},
    {"id":6,"name":"江西省宜春市人民政府","type":"政府","level":"地级","parent":"江西省人民政府","location":"江西省宜春市"},
    {"id":7,"name":"江西省人民政府","type":"政府","level":"省级","parent":"","location":"江西省南昌市"},
    {"id":8,"name":"福州市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福州市"},
    {"id":9,"name":"中共福州市委员会","type":"党委","level":"副省级","parent":"中共福建省委员会","location":"福州市"},
    {"id":10,"name":"中共华安县委员会","type":"党委","level":"县处级","parent":"中共漳州市委员会","location":"漳州市华安县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 兰文 — 区委书记
    {"id":1,"person_id":1,"org_id":1,"title":"长乐区委书记","start":"2025?","end":"至今","rank":"正厅长级","note":"兼任福州新区党工委分管日常工作的副书记"},
    {"id":2,"person_id":1,"org_id":3,"title":"福州新区党工委分管日常工作的副书记","start":"2025?","end":"至今","rank":"正厅长级","note":"兼任"},

    # 胡旭彬 — 代区长
    {"id":3,"person_id":2,"org_id":2,"title":"长乐区委副书记、区政府代区长","start":"2026-05","end":"至今","rank":"正厅长级","note":"福州新区管委会分管日常工作的副主任兼任"},
    {"id":4,"person_id":2,"org_id":4,"title":"福州新区党工委委员、管委会分管日常工作的副主任","start":"","end":"至今","rank":"正厅长级","note":"兼任"},
    {"id":5,"person_id":2,"org_id":8,"title":"福州市人民政府党组成员","start":"","end":"至今","rank":"正厅长级","note":"兼任"},

    # 游昕
    {"id":6,"person_id":3,"org_id":2,"title":"长乐区委常委、副区长","start":"","end":"至今","rank":"副处级","note":"福州新区党工委委员、管委会副主任"},
    {"id":7,"person_id":3,"org_id":4,"title":"福州新区党工委委员、管委会副主任","start":"","end":"至今","rank":"副厅级","note":"兼任"},

    # 林宇
    {"id":8,"person_id":4,"org_id":2,"title":"长乐区副区长","start":"","end":"至今","rank":"副处级","note":"农工党党员"},

    # 周勇
    {"id":9,"person_id":5,"org_id":2,"title":"长乐区副区长","start":"","end":"至今","rank":"副处级","note":"区政府党组成员"},

    # 陈爱玉
    {"id":10,"person_id":6,"org_id":2,"title":"长乐区副区长","start":"","end":"至今","rank":"副处级","note":"区政府党组成员"},

    # 邹亮
    {"id":11,"person_id":7,"org_id":2,"title":"长乐区副区长","start":"","end":"至今","rank":"副处级","note":""},

    # 曹可
    {"id":12,"person_id":8,"org_id":2,"title":"长乐区副区长","start":"","end":"至今","rank":"副处级","note":"区政府党组成员"},

    # 李继志
    {"id":13,"person_id":9,"org_id":2,"title":"长乐区副区长","start":"","end":"至今","rank":"副处级","note":"区政府党组成员"},
    {"id":14,"person_id":9,"org_id":5,"title":"长乐公安分局党委书记、局长、督察长","start":"","end":"至今","rank":"二级高级警长","note":"兼任"},

    # 张帆 — 前任区委书记
    {"id":15,"person_id":10,"org_id":1,"title":"长乐区委书记","start":"2021?","end":"2025?","rank":"正厅级（离任）","note":"后升任正厅长级"},

    # 何杰民 — 前前任区委书记
    {"id":16,"person_id":11,"org_id":1,"title":"长乐区委书记（原长乐市委书记）","start":"2016?","end":"2021","rank":"县处级→副厅级","note":"经历2017年撤市设区"},
    {"id":17,"person_id":11,"org_id":8,"title":"福州市副市长","start":"2021","end":"2021-02","rank":"副厅级","note":"短暂任职后调江西"},
    {"id":18,"person_id":11,"org_id":6,"title":"宜春市委副书记、市长","start":"2021-02","end":"","rank":"正厅级","note":"跨省调动至江西"},

    # 许南吉 — 前任长乐市委书记
    {"id":19,"person_id":12,"org_id":1,"title":"长乐市委书记","start":"2015?","end":"2016?","rank":"县处级","note":"长乐撤市设区前"},
    {"id":20,"person_id":12,"org_id":7,"title":"江西省副省长","start":"","end":"","rank":"副部级","note":"后升任副部级"},

    # 廖海军 — 前任区长
    {"id":21,"person_id":13,"org_id":2,"title":"长乐区区长","start":"2021-06","end":"2026","rank":"县处级","note":"后调任华安县委书记"},
    {"id":22,"person_id":13,"org_id":10,"title":"华安县委书记","start":"2026","end":"至今","rank":"县处级","note":"调任"},

    # 蔡劲松 — 前区长
    {"id":23,"person_id":14,"org_id":2,"title":"长乐区区长（原长乐市长）","start":"2016?","end":"2021-06","rank":"县处级","note":"撤市设区后的首任区长"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 兰文 vs 胡旭彬 — 党政搭档
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档",
     "context":"兰文（区委书记）与胡旭彬（代区长）在长乐区共事，均高配正厅长级",
     "overlap_org":"长乐区","overlap_period":"2026至今"},

    # 兰文 → 张帆 — 前后任
    {"id":2,"person_a":10,"person_b":1,"type":"前后任",
     "context":"张帆（前任书记）→ 兰文（现任书记）",
     "overlap_org":"中共福州市长乐区委员会","overlap_period":"不重叠（前后任）"},

    # 张帆 → 何杰民 — 前后任
    {"id":3,"person_a":11,"person_b":10,"type":"前后任",
     "context":"何杰民（前前任书记）→ 张帆（前任书记）",
     "overlap_org":"中共福州市长乐区委员会","overlap_period":"不重叠（前后任）"},

    # 何杰民 → 许南吉 — 前后任
    {"id":4,"person_a":12,"person_b":11,"type":"前后任",
     "context":"许南吉（长乐市委书记）→ 何杰民（末任市委书记、首任区委书记）",
     "overlap_org":"中共长乐市委/区委","overlap_period":"不重叠（前后任）"},

    # 胡旭彬 → 廖海军 — 前后任
    {"id":5,"person_a":13,"person_b":2,"type":"前后任",
     "context":"廖海军（前任区长）→ 胡旭彬（现任代区长）",
     "overlap_org":"福州市长乐区人民政府","overlap_period":"不重叠（前后任）"},

    # 廖海军 → 蔡劲松 — 前后任
    {"id":6,"person_a":14,"person_b":13,"type":"前后任",
     "context":"蔡劲松（前区长）→ 廖海军（前任区长）",
     "overlap_org":"福州市长乐区人民政府","overlap_period":"不重叠（前后任）"},

    # 何杰民 → 廖海军 — 曾搭档
    {"id":7,"person_a":11,"person_b":13,"type":"党政搭档",
     "context":"何杰民（区委书记）与廖海军（区长）在长乐区共事",
     "overlap_org":"长乐区","overlap_period":"2021.6-2021"},

    # 游昕 — 区委常委→区政府的桥梁角色
    {"id":8,"person_a":3,"person_b":2,"type":"上下级",
     "context":"游昕（区委常委、副区长）协助胡旭彬（代区长）工作",
     "overlap_org":"长乐区人民政府","overlap_period":"至今"},
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
    if "书记" in post and "区委" in post:
        return "230,50,50"  # red for party secretary
    if "区长" in post or "代区长" in post:
        return "50,100,230"  # blue for district mayor
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","新区":"200,255,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>长乐区（福州市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
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
    is_top = any(k in p.get("current_post","") for k in ["区委书记","区长","代区长"])
    sz = "20.0" if is_top else "12.0"
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
print("\n⚠️ NOTE: This data requires verification. Key items:")
print("  1. Verify 兰文's full name and birth/education details")
print("  2. Verify 张帆 and 何杰民's exact tenure months")
print("  3. Complete career timelines for all officials")
print("  4. Standing committee members (区纪委、组织部、宣传部、政法委等) pending addition")
