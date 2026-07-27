#!/usr/bin/env python3
import sqlite3, os

OUT = "/workspace/data/xieming/other-codes/gov-relation"
DB = os.path.join(OUT, "zigong_network.db")
GF = os.path.join(OUT, "zigong_network.gexf")

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# ── data ──
persons = [
    ("z","曾洪扬","男","汉族","1972-02","四川广汉","上海交大","1993-03","1994-07","自贡市委书记","中共自贡市委","百度/川观"),
    ("s","石钢","男","汉族","1970-07","四川渠县","西南财大","1999-06","1991-07","自贡市市长","自贡市政府","百度"),
    ("h","何礼","男","汉族","","","","","","离任(原自贡市委书记)","","川观2023.2"),
    ("f","范波","男","汉族","","","","","","山东省任职(原自贡书记)","山东省","百度"),
    ("lg","李刚","男","汉族","","","","","","历任巴中市委等","","百度"),
    ("hx","黄雪智","男","汉族","","","","","","原副市长(已免)","自贡市政府","人大公告"),
    ("zb","朱斌","男","汉族","","","","","","市人大副主任","自贡市人大","2025.2"),
    ("tb","谭豹","男","汉族","","","","","","市人大主任","自贡市人大","自贡人大网"),
    ("yz","张颖","男","汉族","","","","","","副市长","自贡市政府","2025.12"),
    ("hrb","黄如贝","男","汉族","","","","","","市政府秘书长","自贡市政府","2025.12"),
]
orgs = [
    ("city","自贡市","地级市","prefecture","四川省","四川"),
    ("cpc","中共自贡市委","党委","prefecture","四川省委","自贡"),
    ("gov","自贡市政府","政府","prefecture","自贡市委","自贡"),
    ("npc","自贡市人大","人大","prefecture","","自贡"),
    ("leshan_cpc","中共乐山市委","党委","prefecture","四川省委","乐山"),
    ("housing","四川省住建厅","政府厅局","dept","四川省","成都"),
    ("finance","四川省财政厅","政府厅局","dept","四川省","成都"),
    ("ndrc","四川省发改委","政府厅局","dept","四川省","成都"),
    ("shandong","山东省","省份","province","中国","山东"),
    ("guangan","广安市","地级市","prefecture","四川省","广安"),
    ("bazhong","巴中市","地级市","prefecture","四川省","巴中"),
]
positions = [
    ("z","guangan","广安市工作","1994","2015","","起步"),
    ("z","leshan_cpc","乐山市委副书记","2016","2021","","跨市"),
    ("z","gov","自贡市长","2021","2023.2","chief",""),
    ("z","cpc","自贡市委书记","2023.2","","chief",""),
    ("s","housing","省住建厅副厅长","","2023","","来源"),
    ("s","gov","自贡市长","2023","","chief",""),
    ("h","finance","省财政厅","","","",""),
    ("h","cpc","自贡市委书记","2021","2023.2","chief","卸任"),
    ("f","ndrc","省发改委","","2017","",""),
    ("f","cpc","自贡市委书记","2017","2021","chief","跨省"),
    ("f","shandong","山东省任职","2021","","","跨省"),
    ("lg","cpc","自贡市委书记","","2016","chief","前任"),
    ("zb","gov","市政府秘书长","","2025.2","deputy",""),
    ("zb","npc","市人大副主任","2025.2","","deputy",""),
    ("hx","gov","副市长","","","deputy","已免"),
    ("yz","gov","副市长","2025.12","","deputy","新"),
    ("hrb","gov","秘书长","2025.12","","deputy","新"),
    ("tb","npc","市人大主任","","","chief",""),
]
relationships = [
    ("z","h","succession","曾接替何任书记","cpc","2023"),
    ("h","f","succession","何接替范","cpc","约2021"),
    ("lg","f","succession","李→范","cpc","约2017"),
    ("z","s","colleague","曾+石搭班子","cpc","2023至今"),
]

if os.path.exists(DB): os.remove(DB)
if os.path.exists(GF): os.remove(GF)

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript("""
CREATE TABLE persons (id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT, current_post TEXT, current_org TEXT, source TEXT);
CREATE TABLE organizations (id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT);
CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT, FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT, FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id));
""")
for p in persons: cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
for o in orgs: cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
for po in positions: cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)", po)
for r in relationships: cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", r)
conn.commit(); conn.close()
print(f"[✓] SQLite {DB} — {len(persons)}p {len(orgs)}o {len(positions)}pos {len(relationships)}rels")

# ── GEXF ──
def color(role):
    if "书记" in role and "副" not in role: return 'r="200" g="40" b="50" sz="20.0"'
    if "市长" in role and "副" not in role: return 'r="30" g="100" b="200" sz="20.0"'
    if "副" in role: return 'r="240" g="140" b="30" sz="12.0"'
    return 'r="150" g="150" b="150" sz="12.0"'

nxml = ""
for p in persons:
    c = color(p[9])
    nxml += f'  <node id="n_{esc(p[0])}" label="{esc(p[1])}\\n{esc(p[9])}"><viz:color {c} /><viz:size value="20.0"/></node>\n'
for o in orgs:
    c = 'r="80" g="180" b="80"'
    nxml += f'  <node id="o_{esc(o[0])}" label="{esc(o[1])}"><viz:color {c} /><viz:size value="8.0"/></node>\n'

exml = ""
eid = 0
for po in positions:
    eid += 1
    exml += f'  <edge id="e{eid}" source="n_{esc(po[0])}" target="o_{esc(po[1])}"><attvalues><attvalue for="title" value="{esc(po[2])}" /></attvalues></edge>\n'
for r in relationships:
    eid += 1
    exml += f'  <edge id="e{eid}" source="n_{esc(r[0])}" target="n_{esc(r[1])}" type="succession"><attvalues><attvalue for="title" value="{esc(r[3])}" /></attvalues></edge>\n'

gfxml = f'''<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta><description>自贡干部交流网络 2026-07-26</description></meta>
  <graph mode="static" defaultedgetype="directed">
    <attributes class="edge">
      <attribute id="type" title="edge_type" type="string"/>
      <attribute id="title" title="title" type="string"/>
    </attributes>
    <nodes>{nxml}</nodes>
    <edges>{exml}</edges>
  </graph>
</gexf>'''
with open(GF,"w",encoding="utf-8") as f:
    f.write(gexml)
print(f"[GEXF] {GF} ({len(persons)+len(orgs)} nodes, {eid} edges)")
print("DONE")
