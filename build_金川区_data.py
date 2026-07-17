#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Jinchuan District (金川区), Jinchang, Gansu.

金川区 — 甘肃省金昌市下辖的市辖区，金昌市政治经济文化中心，镍都核心区。
Covers current district leaders (区委书记 and 区长), their predecessors,
key deputies, and relationship network.

Based on:
- 金昌市 build script (李生虎 as 金川区委书记, recognized from https://www.jinchang.gov.cn)
- Wikipedia/Jinchang
- TODO task gansu_金川区
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_金川区")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "金川区_network.db")
GEXF_PATH = os.path.join(TMP, "金川区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # -- A. Current Top Leaders --
    # 李生虎 — 金川区委书记 (as of 2024, referenced from build_金昌市_data.py)
    {"id": 1, "name": "李生虎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "金川区委书记",
     "current_org": "中共金川区委员会",
     "source": "https://github.com/xieming/gov-relation/blob/main/build_金昌市_data.py"},

    # 金川区区长 — 待确认
    # The district mayor (区长) name could not be confirmed from available sources.
    # Potential candidates from public records need verification.
    # Marked as unknown with plausible alternatives.
    {"id": 2, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "金川区区长",
     "current_org": "金川区人民政府",
     "source": ""},

    # -- B. Previous Leaders (区委书记 predecessors) --
    # 王方太 — 曾任金川区委书记, 后任金昌市长→市委书记
    {"id": 3, "name": "王方太", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-02", "birthplace": "甘肃天水",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "金昌市委书记（原金川区委书记/金昌市长）",
     "current_org": "中共金昌市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%87%91%E6%98%8C%E5%B8%82"},

    # 王钧 — 曾任金川区委书记(or 金昌副市长), 后任金昌市长→书记→副省长
    # Note: 王钧's district-level role needs verification
    {"id": 4, "name": "王钧", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-02", "birthplace": "甘肃陇南",
     "education": "西北师范大学",
     "party_join": "1992-06", "work_start": "",
     "current_post": "甘肃省副省长（原金昌市委书记/市长）",
     "current_org": "甘肃省人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E9%92%A7_(1971%E5%B9%B4)"},

    # -- C. Standing Committee Members / Key Deputies --
    # 金川区纪委书记
    {"id": 5, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "金川区委常委、纪委书记",
     "current_org": "中共金川区纪律检查委员会",
     "source": ""},

    # 金川区委组织部部长
    {"id": 6, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "金川区委常委、组织部部长",
     "current_org": "中共金川区委员会",
     "source": ""},

    # 金川区人大常委会主任
    {"id": 7, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "金川区人大常委会主任",
     "current_org": "金川区人民代表大会常务委员会",
     "source": ""},

    # 金川区政协主席
    {"id": 8, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "金川区政协主席",
     "current_org": "中国人民政治协商会议金川区委员会",
     "source": ""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 金川区级核心
    {"id": 1, "name": "中共金川区委员会", "type": "党委", "level": "县级",
     "parent": "中共金昌市委员会", "location": "甘肃省金昌市金川区"},
    {"id": 2, "name": "金川区人民政府", "type": "政府", "level": "县级",
     "parent": "金昌市人民政府", "location": "甘肃省金昌市金川区"},
    {"id": 3, "name": "金川区人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "金昌市人大常委会", "location": "甘肃省金昌市金川区"},
    {"id": 4, "name": "中国人民政治协商会议金川区委员会", "type": "政协", "level": "县级",
     "parent": "金昌市政协", "location": "甘肃省金昌市金川区"},
    {"id": 5, "name": "中共金川区纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共金川区委员会", "location": "甘肃省金昌市金川区"},

    # 上级组织
    {"id": 6, "name": "中共金昌市委员会", "type": "党委", "level": "地级",
     "parent": "中共甘肃省委员会", "location": "甘肃省金昌市金川区"},
    {"id": 7, "name": "金昌市人民政府", "type": "政府", "level": "地级",
     "parent": "甘肃省人民政府", "location": "甘肃省金昌市金川区"},
    {"id": 8, "name": "甘肃省人民政府", "type": "政府", "level": "省级",
     "parent": "", "location": "甘肃省兰州市"},

    # 下辖乡镇街道
    {"id": 9, "name": "金川区广州路街道办事处", "type": "乡镇/街道", "level": "乡科级",
     "parent": "金川区人民政府", "location": "甘肃省金昌市金川区"},
    {"id": 10, "name": "金川区宁远堡镇人民政府", "type": "乡镇/街道", "level": "乡科级",
     "parent": "金川区人民政府", "location": "甘肃省金昌市金川区"},
    {"id": 11, "name": "金川区双湾镇人民政府", "type": "乡镇/街道", "level": "乡科级",
     "parent": "金川区人民政府", "location": "甘肃省金昌市金川区"},

    # 重要地方企业
    {"id": 12, "name": "金川集团股份有限公司", "type": "事业单位", "level": "地级",
     "parent": "甘肃省人民政府", "location": "甘肃省金昌市金川区"},
]

# =========================================================================
# POSITIONS (career timeline edges)
# =========================================================================
positions = [
    # 李生虎 — 金川区委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "金川区委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "当前任职，上任日期待确认"},

    # 王方太 — 曾任金川区委书记
    {"id": 2, "person_id": 3, "org_id": 1, "title": "金川区委书记",
     "start": "", "end": "", "rank": "正县级", "note": "曾任，具体任期待查"},
    {"id": 3, "person_id": 3, "org_id": 7, "title": "金昌市人民政府市长",
     "start": "2021-07", "end": "2024-07", "rank": "正厅级", "note": "后任市委书记"},
    {"id": 4, "person_id": 3, "org_id": 6, "title": "金昌市委书记",
     "start": "2024-07", "end": "present", "rank": "正厅级", "note": ""},

    # 王钧 — 金昌市层面领导 (district role待确认)
    {"id": 5, "person_id": 4, "org_id": 7, "title": "金昌市人民政府市长",
     "start": "2020-09", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"id": 6, "person_id": 4, "org_id": 6, "title": "金昌市委书记",
     "start": "2021-07", "end": "2024-07", "rank": "正厅级", "note": ""},
    {"id": 7, "person_id": 4, "org_id": 8, "title": "甘肃省副省长",
     "start": "2024-07", "end": "present", "rank": "副省级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 李生虎 ← → 王方太: 区委书记继任关系 (plausible, based on timeline)
    {"id": 1, "person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "李生虎接任王方太金川区委书记（推测，王方太2021年升任金昌市长后由李生虎接任区委书记）",
     "overlap_org": "中共金川区委员会", "overlap_period": "",
     "confidence": "plausible"},

    # 王方太 ← → 王钧: 金昌市委层面继任
    {"id": 2, "person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "王钧→王方太: 王钧2024年升副省长，王方太接任金昌市委书记",
     "overlap_org": "中共金昌市委员会", "overlap_period": "2024-07",
     "confidence": "confirmed"},
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    current = p.get("current_post", "")
    is_party_sec = ("书记" in current and "副" not in current.split("书记")[0])
    is_gov_head = ("区长" in current and "副" not in current) or ("市长" in current and "副" not in current)
    is_discipline = "纪委书记" in current or "监委" in current
    if is_party_sec:
        return "255,50,50"
    elif is_gov_head:
        return "50,100,255"
    elif is_discipline:
        return "255,165,0"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(p):
    current = p.get("current_post", "")
    key_roles = ["区委书记", "区长", "市委书记", "市长"]
    for role in key_roles:
        if role in current and "副" not in current.split(role)[0]:
            return True
    return False

# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
                   p.get("birth",""), p.get("birthplace",""), p.get("education",""),
                   p.get("party_join",""), p.get("work_start",""),
                   p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o.get("type",""), o.get("level",""),
                   o.get("parent",""), o.get("location","")))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start",""), pos.get("end",""), pos.get("rank",""),
                   pos.get("note","")))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r.get("context",""), r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")


# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>金川区领导关系网络 - Jinchuan District Leadership Network (Jinchang, Gansu)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship), weight="2.0"
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
