#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 兰坪白族普米族自治县 leadership network."""
import sqlite3
import os
from datetime import datetime

STAGING = "/workspace/data/xieming/other-codes/gov-relation/data/tmp/yunnan_兰坪白族普米族自治县"
DB_PATH = os.path.join(STAGING, "兰坪白族普米族自治县_network.db")
GEXF_PATH = os.path.join(STAGING, "兰坪白族普米族自治县_network.gexf")

# ── Persons ──

persons = [
    # ═══════ County Party Committee (县委) ═══════
    {"id": 1, "name": "张竞超", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共兰坪白族普米族自治县委书记",
     "current_org": "中共兰坪白族普米族自治县委员会",
     "source": "https://www.lanping.gov.cn/2026/0716/1874.html"},

    {"id": 2, "name": "和庚全", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委副书记",
     "current_org": "中共兰坪白族普米族自治县委员会",
     "source": "https://www.lanping.gov.cn/2026/0401/1849.html"},

    {"id": 3, "name": "寸利山", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委副书记",
     "current_org": "中共兰坪白族普米族自治县委员会",
     "source": "https://www.lanping.gov.cn/2026/0716/1874.html"},

    {"id": 4, "name": "李文东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委常委、县纪委书记、县监委主任",
     "current_org": "中共兰坪白族普米族自治县纪律检查委员会",
     "source": "https://www.lanping.gov.cn/2026/0401/1849.html"},

    {"id": 5, "name": "张艺缤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委常委、组织部部长、县委党校校长",
     "current_org": "中共兰坪白族普米族自治县委员会组织部",
     "source": "https://www.lanping.gov.cn/2026/0706/1872.html"},

    {"id": 6, "name": "肖叶琳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委常委、宣传部部长",
     "current_org": "中共兰坪白族普米族自治县委员会宣传部",
     "source": "https://www.lanping.gov.cn/2025/1113/1799.html"},

    {"id": 7, "name": "和磊域", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委常委、副县长候选人",
     "current_org": "兰坪白族普米族自治县人民政府",
     "source": "https://www.lanping.gov.cn/2026/0608/1862.html"},

    # ═══════════ Government Leaders ═══════════
    {"id": 8, "name": "和春梅", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县委副书记、县长",
     "current_org": "兰坪白族普米族自治县人民政府",
     "source": "https://www.lanping.gov.cn/2026/0716/1874.html"},

    {"id": 9, "name": "余金成", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县人民政府副县长",
     "current_org": "兰坪白族普米族自治县人民政府",
     "source": "https://www.lanping.gov.cn/2026/0608/1862.html"},

    {"id": 10, "name": "简崇云", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县人民政府副县长",
     "current_org": "兰坪白族普米族自治县人民政府",
     "source": "https://www.lanping.gov.cn/2026/0608/1862.html"},

    {"id": 11, "name": "和仕俊", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县人民政府副县长",
     "current_org": "兰坪白族普米族自治县人民政府",
     "source": "https://www.lanping.gov.cn/2026/0608/1862.html"},

    {"id": 12, "name": "何志昌", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县人民政府副县长候选人、公安局局长",
     "current_org": "兰坪白族普米族自治县公安局",
     "source": "https://www.lanping.gov.cn/2026/0608/1862.html"},

    # ═══════════ People's Congress ═══════════
    {"id": 13, "name": "李铁嵘", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县人大常委会主任",
     "current_org": "兰坪白族普米族自治县人大常委会",
     "source": "https://www.lanping.gov.cn/2026/0716/1874.html"},

    # ═══════════ Industrial Park ═══════════
    {"id": 14, "name": "李翼鸿", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "云南兰坪产业园区党工委副书记、管委会常务副主任",
     "current_org": "云南兰坪产业园区",
     "source": "https://www.lanping.gov.cn/2026/0716/1874.html"},

    # ═══════════ Other County Leaders ═══════════
    {"id": 15, "name": "杨君", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县领导",
     "current_org": "兰坪县",
     "source": "https://www.lanping.gov.cn/2025/1127/1807.html"},

    {"id": 16, "name": "李金奎", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县领导",
     "current_org": "兰坪县",
     "source": "https://www.lanping.gov.cn/2025/1127/1807.html"},

    {"id": 17, "name": "和云", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县领导",
     "current_org": "兰坪县",
     "source": "https://www.lanping.gov.cn/2025/1127/1807.html"},

    {"id": 18, "name": "杨四红", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县领导",
     "current_org": "兰坪县",
     "source": "https://www.lanping.gov.cn/2025/1127/1807.html"},

    {"id": 19, "name": "刘慧海", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县领导",
     "current_org": "兰坪县",
     "source": "https://www.lanping.gov.cn/2025/1127/1807.html"},

    {"id": 20, "name": "张耀明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "兰坪县领导",
     "current_org": "兰坪县",
     "source": "https://www.lanping.gov.cn/2025/1127/1807.html"},
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共兰坪白族普米族自治县委员会", "type": "党委", "level": "县", "parent": "中共怒江傈僳族自治州委员会", "location": "兰坪县"},
    {"id": 2, "name": "中共兰坪县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共兰坪白族普米族自治县委员会", "location": "兰坪县"},
    {"id": 3, "name": "中共兰坪县委组织部", "type": "党委", "level": "县", "parent": "中共兰坪白族普米族自治县委员会", "location": "兰坪县"},
    {"id": 4, "name": "中共兰坪县委宣传部", "type": "党委", "level": "县", "parent": "中共兰坪白族普米族自治县委员会", "location": "兰坪县"},
    {"id": 5, "name": "兰坪白族普米族自治县人民政府", "type": "政府", "level": "县", "parent": "怒江傈僳族自治州人民政府", "location": "兰坪县"},
    {"id": 6, "name": "兰坪白族普米族自治县公安局", "type": "政府", "level": "县", "parent": "兰坪白族普米族自治县人民政府", "location": "兰坪县"},
    {"id": 7, "name": "兰坪白族普米族自治县人大常委会", "type": "人大", "level": "县", "parent": "怒江傈僳族自治州人大常委会", "location": "兰坪县"},
    {"id": 8, "name": "云南兰坪产业园区", "type": "开发区", "level": "县", "parent": "兰坪白族普米族自治县人民政府", "location": "兰坪县"},
    {"id": 9, "name": "中共兰坪县委政法委", "type": "党委", "level": "县", "parent": "中共兰坪白族普米族自治县委员会", "location": "兰坪县"},
]

# ── Positions ──

positions = [
    # Party Committee
    {"person_id": 1, "org_id": 1, "title": "兰坪县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "十三届县委"},
    {"person_id": 2, "org_id": 1, "title": "兰坪县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "also 县委教育工委书记"},
    {"person_id": 3, "org_id": 1, "title": "兰坪县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "兰坪县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "兰坪县委常委、组织部部长、县委党校校长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "兰坪县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # Government
    {"person_id": 8, "org_id": 5, "title": "兰坪县委副书记、县长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "兰坪县委常委、副县长候选人", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "兰坪县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "兰坪县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "兰坪县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "兰坪县副县长候选人、公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # NPC
    {"person_id": 13, "org_id": 7, "title": "兰坪县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # Industrial Park
    {"person_id": 14, "org_id": 8, "title": "云南兰坪产业园区党工委副书记、管委会常务副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── Relationships ──

relationships = [
    # Core leadership team - same organization overlap
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共兰坪白族普米族自治县委员会/兰坪县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与副书记", "overlap_org": "中共兰坪白族普米族自治县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与副书记", "overlap_org": "中共兰坪白族普米族自治县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共兰坪白族普米族自治县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共兰坪白族普米族自治县委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与宣传部部长", "overlap_org": "中共兰坪白族普米族自治县委员会", "overlap_period": "2025-至今"},
    {"person_a": 8, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长候选人", "overlap_org": "兰坪白族普米族自治县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 8, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "兰坪白族普米族自治县人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "兰坪白族普米族自治县人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "兰坪白族普米族自治县人民政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 1, "type": "overlap", "context": "县人大常委会主任与县委书记同届", "overlap_org": "兰坪县", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "两位副书记共事", "overlap_org": "中共兰坪白族普米族自治县委员会", "overlap_period": ""},
]

# ── Build ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""CREATE TABLE persons (
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
    )""")

    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    )""")

    cur.execute("""CREATE TABLE positions (
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
    )""")

    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    cols = ["id","name","gender","ethnicity","birth","birthplace","education","party_join","work_start","current_post","current_org","source"]
    for p in persons:
        values = [p.get(c, "") for c in cols]
        cur.execute(f"INSERT INTO persons ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", values)

    ocols = ["id","name","type","level","parent","location"]
    for o in organizations:
        values = [o.get(c, "") for c in ocols]
        cur.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join(['?']*len(ocols))})", values)

    pcols = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        values = [pos.get(c, "") for c in pcols]
        cur.execute(f"INSERT INTO positions ({','.join(pcols)}) VALUES ({','.join(['?']*len(pcols))})", values)

    rcols = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        values = [r.get(c, "") for c in rcols]
        cur.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join(['?']*len(rcols))})", values)

    conn.commit()
    conn.close()
    print(f"DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def person_color(post):
    if "书记" in post and "副" not in post:
        return "200,30,30"
    elif "县长" in post and "副" not in post:
        return "30,100,200"
    elif "副书记" in post:
        return "220,80,80"
    elif "副" in post or "候选人" in post:
        return "100,150,220"
    elif "常委" in post:
        return "180,100,180"
    elif "主任" in post:
        return "60,180,60"
    else:
        return "100,100,100"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>兰坪白族普米族自治县领导班子的工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        r, g, b = c.split(",")
        is_top = any(kw in p.get("current_post", "") for kw in ["县委书记", "副书记、县长", "县长"])
        sz = "20.0" if (p["id"] in [1, 8]) else "12.0"
        pid = p["id"]
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {len(persons)} person nodes, {len(organizations)} org nodes, {eid} edges")

if __name__ == "__main__":
    person_color = lambda post: (
        "200,30,30" if "省委书记" in post or ("书记" in post and "副" not in post and "委" in post)
        else "220,80,80" if "副" in post and "书记" in post
        else "30,100,200" if "县长" in post and "副" not in post
        else "100,150,220" if "副" in post
        else "180,100,180" if "常委" in post or "委员" in post
        else "60,180,60" if "主任" in post or "组长" in post
        else "100,100,100"
    )
    build_db()
    build_gexf()
    print("Build complete.")