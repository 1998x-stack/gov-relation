#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 西充县 leadership network."""

import sqlite3
import os
from xml.etree import ElementTree as ET

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(OUT_DIR, "xichong_network.db")
GEXF_PATH = os.path.join(OUT_DIR, "xichong_network.gexf")

# ============================================================
# DATA
# ============================================================

persons = [
    # core leaders (note: most info is "待查" = to be confirmed)
    {"id": "xichong_he_peng", "name": "何鹏", "role": "party_secretary", "gender": "男", "ethnicity": "汉族", "current_post": "西充县委书记", "current_org": "中共西充县委"},
    {"id": "xichong_zhang_hongbo", "name": "张洪波", "role": "mayor", "gender": "男", "ethnicity": "汉族", "current_post": "西充县委副书记、县长", "current_org": "西充县人民政府"},
    {"id": "xichong_zhang_hong", "name": "张洪", "role": "deputy_secretary", "gender": "男", "ethnicity": "汉族", "current_post": "西充县委副书记", "current_org": "中共西充县委"},
    
    # Standing committee members
    {"id":"xichong_gong_cheng", "name": "龚诚", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、副县长", "current_org": "西充县人民政府"},
    {"id":"xichong_tu_jidong", "name": "屠继东", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、政法委书记", "current_org": "中共西充县委"},
    {"id":"xichong_tu_kaimei", "name": "涂开美", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、统战部部长", "current_org": "中共西充县委"},
    {"id":"xichong_yao_yan", "name": "姚艳", "role": "other", "gender": "女", "ethnicity": "汉族", "current_post": "县委常委、总工会主席", "current_org": "西充县总工会"},
    {"id":"xichong_peng_yongjin", "name": "彭永金", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、人武部部长", "current_org": "西充县人武部"},
    {"id":"xichong_zhao_quanyu", "name": "赵全昱", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、组织部部长", "current_org": "中共西充县委"},
    {"id":"xichong_huang_yongqiang", "name": "黄永强", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、宣传部部长", "current_org": "中共西充县委"},
    {"id":"xichong_feng_min", "name": "冯敏", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、纪委书记", "current_org": "中共西充县纪委"},
    {"id":"xichong_su_maoke", "name": "苏茂科", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "县委常委、副县长（挂职）", "current_org": "西充县人民政府"},
    
    # Other county government leaders
    {"id":"xichong_lan_yao", "name": "兰耀", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "副县长、公安局局长", "current_org": "西充县人民政府"},
    {"id":"xichong_li_hongxia", "name": "李红霞", "role": "other", "gender": "女", "ethnicity": "汉族", "current_post": "副县长", "current_org": "西充县人民政府"},
    {"id":"xichong_zhu_jiayu", "name": "朱佳宇", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "副县长", "current_org": "西充县人民政府"},
    {"id":"xichong_li_ling", "name": "李灵", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "副县长", "current_org": "西充县人民政府"},
    {"id":"xichong_wang_honglin", "name": "王洪林", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "副县长", "current_org": "西充县人民政府"},
    
    # Former
    {"id":"xichong_zhang_guangquan", "name": "张光全", "role": "other", "gender": "男", "ethnicity": "汉族", "current_post": "前任西充县委书记（去向待查）", "current_org": "未知"},
]

organizations = [
    {"id":"xichong_party", "name":"中共西充县委", "type":"party", "level":"county"},
    {"id":"xichong_gov", "name":"西充县人民政府", "type":"government", "level":"county"},
    {"id":"xichong_discipline", "name":"西充县纪委监委", "type":"discipline", "level":"county"},
    {"id":"xichong_politics", "name":"西充县委政法委", "type":"party", "level":"county"},
    {"id":"xichong_military", "name":"西充县人武部", "type":"military", "level":"county"},
    {"id":"xichong_union", "name":"西充县总工会", "type":"mass_org", "level":"county"},
    {"id":"xichong_psb", "name":"西充县公安局", "type":"government", "level":"county"},
]

positions = [
    # He Peng
    {"pid":"xichong_he_peng", "org":"xichong_party", "title":"县委书记", "start":"2024-10", "end":""},
    
    # Zhang Hongbo
    {"pid":"xichong_zhang_hongbo", "org":"xichong_party", "title":"县委副书记", "start":"2022-09", "end":""},
    {"pid":"xichong_zhang_hongbo", "org":"xichong_gov", "title":"县长", "start":"2022-09", "end":""},
    
    # Zhang Hong
    {"pid":"xichong_zhang_hong", "org":"xichong_party", "title":"县委副书记", "start":"2025-08", "end":""},
]

relationships = [
    {"a":"xichong_he_peng", "b":"xichong_zhang_hongbo", "type":"collaboration", "context":"书记-县长党政同框，2026年多次联合调研"},
    {"a":"xichong_he_peng", "b":"xichong_zhang_hong", "type":"collaboration", "context":"书记-专职副书记，张洪协助何鹏抓党建"},
    {"a":"xichong_zhang_hongbo", "b":"xichong_zhang_hong", "type":"collaboration", "context":"共同参与何鹏主持的会议活动"},
]

# ============================================================
# BUILD SQLite
# ============================================================

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT, person_b TEXT, type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
)""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 None, None, None, None, None,
                 p["current_post"], p["current_org"], "xichong.gov.cn"))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["name"], o["name"], o["type"], o["level"], None, None))

for pos in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end) VALUES (?,?,?,?,?)",
                (pos["pid"], pos["org"], pos["title"], pos["start"], pos["end"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context) VALUES (?,?,?,?)",
                (r["a"], r["b"], r["type"], r["context"]))

conn.commit()

# Stats
p_count = cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
o_count = cur.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
pos_count = cur.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
rel_count = cur.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

conn.close()

print(f"SQLite: {DB_PATH}")
print(f"  {p_count} persons, {o_count} orgs, {pos_count} positions, {rel_count} relationships")

# ============================================================
# BUILD GEXF
# ============================================================

NS = {
    "ns": "http://gexf.net/1.3",
    "viz": "http://gexf.net/1.3/viz"
}
ET.register_namespace("", "http://gexf.net/1.3")
ET.register_namespace("viz", "http://gexf.net/1.3/viz")

gexf = ET.Element("{http://gexf.net/1.3}gexf", version="1.3")
graph = ET.SubElement(gexf, "{http://gexf.net/1.3}graph",
                      defaultedgetype="undirected",
                      mode="static")

# Attributes
attrs = ET.SubElement(graph, "{http://gexf.net/1.3}attributes", class_type="node")
for name, typ in [("role", "string"), ("current_post", "string")]:
    a = ET.SubElement(attrs, "{http://gexf.net/1.3}attribute", id=name, title=name, type=typ)
    ET.SubElement(a, "{http://gexf.net/1.3}default").text = ""

# Nodes - persons
nodes = ET.SubElement(graph, "{http://gexf.net/1.3}nodes")
person_map = {}
for p in persons:
    n = ET.SubElement(nodes, "{http://gexf.net/1.3}node", id=p["id"], label=p["name"])
    role = p.get("role", "other")
    if role == "party_secretary":
        color = "#E03C31"; size = 20.0
    elif role == "mayor":
        color = "#4A7FB5"; size = 20.0
    elif role == "deputy_secretary":
        color = "#C9A94E"; size = 16.0
    else:
        color = "#888888"; size = 12.0
    
    viz_n = ET.SubElement(n, "{http://gexf.net/1.3/viz}color",
                          r=str(int(color[1:3],16)),
                          g=str(int(color[3:5],16)),
                          b=str(int(color[5:7],16)))
    ET.SubElement(n, "{http://gexf.net/1.3/viz}size", value=str(size))
    
    # Attribute values
    av = ET.SubElement(n, "{http://gexf.net/1.3}attvalues")
    ET.SubElement(av, "{http://gexf.net/1.3}attvalue", for_="role", value=role)
    ET.SubElement(av, "{http://gexf.net/1.3}attvalue", for_="current_post", value=p["current_post"])
    
    person_map[p["id"]] = p["name"]

# Nodes - orgs
for o in organizations:
    n = ET.SubElement(nodes, "{http://gexf.net/1.3}node", id=o["name"], label=o["name"])
    c = {"party":"#E8A040", "government":"#40A040", "discipline":"#C04040",
         "military":"#8040C0", "mass_org":"#A06040"}.get(o.get("type",""), "#888888")
    ET.SubElement(n, "{http://gexf.net/1.3/viz}color",
                  r=str(int(c[1:3],16)), g=str(int(c[3:5],16)), b=str(int(c[5:7],16)))
    ET.SubElement(n, "{http://gexf.net/1.3/viz}size", value="8.0")

# Edges
edges = ET.SubElement(graph, "{http://gexf.net/1.3}edges")
edge_id = 0

# person -> org (worked_at)
for pos in positions:
    e = ET.SubElement(edges, "{http://gexf.net/1.3}edge",
                      id=str(edge_id), source=pos["pid"], target=pos["org"])
    e.set("label", pos["title"])      }
    e.set("type", "directed")
    eid += 1

# person -> person (relationship)
for r in relationships:
    e = ET.SubElement(edges, "{http://gexf.net/1.3}edge",
                      id=str(edge_id), source=r["a"], target=r["b"])
    e.set("label", r["context"])
    if r.get("type") == "strong":
        # Gold color for confirm relationships
        for attr in [("color", "200,169,78"), ("thickness", "3.0")]:
            pass  # vis attributes not in GEXF
    edge_id += 1

tree_data = ET.tostring(gexf, encoding="utf-8", xml_declaration=True).decode()
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(tree_data)

print(f"GEXF: {GEXF_PATH}")
print("Done.")
