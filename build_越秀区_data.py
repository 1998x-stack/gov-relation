#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yuexiu District (越秀区), Guangzhou, Guangdong."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_越秀区")
DB_PATH = os.path.join(TMP, "越秀区_network.db")
GEXF_PATH = os.path.join(TMP, "越秀区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "王焕清", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-01", "birthplace": "广东丰顺", "education": "省委党校研究生/管理学博士",
     "party_join": "1992-06", "work_start": "1992-07",
     "current_post": "越秀区委书记", "current_org": "中共广州市越秀区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E8%B6%8A%E7%A7%80%E5%8C%BA"},
    {"id": 2, "name": "罗光华", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-05", "birthplace": "", "education": "研究生/管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区委副书记、区长", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/lgh/"},

    # ── Deputy Leaders ──
    {"id": 3, "name": "颜强", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-06", "birthplace": "", "education": "大学/会计硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区委常委、副区长（常务）", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/yq/"},
    {"id": 4, "name": "陈烯", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "", "education": "研究生/法学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区委常委、副区长", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/cx/"},
    {"id": 5, "name": "张正彪", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-01", "birthplace": "", "education": "大学",
     "party_join": "民建", "work_start": "",
     "current_post": "越秀区副区长", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/zzb/"},
    {"id": 6, "name": "李剑怆", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-03", "birthplace": "", "education": "研究生/公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区副区长", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/ljc/"},
    {"id": 7, "name": "赵翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-09", "birthplace": "", "education": "大学/法律硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区副区长、区公安分局局长", "current_org": "广州市公安局越秀区分局",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/zx/"},
    {"id": 8, "name": "王卫国", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-05", "birthplace": "", "education": "大学/文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区副区长", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/wwg/"},
    {"id": 9, "name": "张雅丽", "gender": "女", "ethnicity": "汉族",
     "birth": "1969-10", "birthplace": "", "education": "大学/公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区副区长", "current_org": "广州市越秀区人民政府",
     "source": "https://www.yuexiu.gov.cn/zwgk/ldzc/qzf/zyl/"},

    # ── Predecessors ──
    {"id": 10, "name": "郭环", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "越秀区政协主席", "current_org": "中国人民政治协商会议广州市越秀区委员会",
     "source": "https://www.yuexiu.gov.cn/yxdt/yxkx/content/post_10884602.html"},
]

organizations = [
    {"id": 1, "name": "中共广州市越秀区委员会", "type": "党委", "level": "县处级", "parent": "中共广州市委员会",
     "location": "广东省广州市越秀区"},
    {"id": 2, "name": "广州市越秀区人民政府", "type": "政府", "level": "县处级", "parent": "广州市人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 3, "name": "越秀区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "广州市人大常委会",
     "location": "广东省广州市越秀区"},
    {"id": 4, "name": "中国人民政治协商会议广州市越秀区委员会", "type": "政协", "level": "县处级", "parent": "广州市政协",
     "location": "广东省广州市越秀区"},
    {"id": 5, "name": "广州市公安局越秀区分局", "type": "政府", "level": "乡科级", "parent": "广州市公安局",
     "location": "广东省广州市越秀区"},
    {"id": 6, "name": "广州市越秀区发展和改革局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 7, "name": "广州市越秀区财政局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 8, "name": "广州市越秀区教育局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 9, "name": "广州市越秀区卫生健康局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 10, "name": "广州市越秀区司法局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 11, "name": "广州市越秀区民政局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 12, "name": "广州市越秀区城市管理和综合执法局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 13, "name": "广州市越秀区人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 14, "name": "广州市越秀区政务服务和数据管理局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 15, "name": "广州市越秀区住房建设和水务局", "type": "政府", "level": "乡科级", "parent": "广州市越秀区人民政府",
     "location": "广东省广州市越秀区"},
    {"id": 16, "name": "越秀区珠光街道办事处", "type": "乡镇/街道", "level": "乡科级",
     "parent": "广州市越秀区人民政府", "location": "广东省广州市越秀区"},
    {"id": 17, "name": "广州北京路文化核心区管理委员会", "type": "事业单位", "level": "县处级",
     "parent": "广州市越秀区人民政府", "location": "广东省广州市越秀区"},
]

positions = [
    # ── Wang Huanqing's Career (王焕清) ──
    {"person_id": 1, "org_id": 1, "title": "越秀区委书记", "start": "2019", "end": "present", "rank": "副厅级",
     "note": "2019年起任越秀区委书记。此前曾任共青团广州市委书记、广州市发改委主任等职。据Wikipedia记载。"},
    {"person_id": 1, "org_id": 1, "title": "越秀区委副书记、区长", "start": "2015", "end": "2019", "rank": "正县级",
     "note": ""},
    {"person_id": 1, "org_id": 1, "title": "越秀区委常委、常务副区长", "start": "2011", "end": "2015", "rank": "副县级",
     "note": ""},

    # ── Luo Guanghua's Career (罗光华) ──
    {"person_id": 2, "org_id": 2, "title": "越秀区委副书记、区长", "start": "2022", "end": "present", "rank": "正县级",
     "note": "2022年起任越秀区委副书记、区长，主持区政府全面工作"},
    {"person_id": 2, "org_id": 2, "title": "越秀区委副书记、代区长", "start": "2022", "end": "2022", "rank": "正县级",
     "note": ""},

    # ── Yan Qiang (颜强) ──
    {"person_id": 3, "org_id": 2, "title": "越秀区委常委、副区长（常务）", "start": "", "end": "present", "rank": "副县级",
     "note": "常务副区长，负责区政府常务工作，协助区长分管审计"},
    {"person_id": 3, "org_id": 1, "title": "越秀区委常委", "start": "", "end": "present", "rank": "副县级",
     "note": "区委常委、区政府党组副书记"},

    # ── Chen Xi (陈烯) ──
    {"person_id": 4, "org_id": 2, "title": "越秀区委常委、副区长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责科技工业、信息化、商贸、市场监管、金融等"},
    {"person_id": 4, "org_id": 1, "title": "越秀区委常委、区委办公室主任", "start": "", "end": "", "rank": "副县级",
     "note": ""},

    # ── Zhang Zhengbiao (张正彪) ──
    {"person_id": 5, "org_id": 2, "title": "越秀区副区长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责教育、民族宗教、文化、体育、旅游等（民建）"},

    # ── Li Jianchuang (李剑怆) ──
    {"person_id": 6, "org_id": 2, "title": "越秀区副区长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责卫生健康、城市管理、园林绿化、生态环境等"},

    # ── Zhao Xiang (赵翔) ──
    {"person_id": 7, "org_id": 2, "title": "越秀区副区长、区公安分局局长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责公安、打私、司法、法制等。区委政法委第一副书记"},

    # ── Wang Weiguo (王卫国) ──
    {"person_id": 8, "org_id": 2, "title": "越秀区副区长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责区政府机关、外事、退役军人事务、信访等"},
    {"person_id": 8, "org_id": 16, "title": "珠光街道党工委书记", "start": "", "end": "present", "rank": "乡科级",
     "note": "兼任珠光街道党工委书记"},

    # ── Zhang Yali (张雅丽) ──
    {"person_id": 9, "org_id": 2, "title": "越秀区副区长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责民政、人力资源和社会保障、北京路文化核心区等"},
    {"person_id": 9, "org_id": 13, "title": "区人力资源社会保障局党组书记、局长", "start": "", "end": "", "rank": "乡科级",
     "note": "兼任"},
    {"person_id": 9, "org_id": 17, "title": "北京路文化核心区管理委员会主任", "start": "", "end": "present", "rank": "县处级",
     "note": "兼任核心区管委会主任"},

    # ── Guo Huan (郭环) ──
    {"person_id": 10, "org_id": 4, "title": "越秀区政协主席", "start": "", "end": "present", "rank": "正县级",
     "note": "2026年已在任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "王焕清作为区委书记，罗光华作为区长，是党政一把手搭档关系",
     "overlap_org": "中共广州市越秀区委员会/广州市越秀区人民政府",
     "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "罗光华与颜强在区政府共事，颜强为常务副区长协助区长工作",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "罗光华与陈烯在区政府共事，陈烯为区委常委、副区长",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "罗光华与张正彪在区政府共事",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "罗光华与李剑怆在区政府共事",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "罗光华与赵翔在区政府共事，赵翔任副区长兼公安分局局长",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "罗光华与王卫国在区政府共事",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "strength": "medium",
     "context": "罗光华与张雅丽在区政府共事",
     "overlap_org": "广州市越秀区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "王焕清与陈烯在区委共事，陈烯任区委常委、区委办公室主任",
     "overlap_org": "中共广州市越秀区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "王焕清与颜强在区委共事，颜强为区委常委",
     "overlap_org": "中共广州市越秀区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "颜强与陈烯同任区委常委",
     "overlap_org": "中共广州市越秀区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
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
    elif "政协主席" in role:
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
    lines.append('    <description>越秀区领导班子工作关系网络 - 广东省广州市越秀区</description>')
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
