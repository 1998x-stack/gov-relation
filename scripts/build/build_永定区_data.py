#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Yongding District (永定区), Longyan City, Fujian.

Covers: Party Secretary (区委书记), District Mayor (区长), key leadership,
predecessor/successor chains, and the district-level leadership network.

Sources:
- Wikipedia (Chinese): 永定区 (龙岩市) leadership info
- yongding.gov.cn: Official Yongding district government website
- Various news reports

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_永定区")
DB_PATH = os.path.join(TMP, "永定区_network.db")
GEXF_PATH = os.path.join(TMP, "永定区_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 李强 — 永定区委书记（2025?-present）
    {"id":1,"name":"李强","gender":"男","ethnicity":"汉族","birth":"1979-09","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"永定区委书记","current_org":"中共龙岩市永定区委员会",
     "source":"https://zh.wikipedia.org/wiki/%E6%B0%B8%E5%AE%9A%E5%8C%BA_(%E9%BE%99%E5%B2%A9%E5%B8%82)"},

    # 王秀金 — 永定区代理区长（2026?-present）
    {"id":2,"name":"王秀金","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"永定区代理区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},

    # ── Deputy District Mayors ──
    {"id":3,"name":"卢权国","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":4,"name":"王文龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":5,"name":"毛四勤","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":6,"name":"龚泽祥","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":7,"name":"吴文琴","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":8,"name":"温福英","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":9,"name":"陈建平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":10,"name":"李达才","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},
    {"id":11,"name":"赖大彬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"永定区副区长","current_org":"龙岩市永定区人民政府",
     "source":"https://www.yongding.gov.cn/xxgk/"},

    # ── Other key district leaders ──
    {"id":12,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"区人大常委会主任（待确认）","current_org":"龙岩市永定区人大常委会",
     "source":"待确认"},
    {"id":13,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"区政协主席（待确认）","current_org":"政协龙岩市永定区委员会",
     "source":"待确认"},

    # ── Predecessors — 区委书记 ──
    # 李强的已知前任信息有限，需后续调查
    {"id":14,"name":"（前任区委书记待核实）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"待核实"},

    # ── Predecessors — 区长 ──
    # 王秀金接任前的区长待核实
    {"id":15,"name":"（前任区长待核实）","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"待核实"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共龙岩市永定区委员会","type":"党委","level":"县处级","parent":"中共龙岩市委员会","location":"福建省龙岩市永定区"},
    {"id":2,"name":"龙岩市永定区人民政府","type":"政府","level":"县处级","parent":"龙岩市人民政府","location":"福建省龙岩市永定区"},
    {"id":3,"name":"龙岩市永定区人大常委会","type":"人大","level":"县处级","parent":"","location":"福建省龙岩市永定区"},
    {"id":4,"name":"政协龙岩市永定区委员会","type":"政协","level":"县处级","parent":"","location":"福建省龙岩市永定区"},
    {"id":5,"name":"中共龙岩市永定区纪律检查委员会","type":"纪委","level":"县处级","parent":"中共龙岩市永定区委员会","location":"福建省龙岩市永定区"},
    {"id":6,"name":"中共龙岩市委组织部","type":"党委部门","level":"地厅级","parent":"中共龙岩市委员会","location":"福建省龙岩市"},
    # Key towns/sub-districts
    {"id":7,"name":"永定区凤城街道","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":8,"name":"永定区坎市镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":9,"name":"永定区高陂镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":10,"name":"永定区湖雷镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":11,"name":"永定区下洋镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":12,"name":"永定区培丰镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":13,"name":"永定区抚市镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":14,"name":"永定区湖坑镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":15,"name":"永定区龙潭镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":16,"name":"永定区峰市镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":17,"name":"永定区城郊镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":18,"name":"永定区仙师镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":19,"name":"永定区虎岗镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":20,"name":"永定区堂堡镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":21,"name":"永定区岐岭镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":22,"name":"永定区西溪乡","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":23,"name":"永定区金砂镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":24,"name":"永定区洪山镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":25,"name":"永定区湖山乡","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":26,"name":"永定区古竹乡","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":27,"name":"永定区合溪乡","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":28,"name":"永定区大溪乡","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":29,"name":"永定区陈东乡","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
    {"id":30,"name":"永定区高头镇","type":"乡镇/街道","level":"乡科级","parent":"龙岩市永定区人民政府","location":"福建省龙岩市永定区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 李强 — Party Secretary
    {"person_id":1,"org_id":1,"title":"永定区委书记","start":"","end":"present","rank":"正处级","note":"Wikipedia记载为现任区委书记（1979年9月出生）"},

    # 王秀金 — Acting District Mayor
    {"person_id":2,"org_id":2,"title":"永定区代理区长","start":"","end":"present","rank":"正处级","note":"2026年7月区人民政府网站显示为代理区长"},
    {"person_id":2,"org_id":1,"title":"永定区委副书记","start":"","end":"present","rank":"正处级","note":""},

    # Deputy District Mayors
    {"person_id":3,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":4,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":5,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":6,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":7,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":"女"},
    {"person_id":8,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":"女"},
    {"person_id":9,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":10,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":11,"org_id":2,"title":"永定区副区长","start":"","end":"present","rank":"副处级","note":""},

    # 人大、政协（待确认）
    {"person_id":12,"org_id":3,"title":"区人大常委会主任（待确认）","start":"","end":"present","rank":"正处级","note":"姓名待确认"},
    {"person_id":13,"org_id":4,"title":"区政协主席（待确认）","start":"","end":"present","rank":"正处级","note":"姓名待确认"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 区委书记与区长搭班关系
    {"person_a":1,"person_b":2,"type":"colleague","context":"李强任区委书记、王秀金任代理区长搭班","overlap_org":"中共龙岩市永定区委员会","overlap_period":"2026-","direction":"undirected","strength":"strong"},
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        direction TEXT, strength TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"],
                   o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                   pos["end"], pos["rank"], pos.get("note", "")))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, direction, strength) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"], r["direction"], r["strength"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b string for a person by role."""
    title = p["current_post"]
    if "书记" in title and "区委" in title:
        return "255,50,50"   # Red for Party Secretary
    elif "区长" in title:
        return "50,100,255"  # Blue for District Mayor
    elif "副区长" in title:
        return "50,100,255"  # Blue for Deputy Mayor
    elif "纪委" in title:
        return "255,165,0"   # Orange for Discipline
    else:
        return "100,100,100"  # Grey for others


def org_color(o):
    """Return r,g,b string for an organization by type."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "纪委" in t:
        return "255,200,150"
    else:
        return "200,200,200"


def is_top_leader(p):
    """Check if a person is a top leader (书记/区长)."""
    return p["id"] in [1, 2]


def org_size(o):
    return "8.0"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>龙岩市永定区领导班子工作关系网络 - Fujian Province, Longyan City, Yongding District</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="福建省龙岩市永定区"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{org_size(o)}"/>')
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
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(pid, filename_suffix):
    p = next(x for x in persons if x["id"] == pid)
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})

    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            person_positions.append({
                "start":pos["start"],"end":pos["end"],"org":org["name"] if org else "",
                "title":pos["title"],"level":pos.get("rank",""),"location":org["location"] if org else "",
                "system":"party" if org and "党委" in org["type"] else "government",
                "rank":pos.get("rank",""),"is_key_promotion":False,"notes":pos.get("note",""),
                "confidence":"confirmed","source_ids":["S001","S002"]
            })

    profile = {
        "schema_version": "1.0",
        "generated_at": "2026-07-17",
        "investigation_scope": {
            "province": "福建省",
            "city": "龙岩市",
            "region": "永定区",
            "job": filename_suffix,
            "task_id": "fujian_永定区",
            "time_focus": "2020-present"
        },
        "identity": {
            "person_id": f"fujian_yongding_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":"","study_type":"unknown","source_ids":[]}],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {"name_birth":"","name_birthplace":"","official_profile_url":""}
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正处级",
            "as_of": "2026-07-17",
            "is_current_confirmed": True if p["name"] not in ["（待确认）","（前任区委书记待核实）","（前任区长待核实）"] else False,
            "source_ids": ["S001","S002"]
        },
        "career_timeline": person_positions,
        "organizations": [],
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
        "source_register": [
            {"id":"S001","title":"永定区 (龙岩市) - 维基百科","url":"https://zh.wikipedia.org/wiki/%E6%B0%B8%E5%AE%9A%E5%8C%BA_(%E9%BE%99%E5%B2%A9%E5%B8%82)",
             "publisher":"维基百科","published_at":"","accessed_at":"2026-07-17","source_type":"encyclopedia","reliability":"medium","notes":"提供了区委书记李强信息"},
            {"id":"S002","title":"永定区人民政府门户网站","url":"https://www.yongding.gov.cn/xxgk/",
             "publisher":"龙岩市永定区人民政府","published_at":"","accessed_at":"2026-07-17","source_type":"official","reliability":"high","notes":"提供了代理区长王秀金及9名副区长名单"}
        ],
        "confidence_summary": {
            "identity":"partial" if "待" in p["name"] else "confirmed",
            "current_role":"confirmed" if p["name"] not in ["（待确认）","（前任区委书记待核实）","（前任区长待核实）"] else "unverified",
            "career_completeness":"thin",
            "relationship_confidence":"medium",
            "biggest_gap":f"缺少{p['name']}的完整履历——出生地、教育背景、任职经历"
        },
        "open_questions": [
            {"priority":"high","question":f"{p['name']}的出生地和教育背景","why_it_matters":"影响人物身份确认","suggested_queries":[f"{p['name']} 简历",f"{p['name']} 出生"],"last_attempted":"2026-07-17"},
            {"priority":"high","question":f"{p['name']}在任永定区前的完整履历","why_it_matters":"理解其职业发展路径","suggested_queries":[f"{p['name']} 任职经历"],"last_attempted":"2026-07-17"}
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
    write_person_json(1, "区委书记")
    write_person_json(2, "代理区长")
    print("\nDone. All artifacts written to", TMP)
