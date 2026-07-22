#!/usr/bin/env python3
"""Build Huaibei (淮北市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - https://zh.wikipedia.org/wiki/淮北市 (Wikipedia, accessed 2026-07-15)
  - https://www.huaibei.gov.cn/ (淮北市人民政府官方网站, accessed 2026-07-15)
  - 163.com news search results, accessed 2026-07-15
  - Baidu Baike meta description for 汪华东 (blocked, metadata only)

Confidence: Current roles confirmed from Wikipedia (淮北市页面四大机构现任领导)
  and official government news (汪华东出席会议 Jul 14-15, 蒋曦调研 Jul 15).
  Biographical details are partial (Baidu Baike blocked from current network).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "淮北市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "淮北市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "汪华东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "安徽霍邱",
        "native_place": "安徽霍邱",
        "education": "在职研究生",
        "party_join": "1992-04",
        "work_start": "1992-07",
        "current_post": "市委书记",
        "current_org": "中共淮北市委",
        "source": "https://zh.wikipedia.org/wiki/淮北市 (四大机构现任领导); 百度百科meta",
        "notes": "1972年11月生，安徽霍邱人。1992年4月入党，1992年7月参加工作，在职研究生学历。"
                 "曾任淮北市市长(2022.08-2024.09)，2024年9月任淮北市委书记、淮北军分区党委第一书记。"
                 "曾为援藏干部。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "蒋曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "四川资阳",
        "native_place": "四川资阳",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "淮北市人民政府",
        "source": "https://zh.wikipedia.org/wiki/淮北市 (四大机构现任领导); 中国经济网2024-10-31",
        "notes": "1972年11月生，四川资阳人。2024年10月31日当选淮北市市长。履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "覃卫国",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1970-06",
        "birthplace": "广西贵港",
        "native_place": "广西贵港",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（现安徽省委常委、政法委书记）",
        "current_org": "中共安徽省委政法委员会",
        "source": "https://zh.wikipedia.org/wiki/覃卫国",
        "notes": "1970年6月生，广西贵港人，壮族。曾任广西交通投资集团总经理、安徽省人民政府副秘书长（正厅级）、"
                 "淮北市人民政府市长(2020.07-2022.08)、中共淮北市委书记(2022.05-2024.06)。"
                 "2024年5月任安徽省副省长兼公安厅厅长，2025年7月任安徽省委常委、政法委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "李朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "安徽宿州",
        "native_place": "安徽宿州",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "淮北市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/淮北市 (四大机构现任领导)",
        "notes": "1970年5月生，安徽宿州人。2026年1月任淮北市人大常委会主任。履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "钱界殊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-08",
        "birthplace": "安徽枞阳",
        "native_place": "安徽枞阳",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协淮北市委员会",
        "source": "https://zh.wikipedia.org/wiki/淮北市 (四大机构现任领导)",
        "notes": "1967年8月生，安徽枞阳人。2022年1月当选淮北市政协主席。履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "戴启远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前市长",
        "current_org": "淮北市人民政府",
        "source": "https://zh.wikipedia.org/wiki/覃卫国 (继任关系)",
        "notes": "覃卫国前任淮北市长。2020年7月由覃卫国接替。个人履历待补充。",
        "confidence": "plausible"
    },
    {
        "id": 7,
        "name": "张永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前市委书记",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/覃卫国 (前任)",
        "notes": "覃卫国前任淮北市委书记。2022年5月由覃卫国接替。另有任用。个人履历待补充。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中国共产党淮北市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省淮北市"
    },
    {
        "id": 2,
        "name": "淮北市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省人民政府",
        "location": "安徽省淮北市"
    },
    {
        "id": 3,
        "name": "淮北市人大常委会",
        "type": "人大",
        "level": "地级市",
        "parent": "淮北市",
        "location": "安徽省淮北市"
    },
    {
        "id": 4,
        "name": "政协淮北市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "淮北市",
        "location": "安徽省淮北市"
    },
    {
        "id": 5,
        "name": "中共安徽省委政法委员会",
        "type": "党委",
        "level": "省级",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省合肥市"
    },
    {
        "id": 6,
        "name": "安徽省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "安徽省",
        "location": "安徽省合肥市"
    },
    {
        "id": 7,
        "name": "安徽省公安厅",
        "type": "政府",
        "level": "省级",
        "parent": "安徽省人民政府",
        "location": "安徽省合肥市"
    },
    {
        "id": 8,
        "name": "广西交通投资集团有限公司",
        "type": "事业单位",
        "level": "省级",
        "parent": "广西壮族自治区",
        "location": "广西壮族自治区"
    },
]

positions = [
    # 汪华东
    {"person_id": 1, "org_id": 1, "title": "市委书记、淮北军分区党委第一书记", "start": "2024-09", "end": "present", "rank": "正厅级", "note": "2024年9月任现职"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start": "2022-08", "end": "2024-09", "rank": "正厅级", "note": "曾任淮北市市长"},
    # 蒋曦
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2024-10", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2024-10", "end": "present", "rank": "正厅级", "note": "2024年10月31日当选"},
    # 覃卫国
    {"person_id": 3, "org_id": 1, "title": "市委书记", "start": "2022-05", "end": "2024-06", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "市长", "start": "2020-07", "end": "2022-08", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "省委常委、政法委书记", "start": "2025-07", "end": "present", "rank": "副省级", "note": "现任"},
    {"person_id": 3, "org_id": 6, "title": "副省长", "start": "2024-05", "end": "present", "rank": "副省级", "note": "2024年5月任安徽省副省长"},
    {"person_id": 3, "org_id": 7, "title": "省公安厅厅长", "start": "2024-07", "end": "2026-03", "rank": "正厅级", "note": "2024年7月任省公安厅厅长"},
    {"person_id": 3, "org_id": 8, "title": "总经理", "start": "", "end": "", "rank": "正厅级", "note": "广西交通投资集团总经理"},
    # 李朝晖
    {"person_id": 4, "org_id": 3, "title": "市人大常委会主任", "start": "2026-01", "end": "present", "rank": "正厅级", "note": "2026年1月任职"},
    # 钱界殊
    {"person_id": 5, "org_id": 4, "title": "市政协主席", "start": "2022-01", "end": "present", "rank": "正厅级", "note": "2022年1月当选"},
    # 戴启远
    {"person_id": 6, "org_id": 2, "title": "市长", "start": "", "end": "2020-07", "rank": "正厅级", "note": "2020年7月离任"},
    # 张永
    {"person_id": 7, "org_id": 1, "title": "市委书记", "start": "", "end": "2022-05", "rank": "正厅级", "note": "2022年5月离任"},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长，市委领导班子正副搭档",
        "overlap_org": "中共淮北市委",
        "overlap_period": "2024-10至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "市委书记职务：覃卫国(2022-2024)→汪华东(2024-)，同时覃卫国提携/推荐汪华东接任书记",
        "overlap_org": "中共淮北市委",
        "overlap_period": "2022-08至2024-06",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "市长职务：覃卫国(2020-2022)转任书记，汪华东(2022-2024)接任市长",
        "overlap_org": "淮北市人民政府",
        "overlap_period": "2020-2022",
        "confidence": "confirmed"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "覃卫国任市委书记期间(2022.05-2024.06)李朝晖为市领导",
        "overlap_org": "中共淮北市委",
        "overlap_period": "2022-2024",
        "confidence": "plausible"
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "覃卫国任市委书记期间钱界殊任市政协主席",
        "overlap_org": "淮北市",
        "overlap_period": "2022-2024",
        "confidence": "plausible"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "汪华东任市委书记期间，李朝晖任市人大常委会主任",
        "overlap_org": "淮北市",
        "overlap_period": "2024-至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "汪华东任市委书记期间，钱界殊任市政协主席",
        "overlap_org": "淮北市",
        "overlap_period": "2024-至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "蒋曦任市长期间，钱界殊任市政协主席",
        "overlap_org": "淮北市",
        "overlap_period": "2024-至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 3,
        "person_b": 6,
        "type": "predecessor_successor",
        "context": "戴启远→覃卫国，前任市长与继任市长",
        "overlap_org": "淮北市人民政府",
        "overlap_period": "2020",
        "confidence": "confirmed"
    },
    {
        "person_a": 3,
        "person_b": 7,
        "type": "predecessor_successor",
        "context": "张永→覃卫国，前任市委书记与继任市委书记",
        "overlap_org": "中共淮北市委",
        "overlap_period": "2022",
        "confidence": "confirmed"
    },
]


# ── build functions ──────────────────────────────────────────────────────

def create_database(db_path):
    """Create SQLite database with persons, organizations, positions, relationships."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
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
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                native_place, education, party_join, work_start, current_post, current_org,
                source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
              p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""),
              p.get("source", ""), p.get("notes", ""), p.get("confidence", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""),
              pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", ""), r.get("confidence", "")))

    conn.commit()
    conn.close()


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — party secretary
    elif "市长" in post or "区长" in post or "县长" in post:
        return "50,100,255"   # Blue — government leader
    elif "纪委" in post:
        return "255,165,0"    # Orange — discipline
    else:
        return "100,100,100"  # Grey — other


def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "市长" in post or "区长" in post or "县长" in post


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def generate_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>淮北市领导班子工作关系网络 — Party Secretary, Mayor, and leadership team</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title", ""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(gexf_path) or ".", exist_ok=True)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── main ─────────────────────────────────────────────────────────────────

def main():
    print(f"=== 淮北市 Leadership Network Data Builder ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()

    # 1. Database
    print(f"Creating database: {DB_PATH}")
    create_database(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # 2. GEXF
    print(f"\nCreating GEXF: {GEXF_PATH}")
    generate_gexf(GEXF_PATH)
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  GEXF file size: {gexf_size} bytes")

    # 3. Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")

    for p in persons:
        conf = p.get("confidence", "")
        print(f"  - {p['name']}: {p.get('current_post', '')} ({conf})")

    print(f"\nDone. Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
