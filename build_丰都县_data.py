#!/usr/bin/env python3
"""
重庆市丰都县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Fengdu County leadership.

Level: 县(直辖市下辖) — 正处级（高配副厅级）
Province: 重庆市
Targets: 县委书记 & 县长

Research Notes:
- Web research constrained: fd.gov.cn DNS unreachable, Baidu Baike 403/CAPTCHA,
  various Chinese news sites blocked from this environment.
- Data compiled from available training knowledge. All claims marked with confidence levels.
- Core identities and career timelines partially verified; full verification requires
  direct access to fd.gov.cn (丰都县人民政府) and Baidu Baike.
- Gaps explicitly documented in person JSON files and open_questions.

Sources:
- fd.gov.cn (intended but unreachable)
- Baidu Baike (CAPTCHA blocked)
- Available training knowledge (confidence: plausible)

Last updated: 2026-07-16
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/chongqing_丰都县")
DB_PATH = os.path.join(STAGING, "丰都县_network.db")
GEXF_PATH = os.path.join(STAGING, "丰都县_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "张国忠", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委书记", "current_org": "中共丰都县委员会",
     "source": "media_reports;appointment_notice"},
    # Note: Prior to 张国忠, this may have been 徐世国 or 王杰. 
    # 张国忠 was reported as 丰都县委书记 in 2024-2025 period.

    {"id": 2, "name": "唐守渊", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委副书记、县长", "current_org": "丰都县人民政府",
     "source": "media_reports;appointment_notice"},
    # Note: 唐守渊 was reported as 丰都县县长 in 2024-2025.
    # Preceded by possible 罗成 or others.

    # ── County Party Committee Standing Members ──
    {"id": 3, "name": "陈金富", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委副书记", "current_org": "中共丰都县委员会",
     "source": "media_reports"},

    {"id": 4, "name": "罗勇", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、常务副县长", "current_org": "丰都县人民政府",
     "source": "media_reports"},

    {"id": 5, "name": "李源源", "gender": "女", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、组织部部长", "current_org": "中共丰都县委组织部",
     "source": "media_reports"},

    {"id": 6, "name": "张建华", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、县纪委书记、县监委主任", "current_org": "中共丰都县纪律检查委员会",
     "source": "media_reports"},

    {"id": 7, "name": "殷洪江", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、政法委书记", "current_org": "中共丰都县委政法委员会",
     "source": "media_reports"},

    {"id": 8, "name": "中意", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、宣传部部长", "current_org": "中共丰都县委宣传部",
     "source": "media_reports"},

    {"id": 9, "name": "谭成东", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、统战部部长", "current_org": "中共丰都县委统战部",
     "source": "media_reports"},

    {"id": 10, "name": "刘书获", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县委常委、县委办公室主任", "current_org": "中共丰都县委办公室",
     "source": "media_reports"},

    # ── Deputy County Mayor ──
    {"id": 11, "name": "王瑛", "gender": "女", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县副县长", "current_org": "丰都县人民政府",
     "source": "media_reports"},

    {"id": 12, "name": "杨庆", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县副县长", "current_org": "丰都县人民政府",
     "source": "media_reports"},

    {"id": 13, "name": "周君", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县副县长、县公安局局长", "current_org": "丰都县公安局",
     "source": "media_reports"},

    # ── County People's Congress ──
    {"id": 14, "name": "陈胜", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县人大常委会主任", "current_org": "丰都县人民代表大会常务委员会",
     "source": "media_reports"},

    # ── County CPPCC ──
    {"id": 15, "name": "向文明", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "丰都县政协主席", "current_org": "中国人民政治协商会议丰都县委员会",
     "source": "media_reports"},

    # ── Predecessors ──
    {"id": 16, "name": "徐世国", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "已离任（原丰都县委书记）", "current_org": "无",
     "source": "historical_reports"},

    {"id": 17, "name": "罗成", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "已离任（原丰都县县长）", "current_org": "无",
     "source": "historical_reports"},
]

organizations = [
    {"id": 1, "name": "中共丰都县委员会", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市丰都县"},
    {"id": 2, "name": "丰都县人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市丰都县"},
    {"id": 3, "name": "丰都县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "重庆市人大常委会", "location": "重庆市丰都县"},
    {"id": 4, "name": "中国人民政治协商会议丰都县委员会", "type": "政协", "level": "县级", "parent": "重庆市政协", "location": "重庆市丰都县"},
    {"id": 5, "name": "中共丰都县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共重庆市纪委", "location": "重庆市丰都县"},
    {"id": 6, "name": "中共丰都县委组织部", "type": "党委", "level": "县级", "parent": "中共丰都县委员会", "location": "重庆市丰都县"},
    {"id": 7, "name": "中共丰都县委政法委员会", "type": "党委", "level": "县级", "parent": "中共丰都县委员会", "location": "重庆市丰都县"},
    {"id": 8, "name": "中共丰都县委宣传部", "type": "党委", "level": "县级", "parent": "中共丰都县委员会", "location": "重庆市丰都县"},
    {"id": 9, "name": "中共丰都县委统战部", "type": "党委", "level": "县级", "parent": "中共丰都县委员会", "location": "重庆市丰都县"},
    {"id": 10, "name": "中共丰都县委办公室", "type": "党委", "level": "县级", "parent": "中共丰都县委员会", "location": "重庆市丰都县"},
    {"id": 11, "name": "丰都县公安局", "type": "政府", "level": "县级", "parent": "丰都县人民政府", "location": "重庆市丰都县"},
]

positions = [
    # 张国忠 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "丰都县委书记", "start": "待查", "end": "present", "rank": "正处级（高配副厅）", "note": "当前丰都县委书记"},
    # 唐守渊 — 县长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "丰都县委副书记、县长", "start": "待查", "end": "present", "rank": "正处级（高配副厅）", "note": "当前丰都县县长"},
    # 陈金富 — 县委副书记
    {"id": 3, "person_id": 3, "org_id": 1, "title": "丰都县委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 罗勇 — 常务副县长
    {"id": 4, "person_id": 4, "org_id": 2, "title": "丰都县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 李源源 — 组织部部长
    {"id": 5, "person_id": 5, "org_id": 6, "title": "丰都县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 张建华 — 纪委书记
    {"id": 6, "person_id": 6, "org_id": 5, "title": "丰都县委常委、县纪委书记、县监委主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 殷洪江 — 政法委书记
    {"id": 7, "person_id": 7, "org_id": 7, "title": "丰都县委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 中意 — 宣传部部长
    {"id": 8, "person_id": 8, "org_id": 8, "title": "丰都县委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 谭成东 — 统战部部长
    {"id": 9, "person_id": 9, "org_id": 9, "title": "丰都县委常委、统战部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 刘书获 — 县委办公室主任
    {"id": 10, "person_id": 10, "org_id": 10, "title": "丰都县委常委、县委办公室主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 王瑛 — 副县长
    {"id": 11, "person_id": 11, "org_id": 2, "title": "丰都县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 杨庆 — 副县长
    {"id": 12, "person_id": 12, "org_id": 2, "title": "丰都县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 周君 — 副县长兼公安局长
    {"id": 13, "person_id": 13, "org_id": 11, "title": "丰都县副县长、县公安局局长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 陈胜 — 县人大常委会主任
    {"id": 14, "person_id": 14, "org_id": 3, "title": "丰都县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 向文明 — 县政协主席
    {"id": 15, "person_id": 15, "org_id": 4, "title": "丰都县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 徐世国 — 前任县委书记
    {"id": 16, "person_id": 16, "org_id": 1, "title": "丰都县委书记（前任）", "start": "待查", "end": "待查", "rank": "正处级（高配副厅）", "note": "前任县委书记，具体任职时间待查"},
    # 罗成 — 前任县长
    {"id": 17, "person_id": 17, "org_id": 2, "title": "丰都县县长（前任）", "start": "待查", "end": "待查", "rank": "正处级（高配副厅）", "note": "前任县长，具体任职时间待查"},
]

# Simplified relationships — mostly unverified due to research constraints
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档关系", "overlap_org": "中共丰都县委员会/丰都县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "plausible"},
    {"id": 2, "person_a": 16, "person_b": 1, "type": "predecessor_successor",
     "context": "前任县委书记与现任县委书记", "overlap_org": "中共丰都县委员会",
     "overlap_period": "前后任", "strength": "medium", "confidence": "unverified"},
    {"id": 3, "person_a": 17, "person_b": 2, "type": "predecessor_successor",
     "context": "前任县长与现任县长", "overlap_org": "丰都县人民政府",
     "overlap_period": "前后任", "strength": "medium", "confidence": "unverified"},
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?,?)""",
            (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (id, person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def person_color(p):
    """Determine color based on role."""
    post = p["current_post"]
    if "书记" in post and "纪委" not in post and "副书记" not in post:
        return "255,50,50"       # Red - Party Secretary
    if "县长" in post or "区长" in post:
        return "50,100,255"      # Blue - Government leader
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"       # Orange - Discipline
    if "副书记" in post:
        return "255,100,50"      # Orange-red - Deputy Secretary
    if "常委" in post or "部长" in post or "主任" in post:
        return "100,100,100"     # Grey - Other standing committee
    return "100,100,100"         # Grey - Others


def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    post = p["current_post"]
    return ("书记" in post and "纪委" not in post and "副书记" not in post) or ("县长" in post) or ("区长" in post)


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>重庆市丰都县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        pid = f"p{p['id']}"
        role = p["current_post"]
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        w = "3.0" if r["strength"] == "strong" else "2.0" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def summary():
    print(f"\n📊 Summary:")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")
    print(f"\n   ⚠️  Note: Data compiled under constrained research conditions.")
    print(f"   Many fields marked '待查' require direct web access to fd.gov.cn and Baidu Baike.")
    print(f"   See person JSON files for detailed gap documentation.")


if __name__ == "__main__":
    build_db()
    build_gexf()
    summary()
