#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Tibet cross-province cadre transfers.

调查日期: 2026-07-28
信息来源: Wikipedia (英文/中文), Xinhua, The Paper, sina.com
调查级别: 自治区 (省级)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(REPO_ROOT, "data", "database", "tibet_cross_province_transfers_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", "tibet_cross_province_transfers_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")
SLUG = "西藏自治区跨省干部交流网络"

# ══════════════════════════════════════════════════════════════════════
# PERSONS — Senior leaders of Tibet and their cross-province career paths
# ══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current leadership ──
    {
        "id": 1,
        "name": "王君正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-05-17",
        "birthplace": "山东临沂",
        "education": "山东大学、清华大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西藏自治区党委书记",
        "current_org": "西藏自治区委员会",
        "source": "https://en.wikipedia.org/wiki/Wang_Junzheng",
        "province_in": "新疆→西藏",  # cross-province note
        "province_out": "（现任）",
    },
    {
        "id": 2,
        "name": "嘎玛泽登",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1967-12",
        "birthplace": "西藏江达县",
        "education": "中央民族大学、中央党校",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西藏自治区政府主席",
        "current_org": "西藏自治区人民政府",
        "source": "https://en.wikipedia.org/wiki/Garma_Cedain",
        "language_in": "西藏本地提拔",
        "language_out": "（现任）",
    },
    {
        "id": 3,
        "name": "严金海",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1962-03",
        "birthplace": "青海民和回族土族自治",
        "education": "青海民族大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西藏自治区人大主任",
        "current_org": "西藏自治区人大常委会",
        "source": "https://en.wikipedia.org/wiki/Yan_Jinhai",
        "language_in": "青海→西藏",
        "language_out": "西藏人大主任",
    },
    # ── Historical Party Secretaries (Han, sent from outside) ──
    {
        "id": 4,
        "name": "吴英杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1956-12",
        "birthplace": "山东昌邑",
        "education": "西藏民族大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前西藏自治区党委书记，已落马）",
        "current_org": "（被开除党籍）",
        "source": "https://en.wikipedia.org/wiki/Wu_Yingjie",
        "language_in": "lifetime Tibet career（例外）",
        "language_out": "→全国政协→2024被捕，死缓",
    },
    {
        "id": 5,
        "name": "陈全国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1955-11",
        "birthplace": "河南平舆",
        "education": "郑州大学、武汉理工大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（退休）",
        "current_org": "中央农村工作领导小组",
        "source": "https://en.wikipedia.org/wiki/Chen_Quanguo",
        "language_in": "河南→河北→西藏",
        "language_out": "西藏→新疆党委书记",
    },
    {
        "id": 6,
        "name": "张庆黎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1951",
        "birthplace": "山东东平",
        "education": "",
        "current_post": "（退休）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Party_Secretary_of_Tibet",
        "language_in": "山东→?→西藏",
        "language_out": "西藏→河北/黑龙江",
    },
    {
        "id": 7,
        "name": "杨传堂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1954",
        "birthplace": "山东？？",
        "education": "",
        "current_post": "（退休）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Party_Secretary_of_Tibet",
        "language_in": "山东→?→西藏",
        "language_out": "西藏→供销总社",
    },
    {
        "id": 8,
        "name": "郭金龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1947",
        "birthplace": "江苏南京",
        "education": "",
        "current_post": "（退休）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Party_Secretary_of_Tibet",
        "language_in": "江苏→西藏",
        "language_out": "西藏→北京市长→市委书记",
    },
    {
        "id": 9,
        "name": "陈奎元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1941",
        "birthplace": "辽宁康平",
        "education": "",
        "current_post": "（退休）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Party_Secretary_of_Tibet",
        "language_in": "河南→中央→西藏",
        "language_out": "西藏→中国社科院",
    },
    {
        "id": 10,
        "name": "胡锦涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1942-12",
        "birthplace": "安徽绩溪",
        "education": "清华大学",
        "current_post": "（退休—前党和国家领导人）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Party_Secretary_of_Tibet",
        "language_in": "共青团中央→贵州→西藏",
        "language_out": "西藏→贵州书记→北京→国家领导人",
    },
    # ── Historical Government Chairpersons (Tibetan ethnicity) ──
    {
        "id": 11,
        "name": "齐扎拉",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1958-08",
        "birthplace": "云南中甸（香格里拉）",
        "education": "云南民族大学、中央党校",
        "current_post": "（2025年被查，2026年判无期）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Che_Dalha",
        "language_in": "云南→西藏",
        "language_out": "西藏→全国政协→落马",
    },
    {
        "id": 12,
        "name": "洛桑江村",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1957-07",
        "birthplace": "西藏察雅县",
        "education": "西藏民族学院、中央党校",
        "current_post": "全国人大常委会副委员长",
        "current_org": "全国人大",
        "source": "https://en.wikipedia.org/wiki/Losang_Jamcan",
        "language_in": "西藏本地提拔",
        "language_out": "西藏→全国人大副委员长",
    },
    # ── Deputy Secretaries and other key figures ──
    {
        "id": 13,
        "name": "帕巴拉格列朗杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1940",
        "birthplace": "四川省理塘",
        "education": "",
        "current_post": "全国政协副主席、西藏政协主席",
        "current_org": "全国政协/西藏政协",
        "source": "",
        "language_in": "",
        "language_out": "",
    },
]

# ══════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "西藏自治区委员会", "type": "党委", "level": "自治区", "parent": "", "location": "西藏拉"},
    {"id": 2, "name": "西藏自治区人民政府", "type": "政府", "level": "自治区", "parent": "", "location": "西藏拉"},
    {"id": 3, "name": "西藏自治区人大常委会", "type": "人大", "level": "自治区", "parent": "", "location": "西藏拉"},
    {"id": 4, "name": "中国共产党新疆维子自治区委员会", "type": "党委", "level": "自治区", "parent": "", "location": "新疆乌鲁木齐"},
    {"id": 5, "name": "中国共产党河北省委员会", "type": "党委", "level": "省", "parent": "", "location": "河北石家庄"},
    {"id": 6, "name": "全国政协", "type": "其他", "level": "中央", "parent": "", "location": "北京"},
    {"id": 7, "name": "全国人大", "type": "其他", "level": "中央", "parent": "", "location": "北京"},
    {"id": 8, "name": "中国社科院", "type": "事业单位", "level": "中央", "parent": "", "location": "北京"},
    {"id": 9, "name": "北京市政府", "type": "政府", "level": "直辖市", "parent": "", "location": "北京"},
    {"id": 10, "name": "中国共产党青海省委员会", "type": "党委", "level": "省", "parent": "", "location": "青海西宁"},
    {"id": 11, "name": "新疆生产建设兵团", "type": "特殊", "level": "自治区", "parent": "", "location": "新疆"},
    {"id": 12, "name": "中国共产党中央委员会农村工作领导小组", "type": "其他", "level": "中央", "parent": "", "location": "北京"},
]

# ══════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════

positions = [
    # Wang Junzheng
    {"person_id": 1, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "2021-10", "end_date": "", "rank": "正部级", "note": "From XPCC"},
    {"person_id": 1, "org_id": 11, "title": "新疆生产建设兵团党委书记", "start_date": "2020-5", "end_date": "2021-10", "rank": "正部级", "note": "前"},
    # Garma Cedain
    {"person_id": 2, "org_id": 2, "title": "西藏自治区政府主席", "start_date": "2024-11", "end_date": "", "rank": "正部级", "note": "现任"},
    # Yan Jinhai
    {"person_id": 3, "org_id": 3, "title": "西藏自治区人大常委会主任", "start_date": "2025-1", "end_date": "", "rank": "正部级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "西藏自治区政府主席", "start_date": "2021-10", "end_date": "2024-11", "rank": "正部级", "note": "前任"},
    {"person_id": 3, "org_id": 10, "title": "青海省副省长", "start_date": "2013-1", "end_date": "2020-7", "rank": "副部级", "note": "青海-西藏走廊"},
    # Wu Yingjie
    {"person_id": 4, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "2016-8", "end_date": "2021-10", "rank": "正部级", "note": "例外：终身藏干部"},
    {"person_id": 4, "org_id": 6, "title": "全国政协文化文史和学习委员会主任", "start_date": "2021-10", "end_date": "2024-6", "rank": "正部级", "note": ""},
    # Chen Quanguo
    {"person_id": 5, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "2011-8", "end_date": "2016-8", "rank": "正部级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "新疆维子自治区党委书记", "start_date": "2016-8", "end_date": "2021-12", "rank": "正部级", "note": "唯一执掌西藏和新疆的人"},
    {"person_id": 5, "org_id": 12, "title": "中央农村工作领导小组副Group长", "start_date": "2022", "end_date": "", "rank": "正部级", "note": ""},
    # Zhang Qingli
    {"person_id": 6, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "2006-5", "end_date": "2011-8", "rank": "正部级", "note": ""},
    # Yang Chuantang
    {"person_id": 7, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "2004-12", "end_date": "2006-5", "rank": "正部级", "note": ""},
    # Guo Jinlong
    {"person_id": 8, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "2000-10", "end_date": "2004-12", "rank": "正部级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "北京市市长", "start_date": "2005", "end_date": "2007", "rank": "正部级", "note": "西藏后提拔"},
    {"person_id": 8, "org_id": 9, "title": "北京市委书记", "start_date": "2007", "end_date": "2012", "rank": "副国级", "note": ""},
    # Chen Kuiyuan
    {"person_id": 9, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "1992-12", "end_date": "2000-10", "rank": "正部级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "中国社科院院长", "start_date": "2000", "end_date": "2005", "rank": "正部级", "note": ""},
    # Hu Jintao
    {"person_id": 10, "org_id": 1, "title": "西藏自治区党委书记", "start_date": "1988-12", "end_date": "1992-12", "rank": "正部级", "note": ""},
    # Che Dalha
    {"person_id": 11, "org_id": 2, "title": "西藏自治区主席", "start_date": "2017-1", "end_date": "2021-10", "rank": "正部级", "note": "云南藏族"},
    # Losang Jamcan
    {"person_id": 12, "org_id": 2, "title": "西藏自治区主席", "start_date": "2013-1", "end_date": "2017-1", "rank": "正部级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "全国人大常委会副委员长", "start_date": "2023-3", "end_date": "", "rank": "副国级", "note": "西藏→国家领导人"},
]

# ══════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════

relationships = [
    # Wang Junzheng & Yan Jinhai — worked together 2021-2024
    {"person_a": 1, "person_b": 3, "type": "工作关系", "context": "王君正（党委书记）+严金海（主席）搭档", "overlap_org": "西藏自治区", "overlap_period": "2021-10至2024-11"},
    # Wang Junzheng & Garma Cedain — current leadership
    {"person_a": 1, "person_b": 2, "type": "工作关系", "context": "王君正（党委书记）+嘎玛泽登（主席）现任搭档", "overlap_org": "西藏自治区", "overlap_period": "2024-11至今"},
    # Chen Quanguo & Wu Yingjie — succession
    {"person_a": 5, "person_b": 4, "type": "前任-后任", "context": "陈全国交班吴英杰任西藏党委书记", "overlap_org": "西藏自治区", "overlap_period": "2016"},
    # Wu Yingjie & Wang Junzheng — succession
    {"person_a": 4, "person_b": 1, "type": "前任-后任", "context": "吴英杰交班→王君正接任", "overlap_org": "西藏自治区", "overlap_period": "2021"},
    # Chen Quanguo & Losang Jamcan — worked together
    {"person_a": 5, "person_b": 12, "type": "工作关系", "context": "陈全国（党委书记）+洛桑江村（主席）搭档", "overlap_org": "西藏自治区", "overlap_period": "2013-2016"},
    # Yan Jinhai & Che Dalha — succession
    {"person_a": 3, "person_b": 11, "type": "前任-后任", "context": "齐扎拉→严金海接任主席", "overlap_org": "西藏政府", "overlap_period": "2021"},
    # Hu Jintao & Chen Kuiyuan — succession
    {"person_a": 10, "person_b": 9, "type": "前任-后任", "context": "胡锦涛→陈奎元接任书记", "overlap_org": "西藏党委", "overlap_period": "1992"},
    # Chen Quanguo — key unique transfer Tibet↔Xinjiang
    {"person_a": 5, "person_b": 1, "type": "跨区相似路径", "context": "两人都先后在新疆和西藏担任主要领导职务", "overlap_period": ""},
    # Yan Jinhai & Che Dalha — both ethnic Tibetan from outside TAR
    {"person_a": 3, "person_b": 11, "type": "共同特点", "context": "都出生在藏区但不在西藏自治区内（青海/云南）来西藏任职主席", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "党委书记" in post or "党委书记" in post:
        return ("255,50,50", 20.0)
    elif "政府主席" in post or "主席" in post:
        return ("50, 179, 255", 20.0)
    elif "人大主任" in post or "人大常委会" in post:
        return ("50, 205, 50", 15.0)
    elif "全国政协" in post or "副委员长" in post:
        return ("255, 215, 0", 18.0)
    elif "落马" in post or "被开除" in post:
        return ("120, 120, 120", 12.0)
    elif "退休" in post:
        return ("160, 160, 160", 10.0)
    else:
        return ("128, 128, 128", 12.0)

def build():
    print("=" * 60)
    print(f"  {SLUG}")
    print(f"  调查日期: {TODAY}")
    print("=" * 60)

    # Build DB
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT '',
            language_in TEXT DEFAULT '',
            language_out TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_a INTEGER NOT NULL,
            persona_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (persona_a) REFERENCES persons(id),
            FOREIGN KEY (persona_b) REFERENCES persons(id)
        );
    """)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT OR REPLACE INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT OR REPLACE INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for p in positions:
        vals = [p.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # Build GEXF
    print("\n--- Building GEXF graph ---")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{datetime.now().strftime("%Y%m%d")}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG}</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '      <attribute id="5" title="language_in" type="string"/>',
        '      <attribute id="6" title="language_out" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("language_in",""))}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p.get("language_out",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0].strip()}" g="{c.split(",")[1].strip()}" b="{c.split(",")[2].strip()}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n  {SLUG} 构建完成。")

if __name__ == "__main__":
    build()
    main()
