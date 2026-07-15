#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 广丰区 (Guangfeng District) leadership network.

上饶市广丰区 — district-level administrative division of Shangrao City, Jiangxi Province.
广丰区原为广丰县，2015年撤县设区。

Targets: 区委书记 & 区长

⚠️ 网络环境限制：所有外部搜索工具（Exa/Baidu/Google/政府网站/维基百科）均不可达。
当前数据由仓库既有资料推断，核心领导姓名和履历均待确认。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_广丰区")
DB_PATH = os.path.join(STAGING, "广丰区_network.db")
GEXF_PATH = os.path.join(STAGING, "广丰区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ── Current Party Secretary (区委书记) — 姓名待确认 ──
    {
        "id": 1,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广丰区委书记",
        "current_org": "中共上饶市广丰区委员会",
        "source": "⚠️ 所有外部搜索工具不可达，姓名完全未知。需访问 www.gfq.gov.cn 或上饶市任前公示确认。"
    },

    # ── Current District Mayor (区长) — 姓名待确认 ──
    {
        "id": 2,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广丰区区长",
        "current_org": "广丰区人民政府",
        "source": "⚠️ 所有外部搜索工具不可达，姓名完全未知。需访问 www.gfq.gov.cn 或上饶市任前公示确认。"
    },

    # ── 曾任广丰区领导（从现有仓库数据推断） ──
    # 根据 build_shangrao_data.py: 俞健（上饶市政协主席）出生地为"江西上饶广丰区"
    {
        "id": 3,
        "name": "俞健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-02",
        "birthplace": "江西上饶广丰区",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上饶市政协主席",
        "current_org": "政协上饶市委员会",
        "source": "build_shangrao_data.py — wikipedia/上饶市"
    },

    # ── City-level leadership (上饶市) ──
    {
        "id": 4,
        "name": "刘烁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "山东诸城",
        "education": "南开大学化学系化学专业+企业管理专业双学士",
        "party_join": "1991-02",
        "work_start": "1992-07",
        "current_post": "上饶市委书记",
        "current_org": "中共上饶市委员会",
        "source": "build_shangrao_data.py — https://zh.wikipedia.org/wiki/刘烁"
    },
    {
        "id": 5,
        "name": "李建涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "河南方城",
        "education": "研究生学历，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上饶市委副书记、市长",
        "current_org": "上饶市人民政府",
        "source": "build_shangrao_data.py — https://www.sr.gov.cn 领导之窗"
    },
    {
        "id": 6,
        "name": "李高兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "江西余干",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上饶市人大常委会主任",
        "current_org": "上饶市人大常委会",
        "source": "build_shangrao_data.py — wikipedia/上饶市"
    },
    {
        "id": 7,
        "name": "陈云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "江西南昌",
        "education": "江西师范大学",
        "party_join": "中共党员",
        "work_start": "1999-07",
        "current_post": "九江市委书记（2026年5月调任）",
        "current_org": "中共九江市委员会",
        "source": "build_shangrao_data.py — baike/陈云"
    },
    {
        "id": 8,
        "name": "邱向军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-02",
        "birthplace": "江西资溪",
        "education": "江西师范大学政教系本科/江西财经大学MBA/江西师范大学法学博士",
        "party_join": "1988-01",
        "work_start": "1990-07",
        "current_post": "江西省民政厅厅长",
        "current_org": "江西省民政厅",
        "source": "build_shangrao_data.py — wikipedia/邱向军"
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {"id": 1, "name": "中共上饶市广丰区委员会", "type": "党委", "level": "区级", "parent": "中共上饶市委员会", "location": "江西省上饶市广丰区"},
    {"id": 2, "name": "广丰区人民政府", "type": "政府", "level": "区级", "parent": "上饶市人民政府", "location": "江西省上饶市广丰区"},
    {"id": 3, "name": "广丰区人大常委会", "type": "人大", "level": "区级", "parent": "上饶市人大常委会", "location": "江西省上饶市广丰区"},
    {"id": 4, "name": "政协广丰区委员会", "type": "政协", "level": "区级", "parent": "政协上饶市委员会", "location": "江西省上饶市广丰区"},
    {"id": 5, "name": "中共上饶市委员会", "type": "党委", "level": "地级", "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 6, "name": "上饶市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西省上饶市"},
    {"id": 7, "name": "上饶市人大常委会", "type": "人大", "level": "地级", "parent": "江西省人大常委会", "location": "江西省上饶市"},
    {"id": 8, "name": "政协上饶市委员会", "type": "政协", "level": "地级", "parent": "政协江西省委员会", "location": "江西省上饶市"},
    {"id": 9, "name": "中共九江市委员会", "type": "党委", "level": "地级", "parent": "中共江西省委员会", "location": "江西省九江市"},
    {"id": 10, "name": "江西省民政厅", "type": "政府", "level": "省级", "parent": "江西省人民政府", "location": "江西省南昌市"},
]

# ── POSITIONS ──
positions = [
    # 广丰区委书记(1) - 【待确认】current party secretary
    {"id": 1, "person_id": 1, "org_id": 1, "title": "广丰区委书记", "start": "", "end": "", "rank": "正处级", "note": "⚠️ 姓名完全未知，需补充"},

    # 广丰区区长(2) - 【待确认】current mayor
    {"id": 2, "person_id": 2, "org_id": 2, "title": "广丰区区长", "start": "", "end": "", "rank": "正处级", "note": "⚠️ 姓名完全未知，需补充"},

    # 俞健(3) - current Shangrao CPPCC chairman, native of Guangfeng
    {"id": 3, "person_id": 3, "org_id": 8, "title": "上饶市政协主席", "start": "2021-10", "end": "", "rank": "正厅级", "note": "广丰区籍贯"},

    # 刘烁(4) - current Shangrao party secretary
    {"id": 4, "person_id": 4, "org_id": 5, "title": "上饶市委书记", "start": "2026-05", "end": "", "rank": "正厅级", "note": "2026年5月从萍乡调任"},
    {"id": 5, "person_id": 4, "org_id": 5, "title": "萍乡市委书记（前任）", "start": "2023-03", "end": "2026-05", "rank": "正厅级", "note": ""},

    # 李建涛(5) - current Shangrao mayor
    {"id": 6, "person_id": 5, "org_id": 6, "title": "上饶市委副书记、市长", "start": "2025-09", "end": "", "rank": "正厅级", "note": "跨省交流干部(河南→江西)"},

    # 李高兴(6) - Shangrao NPC Standing Committee chair
    {"id": 7, "person_id": 6, "org_id": 7, "title": "上饶市人大常委会主任", "start": "2022-12", "end": "", "rank": "正厅级", "note": ""},

    # 陈云(7) - former Shangrao party secretary
    {"id": 8, "person_id": 7, "org_id": 5, "title": "上饶市委书记（前任）", "start": "2021-12", "end": "2026-05", "rank": "正厅级", "note": ""},
    {"id": 9, "person_id": 7, "org_id": 9, "title": "九江市委书记", "start": "2026-05", "end": "", "rank": "正厅级", "note": ""},

    # 邱向军(8) - former Shangrao mayor
    {"id": 10, "person_id": 8, "org_id": 10, "title": "江西省民政厅厅长", "start": "2025-08", "end": "", "rank": "正厅级", "note": ""},
    {"id": 11, "person_id": 8, "org_id": 6, "title": "上饶市委副书记、市长（前任）", "start": "2021-12", "end": "2025-07", "rank": "正厅级", "note": ""},
]

# ── RELATIONSHIPS ──
relationships = [
    # 广丰区与原上饶市领导的关联
    {"person_a": 1, "person_b": 4, "type": "前后任上下级", "context": "广丰区委书记（待确认）与上饶市委书记刘烁为上下级关系（名义上）", "overlap_org": "上饶市", "overlap_period": "2026-05至今"},
    {"person_a": 2, "person_b": 5, "type": "前后任上下级", "context": "广丰区区长（待确认）与上饶市长李建涛为上下级关系（名义上）", "overlap_org": "上饶市", "overlap_period": "2025-09至今"},
    {"person_a": 3, "person_b": 1, "type": "同乡关联", "context": "俞健（上饶市政协主席）为广丰区籍贯，与广丰区委书记可能有同乡/工作关系", "overlap_org": "广丰区", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "党政搭档", "context": "刘烁（市委书记）与李建涛（市长）为上饶市党政一把手", "overlap_org": "上饶市", "overlap_period": "2026-05至今"},
    {"person_a": 7, "person_b": 4, "type": "前后任", "context": "陈云（2021-2026书记）→ 刘烁（2026年5月接任）", "overlap_org": "中共上饶市委员会", "overlap_period": "前后任"},
    {"person_a": 7, "person_b": 8, "type": "党政搭档（前）", "context": "陈云（书记）与邱向军（市长）在上饶搭班子约3年半", "overlap_org": "上饶市", "overlap_period": "2021-12至2025-07"},
    {"person_a": 8, "person_b": 5, "type": "前后任", "context": "邱向军（2021-2025市长）→ 李建涛（2025年9月接任）", "overlap_org": "上饶市人民政府", "overlap_period": "前后任"},
]


# =========================================================================
# HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "副" not in role.replace("常务副", ""):
        return "255,50,50"
    if "区长" in role and "副" not in role:
        return "50,100,255"
    if "市长" in role and "副" not in role:
        return "50,100,255"
    if "政协" in role:
        return "255,240,200"
    if "人大" in role:
        return "200,255,255"
    if "副区长" in role or "副市长" in role:
        return "80,140,230"
    return "100,100,100"


def person_size(p):
    role = p.get("current_post", "")
    if "区委书记" in role or "市委书记" in role:
        return "20.0"
    if "区长" in role or "市长" in role:
        return "18.0"
    if "政协" in role or "人大" in role:
        return "14.0"
    return "12.0"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    return "200,200,200"


# =========================================================================
# BUILD DATABASE
# =========================================================================

def create_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                   p["education"], p["party_join"], p["work_start"], p["current_post"],
                   p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for i, r in enumerate(relationships):
        c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (i + 1, r["person_a"], r["person_b"], r["type"], r["context"],
                   r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# =========================================================================
# BUILD GEXF
# =========================================================================

def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append('    <description>上饶市广丰区领导班子工作关系网络 — 2026年7月15日生成（⚠️ 部分数据待确认）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "role"), ("2", "birth"), ("3", "birthplace")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        label = esc(p["name"])
        role = esc(p["current_post"])
        birth = esc(p["birth"])
        birthplace = esc(p["birthplace"])
        c = person_color(p)
        sz = person_size(p)
        rgb = c.split(",")
        lines.append(f'      <node id="p{pid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{birth}"/>')
        lines.append(f'          <attvalue for="3" value="{birthplace}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"]
        label = esc(o["name"])
        otype = esc(o["type"])
        c = org_color(o)
        rgb = c.split(",")
        lines.append(f'      <node id="o{oid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="org"/>')
        lines.append(f'          <attvalue for="1" value="{otype}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = esc(pos["title"])
        start = esc(pos["start"])
        end = esc(pos["end"])
        rank = esc(pos["rank"])
        note = esc(pos["note"])
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{title}" type="directed">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{start}"/>')
        lines.append(f'          <attvalue for="2" value="{end}"/>')
        lines.append(f'          <attvalue for="3" value="{note}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = r["person_a"]
        b = r["person_b"]
        rtype = esc(r["type"])
        context = esc(r["context"])
        ov = esc(r["overlap_period"])
        is_strong = "党政" in str(r["type"]) or "前后任" in str(r["type"])
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = "2.5" if is_strong else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{rtype}" type="undirected">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{ov}"/>')
        lines.append(f'          <attvalue for="3" value="{context}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{thickness}"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


# =========================================================================
# STATS
# =========================================================================

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {cnt}")
        if table == "persons":
            pending = c.execute("SELECT COUNT(*) FROM persons WHERE source LIKE '%待确认%'").fetchone()[0]
            print(f"    └─ 待确认: {pending}, 已确认: {cnt - pending}")
    conn.close()


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  上饶市广丰区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n✅ Done.")
