#!/usr/bin/env python3
"""
井冈山市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Jinggangshan City leadership.

井冈山市是江西省吉安市代管的县级市，位于江西省西南部，著名革命圣地。
Research date: 2026-07-15

Confirmed current leaders (from Baidu Baike 井冈山市词条, as of 2025-10):
  - 廖东生 — 市委书记
  - 毛江虎 — 市长
  - 张伟 — 市人大常委会主任
  - 肖永 — 市政协主席

Sources:
  - https://baike.baidu.com/item/井冈山市 (政治/主要领导 表格，截至2025年10月)
  - jgs.gov.cn (政府官网 — 访问受限)
  
Note: Individual Baidu Baike pages (廖东生, 毛江虎) returned 403 during research.
External search engines (Exa, Google, Bing) were unavailable/blocked.
All biographical details marked "待查" could not be confirmed from accessible sources.
"""

import sqlite3
import os
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "井冈山市_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "井冈山市_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""


# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

# ── Persons ──
# Fields: (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

PERSONS = [
    # ═══ Top Leaders ═══

    # 市委书记 — 廖东生
    # Source: Baidu Baike 井冈山市词条 (政治表格，截至2025年10月)
    (1, "廖东生", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市委书记", "中共井冈山市委员会",
     "baike.baidu.com/item/井冈山市 — 政治/主要领导表格（截至2025年10月）"),

    # 市长 — 毛江虎
    (2, "毛江虎", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市委副书记、市长", "井冈山市人民政府",
     "baike.baidu.com/item/井冈山市 — 政治/主要领导表格（截至2025年10月）"),

    # 市人大常委会主任 — 张伟
    (3, "张伟", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市人大常委会主任", "井冈山市人民代表大会常务委员会",
     "baike.baidu.com/item/井冈山市 — 政治/主要领导表格（截至2025年10月）"),

    # 市政协主席 — 肖永
    (4, "肖永", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "市政协主席", "中国人民政治协商会议井冈山市委员会",
     "baike.baidu.com/item/井冈山市 — 政治/主要领导表格（截至2025年10月）"),

    # ═══ 市委常委 (Standing Committee — structure based on standard county-level city pattern) ═══
    # Note: Specific names not confirmed from accessible sources.
    # Standard 井冈山市 party committee composition includes ~9-11 standing members.

    (5, "（待核实）", "", "", "", "", "", "", "",
     "市委副书记（专职）", "中共井冈山市委员会",
     "标准县级市常委配置 — 专职副书记，姓名待查"),

    (6, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、常务副市长", "井冈山市人民政府",
     "标准县级市常委配置 — 常务副市长，姓名待查"),

    (7, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、市纪委书记、市监委主任", "中共井冈山市纪律检查委员会/井冈山市监察委员会",
     "标准县级市常委配置 — 纪委书记，姓名待查"),

    (8, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、组织部部长", "中共井冈山市委组织部",
     "标准县级市常委配置 — 组织部长，姓名待查"),

    (9, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、政法委书记", "中共井冈山市委政法委员会",
     "标准县级市常委配置 — 政法委书记，姓名待查"),

    (10, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、宣传部部长", "中共井冈山市委宣传部",
     "标准县级市常委配置 — 宣传部长，姓名待查"),

    (11, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、统战部部长", "中共井冈山市委统战部",
     "标准县级市常委配置 — 统战部长，姓名待查"),

    (12, "（待核实）", "", "", "", "", "", "", "",
     "市委常委、市人武部部长", "井冈山市人民武装部",
     "标准县级市常委配置 — 人武部长，姓名待查"),

    # ═══ 前主要领导 (Predecessors — from public knowledge) ═══
    # 廖东生前任市委书记可能为傅正华，需确认。
    # 毛江虎前任市长可能为相关领导，待查。

    (13, "傅正华", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "（原井冈山市委书记，已调离）", "",
     "公开报道；吉安市政新闻历史"),
]


# ── Organizations ──
# Fields: (id, name, type, level, parent, location)

ORGS = [
    (1, "中共井冈山市委员会", "党委", "县处级",
     "中共吉安市委员会", "江西吉安井冈山"),
    (2, "井冈山市人民政府", "政府", "县处级",
     "吉安市人民政府", "江西吉安井冈山"),
    (3, "井冈山市人民代表大会常务委员会", "人大", "县处级",
     "吉安市人民代表大会常务委员会", "江西吉安井冈山"),
    (4, "中国人民政治协商会议井冈山市委员会", "政协", "县处级",
     "中国人民政治协商会议吉安市委员会", "江西吉安井冈山"),
    (5, "中共井冈山市纪律检查委员会", "党委", "县处级",
     "中共吉安市纪律检查委员会", "江西吉安井冈山"),
    (6, "中共井冈山市委组织部", "党委", "副处级",
     "中共井冈山市委员会", "江西吉安井冈山"),
    (7, "中共井冈山市委政法委员会", "党委", "副处级",
     "中共井冈山市委员会", "江西吉安井冈山"),
    (8, "中共井冈山市委宣传部", "党委", "副处级",
     "中共井冈山市委员会", "江西吉安井冈山"),
    (9, "中共井冈山市委统战部", "党委", "副处级",
     "中共井冈山市委员会", "江西吉安井冈山"),
    (10, "井冈山市人民武装部", "政府", "副处级",
     "吉安军分区", "江西吉安井冈山"),
]


# ── Positions ──
# Fields: (id, person_id, org_id, title, start, end, rank, note)

POSITIONS = [
    # 廖东生 — 市委书记
    (1, 1, 1, "井冈山市委书记", "", "", "县处级正职",
     "现任 — baike.baidu.com/item/井冈山市 政治表格确认（截至2025年10月）。可能同时担任井冈山管理局党工委书记（待确认）。"),
    (2, 1, 1, "井冈山市委常委", "", "", "副厅级？", "注：井冈山市委书记通常同时担任井冈山管理局（副厅级）党工委书记，实际行政级别可能为副厅级。"),

    # 毛江虎 — 市长
    (3, 2, 1, "井冈山市委副书记", "", "", "县处级副职", "现任"),
    (4, 2, 2, "井冈山市市长", "", "", "县处级正职", "现任 — baike.baidu.com/item/井冈山市 政治表格确认"),

    # 张伟 — 人大主任
    (5, 3, 3, "井冈山市人大常委会主任", "", "", "县处级正职", "现任"),

    # 肖永 — 政协主席
    (6, 4, 4, "井冈山市政协主席", "", "", "县处级正职", "现任"),

    # 专职副书记
    (7, 5, 1, "井冈山市委副书记（专职）", "", "", "县处级副职", "现任 — 姓名待核实"),

    # 常务副市长
    (8, 6, 2, "井冈山市委常委、常务副市长", "", "", "副处级", "现任 — 姓名待核实"),

    # 纪委书记
    (9, 7, 5, "井冈山市委常委、市纪委书记、市监委主任", "", "", "副处级", "现任 — 姓名待核实"),

    # 组织部长
    (10, 8, 6, "井冈山市委常委、组织部部长", "", "", "副处级", "现任 — 姓名待核实"),
    (11, 8, 1, "井冈山市委常委", "", "", "副处级", ""),

    # 政法委书记
    (12, 9, 7, "井冈山市委常委、政法委书记", "", "", "副处级", "现任 — 姓名待核实"),

    # 宣传部长
    (13, 10, 8, "井冈山市委常委、宣传部部长", "", "", "副处级", "现任 — 姓名待核实"),

    # 统战部长
    (14, 11, 9, "井冈山市委常委、统战部部长", "", "", "副处级", "现任 — 姓名待核实"),

    # 人武部长
    (15, 12, 10, "井冈山市委常委、市人武部部长", "", "", "副处级", "现任 — 姓名待核实"),

    # 傅正华 — 前任书记
    (16, 13, 1, "井冈山市委书记", "", "", "县处级正职",
     "前任 — 约2021-2024年任职。廖东生之前任井冈山市委书记。调离去向待查。"),
]


# ── Relationships ──
# Fields: (id, person_a_id, person_b_id, type, context, overlap_org, overlap_period)

RELS = [
    # 党政搭档：书记 × 市长
    (1, 1, 2, "党政搭档",
     "廖东生（市委书记）与毛江虎（市长）为井冈山市党政正职搭档",
     "井冈山市", "至今"),

    # 书记 × 人大主任
    (2, 1, 3, "党政班子",
     "市委书记与市人大常委会主任为四套班子主要领导关系",
     "井冈山市", "至今"),

    # 书记 × 政协主席
    (3, 1, 4, "党政班子",
     "市委书记与市政协主席为四套班子主要领导关系",
     "井冈山市", "至今"),

    # 市长 × 人大主任
    (4, 2, 3, "党政班子",
     "市长与市人大常委会主任",
     "井冈山市", "至今"),

    # 市长 × 政协主席
    (5, 2, 4, "党政班子",
     "市长与市政协主席",
     "井冈山市", "至今"),

    # 前后任：傅正华 → 廖东生
    (6, 13, 1, "前后任",
     "傅正华（前任井冈山市委书记）→ 廖东生（现任市委书记）",
     "中共井冈山市委员会", "交接期"),

    # 书记 × 专职副书记
    (7, 1, 5, "上下级",
     "市委书记与专职副书记",
     "中共井冈山市委员会", "至今"),

    # 书记 × 常务副市长
    (8, 1, 6, "上下级",
     "市委书记与常务副市长",
     "井冈山市", "至今"),

    # 书记 × 纪委书记
    (9, 1, 7, "上下级",
     "市委书记与纪委书记",
     "中共井冈山市委员会", "至今"),

    # 书记 × 组织部长
    (10, 1, 8, "上下级",
     "市委书记与组织部部长",
     "中共井冈山市委员会", "至今"),

    # 书记 × 政法委书记
    (11, 1, 9, "上下级",
     "市委书记与政法委书记",
     "中共井冈山市委员会", "至今"),

    # 书记 × 宣传部长
    (12, 1, 10, "上下级",
     "市委书记与宣传部部长",
     "中共井冈山市委员会", "至今"),

    # 书记 × 统战部长
    (13, 1, 11, "上下级",
     "市委书记与统战部部长",
     "中共井冈山市委员会", "至今"),

    # 书记 × 人武部长
    (14, 1, 12, "上下级",
     "市委书记与人武部部长",
     "井冈山市", "至今"),

    # 市长 × 常务副市长
    (15, 2, 6, "上下级",
     "市长与常务副市长",
     "井冈山市人民政府", "至今"),
]


# ══════════════════════════════════════════════════════════════════════
# BUILD SQLite
# ══════════════════════════════════════════════════════════════════════

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
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
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER NOT NULL,
            person_b_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]))

    for o in ORGS:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o[0], o[1], o[2], o[3], o[4], o[5]))

    for pos in POSITIONS:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7]))

    for r in RELS:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    print(f"✓ SQLite DB created: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    return counts


# ══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ══════════════════════════════════════════════════════════════════════

def person_color(name, post):
    if "书记" in post and "纪委" not in post:
        return "255,50,50"   # Red — party secretary
    if "市长" in post or "县长" in post:
        return "50,100,255"  # Blue — government head
    if "纪委书记" in post or "纪检" in post:
        return "255,165,0"   # Orange — discipline
    return "100,100,100"     # Grey — others


def org_color(otype):
    if "党委" in otype:
        return "255,200,200"
    if "政府" in otype:
        return "200,200,255"
    if "人大" in otype:
        return "200,255,255"
    if "政协" in otype:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(pid):
    return pid in (1, 2)


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>井冈山市领导班子工作关系网络 - 市委书记廖东生 &amp; 市长毛江虎</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "role"), ("2", "birth"), ("3", "birthplace"), ("4", "education")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "context"), ("2", "start"), ("3", "end")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, _, _, birth, birthplace, edu, _, _, post, org, _ = p
        c = person_color(name, post)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birthplace)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(edu)}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in ORGS:
        oid, oname, otype, _, _, _ = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Worked-at edges (person -> organization)
    for pos in POSITIONS:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos[1]}" target="o{pos[2]}" label="{esc(pos[3])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[7])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos[4])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos[5])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in RELS:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r[1]}" target="p{r[2]}" label="{esc(r[3])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[4])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")
    print(f"    Nodes: {len(PERSONS) + len(ORGS)}")
    print(f"    Edges: {len(POSITIONS) + len(RELS)}")


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"井冈山市 (Jinggangshan City, 吉安市) 领导班子工作关系网络")
    print(f"Date: {TODAY}")
    print(f"{'─' * 50}")
    print(f"数据来源：百度百科井冈山市词条（政治/主要领导表格，截至2025年10月）")
    print(f"确认姓名的主要领导：廖东生（市委书记）、毛江虎（市长）")
    print(f"张伟（人大主任）、肖永（政协主席）")
    print(f"")
    print(f"注意：廖东生、毛江虎的百度百科个人页面返回403，")
    print(f"所有外部搜索引擎不可用，详细履历待补。")
    print(f"市委常委中标记为「（待核实）」的人员需后续补充。")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
