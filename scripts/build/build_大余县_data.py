#!/usr/bin/env python3
"""
Build 大余县 (Dayu County, 赣州市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

大余县 is a county under 赣州市, Jiangxi Province.
Current as of: 2026-07-15

Targets: 县委书记 & 县长
Core figures: 韩相云 (县委书记), 曾志平 (县委副书记、县长)

Official leadership page: https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/
Leadership members listed on gov site: 曾志平, 王勤, 张桂成, 欧自刚, 曾毅, 黄龙国, 曾琦, 谢光胜, 陈龙
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
# When in data/tmp/jiangxi_大余县/, BASE resolves to that dir
if "data/tmp" in BASE:
    REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
else:
    REPO_ROOT = BASE

today = datetime.now().strftime("%Y-%m-%d")

DB_REL = "data/database/大余县_network.db"
GEXF_REL = "data/graph/大余县_network.gexf"

DB_PATH = os.path.join(REPO_ROOT, DB_REL)
GEXF_PATH = os.path.join(REPO_ROOT, GEXF_REL)

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ===== Core leaders =====
    {
        "id": 1,
        "name": "韩相云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "江西寻乌",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1995-08",
        "current_post": "大余县委书记",
        "current_org": "中共大余县委员会",
        "source": "https://www.jxdy.gov.cn; https://baike.baidu.com/item/韩相云/64736440",
    },
    {
        "id": 2,
        "name": "曾志平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-05",
        "birthplace": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县委副书记、县长",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn",
    },
    # ===== Leadership team (listed on official gov site) =====
    {
        "id": 3,
        "name": "王勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县委常委、县政府领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 4,
        "name": "张桂成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县委常委、县政府领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 5,
        "name": "欧自刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 6,
        "name": "曾毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 7,
        "name": "黄龙国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 8,
        "name": "曾琦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 9,
        "name": "谢光胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
    {
        "id": 10,
        "name": "陈龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大余县领导",
        "current_org": "大余县人民政府",
        "source": "https://www.jxdy.gov.cn/zwgk/fdzdgknr/ldxx/",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共大余县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共赣州市委员会",
        "location": "江西赣州大余",
    },
    {
        "id": 2,
        "name": "大余县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "赣州市人民政府",
        "location": "江西赣州大余",
    },
    {
        "id": 3,
        "name": "中共大余县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大余县委员会",
        "location": "江西赣州大余",
    },
    {
        "id": 4,
        "name": "大余县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "大余县",
        "location": "江西赣州大余",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议大余县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "大余县",
        "location": "江西赣州大余",
    },
    {
        "id": 6,
        "name": "中共寻乌县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共赣州市委员会",
        "location": "江西赣州寻乌",
    },
    {
        "id": 7,
        "name": "寻乌县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "赣州市人民政府",
        "location": "江西赣州寻乌",
    },
]

positions = [
    # 韩相云 - 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "大余县委书记", "start": "2021-08", "end": "", "rank": "县处级正职",
     "note": "现任。此前担任大余县委副书记、县长"},
    # 韩相云 - previous roles
    {"id": 2, "person_id": 1, "org_id": 2, "title": "大余县委副书记、县长", "start": "2020-06", "end": "2021-08", "rank": "县处级正职",
     "note": "任县长后升任县委书记"},
    {"id": 3, "person_id": 1, "org_id": 7, "title": "寻乌县副县长", "start": "2013", "end": "2016", "rank": "县处级副职",
     "note": "早期在寻乌县工作"},
    {"id": 4, "person_id": 1, "org_id": 6, "title": "寻乌县委常委、政法委书记", "start": "2016", "end": "2020-03", "rank": "县处级副职",
     "note": ""},
    # 曾志平 - 县长
    {"id": 5, "person_id": 2, "org_id": 2, "title": "大余县委副书记、县长", "start": "2021-08", "end": "", "rank": "县处级正职",
     "note": "现任。接替韩相云任县长"},
    # 王勤
    {"id": 6, "person_id": 3, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 张桂成
    {"id": 7, "person_id": 4, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 欧自刚
    {"id": 8, "person_id": 5, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 曾毅
    {"id": 9, "person_id": 6, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 黄龙国
    {"id": 10, "person_id": 7, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 曾琦
    {"id": 11, "person_id": 8, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 谢光胜
    {"id": 12, "person_id": 9, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
    # 陈龙
    {"id": 13, "person_id": 10, "org_id": 2, "title": "大余县政府领导", "start": "", "end": "", "rank": "县处级副职",
     "note": "在官方领导名单中"},
]

relationships = [
    # 韩相云 ↔ 曾志平
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "韩相云（县委书记）与曾志平（县长）为大余县党政正职搭档",
     "overlap_org": "大余县", "overlap_period": "2021至今"},
    # 韩相云 ↔ 曾志平 (predecessor-successor: 韩相云曾是县长, 曾志平接任县长)
    {"id": 2, "person_a_id": 1, "person_b_id": 2, "type": "接替关系",
     "context": "韩相云升任县委书记后，曾志平接替其县长职务",
     "overlap_org": "大余县", "overlap_period": "2021"},
]

# ===== Career timeline data for core figures (for person JSON) =====
han_xiangyun_career = [
    {"start": "1995-08", "end": "unknown", "org": "寻乌县", "title": "基层工作", "level": "", "location": "江西寻乌",
     "system": "government", "rank": "", "is_key_promotion": False, "notes": "早期履历未详",
     "confidence": "unverified", "source_ids": ["S001"]},
    {"start": "2013", "end": "2016", "org": "寻乌县人民政府", "title": "寻乌县副县长", "level": "县处级副职",
     "location": "江西寻乌", "system": "government", "rank": "副处级", "is_key_promotion": True,
     "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    {"start": "2016", "end": "2020-03", "org": "中共寻乌县委员会", "title": "寻乌县委常委、政法委书记",
     "level": "县处级副职", "location": "江西寻乌", "system": "party", "rank": "副处级",
     "is_key_promotion": True,
     "notes": "进入县委常委班子", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    {"start": "2020-03", "end": "2020-06", "org": "中共大余县委员会", "title": "大余县委副书记、代县长",
     "level": "县处级正职", "location": "江西赣州大余", "system": "government", "rank": "正处级",
     "is_key_promotion": True,
     "notes": "从寻乌调任大余，跨县提拔", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"start": "2020-06", "end": "2021-08", "org": "大余县人民政府", "title": "大余县委副书记、县长",
     "level": "县处级正职", "location": "江西赣州大余", "system": "government", "rank": "正处级",
     "is_key_promotion": False,
     "notes": "正式当选县长", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    {"start": "2021-08", "end": "present", "org": "中共大余县委员会", "title": "大余县委书记",
     "level": "县处级正职", "location": "江西赣州大余", "system": "party", "rank": "正处级",
     "is_key_promotion": True,
     "notes": "升任县委书记，党政一把手", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
]

zeng_zhiping_career = [
    {"start": "unknown", "end": "2021", "org": "赣州市直单位", "title": "前期工作",
     "level": "", "location": "江西赣州", "system": "government", "rank": "",
     "is_key_promotion": False, "notes": "早期履历待查",
     "confidence": "unverified", "source_ids": ["S003"]},
    {"start": "2021", "end": "2021-08", "org": "大余县人民政府", "title": "大余县委常委、副县长",
     "level": "县处级副职", "location": "江西赣州大余", "system": "government", "rank": "副处级",
     "is_key_promotion": True,
     "notes": "调任大余县", "confidence": "plausible", "source_ids": ["S003"]},
    {"start": "2021-08", "end": "present", "org": "大余县人民政府", "title": "大余县委副书记、县长",
     "level": "县处级正职", "location": "江西赣州大余", "system": "government", "rank": "正处级",
     "is_key_promotion": True,
     "notes": "接替韩相云任县长", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
]

# ── BUILD FUNCTIONS ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    post = post or ""
    if "书记" in post and ("县委" in post or "区委" in post):
        return "230,50,50"
    if "县长" in post or "区长" in post:
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    return "120,120,120"


def ocolor_viz(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(otype, "200,200,200")


def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
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

    return counts


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus</creator>')
    lines.append(f'    <description>大余县领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = pcolor_viz(p.get("current_post", ""))
        sz = "20.0" if p["id"] <= 2 else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")), ("2", p.get("birthplace", "")),
                      ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""), ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")), ("2", pos.get("end", "")),
                      ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("大余县 Government Personnel Network Builder")
    print(f"Date: {today}")
    print(f"Staging dir: {BASE}")
    print("=" * 60)

    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB file not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF file not created: {GEXF_PATH}")

    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE - All artifacts created successfully")
