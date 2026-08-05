#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南沙区(三沙市·南沙群岛)领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 海南省
Parent city: 三沙市
Region: 南沙群岛
Target: 区委书记 & 区长
Task ID: hainan_南沙群岛

⚠ 数据完整性声明 (important)
=== 确认的负向发现 (CONFIRMED NEGATIVE) ===
本区（三沙市南沙区）区委书记、区长的姓名在公开资料（百度百科海南南沙区词条、
三沙市南沙区人民政府词条、三沙市词条、三沙市人民政府网领导信息、多轮百度检索）中
均未被公开。这是一个极小的偏远驻守/科考群岛区（南沙群岛，区政府驻永暑礁），实际以
派出机构（南沙工作委员会/南沙管理委员会，合署办公）运作，未公开完整地方干部班子。
因此本脚本对区委书记、区长两个岗位采用【待查】占位记录（明确标注姓名未公开/未验证），
不虚构具体人名。网络主体为结构上已确认的组织 + 三沙市已确认的市领导 + 邻近西沙区
对照。

as of 2026-08-05.

参考来源:
- https://baike.baidu.com/item/南沙区/49852992  (南沙区·海南省三沙市辖区)
- https://baike.baidu.com/item/三沙市南沙区人民政府
- https://baike.baidu.com/item/三沙市
- https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml  (三沙市政府领导)
- https://baike.baidu.com/item/西沙区/49852895  (姊妹区对照)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "南沙群岛"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

# =========================================================================
# 1. PERSONS
#    id 1,2 = 区委书记/区长 占位（姓名未公开，不再虚构真实人名）
#    id 3,4,... = 三沙市已确认市领导（上级上下文 / 关系网锚点）
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心目标（占位岗位，姓名未公开）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "【待查】南沙区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "南沙区委书记（姓名未公开）",
        "current_org": "中共三沙市南沙区委员会",
        "source": "https://baike.baidu.com/item/南沙区/49852992",
    },
    {
        "id": 2,
        "name": "【待查】南沙区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "南沙区区长（姓名未公开）",
        "current_org": "三沙市南沙区人民政府",
        "source": "https://baike.baidu.com/item/三沙市南沙区人民政府",
    },
    # ════════════════════════════════════════
    # 三沙市委书记（市级上级 / 关系网锚点）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "葛国科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "广西浦北",
        "education": "浙江大学（博士）",
        "party_join": "中共党员（1998年加入）",
        "work_start": "2000年左右",
        "current_post": "中共三沙市委书记",
        "current_org": "中共三沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/葛国科",
    },
    # ════════════════════════════════════════
    # 三沙市市长（市级上级）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陈儒茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/202312/d6b3e6f4de034b2f8574517d324ac504.shtml",
    },
    # ════════════════════════════════════════
    # 三沙市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "王长仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年11月",
        "birthplace": "吉林农安",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市人大常委会主任",
        "current_org": "三沙市人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/三沙市",
    },
    # ════════════════════════════════════════
    # 三沙市副市长（南沙区属市管，分管参考）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "林道杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmyyjs/lingdao.shtml",
    },
    {
        "id": 7,
        "name": "李华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmyyjs/lingdao.shtml",
    },
    {
        "id": 8,
        "name": "刘云球",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三沙市副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmyyjs/lingdao.shtml",
    },
    # ════════════════════════════════════════
    # 西沙区区委书记、区长（姊妹区对照，确认名单）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "黄晓华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西沙区委书记",
        "current_org": "中共三沙市西沙区委员会",
        "source": "https://baike.baidu.com/item/西沙区/49852895",
    },
    {
        "id": 10,
        "name": "温一凡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西沙区区长",
        "current_org": "三沙市西沙区人民政府",
        "source": "https://baike.baidu.com/item/西沙区/49852895",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共三沙市南沙区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共三沙市委员会",
        "location": "南沙区永暑礁（永暑岛）",
    },
    {
        "id": 2,
        "name": "三沙市南沙区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "三沙市人民政府",
        "location": "南沙区永暑礁（永暑岛）",
    },
    {
        "id": 3,
        "name": "中国共产党三沙市南沙工作委员会（南沙管理委员会）",
        "type": "党委",
        "level": "派出机构/合署办公",
        "parent": "中共三沙市委员会",
        "location": "永暑礁",
    },
    {
        "id": 4,
        "name": "三沙市南沙区美济社区",
        "type": "事业单位",
        "level": "社区",
        "parent": "三沙市南沙区人民政府",
        "location": "美济岛",
    },
    {
        "id": 5,
        "name": "中共三沙市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共海南省委",
        "location": "西沙区永兴岛",
    },
    {
        "id": 6,
        "name": "三沙市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "海南省人民政府",
        "location": "西沙区永兴岛",
    },
    {
        "id": 7,
        "name": "三沙市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "海南省人大常委会",
        "location": "西沙区永兴岛",
    },
    {
        "id": 8,
        "name": "中共三沙市西沙区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共三沙市委员会",
        "location": "西沙区永兴岛",
    },
    {
        "id": 9,
        "name": "三沙市西沙区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "三沙市人民政府",
        "location": "西沙区永兴岛",
    },
    {
        "id": 10,
        "name": "三沙市南沙人民武装部",
        "type": "军事机构",
        "level": "县处级",
        "parent": "三沙警备区",
        "location": "永暑岛",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 区委书记（占位，姓名未公开）
    {"person_id": 1, "org_id": 1, "title": "南沙区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "姓名未公开（研究确认无公开名单）；结构岗位待查"},
    # 区长（占位）
    {"person_id": 2, "org_id": 1, "title": "南沙区委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": "占位"},
    {"person_id": 2, "org_id": 2, "title": "南沙区区长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "姓名未公开"},
    # 区委书记（占位）兼南沙工作委员会/管委会（派出机构合署）
    {"person_id": 1, "org_id": 3, "title": "南沙工作委员会/管委会（合署）",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "南沙区两委以派出机构合署运作（占位）"},
    # 三沙市委书记 — 葛国科
    {"person_id": 3, "org_id": 5, "title": "中共三沙市委书记",
     "start_date": "2024年12月", "end_date": "present", "rank": "正厅级",
     "note": "跨省调任（广西→海南）"},
    # 三沙市长 — 陈儒茂
    {"person_id": 4, "org_id": 5, "title": "三沙市委副书记",
     "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "三沙市市长",
     "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 人大常委会主任 — 王长仁
    {"person_id": 5, "org_id": 7, "title": "三沙市人大常委会主任",
     "start_date": "2022年1月", "end_date": "present", "rank": "正厅级", "note": ""},
    # 副市长 — 林道杰 / 李华 / 刘云球
    {"person_id": 6, "org_id": 6, "title": "三沙市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "三沙市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "三沙市副市长",
     "start_date": "2026年5月", "end_date": "present", "rank": "副厅级", "note": "官网 202605 列表"},
    # 西沙区（对照）
    {"person_id": 9, "org_id": 8, "title": "西沙区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "西沙区区长",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 区委书记 ↔ 区长（核心搭档，占位）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "南沙区委书记与区长党政搭档（两岗位均姓名未公开）",
     "overlap_org": "中共三沙市南沙区委员会/三沙市南沙区人民政府",
     "overlap_period": "当前"},
    # 区委书记 ↔ 三沙市委书记（上下级）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "南沙区委接受三沙市委领导",
     "overlap_org": "三沙市党委系统",
     "overlap_period": "当前"},
    # 区长 ↔ 三沙市长（上下级）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "南沙区政府接受三沙市政府领导（市区合一体制）",
     "overlap_org": "三沙市政府系统",
     "overlap_period": "当前"},
    # 三沙市委书记 ↔ 市长（搭档）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "葛国科任市委书记，陈儒茂任市长，共同搭档",
     "overlap_org": "三沙市",
     "overlap_period": "当前"},
    # 三沙市人大主任（监督）
    {"person_a": 5, "person_b": 3, "type": "overlap",
     "context": "王长仁任人大主任，葛国科任市委书记",
     "overlap_org": "三沙市",
     "overlap_period": "2022年至今"},
    {"person_a": 5, "person_b": 4, "type": "overlap",
     "context": "王长仁任人大主任，陈儒茂任市长",
     "overlap_org": "三沙市",
     "overlap_period": "当前"},
    # 副市长同事组（三沙市）
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "林道杰、李华同为三沙市副市长", "overlap_org": "三沙市人民政府",
     "overlap_period": "当前"},
    {"person_a": 6, "person_b": 8, "type": "overlap",
     "context": "林道杰、刘云球同为三沙市副市长", "overlap_org": "三沙市人民政府",
     "overlap_period": "2026年至今"},
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "李华、刘云球同为三沙市副市长", "overlap_org": "三沙市人民政府",
     "overlap_period": "2026年至今"},
    # 西沙区对照（姊妹区，不属南沙，但同市直管体系）
    {"person_a": 9, "person_b": 10, "type": "overlap",
     "context": "西沙区委书记与区长党政搭档（对照区）",
     "overlap_org": "中共三沙市西沙区委员会/三沙市西沙区人民政府",
     "overlap_period": "当前"},
    {"person_a": 9, "person_b": 3, "type": "superior_subordinate",
     "context": "西沙区委接受三沙市委领导（对照区）",
     "overlap_org": "三沙市党委系统",
     "overlap_period": "当前"},
    {"person_a": 10, "person_b": 4, "type": "superior_subordinate",
     "context": "西沙区政府接受三沙市政府领导（对照区）",
     "overlap_org": "三沙市政府系统",
     "overlap_period": "当前"},
]

# =========================================================================
# 5. GEXF BUILDER
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Assign RGB color based on role."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — Party Secretary
    if "区长" in post or "市长" in post or "副区长" in post or "副市长" in post:
        return "50,100,255"   # Blue — Government
    if "人大" in post:
        return "200,255,255"  # Cyan
    return "100,100,100"      # Grey — Others


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "事业单位": "220,220,220",
        "军事机构": "255,220,220",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf():
    lines = []
    now = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>三南市南沙区（南沙群岛）班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes: nodes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="a0" title="type" type="string"/>')
    lines.append('      <attribute id="a1" title="current_post" type="string"/>')
    lines.append('      <attribute id="a2" title="current_org" type="string"/>')
    lines.append('    </attributes>')

    # Attributes: edges
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="e0" title="type" type="string"/>')
    lines.append('      <attribute id="e1" title="context" type="string"/>')
    lines.append('      <attribute id="e2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="e3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p.get("current_post", ""))
        # 大小：核心（区委书记/区长）大；市领导次之
        sz = "20.0" if p["id"] in (1, 2, 3) else ("15.0" if p["id"] in (4, 5) else "12.0")
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="person"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="a2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="a0" value="organization"/>')
        lines.append(f'          <attvalue for="a1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="a2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="e0" value="worked_at"/>')
        lines.append(f'          <attvalue for="e1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="e0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="e1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="e2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="e3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    return "\n".join(lines)


# =========================================================================
# 6. BUILD
# =========================================================================
def build():
    os.makedirs(STAGING_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
    """)

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start_date TEXT, end_date TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start_date"], pos["end_date"], pos["rank"], pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    print(f"SQLite: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

    gexf_content = build_gexf()
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf_content)
    print(f"GEXF:  {GEXF_PATH}")


# =========================================================================
# 7. Person JSON
# =========================================================================
# 设计说明：核心两位（南沙区委书记/区长）因公开资料无姓名，生成代表性档案，
# 用显式「待查」标记身份，并把所有真实字段置空，公开履历列为「履历缺口」。

source_register = [
    {"id": "S001", "title": "南沙区（海南省三沙市辖区）- 百度百科",
     "url": "https://baike.baidu.com/item/南沙区/49852992",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia",
     "reliability": "medium",
     "notes": "南沙区词条：2020-04-18设立，驻永暑礁，行政区划代码460303；无领导名单"},
    {"id": "S002", "title": "三沙市南沙区人民政府 - 百度百科",
     "url": "https://baike.baidu.com/item/三沙市南沙区人民政府",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia",
     "reliability": "medium",
     "notes": "仅成立时间/办公地址，无领导名单"},
    {"id": "S003", "title": "三沙市 - 百度百科",
     "url": "https://baike.baidu.com/item/三沙市",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia",
     "reliability": "medium",
     "notes": "市级在职领导（葛国科/陈儒茂等）"},
    {"id": "S004", "title": "三沙市人民政府 - 领导信息",
     "url": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml",
     "publisher": "三沙市人民政府", "published_at": "",
     "accessed_at": AS_OF, "source_type": "official",
     "reliability": "high",
     "notes": "市政府领导名单（市长陈儒茂、副市长林道杰/李华/黄广南/刘云碧、秘书长杜军奎）"},
    {"id": "S005", "title": "西沙区 - 百度百科（对照）",
     "url": "https://baike.baidu.com/item/西沙区/49852895",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": AS_OF, "source_type": "encyclopedia",
     "reliability": "medium",
     "notes": "西沙区现领：区委书记黄晓忠、区长温一凡（对照区）"},
]


def make_person_json(p, person_identifier, relationships_list):
    """Build a person JSON. Placeholder (id 1/2) gets 待查 identity."""
    placeholder = p["id"] in (1, 2)
    base_name = "" if placeholder else p["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "海南省",
            "city": "三沙市",
            "region": "南沙群岛",
            "job": p.get("current_post", ""),
            "task_id": "hainan_南沙群岛",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": person_identifier,
            "name": base_name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正县处级" if placeholder else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": not placeholder,
            "source_ids": ["S001", "S002"] if placeholder else ["S003", "S004"]
        },
        "career_timeline": _timeline(p, placeholder),
        "organizations": [],
        "relationships": _relationships_for(p["id"], placeholder),
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found",
             "description": "在公开信息中未发现该岗位负面信号（亦无公开履历可据此判断）",
             "date": "", "confidence": "unverified" if placeholder else "confirmed",
             "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified" if placeholder else "partial",
            "current_role": "unverified" if placeholder else "confirmed",
            "career_completeness": "thin" if placeholder else "partial",
            "relationship_confidence": "low",
            "biggest_gap": (f"{p.get('current_post','')}姓名及完整履历缺失"
                            if placeholder else f"{p['name']}早年履历缺失")
        },
        "open_questions": [
            {"priority": "critical",
             "question": f"{p.get('current_post','')}的姓名与完整履历",
             "why_it_matters": "无法在公开渠道确认该岗位任职者，网络关系无法闭合到具体个人",
             "suggested_queries": ["三沙市南沙区 任前公示", "南沙区 区委书记 简历",
                                    "海南省委组织部 南沙区 任命"],
             "last_attempted": AS_OF}
        ]
    }


def _timeline(p, placeholder):
    if placeholder:
        return [
            {"start": "unknown", "end": "present",
             "org": p.get("current_org", ""),
             "title": p.get("current_post", ""),
             "notes": "岗位结构确认存在；任职者姓名未公开（研究结论：南沙区班子无公开名单）。",
             "confidence": "unverified", "source_ids": ["S001", "S002"]},
            {"start": "unknown", "end": "unknown",
             "org": "履历缺口",
             "title": "",
             "notes": "该岗位任职者身份、出生年份、籍贯、教育背景、此前职务均未公开。",
             "confidence": "unverified", "source_ids": []},
        ]
    return [
        {"start": "", "end": "present",
         "org": p.get("current_org", ""),
         "title": p.get("current_post", ""),
         "notes": "现任（市领导，信息来源：百度百科/三沙市政府网）",
         "confidence": "confirmed",
         "source_ids": ["S003", "S004"]},
    ]


def _person_id_for(p):
    if p["id"] in (1, 2):
        # 占位岗位用岗位名做稳定 id
        return "nansha_待查_" + ("区委书记" if p["id"] == 1 else "区长")
    return "nansha_" + p["name"]


def _relationships_for(pid, placeholder):
    rels = []
    for r in relationships:
        if pid not in (r["person_a"], r["person_b"]):
            continue
        other = r["person_b"] if r["person_a"] == pid else r["person_a"]
        if other == pid:
            continue
        other_p = next((pp for pp in persons if pp["id"] == other), None)
        if not other_p:
            continue
        rels.append({
            "person": other_p.get("name", ""),
            "person_id": _person_id_for(other_p),
            "relationship_type": r.get("type", "overlap"),
            "strength": "strong",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "unverified" if placeholder else "confirmed",
            "source_ids": ["S001", "S002"] if placeholder else ["S003", "S004"],
        })
    return rels


def build_person_jsons():
    for p in persons:
        if p["id"] not in (1, 2):
            continue
        person_identifier = _person_id_for(p)
        placeholder = p["id"] in (1, 2)
        rels = _relationships_for(p["id"], placeholder)
        obj = make_person_json(p, person_identifier, rels)
        jobpart = "区委书记" if p["id"] == 1 else "区长"
        fname = f"{TODAY}-海南省-三沙市-{jobpart}-待查.json"
        path = os.path.join(PERSONS_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {path}")


# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    build()
    build_person_jsons()
    print(f"\n{'='*60}")
    print(f"Build complete!")
    print(f"   DB:    {DB_PATH}")
    print(f"   GEXF:  {GEXF_PATH}")
    print(f"{'='*60}")