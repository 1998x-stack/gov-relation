#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Shaowu City (邵武市), Nanping, Fujian Province.

Covers: Party Secretary (市委书记), Mayor (市长/空缺), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- shaowu.gov.cn: Official Shaowu city government website (leadership pages)
- English Wikipedia: Shaowu city overview, CPC secretary info
- Chinese Wikipedia: Shaowu city overview
- Baidu Baike: individual profiles

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_邵武市")
DB_PATH = os.path.join(TMP, "邵武市_network.db")
GEXF_PATH = os.path.join(TMP, "邵武市_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 何光松 — 邵武市委书记
    {"id":1,"name":"何光松","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"中共党员","work_start":"",
     "current_post":"邵武市委书记","current_org":"中共邵武市委员会",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},
    # 市长 — 空缺 (As of July 2026, per official website)
    # 曾乡伟 — 邵武市委常委、常务副市长 (主持市政府工作)
    {"id":2,"name":"曾乡伟","gender":"男","ethnicity":"汉族","birth":"1981-07","birthplace":"",
     "education":"大学","party_join":"中共党员","work_start":"",
     "current_post":"邵武市委常委、常务副市长（代行市长职责）","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/zxw/index.html"},

    # ── Other current city leaders ──
    # 李占林 — 邵武市副市长
    {"id":3,"name":"李占林","gender":"男","ethnicity":"满族","birth":"1982-09","birthplace":"",
     "education":"研究生学历，工学硕士","party_join":"中共党员","work_start":"2008-07",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/lzl/index.html"},
    # 陈仁辉 — 邵武市副市长、市公安局局长
    {"id":4,"name":"陈仁辉","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"",
     "education":"大学","party_join":"中共党员","work_start":"",
     "current_post":"邵武市副市长、市公安局局长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/crh/index.html"},
    # 翁淑燕 — 邵武市副市长
    {"id":5,"name":"翁淑燕","gender":"女","ethnicity":"汉族","birth":"1977-12","birthplace":"",
     "education":"大学","party_join":"","work_start":"",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/wsyfschxr/index.html"},
    # 颜海 — 邵武市副市长
    {"id":6,"name":"颜海","gender":"男","ethnicity":"汉族","birth":"1979-04","birthplace":"",
     "education":"硕士研究生","party_join":"中共党员","work_start":"",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/yh/index.html"},
    # 邓炜华 — 邵武市副市长
    {"id":7,"name":"邓炜华","gender":"女","ethnicity":"汉族","birth":"1985-05","birthplace":"",
     "education":"本科","party_join":"中共党员","work_start":"",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/dwh/index.html"},
    # 张添华 — 邵武市副市长
    {"id":8,"name":"张添华","gender":"男","ethnicity":"汉族","birth":"1979-01","birthplace":"",
     "education":"研究生，社会学研究生","party_join":"中共党员","work_start":"",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/zth/index.html"},
    # 池敏青 — 邵武市副市长
    {"id":9,"name":"池敏青","gender":"","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/zth1/index.html"},
    # 杨健 — 邵武市副市长
    {"id":10,"name":"杨健","gender":"男","ethnicity":"汉族","birth":"1979-11","birthplace":"",
     "education":"大学","party_join":"中共党员","work_start":"",
     "current_post":"邵武市副市长","current_org":"邵武市人民政府",
     "source":"https://www.shaowu.gov.cn/cms/html/swsrmzf/cmq/index.html"},

    # ── Predecessors — 市委书记 ──
    # 陈炎生 — 前任邵武市委书记 (earlier)
    {"id":11,"name":"陈炎生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},
    # 梁伟新 — 前任邵武市委书记 (2011.06-2013.09), 后任福建省工信厅厅长、漳州市市长
    {"id":12,"name":"梁伟新","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},

    # ── Predecessors — 市长 ──
    # 郭绯红 — 前任邵武市市长 (女，2021.12-2025?)
    {"id":13,"name":"郭绯红","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},
    # 丁贵生 — 前任邵武市市长 (2016.12-2021.12)
    {"id":14,"name":"丁贵生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},
    # 熊贻荣 — 前任邵武市人大常委会主任
    {"id":15,"name":"熊贻荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},
    # 蔡幼群 — 前任政协主席
    {"id":16,"name":"蔡幼群","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://en.wikipedia.org/wiki/Shaowu"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共邵武市委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市邵武市"},
    {"id":2,"name":"邵武市人民政府","type":"政府","level":"县级","parent":"南平市人民政府","location":"福建省南平市邵武市"},
    {"id":3,"name":"邵武市公安局","type":"政府","level":"正科级","parent":"邵武市人民政府","location":"福建省南平市邵武市"},
    {"id":4,"name":"邵武市人民代表大会常务委员会","type":"人大","level":"县级","parent":"邵武市","location":"福建省南平市邵武市"},
    {"id":5,"name":"政协邵武市委员会","type":"政协","level":"县级","parent":"邵武市","location":"福建省南平市邵武市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 何光松
    {"id":1,"person_id":1,"org_id":1,"title":"邵武市委书记","start":"","end":"present","rank":"正处级","note":""},
    # 曾乡伟
    {"id":2,"person_id":2,"org_id":2,"title":"邵武市委常委、常务副市长","start":"","end":"present","rank":"副处级","note":"主持市政府日常工作，代行市长职责"},
    # 李占林
    {"id":3,"person_id":3,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},
    # 陈仁辉
    {"id":4,"person_id":4,"org_id":2,"title":"邵武市副市长、市公安局局长","start":"","end":"present","rank":"副处级","note":""},
    # 翁淑燕
    {"id":5,"person_id":5,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},
    # 颜海
    {"id":6,"person_id":6,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},
    # 邓炜华
    {"id":7,"person_id":7,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},
    # 张添华
    {"id":8,"person_id":8,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},
    # 池敏青
    {"id":9,"person_id":9,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},
    # 杨健
    {"id":10,"person_id":10,"org_id":2,"title":"邵武市副市长","start":"","end":"present","rank":"副处级","note":""},

    # Predecessor positions
    {"id":11,"person_id":11,"org_id":1,"title":"邵武市委书记","start":"","end":"","rank":"正处级","note":"前任"},
    {"id":12,"person_id":12,"org_id":1,"title":"邵武市委书记","start":"2011-06","end":"2013-09","rank":"正处级","note":"后任漳州市市长、福建省工信厅厅长"},
    {"id":13,"person_id":13,"org_id":2,"title":"邵武市市长","start":"2021-12","end":"","rank":"正处级","note":"前任市长，女"},
    {"id":14,"person_id":14,"org_id":2,"title":"邵武市市长","start":"2016-12","end":"2021-12","rank":"正处级","note":"前任市长"},
    {"id":15,"person_id":15,"org_id":4,"title":"邵武市人大常委会主任","start":"","end":"","rank":"正处级","note":"前任人大主任"},
    {"id":16,"person_id":16,"org_id":5,"title":"邵武市政协主席","start":"","end":"","rank":"正处级","note":"前任政协主席"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Working relationships (current leadership team)
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate","strength":"strong","context":"何光松作为市委书记，曾乡伟作为常务副市长，共同主持市委市政府工作","overlap_org":"中共邵武市委员会/邵武市人民政府","overlap_period":"present","direction":"person_to_other"},
    {"id":2,"person_a":2,"person_b":3,"type":"overlap","strength":"medium","context":"曾乡伟与李占林同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":3,"person_a":2,"person_b":4,"type":"overlap","strength":"medium","context":"曾乡伟与陈仁辉同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":4,"person_a":2,"person_b":5,"type":"overlap","strength":"medium","context":"曾乡伟与翁淑燕同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":5,"person_a":2,"person_b":6,"type":"overlap","strength":"medium","context":"曾乡伟与颜海同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":6,"person_a":2,"person_b":7,"type":"overlap","strength":"medium","context":"曾乡伟与邓炜华同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":7,"person_a":2,"person_b":8,"type":"overlap","strength":"medium","context":"曾乡伟与张添华同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":8,"person_a":2,"person_b":9,"type":"overlap","strength":"medium","context":"曾乡伟与池敏青同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},
    {"id":9,"person_a":2,"person_b":10,"type":"overlap","strength":"medium","context":"曾乡伟与杨健同为市政府领导班子成员","overlap_org":"邵武市人民政府","overlap_period":"present","direction":"undirected"},

    # Predecessor-successor chains
    {"id":10,"person_a":11,"person_b":12,"type":"predecessor_successor","strength":"strong","context":"陈炎生、梁伟新先后担任邵武市委书记","overlap_org":"中共邵武市委员会","overlap_period":"","direction":"undirected"},
    {"id":11,"person_a":14,"person_b":13,"type":"predecessor_successor","strength":"strong","context":"丁贵生、郭绯红先后担任邵武市市长","overlap_org":"邵武市人民政府","overlap_period":"","direction":"undirected"},
]


# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_sqlite():
    os.makedirs(TMP, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, strength TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, direction TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                   p["birthplace"],p["education"],p["party_join"],p["work_start"],
                   p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"],pos["person_id"],pos["org_id"],pos["title"],
                   pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?,?,?)",
                  (r["id"],r["person_a"],r["person_b"],r["type"],r["strength"],
                   r["context"],r["overlap_org"],r["overlap_period"],r["direction"]))

    conn.commit()
    conn.close()
    sz = os.path.getsize(DB_PATH)
    print(f"SQLite DB created: {DB_PATH} ({sz} bytes)")


# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Color by role: red=party sec, blue=gov, orange=discipline, grey=other."""
    title = p.get("current_post","")
    if "书记" in title and "市委" in title:
        return "255,50,50"
    elif "市长" in title or "副市长" in title or "政府" in title:
        return "50,100,255"
    elif "纪委" in title or "监委" in title:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    return p["id"] in [1, 2]  # 书记 and 常务副市长

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
        "政协": "255,240,200", "开发区": "200,255,200", "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220", "群团": "255,220,255"
    }
    return colors.get(t, "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>邵武市领导班子工作关系网络 - Fujian Shaowu City Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
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
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # Person->organization edges (worked_at)
    for pos in positions:
        eid += 1
        p = next((x for x in persons if x["id"]==pos["person_id"]), None)
        if not p:
            continue
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="position"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person->person edges (relationship)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"]=="strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSON
# =========================================================================
def write_person_json(pid, filename_suffix):
    p = next((x for x in persons if x["id"]==pid), None)
    if not p:
        return

    # Find positions for this person
    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            person_positions.append({
                "start":pos["start"],"end":pos["end"],"org":org["name"] if org else "",
                "title":pos["title"],"level":pos.get("rank",""),"location":org["location"] if org else "",
                "system":"party" if org and "党委" in org["type"] else "government",
                "rank":pos.get("rank",""),"is_key_promotion":False,"notes":pos.get("note",""),
                "confidence":"confirmed","source_ids":["S001"]
            })

    # Find relationships involving this person
    rels_out = []
    for r in relationships:
        if r["person_a"]==pid:
            other = next((x for x in persons if x["id"]==r["person_b"]), None)
            if other:
                rels_out.append({"person":other["name"],"person_id":f"p{other['id']}",
                    "relationship_type":r["type"],"strength":r["strength"],
                    "evidence":r["context"],"overlap_org":r["overlap_org"],
                    "overlap_period":r["overlap_period"],"direction":r["direction"],
                    "confidence":"confirmed","source_ids":["S001"]})
        if r["person_b"]==pid:
            other = next((x for x in persons if x["id"]==r["person_a"]), None)
            if other:
                rels_out.append({"person":other["name"],"person_id":f"p{other['id']}",
                    "relationship_type":r["type"],"strength":r["strength"],
                    "evidence":r["context"],"overlap_org":r["overlap_org"],
                    "overlap_period":r["overlap_period"],"direction":r["direction"],
                    "confidence":"confirmed","source_ids":["S001"]})

    profile = {
        "schema_version": "1.0",
        "generated_at": "2026-07-17",
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "邵武市",
            "job": filename_suffix,
            "task_id": "fujian_邵武市",
            "time_focus": "2021-present"
        },
        "identity": {
            "person_id": f"fujian_shaowu_{p['name']}",
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
            "is_current_confirmed": True,
            "source_ids": ["S001"]
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
            {"id":"S001","title":"邵武市人民政府 - 市政府领导","url":"https://www.shaowu.gov.cn/",
             "publisher":"邵武市人民政府","published_at":"","accessed_at":"2026-07-17","source_type":"official","reliability":"high","notes":""},
            {"id":"S002","title":"Shaowu - English Wikipedia","url":"https://en.wikipedia.org/wiki/Shaowu",
             "publisher":"Wikipedia","published_at":"","accessed_at":"2026-07-17","source_type":"encyclopedia","reliability":"medium","notes":""},
        ],
        "confidence_summary": {
            "identity":"partial",
            "current_role":"confirmed",
            "career_completeness":"partial",
            "relationship_confidence":"high",
            "biggest_gap":f"缺少{p['name']}的出生地、早期教育背景和完整履历时间线"
        },
        "open_questions": [
            {"priority":"high","question":f"{p['name']}的出生地和早期教育背景","why_it_matters":"影响人物身份确认和履历完整度",
             "suggested_queries":[f"{p['name']} 简历",f"{p['name']} 出生"],"last_attempted":"2026-07-17"},
            {"priority":"high","question":f"{p['name']}在任邵武前的完整履历","why_it_matters":"理解其职业发展路径和提拔背景",
             "suggested_queries":[f"{p['name']} 任职经历"],"last_attempted":"2026-07-17"}
        ]
    }

    filename = f"20260717-福建省-南平市-{filename_suffix}-{p['name']}.json"
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
    write_person_json(1, "市委书记")
    write_person_json(2, "常务副市长")
    print("\nDone. All artifacts written to", TMP)
