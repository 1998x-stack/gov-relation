#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乡城县 (Xiangcheng County, Sichuan) leadership network."""
import sqlite3
import os, sys
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(STAGING))
DB_PATH = os.path.join(STAGING, "乡城县_network.db")
GEXF_PATH = os.path.join(STAGING, "乡城县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════
    # Top Leaders: Party Secretary & County Mayor
    # ═══════════════════════════════════════════════════════════════
    {"id": 1, "name": "杨林", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘孜州政府党组成员、副州长（提名），乡城县委书记",
     "current_org": "中共乡城县委员会",
     "source": "http://www.xcx.gov.cn/xcxx/article/724415"},

    {"id": 2, "name": "尼玛西日", "gender": "男", "ethnicity": "藏族",
     "birth": "1975-02", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县委副书记、县长、党组书记",
     "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    # ═══════════════════════════════════════════════════════════════
    # County Party Leadership (县委领导)
    # ═══════════════════════════════════════════════════════════════
    {"id": 3, "name": "降拥尼玛", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县委副书记", "current_org": "中共乡城县委员会",
     "source": "http://www.xcx.gov.cn/xcxx/article/724415"},

    # ═══════════════════════════════════════════════════════════════
    # Government Leadership (县政府)
    # ═══════════════════════════════════════════════════════════════
    {"id": 4, "name": "黄万明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县委常委、常务副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 5, "name": "陈文铭", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县委常委、副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 6, "name": "郎佳宁", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县委常委、副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 7, "name": "徐启良", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县委常委、副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 8, "name": "李辉", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 9, "name": "徐鑫", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 10, "name": "生龙降措", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 11, "name": "杨薇", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    {"id": 12, "name": "杨成", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县副县长", "current_org": "乡城县人民政府",
     "source": "http://www.xcx.gov.cn/ldzc"},

    # ═══════════════════════════════════════════════════════════════
    # People's Congress & CPPCC (人大、政协)
    # ═══════════════════════════════════════════════════════════════
    {"id": 13, "name": "李新", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县人大常委会主任", "current_org": "乡城县人民代表大会",
     "source": "http://www.xcx.gov.cn/xcxx/article/724415"},

    {"id": 14, "name": "达尔比", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "乡城县政协主席", "current_org": "中国人民政治协商会议乡城县委员会",
     "source": "http://www.xcx.gov.cn/xcxx/article/724415"},
]

organizations = [
    {"id": 1, "name": "中共乡城县委员会", "type": "党委", "level": "县处级",
     "parent": "中共甘孜藏族自治州委员会", "location": "四川省甘孜州乡城县"},
    {"id": 2, "name": "乡城县人民政府", "type": "政府", "level": "县处级",
     "parent": "甘孜藏族自治州人民政府", "location": "四川省甘孜州乡城县"},
    {"id": 3, "name": "乡城县人民代表大会", "type": "人大", "level": "县处级",
     "parent": "甘孜藏族自治州人民代表大会", "location": "四川省甘孜州乡城县"},
    {"id": 4, "name": "中国人民政治协商会议乡城县委员会", "type": "政协", "level": "县处级",
     "parent": "政协甘孜藏族自治州委员会", "location": "四川省甘孜州乡城县"},
    {"id": 5, "name": "甘孜藏族自治州人民政府", "type": "政府", "level": "地厅级",
     "parent": "四川省人民政府", "location": "四川省甘孜州康定市"},
]

positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "乡城县委书记", "start": "", "end": "present",
     "rank": "县处级正职", "note": "同时担任甘孜州政府党组成员、副州长（提名）"},
    # County Mayor
    {"person_id": 2, "org_id": 2, "title": "乡城县委副书记、县长", "start": "", "end": "present",
     "rank": "县处级正职", "note": "县政府党组书记"},
    # Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "乡城县委副书记", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    # Deputies
    {"person_id": 4, "org_id": 2, "title": "乡城县委常委、常务副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "乡城县委常委、副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "乡城县委常委、副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "乡城县委常委、副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "乡城县副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "乡城县副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "乡城县副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "乡城县副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "乡城县副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    # People's Congress
    {"person_id": 13, "org_id": 3, "title": "乡城县人大常委会主任", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},
    # CPPCC
    {"person_id": 14, "org_id": 4, "title": "乡城县政协主席", "start": "", "end": "present",
     "rank": "县处级正职", "note": ""},
    # Party Secretary's concurrent state role
    {"person_id": 1, "org_id": 5, "title": "甘孜州人民政府党组成员、副州长（提名）", "start": "", "end": "present",
     "rank": "副厅级", "note": "兼职"},
]

relationships = [
    # Executive team - same organization overlap
    {"person_a": 1, "person_b": 2, "type": "top_leader_overlap",
     "context": "杨林（县委书记）与尼玛西日（县长）为乡城县党政主要领导搭档",
     "overlap_org": "中共乡城县委员会/乡城县人民政府",
     "overlap_period": "current"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县政府主要领导与常务副县长工作搭档",
     "overlap_org": "乡城县人民政府",
     "overlap_period": "current"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与分管副县长工作关系",
     "overlap_org": "乡城县人民政府",
     "overlap_period": "current"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记工作搭档",
     "overlap_org": "中共乡城县委员会",
     "overlap_period": "current"},
    {"person_a": 1, "person_b": 13, "type": "same_standing_committee",
     "context": "县委与县人大主要领导协同工作",
     "overlap_org": "中共乡城县委员会/乡城县人民代表大会",
     "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "government_consultation",
     "context": "县长与政协主席工作沟通",
     "overlap_org": "乡城县人民政府/政协乡城县委员会",
     "overlap_period": "current"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委主要领导与县委常委、副县长",
     "overlap_org": "中共乡城县委员会/乡城县人民政府",
     "overlap_period": "current"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委主要领导与县委常委、副县长",
     "overlap_org": "中共乡城县委员会/乡城县人民政府",
     "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委主要领导与县委常委、副县长",
     "overlap_org": "中共乡城县委员会/乡城县人民政府",
     "overlap_period": "current"},
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH}")


def build_gexf():
    lines = []
    now = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>乡城县领导班子工作关系网络 - Xiangcheng County leadership network</description>')
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
    lines.append('    </attributes>')

    # Person node color by role
    def person_color(p):
        title = p["current_post"]
        if "书记" in title and "副" not in title:
            return "255,50,50"  # Red - Party Secretary
        if "县长" in title and "副" not in title:
            return "50,100,255"  # Blue - County Mayor
        if "常务副" in title:
            return "50,100,255"  # Blue - senior deputy
        if "常委" in title:
            return "80,130,255"  # Lighter blue
        if "人大" in title:
            return "200,255,255"  # Cyan - People's Congress
        if "政协" in title:
            return "255,240,200"  # Cream - CPPCC
        return "100,100,100"  # Grey - others

    def is_top_leader(p):
        return p["current_post"].startswith("乡城县委书记") or p["current_post"].startswith(("乡城县委副书记、县长"))

    def org_color(o):
        m = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
             "政协": "255,240,200", "事业单位": "220,220,220"}
        return m.get(o["type"], "200,200,200")

    eid = 0

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("15.0" if p["id"] in (3, 4, 13, 14) else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    seen_edges = set()
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for r in relationships:
        eid += 1
        key = tuple(sorted((r["person_a"], r["person_b"])))
        if key in seen_edges:
            continue
        seen_edges.add(key)
        w = "2.0" if r["type"] in ("top_substr_overlap",) else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    print("Building 乡城县 leadership network...")
    build_db()
    build_gexf()
    print("Done.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")