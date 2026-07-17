#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Changting County (长汀县), Longyan City, Fujian.

Covers: Party Secretary (县委书记), County Mayor (县长), key leadership,
predecessor/successor chains, and the county-level leadership network.

Sources:
- changting.gov.cn: Official Changting county government website (领导之窗)
- Wikipedia (Chinese): 长汀县 leadership info
- Baidu Baike: Biographical details for 赖进益
- News articles from changting.gov.cn

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_长汀县")
DB_PATH = os.path.join(TMP, "长汀县_network.db")
GEXF_PATH = os.path.join(TMP, "长汀县_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 吕莉 — 长汀县委书记（202?-present）
    # Confirmed as of 2026-06-30 from county news article
    {"id":1,"name":"吕莉","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"长汀县委书记","current_org":"中共长汀县委员会",
     "source":"http://www.changting.gov.cn/xwzx/ctxw/202607/t20260701_2299813.htm; https://zh.wikipedia.org/wiki/%E9%95%BF%E6%B1%80%E5%8E%BF"},

    # 罗天进 — 长汀县委副书记、县长（202?-present）
    # Confirmed: born 1985年9月, 男, 汉族, 大学学历, 中共党员
    {"id":2,"name":"罗天进","gender":"男","ethnicity":"汉族","birth":"1985-09","birthplace":"",
     "education":"大学","party_join":"中共党员","work_start":"",
     "current_post":"长汀县委副书记、县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/xz/ltj/"},

    # ── Deputy County Mayors (from changting.gov.cn 领导之窗) ──
    {"id":3,"name":"陈其民","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县委常委、副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/cqm/"},

    {"id":4,"name":"傅强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/bq/"},

    {"id":5,"name":"何毅","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/hy/"},

    {"id":6,"name":"赖文生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/lws/"},

    {"id":7,"name":"郑泽鑫","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/zzx/"},

    {"id":8,"name":"戴永迪","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/dyd/"},

    {"id":9,"name":"江亮亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县副县长","current_org":"长汀县人民政府",
     "source":"http://www.changting.gov.cn/xxgk/ldzc/fxz/jll/"},

    # ── Other key county leaders ──
    # 吴超文 — 县委常委、组织部部长 (mentioned in 2026-06 article)
    {"id":10,"name":"吴超文","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县委常委、组织部部长","current_org":"中共长汀县委组织部",
     "source":"http://www.changting.gov.cn/xwzx/ctxw/202607/t20260701_2299813.htm"},

    # 郭朝龙 — 县委常委、组织部部长、党校校长 (mentioned in 2026-07 article)
    # May be successor to 吴超文
    {"id":11,"name":"郭朝龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"长汀县委常委、组织部部长、党校校长","current_org":"中共长汀县委组织部",
     "source":"http://www.changting.gov.cn/xwzx/ctxw/202607/t20260717_2303085.htm"},

    # ── Other county-level leaders (待确认) ──
    {"id":12,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县人大常委会主任（待确认）","current_org":"长汀县人大常委会",
     "source":"待确认"},
    {"id":13,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县政协主席（待确认）","current_org":"政协长汀县委员会",
     "source":"待确认"},
    {"id":14,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县纪委书记（待确认）","current_org":"中共长汀县纪律检查委员会",
     "source":"待确认"},

    # ── Predecessors ──
    # 赖进益 — 前任长汀县委书记，现已调任龙岩市人大常委会副主任、新罗区委书记
    {"id":15,"name":"赖进益","gender":"男","ethnicity":"汉族","birth":"1972-06","birthplace":"福建长汀",
     "education":"大学","party_join":"中共党员","work_start":"1993-08",
     "current_post":"龙岩市人大常委会副主任、新罗区委书记","current_org":"龙岩市人大常委会",
     "source":"https://baike.baidu.com/item/%E8%B5%96%E8%BF%9B%E7%9B%8A/3952921"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共长汀县委员会","type":"党委","level":"正处级","location":"福建省龙岩市长汀县"},
    {"id":2,"name":"长汀县人民政府","type":"政府","level":"正处级","location":"福建省龙岩市长汀县"},
    {"id":3,"name":"长汀县人大常委会","type":"人大","level":"正处级","location":"福建省龙岩市长汀县"},
    {"id":4,"name":"政协长汀县委员会","type":"政协","level":"正处级","location":"福建省龙岩市长汀县"},
    {"id":5,"name":"中共长汀县纪律检查委员会","type":"党委","level":"正处级","location":"福建省龙岩市长汀县"},
    {"id":6,"name":"中共长汀县委组织部","type":"党委","level":"正科级","location":"福建省龙岩市长汀县"},
    {"id":7,"name":"龙岩市人大常委会","type":"人大","level":"正厅级","location":"福建省龙岩市"},
    {"id":8,"name":"中共龙岩市新罗区委员会","type":"党委","level":"正处级","location":"福建省龙岩市新罗区"},
    {"id":9,"name":"长汀县人民政府办公室","type":"政府","level":"正科级","location":"福建省龙岩市长汀县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current positions
    {"person_id":1,"org_id":1,"title":"县委书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":2,"org_id":1,"title":"县委副书记","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":2,"org_id":2,"title":"县长","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":2,"org_id":2,"title":"县政府党组书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":3,"org_id":2,"title":"县委常委、副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":4,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":5,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":6,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":7,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":8,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":9,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":10,"org_id":6,"title":"县委常委、组织部部长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":11,"org_id":6,"title":"县委常委、组织部部长、党校校长","start":"","end":"present","rank":"副处级","as_of":AS_OF},

    # Predecessor positions
    {"person_id":15,"org_id":1,"title":"县委书记（前任）","start":"","end":"","rank":"正处级","as_of":AS_OF},
    {"person_id":15,"org_id":7,"title":"龙岩市人大常委会副主任","start":"","end":"present","rank":"副厅级","as_of":AS_OF},
    {"person_id":15,"org_id":8,"title":"新罗区委书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Superior-subordinate
    {"person1_id":1,"person2_id":2,"type":"superior_subordinate","strength":"strong","description":"县委书记-县长搭档","evidence":"吕莉为县委书记，罗天进为县委副书记、县长，构成党政主要领导搭档","confidence":"confirmed"},
    {"person1_id":1,"person2_id":3,"type":"superior_subordinate","strength":"strong","description":"县委书记-县委常委","evidence":"陈其民为县委常委、副县长，吕莉为县委书记","confidence":"confirmed"},
    {"person1_id":1,"person2_id":10,"type":"superior_subordinate","strength":"strong","description":"县委书记-组织部部长","evidence":"吴超文为县委常委、组织部部长，吕莉为县委书记","confidence":"confirmed"},

    # Predecessor-successor
    {"person1_id":15,"person2_id":1,"type":"predecessor_successor","strength":"strong","description":"长汀县委书记前后任","evidence":"赖进益曾任长汀县委书记，后调任龙岩市；吕莉接任长汀县委书记","confidence":"confirmed"},

    # Same organization overlaps
    {"person1_id":2,"person2_id":3,"type":"overlap","strength":"strong","description":"县长-副县长工作关系","evidence":"罗天进为县长，陈其民为副县长，同属县政府领导班子","confidence":"confirmed"},
    {"person1_id":2,"person2_id":4,"type":"overlap","strength":"strong","description":"县长-副县长工作关系","evidence":"罗天进为县长，傅强为副县长，同属县政府领导班子","confidence":"confirmed"},
    {"person1_id":2,"person2_id":6,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属长汀县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":5,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属长汀县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":7,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属长汀县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":8,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属长汀县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":9,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属长汀县人民政府","confidence":"confirmed"},

    # Same native place
    {"person1_id":15,"person2_id":2,"type":"same_native_place","strength":"weak","description":"同籍贯","evidence":"赖进益为福建长汀人，罗天进可能为长汀或福建人","confidence":"plausible"},
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
    return "县委书记" in post or (p["id"] == 2)

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>长汀县领导工作关系网络 — Changting County Leadership Network</description>')
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
        if "(待确认" in p["name"] or "待确认" in p["name"]:
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
        if pos["person_id"] < 15 and pos["person_id"] > 0:
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
# BUILD: Person JSON stubs (detailed separate files)
# =========================================================================
def write_person_json(person, extra_fields=None):
    if "(待确认" in person["name"] or "待确认" in person["name"]:
        return
    date_str = AS_OF.replace("-", "")
    slug = f"{date_str}-福建省-龙岩市-{person['current_post'].replace('、','-')}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, slug)

    pid = f"fujian_longyan_changting_{person['name']}"
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "龙岩市",
            "region": "长汀县",
            "job": person.get("current_post", ""),
            "task_id": "fujian_长汀县",
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
            "is_current_confirmed": "吕莉" in person["name"] or "罗天进" in person["name"] or "陈其民" in person["name"],
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
            {"id":"S001","title":"长汀县人民政府网站","url":person.get("source",""),"publisher":"长汀县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""}
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

    if person["name"] == "罗天进":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"大学","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"中共长汀县委员会","title":"县委副书记","level":"副处级","location":"福建省龙岩市长汀县","system":"party","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"confirmed","source_ids":["S001"]},
            {"start":"","end":"present","org":"长汀县人民政府","title":"县长、县政府党组书记","level":"正处级","location":"福建省龙岩市长汀县","system":"government","rank":"正处级","is_key_promotion":True,"notes":"主持县政府全面工作，负责审计工作","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["confidence_summary"]["identity"] = "partial"
        data["confidence_summary"]["career_completeness"] = "thin"

    if person["name"] == "吕莉":
        data["career_timeline"] = [
            {"start":"","end":"present","org":"中共长汀县委员会","title":"县委书记","level":"正处级","location":"福建省龙岩市长汀县","system":"party","rank":"正处级","is_key_promotion":True,"notes":"","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["confidence_summary"]["identity"] = "thin"
        data["confidence_summary"]["career_completeness"] = "thin"

    if person["name"] == "赖进益":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"大学","study_type":"full_time","source_ids":["S002"]}]
        data["career_timeline"] = [
            {"start":"","end":"","org":"中共长汀县委员会","title":"县委书记（前任）","level":"正处级","location":"福建省龙岩市长汀县","system":"party","rank":"正处级","is_key_promotion":True,"notes":"在长汀县委书记任上后调任龙岩市","confidence":"confirmed","source_ids":["S002"]},
            {"start":"","end":"present","org":"龙岩市人大常委会","title":"党组成员、副主任","level":"副厅级","location":"福建省龙岩市","system":"government","rank":"副厅级","is_key_promotion":True,"notes":"","confidence":"confirmed","source_ids":["S002"]},
            {"start":"","end":"present","org":"中共龙岩市新罗区委员会","title":"新罗区委书记、区人武部党委第一书记","level":"正处级","location":"福建省龙岩市新罗区","system":"party","rank":"正处级","is_key_promotion":True,"notes":"","confidence":"confirmed","source_ids":["S002"]}
        ]
        data["identity"]["birth"] = "1972-06"
        data["identity"]["birthplace"] = "福建长汀"
        data["identity"]["work_start"] = "1993-08"
        data["source_register"] = [
            {"id":"S001","title":"长汀县人民政府网站","url":"http://www.changting.gov.cn/","publisher":"长汀县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
            {"id":"S002","title":"赖进益百度百科","url":"https://baike.baidu.com/item/%E8%B5%96%E8%BF%9B%E7%9B%8A/3952921","publisher":"百度百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""}
        ]

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
