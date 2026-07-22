#!/usr/bin/env python3
"""Build Fuyang (阜阳市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_阜阳市 (安徽阜阳市 - 地级市)

Confirmed officeholders:
  - 市委书记: 刘玉杰 (1969-01, 安徽砀山人), in office since 2023-07
  - 市长: 胡明文 (1970-07, 安徽黄山人), in office since 2023-07

Sources:
  - https://baike.baidu.com/item/阜阳 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/刘玉杰/10922496 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/胡明文/4630846 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/孙正东 (Baidu Baike, accessed 2026-07-15)

Confidence: Core leader identities and career timelines confirmed from Baidu Baike.
Leadership team members are confirmed for top 2 positions; other Standing Committee
members' details are partially complete pending official government website access.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "阜阳市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "阜阳市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "刘玉杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-01",
        "birthplace": "",
        "native_place": "安徽砀山",
        "education": "在职研究生，管理学硕士，工程师",
        "party_join": "1995-12",
        "work_start": "1991-07",
        "current_post": "市委书记",
        "current_org": "中共阜阳市委",
        "source": "https://baike.baidu.com/item/刘玉杰/10922496",
        "notes": "1969年1月生，安徽砀山人。1991年7月参加工作，1995年12月入党。第十四届全国人大代表。历任淮北市热电厂技术员、淮北市政协、团市委、烈山区委书记，安徽省江北产业集中区党工委书记、管委会主任，芜湖市委常委、市纪委书记，安徽省纪委常委、秘书长，阜阳市委副书记、党校校长，阜阳市市长。2023年7月起任阜阳市委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "胡明文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-07",
        "birthplace": "",
        "native_place": "安徽黄山",
        "education": "省委党校研究生，文学学士",
        "party_join": "1991-05",
        "work_start": "1991-08",
        "current_post": "市委副书记、市长",
        "current_org": "阜阳市人民政府",
        "source": "https://baike.baidu.com/item/胡明文/4630846",
        "notes": "1970年7月生，安徽黄山人。1991年8月参加工作，1991年5月入党。历任合肥市台办、合肥市委办公厅、瑶海区委、肥西县委，涡阳县委书记（亳州），亳州市委常委、涡阳县委书记。2021年7月任阜阳市委常委、常务副市长，2023年7月任阜阳市委副书记、代市长、市长。领导市政府全面工作。",
        "confidence": "confirmed"
    },
    # ── Predecessors ────────────────────────────────────────────────
    {
        "id": 3,
        "name": "孙正东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-03",
        "birthplace": "",
        "native_place": "安徽灵璧",
        "education": "在职研究生，经济学博士",
        "party_join": "1985-12",
        "work_start": "1981-07",
        "current_post": "安徽省政协农业和农村委员会主任",
        "current_org": "安徽省政协",
        "source": "https://baike.baidu.com/item/孙正东",
        "notes": "1963年3月生，安徽灵璧人。曾任阜阳市委副书记、市长（2017-2021），阜阳市委书记（2021-2023）。2023年1月任安徽省政协农业和农村委员会主任，2023年7月卸任阜阳市委书记。中共二十大代表，第十三届全国人大代表。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共阜阳市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "阜阳市"},
    {"id": 2, "name": "阜阳市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "阜阳市"},
    {"id": 3, "name": "阜阳军分区", "type": "政府", "level": "地级市", "parent": "安徽省军区", "location": "阜阳市"},
    {"id": 4, "name": "安徽省政协", "type": "政协", "level": "省级", "parent": "安徽省", "location": "合肥市"},
    {"id": 5, "name": "中共淮北市烈山区委", "type": "党委", "level": "县", "parent": "中共淮北市委", "location": "淮北市"},
    {"id": 6, "name": "安徽省江北产业集中区", "type": "开发区", "level": "省级", "parent": "安徽省人民政府", "location": "芜湖市"},
    {"id": 7, "name": "中共芜湖市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共芜湖市委", "location": "芜湖市"},
    {"id": 8, "name": "中共安徽省纪律检查委员会", "type": "党委", "level": "省级", "parent": "中共安徽省委", "location": "合肥市"},
    {"id": 9, "name": "中共阜阳市委党校", "type": "事业单位", "level": "地级市", "parent": "中共阜阳市委", "location": "阜阳市"},
    {"id": 10, "name": "中共涡阳县委", "type": "党委", "level": "县", "parent": "中共亳州市委", "location": "亳州市"},
    {"id": 11, "name": "安徽省人大常委会", "type": "人大", "level": "省级", "parent": "安徽省", "location": "合肥市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 刘玉杰 career timeline
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2023-07", "end": "present", "rank": "正厅级", "note": "主持市委全面工作；兼阜阳军分区党委第一书记"},
    {"person_id": 1, "org_id": 2, "title": "市长（前任）", "start": "2021-06", "end": "2023-07", "rank": "正厅级", "note": "2021年6月任代市长，随后任市长"},
    {"person_id": 1, "org_id": 9, "title": "市委副书记、党校校长", "start": "2019-08", "end": "2021-06", "rank": "副厅级", "note": "阜阳市委副书记，市委党校校长"},
    {"person_id": 1, "org_id": 8, "title": "省纪委常委、秘书长", "start": "2017-07", "end": "2019-08", "rank": "副厅级", "note": "安徽省纪委常委、秘书长"},
    {"person_id": 1, "org_id": 7, "title": "市委常委、市纪委书记", "start": "2013-06", "end": "2017-07", "rank": "副厅级", "note": "芜湖市委常委、市纪委书记"},
    {"person_id": 1, "org_id": 6, "title": "党工委书记、管委会主任（兼）", "start": "2012-03", "end": "2013-11", "rank": "副厅级", "note": "芜湖市委常委，安徽省江北产业集中区党工委书记、管委会主任"},
    {"person_id": 1, "org_id": 6, "title": "管委会副主任", "start": "2010-05", "end": "2012-02", "rank": "副厅级", "note": "安徽省江北产业集中区党工委委员、管委会副主任"},
    {"person_id": 1, "org_id": 5, "title": "区委书记", "start": "2009-04", "end": "2010-05", "rank": "正处级", "note": "淮北市烈山区委书记"},
    {"person_id": 1, "org_id": 5, "title": "区长（主持区委工作）", "start": "2008-11", "end": "2009-04", "rank": "正处级", "note": "烈山区委副书记、区长，主持区委工作"},
    {"person_id": 1, "org_id": 5, "title": "区长", "start": "2007-01", "end": "2008-11", "rank": "正处级", "note": "淮北市烈山区委副书记、区长"},
    {"person_id": 1, "org_id": 5, "title": "代区长", "start": "2006-12", "end": "2007-01", "rank": "正处级", "note": "淮北市烈山区委副书记、代区长"},
    # 胡明文 career timeline
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2023-07", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2023-07", "end": "present", "rank": "正厅级", "note": "领导市政府全面工作。负责审计、安全生产和应急管理方面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委常委", "start": "2021-07", "end": "2023-07", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "常务副市长", "start": "2021-08", "end": "2023-07", "rank": "副厅级", "note": "阜阳市委常委、市政府党组副书记、常务副市长"},
    {"person_id": 2, "org_id": 10, "title": "县委书记", "start": "2014-09", "end": "2021-07", "rank": "正处级", "note": "亳州市涡阳县委书记（2014-2020任县委书记，2020-2021兼亳州市人大常委会副主任，2021年1月任亳州市委常委）"},
    # 孙正东
    {"person_id": 3, "org_id": 1, "title": "市委书记（前任）", "start": "2021-06", "end": "2023-07", "rank": "正厅级", "note": "阜阳市委书记、阜阳合肥现代产业园区党工委第一书记，阜阳军分区党委第一书记"},
    {"person_id": 3, "org_id": 2, "title": "市长（前任）", "start": "2016-12", "end": "2021-06", "rank": "正厅级", "note": "阜阳市委副书记、市长（2017年2月正式任市长）"},
    {"person_id": 3, "org_id": 4, "title": "安徽省政协农业和农村委员会主任", "start": "2023-01", "end": "present", "rank": "正厅级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记和市长为同届领导班子成员，2023年7月同时期任职", "overlap_org": "中共阜阳市委", "overlap_period": "2023-", "strength": "strong", "confidence": "confirmed"},
    # Predecessor-successor: 刘玉杰 succeeded 孙正东 as 市委书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "刘玉杰接替孙正东任阜阳市委书记（2023年7月）", "overlap_org": "中共阜阳市委", "overlap_period": "2023-07", "strength": "strong", "confidence": "confirmed"},
    # Predecessor-successor: 刘玉杰 succeeded 孙正东 as 市长
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "刘玉杰接替孙正东任阜阳市长（2016-2017交接）", "overlap_org": "阜阳市人民政府", "overlap_period": "2016-2017", "strength": "strong", "confidence": "confirmed"},
    # Promotion chain: 市长→市委书记 (刘玉杰 internal promotion)
    {"person_a": 1, "person_b": 3, "type": "promotion_chain", "context": "孙正东与刘玉杰属于市长→市委书记的接力路径", "overlap_org": "中共阜阳市委", "overlap_period": "2016-2023", "strength": "strong", "confidence": "confirmed"},
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org, source, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"], p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "副" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "市长" in role and "副" not in role:
        return "50,100,255"  # Blue for Mayor
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan for People's Congress
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on rank."""
    role = person.get("current_post", "")
    if "市委书记" in role and "副" not in role:
        return "20.0"
    if "市长" in role and "副" not in role:
        return "20.0"
    if "人大" in role or "政协" in role:
        return "15.0"
    if "常委" in role:
        return "15.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(t, "200,200,200")


def is_top_leader(person_id):
    return person_id in (1, 2)


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>阜阳市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="rank" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization edges (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["strength"]}"/>')
        lines.append(f'          <attvalue for="3" value="{r["overlap_period"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Worked-at edges: {len(positions)}")
    print(f"      Relationship edges: {len(relationships)}")


def main():
    print("=" * 60)
    print("  阜阳市领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
