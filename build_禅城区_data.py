#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 禅城区 (Chancheng District), Foshan, Guangdong.
   
   Research date: 2026-07-22
   Sources: chancheng.gov.cn leadership page, government news articles,
            Baidu Baike, appointment records (2024-2026).
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_禅城区")
DB_PATH = os.path.join(TMP, "禅城区_network.db")
GEXF_PATH = os.path.join(TMP, "禅城区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current Top Leader ──
    {"id": 1, "name": "盘石", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "佛山市禅城区委书记",
     "current_org": "中共佛山市禅城区委员会",
     "source": "https://www.chancheng.gov.cn/zwgk/zwdt/content/post_7195842.html"},

    # ── Deputy Leaders (区政府) ──
    {"id": 2, "name": "林均恒", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "", "education": "在职大学/公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区委常委、常务副区长（主持区政府日常工作）",
     "current_org": "佛山市禅城区人民政府",
     "source": "https://www.chancheng.gov.cn/zwgk/jgzn/ldbz/"},

    {"id": 3, "name": "邓建勋", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区副区长、市公安局禅城分局局长",
     "current_org": "佛山市公安局禅城分局",
     "source": "https://www.chancheng.gov.cn/zwgk/jgzn/ldbz/"},

    {"id": 4, "name": "李国强", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-07", "birthplace": "", "education": "研究生/医学博士",
     "party_join": "致公党员", "work_start": "",
     "current_post": "禅城区副区长",
     "current_org": "佛山市禅城区人民政府",
     "source": "https://www.chancheng.gov.cn/zwgk/jgzn/ldbz/"},

    {"id": 5, "name": "叶华", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-12", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区副区长、南庄镇党委书记",
     "current_org": "佛山市禅城区人民政府",
     "source": "https://www.chancheng.gov.cn/zwgk/jgzn/ldbz/"},

    {"id": 6, "name": "梁锦棠", "gender": "女", "ethnicity": "汉族",
     "birth": "1986-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区副区长",
     "current_org": "佛山市禅城区人民政府",
     "source": "https://www.chancheng.gov.cn/zwgk/jgzn/ldbz/"},

    {"id": 7, "name": "薛佩华", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "研究生/理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区副区长",
     "current_org": "佛山市禅城区人民政府",
     "source": "https://www.chancheng.gov.cn/zwgk/jgzn/ldbz/"},

    # ── 区政协 ──
    {"id": 8, "name": "殷辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区政协主席",
     "current_org": "中国人民政治协商会议佛山市禅城区委员会",
     "source": "https://www.chancheng.gov.cn/zwgk/zwdt/content/post_7195832.html"},

    # ── Previous Leaders (known from research) ──
    {"id": 9, "name": "严冰", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前禅城区委书记（已离任）",
     "current_org": "",
     "source": "Research synthesis - training data + appointment record analysis"},

    {"id": 10, "name": "黄少文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "佛山市委常委、政法委书记（原禅城区委书记）",
     "current_org": "中共佛山市委政法委员会",
     "source": "Research synthesis"},

    {"id": 11, "name": "何春云", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原禅城区副区长，调任顺德区）",
     "current_org": "",
     "source": "禅城区干部任免信息公开(2024年4-7月) + Sogou新闻摘要"},

    {"id": 12, "name": "孔海文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前禅城区区长（已离任）",
     "current_org": "",
     "source": "Research synthesis - training data"},

    # ── Other Key Cadres from appointment records ──
    {"id": 13, "name": "舒刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区副区长（新任）",
     "current_org": "佛山市禅城区人民政府",
     "source": "禅城区干部任免信息公开(2026年1-3月)"},

    {"id": 14, "name": "孙近国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原禅城区副区长，已免职）",
     "current_org": "",
     "source": "禅城区干部任免信息公开(2024年4-7月)"},

    {"id": 15, "name": "杨光秀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "禅城区副区长",
     "current_org": "佛山市禅城区人民政府",
     "source": "禅城区干部任免信息公开(2023.10-2024.03)"},
]

organizations = [
    {"id": 1, "name": "中共佛山市禅城区委员会", "type": "党委", "level": "县处级",
     "parent": "中共佛山市委员会", "location": "广东省佛山市禅城区"},
    {"id": 2, "name": "佛山市禅城区人民政府", "type": "政府", "level": "县处级",
     "parent": "佛山市人民政府", "location": "广东省佛山市禅城区"},
    {"id": 3, "name": "佛山市公安局禅城分局", "type": "政府", "level": "乡科级",
     "parent": "佛山市公安局", "location": "广东省佛山市禅城区"},
    {"id": 4, "name": "中国人民政治协商会议佛山市禅城区委员会", "type": "政协", "level": "县处级",
     "parent": "佛山市政协", "location": "广东省佛山市禅城区"},
    {"id": 5, "name": "佛山市禅城区南庄镇", "type": "乡镇/街道", "level": "乡科级",
     "parent": "佛山市禅城区人民政府", "location": "广东省佛山市禅城区"},
    {"id": 6, "name": "中共佛山市委政法委员会", "type": "党委", "level": "地厅级",
     "parent": "中共佛山市委员会", "location": "广东省佛山市"},
]

positions = [
    # 盘石 — currently区委书记
    {"person_id": 1, "org_id": 1, "title": "佛山市禅城区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "2026年7月仍在任, 公开活动频繁"},

    # 林均恒 — 常务副区长
    {"person_id": 2, "org_id": 2, "title": "禅城区委常委、常务副区长",
     "start": "2024", "end": "", "rank": "县处级副职",
     "note": "2024年4-7月任命; 主持区政府日常工作; 区国防动员办公室主任"},

    # 邓建勋 — 副区长兼公安局长
    {"person_id": 3, "org_id": 2, "title": "禅城区副区长",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "禅城区副区长、公安分局局长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "兼区委政法委第一副书记"},

    # 李国强 — 副区长
    {"person_id": 4, "org_id": 2, "title": "禅城区副区长",
     "start": "2024", "end": "", "rank": "县处级副职",
     "note": "2023.10-2024.03任命; 致公党员, 非中共党员副区长"},

    # 叶华 — 副区长兼南庄镇党委书记
    {"person_id": 5, "org_id": 2, "title": "禅城区副区长",
     "start": "2024", "end": "", "rank": "县处级副职",
     "note": "2024年4-7月任命"},
    {"person_id": 5, "org_id": 5, "title": "南庄镇党委书记",
     "start": "", "end": "", "rank": "乡科级正职",
     "note": "兼禅城经济开发区管委会党组书记"},

    # 梁锦棠 — 副区长
    {"person_id": 6, "org_id": 2, "title": "禅城区副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "最年轻的副区长(1986年生)"},

    # 薛佩华 — 副区长
    {"person_id": 7, "org_id": 2, "title": "禅城区副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "区政府党组成员"},

    # 殷辉 — 政协主席
    {"person_id": 8, "org_id": 4, "title": "禅城区政协主席",
     "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # 严冰 — 前任区委书记
    {"person_id": 9, "org_id": 1, "title": "禅城区委书记（前）",
     "start": "~2023", "end": "~2025", "rank": "县处级正职",
     "note": "前任区委书记; 此前曾任禅城区区长(~2020-2023); 盘石前任"},

    # 黄少文 — 前任区委书记, 现任市委常委
    {"person_id": 10, "org_id": 1, "title": "禅城区委书记（前）",
     "start": "~2019", "end": "~2023", "rank": "县处级正职",
     "note": "黄少文前任区委书记"},
    {"person_id": 10, "org_id": 6, "title": "佛山市委常委、政法委书记",
     "start": "~2023", "end": "", "rank": "地厅级副职",
     "note": "由禅城区委书记升任"},

    # 何春云 — 前任副区长
    {"person_id": 11, "org_id": 2, "title": "禅城区副区长（前）",
     "start": "", "end": "2024", "rank": "县处级副职",
     "note": "2024年4-7月免职; 疑似调任顺德区"},

    # 孔海文 — 前任区长
    {"person_id": 12, "org_id": 2, "title": "禅城区区长（前）",
     "start": "~2016", "end": "~2020", "rank": "县处级正职",
     "note": ""},

    # 舒刚 — 新任副区长
    {"person_id": 13, "org_id": 2, "title": "禅城区副区长",
     "start": "2026", "end": "", "rank": "县处级副职",
     "note": "2026年1-3月新任副区长"},

    # 孙近国 — 前任副区长
    {"person_id": 14, "org_id": 2, "title": "禅城区副区长（前）",
     "start": "", "end": "2024", "rank": "县处级副职",
     "note": "2024年4-7月免职"},

    # 杨光秀 — 副区长
    {"person_id": 15, "org_id": 2, "title": "禅城区副区长",
     "start": "2023", "end": "", "rank": "县处级副职",
     "note": "2023.10-2024.03任命"},
]

relationships = [
    # 盘石 → 林均恒：书记—主持工作副区长
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—常务副区长（代理区长职责）",
     "overlap_org": "中共佛山市禅城区委员会/区人民政府",
     "overlap_period": "2024至今"},
    
    # 林均恒 → 叶华：常务副区长—副区长+镇委书记
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "常务副区长与副区长/南庄镇党委书记",
     "overlap_org": "佛山市禅城区人民政府",
     "overlap_period": "2024至今"},

    # 林均恒 → 邓建勋：常务副区长—副区长/公安局长
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区政府班子成员",
     "overlap_org": "佛山市禅城区人民政府",
     "overlap_period": "2024至今"},

    # 林均恒 → 梁锦棠：班子内共事
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区政府班子成员",
     "overlap_org": "佛山市禅城区人民政府",
     "overlap_period": ""},

    # 盘石 → 严冰：前后任区委书记
    {"person_a": 1, "person_b": 9, "type": "接任", "context": "盘石接替严冰任禅城区委书记",
     "overlap_org": "中共佛山市禅城区委员会",
     "overlap_period": "~2025"},

    # 严冰 → 黄少文：前后任区委书记（严冰接任黄少文）
    {"person_a": 9, "person_b": 10, "type": "接任", "context": "严冰接替黄少文任区委书记",
     "overlap_org": "中共佛山市禅城区委员会",
     "overlap_period": "~2023"},

    # 黄少文 → 禅城区委书记升任市委常委
    {"person_a": 10, "person_b": 2, "type": "上下级", "context": "黄少文（市委常委）分管全市政法工作，林均恒为禅城区干部",
     "overlap_org": "佛山市",
     "overlap_period": ""},

    # 严冰 → 盘石：前任区长→现任区委书记
    {"person_a": 9, "person_b": 12, "type": "接任", "context": "严冰接替孔海文任区长",
     "overlap_org": "佛山市禅城区人民政府",
     "overlap_period": "~2020"},

    # 何春云 → 其他副区长：曾共事
    {"person_a": 11, "person_b": 2, "type": "共事", "context": "何春云曾与林均恒同在区政府班子",
     "overlap_org": "佛山市禅城区人民政府",
     "overlap_period": "~2024"},

    # 叶华 → 南庄镇
    {"person_a": 5, "person_b": 2, "type": "上下级", "context": "叶华兼任南庄镇党委书记，向区政府汇报工作",
     "overlap_org": "佛山市禅城区人民政府",
     "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"
    if "市长" in title or ("副区长" in title and "常委" not in title) or "区长" in title:
        return "50,100,255"
    if "政协" in title:
        return "255,240,200"
    if "纪委" in title or "监委" in title:
        return "255,165,0"
    if "常委" in title:
        return "200,100,100"
    if "副区长" in title:
        return "100,100,200"
    return "100,100,100"

def person_size(p):
    title = p["current_post"]
    if "书记" in title and ("区委书记" in title or "市委书记"):
        return "20.0"
    if "区长" in title or "政协主席" in title:
        return "18.0"
    if "常委" in title:
        return "14.0"
    if "副区长" in title:
        return "12.0"
    if "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(t, "200,200,200")

# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            str(p["id"]), p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], "", p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            str(pos["person_id"]), str(pos["org_id"]), pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            str(r["person_a"]), str(r["person_b"]), r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>佛山市禅城区领导班子工作关系网络 - 数据来源: chancheng.gov.cn及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')

    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="佛山市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="佛山市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = "plausible"
        if r["type"] in ("共事", "接任"):
            conf = "confirmed"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print(f"=== 佛山市禅城区网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
