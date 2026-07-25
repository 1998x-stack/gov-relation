#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Gaomi City (高密市), Weifang, Shandong.

高密市 is a county-level city under Weifang City, Shandong Province.

IMPORTANT: This file was built under degraded web access conditions.
See report/open_gaps.md and person JSON open_questions for specific gaps.
"""

import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/shandong_高密市")
DB_PATH = os.path.join(TMP, "高密市_network.db")
GEXF_PATH = os.path.join(TMP, "高密市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────
# NOTE: All data is subject to verification. Confidence labels are applied throughout.

persons = [
    # ── Current Top Leaders ──
    # 市委书记
    {
        "id": 1, "name": "董广明", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委书记",
        "current_org": "中共高密市委员会",
        "source": "待查 — 需通过高密市政府官网或潍坊市组织部任前公示确认"
    },
    # 市长
    {
        "id": 2, "name": "王大伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委副书记、市长",
        "current_org": "高密市人民政府",
        "source": "待查 — 需通过高密市政府官网或潍坊市组织部任前公示确认"
    },

    # ── Previous Leaders ──
    {
        "id": 3, "name": "王文琦", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "前任高密市委书记（去向待查）",
        "current_org": "未知",
        "source": "据公开报道，王文琦在2021年前后曾任高密市委书记"
    },
    {
        "id": 4, "name": "刘玉", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "前任高密市委书记（去向待查）",
        "current_org": "未知",
        "source": "据公开报道，刘玉曾接替王文琦任高密市委书记"
    },
    {
        "id": 5, "name": "万丽", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市人大常委会主任",
        "current_org": "高密市人民代表大会常务委员会",
        "source": "待查"
    },
    {
        "id": 6, "name": "张明", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市政协主席",
        "current_org": "中国人民政治协商会议高密市委员会",
        "source": "待查"
    },
    # ── Standing Committee Members ──
    {
        "id": 7, "name": "陈珊", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委副书记",
        "current_org": "中共高密市委员会",
        "source": "待查"
    },
    {
        "id": 8, "name": "王永亮", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委常委、副市长（常务）",
        "current_org": "高密市人民政府",
        "source": "待查"
    },
    {
        "id": 9, "name": "孙业宗", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委常委、组织部部长",
        "current_org": "中共高密市委组织部",
        "source": "待查"
    },
    {
        "id": 10, "name": "孔逢春", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委常委、宣传部部长",
        "current_org": "中共高密市委宣传部",
        "source": "待查"
    },
    {
        "id": 11, "name": "张维兵", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委常委、政法委书记",
        "current_org": "中共高密市委政法委员会",
        "source": "待查"
    },
    {
        "id": 12, "name": "张昭", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委常委、市纪委书记、市监委主任",
        "current_org": "中共高密市纪律检查委员会",
        "source": "待查"
    },
    {
        "id": 13, "name": "李长军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市委常委、市委办公室主任",
        "current_org": "中共高密市委办公室",
        "source": "待查"
    },
    # ── Deputy Mayors ──
    {
        "id": 14, "name": "马明", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市副市长",
        "current_org": "高密市人民政府",
        "source": "待查"
    },
    {
        "id": 15, "name": "韩志超", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市副市长、市公安局局长",
        "current_org": "高密市公安局",
        "source": "待查"
    },
    {
        "id": 16, "name": "李文东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "高密市副市长",
        "current_org": "高密市人民政府",
        "source": "待查"
    },
]

organizations = [
    {"id": 1, "name": "中共高密市委员会", "type": "党委", "level": "县处级",
     "parent": "中共潍坊市委员会", "location": "山东省潍坊市高密市"},
    {"id": 2, "name": "高密市人民政府", "type": "政府", "level": "县处级",
     "parent": "潍坊市人民政府", "location": "山东省潍坊市高密市"},
    {"id": 3, "name": "高密市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "潍坊市人大常委会", "location": "山东省潍坊市高密市"},
    {"id": 4, "name": "中国人民政治协商会议高密市委员会", "type": "政协", "level": "县处级",
     "parent": "潍坊市政协", "location": "山东省潍坊市高密市"},
    {"id": 5, "name": "中共高密市委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共高密市委员会", "location": "山东省潍坊市高密市"},
    {"id": 6, "name": "中共高密市委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共高密市委员会", "location": "山东省潍坊市高密市"},
    {"id": 7, "name": "中共高密市委政法委员会", "type": "党委", "level": "乡科级",
     "parent": "中共高密市委员会", "location": "山东省潍坊市高密市"},
    {"id": 8, "name": "中共高密市纪律检查委员会", "type": "党委", "level": "乡科级",
     "parent": "中共高密市委员会", "location": "山东省潍坊市高密市"},
    {"id": 9, "name": "中共高密市委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共高密市委员会", "location": "山东省潍坊市高密市"},
    {"id": 10, "name": "高密市公安局", "type": "政府", "level": "乡科级",
     "parent": "高密市人民政府", "location": "山东省潍坊市高密市"},
    {"id": 11, "name": "潍坊市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共山东省委员会", "location": "山东省潍坊市"},
    {"id": 12, "name": "潍坊市人民政府", "type": "政府", "level": "地厅级",
     "parent": "山东省人民政府", "location": "山东省潍坊市"},
]

positions = [
    # ── 董广明 (市委书记) ──
    {"person_id": 1, "org_id": 1, "title": "高密市委书记",
     "start": "", "end": "present", "rank": "副厅级",
     "note": "当前在任高密市委书记；前任为刘玉、王文琦"},
    # ── 王大伟 (市长) ──
    {"person_id": 2, "org_id": 2, "title": "高密市委副书记、市长",
     "start": "", "end": "present", "rank": "正县级",
     "note": "当前在任高密市市长"},
    # ── 王文琦 (前任书记) ──
    {"person_id": 3, "org_id": 1, "title": "高密市委书记",
     "start": "", "end": "2022?", "rank": "副厅级",
     "note": "前任市委书记；约2021年前后在任"},
    # ── 刘玉 (前任书记) ──
    {"person_id": 4, "org_id": 1, "title": "高密市委书记",
     "start": "2022?", "end": "2023?", "rank": "副厅级",
     "note": "接替王文琦任市委书记；任期待查"},
    # ── 万丽 (人大主任) ──
    {"person_id": 5, "org_id": 3, "title": "高密市人大常委会主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    # ── 张明 (政协主席) ──
    {"person_id": 6, "org_id": 4, "title": "高密市政协主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    # ── 陈珊 (副书记) ──
    {"person_id": 7, "org_id": 1, "title": "高密市委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 王永亮 (常务副市长) ──
    {"person_id": 8, "org_id": 2, "title": "高密市委常委、副市长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "负责市政府常务工作"},
    # ── 孙业宗 (组织部长) ──
    {"person_id": 9, "org_id": 5, "title": "高密市委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 孔逢春 (宣传部长) ──
    {"person_id": 10, "org_id": 6, "title": "高密市委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 张维兵 (政法委书记) ──
    {"person_id": 11, "org_id": 7, "title": "高密市委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 张昭 (纪委书记) ──
    {"person_id": 12, "org_id": 8, "title": "高密市委常委、市纪委书记、市监委主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 李长军 (市委办公室主任) ──
    {"person_id": 13, "org_id": 9, "title": "高密市委常委、市委办公室主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 马明 (副市长) ──
    {"person_id": 14, "org_id": 2, "title": "高密市副市长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    # ── 韩志超 (副市长/公安局长) ──
    {"person_id": 15, "org_id": 2, "title": "高密市副市长、市公安局局长",
     "start": "", "end": "present", "rank": "副县级",
     "note": "兼市公安局局长"},
    # ── 李文东 (副市长) ──
    {"person_id": 16, "org_id": 2, "title": "高密市副市长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
]

relationships = [
    # ── Core Leadership Pair ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "董广明作为市委书记，王大伟作为市长，是党政一把手搭档关系",
     "overlap_org": "中共高密市委员会/高密市人民政府",
     "overlap_period": "当前任期", "confidence": "unverified"},
    # ── Predecessor Chain ──
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "strength": "medium",
     "context": "董广明接替刘玉任高密市委书记（推测）",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "", "confidence": "unverified"},
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "strength": "medium",
     "context": "刘玉接替王文琦任高密市委书记（推测）",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "", "confidence": "unverified"},
    # ── 书记 ↔ 副书记 ──
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "strength": "strong",
     "context": "董广明作为书记，陈珊作为副书记，在市委班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    # ── 书记 ↔ 常务副市长 ──
    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "董广明与王永亮在市委班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    # ── 市长 ↔ 常务副市长 ──
    {"person_a": 2, "person_b": 8, "type": "overlap", "strength": "strong",
     "context": "王大伟作为市长，王永亮作为常务副市长，在市政府班子共事",
     "overlap_org": "高密市人民政府",
     "overlap_period": "当前任期", "confidence": "unverified"},
    # ── 书记 ↔ 常委成员 ──
    {"person_a": 1, "person_b": 9, "type": "overlap", "strength": "medium",
     "context": "董广明与孙业宗在市委班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "medium",
     "context": "董广明与孔逢春在市委班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "strength": "medium",
     "context": "董广明与张维兵在市委班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "strength": "medium",
     "context": "董广明与张昭在市委班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "strength": "strong",
     "context": "董广明与李长军共事，李长军作为市委办公室主任直接服务书记",  # 高密 means high density here but is used differently
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    # ── 市长 ↔ 副市长 ──
    {"person_a": 2, "person_b": 14, "type": "overlap", "strength": "medium",
     "context": "王大伟与马明在市政府班子共事",
     "overlap_org": "高密市人民政府",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "strength": "medium",
     "context": "王大伟与韩志超在市政府班子共事，韩志超兼任公安局长",
     "overlap_org": "高密市人民政府",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "strength": "medium",
     "context": "王大伟与李文东在市政府班子共事",
     "overlap_org": "高密市人民政府",
     "overlap_period": "当前任期", "confidence": "unverified"},
    # ── 人大、政协 ↔ 书记 ──
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "董广明与万丽在党政班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "董广明与张明在党政班子共事",
     "overlap_org": "中共高密市委员会",
     "overlap_period": "当前任期", "confidence": "unverified"},
]


# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "市委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "市长" in role and "副书记" in role:
        return "50,100,255"
    elif "市长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role or "监委" in role:
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
    return "市委书记" in role and "副书记" not in role

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
    lines.append('    <description>高密市领导班子工作关系网络 - 山东省潍坊市高密市 (县级市)</description>')
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
        lines.append(f'          <attvalue for="3" value="unverified"/>')
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
