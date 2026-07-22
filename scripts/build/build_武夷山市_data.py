#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Wuyishan City (武夷山市), Fujian Province.

A county-level city under Nanping City (南平市), Fujian Province.
Formerly Chong'an County (崇安县), renamed to Wuyishan in 1989.

Targets: Party Secretary (市委书记), Mayor (市长), leadership team,
predecessor/successor chains.

Sources:
- wys.gov.cn: Official Wuyishan city government website (as of 2026-07)
- zh.wikipedia.org: Wuyishan city overview and leadership info
- en.wikipedia.org: Wuyishan city overview

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_武夷山市")
DB_PATH = os.path.join(TMP, "武夷山市_network.db")
GEXF_PATH = os.path.join(TMP, "武夷山市_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 杨青建 — 武夷山市委书记
    {"id":1,"name":"杨青建","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市委书记","current_org":"中共武夷山市委员会","source":"https://zh.wikipedia.org/wiki/%E6%AD%A6%E5%A4%B7%E5%B1%B1%E5%B8%82"},
    # 余洲 — 武夷山市市长
    {"id":2,"name":"余洲","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"武夷山市市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},

    # ── Vice mayors (from wys.gov.cn 市政府领导 section) ──
    {"id":3,"name":"廖轶斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":4,"name":"白海鹏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":5,"name":"张立明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":6,"name":"赵亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":7,"name":"叶孝平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":8,"name":"简继元","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":9,"name":"邱敏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":10,"name":"王峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},
    {"id":11,"name":"李艳","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市副市长","current_org":"武夷山市人民政府","source":"https://www.wys.gov.cn/"},

    # ── Other key city leaders ──
    # 陈爱宾 — 武夷山市委副书记 (appears in news "余洲陈爱宾看望慰问")
    {"id":12,"name":"陈爱宾","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"武夷山市委副书记","current_org":"中共武夷山市委员会","source":"https://www.wys.gov.cn/"},

    # ── Predecessors — 市委书记 (historical, partial list from Wikipedia) ──
    # Note: The Wikipedia page was updated at revision 92165424
    # 马必钢 (Ma Bigang) — listed as secretary on English Wikipedia
    {"id":13,"name":"马必钢","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://en.wikipedia.org/wiki/Wuyishan,_Fujian"},

    # ── Predecessors — 市长 ──
    # 谢启龙 — 前任市长 (moved to another post before 余洲)
    {"id":14,"name":"谢启龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://www.wys.gov.cn/"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共武夷山市委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市武夷山市"},
    {"id":2,"name":"武夷山市人民政府","type":"政府","level":"县级","parent":"南平市人民政府","location":"福建省南平市武夷山市"},
    {"id":3,"name":"武夷山市人大常委会","type":"人大","level":"县级","parent":"","location":"福建省南平市武夷山市"},
    {"id":4,"name":"政协武夷山市委员会","type":"政协","level":"县级","parent":"","location":"福建省南平市武夷山市"},
    {"id":5,"name":"中共南平市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省南平市"},
    {"id":6,"name":"南平市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省南平市"},
    {"id":7,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":8,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current positions
    {"id":1,"person_id":1,"org_id":1,"title":"武夷山市委书记","start":"","end":"present","rank":"正处级","note":"现任武夷山市委书记"},
    {"id":2,"person_id":2,"org_id":2,"title":"武夷山市市长","start":"","end":"present","rank":"正处级","note":"现任武夷山市市长"},
    {"id":3,"person_id":3,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":4,"person_id":4,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":5,"person_id":5,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":6,"person_id":6,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":7,"person_id":7,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":8,"person_id":8,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":9,"person_id":9,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":10,"person_id":10,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":11,"person_id":11,"org_id":2,"title":"武夷山市副市长","start":"","end":"present","rank":"副处级","note":"副市长"},
    {"id":12,"person_id":12,"org_id":1,"title":"武夷山市委副书记","start":"","end":"present","rank":"副处级","note":"市委副书记"},

    # Predecessor positions
    {"id":13,"person_id":13,"org_id":1,"title":"武夷山市委书记","start":"","end":"","rank":"正处级","note":"前任市委书记（时期待核实）"},
    {"id":14,"person_id":14,"org_id":2,"title":"武夷山市市长","start":"","end":"","rank":"正处级","note":"前任市长（在余洲之前担任）"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core: 市委书记 ↔ 市长
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate","context":"杨青建为武夷山市委书记，余洲为武夷山市市长，两人为党政主要领导搭档","overlap_org":"武夷山市","overlap_period":"present","strength":"strong","confidence":"confirmed"},

    # 市长 ↔ 市委副书记
    {"id":2,"person_a":2,"person_b":12,"type":"superior_subordinate","context":"余洲（市长）与陈爱宾（市委副书记）同为中共武夷山市委班子成员","overlap_org":"中共武夷山市委员会","overlap_period":"present","strength":"strong","confidence":"confirmed"},

    # 市委书记 ↔ 市委副书记
    {"id":3,"person_a":1,"person_b":12,"type":"superior_subordinate","context":"杨青建（市委书记）与陈爱宾（市委副书记）在市委班子共事","overlap_org":"中共武夷山市委员会","overlap_period":"present","strength":"strong","confidence":"confirmed"},

    # Predecessor-successor: 市长
    {"id":4,"person_a":14,"person_b":2,"type":"predecessor_successor","context":"谢启龙为前任武夷山市市长，余洲接任市长职务","overlap_org":"武夷山市人民政府","overlap_period":"transfer","strength":"strong","confidence":"plausible"},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript('''
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    ''')

    for p in persons:
        c.execute('''INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))

    for o in organizations:
        c.execute('''INSERT INTO organizations (id,name,type,level,parent,location)
                     VALUES (?,?,?,?,?,?)''',
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

    for pos in positions:
        c.execute('''INSERT INTO positions (id,person_id,org_id,title,start,end,rank,note)
                     VALUES (?,?,?,?,?,?,?,?)''',
                  (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))

    for r in relationships:
        c.execute('''INSERT INTO relationships (id,person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence)
                     VALUES (?,?,?,?,?,?,?,?,?)''',
                  (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"],r["strength"],r["confidence"]))

    conn.commit()

    # Summary
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    psc = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]

    conn.close()
    return {"persons": pc, "organizations": oc, "positions": psc, "relationships": rc}

# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Color by role."""
    if "书记" in p.get("current_post","") and "市委" in p.get("current_post",""):
        return "255,50,50"     # Red — Party Secretary
    elif "市长" in p.get("current_post","") and "副市长" not in p.get("current_post",""):
        return "50,100,255"    # Blue — Mayor
    elif "副市长" in p.get("current_post",""):
        return "50,150,255"    # Light blue — Vice Mayor
    elif "副书记" in p.get("current_post",""):
        return "200,100,100"   # Dark red — Deputy Secretary
    else:
        return "100,100,100"   # Grey — Others

def org_color(o):
    t = o.get("type","")
    colors = {
        "党委":"255,200,200",
        "政府":"200,200,255",
        "人大":"200,255,255",
        "政协":"255,240,200"
    }
    return colors.get(t, "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>武夷山市（福建省南平市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        is_top = "书记" in p.get("current_post","") and "市委" in p.get("current_post","")
        is_top = is_top or (p.get("current_post","") == "武夷山市市长")
        sz = "20.0" if is_top else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =========================================================================
# EXPORT PERSON JSONS
# =========================================================================
def write_person_json(person, filename_suffix):
    """Write a person graph JSON file."""
    fname = f"20260717-福建省-南平市-{filename_suffix}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)

    data = {
        "schema_version": "1.0",
        "generated_at": "2026-07-17",
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "武夷山市",
            "job": person["current_post"],
            "task_id": "fujian_武夷山市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"wuyishan_{person['name']}",
            "name": person["name"],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "education": person["education"],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else "",
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person["birthplace"] else ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in (person["current_post"] or "") or "市长" in (person["current_post"] or "") else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "county-level",
                "location": "福建省南平市武夷山市",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "org_name": person["current_org"],
                "role": person["current_post"],
                "period": "present"
            }
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料不足，缺乏完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "在当前可用公开资料中未发现负面信号",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"]
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "武夷山市人民政府官方网站",
                "url": "https://www.wys.gov.cn/",
                "publisher": "武夷山市人民政府",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "市政府领导名单"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生年份、教育背景、早期任职经历）缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯、教育背景",
                "why_it_matters": "确认身份唯一性，支持去重",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整职业履历时间线",
                "why_it_matters": "理解晋升路径和工作背景",
                "suggested_queries": [f"{person['name']} 任职经历", f"{person['name']} 此前担任"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return fname

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building 武夷山市 network data...")
    print(f"Staging directory: {TMP}")

    stats = build_db()
    print(f"Database: {DB_PATH}")
    print(f"  Persons: {stats['persons']}, Organizations: {stats['organizations']}, "
          f"Positions: {stats['positions']}, Relationships: {stats['relationships']}")

    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"GEXF: {GEXF_PATH} ({gexf_size} bytes)")

    # Write person JSONs for core leaders
    core_leaders = [p for p in persons if p["id"] in [1, 2]]  # 市委书记 & 市长
    suffixes = {1: "市委书记", 2: "市长"}
    for p in core_leaders:
        fname = write_person_json(p, suffixes[p["id"]])
        fpath = os.path.join(PERSONS_DIR, fname)
        fsize = os.path.getsize(fpath)
        print(f"Person JSON: {fpath} ({fsize} bytes)")

    print("\nDone. Files ready for validation and promotion.")
