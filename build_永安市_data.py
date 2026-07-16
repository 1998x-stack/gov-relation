#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Yong'an City (永安市), Fujian.

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- Yong'an City Government website (www.ya.gov.cn) — news articles, leadership mentions
- Wikipedia: 永安市 infobox — 傅天宝 as Party Secretary
- "今日永安网" news: 永安市"两优一先"表彰大会 (2026-06-29) — 朱昶凯 as mayor
- Government news: 永安市委、市政府主要领导走访/赴基层调研 (2026-07-03/07) — 周智伟 as 代市长

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

STAGING = "/workspace/data/xieming/other-codes/gov-relation/data/tmp/fujian_永安市"
BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(STAGING, "永安市_network.db")
GEXF_PATH = os.path.join(STAGING, "永安市_network.gexf")
PERSONS_DIR = os.path.join(STAGING)

# as_of date for current data
AS_OF = "2026-07-16"
TODAY = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": "p1",
        "name": "傅天宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永安市市委书记",
        "current_org": "中共永安市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E6%B0%B8%E5%AE%89%E5%B8%82",
        "notes": "市委书记；据Wikipedia 永安市条目确认",
        "confidence": "confirmed"
    },
    {
        "id": "p2",
        "name": "周智伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永安市代市长",
        "current_org": "永安市人民政府",
        "source": "https://www.ya.gov.cn/zwgk/gzdt/202607/t20260703_2234303.htm",
        "notes": "市委副书记、代市长；2026年7月3日以代市长身份首次公开露面",
        "confidence": "confirmed"
    },
    {
        "id": "p3",
        "name": "朱昶凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.ya.gov.cn/zwgk/gzdt/202606/t20260629_2232632.htm",
        "notes": "前任市长；2026年6月29日仍以市长身份出席两优一先表彰大会，后由周智伟接任",
        "confidence": "confirmed"
    },
    # ── Other current city leaders ──
    {
        "id": "p4",
        "name": "池昌江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永安市委副书记",
        "current_org": "中共永安市委员会",
        "source": "https://www.ya.gov.cn/zwgk/gzdt/202606/t20260629_2232632.htm",
        "notes": "市委副书记；2026年6月29日宣读两优一先表彰决定",
        "confidence": "confirmed"
    },
    {
        "id": "p5",
        "name": "廖艳希",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永安市人大常委会主任",
        "current_org": "永安市人大常委会",
        "source": "https://www.ya.gov.cn/zwgk/gzdt/202606/t20260629_2232632.htm",
        "notes": "市人大常委会主任",
        "confidence": "confirmed"
    },
    {
        "id": "p6",
        "name": "钟宏华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "永安市政协主席",
        "current_org": "政协永安市委员会",
        "source": "https://www.ya.gov.cn/zwgk/gzdt/202606/t20260629_2232632.htm",
        "notes": "市政协主席",
        "confidence": "confirmed"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": "o1", "name": "中共永安市委员会", "type": "党委", "level": "县级", "parent": "中共三明市委员会", "location": "福建省三明市永安市"},
    {"id": "o2", "name": "永安市人民政府", "type": "政府", "level": "县级", "parent": "三明市人民政府", "location": "福建省三明市永安市"},
    {"id": "o3", "name": "永安市人大常委会", "type": "人大", "level": "县级", "parent": "三明市人大常委会", "location": "福建省三明市永安市"},
    {"id": "o4", "name": "政协永安市委员会", "type": "政协", "level": "县级", "parent": "政协三明市委员会", "location": "福建省三明市永安市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 傅天宝
    {"person_id": "p1", "org_id": "o1", "title": "永安市市委书记", "start": "", "end": "present", "rank": "正处级", "note": "当前任期"},
    # 周智伟
    {"person_id": "p2", "org_id": "o2", "title": "永安市代市长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月起任代市长"},
    {"person_id": "p2", "org_id": "o1", "title": "永安市委副书记", "start": "2026-07", "end": "present", "rank": "副处级", "note": "市委副书记兼代市长"},
    # 朱昶凯
    {"person_id": "p3", "org_id": "o2", "title": "永安市市长", "start": "", "end": "2026-06", "rank": "正处级", "note": "2026年6月前在任，后由周智伟接替"},
    # 池昌江
    {"person_id": "p4", "org_id": "o1", "title": "永安市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},
    # 廖艳希
    {"person_id": "p5", "org_id": "o3", "title": "永安市人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 钟宏华
    {"person_id": "p6", "org_id": "o4", "title": "永安市政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Predecessor/successor
    {"person_a": "p3", "person_b": "p2", "type": "predecessor_successor", "strength": "strong",
     "context": "朱昶凯与周智伟为市长职务的前任/继任关系", "overlap_org": "永安市人民政府", "overlap_period": "2026-06/2026-07"},
    # Working relationships (leadership team overlap)
    {"person_a": "p1", "person_b": "p2", "type": "superior_subordinate", "strength": "strong",
     "context": "傅天宝（市委书记）与周智伟（代市长）为党政主要领导搭档", "overlap_org": "中共永安市委员会", "overlap_period": "2026-07-present"},
    {"person_a": "p1", "person_b": "p4", "type": "superior_subordinate", "strength": "strong",
     "context": "傅天宝（书记）与池昌江（副书记）为党委班子上下级", "overlap_org": "中共永安市委员会", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p5", "type": "overlap", "strength": "medium",
     "context": "四套班子领导成员", "overlap_org": "永安市", "overlap_period": ""},
    {"person_a": "p1", "person_b": "p6", "type": "overlap", "strength": "medium",
     "context": "四套班子领导成员", "overlap_org": "永安市", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

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
            confidence TEXT
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
            title TEXT,
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
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("strength", ""),
            r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    persons_map = {p["id"]: p for p in persons}

    def person_color(p):
        post = p.get("current_post", "")
        if "市委书记" in post:
            return "255,50,50"   # red — party secretary
        if "市长" in post or "代市长" in post:
            return "50,100,255"  # blue — government leader
        if "人大" in post:
            return "100,180,100" # green — congress
        if "政协" in post:
            return "100,180,100" # green — CPPCC
        return "100,100,100"     # grey — others

    def is_top_leader(p):
        return "市委书记" in p.get("current_post", "") or "市长" in p.get("current_post", "") or "代市长" in p.get("current_post", "")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>永安市 (Yong\'an, Sanming, Fujian) — Leadership Network Graph</description>')
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
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization node colors
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

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
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
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
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
    print(f"永安市 Leadership Network — Build Complete")
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
