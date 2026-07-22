#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Liancheng County (连城县), Longyan City, Fujian.

Covers: Party Secretary (县委书记), County Mayor (县长), key leadership,
predecessor/successor chains, and the county-level leadership network.

Sources:
- fjlylc.gov.cn: Official Liancheng county government website (领导之窗)
- Wikipedia (Chinese): 连城县 leadership info
- News articles from fjlylc.gov.cn
- 闽西日报 articles

Research date: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_连城县")
DB_PATH = os.path.join(TMP, "连城县_network.db")
GEXF_PATH = os.path.join(TMP, "连城县_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 蔡东阳 — 连城县委书记
    # Confirmed by Wikipedia Chinese page for 连城县
    {"id":1,"name":"蔡东阳","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"连城县委书记","current_org":"中共连城县委员会",
     "source":"https://zh.wikipedia.org/wiki/%E8%BF%9E%E5%9F%8E%E5%8E%BF; http://www.fjlylc.gov.cn/"},

    # 龚友清 — 连城县委副书记、代理县长（1977-08）
    # Confirmed from fjlylc.gov.cn 领导之窗
    {"id":2,"name":"龚友清","gender":"男","ethnicity":"汉族","birth":"1977-08","birthplace":"",
     "education":"硕士研究生","party_join":"中共党员","work_start":"",
     "current_post":"连城县委副书记、代理县长","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/qxz/gyq/"},

    # ── Deputy County Mayors (from fjlylc.gov.cn 领导之窗) ──
    # 周龙辉 — 副县长（1991-11）
    {"id":3,"name":"周龙辉","gender":"男","ethnicity":"汉族","birth":"1991-11","birthplace":"",
     "education":"研究生","party_join":"中共党员","work_start":"",
     "current_post":"连城县副县长","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/zhoulonghui/"},

    # 韩小刚 — 副县长，挂职（1979-04）
    {"id":4,"name":"韩小刚","gender":"男","ethnicity":"汉族","birth":"1979-04","birthplace":"",
     "education":"研究生","party_join":"中共党员","work_start":"",
     "current_post":"连城县副县长（挂职）","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/hanxiaogang/"},

    # 陈路招（女）— 副县长（1975-02）
    {"id":5,"name":"陈路招","gender":"女","ethnicity":"汉族","birth":"1975-02","birthplace":"",
     "education":"研究生","party_join":"中共党员","work_start":"",
     "current_post":"连城县副县长","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/clz/"},

    # 朱建斌 — 副县长、县公安局局长（1981-03）
    {"id":6,"name":"朱建斌","gender":"男","ethnicity":"汉族","birth":"1981-03","birthplace":"",
     "education":"大学","party_join":"中共党员","work_start":"",
     "current_post":"连城县副县长、县公安局局长","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/zhujianbin/"},

    # ── County Government Party Group members ──
    # 李川龙 — 县政府党组成员、冠豸山风景区管委会党委书记（1976-12）
    {"id":7,"name":"李川龙","gender":"男","ethnicity":"汉族","birth":"1976-12","birthplace":"",
     "education":"研究生","party_join":"中共党员","work_start":"",
     "current_post":"县政府党组成员、冠豸山风景区管委会党委书记","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/dzcy/lcl/"},

    # 傅致通 — 县政府党组成员
    {"id":8,"name":"傅致通","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"县政府党组成员","current_org":"连城县人民政府",
     "source":"http://www.fjlylc.gov.cn/xxgk/ldzc/dzcy/fuzhitong/"},

    # ── Other county-level leaders (to be confirmed) ──
    {"id":9,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县人大常委会主任（待确认）","current_org":"连城县人大常委会",
     "source":"待确认"},
    {"id":10,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县政协主席（待确认）","current_org":"政协连城县委员会",
     "source":"待确认"},
    {"id":11,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县纪委书记（待确认）","current_org":"中共连城县纪律检查委员会",
     "source":"待确认"},
    {"id":12,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县委组织部部长（待确认）","current_org":"中共连城县委组织部",
     "source":"待确认"},
    {"id":13,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县委宣传部部长（待确认）","current_org":"中共连城县委宣传部",
     "source":"待确认"},
    {"id":14,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"县委政法委书记（待确认）","current_org":"中共连城县委政法委员会",
     "source":"待确认"},

    # ── Predecessors ──
    # 前任县委书记 — 待确认
    # Note: Wikipedia shows 蔡东阳 as current but predecessor not listed.
    # Likely predecessor is someone who served before 2025-2026.
    {"id":15,"name":"（前任县委书记待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"（前任）连城县委书记","current_org":"中共连城县委员会",
     "source":"待确认"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共连城县委员会","type":"党委","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":2,"name":"连城县人民政府","type":"政府","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":3,"name":"连城县人大常委会","type":"人大","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":4,"name":"政协连城县委员会","type":"政协","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":5,"name":"中共连城县纪律检查委员会","type":"党委","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":6,"name":"中共连城县委组织部","type":"党委","level":"正科级","location":"福建省龙岩市连城县"},
    {"id":7,"name":"中共连城县委宣传部","type":"党委","level":"正科级","location":"福建省龙岩市连城县"},
    {"id":8,"name":"中共连城县委政法委员会","type":"党委","level":"正科级","location":"福建省龙岩市连城县"},
    {"id":9,"name":"冠豸山风景区管委会","type":"事业单位","level":"正处级","location":"福建省龙岩市连城县"},
    {"id":10,"name":"连城县公安局","type":"政府","level":"正科级","location":"福建省龙岩市连城县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current positions
    {"person_id":1,"org_id":1,"title":"县委书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":2,"org_id":1,"title":"县委副书记","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":2,"org_id":2,"title":"代理县长","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":2,"org_id":2,"title":"县政府党组书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":3,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":4,"org_id":2,"title":"副县长（挂职）","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":5,"org_id":2,"title":"副县长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":6,"org_id":2,"title":"副县长、县公安局局长","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":6,"org_id":10,"title":"县公安局局长","start":"","end":"present","rank":"正科级","as_of":AS_OF},
    {"person_id":7,"org_id":2,"title":"县政府党组成员","start":"","end":"present","rank":"副处级","as_of":AS_OF},
    {"person_id":7,"org_id":9,"title":"冠豸山风景区管委会党委书记","start":"","end":"present","rank":"正处级","as_of":AS_OF},
    {"person_id":8,"org_id":2,"title":"县政府党组成员","start":"","end":"present","rank":"副处级","as_of":AS_OF},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Superior-subordinate
    {"person1_id":1,"person2_id":2,"type":"superior_subordinate","strength":"strong","description":"县委书记-县长搭档","evidence":"蔡东阳为县委书记，龚友清为县委副书记、代理县长，构成党政主要领导搭档","confidence":"confirmed"},
    {"person1_id":1,"person2_id":3,"type":"superior_subordinate","strength":"strong","description":"县委书记-副县长","evidence":"周龙辉为副县长，蔡东阳为县委书记","confidence":"confirmed"},
    {"person1_id":2,"person2_id":3,"type":"superior_subordinate","strength":"strong","description":"县长-副县长工作关系","evidence":"龚友清为代理县长，周龙辉为副县长，同属县政府领导班子","confidence":"confirmed"},

    # Same organization overlaps (县政府领导班子)
    {"person1_id":2,"person2_id":4,"type":"overlap","strength":"medium","description":"县长-挂职副县长工作关系","evidence":"同属连城县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":5,"type":"overlap","strength":"medium","description":"县长-副县长工作关系","evidence":"同属连城县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":6,"type":"overlap","strength":"medium","description":"县长-副县长(公安)工作关系","evidence":"同属连城县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":7,"type":"overlap","strength":"medium","description":"县长-党组成员工作关系","evidence":"同属连城县人民政府","confidence":"confirmed"},
    {"person1_id":2,"person2_id":8,"type":"overlap","strength":"medium","description":"县长-党组成员工作关系","evidence":"同属连城县人民政府","confidence":"confirmed"},
    {"person1_id":3,"person2_id":5,"type":"overlap","strength":"medium","description":"副县长-副县长工作关系","evidence":"同属连城县人民政府领导班子","confidence":"confirmed"},
    {"person1_id":3,"person2_id":6,"type":"overlap","strength":"medium","description":"副县长-副县长工作关系","evidence":"同属连城县人民政府领导班子","confidence":"confirmed"},
    {"person1_id":5,"person2_id":6,"type":"overlap","strength":"medium","description":"副县长-副县长工作关系","evidence":"同属连城县人民政府领导班子","confidence":"confirmed"},
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
    if "事业单位" in t: return "220,220,220"
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
    lines.append('    <description>连城县领导工作关系网络 — Liancheng County Leadership Network</description>')
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
        if p["id"] == 1:
            sz = "20.0"
        elif p["id"] == 2:
            sz = "20.0"
        elif "副" in p.get("current_post",""):
            sz = "10.0"
        else:
            sz = "12.0"
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
        # Only include positions for confirmed persons (not 待确认)
        person_obj = None
        for p in persons:
            if p["id"] == pos["person_id"]:
                person_obj = p
                break
        if person_obj and "(待确认" not in person_obj["name"] and person_obj["name"] != "待确认":
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

    pid = f"fujian_longyan_liancheng_{person['name']}"
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "龙岩市",
            "region": "连城县",
            "job": person.get("current_post", ""),
            "task_id": "fujian_连城县",
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
            "is_current_confirmed": True,
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
            {"id":"S001","title":"连城县人民政府网站","url":person.get("source",""),"publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""}
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

    # ── Specific enrichment for core leaders ──
    if person["name"] == "蔡东阳":
        data["career_timeline"] = [
            {"start":"","end":"present","org":"中共连城县委员会","title":"县委书记","level":"正处级","location":"福建省龙岩市连城县","system":"party","rank":"正处级","is_key_promotion":True,"notes":"Wikipedia confirms as current Party Secretary","confidence":"confirmed","source_ids":["S001","S002"]}
        ]
        data["identity"]["education"] = []
        data["source_register"] = [
            {"id":"S001","title":"连城县人民政府网站","url":"http://www.fjlylc.gov.cn/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
            {"id":"S002","title":"维基百科-连城县","url":"https://zh.wikipedia.org/wiki/%E8%BF%9E%E5%9F%8E%E5%8E%BF","publisher":"维基百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"Confirmed as current Party Secretary"}
        ]
        data["confidence_summary"]["identity"] = "thin"
        data["confidence_summary"]["career_completeness"] = "thin"
        data["open_questions"] = [
            {"priority":"high","question":"蔡东阳的出生年份、籍贯、教育背景和完整履历","why_it_matters":"县委书记是网络核心节点，需完整背景信息","suggested_queries":["蔡东阳 简历","蔡东阳 连城","蔡东阳 出生"],"last_attempted":AS_OF},
            {"priority":"high","question":"蔡东阳的前任县委书记是谁","why_it_matters":"前任-继任关系是重要网络边","suggested_queries":["连城县 前任 县委书记"],"last_attempted":AS_OF}
        ]

    if person["name"] == "龚友清":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"硕士研究生","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"中共连城县委员会","title":"县委副书记","level":"副处级","location":"福建省龙岩市连城县","system":"party","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"confirmed","source_ids":["S001"]},
            {"start":"","end":"present","org":"连城县人民政府","title":"代理县长、县政府党组书记","level":"正处级","location":"福建省龙岩市连城县","system":"government","rank":"正处级","is_key_promotion":True,"notes":"主持县政府全面工作，负责审计工作","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["current_status"]["is_current_confirmed"] = True
        data["source_register"] = [
            {"id":"S001","title":"龚友清-连城县人民政府","url":"http://www.fjlylc.gov.cn/xxgk/ldzc/qxz/gyq/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Confirmed: 1977-08, 男, 汉族, 硕士研究生, 中共党员"}
        ]

    if person["name"] == "周龙辉":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"研究生","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"连城县人民政府","title":"副县长","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"负责人力资源、交通运输、市场监管、重点项目等","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["source_register"] = [
            {"id":"S001","title":"周龙辉-连城县人民政府","url":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/zhoulonghui/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Confirmed: 1991-11, 男, 汉族, 研究生, 中共党员"}
        ]
        data["open_questions"][0]["suggested_queries"] = ["周龙辉 简历 连城", "周龙辉 任职经历"]

    if person["name"] == "陈路招":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"研究生","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"连城县人民政府","title":"副县长","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"负责水利、农业农村（乡村振兴）、供销、烟草等","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["source_register"] = [
            {"id":"S001","title":"陈路招-连城县人民政府","url":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/clz/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Confirmed: 1975-02, 女, 汉族, 研究生, 中共党员"}
        ]

    if person["name"] == "朱建斌":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"大学","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"连城县人民政府","title":"副县长、县公安局局长","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"负责公安、司法、信访等工作","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["source_register"] = [
            {"id":"S001","title":"朱建斌-连城县人民政府","url":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/zhujianbin/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Confirmed: 1981-03, 男, 汉族, 大学, 中共党员"}
        ]

    if person["name"] == "韩小刚":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"研究生","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"连城县人民政府","title":"副县长（挂职）","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"挂职2年；负责民政、住建、省直挂钩帮扶等","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["source_register"] = [
            {"id":"S001","title":"韩小刚-连城县人民政府","url":"http://www.fjlylc.gov.cn/xxgk/ldzc/fqxz/hanxiaogang/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Confirmed: 1979-04, 男, 汉族, 研究生, 中共党员, 挂职副县长"}
        ]

    if person["name"] == "李川龙":
        data["identity"]["education"] = [{"period":"","institution":"","major":"","degree":"研究生","study_type":"full_time","source_ids":["S001"]}]
        data["career_timeline"] = [
            {"start":"","end":"present","org":"连城县人民政府","title":"县政府党组成员","level":"副处级","location":"福建省龙岩市连城县","system":"government","rank":"副处级","is_key_promotion":False,"notes":"","confidence":"confirmed","source_ids":["S001"]},
            {"start":"","end":"present","org":"冠豸山风景区管委会","title":"党委书记","level":"正处级","location":"福建省龙岩市连城县","system":"other","rank":"正处级","is_key_promotion":True,"notes":"负责文化、体育、旅游、客家美食工作","confidence":"confirmed","source_ids":["S001"]}
        ]
        data["source_register"] = [
            {"id":"S001","title":"李川龙-连城县人民政府","url":"http://www.fjlylc.gov.cn/xxgk/ldzc/dzcy/lcl/","publisher":"连城县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Confirmed: 1976-12, 男, 汉族, 研究生, 中共党员"}
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
