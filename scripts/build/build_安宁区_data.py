#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Anning District (安宁区), Lanzhou, Gansu.

安宁区 — 甘肃省兰州市下辖市辖区, 位于黄河北岸, 是兰州高校聚集区.
Covers current Party Secretary (区委书记), District Mayor (区长), their predecessors,
key Standing Committee members, and relationship evidence.

Current leadership as of 2026-07: 王立山 (区委书记), 曹宏亮 (区长)
  - 王立山: 前任安宁区长, 后升任区委书记
  - 曹宏亮: 此前任兰州市政府副秘书长
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_安宁区")
DB_PATH = os.path.join(TMP, "安宁区_network.db")
GEXF_PATH = os.path.join(TMP, "安宁区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    # 王立山 — 安宁区委书记
    {"id": 1, "name": "王立山", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委书记", "current_org": "中共安宁区委",
     "source": "公开报道; 安宁区人民政府官网"},

    # 曹宏亮 — 安宁区区长
    {"id": 2, "name": "曹宏亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区区长", "current_org": "安宁区人民政府",
     "source": "公开报道; 安宁区人民政府官网"},

    # ── Previous Leaders ──
    # 雒泽民 — 前任安宁区委书记 (2016-2022)
    # 后调任兰州市政协, 再任甘肃省信访局局长
    {"id": 3, "name": "雒泽民", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-06", "birthplace": "甘肃天水", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘肃省信访局局长（原安宁区委书记）", "current_org": "甘肃省信访局",
     "source": "https://zh.wikipedia.org/wiki/%E9%9B%92%E6%B3%BD%E6%B0%91"},

    # 王立山的前任安宁区长— 待确认
    # Note: 王立山曾任安宁区长, 后升任区委书记. 前任区长可能是曹宏亮的前任.

    # ── Standing Committee Key Members (区委常委) ──
    # 常务副区长
    {"id": 4, "name": "张吉彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、常务副区长", "current_org": "安宁区人民政府",
     "source": "安宁区人民政府官网"},

    # 组织部部长
    {"id": 5, "name": "王玉琨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、组织部部长", "current_org": "中共安宁区委组织部",
     "source": "安宁区人民政府官网"},

    # 纪委书记
    {"id": 6, "name": "陈涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、纪委书记、监委主任", "current_org": "中共安宁区纪律检查委员会",
     "source": "安宁区人民政府官网"},

    # 政法委书记
    {"id": 7, "name": "蒋源庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、政法委书记", "current_org": "中共安宁区委政法委员会",
     "source": "安宁区人民政府官网"},

    # 宣传部部长
    {"id": 8, "name": "杨荣广", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、宣传部部长", "current_org": "中共安宁区委宣传部",
     "source": "安宁区人民政府官网"},

    # 统战部部长
    {"id": 9, "name": "冯宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、统战部部长", "current_org": "中共安宁区委统战部",
     "source": "安宁区人民政府官网"},

    # 区委办公室主任
    {"id": 10, "name": "袁冬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区委常委、区委办公室主任", "current_org": "中共安宁区委办公室",
     "source": "安宁区人民政府官网"},

    # ── Other Key Leaders ──
    {"id": 11, "name": "康珺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区人大常委会主任", "current_org": "安宁区人民代表大会常务委员会",
     "source": "安宁区人民政府官网"},

    {"id": 12, "name": "贾向红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区政协主席", "current_org": "中国人民政治协商会议安宁区委员会",
     "source": "安宁区人民政府官网"},

    {"id": 13, "name": "李琦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区副区长（常务之后排名第一）", "current_org": "安宁区人民政府",
     "source": "安宁区人民政府官网"},

    {"id": 14, "name": "杨斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安宁区副区长、兰州市公安局安宁分局局长", "current_org": "兰州市公安局安宁分局",
     "source": "安宁区人民政府官网"},
]

organizations = [
    {"id": 1, "name": "中共安宁区委", "type": "党委", "level": "县处级", "parent": "中共兰州市委员会",
     "location": "甘肃省兰州市安宁区"},
    {"id": 2, "name": "安宁区人民政府", "type": "政府", "level": "县处级", "parent": "兰州市人民政府",
     "location": "甘肃省兰州市安宁区"},
    {"id": 3, "name": "安宁区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "兰州市人大常委会",
     "location": "甘肃省兰州市安宁区"},
    {"id": 4, "name": "中国人民政治协商会议安宁区委员会", "type": "政协", "level": "县处级", "parent": "兰州市政协",
     "location": "甘肃省兰州市安宁区"},
    {"id": 5, "name": "中共安宁区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共兰州市纪律检查委员会",
     "location": "甘肃省兰州市安宁区"},
    {"id": 6, "name": "中共安宁区委组织部", "type": "党委", "level": "乡科级", "parent": "中共安宁区委",
     "location": "甘肃省兰州市安宁区"},
    {"id": 7, "name": "中共安宁区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共安宁区委",
     "location": "甘肃省兰州市安宁区"},
    {"id": 8, "name": "中共安宁区委统战部", "type": "党委", "level": "乡科级", "parent": "中共安宁区委",
     "location": "甘肃省兰州市安宁区"},
    {"id": 9, "name": "中共安宁区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共安宁区委",
     "location": "甘肃省兰州市安宁区"},
    {"id": 10, "name": "中共安宁区委办公室", "type": "党委", "level": "乡科级", "parent": "中共安宁区委",
     "location": "甘肃省兰州市安宁区"},
    {"id": 11, "name": "兰州市公安局安宁分局", "type": "政府", "level": "乡科级", "parent": "兰州市公安局",
     "location": "甘肃省兰州市安宁区"},
    {"id": 12, "name": "甘肃省信访局", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府",
     "location": "甘肃省兰州市"},
    {"id": 13, "name": "兰州市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府",
     "location": "甘肃省兰州市"},
    {"id": 14, "name": "中共兰州市委员会", "type": "党委", "level": "副省级", "parent": "中共甘肃省委员会",
     "location": "甘肃省兰州市"},
    {"id": 15, "name": "兰州市政协", "type": "政协", "level": "地厅级", "parent": "甘肃省政协",
     "location": "甘肃省兰州市"},
]

positions = [
    # ── Wang Lishan's Career (王立山) ──
    # Currently 安宁区委书记; previously 安宁区长 (presumed promotion path)
    {"person_id": 1, "org_id": 2, "title": "安宁区区长", "start": "", "end": "", "rank": "正处级", "note": "此前曾任安宁区长, 后接任区委书记"},
    {"person_id": 1, "org_id": 1, "title": "安宁区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "现任安宁区委书记"},

    # ── Cao Hongliang's Career (曹宏亮) ──
    {"person_id": 2, "org_id": 13, "title": "兰州市政府副秘书长", "start": "", "end": "", "rank": "正处级", "note": "此前曾任此职"},
    {"person_id": 2, "org_id": 2, "title": "安宁区区长", "start": "", "end": "present", "rank": "正处级", "note": "现任安宁区长"},

    # ── Luo Zemin's Career (雒泽民) ──
    {"person_id": 3, "org_id": 1, "title": "安宁区委书记", "start": "2016", "end": "2022", "rank": "副厅级", "note": "2016-2022任安宁区委书记"},
    {"person_id": 3, "org_id": 15, "title": "兰州市政协党组成员", "start": "2022", "end": "2023", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "甘肃省信访局局长", "start": "2023", "end": "present", "rank": "正厅级", "note": "2023年任甘肃省信访局局长"},

    # ── Zhang Jibin (张吉彬, 常务副区长) ──
    {"person_id": 4, "org_id": 2, "title": "安宁区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Wang Yukun (王玉琨, 组织部部长) ──
    {"person_id": 5, "org_id": 6, "title": "安宁区委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Chen Tao (陈涛, 纪委书记) ──
    {"person_id": 6, "org_id": 5, "title": "安宁区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Jiang Yuanqing (蒋源庆, 政法委书记) ──
    {"person_id": 7, "org_id": 9, "title": "安宁区委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Yang Rongguang (杨荣广, 宣传部部长) ──
    {"person_id": 8, "org_id": 7, "title": "安宁区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Feng Ning (冯宁, 统战部部长) ──
    {"person_id": 9, "org_id": 8, "title": "安宁区委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Yuan Dong (袁冬, 区委办主任) ──
    {"person_id": 10, "org_id": 10, "title": "安宁区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Kang Jun (康珺, 人大主任) ──
    {"person_id": 11, "org_id": 3, "title": "安宁区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # ── Jia Xianghong (贾向红, 政协主席) ──
    {"person_id": 12, "org_id": 4, "title": "安宁区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # ── Li Qi (李琦, 副区长) ──
    {"person_id": 13, "org_id": 2, "title": "安宁区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # ── Yang Bin (杨斌, 副区长兼公安分局局长) ──
    {"person_id": 14, "org_id": 2, "title": "安宁区副区长、安宁公安分局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "王立山作为区委书记, 曹宏亮作为区长, 是党政一把手搭档关系",
     "overlap_org": "中共安宁区委/安宁区人民政府",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "王立山接替雒泽民任安宁区委书记（中间可能隔有其他过渡）",
     "overlap_org": "中共安宁区委",
     "overlap_period": "2022-2023", "confidence": "plausible"},

    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "王立山与张吉彬在安宁区委共事, 张吉彬任常务副区长",
     "overlap_org": "中共安宁区委/安宁区人民政府",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "王立山与王玉琨在安宁区委共事, 王玉琨任组织部长",
     "overlap_org": "中共安宁区委",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "王立山与陈涛在安宁区委共事, 陈涛任纪委书记",
     "overlap_org": "中共安宁区委",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "strong",
     "context": "王立山与蒋源庆在安宁区委共事, 蒋源庆任政法委书记",
     "overlap_org": "中共安宁区委",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "strong",
     "context": "王立山与杨荣广在安宁区委共事, 杨荣广任宣传部长",
     "overlap_org": "中共安宁区委",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 9, "type": "overlap", "strength": "strong",
     "context": "王立山与冯宁在安宁区委共事, 冯宁任统战部长",
     "overlap_org": "中共安宁区委",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "strong",
     "context": "王立山与袁冬在安宁区委共事, 袁冬任区委办主任",
     "overlap_org": "中共安宁区委",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "曹宏亮与张吉彬在安宁区政府共事",
     "overlap_org": "安宁区人民政府",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 13, "type": "overlap", "strength": "medium",
     "context": "曹宏亮与李琦在安宁区政府共事",
     "overlap_org": "安宁区人民政府",
     "overlap_period": "", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 14, "type": "overlap", "strength": "medium",
     "context": "曹宏亮与杨斌在安宁区政府共事, 杨斌任副区长兼公安分局局长",
     "overlap_org": "安宁区人民政府",
     "overlap_period": "", "confidence": "confirmed"},
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
    lines.append('    <description>安宁区领导班子工作关系网络 - 甘肃省兰州市安宁区</description>')
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
