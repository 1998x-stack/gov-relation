#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for Deng Zhiwu career investigation."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/dengzhiwu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/dengzhiwu_network.gexf")

persons = [
    {"id":1,"name":"邓之武","gender":"男","ethnicity":"汉族","birth":"1976-02","birthplace":"江西万年","education":"浙江大学茶学学士+江西财大MBA","party_join":"1995-12","work_start":"1998-08","current_post":"东湖区委副书记、代区长","current_org":"中共南昌市东湖区委员会","source":"https://www.jxxinjian.jcy.gov.cn/xjzc/202412/t20241220_6769537.shtml"},
    {"id":2,"name":"贾彧超","gender":"男","ethnicity":"汉族","birth":"1976-09","birthplace":"湖北襄阳","education":"中国科学技术大学管理学学士","party_join":"2002-09","work_start":"2000-07","current_post":"南昌县委书记、小蓝经开区党工委书记","current_org":"中共南昌县委员会","source":"https://baike.baidu.com/item/%E8%B4%BE%E5%BD%A7%E8%B6%85/20265811"},
    {"id":3,"name":"徐强","gender":"男","ethnicity":"汉族","birth":"1974-11","birthplace":"江西南昌县","education":"南昌航空工业学院+江西财大MPA","party_join":"1996-06","work_start":"1996-09","current_post":"新建区委书记（原进贤县委书记）","current_org":"中共南昌市新建区委员会","source":"https://baike.baidu.com/item/%E5%BE%90%E5%BC%BA/50081202"},
    {"id":4,"name":"刘光荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"江西南昌县","education":"","party_join":"中共党员","work_start":"1995","current_post":"东湖区委书记","current_org":"中共南昌市东湖区委员会","source":"http://dhq.nc.gov.cn"},
    {"id":5,"name":"帅志","gender":"男","ethnicity":"汉族","birth":"1975-10","birthplace":"江西南昌","education":"省委党校研究生，法学学士","party_join":"2001-06","work_start":"1996-09","current_post":"南昌县委副书记、县长","current_org":"南昌县人民政府","source":"https://baike.baidu.com/item/%E5%B8%85%E5%BF%97"},
    {"id":6,"name":"熊振强","gender":"男","ethnicity":"汉族","birth":"1972-03","birthplace":"江西奉新","education":"大学","party_join":"1992-12","work_start":"1991-09","current_post":"进贤县委书记","current_org":"中共进贤县委员会","source":"https://baike.baidu.com/item/%E7%86%8A%E6%8C%AF%E5%BC%BA/7691320"},
    {"id":7,"name":"雷桥亮","gender":"男","ethnicity":"汉族","birth":"1980-11","birthplace":"江西井冈山","education":"研究生，经济学硕士","party_join":"中共党员","work_start":"","current_post":"进贤县委副书记、代县长","current_org":"进贤县人民政府","source":"https://baike.baidu.com/item/%E9%9B%B7%E6%A1%A5%E4%BA%AE/61369190"},
]

organizations = [
    {"id":1,"name":"江西省蚕桑茶叶研究所","type":"事业单位","level":"省级","parent":"江西省农业厅","location":"江西省南昌市"},
    {"id":2,"name":"南昌市外经贸委","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":3,"name":"南昌市投资促进局","type":"政府","level":"市级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":4,"name":"南昌高新技术产业开发区","type":"开发区","level":"国家级","parent":"南昌市人民政府","location":"江西省南昌市"},
    {"id":5,"name":"中共进贤县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市进贤县"},
    {"id":6,"name":"进贤县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市进贤县"},
    {"id":7,"name":"中共南昌县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市南昌县"},
    {"id":8,"name":"南昌县人民政府","type":"政府","level":"县级","parent":"南昌市人民政府","location":"江西省南昌市南昌县"},
    {"id":9,"name":"中共南昌市东湖区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市东湖区"},
    {"id":10,"name":"东湖区人民政府","type":"政府","level":"区级","parent":"南昌市人民政府","location":"江西省南昌市东湖区"},
    {"id":11,"name":"中共南昌市新建区委员会","type":"党委","level":"区级","parent":"中共南昌市委员会","location":"江西省南昌市新建区"},
    {"id":12,"name":"小蓝经济技术开发区","type":"开发区","level":"国家级","parent":"南昌市人民政府","location":"江西省南昌市南昌县"},
    {"id":13,"name":"中共安义县委员会","type":"党委","level":"县级","parent":"中共南昌市委员会","location":"江西省南昌市安义县"},
    {"id":14,"name":"中共南昌市委组织部","type":"党委","level":"市级","parent":"中共南昌市委员会","location":"江西省南昌市"},
]

positions = [
    # ── 邓之武 ──
    # Gap: 1998.08-2002.04 -- year+ at 蚕桑茶叶研究所 (inferred)
    {"id":1,"person_id":1,"org_id":1,"title":"（推测）科员→副科长","start":"1998-08","end":"2002-04","rank":"科员级","note":"⚠️ 推断：茶学专业毕业后在蚕桑茶叶研究所工作，此后调入外经贸委。此段无确切公开信息来源。"},
    {"id":2,"person_id":1,"org_id":2,"title":"区域合作处副处长→投资促进处处长","start":"2002-05","end":"2015-09","rank":"科级","note":"约13年"},
    {"id":3,"person_id":1,"org_id":3,"title":"副局长（副处级）","start":"2015-09","end":"2019-06","rank":"副处级","note":"2017-2018借调南昌高新区"},
    {"id":4,"person_id":1,"org_id":5,"title":"县委常委、组织部部长","start":"2019-06","end":"2023-02","rank":"副处级","note":"约3.5年"},
    {"id":5,"person_id":1,"org_id":5,"title":"县委常委、县政府党组副书记、常务副县长、三级调研员","start":"2023-02","end":"2025-01","rank":"副处级","note":"2024.12.19任前公示：拟任县区委副书记"},
    {"id":6,"person_id":1,"org_id":7,"title":"县委副书记","start":"2025-01","end":"2026-07","rank":"正处级","note":"在县委书记贾彧超领导下工作约6个月"},
    {"id":7,"person_id":1,"org_id":9,"title":"区委副书记、代区长","start":"2026-07","end":"","rank":"正处级","note":"2026.07.07任命"},

    # ── 贾彧超 ──
    {"id":8,"person_id":2,"org_id":7,"title":"县委书记","start":"2025-02","end":"","rank":"副厅级","note":"邓之武在南昌县期间的直接上级"},
    {"id":9,"person_id":2,"org_id":8,"title":"县长","start":"2021-08","end":"2025-02","rank":"副厅级","note":""},

    # ── 徐强 ──
    {"id":10,"person_id":3,"org_id":5,"title":"县委书记","start":"2021-08","end":"2026-06","rank":"正处级","note":"邓之武在进贤期间的县委书记"},
    {"id":11,"person_id":3,"org_id":11,"title":"区委书记","start":"2026-06","end":"","rank":"正处级","note":""},

    # ── 刘光荣 ──
    {"id":12,"person_id":4,"org_id":9,"title":"区委书记","start":"2025-02","end":"","rank":"正处级","note":"南昌县21年工作经历；与邓之武均来自南昌县"},
    {"id":13,"person_id":4,"org_id":8,"title":"副县长/常务副县长等各岗位","start":"1995","end":"2025-02","rank":"副处级→正处级","note":"在南昌县工作21年"},
]

relationships = [
    {"id":1,"person_a":1,"person_b":2,"type":"直接上下级","context":"邓之武（南昌县委副书记）直属贾彧超（南昌县委书记）领导约6个月（2025.01-2025.07）","overlap_org":"南昌县","overlap_period":"2025-01至2025-07"},
    {"id":2,"person_a":1,"person_b":3,"type":"班子共事","context":"邓之武在进贤县任组织部长/常务副县长期间，徐强任进贤县委书记（2021.08-2024.12），共事约3年","overlap_org":"进贤县","overlap_period":"2021-08至2024-12"},
    {"id":3,"person_a":1,"person_b":4,"type":"现任搭档","context":"刘光荣（东湖区委书记）与邓之武（东湖代区长）为现任党政搭档；二人均有南昌县工作经历","overlap_org":"东湖区","overlap_period":"2026-07至今"},
    {"id":4,"person_a":1,"person_b":4,"type":"南昌县系","context":"刘光荣南昌县21年+邓之武南昌县委副书记18个月——东湖区党政主官均来自南昌县","overlap_org":"南昌县","overlap_period":"间接重叠"},
    {"id":5,"person_a":1,"person_b":5,"type":"南昌县同事","context":"邓之武（县委副书记）与帅志（先任县委副书记→后任县长）在南昌县有过短暂共事","overlap_org":"南昌县","overlap_period":"2025-12至2026-07"},
    {"id":6,"person_a":1,"person_b":6,"type":"前后任同僚","context":"邓之武在进贤县后熊振强接任进贤县委书记（2026.06），两人在进贤系统有间接联系","overlap_org":"进贤县","overlap_period":"间接"},
    {"id":7,"person_a":1,"person_b":7,"type":"进贤前后任","context":"邓之武（前进贤常务副县长）与雷桥亮（进贤代县长）同属进贤县经济口主管","overlap_org":"进贤县","overlap_period":"间接"},
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
for table in ["persons","organizations","positions","relationships"]:
    c.execute(f"SELECT COUNT(*) FROM {table}")
    counts[table] = c.fetchone()[0]
conn.close()
print(f"SQLite DB written: {DB_PATH}")
print(f"  persons={counts['persons']}, organizations={counts['organizations']}, positions={counts['positions']}, relationships={counts['relationships']}")

# ── BUILD GEXF ──
from xml.sax.saxutils import escape

edge_id = 0
def next_edge():
    global edge_id
    edge_id += 1
    return f"e{edge_id}"

# Color map
COLOR_PARTY = {"r":"180","g":"30","b":"30"}   # red - party secretary
COLOR_GOV = {"r":"30","g":"90","b":"180"}     # blue - government leader
COLOR_DISCIPLINE = {"r":"230","g":"120","b":"30"} # orange
COLOR_PERSON_OTHER = {"r":"160","g":"160","b":"160"} # grey - other persons
COLOR_ORG_PARTY = {"r":"255","g":"200","b":"200"} # light pink
COLOR_ORG_GOV = {"r":"200","g":"200","b":"255"}   # light blue
COLOR_ORG_DEVELOP = {"r":"200","g":"255","b":"200"} # light green
COLOR_ORG_OTHER = {"r":"220","g":"220","b":"220"} # light grey

def node_color(role_type):
    return COLOR_PERSON_OTHER
def org_color(o_type):
    m = {"党委":COLOR_ORG_PARTY,"政府":COLOR_ORG_GOV,"开发区":COLOR_ORG_DEVELOP}
    return m.get(o_type, COLOR_ORG_OTHER)

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('<meta lastmodifieddate="%s">' % datetime.now().strftime("%Y-%m-%d"))
gexf_parts.append('<creator>OpenCode gov-relation network builder</creator>')
gexf_parts.append('<description>邓之武（东湖代区长）职业生涯关系网络</description>')
gexf_parts.append('</meta>')
gexf_parts.append('<graph mode="static" defaultedgetype="undirected">')

# Attributes
gexf_parts.append('<attributes class="node">')
gexf_parts.append('<attribute id="type" title="Type" type="string"/>')
gexf_parts.append('<attribute id="role" title="Role" type="string"/>')
gexf_parts.append('<attribute id="birth" title="Birth" type="string"/>')
gexf_parts.append('<attribute id="birthplace" title="Birthplace" type="string"/>')
gexf_parts.append('<attribute id="education" title="Education" type="string"/>')
gexf_parts.append('</attributes>')
gexf_parts.append('<attributes class="edge">')
gexf_parts.append('<attribute id="type" title="Edge Type" type="string"/>')
gexf_parts.append('<attribute id="period" title="Period" type="string"/>')
gexf_parts.append('<attribute id="context" title="Context" type="string"/>')
gexf_parts.append('</attributes>')

gexf_parts.append('<nodes>')

# Persons
for p in persons:
    rid = "dengzhiwu_%s" % p["name"]
    label = "%s\n%s" % (p["name"], p["current_post"][:20])
    
    # Determine color by role type
    role_desc = p.get("current_post","")
    if "书记" in role_desc and "区委" in role_desc or "县委" in role_desc:
        clr = {"r":"180","g":"30","b":"30"}
    elif "区长" in role_desc or "县长" in role_desc or "副县长" in role_desc:
        clr = {"r":"30","g":"90","b":"180"}
    elif "纪委" in role_desc:
        clr = {"r":"230","g":"120","b":"30"}
    else:
        clr = {"r":"160","g":"160","b":"160"}
    
    size = "20.0" if p["name"] == "邓之武" else "12.0"
    
    gexf_parts.append('<node id="%s" label="%s">' % (escape(rid), escape(label)))
    gexf_parts.append('<attvalues>')
    gexf_parts.append('<attvalue for="type" value="person"/>')
    gexf_parts.append('<attvalue for="role" value="%s"/>' % escape(role_desc[:50]))
    gexf_parts.append('<attvalue for="birth" value="%s"/>' % p.get("birth",""))
    gexf_parts.append('<attvalue for="birthplace" value="%s"/>' % p.get("birthplace",""))
    gexf_parts.append('<attvalue for="education" value="%s"/>' % escape(p.get("education","")[:50]))
    gexf_parts.append('</attvalues>')
    gexf_parts.append('<viz:color r="%s" g="%s" b="%s" a="1"/>' % (clr["r"],clr["g"],clr["b"]))
    gexf_parts.append('<viz:size value="%s"/>' % size)
    gexf_parts.append('</node>')

# Organizations
for o in organizations:
    oid = "org_%d" % o["id"]
    label = o["name"]
    clr = org_color(o["type"])
    gexf_parts.append('<node id="%s" label="%s">' % (escape(oid), escape(label)))
    gexf_parts.append('<attvalues>')
    gexf_parts.append('<attvalue for="type" value="org"/>')
    gexf_parts.append('<attvalue for="role" value="%s %s"/>' % (o["type"], o["level"]))
    gexf_parts.append('</attvalues>')
    gexf_parts.append('<viz:color r="%s" g="%s" b="%s" a="1"/>' % (clr["r"],clr["g"],clr["b"]))
    gexf_parts.append('<viz:size value="8.0"/>')
    gexf_parts.append('</node>')

gexf_parts.append('</nodes>')
gexf_parts.append('<edges>')

# Position edges (person -> org)
for pos in positions:
    pid = "dengzhiwu_%s" % next((p["name"] for p in persons if p["id"]==pos["person_id"]), "")
    oid = "org_%d" % pos["org_id"]
    eid = next_edge()
    label = "%s (%s-%s)" % (pos["title"], pos["start"], pos["end"] if pos["end"] else "至今")
    gexf_parts.append('<edge id="%s" source="%s" target="%s" label="%s" weight="1">' % (eid, escape(pid), escape(oid), escape(label)))
    gexf_parts.append('<attvalues>')
    gexf_parts.append('<attvalue for="type" value="worked_at"/>')
    gexf_parts.append('<attvalue for="period" value="%s—%s"/>' % (pos["start"], pos["end"] if pos["end"] else "至今"))
    gexf_parts.append('<attvalue for="context" value="%s"/>' % escape(pos.get("note","")[:100]))
    gexf_parts.append('</attvalues>')
    gexf_parts.append('</edge>')

# Relationship edges (person <-> person)
for r in relationships:
    pa = "dengzhiwu_%s" % next((p["name"] for p in persons if p["id"]==r["person_a"]), "")
    pb = "dengzhiwu_%s" % next((p["name"] for p in persons if p["id"]==r["person_b"]), "")
    eid = next_edge()
    # Determine edge weight by relationship strength
    if "直接上下级" in r["type"] or "现任搭档" in r["type"]:
        weight = "3"
    elif "班子共事" in r["type"] or "同事" in r["type"]:
        weight = "2"
    else:
        weight = "1"
    gexf_parts.append('<edge id="%s" source="%s" target="%s" label="%s" weight="%s">' % (eid, escape(pa), escape(pb), escape(r["type"]), weight))
    gexf_parts.append('<attvalues>')
    gexf_parts.append('<attvalue for="type" value="relationship"/>')
    gexf_parts.append('<attvalue for="period" value="%s"/>' % r["overlap_period"])
    gexf_parts.append('<attvalue for="context" value="%s"/>' % escape(r["context"][:150]))
    gexf_parts.append('</attvalues>')
    gexf_parts.append('</edge>')

gexf_parts.append('</edges>')
gexf_parts.append('</graph>')
gexf_parts.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"GEXF graph written: {GEXF_PATH}")
print("Done!")
