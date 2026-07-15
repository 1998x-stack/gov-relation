#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 金溪县 (抚州市, 江西省) leadership network.

金溪县概况: 金溪县是江西省抚州市下辖的一个县，位于江西省东部，抚州市北部。
面积约1358平方公里，人口约34万。下辖8镇5乡、1个垦殖场。
金溪县素有"象山故里、江南书乡"之称，是南宋思想家陆九渊（象山先生）的故乡。
经济以香料香精产业闻名，是全国最大的天然香料生产基地之一，被誉为"华夏香都"。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_金溪县")
DB_PATH = os.path.join(STAGING, "金溪县_network.db")
GEXF_PATH = os.path.join(STAGING, "金溪县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ── Core Leader: County Party Secretary ──
    {
        "id": 1,
        "name": "熊晋喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委书记",
        "current_org": "中共金溪县委员会",
        "source": "金溪县人民政府网站领导之窗; 百度百科; 江西省委组织部任前公示"
    },

    # ── Core Leader: County Mayor ──
    {
        "id": 2,
        "name": "邹俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-09",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委副书记、县长",
        "current_org": "金溪县人民政府",
        "source": "金溪县人民政府网站领导之窗; 百度百科; 江西省委组织部任前公示"
    },

    # ── Predecessors ──
    {
        "id": 3,
        "name": "张文贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "江西临川",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委书记（前任）",
        "current_org": "中共金溪县委员会",
        "source": "百度百科; 人民网地方领导资料库"
    },
    {
        "id": 4,
        "name": "吴斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县长（前任）",
        "current_org": "金溪县人民政府",
        "source": "金溪县政府网站历史资料; 新闻报道"
    },

    # ── Standing Committee Members ──
    {
        "id": 5,
        "name": "杜蔚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委常委、常务副县长",
        "current_org": "金溪县人民政府",
        "source": "金溪县政府网站领导之窗"
    },
    {
        "id": 6,
        "name": "王建荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委常委、纪委书记、监委主任",
        "current_org": "中共金溪县纪律检查委员会",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 7,
        "name": "曾维东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委常委、组织部部长",
        "current_org": "中共金溪县委组织部",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 8,
        "name": "罗中原",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委常委、政法委书记",
        "current_org": "中共金溪县委政法委员会",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 9,
        "name": "江长青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委常委、宣传部部长",
        "current_org": "中共金溪县委宣传部",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 10,
        "name": "赖昌明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县人大常委会主任",
        "current_org": "金溪县人大常委会",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 11,
        "name": "张爱群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县政协主席",
        "current_org": "政协金溪县委员会",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 12,
        "name": "朱小荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县委统战部部长（原任职）",
        "current_org": "中共金溪县委统战部",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 13,
        "name": "谢赛赛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县领导（县人武部）",
        "current_org": "金溪县人民武装部",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 14,
        "name": "杨海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县副县长",
        "current_org": "金溪县人民政府",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 15,
        "name": "宋志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县副县长",
        "current_org": "金溪县人民政府",
        "source": "金溪县政府网站; 新闻报道"
    },
    {
        "id": 16,
        "name": "王茂柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "金溪县副县长",
        "current_org": "金溪县人民政府",
        "source": "金溪县政府网站; 新闻报道"
    },
]

organizations = [
    {"id": 1, "name": "中共金溪县委员会", "type": "党委", "level": "县处级", "parent": "中共抚州市委员会", "location": "江西省抚州市金溪县"},
    {"id": 2, "name": "金溪县人民政府", "type": "政府", "level": "县处级", "parent": "抚州市人民政府", "location": "江西省抚州市金溪县"},
    {"id": 3, "name": "中共金溪县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共抚州市纪律检查委员会", "location": "江西省抚州市金溪县"},
    {"id": 4, "name": "中共金溪县委组织部", "type": "党委", "level": "县处级", "parent": "中共金溪县委员会", "location": "江西省抚州市金溪县"},
    {"id": 5, "name": "中共金溪县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共金溪县委员会", "location": "江西省抚州市金溪县"},
    {"id": 6, "name": "中共金溪县委宣传部", "type": "党委", "level": "县处级", "parent": "中共金溪县委员会", "location": "江西省抚州市金溪县"},
    {"id": 7, "name": "金溪县人大常委会", "type": "人大", "level": "县处级", "parent": "抚州市人大常委会", "location": "江西省抚州市金溪县"},
    {"id": 8, "name": "政协金溪县委员会", "type": "政协", "level": "县处级", "parent": "政协抚州市委员会", "location": "江西省抚州市金溪县"},
    {"id": 9, "name": "中共金溪县委统战部", "type": "党委", "level": "县处级", "parent": "中共金溪县委员会", "location": "江西省抚州市金溪县"},
    {"id": 10, "name": "金溪县人民武装部", "type": "政府", "level": "县处级", "parent": "抚州市军分区", "location": "江西省抚州市金溪县"},
]

positions = [
    # 熊晋喜 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "金溪县委书记", "start": "2024-", "end": "present", "rank": "县处级正职", "note": "从德安县交流至金溪县任职县委书记"},

    # 邹俊 — 县长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "金溪县委副书记、县长", "start": "2021-", "end": "present", "rank": "县处级正职", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "金溪县委副书记", "start": "2021-", "end": "present", "rank": "县处级副职", "note": ""},

    # 张文贵 — 前任县委书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "金溪县委书记（前任）", "start": "2020-", "end": "2024-", "rank": "县处级正职", "note": "接替高连珠任县委书记，后由熊晋喜接替"},

    # 吴斌 — 前任县长
    {"id": 5, "person_id": 4, "org_id": 2, "title": "金溪县委副书记、县长（前任）", "start": "unknown", "end": "2021-", "rank": "县处级正职", "note": "前任县长，后由邹俊接替"},

    # 杜蔚 — 常务副县长
    {"id": 6, "person_id": 5, "org_id": 2, "title": "金溪县委常委、常务副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 王建荣 — 纪委书记
    {"id": 7, "person_id": 6, "org_id": 3, "title": "金溪县委常委、纪委书记、监委主任", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 6, "org_id": 1, "title": "金溪县委常委", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 曾维东 — 组织部长
    {"id": 9, "person_id": 7, "org_id": 4, "title": "金溪县委常委、组织部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 10, "person_id": 7, "org_id": 1, "title": "金溪县委常委", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 罗中原 — 政法委书记
    {"id": 11, "person_id": 8, "org_id": 5, "title": "金溪县委常委、政法委书记", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 12, "person_id": 8, "org_id": 1, "title": "金溪县委常委", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 江长青 — 宣传部长
    {"id": 13, "person_id": 9, "org_id": 6, "title": "金溪县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 14, "person_id": 9, "org_id": 1, "title": "金溪县委常委", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 赖昌明 — 人大主任
    {"id": 15, "person_id": 10, "org_id": 7, "title": "金溪县人大常委会主任", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},

    # 张爱群 — 政协主席
    {"id": 16, "person_id": 11, "org_id": 8, "title": "金溪县政协主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},

    # 朱小荣 — 统战部长
    {"id": 17, "person_id": 12, "org_id": 9, "title": "金溪县委统战部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 谢赛赛 — 县人武部
    {"id": 18, "person_id": 13, "org_id": 10, "title": "金溪县领导（县人武部）", "start": "unknown", "end": "present", "rank": "县处级", "note": ""},

    # 杨海波 — 副县长
    {"id": 19, "person_id": 14, "org_id": 2, "title": "金溪县副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 宋志华 — 副县长
    {"id": 20, "person_id": 15, "org_id": 2, "title": "金溪县副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # 王茂柱 — 副县长
    {"id": 21, "person_id": 16, "org_id": 2, "title": "金溪县副县长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    # 熊晋喜 ← predecessor_successor → 张文贵
    {"id": 1, "person_a_id": 1, "person_b_id": 3, "type": "predecessor_successor",
     "context": "熊晋喜接替张文贵任金溪县委书记", "overlap_org": "中共金溪县委员会",
     "overlap_period": "2024年交接"},

    # 熊晋喜 ← overlap → 邹俊 (as party secretary and mayor)
    {"id": 2, "person_a_id": 1, "person_b_id": 2, "type": "overlap",
     "context": "熊晋喜作为县委书记与县长邹俊共事", "overlap_org": "金溪县四套班子",
     "overlap_period": "2024年至今"},

    # 邹俊 ← predecessor_successor → 吴斌
    {"id": 3, "person_a_id": 2, "person_b_id": 4, "type": "predecessor_successor",
     "context": "邹俊接替吴斌任金溪县长", "overlap_org": "金溪县人民政府",
     "overlap_period": "2021年交接"},

    # 邹俊 ← overlap → 杜蔚 (mayor and executive deputy mayor)
    {"id": 4, "person_a_id": 2, "person_b_id": 5, "type": "overlap",
     "context": "邹俊作为县长与常务副县长杜蔚共事", "overlap_org": "金溪县人民政府",
     "overlap_period": "unknown至今"},

    # 邹俊 ← overlap → 王建荣 (mayor and discipline inspection)
    {"id": 5, "person_a_id": 2, "person_b_id": 6, "type": "overlap",
     "context": "邹俊作为县长与纪委书记王建荣在常委班子共事", "overlap_org": "中共金溪县委员会",
     "overlap_period": "unknown至今"},

    # 熊晋喜 ← overlap → 王建荣 (party secretary and discipline secretary)
    {"id": 6, "person_a_id": 1, "person_b_id": 6, "type": "overlap",
     "context": "熊晋喜作为县委书记与纪委书记王建荣在常委班子共事", "overlap_org": "中共金溪县委员会",
     "overlap_period": "2024年至今"},

    # 熊晋喜 ← overlap → 曾维东 (party secretary and organization)
    {"id": 7, "person_a_id": 1, "person_b_id": 7, "type": "overlap",
     "context": "熊晋喜作为县委书记与组织部部长曾维东在常委班子共事", "overlap_org": "中共金溪县委员会",
     "overlap_period": "2024年至今"},

    # 熊晋喜 ← overlap → 罗中原 (party secretary and political-legal)
    {"id": 8, "person_a_id": 1, "person_b_id": 8, "type": "overlap",
     "context": "熊晋喜作为县委书记与政法委书记罗中原在常委班子共事", "overlap_org": "中共金溪县委员会",
     "overlap_period": "2024年至今"},

    # 熊晋喜 ← overlap → 江长青 (party secretary and propaganda)
    {"id": 9, "person_a_id": 1, "person_b_id": 9, "type": "overlap",
     "context": "熊晋喜作为县委书记与宣传部长江长青在常委班子共事", "overlap_org": "中共金溪县委员会",
     "overlap_period": "2024年至今"},

    # 张文贵 ← predecessor_successor → 高连珠 (previous party secretary)
    {"id": 10, "person_a_id": 3, "person_b_id": 0, "type": "predecessor_successor",
     "context": "张文贵接替高连珠任金溪县委书记", "overlap_org": "中共金溪县委员会",
     "overlap_period": "2020年交接"},
]


# =========================================================================
# BUILD DATABASE
# =========================================================================

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE persons(
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()


# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "县委书记" in post:
        return "255,50,50"
    elif "县长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    current = p["current_post"]
    return "县委书记" in current or "县长" in current


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>金溪县领导班子工作关系网络 - 江西省抚州市金溪县</description>')
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
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
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
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        label = f"{pos['title']}"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"][:50]) if pos["note"] else ""}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship)
    for r in relationships:
        if r["person_a_id"] == 0 or r["person_b_id"] == 0:
            continue  # Skip placeholder relationships
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF nodes: {len(persons) + len(organizations)}")
    print(f"  GEXF edges: {eid}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("Building 金溪县 network data...")
    build_db()
    build_gexf()
    print(f"\nDone! Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
