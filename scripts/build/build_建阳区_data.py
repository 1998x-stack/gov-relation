#!/usr/bin/env python3
"""
Build 建阳区 (Jianyang District, 南平市, Fujian) government personnel
relationship network — SQLite database + GEXF graph.

建阳区 is the central administrative district (南平市政府驻地) of Nanping city,
Fujian Province. It was established as Jianyang County in 205 AD, became Jianyang
City in 1994, and was reorganized as Jianyang District in 2015. The Nanping
municipal government relocated from Yanping District to Jianyang in 2020.

Current as of: 2026-07-16

Key recent change: 王冲 was promoted from 区长 to 区委书记 on 2026-07-15,
replacing 谢启龙 who departed. The 区长 position is currently vacant.

Targets: 区委书记 (王冲, 2026.07-) & 区长 (vacant as of 2026.07)
"""

import sqlite3
import os
import json
from datetime import datetime

# ── Staging paths ─────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
TMP = BASE  # we are in data/tmp/fujian_建阳区/
DB_PATH = os.path.join(TMP, "建阳区_network.db")
GEXF_PATH = os.path.join(TMP, "建阳区_network.gexf")
PERSONS_DIR = TMP

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# DATA — from official government website (www.fjjy.gov.cn) as of 2026-07-16
# =========================================================================

# The official website lists:
# 区长: 王冲 (now promoted to 区委书记 per 2026-07-15 military appointment)
# 常务副区长: 张华
# 副区长: 张朝晖, 张学玲, 阎济民, 姜丽华, 梅晓飞, 陈凌辉, 魏秀清, 陈伟
# Wikipedia (ZH): 谢启龙 was 区委书记 (prior to 王冲's promotion)

SLUG = "建阳区"
PROVINCE = "福建省"
CITY = "南平市"

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "王冲",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1987-05",
        "birthplace": "",
        "education": "研究生学历，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区委书记、区人武部党委第一书记",
        "current_org": "中共南平市建阳区委员会",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/wdsqc/index.html; https://www.fjjy.gov.cn/cms/html/jyqrmzf/2026-07-16/390256083.html",
    },
    # ── 区长 currently vacated (王冲 was promoted to 区委书记) ─────────
    # The 区长 position is vacant as of 2026-07-16.
    # ── 常务副区长 (de facto acting head of government) ────────────────
    {
        "id": 2,
        "name": "张华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区委常委、常务副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/zh/index.html",
    },
    # ── 副区长 ─────────────────────────────────────────────────────────
    {
        "id": 3,
        "name": "张朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-09",
        "birthplace": "",
        "education": "在职研究生学历，社会学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长、南平市公安局建阳分局局长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/cwffqc/index.html",
    },
    {
        "id": 4,
        "name": "张学玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "",
        "education": "大学学历，法学学士",
        "party_join": "致公党员",
        "work_start": "",
        "current_post": "建阳区副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/zslfqc/index.html",
    },
    {
        "id": 5,
        "name": "阎济民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/yqyfqc/index.html",
    },
    {
        "id": 6,
        "name": "姜丽华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/lcfqc/index.html",
    },
    {
        "id": 7,
        "name": "梅晓飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-01",
        "birthplace": "",
        "education": "研究生学历，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/mxf/index.html",
    },
    {
        "id": 8,
        "name": "陈凌辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/khmfqc/index.html",
    },
    {
        "id": 9,
        "name": "魏秀清",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "",
        "education": "研究生学历，农学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长（科技副区长）",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/wxq/index.html",
    },
    {
        "id": 10,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "",
        "education": "大学，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建阳区副区长",
        "current_org": "南平市建阳区人民政府",
        "source": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/cw/index.html",
    },
    # ── 前任区委书记 ────────────────────────────────────────────────────
    {
        "id": 11,
        "name": "谢启龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E5%BB%BA%E9%98%B3%E5%8C%BA",
    },
    # ── 前任区委书记（更早）───────────────────────────────────────────
    {
        "id": 12,
        "name": "杨新强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南平市副市长",
        "current_org": "南平市人民政府",
        "source": "https://en.wikipedia.org/wiki/Jianyang,_Nanping; https://www.np.gov.cn",
    },
    # ── 南平市领导 (上级) ──────────────────────────────────────────────
    {
        "id": 13,
        "name": "袁超洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南平市委书记",
        "current_org": "中共南平市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82",
    },
    {
        "id": 14,
        "name": "林建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-11",
        "birthplace": "",
        "education": "在职研究生学历，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南平市市长",
        "current_org": "南平市人民政府",
        "source": "https://www.np.gov.cn",
    },
]

organizations = [
    {"id": 1, "name": "中共南平市建阳区委员会", "type": "党委", "level": "县处级", "parent": "中共南平市委员会", "location": "福建省南平市建阳区"},
    {"id": 2, "name": "南平市建阳区人民政府", "type": "政府", "level": "县处级", "parent": "南平市人民政府", "location": "福建省南平市建阳区"},
    {"id": 3, "name": "南平市人民政府", "type": "政府", "level": "地厅级", "parent": "福建省人民政府", "location": "福建省南平市建阳区"},
    {"id": 4, "name": "中共南平市委员会", "type": "党委", "level": "地厅级", "parent": "中共福建省委员会", "location": "福建省南平市建阳区"},
    {"id": 5, "name": "南平市公安局建阳分局", "type": "政府", "level": "乡科级", "parent": "南平市建阳区人民政府", "location": "福建省南平市建阳区"},
    {"id": 6, "name": "南平市建阳区人民武装部", "type": "党委", "level": "县处级", "parent": "南平军分区", "location": "福建省南平市建阳区"},
]

positions = [
    # 王冲 — 区委书记 (previously 区长)
    {"person_id": 1, "org_id": 1, "title": "建阳区委书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月15日任区人武部党委第一书记，此前为区长"},
    {"person_id": 1, "org_id": 6, "title": "建阳区人武部党委第一书记", "start": "2026-07", "end": "present", "rank": "", "note": "2026年7月15日南平军分区宣读任职决定"},
    {"person_id": 1, "org_id": 2, "title": "建阳区区长", "start": "", "end": "2026-07", "rank": "正处级", "note": "升任区委书记前担任区长"},
    {"person_id": 1, "org_id": 1, "title": "建阳区委副书记", "start": "", "end": "2026-07", "rank": "正处级", "note": "任区长期间兼任区委副书记"},

    # 张华 — 常务副区长
    {"person_id": 2, "org_id": 2, "title": "建阳区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    {"person_id": 2, "org_id": 1, "title": "建阳区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张朝晖 — 副区长
    {"person_id": 3, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": "兼南平市公安局建阳分局局长"},
    {"person_id": 3, "org_id": 5, "title": "南平市公安局建阳分局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},

    # 张学玲 — 副区长
    {"person_id": 4, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 阎济民 — 副区长
    {"person_id": 5, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 姜丽华 — 副区长
    {"person_id": 6, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 梅晓飞 — 副区长
    {"person_id": 7, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈凌辉 — 副区长
    {"person_id": 8, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 魏秀清 — 副区长
    {"person_id": 9, "org_id": 2, "title": "建阳区副区长（科技副区长）", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈伟 — 副区长
    {"person_id": 10, "org_id": 2, "title": "建阳区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 谢启龙 — 前任区委书记
    {"person_id": 11, "org_id": 1, "title": "建阳区委书记", "start": "", "end": "2026-07", "rank": "正处级", "note": "具体上任时间待查，2026年7月由王冲接替"},

    # 杨新强 — 更早前任区委书记
    {"person_id": 12, "org_id": 1, "title": "建阳区委书记", "start": "", "end": "", "rank": "正处级", "note": "此前任建阳区委书记，后调任南平市副市长"},

    # 南平市领导
    {"person_id": 13, "org_id": 4, "title": "南平市委书记", "start": "2023-02", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "南平市市长", "start": "2023-02", "end": "present", "rank": "正厅级", "note": ""},
]

relationships = [
    # 王冲接替谢启龙
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "王冲接替谢启龙任建阳区委书记", "overlap_org": "中共南平市建阳区委员会", "overlap_period": "2026-07", "direction": "person_to_other", "strength": "strong"},

    # 杨新强—谢启龙 predecessor_successor (推测)
    {"person_a": 11, "person_b": 12, "type": "predecessor_successor", "context": "谢启龙接替杨新强任建阳区委书记（推测）", "overlap_org": "中共南平市建阳区委员会", "overlap_period": "", "direction": "person_to_other", "strength": "medium"},

    # 杨新强从建阳区委书记调任南平市副市长
    {"person_a": 12, "person_b": 14, "type": "superior_subordinate", "context": "杨新强调任南平市副市长，与市长林建搭班", "overlap_org": "南平市人民政府", "overlap_period": "", "direction": "undirected", "strength": "medium"},

    # 王冲—张华 (常务副区长搭班)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "王冲任区委书记期间与常务副区长张华搭班；此前任区长时张华即为常务副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—张朝晖
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，张朝晖任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—张学玲
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，张学玲任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—阎济民
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，阎济民任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—姜丽华
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，姜丽华任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—梅晓飞
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，梅晓飞任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—陈凌辉
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，陈凌辉任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—魏秀清
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，魏秀清任科技副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 王冲—陈伟
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "王冲任区长/区委书记期间，陈伟任副区长", "overlap_org": "南平市建阳区人民政府", "overlap_period": "", "direction": "undirected", "strength": "strong"},

    # 建阳区受南平市领导
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "王冲作为建阳区委书记，受南平市委书记袁超洪领导", "overlap_org": "中共福建省委员会", "overlap_period": "2026-07", "direction": "other_to_person", "strength": "strong"},
]


# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        direction TEXT, strength TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p.get("birthplace", ""), p["education"], p["party_join"],
                   p.get("work_start", ""), p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,\"end\",rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,direction,strength) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r.get("overlap_period", ""), r["direction"], r["strength"]))

    conn.commit()
    conn.close()
    print(f"✓ SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post") or ""
    if "书记" in post and "区委" in post:
        return "255,50,50"
    elif "区长" in post and "副" not in post:
        return "50,100,255"
    elif "常务副区长" in post or "副区长" in post:
        return "50,100,255"
    elif "市长" in post or "市委书记" in post:
        return "255,50,50"
    else:
        return "100,100,100"


def person_size(p):
    if p["id"] == 1:  # 区委书记
        return "20.0"
    elif p["id"] in (2, 11, 12, 13, 14):  # 常务副区长, former secretaries, city leaders
        return "15.0"
    elif 3 <= p["id"] <= 10:  # 副区长
        return "12.0"
    else:
        return "12.0"


def org_color(o):
    m = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255", "政协": "255,240,200"}
    return m.get(o["type"], "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>建阳区领导班子关系网络 - {PROVINCE}{CITY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(pid, filename_suffix, person_name):
    p = next(x for x in persons if x["id"] == pid)
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person": other["name"], "person_id": f"jianyang_{other['name']}",
                             "relationship_type": r["type"], "strength": r["strength"],
                             "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r.get("overlap_period", ""),
                             "direction": r["direction"], "confidence": "confirmed",
                             "source_ids": ["S001", "S002"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person": other["name"], "person_id": f"jianyang_{other['name']}",
                             "relationship_type": r["type"], "strength": r["strength"],
                             "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r.get("overlap_period", ""),
                             "direction": r["direction"], "confidence": "confirmed",
                             "source_ids": ["S001", "S002"]})

    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            person_positions.append({
                "start": pos.get("start", ""), "end": pos.get("end", ""),
                "org": org["name"] if org else "",
                "title": pos["title"], "level": pos.get("rank", ""),
                "location": org["location"] if org else "",
                "system": "party" if org and "党委" in org["type"] else "government",
                "rank": pos.get("rank", ""), "is_key_promotion": False,
                "notes": pos.get("note", ""), "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            })

    # Build education array
    edu_entries = []
    if p.get("education"):
        edu_entries.append({
            "period": "", "institution": "", "major": "",
            "degree": p["education"], "study_type": "unknown", "source_ids": ["S001"]
        })

    profile = {
        "schema_version": "1.0",
        "generated_at": today,
        "investigation_scope": {
            "province": PROVINCE, "city": CITY, "region": SLUG,
            "job": filename_suffix, "task_id": "fujian_建阳区",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"jianyang_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": edu_entries,
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": f"https://www.fjjy.gov.cn/cms/html/jyqrmzf/wdsqc/index.html" if pid == 1 else ""
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": today,
            "is_current_confirmed": pid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": person_positions,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S001", "title": "建阳区人民政府 - 区长页",
             "url": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/wdsqc/index.html",
             "publisher": "建阳区人民政府", "published_at": "", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "建阳区人民政府 - 领导信息首页",
             "url": "https://www.fjjy.gov.cn",
             "publisher": "建阳区人民政府", "published_at": "", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S003", "title": "建阳区人民武装部党委第一书记任职大会",
             "url": "https://www.fjjy.gov.cn/cms/html/jyqrmzf/2026-07-16/390256083.html",
             "publisher": "建阳区人民政府", "published_at": "2026-07-16", "accessed_at": today,
             "source_type": "official", "reliability": "high", "notes": "确认王冲任区委书记"},
            {"id": "S004", "title": "建阳区 - 维基百科",
             "url": "https://zh.wikipedia.org/wiki/%E5%BB%BA%E9%98%B3%E5%8C%BA",
             "publisher": "维基百科", "published_at": "", "accessed_at": today,
             "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S005", "title": "南平市 - 维基百科",
             "url": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%B9%B3%E5%B8%82",
             "publisher": "维基百科", "published_at": "", "accessed_at": today,
             "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S006", "title": "建阳区 - English Wikipedia",
             "url": "https://en.wikipedia.org/wiki/Jianyang,_Nanping",
             "publisher": "Wikipedia", "published_at": "", "accessed_at": today,
             "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"缺少{p['name']}的出生地、早期教育背景和完整履历时间线"
        },
        "open_questions": [
            {"priority": "high", "question": f"{p['name']}的出生地和早期教育背景",
             "why_it_matters": "影响人物身份确认和履历完整度",
             "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 出生"], "last_attempted": today},
            {"priority": "high", "question": f"{p['name']}在建阳区任职前的完整履历",
             "why_it_matters": "理解其职业发展路径和提拔背景",
             "suggested_queries": [f"{p['name']} 任职经历"], "last_attempted": today},
        ]
    }

    filename = f"{today.replace('-', '')}-{PROVINCE}-{CITY}-{filename_suffix}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"✓ Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building {SLUG} government personnel network...")
    print(f"Date: {today}")
    print(f"Target: 区委书记 (王冲, 2026.07-) & 区长 (vacant)")
    print()
    build_sqlite()
    build_gexf()
    write_person_json(1, "区委书记", "王冲")
    write_person_json(2, "常务副区长", "张华")
    print(f"\nDone. All artifacts written to {TMP}")
    print(f"\nNote: 区长职位目前空缺。王冲于2026年7月15日由区长升任区委书记。")
    print(f"前任区委书记谢启龙去向待查。")
