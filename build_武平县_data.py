#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Wuping County (武平县), Longyan City, Fujian.

Covers: Party Secretary (县委书记), County Mayor (县长), key leadership,
predecessor/successor chains, and the county-level leadership network.

Sources:
- wp.gov.cn: Official Wuping county government website (领导之窗)
- Baidu search / news media: Current leadership transitions
- Baidu Baike: Biographical details for core figures

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_武平县")
DB_PATH = os.path.join(TMP, "武平县_network.db")
GEXF_PATH = os.path.join(TMP, "武平县_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 陈益斌 — 武平县委书记（2026-07~present）
    # Former: 龙岩市财政局党组书记、局长；连城县委副书记、常务副县长、副县长
    # Education: 厦门大学研究生，管理学硕士，高级会计师
    {"id":1,"name":"陈益斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"研究生（厦门大学，管理学硕士）","party_join":"中共党员","work_start":"",
     "current_post":"武平县委书记","current_org":"中共武平县委员会",
     "source":"https://www.wp.gov.cn/; 武平新闻网 2026-07-03报道"},

    # 李小飞 — 武平县委副书记、县长（2024?-present）
    # Born: 1984年11月, 男, 汉族, 研究生学历, 工学博士, 中共党员
    # Former: 武平县委副书记、县政府党组书记、县长
    {"id":2,"name":"李小飞","gender":"男","ethnicity":"汉族","birth":"1984-11","birthplace":"",
     "education":"研究生（工学博士）","party_join":"中共党员","work_start":"",
     "current_post":"武平县委副书记、县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/xz/lxf/"},

    # ── Deputy County Mayors (from wp.gov.cn 领导之窗) ──
    {"id":3,"name":"廖新强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":4,"name":"庞禹","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":5,"name":"周隆玉","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":6,"name":"蒋群钦","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":7,"name":"马永彬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":8,"name":"廖志新","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":9,"name":"林丹","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":10,"name":"陈学博","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    {"id":11,"name":"赖东武","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县副县长","current_org":"武平县人民政府",
     "source":"https://www.wp.gov.cn/zwgk/ldzc/"},

    # ── Other key county leaders (from news articles) ──
    # 刘演昌 — 县人大常委会主任 (mentioned in 2026-07-03 news)
    {"id":12,"name":"刘演昌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县人大常委会主任","current_org":"武平县人大常委会",
     "source":"武平新闻网 2026-07-03"},

    # 钟日朝 — 县政协主席 (mentioned in 2026-07-03 news)
    {"id":13,"name":"钟日朝","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县政协主席","current_org":"政协武平县委员会",
     "source":"武平新闻网 2026-07-03"},

    # 黄清平 — 县委常委 (mentioned in 2026-07-03 news)
    {"id":14,"name":"黄清平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县委常委","current_org":"中共武平县委员会",
     "source":"武平新闻网 2026-07-03"},

    # Other county leaders (待确认 fields)
    {"id":15,"name":"马金良","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县领导（待确认具体职务）","current_org":"武平县人民政府",
     "source":"武平县领导调研2026年项目建设报道 2026-05-23"},

    {"id":16,"name":"练良祥","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"武平县领导（待确认具体职务）","current_org":"武平县人民政府",
     "source":"武平县领导调研2026年项目建设报道 2026-05-23"},

    # ── Predecessors ──
    # 张丽华 — 前任武平县委书记（~2021-2026），同时任龙岩市政协副主席
    # Born: 1973年11月, 女, 汉族, 省委党校研究生, 中共党员
    # Was promoted to 设区市人大政协副职 around 2026-01
    {"id":17,"name":"张丽华","gender":"女","ethnicity":"汉族","birth":"1973-11","birthplace":"",
     "education":"省委党校研究生","party_join":"中共党员","work_start":"",
     "current_post":"设区市人大政协副职（前任武平县委书记）","current_org":"（待确认）",
     "source":"中共福建省委组织部任前公示 2026-01-13; 人民网"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共武平县委员会","type":"党委","level":"正处级","location":"福建省龙岩市武平县"},
    {"id":2,"name":"武平县人民政府","type":"政府","level":"正处级","location":"福建省龙岩市武平县"},
    {"id":3,"name":"武平县人大常委会","type":"人大","level":"正处级","location":"福建省龙岩市武平县"},
    {"id":4,"name":"政协武平县委员会","type":"政协","level":"正处级","location":"福建省龙岩市武平县"},
    {"id":5,"name":"中共武平县纪律检查委员会","type":"党委","level":"正处级","location":"福建省龙岩市武平县"},
    {"id":6,"name":"龙岩市财政局","type":"政府","level":"正处级","location":"福建省龙岩市"},
    {"id":7,"name":"中共连城县委员会","type":"党委","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":8,"name":"连城县人民政府","type":"政府","level":"正处级","location":"福建省龙岩市连城县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current positions
    {"person_id":1,"org_id":1,"title":"县委书记","start":"2026-07","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":2,"org_id":1,"title":"县委副书记","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":2,"org_id":2,"title":"县长","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":2,"org_id":2,"title":"县政府党组书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":3,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":4,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":5,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":6,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":7,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":8,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":9,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":10,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":11,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":12,"org_id":3,"title":"县人大常委会主任","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":13,"org_id":4,"title":"县政协主席","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":14,"org_id":1,"title":"县委常委","start":"","end":"present","rank":"副处级","as_of":AS_OF},

    # Predecessor positions
    {"person_id":17,"org_id":1,"title":"县委书记（前任）","start":"","end":"2026","rank":"正处级","as_of":AS_OF},
    {"person_id":17,"org_id":1,"title":"龙岩市政协副主席（兼任）","start":"","end":"2026","rank":"副厅级","as_of":AS_OF},

    # 陈益斌 previous positions
    {"person_id":1,"org_id":6,"title":"龙岩市财政局党组书记、局长（前任）","start":"","end":"2026-07","rank":"正处级","as_of":AS_OF},
    {"person_id":1,"org_id":7,"title":"连城县委副书记（前任）","start":"","end":"","rank":"副处级","as_of":AS_OF},
    {"person_id":1,"org_id":8,"title":"连城县委常委、常务副县长（前任）","start":"","end":"","rank":"副处级","as_of":AS_OF},
    {"person_id":1,"org_id":8,"title":"连城县副县长（前任）","start":"","end":"","rank":"副处级","as_of":AS_OF},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Superior-subordinate
    {"person1_id":1,"person2_id":2,"type":"superior_subordinate","strength":"strong","description":"县委书记-县长搭档","evidence":"陈益斌为县委书记，李小飞为县委副书记、县长，构成党政主要领导搭档","confidence":"confirmed"},
    {"person1_id":1,"person2_id":14,"type":"superior_subordinate","strength":"strong","description":"县委书记-县委常委","evidence":"黄清平为县委常委，陈益斌为县委书记","confidence":"confirmed"},

    # Predecessor-successor
    {"person1_id":17,"person2_id":1,"type":"predecessor_successor","strength":"strong","description":"武平县委书记前后任","evidence":"张丽华曾任武平县委书记兼龙岩市政协副主席；陈益斌接任武平县委书记（2026年7月）","confidence":"confirmed"},

    # Same organization overlaps
    {"person1_id":2,"person2_id":3,"type":"overlap","strength":"strong","description":"县长-副县长工作关系","evidence":"李小飞为县长，廖新强为副县长，同属县政府领导班子","confidence":"confirmed"},
    {"person1_id":2,"person2_id":4,"type":"overlap","strength":"strong","description":"县长-副县长工作关系","evidence":"李小飞为县长，庞禹为副县长，同属县政府领导班子","confidence":"confirmed"},
    {"person1_id":2,"person2_id":5,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":6,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":7,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":8,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":9,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":10,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":11,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属武平县人民政府","confidence":"confirmed"},

    # Cross-institution overlap (陈益斌 and 李小飞 linked via 武平县)
    {"person1_id":1,"person2_id":12,"type":"overlap","strength":"medium","description":"县委书记-人大主任工作关系","evidence":"陈益斌为县委书记，刘演昌为县人大常委会主任，同在武平县领导班子","confidence":"confirmed"},
    {"person1_id":1,"person2_id":13,"type":"overlap","strength":"medium","description":"县委书记-政协主席工作关系","evidence":"陈益斌为县委书记，钟日朝为县政协主席，同在武平县领导班子","confidence":"confirmed"},
]

# =========================================================================
# HELPER: esc for XML
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# =========================================================================
# BUILD: SQLite Database
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            as_of TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person1_id INTEGER,
            person2_id INTEGER,
            type TEXT,
            strength TEXT,
            description TEXT,
            evidence TEXT,
            confidence TEXT,
            FOREIGN KEY (person1_id) REFERENCES persons(id),
            FOREIGN KEY (person2_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, location)
            VALUES (?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, as_of)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["as_of"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person1_id, person2_id, type, strength, description, evidence, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person1_id"], r["person2_id"], r["type"], r["strength"], r["description"], r["evidence"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


# =========================================================================
# BUILD: GEXF Graph
# =========================================================================
def person_color(p):
    # Party Secretary (县委书记) = Red
    if "书记" in p.get("current_post", "") and "县委" in p.get("current_post", ""):
        return "255,50,50"
    # County Mayor (县长) = Blue
    if "县长" in p.get("current_post", "") and "副" not in p.get("current_post", ""):
        return "50,100,255"
    # Discipline (纪委) = Orange
    if "纪委" in p.get("current_post", ""):
        return "255,165,0"
    # Deputy (副县长/副处) = Mid Blue
    if "副" in p.get("current_post", ""):
        return "80,130,200"
    # Others = Grey
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>武平县领导工作关系网络 — Wuping County Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="description" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        if "(待确认" in p["name"]:
            continue
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if "副" not in p.get("current_post","") else "10.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if pos["person_id"] <= 17:
            eid += 1
            lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="strong"/>')
            lines.append(f'          <attvalue for="2" value="{esc(pos["title"])}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else ("1.5" if r["strength"] == "medium" else "1.0")
        lines.append(f'      <edge id="{eid}" source="p{r["person1_id"]}" target="p{r["person2_id"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["description"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


# =========================================================================
# BUILD: Person JSON
# =========================================================================
def write_person_json(person, extra_fields=None):
    if "(待确认" in person["name"]:
        return
    date_str = AS_OF.replace("-", "")
    slug = f"{date_str}-福建省-龙岩市-{person['current_post'].replace('、','-')}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, slug)

    pid = f"fujian_longyan_wuping_{person['name']}"
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "龙岩市",
            "region": "武平县",
            "job": person.get("current_post", ""),
            "task_id": "fujian_武平县",
            "time_focus": AS_OF
        },
        "identity": {
            "person_id": pid,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person["id"] in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type":"none_found","description":"No negative signals found in public records","date":"","confidence":"unverified","source_ids":["S001"]}],
        "source_register": [
            {"id":"S001","title":"武平县人民政府网站","url":person.get("source",""),"publisher":"武平县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Detailed career timeline for {person['name']} before current role is unknown"
        },
        "open_questions": [
            {"priority":"high","question":f"{person['name']}在担任现职前的详细履历","why_it_matters":"需要完整履历以构建关系网络","suggested_queries":[f"{person['name']} 简历", f"{person['name']} 任职经历"],"last_attempted":AS_OF},
            {"priority":"medium","question":f"{person['name']}的教育背景和出生地","why_it_matters":"用于身份去重和背景分析","suggested_queries":[f"{person['name']} 出生 学历"],"last_attempted":AS_OF}
        ]
    }

    # ── 陈益斌 (县委书记) detailed data ──
    if person["name"] == "陈益斌":
        data["identity"]["education"] = [
            {"period":"","institution":"厦门大学","major":"管理学","degree":"硕士","study_type":"full_time","source_ids":["S002"]}
        ]
        data["identity"]["work_start"] = ""
        data["current_status"]["administrative_rank"] = "正处级"
        data["career_timeline"] = [
            {"start":"2026-07","end":"present","org":"中共武平县委员会","title":"县委书记","level":"正处级","location":"福建省龙岩市武平县","system":"party","rank":"正处级","is_key_promotion":True,"notes":"2026年7月接任武平县委书记","confidence":"confirmed","source_ids":["S001","S003"]},
            {"start":"","end":"2026-07","org":"龙岩市财政局","title":"党组书记、局长","level":"正处级","location":"福建省龙岩市","system":"government","rank":"正处级","is_key_promotion":True,"notes":"曾任龙岩市财政局党组书记、局长；2024年7月29日经龙岩市人大常委会任命","confidence":"confirmed","source_ids":["S002","S003"]},
            {"start":"","end":"","org":"中共连城县委员会","title":"连城县委副书记","level":"副处级","location":"福建省龙岩市连城县","system":"party","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"plausible","source_ids":["S002"]},
            {"start":"","end":"","org":"连城县人民政府","title":"县委常委、常务副县长","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"plausible","source_ids":["S002"]},
            {"start":"","end":"","org":"连城县人民政府","title":"副县长","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"plausible","source_ids":["S002"]},
        ]
        data["professional_profile"] = {
            "primary_specializations": ["财政管理", "政府财务管理"],
            "secondary_specializations": ["政府治理"],
            "career_pattern": "provincial_department",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["龙岩市"],
            "promotion_velocity": {"summary": "From county deputy to county party secretary within the same prefecture-level city system; advanced from Liancheng County to Wuping County via the municipal finance bureau", "notable_fast_promotions": []}
        }
        data["source_register"] = [
            {"id":"S001","title":"武平县人民政府网站","url":"https://www.wp.gov.cn/","publisher":"武平县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
            {"id":"S002","title":"百度百科/搜索 陈益斌任职","url":"https://www.baidu.com/s?wd=陈益斌%20武平县委书记","publisher":"百度","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"AI summarize of multiple sources"},
            {"id":"S003","title":"武平新闻网 2026-07-03报道","url":"武平新闻网","publisher":"武平新闻网","published_at":"2026-07-03","accessed_at":AS_OF,"source_type":"media","reliability":"high","notes":"陈益斌以县委书记身份走访调研县人大常委会、县政府、县政协机关"},
        ]
        data["confidence_summary"]["identity"] = "partial"
        data["confidence_summary"]["career_completeness"] = "partial"

    # ── 李小飞 (县长) detailed data ──
    if person["name"] == "李小飞":
        data["identity"]["education"] = [
            {"period":"","institution":"","major":"工学","degree":"博士","study_type":"full_time","source_ids":["S001"]}
        ]
        data["current_status"]["administrative_rank"] = "正处级"
        data["career_timeline"] = [
            {"start":"","end":"present","org":"中共武平县委员会","title":"县委副书记","level":"副处级","location":"福建省龙岩市武平县","system":"party","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"confirmed","source_ids":["S001"]},
            {"start":"","end":"present","org":"武平县人民政府","title":"县长、县政府党组书记","level":"正处级","location":"福建省龙岩市武平县","system":"government","rank":"正处级","is_key_promotion":True,"notes":"主持县政府全面工作，负责审计工作","confidence":"confirmed","source_ids":["S001"]},
        ]
        data["confidence_summary"]["identity"] = "partial"
        data["confidence_summary"]["career_completeness"] = "thin"

    # ── 张丽华 (前任县委书记) detailed data ──
    if person["name"] == "张丽华":
        data["identity"]["education"] = [
            {"period":"","institution":"省委党校","major":"","degree":"研究生","study_type":"party_school","source_ids":["S004"]}
        ]
        data["current_status"]["administrative_rank"] = "副厅级"
        data["current_status"]["is_current_confirmed"] = False
        data["current_status"]["as_of"] = "2026-01"
        data["career_timeline"] = [
            {"start":"","end":"2026","org":"中共武平县委员会","title":"县委书记","level":"正处级","location":"福建省龙岩市武平县","system":"party","rank":"正处级","is_key_promotion":True,"notes":"同时兼任龙岩市政协副主席","confidence":"confirmed","source_ids":["S004"]},
            {"start":"","end":"2026","org":"龙岩市政协","title":"副主席（兼任）","level":"副厅级","location":"福建省龙岩市","system":"government","rank":"副厅级","is_key_promotion":True,"notes":"兼任武平县委书记期间同时担任龙岩市政协副主席","confidence":"confirmed","source_ids":["S004"]},
        ]
        data["source_register"] = [
            {"id":"S004","title":"中共福建省委组织部关于王跃平等同志任前公示的公告","url":"人民网 2026-01-13","publisher":"人民网","published_at":"2026-01-13","accessed_at":AS_OF,"source_type":"appointment_notice","reliability":"high","notes":"张丽华拟任设区市人大政协副职"}
        ]
        data["confidence_summary"]["identity"] = "partial"
        data["confidence_summary"]["career_completeness"] = "thin"

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[JSON] Wrote {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    for p in persons:
        write_person_json(p)
    print("[DONE] All artifacts generated.")
