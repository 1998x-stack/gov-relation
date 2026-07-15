#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 贵池区 (Guichi District, Chizhou, Anhui) leadership network.

贵池区 — 安徽省池州市辖区, 池州市政治经济文化中心, 面积2516平方公里.
Research date: 2026-07-15
Sources: https://www.ahgc.gov.cn/ (贵池区人民政府官方网站 领导之窗)
"""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
STAGING = SCRIPT_DIR
DB_PATH = os.path.join(STAGING, "贵池区_network.db")
GEXF_PATH = os.path.join(STAGING, "贵池区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders: 区委书记 何刚 ──
    {"id": 1, "name": "何刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-02", "birthplace": "", "education": "省委党校研究生学历，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市委常委、贵池区委书记",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── Core Leaders: 区长 吴作知 ──
    {"id": 2, "name": "吴作知", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "", "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委副书记、区人民政府区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},

    # ── 张焕 - 区委副书记 ──
    {"id": 3, "name": "张焕", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委副书记",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 彭四平 - 区委常委 ──
    {"id": 4, "name": "彭四平", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 王阳明 - 区委常委、常务副区长 ──
    {"id": 5, "name": "王阳明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委、常务副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 林志 - 区委常委、副区长 ──
    {"id": 6, "name": "林志", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委、副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 刘慧 - 区委常委 ──
    {"id": 7, "name": "刘慧", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 谷畅霞 - 区委常委 ──
    {"id": 8, "name": "谷畅霞", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 陈龙 - 区委常委 ──
    {"id": 9, "name": "陈龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 陈志新 - 区委常委 ──
    {"id": 10, "name": "陈志新", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 方小亚 - 区委常委 ──
    {"id": 11, "name": "方小亚", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区委常委",
     "current_org": "中共贵池区委",
     "source": "https://www.ahgc.gov.cn/Leader/showList/1/0.html"},

    # ── 汪赛荣 - 副区长 ──
    {"id": 12, "name": "汪赛荣", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},

    # ── 柯卫国 - 副区长 ──
    {"id": 13, "name": "柯卫国", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},

    # ── 桂涛 - 副区长 ──
    {"id": 14, "name": "桂涛", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},

    # ── 胡士珍 - 副区长 ──
    {"id": 15, "name": "胡士珍", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},

    # ── 宋婷 - 副区长（挂职） ──
    {"id": 16, "name": "宋婷", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区副区长（挂职）",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},

    # ── 吴志龙 - 副区长 ──
    {"id": 17, "name": "吴志龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵池区副区长",
     "current_org": "贵池区人民政府",
     "source": "https://www.ahgc.gov.cn/Leader/showList/3/0.html"},
]

organizations = [
    {"id": 1, "name": "中共贵池区委", "type": "党委", "level": "市辖区", "parent": "中共池州市委", "location": "贵池区"},
    {"id": 2, "name": "贵池区人民政府", "type": "政府", "level": "市辖区", "parent": "池州市人民政府", "location": "贵池区"},
    {"id": 3, "name": "贵池区人大常委会", "type": "人大", "level": "市辖区", "parent": "池州市人大常委会", "location": "贵池区"},
    {"id": 4, "name": "贵池区政协", "type": "政协", "level": "市辖区", "parent": "池州市政协", "location": "贵池区"},
    {"id": 5, "name": "中共池州市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "池州市"},
    {"id": 6, "name": "池州市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "池州市"},
]

positions = [
    # 何刚 — 区委书记（兼任池州市委常委）
    {"person_id": 1, "org_id": 5, "title": "池州市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": 1, "org_id": 1, "title": "贵池区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "现任，截至2026年7月"},

    # 吴作知 — 区长
    {"person_id": 2, "org_id": 1, "title": "贵池区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "贵池区人民政府区长", "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026年7月"},

    # 张焕 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "贵池区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 彭四平 — 区委常委
    {"person_id": 4, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 王阳明 — 区委常委、常务副区长
    {"person_id": 5, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "贵池区常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 林志 — 区委常委、副区长
    {"person_id": 6, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "贵池区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 刘慧 — 区委常委
    {"person_id": 7, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 谷畅霞 — 区委常委
    {"person_id": 8, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈龙 — 区委常委
    {"person_id": 9, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈志新 — 区委常委
    {"person_id": 10, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 方小亚 — 区委常委
    {"person_id": 11, "org_id": 1, "title": "贵池区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 汪赛荣 — 副区长
    {"person_id": 12, "org_id": 2, "title": "贵池区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 柯卫国 — 副区长
    {"person_id": 13, "org_id": 2, "title": "贵池区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 桂涛 — 副区长
    {"person_id": 14, "org_id": 2, "title": "贵池区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 胡士珍 — 副区长
    {"person_id": 15, "org_id": 2, "title": "贵池区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 宋婷 — 副区长（挂职）
    {"person_id": 16, "org_id": 2, "title": "贵池区副区长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},

    # 吴志龙 — 副区长
    {"person_id": 17, "org_id": 2, "title": "贵池区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    # 何刚 — 吴作知: 书记与区长党政搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政搭档", "overlap_org": "中共贵池区委/贵池区人民政府",
     "overlap_period": "至今"},

    # 何刚 — 张焕: 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记", "overlap_org": "中共贵池区委",
     "overlap_period": "至今"},

    # 吴作知 — 王阳明: 区长与常务副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "贵池区人民政府",
     "overlap_period": "至今"},

    # 何刚 — 王阳明: 书记与常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委", "overlap_org": "中共贵池区委",
     "overlap_period": "至今"},

    # 吴作知 — 林志: 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "贵池区人民政府",
     "overlap_period": "至今"},

    # 何刚 — 张焕 — 吴作知: 常委会集体领导
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委常委会集体领导", "overlap_org": "中共贵池区委常委会",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区委常委会集体领导", "overlap_org": "中共贵池区委常委会",
     "overlap_period": "至今"},
]

# ═══════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════

def build_database():
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return color for person by role."""
    title = p.get("current_post", "")
    if "书记" in title and "纪委" not in title:
        return "255,50,50"  # Red for party secretary
    if "区长" in title or "县长" in title:
        return "50,100,255"  # Blue for government head
    if "常务副" in title:
        return "50,150,255"  # Light blue for executive deputy
    if "纪委" in title:
        return "255,165,0"   # Orange for discipline
    return "100,100,100"     # Grey for others

def is_top_leader(p):
    title = p.get("current_post", "")
    return ("书记" in title and "纪委" not in title) or ("区长" in title and "副" not in title)

def org_color(o):
    otype = o.get("type", "")
    if "党委" in otype:
        return "255,200,200"
    if "政府" in otype:
        return "200,200,255"
    if "人大" in otype:
        return "200,255,255"
    if "政协" in otype:
        return "255,240,200"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>贵池区领导班子关系网络 - Guichi District Leadership Network (2026-07-15)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        oid = o["id"]
        oc = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        notes = esc(pos.get("note", ""))
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{notes}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    build_database()
    build_gexf()
    print("Done!")
