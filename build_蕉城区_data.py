#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 蕉城区 (Jiaocheng District), 宁德市 (Ningde City), 福建省.

Covers: District Party Secretary (区委书记), District Mayor (区长),
key leadership (四大班子), predecessor/successor chains, and the district leadership network.

Current leadership as of 2026-01:
  区委书记: 陈绍曦 (promoted from 区长, 2025.12)
  区长: 王云盛 (appointed acting 2025.12.31, elected 2026.01.02)
  区人大常委会主任: 钟宜国
  区政协主席: 陈秀莺

Sources:
- Baidu Baike: 蕉城区, 陈绍曦, 王云盛, 何必良
- Baidu Baike appointment references
- Baidu Baike news articles

Generated: 2026-07-17
"""

import sqlite3, os, json, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "蕉城区_network.db")
GEXF_PATH = os.path.join(BASE, "蕉城区_network.gexf")
PERSONS_DIR = BASE

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 陈绍曦 — 蕉城区委书记 (appointed 2025.12)
    {"id":1,"name":"陈绍曦","gender":"男","ethnicity":"汉族",
     "birth":"1971-10","birthplace":"福建福安",
     "education":"大学学历",
     "party_join":"中共党员","work_start":"",
     "current_post":"蕉城区委书记","current_org":"中共蕉城区委员会",
     "source":"https://baike.baidu.com/item/%E9%99%88%E7%BB%8D%E6%9B%A6"},

    # 王云盛 — 蕉城区区长 (appointed 2025.12.31 acting, 2026.01.02 elected)
    {"id":2,"name":"王云盛","gender":"男","ethnicity":"汉族",
     "birth":"1974-07","birthplace":"",
     "education":"大学学历，工学学士学位",
     "party_join":"中共党员","work_start":"1996-12",
     "current_post":"蕉城区区长","current_org":"蕉城区人民政府",
     "source":"https://baike.baidu.com/item/%E7%8E%8B%E4%BA%91%E7%9B%9B"},

    # 钟宜国 — 蕉城区人大常委会主任
    {"id":3,"name":"钟宜国","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"蕉城区人大常委会主任","current_org":"蕉城区人大常委会",
     "source":"https://baike.baidu.com/item/%E9%92%9F%E5%AE%9C%E5%9B%BD"},

    # 陈秀莺 — 蕉城区政协主席
    {"id":4,"name":"陈秀莺","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"蕉城区政协主席","current_org":"政协蕉城区委员会",
     "source":"https://baike.baidu.com/item/%E8%95%89%E5%9F%8E%E5%8C%BA"},

    # ── Predecessors ──
    # 何必良 — 前任区委书记 (promoted to 市政协副主席 2025.01)
    {"id":5,"name":"何必良","gender":"男","ethnicity":"汉族",
     "birth":"1967-09","birthplace":"福建仙游",
     "education":"高级工程师",
     "party_join":"中共党员","work_start":"",
     "current_post":"宁德市政协副主席","current_org":"政协宁德市委员会",
     "source":"https://baike.baidu.com/item/%E4%BD%95%E5%BF%85%E8%89%AF"},

    # 陈绍曦 also served as 区长 (predecessor to 王云盛) - same person as id=1
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共蕉城区委员会","type":"党委","level":"县级","parent":"中共宁德市委员会","location":"蕉城区"},
    {"id":2,"name":"蕉城区人民政府","type":"政府","level":"县级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":3,"name":"蕉城区人大常委会","type":"人大","level":"县级","parent":"宁德市人大常委会","location":"蕉城区"},
    {"id":4,"name":"政协蕉城区委员会","type":"政协","level":"县级","parent":"政协宁德市委员会","location":"蕉城区"},
    {"id":5,"name":"福安市社口镇党委","type":"党委","level":"乡镇级","parent":"中共福安市委员会","location":"福安市"},
    {"id":6,"name":"福安市阳头街道办事处","type":"政府","level":"乡镇级","parent":"福安市人民政府","location":"福安市"},
    {"id":7,"name":"福安市阳头街道党工委","type":"党委","level":"乡镇级","parent":"中共福安市委员会","location":"福安市"},
    {"id":8,"name":"东侨经济技术开发区管委会","type":"开发区","level":"县级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":9,"name":"中共霞浦县委统战部","type":"党委","level":"县级","parent":"中共霞浦县委员会","location":"霞浦县"},
    {"id":10,"name":"霞浦县人民政府","type":"政府","level":"县级","parent":"宁德市人民政府","location":"霞浦县"},
    {"id":11,"name":"宁德市人民政府办公室","type":"政府","level":"地市级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":12,"name":"宁德市委军民融合办","type":"党委","level":"地市级","parent":"中共宁德市委员会","location":"蕉城区"},
    {"id":13,"name":"宁德市生态环境局","type":"政府","level":"地市级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":14,"name":"宁德市交通运输局","type":"政府","level":"地市级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":15,"name":"宁德市人民政府防汛抗旱指挥部办公室","type":"政府","level":"地市级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":16,"name":"中共古田县委","type":"党委","level":"县级","parent":"中共宁德市委员会","location":"古田县"},
    {"id":17,"name":"宁德市交通工程勘察设计院","type":"事业单位","level":"地市级","parent":"宁德市交通运输局","location":"蕉城区"},
    {"id":18,"name":"宁德宁武高速公路有限责任公司","type":"事业单位","level":"地市级","parent":"宁德市交通运输局","location":"蕉城区"},
    {"id":19,"name":"宁德市城建集团有限公司","type":"事业单位","level":"地市级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":20,"name":"宁德市住房和城乡建设局","type":"政府","level":"地市级","parent":"宁德市人民政府","location":"蕉城区"},
    {"id":21,"name":"蕉城区人民武装部","type":"党委","level":"县级","parent":"宁德军分区","location":"蕉城区"},
    {"id":22,"name":"政协宁德市委员会","type":"政协","level":"地市级","parent":"","location":"蕉城区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 陈绍曦 (id=1) - career timeline
    {"person_id":1,"org_id":5,"title":"福安市社口镇党委副书记、镇长","start":"","end":"","rank":"正科级","note":""},
    {"person_id":1,"org_id":6,"title":"福安市阳头街道办事处主任","start":"","end":"","rank":"正科级","note":""},
    {"person_id":1,"org_id":7,"title":"福安市阳头街道党工委书记","start":"","end":"","rank":"正科级","note":""},
    {"person_id":1,"org_id":8,"title":"东侨经济技术开发区管委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"person_id":1,"org_id":9,"title":"霞浦县委常委、统战部部长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":1,"org_id":10,"title":"霞浦县委常委、政府副县长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":1,"org_id":11,"title":"宁德市政府副秘书长、市政府办党组成员","start":"","end":"","rank":"正处级","note":""},
    {"person_id":1,"org_id":12,"title":"宁德市委军民融合办常务副主任","start":"","end":"","rank":"正处级","note":""},
    {"person_id":1,"org_id":13,"title":"宁德市生态环境局党组书记、局长","start":"","end":"","rank":"正处级","note":""},
    {"person_id":1,"org_id":1,"title":"蕉城区委副书记、区政府党组书记","start":"","end":"2025-12","rank":"正处级","note":"Before promotion to secretary"},
    {"person_id":1,"org_id":2,"title":"蕉城区区长","start":"","end":"2025-12","rank":"正处级","note":"Served as mayor before becoming secretary"},
    {"person_id":1,"org_id":1,"title":"蕉城区委书记","start":"2025-12","end":"present","rank":"副厅级","note":"Promoted from 区长 to 区委书记, briefly held both roles"},
    {"person_id":1,"org_id":21,"title":"蕉城区人武部党委第一书记","start":"2026-02","end":"present","rank":"","note":""},

    # 王云盛 (id=2)
    {"person_id":2,"org_id":15,"title":"宁德市人民政府防汛抗旱指挥部办公室主任","start":"","end":"","rank":"","note":""},
    {"person_id":2,"org_id":14,"title":"宁德市人民政府办公室副主任","start":"","end":"","rank":"副处级","note":""},
    {"person_id":2,"org_id":16,"title":"古田县委副书记","start":"","end":"","rank":"副处级","note":""},
    {"person_id":2,"org_id":14,"title":"宁德市交通运输局党组书记、局长","start":"2022-03","end":"2026-01","rank":"正处级","note":""},
    {"person_id":2,"org_id":2,"title":"蕉城区人民政府副区长、代理区长","start":"2025-12-31","end":"2026-01","rank":"正处级","note":"Appointed acting mayor"},
    {"person_id":2,"org_id":1,"title":"蕉城区委副书记","start":"2026-01","end":"present","rank":"正处级","note":""},
    {"person_id":2,"org_id":2,"title":"蕉城区区长","start":"2026-01-02","end":"present","rank":"正处级","note":"Elected district mayor"},

    # 钟宜国 (id=3)
    {"person_id":3,"org_id":3,"title":"蕉城区人大常委会主任","start":"","end":"present","rank":"正处级","note":"Current role"},

    # 陈秀莺 (id=4)
    {"person_id":4,"org_id":4,"title":"蕉城区政协主席","start":"","end":"present","rank":"正处级","note":"Current role"},

    # 何必良 (id=5)
    {"person_id":5,"org_id":17,"title":"宁德市交通工程勘察设计院书记、院长","start":"","end":"","rank":"","note":""},
    {"person_id":5,"org_id":14,"title":"宁德市交通运输局副局长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":5,"org_id":18,"title":"宁德宁武高速公路有限责任公司总经理","start":"","end":"","rank":"","note":""},
    {"person_id":5,"org_id":19,"title":"宁德市城建集团有限公司党委书记、董事长","start":"","end":"","rank":"正处级","note":""},
    {"person_id":5,"org_id":20,"title":"宁德市住房和城乡建设局党组书记、局长","start":"","end":"","rank":"正处级","note":""},
    {"person_id":5,"org_id":2,"title":"蕉城区区长","start":"","end":"","rank":"正处级","note":""},
    {"person_id":5,"org_id":1,"title":"蕉城区委书记","start":"","end":"2025-01","rank":"副厅级","note":""},
    {"person_id":5,"org_id":22,"title":"宁德市政协副主席","start":"2025-01","end":"present","rank":"副厅级","note":"Promoted from district party secretary"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 陈绍曦 ↔ 何必良 (predecessor-successor)
    {"person_a":1,"person_b":5,"type":"predecessor_successor","context":"陈绍曦接替何必良任蕉城区委书记","overlap_org":"中共蕉城区委员会","overlap_period":"","direction":"person_to_other","strength":"strong"},

    # 陈绍曦 ↔ 王云盛 (predecessor-successor as mayor)
    {"person_a":1,"person_b":2,"type":"predecessor_successor","context":"陈绍曦任区长时，王云盛接替其任区长","overlap_org":"蕉城区人民政府","overlap_period":"2025-12","direction":"person_to_other","strength":"strong"},

    # 陈绍曦 ↔ 王云盛 (superior-subordinate)
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"陈绍曦作为区委书记，王云盛为区长，党政正职搭档","overlap_org":"中共蕉城区委员会/蕉城区人民政府","overlap_period":"2026-01至今","direction":"person_to_other","strength":"strong"},

    # 何必良 ↔ 陈绍曦 (superior-subordinate, former mayor-secretary)
    {"person_a":5,"person_b":1,"type":"superior_subordinate","context":"何必良任区委书记时，陈绍曦任区长","overlap_org":"中共蕉城区委员会/蕉城区人民政府","overlap_period":"","direction":"other_to_person","strength":"strong"},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        org_id INTEGER,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER,
        person_b INTEGER,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        direction TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"],
                   p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, direction) VALUES (?,?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["direction"]))

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role: red=party secretary, blue=gov leader, orange=discipline, grey=other"""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"
    elif "区长" in post or "市长" in post or "县长" in post or "镇长" in post or "主任" in post:
        return "50,100,255"
    elif "纪委" in post:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post and "纪委" not in post or "区长" in post or "县长" in post

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "开发区" in t:
        return "200,255,200"
    elif "乡镇" in t or "街道" in t:
        return "255,255,200"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "事业" in t:
        return "220,220,220"
    else:
        return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>蕉城区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("end",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# =========================================================================
# BUILD PERSON JSONS
# =========================================================================
def build_person_jsons():
    json_dir = PERSONS_DIR
    today = "2026-07-17"

    # Person profiles
    profiles = {
        "陈绍曦": {
            "person_id": "jiaocheng_chen_shaoxi",
            "name": "陈绍曦",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1971-10",
            "birthplace": "福建福安",
            "native_place": "福建福安",
            "education": [{"period": "unknown", "institution": "未知", "major": "", "degree": "大学学历", "study_type": "full_time", "source_ids": ["S001"]}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "陈绍曦_1971-10", "name_birthplace": "陈绍曦_福建福安", "official_profile_url": "https://baike.baidu.com/item/%E9%99%88%E7%BB%8D%E6%9B%A6"},
            "current_post": "蕉城区委书记",
            "current_org": "中共蕉城区委员会",
            "administrative_rank": "副厅级",
            "as_of": "2026-01",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "福安市社口镇", "title": "党委副书记、镇长", "level": "正科级", "location": "福安市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "福安市阳头街道办事处", "title": "主任", "level": "正科级", "location": "福安市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "福安市阳头街道党工委", "title": "书记", "level": "正科级", "location": "福安市", "system": "party", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "东侨经济技术开发区管委会", "title": "副主任", "level": "副处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "进入副处级", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "霞浦县委统战部", "title": "县委常委、统战部部长", "level": "副处级", "location": "霞浦县", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "霞浦县人民政府", "title": "县委常委、政府副县长", "level": "副处级", "location": "霞浦县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "宁德市人民政府办公室", "title": "市政府副秘书长、市政府办党组成员", "level": "正处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "进入正处级", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "宁德市委军民融合办", "title": "常务副主任", "level": "正处级", "location": "蕉城区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "宁德市生态环境局", "title": "党组书记、局长", "level": "正处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "2025-12", "org": "蕉城区人民政府", "title": "区长", "level": "正处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "任区委副书记、区政府党组书记、区长", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2025-12", "end": "present", "org": "中共蕉城区委员会", "title": "区委书记", "level": "副厅级", "location": "蕉城区", "system": "party", "rank": "", "is_key_promotion": True, "notes": "由区长升任区委书记，进入副厅级", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2026-02", "end": "present", "org": "蕉城区人民武装部", "title": "党委第一书记", "level": "", "location": "蕉城区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "兼任", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "organizations": ["福安市社口镇", "福安市阳头街道", "东侨经济技术开发区", "霞浦县", "宁德市人民政府", "宁德市委军民融合办", "宁德市生态环境局", "蕉城区人民政府", "中共蕉城区委员会"],
            "relationships": [
                {"person": "何必良", "person_id": "jiaocheng_he_biliang", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "陈绍曦接替何必良任蕉城区委书记", "overlap_org": "中共蕉城区委员会", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "何必良", "person_id": "jiaocheng_he_biliang", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "何必良任区委书记时，陈绍曦任区长，党政正职搭档", "overlap_org": "蕉城区", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "王云盛", "person_id": "jiaocheng_wang_yunsheng", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "王云盛接替陈绍曦任蕉城区区长", "overlap_org": "蕉城区人民政府", "overlap_period": "2025-12", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "王云盛", "person_id": "jiaocheng_wang_yunsheng", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "陈绍曦作为区委书记，与区长王云盛党政正职搭档", "overlap_org": "蕉城区", "overlap_period": "2026-01至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["党政管理", "生态环保", "地方治理"],
                "secondary_specializations": ["统一战线"],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government", "united_front", "ecological_environment"],
                "geographic_pattern": ["福安", "霞浦", "宁德", "蕉城"],
                "promotion_velocity": {"summary": "从福安基层逐步晋升至蕉城区主要领导岗位", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "low_profile", "evidence": "公开资料以官方履历为主，无明显个性风格表述", "confidence": "plausible", "source_ids": ["S001"]}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from limited public records."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现纪律处分或负面报道", "date": "", "confidence": "plausible", "source_ids": ["S001"]}],
            "source_register": [
                {"id": "S001", "title": "陈绍曦 - 百度百科", "url": "https://baike.baidu.com/item/%E9%99%88%E7%BB%8D%E6%9B%A6", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
                {"id": "S002", "title": "蕉城区 - 百度百科", "url": "https://baike.baidu.com/item/%E8%95%89%E5%9F%8E%E5%8C%BA", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "Contains leadership table"},
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "各级职务具体任职起止时间不详"
            },
            "open_questions": [
                {"priority": "medium", "question": "陈绍曦各级职务的具体起止月份", "why_it_matters": "精确化履历时间线", "suggested_queries": ["陈绍曦 任职 时间", "陈绍曦 任免"], "last_attempted": AS_OF},
                {"priority": "low", "question": "陈绍曦的出生月份和具体日期", "why_it_matters": "完善身份信息", "suggested_queries": ["陈绍曦 出生"], "last_attempted": AS_OF}
            ]
        },
        "王云盛": {
            "person_id": "jiaocheng_wang_yunsheng",
            "name": "王云盛",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1974-07",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "unknown", "institution": "未知", "major": "", "degree": "大学学历，工学学士", "study_type": "full_time", "source_ids": ["S003"]}],
            "party_join": "中共党员",
            "work_start": "1996-12",
            "dedupe_keys": {"name_birth": "王云盛_1974-07", "name_birthplace": "王云盛_", "official_profile_url": "https://baike.baidu.com/item/%E7%8E%8B%E4%BA%91%E7%9B%9B"},
            "current_post": "蕉城区区长",
            "current_org": "蕉城区人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-01",
            "is_current_confirmed": True,
            "source_ids": ["S003", "S004"],
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "宁德市人民政府防汛抗旱指挥部办公室", "title": "主任", "level": "", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "unknown", "end": "unknown", "org": "宁德市人民政府办公室", "title": "副主任", "level": "副处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "unknown", "end": "unknown", "org": "中共古田县委", "title": "副书记", "level": "副处级", "location": "古田县", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2022-03", "end": "2026-01", "org": "宁德市交通运输局", "title": "党组书记、局长", "level": "正处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003", "S006"]},
                {"start": "2025-12-31", "end": "2026-01", "org": "蕉城区人民政府", "title": "副区长、代理区长", "level": "正处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "区人大常委会任命", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
                {"start": "2026-01-02", "end": "present", "org": "蕉城区人民政府", "title": "区长", "level": "正处级", "location": "蕉城区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "区十八届人大五次会议选举", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
                {"start": "2026-01", "end": "present", "org": "中共蕉城区委员会", "title": "区委副书记", "level": "正处级", "location": "蕉城区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
            ],
            "organizations": ["宁德市防汛办", "宁德市人民政府办公室", "古田县委", "宁德市交通运输局", "蕉城区人民政府"],
            "relationships": [
                {"person": "陈绍曦", "person_id": "jiaocheng_chen_shaoxi", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "王云盛接替陈绍曦任蕉城区区长", "overlap_org": "蕉城区人民政府", "overlap_period": "2025-12", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003", "S004", "S005"]},
                {"person": "陈绍曦", "person_id": "jiaocheng_chen_shaoxi", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "作为区长与区委书记陈绍曦党政正职搭档", "overlap_org": "蕉城区", "overlap_period": "2026-01至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["交通管理", "防汛应急", "地方治理"],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["宁德", "古田", "蕉城"],
                "promotion_velocity": {"summary": "2022-2026年间从市交通局长转任区长", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "low_profile", "evidence": "公开资料以官方履历为主", "confidence": "plausible", "source_ids": ["S003"]}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from limited public records."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现纪律处分或负面报道", "date": "", "confidence": "plausible", "source_ids": ["S003"]}],
            "source_register": [
                {"id": "S003", "title": "王云盛 - 百度百科", "url": "https://baike.baidu.com/item/%E7%8E%8B%E4%BA%91%E7%9B%9B", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
                {"id": "S004", "title": "蕉城区 - 百度百科", "url": "https://baike.baidu.com/item/%E8%95%89%E5%9F%8E%E5%8C%BA", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "Contains leadership table"},
                {"id": "S005", "title": "王云盛任蕉城区人民政府副区长、代理区长职务", "url": "", "publisher": "闽东日报", "published_at": "2025-12-31", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": ""},
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "出生地和早期履历不详"
            },
            "open_questions": [
                {"priority": "high", "question": "王云盛的出生地和籍贯", "why_it_matters": "完善身份信息", "suggested_queries": ["王云盛 籍贯"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "王云盛1996年工作后至任市防汛办主任之前的履历", "why_it_matters": "早期职业轨迹", "suggested_queries": ["王云盛 简历 早期"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "王云盛在古田县委副书记期间的具体分工", "why_it_matters": "了解其专业方向", "suggested_queries": ["王云盛 古田 副书记"], "last_attempted": AS_OF}
            ]
        }
    }

    filenames = {
        "陈绍曦": f"{today}-福建省-宁德市-区委书记-陈绍曦.json",
        "王云盛": f"{today}-福建省-宁德市-区长-王云盛.json",
    }

    for name, profile in profiles.items():
        fname = filenames[name]
        fpath = os.path.join(json_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump({"schema_version": "1.0", "generated_at": AS_OF, "investigation_scope": {
                "province": "福建省", "city": "宁德市", "region": "蕉城区", "job": profile["current_post"],
                "task_id": "fujian_蕉城区", "time_focus": "2025-2026"
            }, "identity": {k: profile[k] for k in ["person_id","name","aliases","gender","ethnicity","birth","birthplace","native_place","education","party_join","work_start","dedupe_keys"]},
            "current_status": {k: profile[k] for k in ["current_post","current_org","administrative_rank","as_of","is_current_confirmed","source_ids"]},
            "career_timeline": profile["career_timeline"],
            "organizations": profile["organizations"],
            "relationships": profile["relationships"],
            "governance_record": profile["governance_record"],
            "professional_profile": profile["professional_profile"],
            "work_style_and_personality": profile["work_style_and_personality"],
            "network_metrics": profile["network_metrics"],
            "risk_and_integrity_signals": profile["risk_and_integrity_signals"],
            "source_register": profile["source_register"],
            "confidence_summary": profile["confidence_summary"],
            "open_questions": profile["open_questions"]}, f, ensure_ascii=False, indent=2)
        print(f"Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    build_person_jsons()
    print("\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("Done.")
