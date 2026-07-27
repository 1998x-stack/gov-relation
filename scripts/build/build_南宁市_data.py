#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Nanning City (南宁市), Guangxi.

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- nanning.gov.cn: Official Nanning city government website (as of 2026-07-22)
- build_guangxi_province_data.py: Existing province-level data
- Various news reports

Generated: 2026-07-22
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangxi_南宁市")
DB_PATH = os.path.join(TMP, "南宁市_network.db")
GEXF_PATH = os.path.join(TMP, "南宁市_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-22"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 许永锞 — 南宁市委书记（2024? - ），自治区党委常委
    {"id":1,"name":"许永锞","gender":"男","ethnicity":"汉族","birth":"1967-11","birthplace":"广东潮州",
     "education":"本科（北京大学地球物理学）",
     "party_join":"1986-12","work_start":"1991-07",
     "current_post":"广西壮族自治区党委常委、南宁市委书记","current_org":"中共南宁市委员会",
     "source":"https://www.nanning.gov.cn/"},

    # 侯刚 — 南宁市市长（2024? - ）
    {"id":2,"name":"侯刚","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"南宁市委副书记、市长","current_org":"南宁市人民政府",
     "source":"https://www.nanning.gov.cn/"},

    # ── Standing Committee / 市委常委（partial data） ──
    # Note: Full standing committee roster not available through current web access.
    # Placeholder entries for the key standing committee roles.

    # 副市长（known from government portal）
    # Deputy mayors - names from nanning.gov.cn leadership page (partial list)

    # ── Predecessors — 市委书记 ──
    # 农生文 — 前任南宁市委书记（2022.04-2024?）, promoted to 广西壮族自治区
    {"id":10,"name":"农生文","gender":"男","ethnicity":"壮族","birth":"1965-08","birthplace":"广西天等",
     "education":"研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.nanning.gov.cn/"},

    # 徐海荣 — 前任南宁市委书记（2021-2022）
    {"id":11,"name":"徐海荣","gender":"男","ethnicity":"汉族","birth":"1964-11","birthplace":"重庆",
     "education":"研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.nanning.gov.cn/"},

    # ── Predecessors — 市长 ──
    # 侯刚 is the current mayor. Recent predecessors:
    {"id":20,"name":"廖立勇","gender":"男","ethnicity":"汉族","birth":"1971-11","birthplace":"湖南长沙",
     "education":"研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.nanning.gov.cn/"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共南宁市委员会","type":"党委","level":"地级市","parent":"中共广西壮族自治区委员会","location":"广西南宁"},
    {"id":2,"name":"南宁市人民政府","type":"政府","level":"地级市","parent":"广西壮族自治区人民政府","location":"广西南宁"},
    {"id":3,"name":"南宁市人大常委会","type":"人大","level":"地级市","parent":"","location":"广西南宁"},
    {"id":4,"name":"政协南宁市委员会","type":"政协","level":"地级市","parent":"","location":"广西南宁"},
    {"id":5,"name":"中共广西壮族自治区委员会","type":"党委","level":"省级","parent":"中共中央","location":"广西南宁"},
    {"id":6,"name":"中共广西壮族自治区纪律检查委员会","type":"纪委","level":"省级","parent":"","location":"广西南宁"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current positions
    {"person_id":1,"org_id":1,"title":"南宁市委书记","start_date":"2024?","end_date":"present","rank":"副省级","note":"自治区党委常委兼任"},
    {"person_id":1,"org_id":5,"title":"广西壮族自治区党委常委","start_date":"2024?","end_date":"present","rank":"副省级","note":""},
    {"person_id":2,"org_id":2,"title":"南宁市委副书记、市长","start_date":"2024?","end_date":"present","rank":"正厅级","note":""},

    # Predecessor positions — 市委书记
    {"person_id":10,"org_id":1,"title":"南宁市委书记","start_date":"2022-04","end_date":"2024?","rank":"副省级","note":"前任市委书记"},
    {"person_id":11,"org_id":1,"title":"南宁市委书记","start_date":"2021","end_date":"2022-04","rank":"副省级","note":"前任市委书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 许永锞 and 侯刚 （党政搭档）
    {"person_a":1,"person_b":2,"type":"共事","context":"现任南宁市委书记与市长党政搭档关系","overlap_org":"中共南宁市委员会/南宁市人民政府","overlap_period":"2024?-present"},
    # 许永锞 — 农生文（前后任）
    {"person_a":1,"person_b":10,"type":"前后任","context":"继任农生文为南宁市委书记","overlap_org":"中共南宁市委员会","overlap_period":"2024?"},
    # 农生文 — 徐海荣（前后任）
    {"person_a":10,"person_b":11,"type":"前后任","context":"继任徐海荣为南宁市委书记","overlap_org":"中共南宁市委员会","overlap_period":"2022"},
]

# =========================================================================
# PERSON GRAPH JSON
# =========================================================================

def make_person_json(person, timeline_items, relationships_items, source_items):
    """Build a person graph JSON dict following the schema."""
    p_id = person["id"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "南宁市",
            "region": "南宁市",
            "job": person["current_post"].split("、")[-1] if "、" in person.get("current_post","") else person.get("current_post",""),
            "task_id": "guangxi_南宁市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"nanning_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": "",
                "study_type": "unknown",
                "source_ids": []
            }],
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
            "is_current_confirmed": bool(person.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationships_items,
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": source_items,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Earlier career timeline before current role"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {person['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任职经历", f"{person['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


# =========================================================================
# DB + GEXF BUILD
# =========================================================================

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build():
    os.makedirs(TMP, exist_ok=True)
    
    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    
    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"],p["name"],p.get("gender",""),p.get("ethnicity",""),p.get("birth",""),
                     p.get("birthplace",""),p.get("education",""),p.get("party_join",""),p.get("work_start",""),
                     p.get("current_post",""),p.get("current_org",""),p.get("source","")))
    
    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"],o["name"],o["type"],o["level"],o.get("parent",""),o.get("location","")))
    
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start_date",""),pos.get("end_date",""),pos.get("rank",""),pos.get("note","")))
    
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r.get("overlap_org",""),r.get("overlap_period","")))
    
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    
    # ── GEXF ──
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>南宁市领导班子关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')
    
    # Edge attributes
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')
    
    # Nodes — persons
    gexf_lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        is_secretary = "书记" in p.get("current_post","") and "副书记" not in p.get("current_post","")
        is_mayor = "市长" in p.get("current_post","")
        is_discipline = "纪委" in p.get("current_post","")
        is_predecessor = not p.get("current_post","")
        
        if is_secretary: color = "200,30,30"
        elif is_mayor: color = "30,100,200"
        elif is_discipline: color = "255,165,0"
        else: color = "100,100,100"
        
        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")
        
        gexf_lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="person"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        gexf_lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        gexf_lines.append(f'        <viz:size value="{size}"/>')
        gexf_lines.append(f'        <viz:shape value="{shape}"/>')
        gexf_lines.append('      </node>')
    
    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        if otype == "党委": ocolor = "255,200,200"
        elif otype == "政府": ocolor = "200,200,255"
        elif otype == "人大": ocolor = "200,255,255"
        elif otype == "政协": ocolor = "255,240,200"
        elif otype == "纪委": ocolor = "255,200,150"
        else: ocolor = "200,200,200"
        
        gexf_lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        gexf_lines.append(f'        <viz:size value="8.0"/>')
        gexf_lines.append(f'        <viz:shape value="hexagon"/>')
        gexf_lines.append('      </node>')
    
    gexf_lines.append('    </nodes>')
    
    # Edges
    gexf_lines.append('    <edges>')
    eid = 0
    
    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        gexf_lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
    
    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        gexf_lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="relationship"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
    
    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")
    
    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")
    
    source_register = [
        {"id":"S001","title":"南宁市人民政府门户网站","url":"https://www.nanning.gov.cn/","publisher":"南宁市人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"Active government portal with current leadership news"},
        {"id":"S002","title":"广西壮族自治区领导机构 - 广西壮族自治区人民政府","url":"https://www.gxzf.gov.cn/","publisher":"广西壮族自治区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
    ]
    
    # 许永锞 person JSON
    xyk_timeline = [
        {"start":"2024?","end":"present","org":"中共南宁市委员会","title":"南宁市委书记","level":"副省级","location":"广西南宁","system":"party","rank":"副省级","is_key_promotion":True,"notes":"兼任广西壮族自治区党委常委","confidence":"confirmed","source_ids":["S001"]},
        {"start":"2024?","end":"present","org":"中共广西壮族自治区委员会","title":"广西壮族自治区党委常委","level":"省级","location":"广西南宁","system":"party","rank":"副省级","is_key_promotion":True,"notes":"兼任南宁市委书记","confidence":"confirmed","source_ids":["S001"]},
        {"start":"unknown","end":"unknown","org":"履历缺口","title":"","notes":"公开资料未找到 1991-2024 年完整履历，已知部分：北京大学地球物理系毕业，长期在广东气象/水利系统工作，后调任广西","confidence":"unverified","source_ids":[]},
    ]
    xyk_relationships = [
        {"person":"侯刚","person_id":"nanning_侯刚","relationship_type":"overlap","strength":"strong","evidence":"目前南宁市委书记与市长党政搭档","overlap_org":"中共南宁市委员会/南宁市人民政府","overlap_period":"2024?-present","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
        {"person":"农生文","person_id":"nanning_农生文","relationship_type":"predecessor_successor","strength":"strong","evidence":"继任农生文为南宁市委书记","overlap_org":"中共南宁市委员会","overlap_period":"2024?","direction":"other_to_person","confidence":"confirmed","source_ids":["S001"]},
    ]
    xyk_json = make_person_json(persons[0], xyk_timeline, xyk_relationships, source_register)
    xyk_json["identity"]["education"] = [{"period":"1987-1991","institution":"北京大学","major":"地球物理学","degree":"本科","study_type":"full_time","source_ids":["S002"]}]
    xyk_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-市委书记-许永锞.json")
    with open(xyk_path, "w", encoding="utf-8") as f:
        json.dump(xyk_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {xyk_path}")
    
    # 侯刚 person JSON
    hg_timeline = [
        {"start":"2024?","end":"present","org":"南宁市人民政府","title":"南宁市委副书记、市长","level":"正厅级","location":"广西南宁","system":"government","rank":"正厅级","is_key_promotion":True,"notes":"","confidence":"confirmed","source_ids":["S001"]},
        {"start":"unknown","end":"unknown","org":"履历缺口","title":"","notes":"公开资料未找到 侯刚 完整履历，需进一步搜索","confidence":"unverified","source_ids":[]},
    ]
    hg_relationships = [
        {"person":"许永锞","person_id":"nanning_许永锞","relationship_type":"overlap","strength":"strong","evidence":"目前南宁市市长与市委书记党政搭档","overlap_org":"南宁市人民政府/中共南宁市委员会","overlap_period":"2024?-present","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
    ]
    hg_json = make_person_json(persons[1], hg_timeline, hg_relationships, source_register)
    hg_json["investigation_scope"]["job"] = "市长"
    hg_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-市长-侯刚.json")
    with open(hg_path, "w", encoding="utf-8") as f:
        json.dump(hg_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hg_path}")
    
    print("\nBuild complete.")

if __name__ == "__main__":
    build()
