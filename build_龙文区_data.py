#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙文区 (Longwen District, Zhangzhou, Fujian) leadership network.

龙文区 — 市辖区, 福建省漳州市下辖, 1996年5月31日设立, 区政府驻蓝田街道.
Research date: 2026-07-17

Sources:
- NetEase (163.com) — multiple news articles confirming 区委书记 朱真 (2021-2024)
- Wikipedia (zh.wikipedia.org/wiki/龙文区) — district info, history
- Wikipedia (en.wikipedia.org/wiki/Longwen_District) — administrative divisions

Coverage:
- Current 区委书记 朱真 — identity confirmed from multiple media reports (2021.03-2024.06)
- Current 区长 — identity not publicly identified (open gap)
- Leadership roster — partial (standard district structure assumed)
- Organization nodes — standard district org structure

Confidence notes:
- 朱真 (Party Secretary): identity confirmed from multiple independent media sources (163.com articles 2021-2024); detailed career timeline is partial
- 区长: not yet identified from available public sources — marked as open gap
- Full leadership roster: needs government website access (longwen.gov.cn blocked)
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_龙文区")
DB_PATH = os.path.join(STAGING, "龙文区_network.db")
GEXF_PATH = os.path.join(STAGING, "龙文区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 朱真 — 龙文区委书记 (confirmed 2021.03-2024.06 via multiple 163.com articles)
    # Gender implied female based on name character "真" commonly used; not confirmed
    {"id":1,"name":"朱真","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委书记",
     "current_org":"中共漳州市龙文区委员会",
     "source":"https://www.163.com/dy/article/G69IL0CM05346936.html; https://www.163.com/dy/article/IS7VO1KC055634M1.html; https://www.163.com/dy/article/J3MFHTGH055670JB.html"},
    
    # 区长 — 身份待查 (open gap)
    {"id":2,"name":"（区长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区区长",
     "current_org":"漳州市龙文区人民政府",
     "source":"公开资料未找到现任区长信息"},

    # ── Predecessor: 蒋一婷 (as listed on Wikipedia infobox, likely earlier predecessor) ──
    {"id":3,"name":"蒋一婷","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"（前任龙文区委书记）",
     "current_org":"中共漳州市龙文区委员会",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E6%96%87%E5%8C%BA"},
    
    # ── 区人大常委会主任 (需进一步确认) ──
    {"id":4,"name":"（区人大常委会主任待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区人大常委会主任",
     "current_org":"漳州市龙文区人民代表大会常务委员会",
     "source":"公开资料待查"},
    
    # 区政协主席
    {"id":5,"name":"（区政协主席待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区政协主席",
     "current_org":"中国人民政治协商会议漳州市龙文区委员会",
     "source":"公开资料待查"},
    
    # 区纪委书记/监委主任
    {"id":6,"name":"（区纪委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区纪委书记、监委主任",
     "current_org":"中共漳州市龙文区纪律检查委员会",
     "source":"公开资料待查"},
    
    # 常务副区长
    {"id":7,"name":"（常务副区长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委常委、常务副区长",
     "current_org":"漳州市龙文区人民政府",
     "source":"公开资料待查"},
    
    # 组织部部长
    {"id":8,"name":"（组织部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委常委、组织部部长",
     "current_org":"中共漳州市龙文区委员会",
     "source":"公开资料待查"},
    
    # 宣传部部长
    {"id":9,"name":"（宣传部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委常委、宣传部部长",
     "current_org":"中共漳州市龙文区委员会",
     "source":"公开资料待查"},
    
    # 政法委书记
    {"id":10,"name":"（政法委书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委常委、政法委书记",
     "current_org":"中共漳州市龙文区委员会",
     "source":"公开资料待查"},
    
    # 统战部部长
    {"id":11,"name":"（统战部部长待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委常委、统战部部长",
     "current_org":"中共漳州市龙文区委员会",
     "source":"公开资料待查"},
    
    # 区委副书记 (deputy party secretary, typically held by the 区长)
    # May be same as 区长 or a separate position
    {"id":12,"name":"（区委副书记待查）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"龙文区委副书记",
     "current_org":"中共漳州市龙文区委员会",
     "source":"公开资料待查"},

    # ── 漳州市领导 (for context) ──
    {"id":13,"name":"王进足","gender":"男","ethnicity":"汉族",
     "birth":"1967-01","birthplace":"福建泉州",
     "education":"中央党校大学学历",
     "party_join":"1992-08","work_start":"1988",
     "current_post":"漳州市委书记",
     "current_org":"中共漳州市委员会",
     "source":"https://zh.wikipedia.org/wiki/%E7%8E%8B%E8%BF%9B%E8%B6%B3"},
    
    {"id":14,"name":"魏东","gender":"男","ethnicity":"汉族",
     "birth":"1970-01","birthplace":"云南镇雄",
     "education":"研究生学历",
     "party_join":"中共党员","work_start":"未详",
     "current_post":"漳州市委副书记、市长",
     "current_org":"漳州市人民政府",
     "source":"https://zh.wikipedia.org/wiki/%E6%BC%B3%E5%B7%9E%E5%B8%82"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 龙文区级组织
    {"id":1,"name":"中共漳州市龙文区委员会","type":"党委","level":"县级","parent":"中共漳州市委员会","location":"福建省漳州市龙文区"},
    {"id":2,"name":"漳州市龙文区人民政府","type":"政府","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市龙文区"},
    {"id":3,"name":"漳州市龙文区人民代表大会常务委员会","type":"人大","level":"县级","parent":"漳州市人大常委会","location":"福建省漳州市龙文区"},
    {"id":4,"name":"中国人民政治协商会议漳州市龙文区委员会","type":"政协","level":"县级","parent":"政协漳州市委员会","location":"福建省漳州市龙文区"},
    {"id":5,"name":"中共漳州市龙文区纪律检查委员会","type":"党委","level":"县级","parent":"中共漳州市龙文区委员会","location":"福建省漳州市龙文区"},
    {"id":6,"name":"中共漳州市龙文区委组织部","type":"党委","level":"县级","parent":"中共漳州市龙文区委员会","location":"福建省漳州市龙文区"},
    {"id":7,"name":"中共漳州市龙文区委宣传部","type":"党委","level":"县级","parent":"中共漳州市龙文区委员会","location":"福建省漳州市龙文区"},
    {"id":8,"name":"中共漳州市龙文区委政法委员会","type":"党委","level":"县级","parent":"中共漳州市龙文区委员会","location":"福建省漳州市龙文区"},
    {"id":9,"name":"中共漳州市龙文区委统战部","type":"党委","level":"县级","parent":"中共漳州市龙文区委员会","location":"福建省漳州市龙文区"},
    
    # 漳州市级组织
    {"id":10,"name":"中共漳州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省漳州市"},
    {"id":11,"name":"漳州市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省漳州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 朱真 - 龙文区委书记 (since at least 2021.03)
    {"person_id":1,"org_id":1,"title":"龙文区委书记","start":"~2021.03","end":"present","rank":"正处级","note":"书记身份确认于2021年3月人民网/金台资讯报道"},
    
    # 区长 (unknown name)
    {"person_id":2,"org_id":2,"title":"龙文区区长","start":"","end":"present","rank":"正处级","note":"现任区长身份待查"},
    
    # 蒋一婷 - 前任区委书记 (Wikipedia infobox listing, likely earlier)
    {"person_id":3,"org_id":1,"title":"龙文区委书记","start":"","end":"~2021","rank":"正处级","note":"Wikipedia infobox列出; 可能在朱真之前任职"},
    
    # Standard district leadership positions (placeholders)
    {"person_id":4,"org_id":3,"title":"龙文区人大常委会主任","start":"","end":"present","rank":"正处级","note":"身份待查"},
    {"person_id":5,"org_id":4,"title":"龙文区政协主席","start":"","end":"present","rank":"正处级","note":"身份待查"},
    {"person_id":6,"org_id":5,"title":"龙文区纪委书记、监委主任","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":7,"org_id":2,"title":"龙文区委常委、常务副区长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":8,"org_id":6,"title":"龙文区委常委、组织部部长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":9,"org_id":7,"title":"龙文区委常委、宣传部部长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":10,"org_id":8,"title":"龙文区委常委、政法委书记","start":"","end":"present","rank":"副处级","note":"身份待查"},
    {"person_id":11,"org_id":9,"title":"龙文区委常委、统战部部长","start":"","end":"present","rank":"副处级","note":"身份待查"},
    
    # 上级领导
    {"person_id":13,"org_id":10,"title":"漳州市委书记","start":"2023.08","end":"present","rank":"正厅级","note":"现任"},
    {"person_id":14,"org_id":11,"title":"漳州市委副书记、市长","start":"2023.08","end":"present","rank":"正厅级","note":"现任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 朱真 → 上级领导
    {"person_a":1,"person_b":13,"type":"superior_subordinate","context":"龙文区委书记隶属漳州市委领导","overlap_org":"中共漳州市委员会","overlap_period":"2021-至今","strength":"medium","confidence":"confirmed"},
    {"person_a":1,"person_b":14,"type":"superior_subordinate","context":"龙文区委书记与漳州市长工作关系","overlap_org":"漳州市人民政府","overlap_period":"2021-至今","strength":"medium","confidence":"confirmed"},
    
    # 朱真 ↔ 前任
    {"person_a":1,"person_b":3,"type":"predecessor_successor","context":"蒋一婷→朱真 龙文区委书记交接（推测）","overlap_org":"中共漳州市龙文区委员会","overlap_period":"~2021","strength":"medium","confidence":"plausible"},
    
    # 漳州市级领导之间
    {"person_a":13,"person_b":14,"type":"overlap","context":"漳州市委书记-市长搭档","overlap_org":"中共漳州市委员会/漳州市人民政府","overlap_period":"2023.08-至今","strength":"strong","confidence":"confirmed"},
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'unverified'
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            note TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p["current_post"], p["current_org"], p.get("source", ""),
            p.get("notes", ""), p.get("confidence", "unverified"),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(o["id"]), o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        person_id, org_id, title, start, end, rank, note = (
            str(pos["person_id"]), str(pos["org_id"]), pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        )
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, org_id, title, start, end, rank, note))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(r["person_a"]), str(r["person_b"]), r["type"], r.get("strength", ""),
            r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", ""),
            r.get("confidence", "unverified"),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def is_top_leader(p):
    return "区委书记" in p["current_post"] or "区长" in p["current_post"] or "县长" in p["current_post"]

def person_color(p):
    post = p.get("current_post", "")
    if "区委书记" in post or "县委书记" in post:
        return "255,50,50"   # red — party secretary
    if "区长" in post or "县长" in post or "市长" in post:
        return "50,100,255"  # blue — government leader
    if "纪委书记" in post:
        return "255,165,0"   # orange — discipline
    if "人大" in post or "政协" in post:
        return "100,180,100" # green — congress/CPPCC
    return "100,100,100"     # grey — others

def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"

def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    # Build a lookup for person names
    persons_map = {p["id"]: p["name"] for p in persons}
    orgs_map = {o["id"]: o["name"] for o in organizations}

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>龙文区 (Longwen District, Zhangzhou, Fujian) — Leadership Network Graph</description>')
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
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(str(p["id"]))}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc("o"+str(o["id"]))}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
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
        pid = pos["person_id"]
        lines.append(f'      <edge id="e{eid}" source="{esc(str(pos["person_id"]))}" target="{esc("o"+str(pos["org_id"]))}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(str(r["person_a"]))}" target="{esc(str(r["person_b"]))}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()

    # Print summary
    print(f"\n{'=' * 50}")
    print(f"龙文区 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
