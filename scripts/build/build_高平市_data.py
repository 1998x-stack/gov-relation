#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 高平市, 晋城市, 山西省."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/shanxi_高平市")
DB_PATH = os.path.join(TMP, "高平市_network.db")
GEXF_PATH = os.path.join(TMP, "高平市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "原健", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "高平市委书记", "current_org": "中共高平市委员会",
     "source": "https://www.sxgp.gov.cn"},
    {"id": 2, "name": "徐浩", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "高平市委副书记、市长", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn"},

    # ── Deputy Mayors (2026-05-29 appointed) ──
    {"id": 3, "name": "原亮亮", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市人民政府副市长", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},
    {"id": 4, "name": "段君毅", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市人民政府副市长", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},
    {"id": 5, "name": "冯秀梅", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市人民政府副市长", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},

    # ── Other Current / Mentioned Leaders ──
    {"id": 6, "name": "冯文虎", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市人民政府副市长", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xwzx_358/zwdt_362/202607/t20260724_2374736.shtml"},
    {"id": 7, "name": "李琳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市人民政府副市长", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xwzx_358/zwdt_362/202607/t20260725_2374771.shtml"},
    {"id": 8, "name": "原张晋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市领导", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xwzx_358/zwdt_362/202607/t20260724_2374736.shtml"},
    {"id": 9, "name": "向阳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "高平市人民政府副市长（挂职）", "current_org": "高平市人民政府",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202509/t20250904_2227540.html"},

    # ── Former Leaders / Deputies Removed ──
    {"id": 10, "name": "郑威剑", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原高平市人民政府副市长（免职）", "current_org": "",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},
    {"id": 11, "name": "邢军军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原高平市人民政府副市长（免职）", "current_org": "",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},
    {"id": 12, "name": "段晓军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原高平市人民政府副市长（免职）", "current_org": "",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},
    {"id": 13, "name": "牛振亮", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原高平市人民政府副市长（免职）", "current_org": "",
     "source": "https://www.sxgp.gov.cn/xxgk/rsxx_383/202605/t20260529_2354944.html"},
]

organizations = [
    {"id": 1, "name": "中共高平市委员会", "type": "党委", "level": "县处级", "parent": "中共晋城市委员会",
     "location": "山西省晋城市高平市"},
    {"id": 2, "name": "高平市人民政府", "type": "政府", "level": "县处级", "parent": "晋城市人民政府",
     "location": "山西省晋城市高平市"},
    {"id": 3, "name": "高平市人大常委会", "type": "人大", "level": "县处级", "parent": "晋城市人大常委会",
     "location": "山西省晋城市高平市"},
    {"id": 4, "name": "高平市政协", "type": "政协", "level": "县处级", "parent": "晋城市政协",
     "location": "山西省晋城市高平市"},
]

positions = [
    # 原健 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "高平市委书记",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "当前在职，截至2026年7月仍有公开活动报道"},

    # 徐浩 - 市长
    {"person_id": 2, "org_id": 2, "title": "高平市委副书记、市长",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "当前在职，截至2026年7月仍以市长身份公开活动"},

    # Deputy Mayors
    {"person_id": 3, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "2026-05-29", "end_date": "至今", "rank": "县处级副职",
     "note": "2026年5月29日高平市第七届人大常委会第四十七次会议任命"},
    {"person_id": 4, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "2026-05-29", "end_date": "至今", "rank": "县处级副职",
     "note": "2026年5月29日高平市第七届人大常委会第四十七次会议任命"},
    {"person_id": 5, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "2026-05-29", "end_date": "至今", "rank": "县处级副职",
     "note": "2026年5月29日高平市第七届人大常委会第四十七次会议任命"},
    {"person_id": 6, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "参与道路交通安全整治调研(2026-07-24)"},
    {"person_id": 7, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "参与市政府教育及停车难专题会议(2026-07-25)"},
    {"person_id": 8, "org_id": 2, "title": "高平市领导",
     "start_date": "", "end_date": "至今", "rank": "",
     "note": "参与道路交通安全调研(2026-07-24)"},
    {"person_id": 9, "org_id": 2, "title": "高平市人民政府副市长（挂职）",
     "start_date": "2025-09-04", "end_date": "至今（挂职一年）", "rank": "县处级副职",
     "note": "2025年9月4日高平市第七届人大常委会第四十一次会议任命，挂职一年"},

    # Former Deputy Mayors (removed 2026-05-29)
    {"person_id": 10, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "", "end_date": "2026-05-29", "rank": "县处级副职",
     "note": "2026年5月29日被免职"},
    {"person_id": 11, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "", "end_date": "2026-05-29", "rank": "县处级副职",
     "note": "2026年5月29日被免职"},
    {"person_id": 12, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "", "end_date": "2026-05-29", "rank": "县处级副职",
     "note": "2026年5月29日被免职"},
    {"person_id": 13, "org_id": 2, "title": "高平市人民政府副市长",
     "start_date": "", "end_date": "2026-05-29", "rank": "县处级副职",
     "note": "2026年5月29日被免职"},
]

relationships = [
    # 书记-市长工作搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "原健（市委书记）与徐浩（市长）为党政正职搭档",
     "overlap_org": "高平市", "overlap_period": "至今"},

    # 书记-副市长们
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "原健（市委书记）与冯文虎（副市长）共同调研交通安全",
     "overlap_org": "高平市", "overlap_period": "2026-07-24"},

    # 市长-副市长们
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "徐浩（市长）与李琳（副市长）参加市政府教育专题会议",
     "overlap_org": "高平市人民政府", "overlap_period": "2026-07-25"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "徐浩（市长）与冯文虎（副市长）参加市政府专题会议",
     "overlap_org": "高平市人民政府", "overlap_period": "2026-07-25"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "徐浩（市长）与段君毅（副市长）参加市政府专题会议",
     "overlap_org": "高平市人民政府", "overlap_period": "2026-07-25"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "市委书记" in post and "原" not in post:
        return "255,50,50"
    if "市长" in post and "原" not in post:
        return "50,100,255"
    if "原" in post:
        return "180,180,180"
    return "100,100,100"

def is_top_leader(p):
    return p["id"] in (1, 2)

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id,org_id,title,start_date,end_date,rank,note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a,person_b,type,context,overlap_org,overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"✓ Database: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>高平市领导班子工作关系网络 - 山西省晋城市高平市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
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
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # worked_at edges (person → organization) from positions
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # relationship edges (person ↔ person)
    for r in relationships:
        eid += 1
        w = "2.0" if r["type"] == "overlap" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}, Edges: {eid}")

if __name__ == "__main__":
    print(f"=== 高平市 数据构建 ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    build_db()
    build_gexf()
    print()
    print("Done.")