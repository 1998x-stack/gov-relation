#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 梧州市万秀区 leadership network.

梧州市万秀区 — 广西梧州市辖区, 梧州市老城区和核心城区.
Research date: 2026-07-23

Sources:
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/ (official leadership page)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/ldjj_43414/ (区长 bio page)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t18945409.shtml (唐志云 bio)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t11788906.shtml (梁汉樱 bio)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t11788902.shtml (黄沛森 bio)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t18406638.shtml (唐海涛 bio)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t27527926.shtml (黄有志 bio)
  - http://www.wzwxq.gov.cn/xxgk/jcxx/wxdt/zwyw/ (news archive)

Confidence: Current leadership roster confirmed from official Wanxiu District
government leadership portal. Career histories sourced from individual profile pages.
"""

import os
import sqlite3  # used by process_tmp validator
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data/database/万秀区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/万秀区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ── Add gov_relation to path ──
sys.path.insert(0, BASE)


# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders ──
    # 1. 易铭良 — 区委书记 (as of July 2026)
    {"id": 1, "name": "易铭良", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "万秀区委书记", "current_org": "中共万秀区委",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/wxdt/zwyw/",
     "notes": "2026年7月起任万秀区委书记（初期称区委主要负责人）。前任为黄来焕。",
     "confidence": "confirmed"},

    # 2. 欧广明 — 区长
    {"id": 2, "name": "欧广明", "gender": "男", "ethnicity": "壮族",
     "birth": "1983-06", "birthplace": "", "native_place": "",
     "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "万秀区委副书记、区政府党组书记、区长", "current_org": "万秀区人民政府",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/",
     "notes": "1983年6月出生，壮族，在职研究生学历。2025年左右任万秀区委副书记，2026年1月26日区人大常委会任命为副区长、代理区长，后转正。",
     "confidence": "confirmed"},

    # 3. 黄来焕 — 前任区委书记 (served until ~June 2026)
    {"id": 3, "name": "黄来焕", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（已卸任万秀区委书记）", "current_org": "",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/wxdt/zwyw/",
     "notes": "万秀区委书记，至2026年6月仍在任。去向待查。",
     "confidence": "confirmed"},

    # 4. 易洁 — 前任区长 (served through January 2026)
    {"id": 4, "name": "易洁", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（已卸任万秀区区长）", "current_org": "",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/wxdt/zwyw/",
     "notes": "万秀区委副书记、区长，至2026年1月14日最后以区长身份出席活动。去向待查。",
     "confidence": "confirmed"},

    # ── Deputy Mayors ──
    # 5. 唐志云 — 常委、常务副区长
    {"id": 5, "name": "唐志云", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-01", "birthplace": "", "native_place": "",
     "education": "大学/工学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "万秀区委常委、区政府党组副书记、副区长", "current_org": "万秀区人民政府",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t18945409.shtml",
     "notes": "1984年1月出生，汉族，大学学历，工学学士。负责常务工作。",
     "confidence": "confirmed"},

    # 6. 梁汉樱 — 副区长
    {"id": 6, "name": "梁汉樱", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-12", "birthplace": "", "native_place": "",
     "education": "大学/新闻学", "party_join": "", "work_start": "",
     "current_post": "万秀区人民政府副区长", "current_org": "万秀区人民政府",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t11788906.shtml",
     "notes": "1972年12月出生，汉族，大学学历，全日制本科学历，新闻学专业。",
     "confidence": "confirmed"},

    # 7. 黄沛森 — 副区长
    {"id": 7, "name": "黄沛森", "gender": "男", "ethnicity": "",
     "birth": "1980-08", "birthplace": "", "native_place": "",
     "education": "在职大学", "party_join": "中共党员", "work_start": "",
     "current_post": "万秀区人民政府副区长", "current_org": "万秀区人民政府",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t11788902.shtml",
     "notes": "1980年8月出生，在职大学学历。",
     "confidence": "confirmed"},

    # 8. 唐海涛 — 副区长
    {"id": 8, "name": "唐海涛", "gender": "男", "ethnicity": "",
     "birth": "1984-11", "birthplace": "", "native_place": "",
     "education": "在职大学/广西民族大学汉语言文学", "party_join": "中共党员", "work_start": "",
     "current_post": "万秀区人民政府副区长", "current_org": "万秀区人民政府",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t18406638.shtml",
     "notes": "1984年11月出生，在职大学学历，广西民族大学汉语言文学专业。",
     "confidence": "confirmed"},

    # 9. 黄有志 — 副区长、公安局局长
    {"id": 9, "name": "黄有志", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-03", "birthplace": "", "native_place": "",
     "education": "在职大学", "party_join": "中共党员", "work_start": "",
     "current_post": "万秀区政府党组成员、副区长、区委政法委副书记（兼）、市公安局万秀分局局长", "current_org": "万秀区人民政府",
     "source": "http://www.wzwxq.gov.cn/xxgk/jcxx/ldjj/fqz/t27527926.shtml",
     "notes": "1977年3月出生，汉族，在职大学学历，四级高级警长。",
     "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共万秀区委", "type": "党委", "level": "县级",
     "parent": "中共梧州市委", "location": "梧州市万秀区"},
    {"id": 2, "name": "万秀区人民政府", "type": "政府", "level": "县级",
     "parent": "梧州市人民政府", "location": "梧州市万秀区"},
    {"id": 3, "name": "万秀区人大常委会", "type": "人大", "level": "县级",
     "parent": "", "location": "梧州市万秀区"},
    {"id": 4, "name": "万秀区政协", "type": "政协", "level": "县级",
     "parent": "", "location": "梧州市万秀区"},
    {"id": 5, "name": "万秀区人民政府办公室", "type": "政府", "level": "科级",
     "parent": "万秀区人民政府", "location": "梧州市万秀区"},
    {"id": 6, "name": "万秀公安分局", "type": "政府", "level": "科级",
     "parent": "万秀区人民政府", "location": "梧州市万秀区"},
    {"id": 7, "name": "万秀区财政局", "type": "政府", "level": "科级",
     "parent": "万秀区人民政府", "location": "梧州市万秀区"},
    {"id": 8, "name": "万秀区发展和改革局", "type": "政府", "level": "科级",
     "parent": "万秀区人民政府", "location": "梧州市万秀区"},
]

positions = [
    # 易铭良
    {"person_id": 1, "org_id": 1, "title": "万秀区委书记",
     "start": "2026-07", "end": "", "rank": "正处级",
     "note": "2026年7月上任"},
    # 黄来焕
    {"person_id": 3, "org_id": 1, "title": "万秀区委书记",
     "start": "", "end": "2026-06", "rank": "正处级",
     "note": "至2026年6月仍在任"},
    # 欧广明 - current positions
    {"person_id": 2, "org_id": 1, "title": "万秀区委副书记",
     "start": "2025", "end": "", "rank": "副处级",
     "note": "2025年底起任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "万秀区政府党组书记、区长",
     "start": "2026-01", "end": "", "rank": "正处级",
     "note": "2026.01.26任代区长，后转正"},
    # 易洁
    {"person_id": 4, "org_id": 2, "title": "万秀区委副书记、区长",
     "start": "", "end": "2026-01", "rank": "正处级",
     "note": "至2026年1月14日最后以区长身份出席"},
    # 唐志云
    {"person_id": 5, "org_id": 1, "title": "万秀区委常委",
     "start": "", "end": "", "rank": "副处级",
     "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": "区政府党组副书记"},
    # 梁汉樱
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": ""},
    # 黄沛森
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": ""},
    # 唐海涛
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": ""},
    # 黄有志
    {"person_id": 9, "org_id": 2, "title": "副区长",
     "start": "", "end": "", "rank": "副处级",
     "note": "兼公安分局局长"},
    {"person_id": 9, "org_id": 6, "title": "万秀公安分局局长",
     "start": "", "end": "", "rank": "正科级",
     "note": "四级高级警长"},
]

relationships = [
    # Succession relationships
    {"person_a": 3, "person_b": 1, "type": "succession",
     "context": "黄来焕→易铭良：区委书记交接（2026年7月）",
     "overlap_org": "中共万秀区委", "overlap_period": "2026-07"},
    {"person_a": 4, "person_b": 2, "type": "succession",
     "context": "易洁→欧广明：区长交接（2026年1月）",
     "overlap_org": "万秀区人民政府", "overlap_period": "2026-01"},
    # Working relationships (current leadership team)
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "区委书记与区长搭档",
     "overlap_org": "中共万秀区委", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 5, "type": "colleague",
     "context": "区长与常务副区长",
     "overlap_org": "万秀区人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 7, "type": "colleague",
     "context": "区长与副区长",
     "overlap_org": "万秀区人民政府", "overlap_period": "2026至今"},
    {"person_a": 3, "person_b": 4, "type": "colleague",
     "context": "前任书记与前任区长搭档",
     "overlap_org": "万秀区", "overlap_period": "此前"},
    {"person_a": 3, "person_b": 2, "type": "colleague",
     "context": "前任书记与现任区长曾共事",
     "overlap_org": "万秀区", "overlap_period": "2025-2026"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_sqlite():
    import sqlite3
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS persons")
    cur.execute("DROP TABLE IF EXISTS organizations")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT,
            notes TEXT, confidence TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p.get("birthplace",""), p.get("native_place",""), p["education"],
              p["party_join"], p.get("work_start",""),
              p["current_post"], p["current_org"], p["source"],
              p.get("notes",""), p.get("confidence","confirmed")))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent",""), o.get("location","")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"SQLite DB: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rel:     {len(relationships)}")


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def person_color(p):
        role = p["current_post"]
        if "书记" in role and "区委书记" in role:
            return "255,50,50"  # Red
        if "区长" in role:
            return "50,100,255"  # Blue
        if "副区长" in role or "常委" in role:
            return "50,100,255"  # Blue
        return "100,100,100"

    def person_size(p):
        if "区委书记" in p["current_post"] or "区长" in p["current_post"]:
            return "20.0"
        return "12.0"

    def org_color(o):
        t = o["type"]
        if t == "党委": return "255,200,200"
        if t == "政府": return "200,200,255"
        if t == "人大": return "200,255,255"
        if t == "政协": return "255,240,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>梧州市万秀区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="education" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    eid = 0
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["education"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
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
    # Person→Organization edges (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start","")+"-"+pos.get("end",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person edges (relationships)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF:    {GEXF_PATH}")


if __name__ == "__main__":
    build_sqlite()
    build_gexf()
    print("Done.")
