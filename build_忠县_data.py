#!/usr/bin/env python3
"""
重庆市忠县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Zhong County leadership.

Level: 县(直辖市下辖) — 正处级
Province: 重庆市
Targets: 县委书记 & 县长

Research Notes:
- Web research constrained: zhongxian.gov.cn main page accessible but subpages 404;
  Baidu Baike 403/CAPTCHA; Chinese news sites blocked from this environment.
- Data compiled from available knowledge and cross-referenced with existing repo data.
- 江夏 as former 忠县 县长 (2016-2020) and 县委书记 (2020-2023-03) confirmed
  from 长寿区 person JSON (source: cqcs.gov.cn, ce.cn).
- Current leadership (post 2023-03) needs direct access to zhongxian.gov.cn leadership page
  and Chongqing Municipal Organization Department appointment notices.
- All claims marked with confidence levels. Gaps explicitly documented.

Known Succession Pattern:
- 江夏: 忠县 县长 (2016-2020) → 忠县 县委书记 (2020-2023-03) → 重庆市水利局局长 (2023-03) → 长寿区委书记 (2024-12)
- Current 县委书记 (post 江夏, since ~2023-03): needs confirmation
- Current 县长 (post 江夏 as 县长 in 2020): a new 县长 was appointed in 2020 when 江夏 became 书记

Sources:
- zhongxian.gov.cn (intended but subpages unreachable)
- Baidu Baike (403 blocked)
- cqcs.gov.cn (长寿区 data - confirms 江夏's 忠县 tenure)
- 中国经济网 ce.cn (江夏 appointment to 长寿区)
- Available training knowledge (confidence: plausible)

Last updated: 2026-07-16
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/chongqing_忠县")
DB_PATH = os.path.join(STAGING, "忠县_network.db")
GEXF_PATH = os.path.join(STAGING, "忠县_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

persons = [
    # ── Current Top Leaders (post 江夏 era) ──
    # Note: 江夏 served as 县委书记 until 2023-03, then transferred to 重庆市水利局.
    # The current 县委书记 succeeding 江夏 needs confirmation from official sources.
    {"id": 1, "name": "待确认", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "忠县县委书记（现任）", "current_org": "中共忠县委员会",
     "source": "待查 — 需从 zhongxian.gov.cn 领导之窗确认"},
    # Note: Successor of 江夏 as 县委书记. Possible candidates from media reports.
    # May be promoted from within 忠县 or transferred from another Chongqing district/county.

    # Note: 江夏 was 县长 before becoming 书记 in 2020. A new 县长 was appointed in 2020.
    # The current 县长 may have changed since then.
    {"id": 2, "name": "待确认", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "忠县县委副书记、县长（现任）", "current_org": "忠县人民政府",
     "source": "待查 — 需从 zhongxian.gov.cn 领导之窗确认"},

    # ── Former Leaders (confirmed from 长寿区 person JSON data) ──
    {"id": 3, "name": "江夏", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年9月", "birthplace": "重庆北碚", "education": "市委党校研究生/高级管理人员工商管理硕士",
     "party_join": "1996年12月", "work_start": "1990年7月",
     "current_post": "长寿区委书记（已调离忠县）", "current_org": "中共重庆市长寿区委员会",
     "source": "cqcs.gov.cn;中国经济网"},
    # 江夏: 忠县 县长 2016-2020, 忠县 县委书记 2020-2023-03

    # ── County Party Committee Standing Members (partial, needs confirmation) ──
    {"id": 4, "name": "待确认（县委副书记）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县县委副书记（待确认）", "current_org": "中共忠县委员会",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    {"id": 5, "name": "待确认（常务副县长）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县委常委、常务副县长（待确认）", "current_org": "忠县人民政府",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    {"id": 6, "name": "待确认（纪委书记）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县委常委、县纪委书记、县监委主任（待确认）", "current_org": "中共忠县纪律检查委员会",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    {"id": 7, "name": "待确认（组织部部长）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县委常委、组织部部长（待确认）", "current_org": "中共忠县委组织部",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    {"id": 8, "name": "待确认（宣传部部长）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县委常委、宣传部部长（待确认）", "current_org": "中共忠县委宣传部",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    {"id": 9, "name": "待确认（政法委书记）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县委常委、政法委书记（待确认）", "current_org": "中共忠县委政法委员会",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    {"id": 10, "name": "待确认（统战部部长）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县委常委、统战部部长（待确认）", "current_org": "中共忠县委统战部",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    # ── County People's Congress ──
    {"id": 11, "name": "待确认（县人大常委会主任）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县人大常委会主任（待确认）", "current_org": "忠县人民代表大会常务委员会",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},

    # ── County CPPCC ──
    {"id": 12, "name": "待确认（县政协主席）", "gender": "待查", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "忠县政协主席（待确认）", "current_org": "中国人民政治协商会议忠县委员会",
     "source": "待查 — 需从 zhongxian.gov.cn 确认"},
]

organizations = [
    {"id": 1, "name": "中共忠县委员会", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市忠县"},
    {"id": 2, "name": "忠县人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市忠县"},
    {"id": 3, "name": "忠县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "重庆市人大常委会", "location": "重庆市忠县"},
    {"id": 4, "name": "中国人民政治协商会议忠县委员会", "type": "政协", "level": "县级", "parent": "重庆市政协", "location": "重庆市忠县"},
    {"id": 5, "name": "中共忠县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共重庆市纪委", "location": "重庆市忠县"},
    {"id": 6, "name": "中共忠县委组织部", "type": "党委", "level": "县级", "parent": "中共忠县委员会", "location": "重庆市忠县"},
    {"id": 7, "name": "中共忠县委宣传部", "type": "党委", "level": "县级", "parent": "中共忠县委员会", "location": "重庆市忠县"},
    {"id": 8, "name": "中共忠县委政法委员会", "type": "党委", "level": "县级", "parent": "中共忠县委员会", "location": "重庆市忠县"},
    {"id": 9, "name": "中共忠县委统战部", "type": "党委", "level": "县级", "parent": "中共忠县委员会", "location": "重庆市忠县"},
    {"id": 10, "name": "中共忠县委办公室", "type": "党委", "level": "县级", "parent": "中共忠县委员会", "location": "重庆市忠县"},
    {"id": 11, "name": "忠县公安局", "type": "政府", "level": "县级", "parent": "忠县人民政府", "location": "重庆市忠县"},
]

positions = [
    # Current 县委书记 (needs confirmation)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "忠县县委书记（现任）", "start": "待查", "end": "present", "rank": "正处级", "note": "接替江夏（2023年3月离任）"},
    # Current 县长 (needs confirmation)
    {"id": 2, "person_id": 2, "org_id": 2, "title": "忠县县委副书记、县长（现任）", "start": "待查", "end": "present", "rank": "正处级", "note": "接替江夏（2020年任县委书记时换任）"},

    # 江夏 — former 县长 and 县委书记 (confirmed)
    {"id": 3, "person_id": 3, "org_id": 1, "title": "忠县县委书记（曾任）", "start": "2020", "end": "2023-03", "rank": "正厅级（高配）", "note": "confirmed from cqcs.gov.cn and ce.cn reports"},
    {"id": 4, "person_id": 3, "org_id": 2, "title": "忠县县委副书记、县长（曾任）", "start": "2016", "end": "2020", "rank": "副厅级", "note": "confirmed from cqcs.gov.cn"},

    # Deputy posts (needs confirmation)
    {"id": 5, "person_id": 4, "org_id": 1, "title": "忠县县委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    {"id": 6, "person_id": 5, "org_id": 2, "title": "忠县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    {"id": 7, "person_id": 6, "org_id": 5, "title": "忠县委常委、县纪委书记、县监委主任", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    {"id": 8, "person_id": 7, "org_id": 6, "title": "忠县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    {"id": 9, "person_id": 8, "org_id": 7, "title": "忠县委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    {"id": 10, "person_id": 9, "org_id": 8, "title": "忠县委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    {"id": 11, "person_id": 10, "org_id": 9, "title": "忠县委常委、统战部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "待确认"},
    # NPC and CPPCC
    {"id": 12, "person_id": 11, "org_id": 3, "title": "忠县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "待确认"},
    {"id": 13, "person_id": 12, "org_id": 4, "title": "忠县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": "待确认"},
]

relationships = [
    # 江夏 as former 县委书记 → 县长
    {"id": 1, "person_a": 3, "person_b": 2, "type": "predecessor_successor",
     "context": "江夏曾任忠县县长（2016-2020），现任县长接替江夏", "overlap_org": "忠县人民政府",
     "overlap_period": "前后任", "strength": "medium", "confidence": "plausible"},
    # 江夏 as former 县委书记 → current 县委书记
    {"id": 2, "person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "江夏曾任忠县县委书记（2020-2023-03），现任书记接替江夏", "overlap_org": "中共忠县委员会",
     "overlap_period": "前后任", "strength": "medium", "confidence": "plausible"},
    # Current 书记 ↔ 县长 relationship
    {"id": 3, "person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "当前县委书记与县长搭档关系（待确认）", "overlap_org": "中共忠县委员会/忠县人民政府",
     "overlap_period": "当前", "strength": "weak", "confidence": "unverified"},
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
    post = p["current_post"]
    if "书记" in post and "纪委" not in post and "副书记" not in post:
        return "255,50,50"
    if "县长" in post or "区长" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "副书记" in post:
        return "255,100,50"
    if "常委" in post or "部长" in post or "主任" in post:
        return "100,100,100"
    return "100,100,100"


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
    lines.append('    <description>重庆市忠县领导班子工作关系网络</description>')
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
    print(f"   Most current leadership fields marked '待查'/'待确认' require direct")
    print(f"   web access to zhongxian.gov.cn leadership page and Baidu Baike.")
    print(f"   Only 江夏's former tenure (as 县长 2016-2020, as 书记 2020-2023-03)")
    print(f"   is confirmed from cqcs.gov.cn and ce.cn sources.")
    print(f"   See person JSON files for detailed gap documentation.")


if __name__ == "__main__":
    build_db()
    build_gexf()
    summary()
