#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Qilihe District (七里河区), Lanzhou, Gansu."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_七里河区")
DB_PATH = os.path.join(TMP, "七里河区_network.db")
GEXF_PATH = os.path.join(TMP, "七里河区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "胡真", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "甘肃会宁", "education": "西北师范大学",
     "party_join": "2001-06", "work_start": "1998-11",
     "current_post": "兰州市七里河区委书记", "current_org": "中共兰州市七里河区委员会",
     "source": "https://www.qlhq.lanzhou.gov.cn"},
    {"id": 2, "name": "孙洋", "gender": "女", "ethnicity": "汉族",
     "birth": "1977-01", "birthplace": "山东平度", "education": "在职研究生/工商管理硕士",
     "party_join": "1999-03", "work_start": "1999-09",
     "current_post": "兰州市七里河区委副书记、区长", "current_org": "兰州市七里河区人民政府",
     "source": "https://www.qlhq.lanzhou.gov.cn"},

    # ── Previous Leaders ──
    {"id": 3, "name": "芮文刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-12", "birthplace": "甘肃景泰", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兰州市政协副主席（原七里河区委书记）", "current_org": "兰州市政协",
     "source": "https://www.sohu.com/a/xxxx"},

    # ── Standing Committee Members ──
    {"id": 4, "name": "王瑞", "gender": "男", "ethnicity": "满族",
     "birth": "1983-01", "birthplace": "甘肃兰州", "education": "大学",
     "party_join": "2004-12", "work_start": "2006-07",
     "current_post": "七里河区委常委、宣传部部长", "current_org": "中共兰州市七里河区委员会",
     "source": "https://www.qlhq.lanzhou.gov.cn"},
    {"id": 5, "name": "岳红宾", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "甘肃榆中", "education": "",
     "party_join": "2001-03", "work_start": "2003-05",
     "current_post": "七里河区委常委、统战部部长、政法委书记", "current_org": "中共兰州市七里河区委员会",
     "source": "https://www.qlhq.lanzhou.gov.cn"},
    {"id": 6, "name": "张福寿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "七里河区人大常委会主任", "current_org": "七里河区人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/%E4%B8%83%E9%87%8C%E6%B2%B3%E5%8C%BA"},
    {"id": 7, "name": "高希明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "七里河区政协主席", "current_org": "中国人民政治协商会议七里河区委员会",
     "source": "https://baike.baidu.com/item/%E4%B8%83%E9%87%8C%E6%B2%B3%E5%8C%BA"},
    {"id": 8, "name": "宋明安", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "七里河区副区长", "current_org": "兰州市七里河区人民政府",
     "source": "https://www.qlhq.lanzhou.gov.cn"},
    {"id": 9, "name": "张国军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "七里河区副区长", "current_org": "兰州市七里河区人民政府",
     "source": "https://www.qlhq.lanzhou.gov.cn"},
    {"id": 10, "name": "张斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "七里河区副区长、公安分局局长", "current_org": "兰州市公安局七里河分局",
     "source": "https://www.qlhq.lanzhou.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共兰州市七里河区委员会", "type": "党委", "level": "县处级", "parent": "中共兰州市委员会",
     "location": "甘肃省兰州市七里河区"},
    {"id": 2, "name": "兰州市七里河区人民政府", "type": "政府", "level": "县处级", "parent": "兰州市人民政府",
     "location": "甘肃省兰州市七里河区"},
    {"id": 3, "name": "七里河区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "兰州市人大常委会",
     "location": "甘肃省兰州市七里河区"},
    {"id": 4, "name": "中国人民政治协商会议七里河区委员会", "type": "政协", "level": "县处级", "parent": "兰州市政协",
     "location": "甘肃省兰州市七里河区"},
    {"id": 5, "name": "兰州市公安局七里河分局", "type": "政府", "level": "乡科级", "parent": "兰州市公安局",
     "location": "甘肃省兰州市七里河区"},
    {"id": 6, "name": "兰州市水务局", "type": "政府", "level": "县处级", "parent": "兰州市人民政府",
     "location": "甘肃省兰州市"},
    {"id": 7, "name": "兰州市政协", "type": "政协", "level": "地厅级", "parent": "兰州市",
     "location": "甘肃省兰州市"},
    {"id": 8, "name": "兰州市城关区委组织部", "type": "党委", "level": "乡科级", "parent": "中共兰州市城关区委员会",
     "location": "甘肃省兰州市城关区"},
    {"id": 9, "name": "共青团城关区委", "type": "群团", "level": "乡科级", "parent": "共青团兰州市委",
     "location": "甘肃省兰州市城关区"},
    {"id": 10, "name": "兰州市城关区何家庄小学", "type": "事业单位", "level": "",
     "parent": "兰州市城关区教育局", "location": "甘肃省兰州市城关区"},
    {"id": 11, "name": "兰州市城关区酒泉路街道", "type": "乡镇/街道", "level": "乡科级",
     "parent": "兰州市城关区人民政府", "location": "甘肃省兰州市城关区"},
    {"id": 12, "name": "兰州市环境保护局", "type": "政府", "level": "县处级",
     "parent": "兰州市人民政府", "location": "甘肃省兰州市"},
]

positions = [
    # ── Hu Zhen's Career (胡真) ──
    {"person_id": 1, "org_id": 10, "title": "教师", "start": "1998-11", "end": "c.2003", "rank": "", "note": "城关区何家庄小学任教"},
    {"person_id": 1, "org_id": 8, "title": "城关区委组织部干部", "start": "c.2003", "end": "2005", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "共青团城关区委书记", "start": "2005", "end": "c.2008", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "酒泉路街道党工委副书记、办事处主任", "start": "c.2008", "end": "c.2010", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "酒泉路街道党工委书记", "start": "c.2010", "end": "2011-09", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "七里河区委常委、区委办主任", "start": "2011-09", "end": "2014", "rank": "副县级", "note": "首次到七里河区工作"},
    {"person_id": 1, "org_id": 2, "title": "七里河区委常委、副区长", "start": "2014", "end": "2022", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "兰州经济技术开发区党工委委员、管委会主任（兼安宁区委副书记）", "start": "2022", "end": "2023-04", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "兰州市水务局党组书记、局长", "start": "2023-04", "end": "2023-12", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "七里河区委书记", "start": "2024-01", "end": "present", "rank": "副厅级", "note": "2024年1月任七里河区委书记"},

    # ── Sun Yang's Career (孙洋) ──
    {"person_id": 2, "org_id": 2, "title": "副区长", "start": "2011", "end": "2016", "rank": "副县级", "note": "兰州商学院毕业后，先后在安宁区工作"},
    {"person_id": 2, "org_id": 1, "title": "七里河区委常委、政法委书记", "start": "2016", "end": "2021-04", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "七里河区委副书记、代区长", "start": "2021-04", "end": "2021-04", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "七里河区委副书记、区长", "start": "2021-04-29", "end": "present", "rank": "正县级", "note": "2021年4月29日当选区长；2021年12月3日连任"},

    # ── Rui Wengang (芮文刚) ──
    {"person_id": 3, "org_id": 12, "title": "兰州市环境保护局局长", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "七里河区委书记", "start": "", "end": "2024-01", "rank": "副厅级", "note": "前任区委书记"},
    {"person_id": 3, "org_id": 7, "title": "兰州市政协副主席", "start": "2024-01", "end": "present", "rank": "副厅级", "note": "2024年1月当选"},

    # ── Wang Rui (王瑞) ──
    {"person_id": 4, "org_id": 1, "title": "七里河区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "此前曾任七里河区副区长"},
    {"person_id": 4, "org_id": 2, "title": "七里河区副区长", "start": "c.2021", "end": "", "rank": "副县级", "note": ""},

    # ── Yue Hongbin (岳红宾) ──
    {"person_id": 5, "org_id": 1, "title": "七里河区委常委、区委办公室主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "七里河区委常委、统战部部长、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": "兼区政协党组副书记"},

    # ── Other positions ──
    {"person_id": 6, "org_id": 3, "title": "七里河区人大常委会主任", "start": "2021-12", "end": "present", "rank": "正县级", "note": "2021年12月3日当选"},
    {"person_id": 7, "org_id": 4, "title": "七里河区政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "七里河区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "七里河区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "七里河区副区长、公安七里河分局局长", "start": "", "end": "present", "rank": "副县级", "note": "原贾波，现为张斌"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "胡真作为区委书记，孙洋作为区长，是党政一把手搭档关系",
     "overlap_org": "中共兰州市七里河区委员会/兰州市七里河区人民政府",
     "overlap_period": "2024-01至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "胡真接替芮文刚任七里河区委书记",
     "overlap_org": "中共兰州市七里河区委员会",
     "overlap_period": "2024-01", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "胡真与王瑞在七里河区委共事，王瑞任区委常委、宣传部部长",
     "overlap_org": "中共兰州市七里河区委员会",
     "overlap_period": "2024-01至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "胡真与岳红宾在七里河区委共事，岳红宾任区委常委、统战部部长、政法委书记",
     "overlap_org": "中共兰州市七里河区委员会",
     "overlap_period": "2024-01至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "孙洋与岳红宾在七里河区共事，岳红宾任区委常委兼政法委书记，孙洋任区长（区禁毒委主任），岳红宾任区禁毒委副主任",
     "overlap_org": "兰州市七里河区人民政府",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "孙洋与王瑞在七里河区共事",
     "overlap_org": "兰州市七里河区人民政府",
     "overlap_period": "2021-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "胡真与张福寿在七里河区党政班子共事",
     "overlap_org": "中共兰州市七里河区委员会",
     "overlap_period": "2024-01至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "strong",
     "context": "胡真与宋明安在七里河区共事，宋明安排名靠前的副区长",
     "overlap_org": "兰州市七里河区人民政府",
     "overlap_period": "2024-01至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "strong",
     "context": "胡真与张斌在七里河区共事，张斌任副区长兼公安分局局长",
     "overlap_org": "兰州市七里河区人民政府",
     "overlap_period": "2024-至今", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
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
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>七里河区领导班子工作关系网络 - 甘肃省兰州市七里河区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
