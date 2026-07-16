#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙海区 (Longhai District, Zhangzhou, Fujian) leadership network.

龙海区 — 市辖区, 福建省漳州市下辖, 2021年2月2日撤市设区, 区政府驻石码街道.
Research date: 2026-07-16

Sources:
- Baidu Baike (baike.baidu.com/item/龙海区) — leadership table, political section, district overview
- Wikipedia (zh.wikipedia.org/wiki/龙海区) — district info, infobox leadership

Coverage:
- Current top 2 leaders: 区委书记 叶毓, 区长 陈艺章
- 区人大常委会主任 林文生, 区政协主席 洪海涛
- Standard district organization nodes
- Key administrative divisions

Confidence notes:
- 叶毓 (Party Secretary): identity confirmed from Wikipedia infobox and Baidu Baike political section
- 陈艺章 (District Mayor): identity confirmed from Baidu Baike political section
- 林文生 (人大主任): identity confirmed from Baidu Baike political section
- 洪海涛 (政协主席): identity confirmed from Baidu Baike political section
- Detailed career timelines for all figures are open gaps — public biographical pages were not accessible at time of research
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_龙海区")
DB_PATH = os.path.join(STAGING, "龙海区_network.db")
GEXF_PATH = os.path.join(STAGING, "龙海区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 叶毓 — 龙海区委书记 (confirmed via Wikipedia infobox and Baidu Baike)
    {"id":"p1","name":"叶毓","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"龙海区委书记",
     "current_org":"中共漳州市龙海区委员会",
     "source":"https://zh.wikipedia.org/wiki/%E9%BE%99%E6%B5%B7%E5%8C%BA",
     "notes":"区委书记，具体出生年月、籍贯、教育背景、入党/工作时间待查。Baidu Baike个人页面无法访问。",
     "confidence":"unverified"},

    # 陈艺章 — 龙海区委副书记、区长 (confirmed via Baidu Baike political section)
    {"id":"p2","name":"陈艺章","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"龙海区委副书记、区长",
     "current_org":"漳州市龙海区人民政府",
     "source":"https://baike.baidu.com/item/%E9%BE%99%E6%B5%B7%E5%8C%BA",
     "notes":"区委副书记、区长，具体出生年月、籍贯、教育背景、入党/工作时间待查。",
     "confidence":"unverified"},

    # 林文生 — 区人大常委会主任 (confirmed via Baidu Baike political section)
    {"id":"p3","name":"林文生","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"龙海区人大常委会主任",
     "current_org":"漳州市龙海区人民代表大会常务委员会",
     "source":"https://baike.baidu.com/item/%E9%BE%99%E6%B5%B7%E5%8C%BA",
     "notes":"区人大常委会主任，详细履历待查。",
     "confidence":"unverified"},

    # 洪海涛 — 区政协主席 (confirmed via Baidu Baike political section)
    {"id":"p4","name":"洪海涛","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"龙海区政协主席",
     "current_org":"中国人民政治协商会议漳州市龙海区委员会",
     "source":"https://baike.baidu.com/item/%E9%BE%99%E6%B5%B7%E5%8C%BA",
     "notes":"区政协主席，详细履历待查。",
     "confidence":"unverified"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 区党委机关
    {"id":"o1","name":"中共漳州市龙海区委员会","type":"党委","level":"县处级","parent":"中共漳州市委员会","location":"漳州市龙海区"},
    {"id":"o2","name":"中共漳州市龙海区纪律检查委员会","type":"纪委","level":"县处级","parent":"中共漳州市龙海区委员会","location":"漳州市龙海区"},
    {"id":"o3","name":"中共漳州市龙海区委组织部","type":"党委部门","level":"正科级","parent":"中共漳州市龙海区委员会","location":"漳州市龙海区"},
    {"id":"o4","name":"中共漳州市龙海区委宣传部","type":"党委部门","level":"正科级","parent":"中共漳州市龙海区委员会","location":"漳州市龙海区"},
    {"id":"o5","name":"中共漳州市龙海区委统战部","type":"党委部门","level":"正科级","parent":"中共漳州市龙海区委员会","location":"漳州市龙海区"},
    {"id":"o6","name":"中共漳州市龙海区委政法委员会","type":"党委部门","level":"正科级","parent":"中共漳州市龙海区委员会","location":"漳州市龙海区"},

    # 区政权机关
    {"id":"o7","name":"漳州市龙海区人民政府","type":"政府","level":"县处级","parent":"漳州市人民政府","location":"漳州市龙海区"},
    {"id":"o8","name":"漳州市龙海区人民代表大会常务委员会","type":"人大","level":"县处级","parent":"漳州市人民代表大会常务委员会","location":"漳州市龙海区"},
    {"id":"o9","name":"中国人民政治协商会议漳州市龙海区委员会","type":"政协","level":"县处级","parent":"政协漳州市委员会","location":"漳州市龙海区"},
    {"id":"o10","name":"漳州市龙海区监察委员会","type":"监察","level":"县处级","parent":"漳州市监察委员会","location":"漳州市龙海区"},

    # 区政府工作部门 (代表)
    {"id":"o11","name":"漳州市龙海区发展和改革局","type":"政府部门","level":"正科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o12","name":"漳州市龙海区教育局","type":"政府部门","level":"正科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o13","name":"漳州市龙海区公安局","type":"政府部门","level":"正科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o14","name":"漳州市龙海区财政局","type":"政府部门","level":"正科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o15","name":"漳州市龙海区人力资源和社会保障局","type":"政府部门","level":"正科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},

    # 乡镇/街道
    {"id":"o16","name":"漳州市龙海区石码街道","type":"乡镇/街道","level":"乡科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o17","name":"漳州市龙海区榜山街道","type":"乡镇/街道","level":"乡科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o18","name":"漳州市龙海区角美街道","type":"乡镇/街道","level":"乡科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o19","name":"漳州市龙海区海澄镇","type":"乡镇/街道","level":"乡科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
    {"id":"o20","name":"漳州市龙海区港尾镇","type":"乡镇/街道","level":"乡科级","parent":"漳州市龙海区人民政府","location":"漳州市龙海区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 叶毓 — 区委书记
    {"person_id":"p1","org_id":"o1","title":"龙海区委书记","start":"","end":"","rank":"正处级","note":"confirmed current role"},

    # 陈艺章 — 区长
    {"person_id":"p2","org_id":"o7","title":"龙海区委副书记、区长","start":"","end":"","rank":"正处级","note":"confirmed current role"},
    {"person_id":"p2","org_id":"o1","title":"龙海区委副书记","start":"","end":"","rank":"正处级","note":"concurrent party post"},

    # 林文生 — 人大主任
    {"person_id":"p3","org_id":"o8","title":"龙海区人大常委会主任","start":"","end":"","rank":"正处级","note":"confirmed current role"},

    # 洪海涛 — 政协主席
    {"person_id":"p4","org_id":"o9","title":"龙海区政协主席","start":"","end":"","rank":"正处级","note":"confirmed current role"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 叶毓 — 陈艺章: 区委书记和区长的党政搭档关系
    {"person_a":"p1","person_b":"p2","type":"党政搭档","context":"区委书记与区长搭档，共同领导龙海区工作","overlap_org":"中共漳州市龙海区委员会","overlap_period":"current","strength":"strong","confidence":"confirmed"},

    # 叶毓 — 林文生: 区委书记与人大主任的协调关系
    {"person_a":"p1","person_b":"p3","type":"党政人大","context":"区委书记与人大常委会主任","overlap_org":"中共漳州市龙海区委员会","overlap_period":"current","strength":"medium","confidence":"confirmed"},

    # 陈艺章 — 林文生: 区长与人大主任关系
    {"person_a":"p2","person_b":"p3","type":"政府人大","context":"区长向区人大报告工作","overlap_org":"漳州市龙海区","overlap_period":"current","strength":"medium","confidence":"confirmed"},
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
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
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""), r.get("strength", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    def person_color(p):
        post = p.get("current_post", "")
        if "书记" in post and "区" in post:
            return "255,50,50"   # red — party secretary
        if "区长" in post:
            return "50,100,255"  # blue — government leader
        if "人大" in post:
            return "100,180,100" # green — congress
        if "政协" in post:
            return "100,180,100" # green — CPPCC
        if "纪委书记" in post:
            return "255,165,0"   # orange — discipline
        return "100,100,100"     # grey — others

    def is_top_leader(p):
        post = p.get("current_post", "")
        return "区委书记" in post or "区长" in post

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
        if "纪委" in t or "监察" in t:
            return "255,220,200"
        if "乡镇" in t:
            return "255,255,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>龙海区 (Longhai District, Zhangzhou, Fujian) — Leadership Network Graph</description>')
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
    print(f"龙海区 Leadership Network — Build Complete")
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
