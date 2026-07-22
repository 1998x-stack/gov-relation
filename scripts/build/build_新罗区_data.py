#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Xinluo District (新罗区), Longyan City, Fujian.

Level: 市辖区
Province: 福建省
Parent City: 龙岩市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 空缺中 (confirmed per Wikipedia - position currently vacant as of July 2026)
- 区长: 邱伟勤 (confirmed per Wikipedia)

Key gaps:
- 区委书记 predecessor(s) not fully verified through official sources
- Birth dates, education, full career timelines for most officials
- Full district leadership roster beyond the top two
- The 区委书记 is listed as 空缺中 (vacant) on Wikipedia - needs verification
  if this is a temporary vacancy or a long-standing gap

Sources:
- Chinese Wikipedia: 新罗区 entry (zh.wikipedia.org) - accessed July 2026
- fjxinluo.gov.cn: Official Xinluo District government website (unreachable during research)
- longyan.gov.cn: Longyan City government website

Current as of: July 2026
"""

import sqlite3, os, json, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "新罗区_network.db")
GEXF_PATH = os.path.join(BASE, "新罗区_network.gexf")
PERSONS_DIR = BASE

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current & recent top leadership
    # ═════════════════════════════════════════════════════════════════════

    # NOTE: 区委书记 entry is intentionally included as an unknown/unconfirmed
    # placeholder. Wikipedia lists the position as "空缺中" (vacant) as of July 2026.
    # The immediate predecessor is unclear from available sources.

    # 邱伟勤 — 新罗区委副书记、区长 (confirmed per Wikipedia)
    {"id":1,"name":"邱伟勤","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"新罗区委副书记、区长","current_org":"新罗区人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E6%96%B0%E7%BD%97%E5%8C%BA"},

    # ═════════════════════════════════════════════════════════════════════
    # Other known district leaders (from available sources)
    # ═════════════════════════════════════════════════════════════════════

    # Known preceding 区委书记 — 张锋 (last known区委书记 before vacancy)
    # Based on news reports from 2022, 张锋 served as 新罗区委书记
    # Removed due to insufficient verification — need official sources

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors — 区委书记 (to be verified)
    # ═════════════════════════════════════════════════════════════════════

    # Predecessor information for 区委书记 position not fully verified.
    # 新罗区 (as Longyan County / Longyan City) has a long history.
    # Recent区委书记 predecessors may include:
    # - 张锋 (pre-2023/2024, needs confirmation)
    # - 陈金龙 (served ~2016-2021, later promoted to 龙岩市 level)
    # These need verification from official sources before inclusion.

    # ═════════════════════════════════════════════════════════════════════
    # Predecessors — 区长
    # ═════════════════════════════════════════════════════════════════════

    # Predecessor 区长 information not yet verified from official sources.
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共龙岩市新罗区委员会","type":"党委","level":"县处级","parent":"中共龙岩市委员会","location":"福建省龙岩市新罗区"},
    {"id":2,"name":"新罗区人民政府","type":"政府","level":"县处级","parent":"龙岩市人民政府","location":"福建省龙岩市新罗区"},
    {"id":3,"name":"中共龙岩市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省龙岩市"},
    {"id":4,"name":"龙岩市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省龙岩市"},
    {"id":5,"name":"中共福建省纪律检查委员会","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},
    {"id":6,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},
    {"id":7,"name":"中共福建省委员会","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 邱伟勤 — District Mayor
    {"person_id":1,"org_id":2,"title":"新罗区区长","start":"","end":"present","rank":"正处级","note":"邱伟勤 — 现任新罗区长（确认于维基百科）"},
    {"person_id":1,"org_id":1,"title":"新罗区委副书记","start":"","end":"present","rank":"正处级","note":"兼任区委副书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # No verified relationship edges with sufficient evidence yet.
    # Will be populated when predecessor/successor and deputy data is available.
]

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT
    )""")
    c.execute("""CREATE TABLE organizations(
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, "end" TEXT,
        rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                   p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "区委书记" in post:
        return "230,50,50"
    if "区长" in post or "代区长" in post:
        return "50,100,230"
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200","人大":"200,255,255","政协":"255,240,200"}.get(otype,"200,200,200")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>新罗区（龙岩市辖区）领导班子工作关系网络 — 2026年7月生成</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = pcolor(p.get("current_post",""))
        # Add a vacant-party-secretary node as a placeholder
        is_top = any(k in p.get("current_post","") for k in ["区委书记","区长","代区长"])
        sz = "20.0" if is_top else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = ocolor(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        ov = r.get("overlap_period","")
        ov_s = ov.split("至今")[0] if "至今" in ov else ov
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    print(f"GEXF: {GEXF_PATH}")
    print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
    print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(pid, filename_suffix):
    p = next(x for x in persons if x["id"] == pid)

    # Build relationships for this person
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r.get("strength","weak"),"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r.get("direction","undirected"),
                             "confidence":"unverified","source_ids":["S001"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r.get("strength","weak"),"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r.get("direction","undirected"),
                             "confidence":"unverified","source_ids":["S001"]})

    # Build positions for this person
    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            system = "government"
            if org:
                if "党委" in org.get("type","") or "纪委" in org.get("type",""):
                    system = "party"
                elif "人大" in org.get("type",""):
                    system = "other"
                elif "政协" in org.get("type",""):
                    system = "other"

            person_positions.append({
                "start":pos.get("start","unknown"),
                "end":pos.get("end","present"),
                "org":org["name"] if org else "",
                "title":pos["title"],
                "level":pos.get("rank",""),
                "location":org["location"] if org else "",
                "system":system,
                "rank":pos.get("rank",""),
                "is_key_promotion":False,
                "notes":pos.get("note",""),
                "confidence":"confirmed",
                "source_ids":["S001"]
            })

    # Source register
    source_register = [
        {"id":"S001","title":"新罗区 - 维基百科","url":"https://zh.wikipedia.org/wiki/%E6%96%B0%E7%BD%97%E5%8C%BA",
         "publisher":"维基百科","published_at":"","accessed_at":"2026-07-17","source_type":"encyclopedia","reliability":"medium",
         "notes":"Wikipedia条目显示区委书记为'空缺中'，区长为邱伟勤。Infobox数据需以官方来源核实。"},
        {"id":"S002","title":"龙岩市新罗区人民政府门户网站","url":"http://www.fjxinluo.gov.cn/",
         "publisher":"新罗区人民政府","published_at":"","accessed_at":"2026-07-17","source_type":"official","reliability":"high",
         "notes":"官方网站在调查期间无法访问"},
    ]

    profile = {
        "schema_version": "1.0",
        "generated_at": "2026-07-17",
        "investigation_scope": {
            "province": "福建省",
            "city": "龙岩市",
            "region": "新罗区",
            "job": filename_suffix,
            "task_id": "fujian_新罗区",
            "time_focus": "present"
        },
        "identity": {
            "person_id": f"fujian_longyan_xinluo_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":"","study_type":"unknown","source_ids":[]}],
            "party_join": p.get("party_join",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "http://www.fjxinluo.gov.cn/"
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正处级",
            "as_of": "2026-07-17",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": person_positions,
        "organizations": [o for o in organizations if "新罗" in o["name"]],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"缺少{p['name']}的出生、教育背景和完整履历。区委书记职位空缺。"
        },
        "open_questions": [
            {"priority":"critical","question":"新罗区委书记最新人选/任命情况（维基百科显示'空缺中'）",
             "why_it_matters":"区委书记是核心领导岗位，空缺状态需要确认是否为正式空缺或维基百科未及时更新",
             "suggested_queries":["新罗区 区委书记 任命 2025","新罗区 区委书记 2026","新罗区 干部大会"],
             "last_attempted":"2026-07-17"},
            {"priority":"high","question":f"{p['name']}的出生地和早期教育背景",
             "why_it_matters":"影响人物身份确认和履历完整度",
             "suggested_queries":[f"{p['name']} 简历 新罗区",f"{p['name']} 出生"],
             "last_attempted":"2026-07-17"},
            {"priority":"high","question":f"{p['name']}在任新罗区前的完整履历",
             "why_it_matters":"理解其职业发展路径和提拔背景",
             "suggested_queries":[f"{p['name']} 任职经历 龙岩"],
             "last_attempted":"2026-07-17"},
            {"priority":"high","question":"前任新罗区委书记的去向和时间线",
             "why_it_matters":"完成前任-继任链条，了解人事变动背景",
             "suggested_queries":["张锋 新罗区委书记","陈金龙 新罗区委书记"],
             "last_attempted":"2026-07-17"},
            {"priority":"medium","question":"新罗区委常委班子完整名单",
             "why_it_matters":"了解区级领导班子全貌，发现潜在关系网",
             "suggested_queries":["新罗区 区委常委 名单"],
             "last_attempted":"2026-07-17"},
            {"priority":"medium","question":"邱伟勤的前任区长是谁",
             "why_it_matches":"完成区长职位的前任-继任链条",
             "suggested_queries":["新罗区 前任区长"],
             "last_attempted":"2026-07-17"}
        ]
    }

    filename = f"20260717-福建省-龙岩市-{filename_suffix}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_sqlite()
    build_gexf()
    # Write person JSON for 邱伟勤 (the confirmed 区长)
    write_person_json(1, "区长")

    print("\nDone. All artifacts written to", BASE)
    print(f"\nNOTE: This data requires significant verification. Key items:")
    print(f"  1. 区委书记 position is listed as '空缺中' (vacant) on Wikipedia as of July 2026")
    print(f"  2. Verify 邱伟勤's full name, birth, education, and career timeline")
    print(f"  3. Confirm the vacancy status — is the区委书记 truly vacant or was Wikipedia not updated?")
    print(f"  4. Add predecessor区委书记 and 区长 chains")
    print(f"  5. Add full standing committee members (区纪委、组织部、宣传部、政法委等)")
