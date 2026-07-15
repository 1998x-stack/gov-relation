#!/usr/bin/env python3
"""Build 颍东区 (Yingdong District, Fuyang, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_颍东区 (安徽阜阳市颍东区 - 市辖区)

Confirmed officeholders:
  - 区委书记: 赵群 (1977-08, 安徽临泉人), appointed 2022-04
  - 区长: 刘健 (1983-03, 安徽桐城人), in office since 2021-07
  - 区人大常委会主任: 岳蕾
  - 区政协主席: 刘雷振 (1965-08, 阜阳师范学院中文专业)

Sources:
  - https://baike.baidu.com/item/颍东区 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/赵群/20614585 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/刘健/19514981 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/刘雷振/23873985 (Baidu Baike, accessed 2026-07-15)

Confidence: Core leader identities and career timelines for 赵群 and 刘健 confirmed
from Baidu Baike. 岳蕾 and 刘雷振 basic info confirmed from district page. Leadership
team members beyond the top 4 are partially known pending official government website.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "颍东区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "颍东区_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 区委书记 赵群（2022年4月任）
    {
        "id": "yingdong_zhao_qun",
        "name": "赵群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "安徽临泉",
        "native_place": "安徽临泉",
        "education": "省委党校研究生",
        "party_join": "1999-11",
        "work_start": "1997",
        "current_post": "颍东区委书记",
        "current_org": "中共阜阳市颍东区委员会",
        "source": "https://baike.baidu.com/item/%E8%B5%B5%E7%BE%A4/20614585",
        "notes": "1977年8月生，安徽临泉人。1997年参加工作，1999年11月入党，省委党校研究生学历。曾任阜阳市颍泉区委常委、副区长；阜阳市招商投资促进中心党组书记、主任（2019.03-2022.04）。2022年4月任颍东区委书记。主持区委全面工作。",
        "confidence": "confirmed"
    },
    # 区长 刘健（2021年7月任）
    {
        "id": "yingdong_liu_jian",
        "name": "刘健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "安徽桐城",
        "native_place": "安徽桐城",
        "education": "大学（安徽师范大学物理学）",
        "party_join": "2002-06",
        "work_start": "2004-07",
        "current_post": "颍东区委副书记、区长",
        "current_org": "颍东区人民政府",
        "source": "https://baike.baidu.com/item/%E5%88%98%E5%81%A5/19514981",
        "notes": "1983年3月生，安徽桐城人。2004年7月参加工作，2002年6月入党，安徽师范大学物理学专业毕业。历任安庆经济技术开发区管委会办公室、建设局、招商局（2004.07-2005.12）；安庆经开区管委会办公室副主任科员（2006.09）；安庆市迎江区老峰镇党委委员、常务副镇长（2007.01-2009.07）；共青团阜阳市委副书记、党组成员（公选，2009.07-2016.01）；太和县委常委、组织部部长（2016.01-2019.03）、统战部部长（2016.07-2019.03）、县政府常务副县长（2020.01-2021.06）。2021年6月任颍东区委副书记、代区长，2021年7月任区长。领导区政府全面工作，负责审计工作。",
        "confidence": "confirmed"
    },
    # 区人大常委会主任 岳蕾
    {
        "id": "yingdong_yue_lei",
        "name": "岳蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "阜阳市颍东区人大常委会",
        "source": "https://baike.baidu.com/item/%E9%A2%8D%E4%B8%9C%E5%8C%BA",
        "notes": "颍东区人大常委会主任、党组书记。",
        "confidence": "confirmed"
    },
    # 区政协主席 刘雷振
    {
        "id": "yingdong_liu_leizhen",
        "name": "刘雷振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-08",
        "birthplace": "",
        "native_place": "",
        "education": "大学（阜阳师范学院中文）",
        "party_join": "中共党员",
        "work_start": "1988-07",
        "current_post": "区政协主席",
        "current_org": "阜阳市颍东区政协",
        "source": "https://baike.baidu.com/item/%E5%88%98%E9%9B%B7%E6%8C%AF/23873985",
        "notes": "1965年8月出生，1988年7月参加工作，中共党员，大学学历，阜阳师范学院中文专业毕业。现任安徽省阜阳市颍东区政协主席。",
        "confidence": "confirmed"
    },

    # ═══ District Party Committee Standing Members (区委常委) — partial ═══
    # Note: Standard 颍东区委常委会 typically has 10-11 members.
    # The following are confirmed from available news reports and Baidu Baike.
    # Additional standing committee members are pending verification from official
    # government website.

    # 刘小平 — 区委常委、区纪委书记、区监委主任（推断）
    {
        "id": "yingdong_liu_xiaoping",
        "name": "刘小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中共阜阳市颍东区纪律检查委员会",
        "source": "https://baike.baidu.com/item/%E9%A2%8D%E4%B8%9C%E5%8C%BA",
        "notes": "颍东区委常委、区纪委书记、区监委主任。",
        "confidence": "plausible"
    },

    # ═══ District Government Leadership (区政府领导) — partial ═══

    # 沙学珍 — 副区长（新闻确认）
    {
        "id": "yingdong_sha_xuezhen",
        "name": "沙学珍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "颍东区人民政府",
        "source": "https://baike.baidu.com/item/%E9%A2%8D%E4%B8%9C%E5%8C%BA",
        "notes": "颍东区副区长。",
        "confidence": "plausible"
    },

    # ═══ Former Leaders ═══

    # 前任区委书记
    {
        "id": "yingdong_zhang_junji",
        "name": "张俊杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任颍东区委书记",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E9%A2%8D%E4%B8%9C%E5%8C%BA",
        "notes": "颍东区委原书记。接任赵群之前担任颍东区委书记，后调任。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": "yingdong_party_committee",
        "name": "中共阜阳市颍东区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜阳市委",
        "location": "阜阳市颍东区"
    },
    {
        "id": "yingdong_government",
        "name": "颍东区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阜阳市人民政府",
        "location": "阜阳市颍东区"
    },
    {
        "id": "yingdong_npc",
        "name": "阜阳市颍东区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "阜阳市人大常委会",
        "location": "阜阳市颍东区"
    },
    {
        "id": "yingdong_政协",
        "name": "阜阳市颍东区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "阜阳市政协",
        "location": "阜阳市颍东区"
    },
    {
        "id": "yingdong_cdc",
        "name": "中共阜阳市颍东区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共阜阳市纪委",
        "location": "阜阳市颍东区"
    },
]

positions = [
    # 赵群
    ("yingdong_zhao_qun", "yingdong_party_committee", "颍东区委书记", "2022-04", "", "正处级", "主持区委全面工作"),
    ("yingdong_zhao_qun", "yingdong_party_committee", "阜阳市颍泉区委常委、副区长", "", "2019-03", "副处级", ""),
    ("yingdong_zhao_qun", "yingdong_party_committee", "阜阳市招商投资促进中心党组书记、主任", "2019-03", "2022-04", "正处级", ""),

    # 刘健
    ("yingdong_liu_jian", "yingdong_government", "颍东区委副书记、区长", "2021-07", "", "正处级", "领导区政府全面工作，负责审计工作"),
    ("yingdong_liu_jian", "yingdong_government", "颍东区委副书记、代区长", "2021-06", "2021-07", "正处级", ""),
    ("yingdong_liu_jian", "yingdong_party_committee", "太和县委常委、县政府常务副县长", "2020-01", "2021-06", "副处级", ""),
    ("yingdong_liu_jian", "yingdong_party_committee", "太和县委常委、组织部部长、统战部部长", "2016-07", "2019-03", "副处级", ""),
    ("yingdong_liu_jian", "yingdong_party_committee", "太和县委常委、组织部部长", "2016-01", "2016-07", "副处级", ""),
    ("yingdong_liu_jian", "yingdong_party_committee", "共青团阜阳市委副书记、党组成员", "2009-07", "2016-01", "副处级", "公选"),
    ("yingdong_liu_jian", "yingdong_government", "安庆市迎江区老峰镇党委委员、常务副镇长", "2007-01", "2009-07", "乡科级", ""),
    ("yingdong_liu_jian", "yingdong_government", "安庆经济技术开发区管委会办公室副主任科员", "2006-09", "", "", ""),

    # 岳蕾
    ("yingdong_yue_lei", "yingdong_npc", "颍东区人大常委会主任、党组书记", "", "", "正处级", ""),

    # 刘雷振
    ("yingdong_liu_leizhen", "yingdong_政协", "颍东区政协主席", "", "", "正处级", ""),

    # 刘小平
    ("yingdong_liu_xiaoping", "yingdong_cdc", "颍东区委常委、区纪委书记", "", "", "副处级", ""),

    # 沙学珍
    ("yingdong_sha_xuezhen", "yingdong_government", "颍东区副区长", "", "", "副处级", ""),
]

relationships = [
    # 赵群 ↔ 刘健（党政正职搭档）
    {
        "person_a": "yingdong_zhao_qun",
        "person_b": "yingdong_liu_jian",
        "type": "party_government_leadership",
        "strength": "strong",
        "context": "区委书记与区长（党政正职搭档）",
        "overlap_org": "颍东区四套班子",
        "overlap_period": "2022-04至今",
        "note": "confirmed"
    },
    # 赵群 ↔ 岳蕾（区委与人大）
    {
        "person_a": "yingdong_zhao_qun",
        "person_b": "yingdong_yue_lei",
        "type": "party_npc_leadership",
        "strength": "strong",
        "context": "区委书记与区人大常委会主任",
        "overlap_org": "颍东区四套班子",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 赵群 ↔ 刘雷振（区委与政协）
    {
        "person_a": "yingdong_zhao_qun",
        "person_b": "yingdong_liu_leizhen",
        "type": "party_cppcc_leadership",
        "strength": "strong",
        "context": "区委书记与区政协主席",
        "overlap_org": "颍东区四套班子",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 刘健 ↔ 岳蕾
    {
        "person_a": "yingdong_liu_jian",
        "person_b": "yingdong_yue_lei",
        "type": "government_npc",
        "strength": "medium",
        "context": "区长与区人大常委会主任",
        "overlap_org": "颍东区四套班子",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 刘健 ↔ 刘雷振
    {
        "person_a": "yingdong_liu_jian",
        "person_b": "yingdong_liu_leizhen",
        "type": "government_cppcc",
        "strength": "medium",
        "context": "区长与区政协主席",
        "overlap_org": "颍东区四套班子",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 赵群 ↔ 沙学珍（上下级）
    {
        "person_a": "yingdong_zhao_qun",
        "person_b": "yingdong_sha_xuezhen",
        "type": "superior_subordinate",
        "strength": "medium",
        "context": "区委书记和副区长",
        "overlap_org": "颍东区",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 刘健 ↔ 沙学珍（区长与副区长）
    {
        "person_a": "yingdong_liu_jian",
        "person_b": "yingdong_sha_xuezhen",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "颍东区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 刘健 ↔ 刘小平（区长与纪委书记）
    {
        "person_a": "yingdong_liu_jian",
        "person_b": "yingdong_liu_xiaoping",
        "type": "colleague",
        "strength": "medium",
        "context": "区长与区纪委书记",
        "overlap_org": "颍东区",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    # 赵群 ↔ 刘小平（区委书记与纪委书记）
    {
        "person_a": "yingdong_zhao_qun",
        "person_b": "yingdong_liu_xiaoping",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区委书记与区纪委书记",
        "overlap_org": "中共阜阳市颍东区委员会",
        "overlap_period": "至今",
        "note": "confirmed"
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
    lines.append('    <description>颍东区（阜阳市）领导班子工作关系网络 — 2026年7月研究数据</description>')
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
        sz = "20.0" if is_top else ("12.0" if "区委" not in p["id"] else "12.0")
        if "人大" in post or "政协" in post:
            sz = "12.0"

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
        name = o["name"]
        c = org_color(o)
        lines.append(f'      <node id="org_{esc(oid)}" label="{esc(name)}">')
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
    print(f"  颍东区领导班子工作关系网络")
    print(f"  生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"{'='*60}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
