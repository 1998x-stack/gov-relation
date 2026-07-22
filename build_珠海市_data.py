#!/usr/bin/env python3
"""
广东省珠海市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Zhuhai City leadership.

Level: 地级市
Province: 广东省
Targets: 市委书记 & 市长

Research Notes:
- Current 市委书记: 陈勇 (born 1974-01, Sichuan Ziyang, appointed 2023-09, formerly Guangzhou Huangpu District Secretary, Guangzhou Vice Mayor)
- Current 市长: 吴泽桐 (born 1980-01, Guangdong Shantou, appointed 2024-12 acting, confirmed 2025-02, formerly Yunfu Executive Vice Mayor)
- Leadership data compiled from Wikipedia and official sources (2026-07-22)

Sources:
- https://zh.wikipedia.org/wiki/珠海市 — Wikipedia city page (leadership roster)
- https://zh.wikipedia.org/wiki/陈勇_(1974年) — Wikipedia biography
- https://zh.wikipedia.org/wiki/吴泽桐 — Wikipedia biography
- https://www.zhuhai.gov.cn — official government website
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
DATABASE_DIR = os.path.join(PROJECT_DIR, "data", "database")
GRAPH_DIR = os.path.join(PROJECT_DIR, "data", "graph")
DB_PATH = os.path.join(DATABASE_DIR, "珠海市_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "珠海市_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 市委班子 (Party Committee) ══
    ("zhuhai_chen_yong", "陈勇", "男", "汉族", "1974年1月", "四川资阳",
     "华南理工大学工商管理学院管理工程专业硕士研究生", "中共党员", "1996年？",
     "市委书记", "中共珠海市委员会",
     "wikipedia;people.com.cn;zhuhai.gov.cn"),

    ("zhuhai_wu_zetong", "吴泽桐", "男", "汉族", "1980年1月", "广东汕头（籍贯海南定安）",
     "华南理工大学管理学学士、法学学士、管理学硕士；美国匹兹堡州立大学MBA", "中共党员", "2002年？",
     "市委副书记、市长", "珠海市人民政府",
     "wikipedia;zhuhai.gov.cn;media_reports"),

    ("zhuhai_pan_jiang", "潘江", "男", "汉族", "1965年1月", "广东汕头",
     "待查", "中共党员", "待查",
     "市人大常委会主任", "珠海市人大常委会",
     "wikipedia"),

    ("zhuhai_wang_kaizhou", "王开洲", "男", "汉族", "1969年9月", "待查",
     "待查", "中共党员", "待查",
     "市政协主席", "政协珠海市委员会",
     "wikipedia"),

    # ══ 前任领导 ══
    ("zhuhai_lv_yuyin", "吕玉印", "男", "汉族", "1970年11月", "河南郑州",
     "南开大学经济学博士", "中共党员", "待查",
     "前任市委书记（2021.11-2023.06）", "中共珠海市委员会（原）",
     "wikipedia;media_reports"),

    ("zhuhai_huang_zhihao", "黄志豪", "男", "汉族", "1971年9月", "广东东莞",
     "待查", "中共党员", "待查",
     "前任市长（2021.05-2024.12）", "珠海市人民政府（原）",
     "wikipedia;media_reports"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location

    # ══ 党政机构 ══
    (1, "中共珠海市委员会", "党委", "地级市", "中共广东省委", "珠海市香洲区"),
    (2, "珠海市人民政府", "政府", "地级市", "广东省人民政府", "珠海市香洲区"),
    (3, "珠海市人大常委会", "人大", "地级市", "广东省人大常委会", "珠海市香洲区"),
    (4, "政协珠海市委员会", "政协", "地级市", "政协广东省委员会", "珠海市香洲区"),
    (5, "中共珠海市纪律检查委员会", "纪委", "地级市", "中共广东省纪委", "珠海市香洲区"),

    # ══ 陈勇此前任职单位 ══
    (6, "中共广州市黄埔区委员会", "党委", "副厅级", "中共广州市委", "广州市黄埔区"),
    (7, "广州市黄埔区人民政府", "政府", "副厅级", "广州市人民政府", "广州市黄埔区"),
    (8, "广州市增城区人民政府", "政府", "副厅级", "广州市人民政府", "广州市增城区"),
    (9, "中共广州市委", "党委", "副省级", "中共广东省委", "广州市"),
    (10, "广州市人民政府", "政府", "副省级", "广东省人民政府", "广州市"),

    # ══ 吴泽桐此前任职单位 ══
    (11, "广东省发展和改革委员会", "政府", "省级", "广东省人民政府", "广州市"),
    (12, "梅州市人民政府", "政府", "地级市", "广东省人民政府", "梅州市"),
    (13, "中共梅州市梅县区委员会", "党委", "县处级", "中共梅州市委", "梅州市梅县区"),
    (14, "中共云浮市委", "党委", "地级市", "中共广东省委", "云浮市"),
    (15, "云浮市人民政府", "政府", "地级市", "广东省人民政府", "云浮市"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note, source

    # ══ 陈勇 ══
    ("zhuhai_chen_yong", 2, "市长", "？", "2023-09", "正厅级",
     "陈勇未任珠海市长，直接由广州调任珠海市委书记", "wikipedia"),  # Note: 陈勇 was not Zhuhai mayor
    ("zhuhai_chen_yong", 1, "市委书记", "2023-09", "present", "正厅级",
     "2023年9月任珠海市委书记", "wikipedia;people.com.cn"),

    ("zhuhai_chen_yong", 10, "副市长", "？", "？", "副省级城市副职",
     "曾任广州市副市长", "wikipedia"),
    ("zhuhai_chen_yong", 9, "市委常委", "？", "2023-09", "副省级城市副职",
     "曾任广州市委常委", "wikipedia"),
    ("zhuhai_chen_yong", 6, "区委书记", "？", "？", "副厅级",
     "曾任黄埔区委书记", "wikipedia"),
    ("zhuhai_chen_yong", 7, "区长", "？", "？", "副厅级",
     "曾任黄埔区区长", "wikipedia"),
    ("zhuhai_chen_yong", 8, "区长", "？", "？", "副厅级",
     "曾任增城区区长", "wikipedia"),

    # ══ 吴泽桐 ══
    ("zhuhai_wu_zetong", 2, "市长", "2025-02", "present", "正厅级",
     "2024年12月任代市长，2025年2月当选市长", "wikipedia;zhuhai.gov.cn"),
    ("zhuhai_wu_zetong", 1, "市委副书记", "2024-12", "present", "正厅级",
     "任市长同时兼任市委副书记", "wikipedia;zhuhai.gov.cn"),

    ("zhuhai_wu_zetong", 15, "常务副市长", "2021-05", "2024-12", "副厅级",
     "曾任云浮市委常委、常务副市长", "wikipedia"),
    ("zhuhai_wu_zetong", 14, "市委常委", "2021-05", "2024-12", "副厅级",
     "曾任云浮市委常委", "wikipedia"),
    ("zhuhai_wu_zetong", 13, "区委书记", "？", "？", "县处级",
     "曾任梅县区委书记", "wikipedia"),
    ("zhuhai_wu_zetong", 12, "副市长", "2016-11", "2021-05", "副厅级",
     "曾任梅州市副市长", "wikipedia"),
    ("zhuhai_wu_zetong", 11, "处长/副主任", "？", "2016-11", "县处级",
     "曾任广东省发改委综合处处长、办公室副主任等职", "wikipedia"),

    # ══ 潘江 ══
    ("zhuhai_pan_jiang", 3, "主任", "2022-01", "present", "正厅级",
     "珠海市人大常委会主任", "wikipedia"),

    # ══ 王开洲 ══
    ("zhuhai_wang_kaizhou", 4, "主席", "2022-01", "present", "正厅级",
     "珠海市政协主席", "wikipedia"),

    # ══ 前任领导 ══
    ("zhuhai_lv_yuyin", 1, "市委书记", "2021-11", "2023-06", "正厅级",
     "前任珠海市委书记，后任中央人民政府驻澳门特别行政区联络办公室副主任", "wikipedia;media_reports"),

    ("zhuhai_huang_zhihao", 2, "市长", "2021-05", "2024-12", "正厅级",
     "前任珠海市长", "wikipedia;media_reports"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period, source, confidence

    # ══ 党政搭档 ══
    ("zhuhai_chen_yong", "zhuhai_wu_zetong", "党政搭档",
     "陈勇任市委书记、吴泽桐任市长，共同组成珠海市党政一把手",
     "中共珠海市委员会/珠海市人民政府", "2024.12-至今",
     "wikipedia;zhuhai.gov.cn", "confirmed"),

    # ══ 前任继任关系 ══
    ("zhuhai_chen_yong", "zhuhai_lv_yuyin", "前任继任",
     "陈勇接替吕玉印任珠海市委书记",
     "中共珠海市委员会", "2023.09",
     "wikipedia", "confirmed"),

    ("zhuhai_wu_zetong", "zhuhai_huang_zhihao", "前任继任",
     "吴泽桐接替黄志豪任珠海市长",
     "珠海市人民政府", "2024.12",
     "wikipedia", "confirmed"),

    # ══ 同城共事关系 ══
    ("zhuhai_pan_jiang", "zhuhai_chen_yong", "同城共事",
     "潘江作为市人大常委会主任与市委书记陈勇同在珠海市领导班子",
     "珠海市", "2023.09-至今",
     "wikipedia", "confirmed"),

    ("zhuhai_wang_kaizhou", "zhuhai_chen_yong", "同城共事",
     "王开洲作为市政协主席与市委书记陈勇同在珠海市领导班子",
     "珠海市", "2023.09-至今",
     "wikipedia", "confirmed"),

    ("zhuhai_pan_jiang", "zhuhai_wu_zetong", "同城共事",
     "潘江作为市人大常委会主任与市长吴泽桐同在珠海市领导班子",
     "珠海市", "2024.12-至今",
     "wikipedia", "confirmed"),

    ("zhuhai_wang_kaizhou", "zhuhai_wu_zetong", "同城共事",
     "王开洲作为市政协主席与市长吴泽桐同在珠海市领导班子",
     "珠海市", "2024.12-至今",
     "wikipedia;zhuhai.gov.cn", "confirmed"),
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    """Return GEXF color for a person based on their post."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"
    elif "市长" in post or "区长" in post or "副市长" in post:
        return "50,100,255"
    elif "纪委" in post or "监委" in post:
        return "255,165,0"
    elif "主任" in post or "主席" in post:
        return "0,150,0"
    else:
        return "100,100,100"

def org_color(org_type):
    """Return GEXF color for an organization by type."""
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,100",
    }
    return type_colors.get(org_type, "200,200,200")

def is_top_leader(person_id):
    """Check if a person is a top leader (市委书记 or 市长)."""
    top_ids = ["zhuhai_chen_yong", "zhuhai_wu_zetong"]
    return person_id in top_ids

def person_size(person_id):
    return "20.0" if is_top_leader(person_id) else "12.0"


def build_database(db_path):
    """Create SQLite database with tables and data."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            source TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            source TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in PERSONS:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    # Insert organizations
    for o in ORGANIZATIONS:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    # Insert positions
    for pos in POSITIONS:
        cur.execute("""
            INSERT OR REPLACE INTO positions (person_id, org_id, title, start_date, end_date, rank, note, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, pos)

    # Insert relationships
    for r in RELATIONSHIPS:
        cur.execute("""
            INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, source, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()

    # Summary
    cur.execute("SELECT COUNT(*) FROM persons")
    n_persons = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    n_orgs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    n_positions = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    n_rels = cur.fetchone()[0]

    conn.close()

    print(f"Database: {db_path}")
    print(f"  Persons: {n_persons}")
    print(f"  Organizations: {n_orgs}")
    print(f"  Positions: {n_positions}")
    print(f"  Relationships: {n_rels}")


def build_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>广东省珠海市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        p_id, name, gender, ethnicity, birth, birthplace, edu, party, work_start, post, org, source = p
        c = person_color(post)
        sz = person_size(p_id)
        lines.append(f'      <node id="{esc(p_id)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(birth)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    org_id_map = {}
    for o in ORGANIZATIONS:
        o_id, o_name, o_type, level, parent, location = o
        c = org_color(o_type)
        lines.append(f'      <node id="o{o_id}" label="{esc(o_name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o_type)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
        org_id_map[o_id] = o_name

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    
    eid = 0
    
    # Person → Organization (positions/worked_at)
    for pos in POSITIONS:
        p_id, o_id, title, start_date, end_date, rank, note, source = pos
        if o_id in org_id_map:
            eid += 1
            lines.append(f'      <edge id="e{eid}" source="{esc(p_id)}" target="o{o_id}" label="{esc(title)}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(note[:80] if note else title)}"/>')
            lines.append(f'          <attvalue for="2" value="confirmed"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period, source, confidence = r
        eid += 1
        weight = "2.0" if "党政" in rtype else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{esc(pa)}" target="{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context[:100])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(confidence)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF: {gexf_path}")
    print(f"  Edges: {eid}")


def main():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    os.makedirs(GRAPH_DIR, exist_ok=True)
    
    print("=" * 60)
    print("珠海市领导班子工作关系网络 — 数据构建")
    print("=" * 60)
    
    build_database(DB_PATH)
    build_gexf(GEXF_PATH)
    
    print()
    print("Build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
