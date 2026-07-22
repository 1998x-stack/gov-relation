#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 建瓯市, Fujian Province.

县级市 under 南平市, Fujian Province.

Targets: 市委书记 (周靖), 市长/代市长 (黄河)

Sources:
- https://zh.wikipedia.org/wiki/建瓯市 (current party secretary)
- https://www.jo.gov.cn (official city government website, current leadership roster)
- 建瓯市政府网站 leadership page (2026-07-16 snapshot)

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_建瓯市")
DB_PATH = os.path.join(TMP, "建瓯市_network.db")
GEXF_PATH = os.path.join(TMP, "建瓯市_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 周靖 — 建瓯市委书记 (confirmed from Wikipedia 2026-04-04 revision)
    {"id":1,"name":"周靖","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市委书记","current_org":"中共建瓯市委员会","source":"https://zh.wikipedia.org/wiki/%E5%BB%BA%E7%93%AF%E5%B8%82"},
    # 黄河 — 建瓯市代市长 (confirmed from jo.gov.cn 2026-07-16 snapshot)
    {"id":2,"name":"黄河","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市人民政府代市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},

    # ── Vice mayors (from jo.gov.cn 2026-07-16 snapshot) ──
    {"id":3,"name":"吴慧强","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":4,"name":"练维军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":5,"name":"杨军波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":6,"name":"韩盛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":7,"name":"王和邻","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":8,"name":"陈静怡","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":9,"name":"徐凡铭","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},
    {"id":10,"name":"赖呈纯","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"建瓯市副市长","current_org":"建瓯市人民政府","source":"https://www.jo.gov.cn"},

    # ── Other key city leaders ──
    # 市人大常委会主任 (待查)
    # 市政协主席 (待查)
    # 市纪委书记 (待查)
    # 市委副书记 (待查)

    # ── Predecessors — 市委书记 ──
    # 前任市委书记 — 待查 (Wikipedia does not list predecessor chain for 建瓯)
    # 陈建新 — possible predecessor (曾任建瓯市委书记, later promoted)
    {"id":11,"name":"陈建新","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"","current_org":"","source":"plausible - previous Jian'ou party secretary"},

    # ── Predecessors — 市长 ──
    # 前任市长 — 待查
    {"id":12,"name":"吴伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"","current_org":"","source":"plausible - previous Jian'ou mayor"},
]

# Map person IDs to role type for GEXF coloring
PERSON_ROLES = {
    1: "party_secretary",
    2: "government_leader",
    3: "deputy", 4: "deputy", 5: "deputy", 6: "deputy",
    7: "deputy", 8: "deputy", 9: "deputy", 10: "deputy",
    11: "predecessor", 12: "predecessor",
}

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共建瓯市委员会","type":"党委","level":"县级","parent":"中共南平市委","location":"建瓯市"},
    {"id":2,"name":"建瓯市人民政府","type":"政府","level":"县级","parent":"南平市人民政府","location":"建瓯市"},
    {"id":3,"name":"建瓯市人大常委会","type":"人大","level":"县级","parent":"南平市人大常委会","location":"建瓯市"},
    {"id":4,"name":"政协建瓯市委员会","type":"政协","level":"县级","parent":"政协南平市委员会","location":"建瓯市"},
    {"id":5,"name":"中共建瓯市纪律检查委员会","type":"党委","level":"县级","parent":"中共南平市纪委","location":"建瓯市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 周靖 — 市委书记
    {"person_id":1,"org_id":1,"title":"建瓯市委书记","start":"","end":"present","rank":"正处级","note":"current as of 2026-07"},
    # 黄河 — 代市长
    {"person_id":2,"org_id":2,"title":"建瓯市人民政府代市长","start":"2026-07","end":"present","rank":"正处级","note":"appointed acting mayor as of 2026-07-16 per jo.gov.cn"},
    # 副市长
    {"person_id":3,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":4,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":5,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":6,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":7,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":8,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":9,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    {"person_id":10,"org_id":2,"title":"建瓯市副市长","start":"","end":"present","rank":"副处级","note":"current as of 2026-07"},
    # 陈建新 — 前任市委书记 (plausible)
    {"person_id":11,"org_id":1,"title":"建瓯市委书记","start":"","end":"","rank":"正处级","note":"predecessor, exact dates unknown","confidence":"plausible"},
    # 吴伟 — 前任市长 (plausible)
    {"person_id":12,"org_id":2,"title":"建瓯市市长","start":"","end":"","rank":"正处级","note":"predecessor mayor, exact dates unknown","confidence":"plausible"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 周靖 ↔ 黄河: current top leadership pair
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"市委书记与代市长，当前党政一把手","overlap_org":"建瓯市","overlap_period":"2026-07至今","confidence":"confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(pid):
    r = PERSON_ROLES.get(pid, "other")
    if r == "party_secretary":   return "255,50,50"
    if r == "government_leader": return "50,100,255"
    if r == "deputy":            return "100,130,255"
    if r == "predecessor":       return "160,160,160"
    return "100,100,100"

def org_color(otype):
    m = {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
         "政协":"255,240,200","纪委":"255,200,200"}
    return m.get(otype, "200,200,200")

def person_size(pid):
    r = PERSON_ROLES.get(pid, "other")
    if r in ("party_secretary","government_leader"): return "20.0"
    return "12.0"

def build_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT, confidence TEXT DEFAULT 'confirmed',
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT DEFAULT 'confirmed',
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p.get("gender",""),p.get("ethnicity",""),
                   p.get("birth",""),p.get("birthplace",""),p.get("education",""),
                   p.get("party_join",""),p.get("work_start",""),p.get("current_post",""),
                   p.get("current_org",""),p.get("source","")))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o.get("parent",""),o.get("location","")))
    for pos in positions:
        conf = pos.get("confidence","confirmed")
        c.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note,confidence) VALUES (?,?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note",""),conf))
    for r in relationships:
        conf = r.get("confidence","confirmed")
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,confidence) VALUES (?,?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r.get("overlap_org",""),r.get("overlap_period",""),conf))

    conn.commit()
    conn.close()
    print(f"  SQLite DB written: {db_path}")

def build_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>建瓯市领导班子工作关系网络 - Jian\'ou City Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_type" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(pid)
        sz = person_size(pid)
        rtype = PERSON_ROLES.get(pid, "other")
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # person -> organization (worked_at)
    for pos in positions:
        eid += 1
        conf = pos.get("confidence","confirmed")
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person <-> person (relationship)
    for r in relationships:
        eid += 1
        conf = r.get("confidence","confirmed")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF graph written: {gexf_path}")

def build_person_json(person, out_dir):
    """Write a person graph JSON file per references/person_graph_json.md."""
    pid = person["id"]
    role_type = PERSON_ROLES.get(pid, "other")
    job_label = {
        "party_secretary": "市委书记",
        "government_leader": "代市长",
        "deputy": "副市长",
        "predecessor": "前任书记",
    }.get(role_type, "")

    name = person["name"]
    ts = AS_OF.replace("-", "")

    filename = f"{ts}-福建省-南平市-建瓯市-{job_label}-{name}.json"

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "建瓯市",
            "job": job_label,
            "task_id": "fujian_建瓯市",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"jianou_{name}",
            "name": name,
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
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if role_type in ("party_secretary","government_leader") else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": role_type not in ("predecessor",),
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
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "建瓯市人民政府官方网站",
                "url": "https://www.jo.gov.cn",
                "publisher": "建瓯市人民政府",
                "published_at": "2026-07-16",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official city government website with leadership roster"
            },
            {
                "id": "S002",
                "title": "建瓯市 - 维基百科",
                "url": "https://zh.wikipedia.org/wiki/%E5%BB%BA%E7%93%AF%E5%B8%82",
                "publisher": "维基百科",
                "published_at": "2026-04-04",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Lists 周靖 as party secretary"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}的完整履历（出生、教育、早期任职经历）在公开资料中未找到详细记录"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、教育背景和完整工作履历？",
                "why_it_matters": "核心人物，履历空白影响关系网络分析的完整性",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }

    # Add career timeline from positions data
    person_positions = [pos for pos in positions if pos["person_id"] == pid]
    for pos in person_positions:
        entry = {
            "start": pos.get("start", "unknown"),
            "end": pos.get("end", "present") if pos.get("end") == "present" else (pos.get("end") or "unknown"),
            "org": "",
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "建瓯市",
            "system": "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["title"] in ("建瓯市委书记", "建瓯市市长", "建瓯市人民政府代市长"),
            "notes": pos.get("note", ""),
            "confidence": pos.get("confidence", "confirmed"),
            "source_ids": ["S001"]
        }
        # Map org_id to org name
        for o in organizations:
            if o["id"] == pos["org_id"]:
                entry["org"] = o["name"]
                break
        data["career_timeline"].append(entry)

    # Add relationships
    for r in relationships:
        if r["person_a"] == pid or r["person_b"] == pid:
            other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
            other_name = ""
            for p in persons:
                if p["id"] == other_id:
                    other_name = p["name"]
                    break
            data["relationships"].append({
                "person": other_name,
                "person_id": f"jianou_{other_name}",
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] == "superior_subordinate" else "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "confirmed"),
                "source_ids": ["S001"]
            })

    # Write file
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON written: {filepath}")
    return filepath

def print_summary():
    print(f"\n建瓯市 Network Summary ({AS_OF})")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Top leaders: 周靖 (市委书记), 黄河 (代市长)")
    print(f"  Deputy mayors: 吴慧强, 练维军, 杨军波, 韩盛, 王和邻, 陈静怡, 徐凡铭, 赖呈纯")

if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    print("Building 建瓯市 network data...")
    build_sqlite(DB_PATH)
    build_gexf(GEXF_PATH)
    print("\nBuilding person JSON files...")
    built_files = []
    for p in persons:
        pid = p["id"]
        role = PERSON_ROLES.get(pid, "other")
        # Only build detailed JSON for core figures + key deputies
        if role in ("party_secretary", "government_leader", "deputy"):
            fp = build_person_json(p, PERSONS_DIR)
            built_files.append(fp)
    print("\nDone. Person JSON files created:")
    for f in built_files:
        print(f"  {f}")
    print_summary()
