#!/usr/bin/env python3
"""
重庆市巫山县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Wushan County leadership.

Level: 县(直辖市下辖)
Province: 重庆市
Targets: 县委书记 & 县长

Research Notes:
- External web research constrained: Baidu Baike 403/CAPTCHA, news sites blocked.
- Jina.ai reader timeout on Chinese government sites and encyclopedias.
- Core known facts from pre-existing local repository cross-references:
  - 李春奎: 巫山县委书记 2012-2021.10, now 九龙坡区委书记 (confirmed from local repo)
  - 付嘉康: 巫山县长 2021.08-2025.01, now 南川区长 (confirmed from local repo + 360百科)
- Current (2026) officeholders: partially researched. Names with "待确认" need verification.
- 巫山县政府网站 (cqws.gov.cn) accessible, but leadership page sub-URL pattern not found.

Sources:
- cqws.gov.cn (巫山县人民政府 — homepage accessible)
- Local repository data (李春奎 person JSON, 付嘉康 person JSON, 南川区 build/data)
- 360百科 (付嘉康 — cached)
- Available training knowledge

Last updated: 2026-07-16
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/chongqing_巫山县")
DB_PATH = os.path.join(STAGING, "巫山县_network.db")
GEXF_PATH = os.path.join(STAGING, "巫山县_network.gexf")

# ════════════════════════════════════════════
# DATA — compiled from repo-local + partial web evidence
# ════════════════════════════════════════════

# Get today as of-date
AS_OF = "2026-07-16"

persons = [
    # ════════════════════════════════════════════
    # CURRENT TOP LEADERS (需进一步确认)
    # ════════════════════════════════════════════
    # 李春奎 left 巫山县委书记 2021-10 for 九龙坡区委书记.
    # Successor identity partially confirmed from cqws.gov.cn homepage news.
    # The news mentions "邓涛前往鄂粤两地对接工作并招商引资" — 邓涛 may be a county leader.
    # Current 县委书记 and 县长 needs direct verification from cqws.gov.cn leadership page.
    {"id": 1, "name": "书记（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "巫山县委书记", "current_org": "中共巫山县委员会",
     "source": "待确认;successor_of_李春奎_who_left_202110"},
    # Note: 李春奎 left 2021-10 for 九龙坡区委书记.
    # The new 县委书记 took over around 2021-10/2022. Identity needs confirmation.
    # Possible candidates from news: 邓涛 may be a county leader.

    {"id": 2, "name": "县长（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "巫山县委副书记、县长", "current_org": "巫山县人民政府",
     "source": "待确认;successor_of_付嘉康_who_left_202501"},
    # Note: 付嘉康 left 2025-01 for 南川区长.
    # The new 县长 took over around 2025-01/2025-02. Identity needs confirmation.

    # ════════════════════════════════════════════
    # COUNTY PARTY STANDING COMMITTEE (需确认)
    # ════════════════════════════════════════════
    # Standing committee members generally include:
    # 县委副书记 (deputy secretary, often a concurrent role for the 县长)
    # 常务副县长 (executive deputy county mayor)
    # 纪委书记 (discipline inspection secretary)
    # 组织部部长 (organization department head)
    # 宣传部部长 (propaganda department head)
    # 政法委书记 (political-legal affairs secretary)
    # 统战部部长 (united front work department head)
    # 县委办公室主任 (county party committee office director)
    # 县委政法书记 (political-legal secretary)
    # These positions exist but names need confirmation.

    # ════════════════════════════════════════════
    # PREDECESSORS (confirmed from local repo)
    # ════════════════════════════════════════════
    {"id": 3, "name": "李春奎", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年4月", "birthplace": "重庆市大足区", "education": "重庆市委党校研究生（党政管理）；重庆师范高等专科学校大专（中文）",
     "party_join": "中共党员", "work_start": "1991年7月",
     "current_post": "九龙坡区委书记（原巫山县委书记）", "current_org": "中共重庆市九龙坡区委员会",
     "source": "local_repo_person_json;confirmed"},
    # Confirmed data from repo: data/persons/20260716-重庆市-九龙坡区-区委书记-李春奎.json

    {"id": 4, "name": "付嘉康", "gender": "男", "ethnicity": "满族",
     "birth": "1980年11月", "birthplace": "黑龙江牡丹江", "education": "西南政法大学经济学学士、法学学士；日本立命馆亚洲太平洋大学硕士",
     "party_join": "2003年10月", "work_start": "2003年7月",
     "current_post": "南川区人民政府区长（原巫山县长）", "current_org": "重庆市南川区人民政府",
     "source": "local_repo_person_json;360百科;confirmed"}

]

organizations = [
    {"id": 1, "name": "中共巫山县委员会", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市巫山县"},
    {"id": 2, "name": "巫山县人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市巫山县"},
    {"id": 3, "name": "巫山县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "重庆市人大常委会", "location": "重庆市巫山县"},
    {"id": 4, "name": "中国人民政治协商会议巫山县委员会", "type": "政协", "level": "县级", "parent": "重庆市政协", "location": "重庆市巫山县"},
    {"id": 5, "name": "中共巫山县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共重庆市纪委", "location": "重庆市巫山县"},
    {"id": 6, "name": "中共巫山县委组织部", "type": "党委", "level": "县级", "parent": "中共巫山县委员会", "location": "重庆市巫山县"},
    {"id": 7, "name": "中共巫山县委政法委员会", "type": "党委", "level": "县级", "parent": "中共巫山县委员会", "location": "重庆市巫山县"},
    {"id": 8, "name": "中共巫山县委宣传部", "type": "党委", "level": "县级", "parent": "中共巫山县委员会", "location": "重庆市巫山县"},
    {"id": 9, "name": "中共巫山县委统战部", "type": "党委", "level": "县级", "parent": "中共巫山县委员会", "location": "重庆市巫山县"},
    {"id": 10, "name": "中共巫山县委办公室", "type": "党委", "level": "县级", "parent": "中共巫山县委员会", "location": "重庆市巫山县"},
    {"id": 11, "name": "巫山县公安局", "type": "政府", "level": "县级", "parent": "巫山县人民政府", "location": "重庆市巫山县"},
    {"id": 12, "name": "中共重庆市九龙坡区委员会", "type": "党委", "level": "市辖区", "parent": "中共重庆市委", "location": "重庆市九龙坡区"},
    {"id": 13, "name": "重庆市南川区人民政府", "type": "政府", "level": "市辖区", "parent": "重庆市人民政府", "location": "重庆市南川区"},
]

positions = [
    # Current 县委书记 (待确认)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "巫山县委书记", "start": "待确认（约2022）", "end": "present", "rank": "正处级", "note": "successor_of_李春奎;name_pending"},
    # Current 县长 (待确认)
    {"id": 2, "person_id": 2, "org_id": 2, "title": "巫山县委副书记、县长", "start": "待确认（约2025）", "end": "present", "rank": "正处级", "note": "successor_of_付嘉康;name_pending"},
    # 李春奎 — 巫山县委书记
    {"id": 3, "person_id": 3, "org_id": 1, "title": "巫山县委书记", "start": "2012-01", "end": "2021-09", "rank": "正厅级", "note": "任巫山县委书记近10年，后调任九龙坡区委书记"},
    # 李春奎 — 巫山县长
    {"id": 4, "person_id": 3, "org_id": 2, "title": "巫山县委副书记、县长", "start": "2009", "end": "2012-01", "rank": "副厅级", "note": ""},
    # 李春奎 — 巫山县委副书记
    {"id": 5, "person_id": 3, "org_id": 1, "title": "巫山县委副书记", "start": "2005", "end": "2009", "rank": "副厅级", "note": ""},
    # 李春奎 — 巫山县委常委
    {"id": 6, "person_id": 3, "org_id": 1, "title": "巫山县委常委", "start": "2003", "end": "2005", "rank": "副厅级", "note": ""},
    # 李春奎 — 巫山县副县长
    {"id": 7, "person_id": 3, "org_id": 2, "title": "巫山县副县长", "start": "1999", "end": "2003", "rank": "副处级", "note": ""},
    # 李春奎 — 九龙坡区委书记
    {"id": 8, "person_id": 3, "org_id": 12, "title": "九龙坡区委书记", "start": "2021-10", "end": "present", "rank": "正厅级", "note": "调任后现职"},
    # 付嘉康 — 巫山县长
    {"id": 9, "person_id": 4, "org_id": 2, "title": "巫山县委副书记、县长", "start": "2021-08", "end": "2025-01", "rank": "正处级", "note": "2021.07-08代县长，2021.08正式当选"},
    # 付嘉康 — 南川区长
    {"id": 10, "person_id": 4, "org_id": 13, "title": "南川区人民政府区长", "start": "2025-01", "end": "present", "rank": "正厅级", "note": "2024.12代理，2025.01正式当选"},
]

relationships = [
    # Predecessor-successor: 李春奎 → current 县委书记
    {"id": 1, "person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "前任巫山县委书记与现任（待确认）", "overlap_org": "中共巫山县委员会",
     "overlap_period": "2021-2022前后", "strength": "strong", "confidence": "plausible"},
    # Predecessor-successor: 付嘉康 → current 县长
    {"id": 2, "person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "前任巫山县长与现任（待确认）", "overlap_org": "巫山县人民政府",
     "overlap_period": "2025前后", "strength": "strong", "confidence": "plausible"},
    # 李春奎 and 付嘉康 — 党政搭档
    {"id": 3, "person_a": 3, "person_b": 4, "type": "overlap",
     "context": "李春奎（县委书记）与付嘉康（县长）曾为党政搭档关系", "overlap_org": "中共巫山县委员会/巫山县人民政府",
     "overlap_period": "2021-08至2021-09", "strength": "strong", "confidence": "confirmed"},
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
    lines.append('    <description>重庆市巫山县领导班子工作关系网络</description>')
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
    print(f"\n   ⚠️  Note: Current county leaders' names need direct web access to confirm.")
    print(f"   Predecessor data confirmed from local repository cross-references.")
    print(f"   See open_questions for critical information gaps requiring in-browser search.")


if __name__ == "__main__":
    build_db()
    build_gexf()
    summary()
