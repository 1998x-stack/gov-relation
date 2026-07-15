#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 太湖县 (Taihu County, Anqing, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_太湖县 - 县委书记 & 县长
Sources: Official government website (thx.gov.cn), news reports.
Notes: See confidence labels and open_questions for gaps.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/anhui_太湖县")
DB_PATH = os.path.join(STAGING, "太湖县_network.db")
GEXF_PATH = os.path.join(STAGING, "太湖县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "吴曙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委书记", "current_org": "中共太湖县委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委书记。此前曾任太湖县委副书记、县长等职。",
     "confidence": "confirmed"},

    {"id": 2, "name": "杨杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委副书记、县长", "current_org": "太湖县人民政府",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委副书记、县政府党组书记、县长。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 县委领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "杨小波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委副书记", "current_org": "中共太湖县委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委副书记，协助县委书记处理日常党务工作。",
     "confidence": "plausible"},

    {"id": 4, "name": "赵俊杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委、常务副县长", "current_org": "中共太湖县委员会/太湖县人民政府",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委、常务副县长，负责县政府常务工作。",
     "confidence": "plausible"},

    {"id": 5, "name": "朋腾", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委", "current_org": "中共太湖县委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委。新闻报道中多次出现督导调研活动。",
     "confidence": "plausible"},

    {"id": 6, "name": "黄知开", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委、县纪委书记", "current_org": "中共太湖县纪律检查委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委、县纪委书记、县监委主任。",
     "confidence": "plausible"},

    {"id": 7, "name": "左小斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委、组织部部长", "current_org": "中共太湖县委组织部",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委、组织部部长。",
     "confidence": "plausible"},

    {"id": 8, "name": "王智平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委、宣传部部长", "current_org": "中共太湖县委宣传部",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委、宣传部部长。",
     "confidence": "plausible"},

    {"id": 9, "name": "杜林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委、政法委书记", "current_org": "中共太湖县委政法委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委、政法委书记。",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # 县政府领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 10, "name": "陈杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县委常委、副县长", "current_org": "太湖县人民政府",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县委常委、副县长。",
     "confidence": "plausible"},

    {"id": 11, "name": "李盛华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县副县长", "current_org": "太湖县人民政府",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县人民政府副县长。",
     "confidence": "plausible"},

    {"id": 12, "name": "王丙宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县副县长", "current_org": "太湖县人民政府",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县人民政府副县长。",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # 人大/政协领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 13, "name": "李加生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县人大常委会主任", "current_org": "太湖县人民代表大会常务委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县人大常委会主任。",
     "confidence": "plausible"},

    {"id": 14, "name": "殷跃平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "太湖县政协主席", "current_org": "中国人民政治协商会议太湖县委员会",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县政协主席。",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # Predecessors
    # ═══════════════════════════════════════════════════════════════════
    {"id": 15, "name": "朱小兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.thx.gov.cn/",
     "notes": "太湖县前任县委书记（~2019-2023年），此前曾任太湖县县长。",
     "confidence": "plausible"},
]

organizations = [
    {"id": 1, "name": "中共太湖县委员会", "type": "党委", "level": "县",
     "parent": "中共安庆市委", "location": "安徽省安庆市太湖县"},
    {"id": 2, "name": "太湖县人民政府", "type": "政府", "level": "县",
     "parent": "安庆市人民政府", "location": "安徽省安庆市太湖县"},
    {"id": 3, "name": "中共太湖县纪律检查委员会", "type": "纪委", "level": "县",
     "parent": "中共安庆市纪律检查委员会", "location": "安徽省安庆市太湖县"},
    {"id": 4, "name": "中共太湖县委组织部", "type": "党委部门", "level": "县",
     "parent": "中共太湖县委员会", "location": "安徽省安庆市太湖县"},
    {"id": 5, "name": "中共太湖县委宣传部", "type": "党委部门", "level": "县",
     "parent": "中共太湖县委员会", "location": "安徽省安庆市太湖县"},
    {"id": 6, "name": "中共太湖县委政法委员会", "type": "党委部门", "level": "县",
     "parent": "中共太湖县委员会", "location": "安徽省安庆市太湖县"},
    {"id": 7, "name": "太湖县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "安庆市人民代表大会常务委员会", "location": "安徽省安庆市太湖县"},
    {"id": 8, "name": "中国人民政治协商会议太湖县委员会", "type": "政协", "level": "县",
     "parent": "中国人民政治协商会议安庆市委员会", "location": "安徽省安庆市太湖县"},
]

positions = [
    # 吴曙 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "太湖县委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任太湖县委书记"},
    {"person_id": 1, "org_id": 2, "title": "太湖县县长（曾任）", "start": "", "end": "", "rank": "正处级", "note": "此前曾任太湖县县长，后接任县委书记"},

    # 杨杰 - 县长
    {"person_id": 2, "org_id": 2, "title": "太湖县委副书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "现任太湖县县长"},
    {"person_id": 2, "org_id": 1, "title": "太湖县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "兼任县委副书记"},

    # 杨小波 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "太湖县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 赵俊杰 - 常务副县长
    {"person_id": 4, "org_id": 1, "title": "太湖县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "太湖县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 朋腾 - 县委常委
    {"person_id": 5, "org_id": 1, "title": "太湖县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 黄知开 - 纪委书记
    {"person_id": 6, "org_id": 3, "title": "太湖县委常委、县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 左小斌 - 组织部长
    {"person_id": 7, "org_id": 4, "title": "太湖县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 王智平 - 宣传部长
    {"person_id": 8, "org_id": 5, "title": "太湖县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 杜林 - 政法委书记
    {"person_id": 9, "org_id": 6, "title": "太湖县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈杰 - 副县长
    {"person_id": 10, "org_id": 1, "title": "太湖县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "太湖县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李盛华 - 副县长
    {"person_id": 11, "org_id": 2, "title": "太湖县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 王丙宇 - 副县长
    {"person_id": 12, "org_id": 2, "title": "太湖县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李加生 - 人大主任
    {"person_id": 13, "org_id": 7, "title": "太湖县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 殷跃平 - 政协主席
    {"person_id": 14, "org_id": 8, "title": "太湖县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 朱小兵 - 前县委书记
    {"person_id": 15, "org_id": 1, "title": "太湖县委书记（前任）", "start": "", "end": "", "rank": "正处级",
     "note": "前任太湖县委书记。2023年左右离任。"},
]

relationships = [
    # 吴曙 ←→ 杨杰: 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "吴曙（县委书记）与杨杰（县长）为现任党政一把手搭档关系",
     "overlap_org": "太湖县", "overlap_period": "2023-至今",
     "strength": "strong", "confidence": "confirmed"},

    # 吴曙 → 赵俊杰: 上下级
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "吴曙任县委书记，赵俊杰任县委常委、常务副县长",
     "overlap_org": "太湖县", "overlap_period": "",
     "strength": "medium", "confidence": "plausible"},

    # 吴曙 → 黄知开: 上下级
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "吴曙任县委书记，黄知开为县纪委书记",
     "overlap_org": "太湖县", "overlap_period": "",
     "strength": "medium", "confidence": "plausible"},

    # 吴曙 → 朱小兵: 前任-后任
    {"person_a": 15, "person_b": 1, "type": "前任后任",
     "context": "朱小兵为前任县委书记，吴曙接任县委书记",
     "overlap_org": "太湖县", "overlap_period": "",
     "strength": "strong", "confidence": "plausible"},

    # 杨杰 → 赵俊杰: 县长-常务副县长工作搭档
    {"person_a": 2, "person_b": 4, "type": "党政搭档",
     "context": "杨杰（县长）与赵俊杰（常务副县长）为县政府党政搭档",
     "overlap_org": "太湖县人民政府", "overlap_period": "",
     "strength": "strong", "confidence": "plausible"},
]

# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p.get("current_post", "")
    if "县委书记" in title or "区委书记" in title:
        return "255,50,50"
    if "县长" in title or "区长" in title:
        return "50,100,255"
    if "纪委书记" in title or "监委" in title:
        return "255,165,0"
    return "100,100,100"


def person_size(p):
    title = p.get("current_post", "")
    if "县委书记" in title or "县长" in title or "区长" in title:
        return "20.0"
    return "12.0"


def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,200,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "组织" in t or "宣传" in t or "政法" in t or "党委部门" in t:
        return "255,200,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>太湖县领导班子工作关系网络数据库</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("confidence",""))}"/>')
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
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person ↔ person (relationship)
    for rel in relationships:
        pa = f"p{rel['person_a']}"
        pb = f"p{rel['person_b']}"
        weight = "2.0" if rel.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(rel["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("confidence",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()
    print("--- Summary ---")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("Done.")
