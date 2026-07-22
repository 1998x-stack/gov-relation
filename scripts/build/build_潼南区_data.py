#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 潼南区 (Tongnan District, Chongqing) leadership network."""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/潼南区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/潼南区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "元方", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-09", "birthplace": "陕西白水", "education": "研究生/管理学博士",
     "party_join": "2000-11", "work_start": "1995-07",
     "current_post": "重庆市潼南区委书记", "current_org": "中共重庆市潼南区委员会",
     "source": "https://baike.baidu.com/item/%E5%85%83%E6%96%B9/7585479"},

    # ── Vacant: 区长李成群被查 ──
    {"id": 2, "name": "李成群", "gender": "男", "ethnicity": "土家族",
     "birth": "1966-02", "birthplace": "重庆石柱", "education": "重庆市委党校大学",
     "party_join": "1989-06", "work_start": "1984-07",
     "current_post": "原潼南区委副书记、区长（被查）", "current_org": "无",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%88%90%E7%BE%A4"},

    # ── District Congress Chairman ──
    {"id": 3, "name": "张彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-03", "birthplace": "重庆潼南", "education": "重庆市委党校研究生",
     "party_join": "1987-08", "work_start": "1985-07",
     "current_post": "潼南区人大常委会主任", "current_org": "重庆市潼南区人大常委会",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%BD%AC/3399749"},

    # ── CPPCC Chairman ──
    {"id": 4, "name": "欧汉东", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-08", "birthplace": "重庆", "education": "党校研究生/工学学士",
     "party_join": "1995-05", "work_start": "1993-07",
     "current_post": "潼南区政协党组书记、主席", "current_org": "中国人民政治协商会议重庆市潼南区委员会",
     "source": "https://baike.baidu.com/item/%E6%AC%A7%E6%B1%89%E4%B8%9C/8926468"},

    # ── Discipline Inspection Secretary ──
    {"id": 5, "name": "施志君", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-02", "birthplace": "四川合江", "education": "研究生/文学硕士",
     "party_join": "2003-10", "work_start": "2008-07",
     "current_post": "潼南区委常委、区纪委书记、区监委主任", "current_org": "中共重庆市潼南区纪律检查委员会",
     "source": "https://baike.baidu.com/item/%E6%96%BD%E5%BF%97%E5%90%9B/58957377"},

    # ── Executive Deputy District Mayor ──
    {"id": 6, "name": "曾伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-12", "birthplace": "重庆潼南", "education": "重庆市委党校大学",
     "party_join": "2002-12", "work_start": "1998-12",
     "current_post": "潼南区委常委、区政府党组副书记、常务副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://baike.baidu.com/item/%E6%9B%BE%E4%BC%9F/5558817"},

    # ── Deputy District Mayor (also Xinjiang aid) ──
    {"id": 7, "name": "张超林", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-08", "birthplace": "四川平昌", "education": "研究生/历史学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "潼南区委常委、副区长（援疆任哈密市委副书记）", "current_org": "重庆市潼南区人民政府",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E8%B6%85%E6%9E%97/59879557"},

    # ── Deputy District Mayors ──
    {"id": 8, "name": "包庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "潼南区副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://www.cqtn.gov.cn/zwgk_184/ldjj/qzfld/wap.html"},

    {"id": 9, "name": "罗全良", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "潼南区副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://www.cqtn.gov.cn/zwgk_184/ldjj/qzfld/wap.html"},

    {"id": 10, "name": "秦云兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "潼南区副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://www.cqtn.gov.cn/zwgk_184/ldjj/qzfld/wap.html"},

    {"id": 11, "name": "廖世祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "潼南区副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://www.cqtn.gov.cn/zwgk_184/ldjj/qzfld/wap.html"},

    {"id": 12, "name": "杨述兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "潼南区副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://www.cqtn.gov.cn/zwgk_184/ldjj/qzfld/wap.html"},

    {"id": 13, "name": "徐燕", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "潼南区副区长", "current_org": "重庆市潼南区人民政府",
     "source": "https://www.cqtn.gov.cn/zwgk_184/ldjj/qzfld/wap.html"},

    # ── Predecessors ──
    {"id": 14, "name": "文天平", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "湖南东安", "education": "研究生/理学硕士",
     "party_join": "中共党员", "work_start": "1997-10",
     "current_post": "新疆维吾尔自治区吐鲁番市委书记", "current_org": "中共吐鲁番市委员会",
     "source": "https://baike.baidu.com/item/%E6%96%87%E5%A4%A9%E5%B9%B3"},
]

organizations = [
    {"id": 1, "name": "中共重庆市潼南区委员会", "type": "党委", "level": "地市级", "parent": "中共重庆市委", "location": "重庆市潼南区"},
    {"id": 2, "name": "重庆市潼南区人民政府", "type": "政府", "level": "地市级", "parent": "重庆市人民政府", "location": "重庆市潼南区"},
    {"id": 3, "name": "重庆市潼南区人大常委会", "type": "人大", "level": "地市级", "parent": "重庆市人大常委会", "location": "重庆市潼南区"},
    {"id": 4, "name": "中国人民政治协商会议重庆市潼南区委员会", "type": "政协", "level": "地市级", "parent": "重庆市政协", "location": "重庆市潼南区"},
    {"id": 5, "name": "中共重庆市潼南区纪律检查委员会", "type": "党委", "level": "地市级", "parent": "中共重庆市纪委", "location": "重庆市潼南区"},
    {"id": 6, "name": "中共资阳市委", "type": "党委", "level": "地市级", "parent": "中共四川省委", "location": "四川省资阳市"},
    {"id": 7, "name": "中共绵阳市委", "type": "党委", "level": "地市级", "parent": "中共四川省委", "location": "四川省绵阳市"},
    {"id": 8, "name": "绵阳市人民政府", "type": "政府", "level": "地市级", "parent": "四川省人民政府", "location": "四川省绵阳市"},
    {"id": 9, "name": "中共吐鲁番市委员会", "type": "党委", "level": "地市级", "parent": "中共新疆维吾尔自治区委", "location": "新疆吐鲁番市"},
    {"id": 10, "name": "中共石柱土家族自治县委", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市石柱县"},
    {"id": 11, "name": "酉阳土家族苗族自治县人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市酉阳县"},
    {"id": 12, "name": "中共武隆县委", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市武隆区"},
    {"id": 13, "name": "中共城口县委", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市城口县"},
    {"id": 14, "name": "中共铜梁县委", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市铜梁区"},
    {"id": 15, "name": "重庆市纪委监委", "type": "党委", "level": "省级", "parent": "中共重庆市纪委", "location": "重庆市"},
    {"id": 16, "name": "中共哈密市委", "type": "党委", "level": "地市级", "parent": "中共新疆维吾尔自治区委", "location": "新疆哈密市"},
]

positions = [
    # 元方
    {"id": 1, "person_id": 1, "org_id": 1, "title": "潼南区委书记", "start": "2025-09", "end": "present", "rank": "正厅级", "note": "跨省从四川资阳调任重庆潼南"},
    {"id": 2, "person_id": 1, "org_id": 6, "title": "资阳市委书记", "start": "2022-01", "end": "2025-09", "rank": "正厅级", "note": ""},
    {"id": 3, "person_id": 1, "org_id": 8, "title": "绵阳市市长", "start": "2019-02", "end": "2022-01", "rank": "正厅级", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 7, "title": "绵阳市委副书记", "start": "2018-07", "end": "2022-01", "rank": "副厅级", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 7, "title": "绵阳市委常委", "start": "2016-10", "end": "2018-07", "rank": "副厅级", "note": "兼市国资委党委书记"},
    {"id": 6, "person_id": 1, "org_id": 8, "title": "绵阳市副市长", "start": "2015-08", "end": "2016-10", "rank": "副厅级", "note": ""},
    # 元方早期：西安航天基地、中国新时代国际工程公司、西安军城集团

    # 李成群（前任区长，被查）
    {"id": 10, "person_id": 2, "org_id": 2, "title": "潼南区委副书记、区长", "start": "2021-07", "end": "2024-01", "rank": "正厅级", "note": "2024年1月被查，12月双开"},
    {"id": 11, "person_id": 2, "org_id": 11, "title": "酉阳县委副书记、县长", "start": "2016-03", "end": "2021-06", "rank": "正厅级", "note": ""},
    {"id": 12, "person_id": 2, "org_id": 12, "title": "武隆县委副书记", "start": "2015-09", "end": "2016-02", "rank": "副厅级", "note": ""},
    {"id": 13, "person_id": 2, "org_id": 12, "title": "武隆县委常委、常务副县长", "start": "2011-02", "end": "2015-09", "rank": "副厅级", "note": ""},
    {"id": 14, "person_id": 2, "org_id": 10, "title": "石柱县委常委、副县长", "start": "2007-02", "end": "2010-01", "rank": "副厅级", "note": ""},

    # 张彬
    {"id": 20, "person_id": 3, "org_id": 3, "title": "潼南区人大常委会主任", "start": "2025-01", "end": "present", "rank": "正厅级", "note": ""},
    {"id": 21, "person_id": 3, "org_id": 4, "title": "潼南区政协主席", "start": "2015-06", "end": "2025-01", "rank": "正厅级", "note": "潼南县政协主席2010-2015，撤县设区续任"},
    {"id": 22, "person_id": 3, "org_id": 2, "title": "潼南县委常委、常务副县长", "start": "2007-02", "end": "2009-11", "rank": "副厅级", "note": ""},
    {"id": 23, "person_id": 3, "org_id": 1, "title": "潼南县委常委、办公室主任", "start": "2003-02", "end": "2007-02", "rank": "副厅级", "note": ""},

    # 欧汉东
    {"id": 30, "person_id": 4, "org_id": 4, "title": "潼南区政协党组书记、主席", "start": "2024-10", "end": "present", "rank": "正厅级", "note": ""},
    {"id": 31, "person_id": 4, "org_id": 14, "title": "铜梁县太平镇党委书记", "start": "2001-10", "end": "2004-06", "rank": "正科级", "note": "兼人大主席"},

    # 施志君
    {"id": 40, "person_id": 5, "org_id": 5, "title": "潼南区委常委、区纪委书记、区监委主任", "start": "2025-07", "end": "present", "rank": "副厅级", "note": "2025年3月任代主任，7月当选"},
    {"id": 41, "person_id": 5, "org_id": 13, "title": "城口县委常委、县纪委书记、县监委主任", "start": "2021-09", "end": "2025-03", "rank": "副厅级", "note": ""},
    {"id": 42, "person_id": 5, "org_id": 15, "title": "重庆市纪委监委组织部副部长", "start": "2018-09", "end": "2021-09", "rank": "正处级", "note": ""},
    {"id": 43, "person_id": 5, "org_id": 15, "title": "重庆市纪委研究室副主任科员/副处级", "start": "2015-04", "end": "2018-09", "rank": "副处级", "note": ""},

    # 曾伟
    {"id": 50, "person_id": 6, "org_id": 2, "title": "潼南区委常委、常务副区长", "start": "2021-12", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 51, "person_id": 6, "org_id": 2, "title": "潼南区副区长", "start": "2019-08", "end": "2021-12", "rank": "副厅级", "note": ""},
    {"id": 52, "person_id": 6, "org_id": 1, "title": "潼南区委办公室主任", "start": "2016-11", "end": "2019-08", "rank": "正处级", "note": ""},

    # 张超林
    {"id": 60, "person_id": 7, "org_id": 2, "title": "潼南区委常委、副区长", "start": "2024-06", "end": "present", "rank": "副厅级", "note": "援疆任哈密市委副书记"},
    {"id": 61, "person_id": 7, "org_id": 16, "title": "哈密市委副书记（援疆）", "start": "2024", "end": "present", "rank": "副厅级", "note": "重庆市对口支援新疆前方指挥部指挥长"},
    {"id": 62, "person_id": 7, "org_id": 2, "title": "南岸区副区长", "start": "", "end": "2024-06", "rank": "副厅级", "note": ""},

    # 包庆等副区长
    {"id": 70, "person_id": 8, "org_id": 2, "title": "潼南区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 71, "person_id": 9, "org_id": 2, "title": "潼南区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 72, "person_id": 10, "org_id": 2, "title": "潼南区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 73, "person_id": 11, "org_id": 2, "title": "潼南区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 74, "person_id": 12, "org_id": 2, "title": "潼南区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"id": 75, "person_id": 13, "org_id": 2, "title": "潼南区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 文天平（前任区委书记）
    {"id": 80, "person_id": 14, "org_id": 9, "title": "吐鲁番市委书记", "start": "2025-09", "end": "present", "rank": "正厅级", "note": "跨省调任"},
    {"id": 81, "person_id": 14, "org_id": 1, "title": "潼南区委书记", "start": "2023-03", "end": "2025-09", "rank": "正厅级", "note": ""},
    {"id": 82, "person_id": 14, "org_id": 15, "title": "重庆市委网信办主任", "start": "2019", "end": "2023-03", "rank": "正厅级", "note": ""},
    {"id": 83, "person_id": 14, "org_id": 15, "title": "重庆市委政法委副书记", "start": "2014-02", "end": "2018-01", "rank": "正厅级", "note": ""},
]

relationships = [
    # 元方 ← predecessor → 文天平（前后任区委书记）
    {"id": 1, "person_a": 1, "person_b": 14, "type": "predecessor_successor", "context": "元方接替文天平任潼南区委书记", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2025-09"},

    # 元方 — 曾伟（上下级，区委书记和常务副区长）
    {"id": 2, "person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "元方作为区委书记，曾伟作为区委常委、常务副区长，为直接上下级", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2025-09至今"},

    # 元方 — 施志君（上下级）
    {"id": 3, "person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "元方为区委书记，施志君为区委常委、纪委书记", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2025-07至今"},

    # 元方 — 张超林（上下级）
    {"id": 4, "person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "元方为区委书记，张超林为区委常委", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2025-09至今"},

    # 文天平 — 李成群（潼南搭档）
    {"id": 5, "person_a": 14, "person_b": 2, "type": "overlap", "context": "文天平任潼南区委书记期间，李成群任区长", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2023-03至2024-01"},

    # 张彬 — 曾伟（均长期在潼南工作）
    {"id": 6, "person_a": 3, "person_b": 6, "type": "overlap", "context": "张彬和曾伟均在潼南县/区长期工作，有数十年共事经历", "overlap_org": "重庆市潼南区", "overlap_period": "2000-2025"},

    # 李成群 — 张彬（曾在潼南班子共事）
    {"id": 7, "person_a": 2, "person_b": 3, "type": "overlap", "context": "李成群任区长期间，张彬任区政协主席", "overlap_org": "重庆市潼南区", "overlap_period": "2021-2024"},

    # 曾伟 — 施志君（区委常委）
    {"id": 8, "person_a": 6, "person_b": 5, "type": "overlap", "context": "同为潼南区委常委", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2025-07至今"},

    # 文天平 — 施志君（上下级短暂共事）
    {"id": 9, "person_a": 14, "person_b": 5, "type": "overlap", "context": "文天平任区委书记期间，施志君调入潼南", "overlap_org": "中共重庆市潼南区委员会", "overlap_period": "2025-03至2025-09"},
]


# ── BUILD DATABASE ──────────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"],
                   pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"],
                   r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database written: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} organizations, {len(positions)} positions, {len(relationships)} relationships")


# ── BUILD GEXF ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    if p["current_post"].startswith("潼南区委书记"):
        return "255,50,50"
    if "区长" in p["current_post"] and "副" not in p["current_post"]:
        return "50,100,255"
    if "纪委书记" in p["current_post"] or "监委" in p["current_post"]:
        return "255,165,0"
    if "人大" in p["current_post"] or "政协" in p["current_post"]:
        return "100,100,100"
    if "常务副" in p["current_post"]:
        return "50,100,255"
    if "副区长" in p["current_post"]:
        return "50,100,255"
    if "原" in p["current_post"]:
        return "150,150,150"
    return "100,100,100"

def org_color(o):
    mapping = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return mapping.get(o["type"], "200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 14)  # current and former party secretaries

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>潼南区领导班子工作关系网络</description>')
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

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("16.0" if p["id"] in (6, 5, 3, 4) else "12.0")
        role = p["current_post"][:20] if p["current_post"] else "other"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
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
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person → organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        note = esc(pos["note"]) if pos["note"] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{note}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person ↔ person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
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
    print(f"✅ GEXF written: {GEXF_PATH}")


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("\n=== Summary ===")
    print(f"Persons:       {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions:     {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("Done.")
