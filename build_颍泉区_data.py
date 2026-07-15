#!/usr/bin/env python3
"""Build 颍泉区 (Yingquan District, Fuyang, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_颍泉区 (安徽阜阳市颍泉区 - 市辖区)

Confirmed officeholders (from project cross-references):
  - 赵群 served as 颍泉区委常委、副区长 until 2019-03 (confirmed from 颍东区 赵群 person JSON)
  - 区委书记: 刘万和 (training knowledge — needs web verification)
  - 区长: 时新 (training knowledge — needs web verification)

Predecessors:
  - 前任区委书记: 刘洪洁 (training knowledge — needs web verification)
  - 前任区长: 虞建斌 (training knowledge — needs web verification)

IMPORTANT: This data was built without web access (all Chinese government/Baidu sites blocked).
Core leader identities and career timelines need verification from:
  - https://baike.baidu.com/item/颍泉区
  - https://www.yingquan.gov.cn/zwgk/ldzc/
  - Baidu Baike entries for 刘万和, 时新, 刘洪洁, 虞建斌

Confidence: Only 赵群's role in 颍泉区 is confirmed from project data.
All other data is from training knowledge and marked "plausible".
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "颍泉区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "颍泉区_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 区委书记 刘万和（training knowledge — needs verification）
    {
        "id": "yingquan_liu_wanhe",
        "name": "刘万和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍泉区委书记",
        "current_org": "中共阜阳市颍泉区委员会",
        "source": "待查：百度百科/颍泉区政府网站",
        "notes": "training knowledge: 曾任颍泉区区长，后接任区委书记。具体任命时间待查。需从百度百科或官方任前公示确认。",
        "confidence": "plausible"
    },
    # 区长 时新（training knowledge — needs verification）
    {
        "id": "yingquan_shi_xin",
        "name": "时新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍泉区委副书记、区长",
        "current_org": "颍泉区人民政府",
        "source": "待查：百度百科/颍泉区政府网站",
        "notes": "training knowledge: 现任颍泉区区长。具体任命时间和履历待查。需从百度百科或官方任前公示确认。",
        "confidence": "plausible"
    },

    # ═══ Former Leaders (Predecessors) ═══

    # 前任区委书记 刘洪洁
    {
        "id": "yingquan_liu_hongjie",
        "name": "刘洪洁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原颍泉区委书记，已调离）",
        "current_org": "",
        "source": "待查：百度百科",
        "notes": "training knowledge: 曾任颍泉区委书记（~2018-2022/2023）。去向待查。",
        "confidence": "unverified"
    },
    # 前任区长 虞建斌
    {
        "id": "yingquan_yu_jianbin",
        "name": "虞建斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原颍泉区区长，已调离）",
        "current_org": "",
        "source": "待查：百度百科",
        "notes": "training knowledge: 曾任颍泉区区长。去向待查。",
        "confidence": "unverified"
    },

    # ═══ Cross-reference: 赵群 (曾任职颍泉区，confirmed from project data) ═══
    {
        "id": "yingquan_zhao_qun",
        "name": "赵群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "安徽临泉",
        "native_place": "安徽临泉",
        "education": "省委党校研究生",
        "party_join": "1999-11",
        "work_start": "1997",
        "current_post": "颍东区委书记（曾任颍泉区委常委、副区长）",
        "current_org": "中共阜阳市颍东区委员会",
        "source": "https://baike.baidu.com/item/%E8%B5%B5%E7%BE%A4/20614585",
        "notes": "1977年8月生，安徽临泉人。曾任阜阳市颍泉区委常委、副区长（至2019年3月）。2019年3月任阜阳市招商投资促进中心党组书记、主任。2022年4月任颍东区委书记。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": "yingquan_party_committee",
        "name": "中共阜阳市颍泉区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜阳市委",
        "location": "阜阳市颍泉区"
    },
    {
        "id": "yingquan_government",
        "name": "颍泉区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阜阳市人民政府",
        "location": "阜阳市颍泉区"
    },
    {
        "id": "yingquan_npc",
        "name": "阜阳市颍泉区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "阜阳市人大常委会",
        "location": "阜阳市颍泉区"
    },
    {
        "id": "yingquan_cppcc",
        "name": "阜阳市颍泉区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "阜阳市政协",
        "location": "阜阳市颍泉区"
    },
    {
        "id": "yingquan_cdc",
        "name": "中共阜阳市颍泉区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共阜阳市纪委",
        "location": "阜阳市颍泉区"
    },
    {
        "id": "fuyang_investment_promotion",
        "name": "阜阳市招商投资促进中心",
        "type": "政府",
        "level": "地级市",
        "parent": "阜阳市人民政府",
        "location": "阜阳市"
    },
    {
        "id": "yingdong_party_committee",
        "name": "中共阜阳市颍东区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜阳市委",
        "location": "阜阳市颍东区"
    },
    {
        "id": "fuyang_party",
        "name": "中共阜阳市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共安徽省委",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_government",
        "name": "阜阳市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省人民政府",
        "location": "阜阳市"
    },
]

positions = [
    # 刘万和
    ("yingquan_liu_wanhe", "yingquan_party_committee", "颍泉区委书记", "", "", "正处级", "主持区委全面工作。任职时间待查（training knowledge）"),
    ("yingquan_liu_wanhe", "yingquan_government", "颍泉区人民政府区长（前任）", "", "", "正处级", "training knowledge: 由区长转任区委书记。时间待查。"),

    # 时新
    ("yingquan_shi_xin", "yingquan_government", "颍泉区委副书记、区长", "", "", "正处级", "领导区政府全面工作。具体任命时间待查。"),

    # 刘洪洁（前任区委书记）
    ("yingquan_liu_hongjie", "yingquan_party_committee", "颍泉区委书记（原）", "", "", "正处级", "前任区委书记。去向待查。"),

    # 虞建斌（前任区长）
    ("yingquan_yu_jianbin", "yingquan_government", "颍泉区人民政府区长（原）", "", "", "正处级", "前任区长。去向待查。"),

    # 赵群（confirmed from project data）
    ("yingquan_zhao_qun", "yingquan_government", "颍泉区委常委、副区长", "", "2019-03", "副处级", ""),
    ("yingquan_zhao_qun", "fuyang_investment_promotion", "阜阳市招商投资促进中心党组书记、主任", "2019-03", "2022-04", "正处级", ""),
    ("yingquan_zhao_qun", "yingdong_party_committee", "颍东区委书记", "2022-04", "", "正处级", "主持区委全面工作"),
]

relationships = [
    # 刘万和 ↔ 时新（党政正职搭档）
    {
        "person_a": "yingquan_liu_wanhe",
        "person_b": "yingquan_shi_xin",
        "type": "party_government_leadership",
        "strength": "strong",
        "context": "区委书记与区长（党政正职搭档）",
        "overlap_org": "颍泉区四套班子",
        "overlap_period": "至今",
        "note": "plausible"
    },
    # 刘万和 ↔ 刘洪洁（前后任区委书记）
    {
        "person_a": "yingquan_liu_hongjie",
        "person_b": "yingquan_liu_wanhe",
        "type": "predecessor_successor",
        "strength": "strong",
        "context": "前后任区委书记",
        "overlap_org": "中共阜阳市颍泉区委员会",
        "overlap_period": "交接期",
        "note": "plausible"
    },
    # 虞建斌 ↔ 时新（前后任区长）
    {
        "person_a": "yingquan_yu_jianbin",
        "person_b": "yingquan_shi_xin",
        "type": "predecessor_successor",
        "strength": "strong",
        "context": "前后任区长",
        "overlap_org": "颍泉区人民政府",
        "overlap_period": "交接期",
        "note": "plausible"
    },
    # 刘万和 ↔ 虞建斌（区委书记与前任区长搭档期）
    {
        "person_a": "yingquan_liu_wanhe",
        "person_b": "yingquan_yu_jianbin",
        "type": "overlap",
        "strength": "medium",
        "context": "刘万和任区长期间可能与虞建斌有工作交集；或刘万和接任区长",
        "overlap_org": "颍泉区",
        "overlap_period": "未知",
        "note": "unverified"
    },
    # 赵群（原颍泉区副区长）↔ 时新（现任区长）
    {
        "person_a": "yingquan_zhao_qun",
        "person_b": "yingquan_shi_xin",
        "type": "overlap",
        "strength": "weak",
        "context": "赵群曾为颍泉区副区长，时新现任区长。时间线可能有交接",
        "overlap_org": "颍泉区人民政府",
        "overlap_period": "未知",
        "note": "unverified"
    },
    # 赵群 ↔ 刘万和（原颍泉区副区长与现任区委书记）
    {
        "person_a": "yingquan_zhao_qun",
        "person_b": "yingquan_liu_wanhe",
        "type": "overlap",
        "strength": "weak",
        "context": "赵群任颍泉区副区长时，刘万和可能在区任职",
        "overlap_org": "颍泉区",
        "overlap_period": "2019年前",
        "note": "unverified"
    },
]


# ══════════════════════════════════════════════════════════════════════
# Database + Graph Builder
# ══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b color string based on role."""
    name = p.get("current_post", "")
    if "区委书记" in name:
        return "255,50,50"
    elif "区长" in name:
        return "50,100,255"
    elif "纪委书记" in name or "纪委" in name:
        return "255,165,0"
    elif "人大" in name:
        return "200,255,255"
    elif "政协" in name:
        return "255,240,200"
    else:
        return "100,100,100"


def org_color(o):
    """Return r,g,b color string based on org type."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "纪委" in t:
        return "255,165,0"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "群团" in t:
        return "255,220,255"
    else:
        return "220,220,220"


def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DROP TABLE IF EXISTS relationships;")
    c.execute("DROP TABLE IF EXISTS positions;")
    c.execute("DROP TABLE IF EXISTS organizations;")
    c.execute("DROP TABLE IF EXISTS persons;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'unverified'
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            note TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
            p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"], p["current_org"],
            p["source"], p["notes"], p["confidence"]
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, org_id, title, start, end, rank, note))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["note"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>颍泉区（阜阳市）领导班子工作关系网络 — 2026年7月研究数据（部分数据待确认）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attribute declarations
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]
        birth = p["birth"]
        conf = p["confidence"]
        c = person_color(p)
        is_top = "区委书记" in post or ("区长" in post and "副书记" in post)
        sz = "20.0" if is_top else "12.0"

        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Nodes: organizations
    lines.append('    <nodes>')
    for o in organizations:
        oid = o["id"]
        oname = o["name"]
        c = org_color(o)
        lines.append(f'      <node id="org_{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person → organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        lines.append(f'      <edge id="e{eid}" source="{esc(person_id)}" target="org_{esc(org_id)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append(f'          <attvalue for="2" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person ↔ person (relationship)
    for r in relationships:
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


def print_summary():
    print(f"\n{'='*60}")
    print(f"  颍泉区领导班子工作关系网络")
    print(f"  生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"{'='*60}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"\n  ⚠ NOTE: 刘万和（区委书记）和时新（区长）的信息来自training knowledge")
    print(f"  ⚠ 需要在web可访问时通过以下URL核实：")
    print(f"     - https://baike.baidu.com/item/颍泉区")
    print(f"     - https://www.yingquan.gov.cn/zwgk/ldzc/")
    print(f"  ✅ 赵群曾担任颍泉区委常委、副区长（至2019年3月）—— 经项目现有数据确认")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
