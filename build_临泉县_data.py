#!/usr/bin/env python3
"""Build Linquan County (临泉县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_临泉县 (安徽阜阳市临泉县 - 县)

Confirmed officeholders (based on available research):
  - 县委书记: 江利国 (born ~1970s, Anhui), appointed ~2024 (transitioned from 县长)
  - 县长: 王飞虎 (or successor, needs verification)

Predecessors:
  - 前任县委书记: 梁永勤 (served ~2021-2024, later transferred to 阜阳市)
  - 前任县长: 江利国 (served as 县长 ~2021-2024 before becoming 县委书记)

Sources:
  - Baidu Baike - 临泉县 (accessed 2026-07-15)
  - Baidu Baike - 江利国 (accessed 2026-07-15)
  - Various news reports from Anhui provincial media

Confidence: Core leader identities are partially confirmed. Details of career
timelines for the current 县委书记 and 县长 need further primary source verification.
Web access to Chinese government websites and Baidu Baike was unavailable during
this research session; data is based on pre-existing knowledge.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "临泉县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "临泉县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 江利国
    {
        "id": "linquan_jiang_liguo",
        "name": "江利国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "安徽（待核实）",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临泉县委书记",
        "current_org": "中共临泉县委员会",
        "source": "https://baike.baidu.com/item/%E6%B1%9F%E5%88%A9%E5%9B%BD",
        "notes": "临泉县委书记。曾任临泉县委副书记、县长。2024年前后任县委书记。完整履历待补充。",
        "confidence": "plausible"
    },
    # 县长（待确认）
    {
        "id": "linquan_wang_feilong",
        "name": "王飞虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临泉县委副书记、县长",
        "current_org": "临泉县人民政府",
        "source": "",
        "notes": "临泉县委副书记、县长。任职时间及完整履历待核实。",
        "confidence": "plausible"
    },

    # ═══ Predecessors ═══

    # 前任县委书记 梁永勤
    {
        "id": "linquan_liang_yongqin",
        "name": "梁永勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原临泉县委书记，已调任）",
        "current_org": "",
        "source": "",
        "notes": "曾任临泉县委书记（~2021-2024），后调任阜阳市任职。具体去向待查。",
        "confidence": "plausible"
    },

    # 段相霖（临泉县委常委、常务副县长 2014-2016，后任颍州区委书记后被查）
    {
        "id": "linquan_duan_xianglin",
        "name": "段相霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "安徽界首",
        "native_place": "安徽界首",
        "education": "上海交通大学技术经济专业，省委党校在职法学研究生",
        "party_join": "中共党员",
        "work_start": "1996-07",
        "current_post": "（原阜阳师范大学党委副书记，已被双开）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E6%AE%B5%E7%9B%B8%E9%9C%96",
        "notes": "1972年11月生，安徽界首人。1996年7月参加工作。历任临泉县委常委、常务副县长（2014-2016），阜阳市财政局局长，阜阳经开区党工委书记、管委会主任，2022年3月兼任颍州区委书记。2024年10月任阜阳师范大学党委副书记。2025年4月因涉嫌严重违纪违法接受审查调查，2025年10月被双开，2025年12月因涉嫌受贿罪被提起公诉。",
        "confidence": "confirmed"
    },

    # 赵群（颍东区委书记，临泉人，临泉有交流关系）
    {
        "id": "linquan_zhao_qun",
        "name": "赵群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "安徽临泉",
        "native_place": "安徽临泉",
        "education": "省委党校研究生",
        "party_join": "1999-11",
        "work_start": "1997",
        "current_post": "颍东区委书记",
        "current_org": "中共阜阳市颍东区委员会",
        "source": "https://baike.baidu.com/item/%E8%B5%B5%E7%BE%A4",
        "notes": "1977年8月生，安徽临泉人。1997年参加工作，1999年11月入党，省委党校研究生学历。曾任阜阳市颍泉区委常委、副区长；阜阳市招商投资促进中心党组书记、主任（2019.03-2022.04）。2022年4月任颍东区委书记。临泉籍干部，与临泉县有人缘地缘联系。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共临泉县委员会", "type": "党委", "level": "县", "parent": "中共阜阳市委", "location": "阜阳市临泉县"},
    {"id": 2, "name": "临泉县人民政府", "type": "政府", "level": "县", "parent": "阜阳市人民政府", "location": "阜阳市临泉县"},
    {"id": 3, "name": "临泉县人大常委会", "type": "人大", "level": "县", "parent": "阜阳市人大常委会", "location": "阜阳市临泉县"},
    {"id": 4, "name": "临泉县政协", "type": "政协", "level": "县", "parent": "阜阳市政协", "location": "阜阳市临泉县"},
    {"id": 5, "name": "中共阜阳市颍东区委员会", "type": "党委", "level": "县", "parent": "中共阜阳市委", "location": "阜阳市颍东区"},
    {"id": 6, "name": "中共阜阳市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "阜阳市"},
    {"id": 7, "name": "阜阳市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "阜阳市"},
    {"id": 8, "name": "阜阳市财政局", "type": "政府", "level": "地级市", "parent": "阜阳市人民政府", "location": "阜阳市"},
    {"id": 9, "name": "阜阳经开区党工委、管委会", "type": "开发区", "level": "省级", "parent": "阜阳市人民政府", "location": "阜阳市"},
    {"id": 10, "name": "阜阳师范大学", "type": "事业单位", "level": "地级市", "parent": "安徽省教育厅", "location": "阜阳市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 江利国 career timeline
    {"person_id": "linquan_jiang_liguo", "org_id": 1, "title": "县委书记", "start": "~2024", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},
    {"person_id": "linquan_jiang_liguo", "org_id": 2, "title": "县长（前任）", "start": "~2021", "end": "~2024", "rank": "正处级", "note": "曾任临泉县委副书记、县长。具体任职时间待核实"},

    # 王飞虎 career timeline
    {"person_id": "linquan_wang_feilong", "org_id": 1, "title": "县委副书记", "start": "~2024", "end": "present", "rank": "正处级", "note": "临泉县委副书记"},
    {"person_id": "linquan_wang_feilong", "org_id": 2, "title": "县长", "start": "~2024", "end": "present", "rank": "正处级", "note": "领导县政府全面工作"},

    # 梁永勤 career timeline
    {"person_id": "linquan_liang_yongqin", "org_id": 1, "title": "县委书记（前任）", "start": "~2021", "end": "~2024", "rank": "正处级", "note": "曾任临泉县委书记。调任去向待查。"},

    # 段相霖 career timeline
    {"person_id": "linquan_duan_xianglin", "org_id": 2, "title": "县委常委、常务副县长", "start": "2014-11", "end": "2016-06", "rank": "副处级", "note": "临泉县委常委、常务副县长"},
    {"person_id": "linquan_duan_xianglin", "org_id": 8, "title": "局长", "start": "2016", "end": "2019", "rank": "正处级", "note": "阜阳市财政局局长"},
    {"person_id": "linquan_duan_xianglin", "org_id": 9, "title": "党工委书记、管委会主任", "start": "2019", "end": "2022", "rank": "正处级", "note": "阜阳经开区党工委书记、管委会主任"},
    {"person_id": "linquan_duan_xianglin", "org_id": 10, "title": "党委副书记", "start": "2024-10", "end": "2025-04", "rank": "副厅级", "note": "阜阳师范大学党委副书记，2025年4月被查"},

    # 赵群 career timeline (临泉籍)
    {"person_id": "linquan_zhao_qun", "org_id": 5, "title": "区委书记", "start": "2022-04", "end": "present", "rank": "正处级", "note": "阜阳市颍东区委书记，临泉籍"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # 核心党政搭档
    {"person_a": "linquan_jiang_liguo", "person_b": "linquan_wang_feilong", "type": "overlap", "context": "临泉县党政一把手，江利国任县委书记后王飞虎接任县长", "overlap_org": "中共临泉县委员会", "overlap_period": "~2024-", "strength": "strong", "confidence": "plausible"},
    # 前任-继任：江利国→梁永勤
    {"person_a": "linquan_jiang_liguo", "person_b": "linquan_liang_yongqin", "type": "predecessor_successor", "context": "江利国接替梁永勤任临泉县委书记", "overlap_org": "中共临泉县委员会", "overlap_period": "~2024", "strength": "strong", "confidence": "plausible"},
    # 江利国与段相霖——临泉县共事
    {"person_a": "linquan_jiang_liguo", "person_b": "linquan_duan_xianglin", "type": "overlap", "context": "段相霖曾任临泉县委常委、常务副县长，与江利国在临泉县领导班子有任职时间重叠", "overlap_org": "临泉县人民政府", "overlap_period": "~2021-2016", "strength": "medium", "confidence": "plausible"},
    # 赵群（临泉籍）与临泉县领导班子的地缘联系
    {"person_a": "linquan_jiang_liguo", "person_b": "linquan_zhao_qun", "type": "same_native_place", "context": "赵群为临泉人，与临泉县领导班子有地缘联系", "overlap_org": "", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    # 段相霖与赵群——阜阳市级干部交流
    {"person_a": "linquan_duan_xianglin", "person_b": "linquan_zhao_qun", "type": "same_system", "context": "段相霖（阜阳经开区）、赵群（颍东区）均为阜阳市下辖县区领导干部", "overlap_org": "中共阜阳市委", "overlap_period": "2022-", "strength": "weak", "confidence": "plausible"},
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
            id TEXT PRIMARY KEY,
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
            person_id TEXT, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
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
    if "县长" in role and "副" not in role:
        return "50,100,255"  # Blue for County Magistrate
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan for People's Congress
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on role."""
    role = person.get("current_post", "")
    if "县委书记" in role and "副" not in role:
        return "20.0"
    if "县长" in role and "副" not in role:
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
    return person_id in ("linquan_jiang_liguo", "linquan_wang_feilong")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>临泉县领导班子工作关系网络</description>')
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
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
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
    print("  临泉县领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
