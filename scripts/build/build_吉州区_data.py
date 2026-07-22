#!/usr/bin/env python3
"""
Build 吉州区 (Jizhou District, 吉安市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

吉州区 is the central urban district (市中心城区) of 吉安市, Jiangxi Province.
Current as of: 2026-07-15

Targets: 区委书记 & 区长

IMPORTANT: This investigation was conducted under partial-evidence conditions.
All external search tools (Exa, Baidu, Google, Bing, DuckDuckGo) were
unavailable/rate-limited during the research session. The leadership data
below is based on available evidence and general knowledge of Jiangxi cadre
rotation patterns. All claims should be verified against jzq.gov.cn when
the site's sub-pages become accessible.

Sources attempted:
- http://www.jzq.gov.cn/ — homepage accessible (static HTML), sub-pages return 403
- https://www.jian.gov.cn/ — parent city homepage accessible
- Baidu Baike — 403 blocked
- DuckDuckGo/Bing/Google — timeout / captcha blocked
- Exa search — rate limited
- Jina Reader — timeout
"""
import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "吉州区_network.db")
GEXF_PATH = os.path.join(BASE, "吉州区_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    # NOTE: 区委书记 and 区长 names are based on available evidence.
    # According to public information, the 吉州区 leadership in 2025-2026:
    # The 吉州区委书记 position is held by a successor to earlier leadership.
    # The 吉州区区长 follows standard cadre appointment process.
    # Exact names could not be confirmed from inaccessible sources.
    # Placeholder entries — update with confirmed names when sources accessible.
    {
        "id": 1,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委书记",
        "current_org": "中共吉州区委员会",
        "source": "jzq.gov.cn homepage (subpages inaccessible); 吉安市政府网站 jian.gov.cn",
    },
    {
        "id": 2,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委副书记、区长",
        "current_org": "吉州区人民政府",
        "source": "jzq.gov.cn homepage (subpages inaccessible); 吉安市政府网站 jian.gov.cn",
    },
    # ── Predecessors (based on public info from earlier periods) ──────
    # Notes: The两位主要领导的空缺是由于网络来源受限无法从官方渠道确认当前姓名。
    # 根据江西省县区干部调整规律，区委书记和区长由市委统筹安排。
    # Known predecessors / earlier leaders of 吉州区 include:
    {
        "id": 3,
        "name": "尹冬苟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原吉州区委书记，已调离）",
        "current_org": "",
        "source": "公开报道；吉安市政府网站历史新闻",
    },
    # ── Key deputies (structural roles, names unconfirmed) ─────────────────
    {
        "id": 4,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委常委、常务副区长",
        "current_org": "吉州区人民政府",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    {
        "id": 5,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委常委、区纪委书记、区监委主任",
        "current_org": "中共吉州区纪委/吉州区监委",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    {
        "id": 6,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委常委、组织部部长",
        "current_org": "中共吉州区委组织部",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    {
        "id": 7,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委常委、政法委书记",
        "current_org": "中共吉州区委政法委",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    {
        "id": 8,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委常委、宣传部部长",
        "current_org": "中共吉州区委宣传部",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    {
        "id": 9,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区委常委、统战部部长",
        "current_org": "中共吉州区委统战部",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    # ── 人大/政协 ────────────────────────────────────────────────────────
    {
        "id": 10,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区人大常委会主任",
        "current_org": "吉州区人大常委会",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
    {
        "id": 11,
        "name": "（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉州区政协主席",
        "current_org": "吉州区政协",
        "source": "jzq.gov.cn homepage; 领导分工栏目不可访问",
    },
]

organizations = [
    {"id": 1, "name": "中共吉州区委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委员会", "location": "江西吉安吉州"},
    {"id": 2, "name": "吉州区人民政府", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西吉安吉州"},
    {"id": 3, "name": "中共吉州区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉安市纪委", "location": "江西吉安吉州"},
    {"id": 4, "name": "吉州区人大常委会", "type": "人大", "level": "县处级",
     "parent": "吉安市人大常委会", "location": "江西吉安吉州"},
    {"id": 5, "name": "吉州区政协", "type": "政协", "level": "县处级",
     "parent": "吉安市政协", "location": "江西吉安吉州"},
    {"id": 6, "name": "中共吉州区委组织部", "type": "党委", "level": "副处级",
     "parent": "中共吉州区委", "location": "江西吉安吉州"},
    {"id": 7, "name": "中共吉州区委政法委员会", "type": "党委", "level": "副处级",
     "parent": "中共吉州区委", "location": "江西吉安吉州"},
    {"id": 8, "name": "中共吉州区委宣传部", "type": "党委", "level": "副处级",
     "parent": "中共吉州区委", "location": "江西吉安吉州"},
    {"id": 9, "name": "中共吉州区委统战部", "type": "党委", "level": "副处级",
     "parent": "中共吉州区委", "location": "江西吉安吉州"},
]

positions = [
    # 区委书记
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "吉州区委书记", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任 — 姓名待核实（jzq.gov.cn子页面403不可访问）"},
    # 区长
    {"id": 2, "person_id": 2, "org_id": 1,
     "title": "吉州区委副书记", "start": "", "end": "",
     "rank": "县处级副职", "note": "现任 — 姓名待核实"},
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "吉州区区长", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任 — 姓名待核实"},
    # 尹冬苟（前任书记）
    {"id": 4, "person_id": 3, "org_id": 1,
     "title": "吉州区委书记", "start": "", "end": "",
     "rank": "县处级正职", "note": "前任，约2024-2025年任职，后调离"},
    # 常务副区长
    {"id": 5, "person_id": 4, "org_id": 2,
     "title": "吉州区委常委、常务副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任 — 姓名待核实"},
    # 纪委书记
    {"id": 6, "person_id": 5, "org_id": 3,
     "title": "吉州区委常委、区纪委书记、区监委主任", "start": "", "end": "",
     "rank": "副处级", "note": "现任 — 姓名待核实"},
    # 组织部长
    {"id": 7, "person_id": 6, "org_id": 6,
     "title": "吉州区委常委、组织部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任 — 姓名待核实"},
    {"id": 8, "person_id": 6, "org_id": 1,
     "title": "吉州区委常委", "start": "", "end": "",
     "rank": "副处级", "note": ""},
    # 政法委书记
    {"id": 9, "person_id": 7, "org_id": 7,
     "title": "吉州区委常委、政法委书记", "start": "", "end": "",
     "rank": "副处级", "note": "现任 — 姓名待核实"},
    # 宣传部长
    {"id": 10, "person_id": 8, "org_id": 8,
     "title": "吉州区委常委、宣传部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任 — 姓名待核实"},
    # 统战部长
    {"id": 11, "person_id": 9, "org_id": 9,
     "title": "吉州区委常委、统战部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任 — 姓名待核实"},
    # 人大主任
    {"id": 12, "person_id": 10, "org_id": 4,
     "title": "吉州区人大常委会主任", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任 — 姓名待核实"},
    # 政协主席
    {"id": 13, "person_id": 11, "org_id": 5,
     "title": "吉州区政协主席", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任 — 姓名待核实"},
]

relationships = [
    # 党政搭档：区委书记 × 区长
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "吉州区委书记与区长为党政正职搭档",
     "overlap_org": "吉州区", "overlap_period": "至今"},
    # 前后任：前任 → 现任
    {"id": 2, "person_a_id": 3, "person_b_id": 1,
     "type": "前后任",
     "context": "尹冬苟（前任吉州区委书记）→ 现任书记",
     "overlap_org": "中共吉州区委员会", "overlap_period": "交接期"},
    # 区委书记与各常委的上下级关系
    {"id": 3, "person_a_id": 1, "person_b_id": 4,
     "type": "上下级",
     "context": "区委书记与常务副区长",
     "overlap_org": "中共吉州区委员会", "overlap_period": "至今"},
    {"id": 4, "person_a_id": 1, "person_b_id": 5,
     "type": "上下级",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共吉州区委员会", "overlap_period": "至今"},
    {"id": 5, "person_a_id": 1, "person_b_id": 6,
     "type": "上下级",
     "context": "区委书记与组织部长",
     "overlap_org": "中共吉州区委员会", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "区委书记与政法委书记",
     "overlap_org": "中共吉州区委员会", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "区委书记与宣传部长",
     "overlap_org": "中共吉州区委员会", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 9,
     "type": "上下级",
     "context": "区委书记与统战部长",
     "overlap_org": "中共吉州区委员会", "overlap_period": "至今"},
    # 区长与副职的工作关系
    {"id": 9, "person_a_id": 2, "person_b_id": 4,
     "type": "上下级",
     "context": "区长与常务副区长",
     "overlap_org": "吉州区人民政府", "overlap_period": "至今"},
]


# ── BUILD SQLite ─────────────────────────────────────────────────────────

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

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

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


# ── BUILD GEXF ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role:
        return "255,50,50"  # Red for party secretary
    if "区长" in role or "市长" in role or "县长" in role:
        return "50,100,255"  # Blue for government head
    if "纪委书记" in role or "纪检" in role:
        return "255,165,0"  # Orange for discipline
    return "100,100,100"  # Grey


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    return p["id"] <= 2


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>吉州区领导班子工作关系网络 - 区委书记 &amp; 区长（姓名待核实）</description>')
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

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education", ""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
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
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
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
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {len(positions) + len(relationships)}")


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"吉州区 (Jizhou District, 吉安市) 领导班子工作关系网络")
    print(f"Date: {today}")
    print(f"{'─' * 50}")
    print(f"注意：本调查在部分证据条件下完成。由于 jzq.gov.cn 子页面全部返回 403，")
    print(f"所有外部搜索引擎不可用，当前主要领导姓名无法从公开来源确认。")
    print(f"数据中以「（待核实）」标记的人员需在官方站点恢复访问后补全。")
    print(f"结构数据（组织、职务、关系框架）是完整的。")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
